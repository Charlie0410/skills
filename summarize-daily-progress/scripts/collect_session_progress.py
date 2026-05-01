from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any


ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
WHITESPACE_RE = re.compile(r"\s+")
NEXT_HINT_RE = re.compile(
    r"\b(next steps?|todo|follow[- ]?up|remaining|blocked?|blockers?|unknowns?|pending|still need)\b"
    r"|下一步|待办|阻塞|未知|后续|剩余",
    re.IGNORECASE,
)
SECRET_PATTERNS = [
    (
        re.compile(
            r"(?i)\b(api[_-]?key|secret|token|password|passwd|authorization)\b"
            r"\s*[:=]\s*['\"]?[^,\s'\"\])}]+"
        ),
        r"\1=[REDACTED]",
    ),
    (re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._\-+/=]{12,}"), "Bearer [REDACTED]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b"), "sk-[REDACTED]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"), "gh_[REDACTED]"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect compact progress evidence from Codex session JSONL files."
    )
    parser.add_argument(
        "--date",
        default="today",
        help="Local date directory to read, as YYYY-MM-DD or 'today'. Defaults to today.",
    )
    parser.add_argument(
        "--sessions-root",
        default=str(Path.home() / ".codex" / "sessions"),
        help="Root directory containing YYYY/MM/DD Codex session folders.",
    )
    parser.add_argument(
        "--max-chars-per-project",
        type=int,
        default=12000,
        help="Approximate character budget for text snippets per project.",
    )
    return parser.parse_args()


def selected_date(value: str) -> date:
    if value.lower() == "today":
        return date.today()
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise SystemExit("--date must be 'today' or YYYY-MM-DD") from exc


def date_dir(sessions_root: Path, day: date) -> Path:
    return sessions_root / f"{day:%Y}" / f"{day:%m}" / f"{day:%d}"


def redact(text: str) -> str:
    redacted = text
    for pattern, replacement in SECRET_PATTERNS:
        redacted = pattern.sub(replacement, redacted)
    return redacted


def clean_text(text: str, limit: int = 700) -> str:
    text = ANSI_RE.sub("", text)
    text = text.replace("\x00", "")
    text = WHITESPACE_RE.sub(" ", text).strip()
    text = redact(text)
    return truncate(text, limit)


def truncate(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    if limit <= 20:
        return text[:limit]
    return text[: limit - 15].rstrip() + " ...[truncated]"


def add_unique(items: list[str], text: str, max_items: int, limit: int = 700) -> None:
    cleaned = clean_text(text, limit)
    if not cleaned or cleaned in items:
        return
    if len(items) < max_items:
        items.append(cleaned)


def text_from_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, dict) and isinstance(item.get("text"), str):
            parts.append(item["text"])
    return "\n".join(parts)


def is_bootstrap_text(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    prefixes = (
        "# AGENTS.md instructions",
        "<environment_context>",
        "<INSTRUCTIONS>",
        "<permissions instructions>",
        "<collaboration_mode>",
        "<apps_instructions>",
        "<skills_instructions>",
        "<plugins_instructions>",
    )
    return stripped.startswith(prefixes)


def nearest_git_root(cwd: str | None) -> str:
    if not cwd:
        return "(unknown cwd)"
    path = Path(cwd).expanduser()
    try:
        path = path.resolve(strict=False)
    except OSError:
        pass
    candidates = [path, *path.parents]
    for candidate in candidates:
        if (candidate / ".git").exists():
            return str(candidate)
    return str(path)


def new_session(path: Path) -> dict[str, Any]:
    return {
        "file": str(path),
        "name": path.name,
        "bytes": path.stat().st_size,
        "session_id": None,
        "started_at": None,
        "ended_at": None,
        "cwd": None,
        "cwd_samples": [],
        "user_requests": [],
        "assistant_summaries": [],
        "next_step_hints": [],
        "tools": Counter(),
        "tool_statuses": defaultdict(Counter),
        "malformed_lines": 0,
    }


def update_time_range(session: dict[str, Any], timestamp: Any) -> None:
    if not isinstance(timestamp, str) or not timestamp:
        return
    if session["started_at"] is None or timestamp < session["started_at"]:
        session["started_at"] = timestamp
    if session["ended_at"] is None or timestamp > session["ended_at"]:
        session["ended_at"] = timestamp


def remember_cwd(session: dict[str, Any], cwd: Any) -> None:
    if not isinstance(cwd, str) or not cwd.strip():
        return
    if session["cwd"] is None:
        session["cwd"] = cwd
    add_unique(session["cwd_samples"], cwd, max_items=5, limit=300)


def record_text(session: dict[str, Any], role: str, text: str) -> None:
    if is_bootstrap_text(text):
        return
    if role == "user":
        add_unique(session["user_requests"], text, max_items=8, limit=900)
    elif role == "assistant":
        add_unique(session["assistant_summaries"], text, max_items=12, limit=900)
        if NEXT_HINT_RE.search(text):
            add_unique(session["next_step_hints"], text, max_items=8, limit=700)


def parse_plan_hints(arguments: Any) -> list[str]:
    if not isinstance(arguments, str):
        return []
    try:
        parsed = json.loads(arguments)
    except json.JSONDecodeError:
        return []
    hints = []
    for item in parsed.get("plan", []):
        if not isinstance(item, dict):
            continue
        status = item.get("status")
        step = item.get("step")
        if status in {"pending", "in_progress"} and isinstance(step, str):
            hints.append(f"{status}: {step}")
    return hints


def parse_session_file(path: Path) -> dict[str, Any] | None:
    if path.stat().st_size == 0:
        return None

    session = new_session(path)
    call_to_tool: dict[str, str] = {}

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                session["malformed_lines"] += 1
                continue

            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue

            update_time_range(session, record.get("timestamp"))
            remember_cwd(session, payload.get("cwd"))

            record_type = record.get("type")
            payload_type = payload.get("type")

            if record_type == "session_meta":
                session["session_id"] = payload.get("id") or session["session_id"]
                update_time_range(session, payload.get("timestamp"))
                continue

            if record_type == "turn_context":
                continue

            if record_type == "event_msg":
                if payload_type == "user_message":
                    record_text(session, "user", str(payload.get("message", "")))
                elif payload_type == "agent_message":
                    record_text(session, "assistant", str(payload.get("message", "")))
                elif payload_type == "exec_command_end":
                    remember_cwd(session, payload.get("cwd"))
                    tool_name = call_to_tool.get(str(payload.get("call_id")), "shell_command")
                    status = payload.get("status") or "completed"
                    exit_code = payload.get("exit_code")
                    if isinstance(exit_code, int) and exit_code != 0:
                        status = f"exit_{exit_code}"
                    session["tool_statuses"][tool_name][str(status)] += 1
                continue

            if record_type != "response_item":
                continue

            if payload_type == "message":
                role = payload.get("role")
                if role not in {"user", "assistant"}:
                    continue
                record_text(session, role, text_from_content(payload.get("content")))
            elif payload_type == "function_call":
                name = str(payload.get("name") or "unknown_tool")
                session["tools"][name] += 1
                call_id = payload.get("call_id")
                if isinstance(call_id, str):
                    call_to_tool[call_id] = name
                for hint in parse_plan_hints(payload.get("arguments")):
                    add_unique(session["next_step_hints"], hint, max_items=8, limit=500)

    return session


def tool_summary(counter: Counter, statuses: dict[str, Counter]) -> list[dict[str, Any]]:
    names = set(counter) | set(statuses)
    summary = []
    for name in sorted(names):
        entry: dict[str, Any] = {"name": name, "calls": counter.get(name, 0)}
        if statuses.get(name):
            entry["statuses"] = dict(sorted(statuses[name].items()))
        summary.append(entry)
    return summary


def apply_text_budget(project: dict[str, Any], max_chars: int) -> None:
    remaining = max(0, max_chars)
    for field in ("user_requests", "assistant_summaries", "next_step_hints"):
        original = project[field]
        kept = []
        for item in original:
            if remaining <= 0:
                break
            clipped = truncate(item, min(len(item), remaining, 900))
            kept.append(clipped)
            remaining -= len(clipped)
        omitted = len(original) - len(kept)
        if omitted:
            kept.append(f"... {omitted} more omitted by --max-chars-per-project")
        project[field] = kept


def build_projects(sessions: list[dict[str, Any]], max_chars: int) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for session in sessions:
        grouped[nearest_git_root(session.get("cwd"))].append(session)

    projects = []
    for project_root, project_sessions in sorted(grouped.items()):
        tools = Counter()
        statuses: dict[str, Counter] = defaultdict(Counter)
        user_requests: list[str] = []
        assistant_summaries: list[str] = []
        next_step_hints: list[str] = []
        cwd_samples: list[str] = []
        malformed_lines = 0

        evidence = []
        for session in sorted(project_sessions, key=lambda item: item.get("started_at") or ""):
            tools.update(session["tools"])
            for tool_name, status_counter in session["tool_statuses"].items():
                statuses[tool_name].update(status_counter)
            malformed_lines += session["malformed_lines"]
            for cwd in session["cwd_samples"]:
                add_unique(cwd_samples, cwd, max_items=8, limit=300)
            for text in session["user_requests"]:
                add_unique(user_requests, text, max_items=20, limit=900)
            for text in session["assistant_summaries"]:
                add_unique(assistant_summaries, text, max_items=24, limit=900)
            for text in session["next_step_hints"]:
                add_unique(next_step_hints, text, max_items=16, limit=700)
            evidence.append(
                {
                    "file": session["name"],
                    "session_id": session["session_id"],
                    "started_at": session["started_at"],
                    "ended_at": session["ended_at"],
                    "cwd": session["cwd"],
                    "bytes": session["bytes"],
                    "malformed_lines": session["malformed_lines"],
                    "user_request_count": len(session["user_requests"]),
                }
            )

        project = {
            "project_root": project_root,
            "project_name": Path(project_root).name if project_root != "(unknown cwd)" else project_root,
            "session_count": len(project_sessions),
            "cwd_samples": cwd_samples,
            "user_requests": user_requests,
            "assistant_summaries": assistant_summaries,
            "next_step_hints": next_step_hints,
            "tools": tool_summary(tools, statuses),
            "malformed_lines": malformed_lines,
            "evidence_sessions": evidence,
        }
        apply_text_budget(project, max_chars)
        projects.append(project)

    return projects


def write_json(value: dict[str, Any]) -> None:
    data = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        print(data)
    except (AttributeError, UnicodeEncodeError):
        sys.stdout.buffer.write(data.encode("utf-8") + b"\n")


def main() -> int:
    args = parse_args()
    day = selected_date(args.date)
    sessions_root = Path(args.sessions_root).expanduser()
    folder = date_dir(sessions_root, day)

    output: dict[str, Any] = {
        "date": f"{day:%Y-%m-%d}",
        "sessions_root": str(sessions_root),
        "date_dir": str(folder),
        "missing": False,
        "warnings": [],
        "projects": [],
    }

    if not folder.exists():
        output["missing"] = True
        output["warnings"].append("Session date directory does not exist.")
        write_json(output)
        return 0

    sessions = []
    empty_files = 0
    for path in sorted(folder.glob("*.jsonl")):
        parsed = parse_session_file(path)
        if parsed is None:
            empty_files += 1
            continue
        sessions.append(parsed)

    if empty_files:
        output["warnings"].append(f"Skipped {empty_files} empty JSONL file(s).")
    if not sessions:
        output["warnings"].append("No non-empty JSONL sessions found.")

    output["projects"] = build_projects(sessions, args.max_chars_per_project)
    write_json(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
