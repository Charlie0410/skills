"""Project-local TOML config helpers.

This module intentionally avoids writing global config. It edits only the
project-local compatibility file at ``.tooling/config.toml`` unless an explicit
``config_path`` is supplied.
"""

from __future__ import annotations

import argparse
import copy
import difflib
import json
import ntpath
import os
import re
import shutil
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PROJECT_CONFIG_RELATIVE_PATH = Path(".tooling") / "config.toml"
DEFAULT_GLOBAL_CONFIG_PATH = Path.home() / ".codex" / "config.toml"

KNOWN_PROJECT_KEYS = {
    "trust_level",
    "sandbox_mode",
    "approval_policy",
    "sandbox_network_access",
}
TRUST_LEVELS = {"trusted", "untrusted"}
SANDBOX_MODES = {"read-only", "workspace-write", "danger-full-access"}
APPROVAL_POLICIES = {"untrusted", "on-failure", "on-request", "never"}


class ProjectConfigError(RuntimeError):
    """Raised when a project config operation cannot be completed safely."""


@dataclass(frozen=True)
class NormalizedPath:
    flavor: str
    value: str


@dataclass(frozen=True)
class TableBlock:
    start: int
    end: int
    path: tuple[str, ...]


def set_project_config(
    project_path: str | os.PathLike[str],
    updates: dict[str, Any],
    *,
    dry_run: bool = False,
    apply: bool = False,
    config_path: str | os.PathLike[str] | None = None,
    allow_global_fallback: bool = False,
    global_config_path: str | os.PathLike[str] | None = None,
    inheritance_strategy: str = "override",
    validate: bool = True,
) -> dict[str, Any]:
    """Create or update the project-local config for one project path.

    ``apply=False`` defaults to dry-run behavior. ``inheritance_strategy`` can
    be ``"override"`` or ``"keep"``.
    """

    if not updates:
        raise ProjectConfigError("updates must not be empty")
    if dry_run and apply:
        raise ProjectConfigError("choose either dry_run or apply, not both")
    if inheritance_strategy not in {"override", "keep"}:
        raise ProjectConfigError("inheritance_strategy must be 'override' or 'keep'")

    effective_dry_run = dry_run or not apply
    project_display = display_project_path(project_path)
    target_config_path = resolve_project_config_path(project_path, config_path)
    global_path = Path(global_config_path).expanduser() if global_config_path else DEFAULT_GLOBAL_CONFIG_PATH

    local_problem = _project_config_unusable_reason(target_config_path)
    if local_problem:
        result = _base_result(project_display, target_config_path, effective_dry_run, apply)
        result["success"] = False
        result["errors"].append(local_problem)
        if allow_global_fallback:
            result["global_fallback"] = {
                "allowed": True,
                "config_path": str(global_path),
                "message": "Project-local config is not usable. A global config proposal may be shown, but this helper will not write it automatically.",
                "proposed_updates": copy.deepcopy(updates),
            }
            return result
        raise ProjectConfigError(local_problem)

    before_text = _read_text_if_exists(target_config_path)
    config_existed = target_config_path.exists()
    inheritance = find_inheritance(
        project_path,
        target_config_path=target_config_path,
        global_config_path=global_path,
    )

    keep_inherited = False
    if inheritance_strategy == "keep":
        inherited_values = _effective_inherited_values(inheritance)
        keep_inherited = all(inherited_values.get(key) == value for key, value in updates.items())

    if keep_inherited:
        after_text = before_text
        changed_keys: list[str] = []
        created_table = False
        diff = ""
    else:
        after_text, changed_keys, created_table = update_project_table_text(before_text, project_display, updates)
        diff = make_unified_diff(before_text, after_text, str(target_config_path))

    validation = validate_config_text(after_text) if validate else {"ok": True, "errors": [], "warnings": []}
    result = _base_result(project_display, target_config_path, effective_dry_run, apply)
    result.update(
        {
            "config_created": bool(not config_existed and changed_keys and apply),
            "would_create_config": bool(not config_existed and changed_keys and effective_dry_run),
            "changed": bool(changed_keys),
            "changed_keys": changed_keys,
            "created_project_table": created_table,
            "diff": diff,
            "validation": validation,
            "inheritance": inheritance,
            "inheritance_options": [
                "keep inherited values",
                "write a more specific project override",
            ]
            if inheritance
            else [],
        }
    )

    if keep_inherited:
        result["message"] = "No local write needed because inherited config already satisfies the requested updates."
        result["success"] = True
        return result

    if validation["errors"]:
        result["success"] = False
        result["errors"].extend(validation["errors"])
        if apply:
            raise ProjectConfigError("validation failed; refusing to write project config")
        return result

    if effective_dry_run:
        result["success"] = True
        return result

    backup_path = None
    if changed_keys:
        try:
            backup_path = backup_config_file(target_config_path)
            atomic_write_text(target_config_path, after_text)
        except OSError as exc:
            result["success"] = False
            result["errors"].append(str(exc))
            if allow_global_fallback:
                result["global_fallback"] = {
                    "allowed": True,
                    "config_path": str(global_path),
                    "message": "Project-local write failed. A global config proposal may be shown, but this helper will not write it automatically.",
                    "proposed_updates": copy.deepcopy(updates),
                }
                return result
            raise

    result["backup_path"] = str(backup_path) if backup_path else None
    result["config_created"] = bool(not config_existed and changed_keys)
    result["success"] = True
    return result


def read_project_config(
    project_path: str | os.PathLike[str],
    *,
    config_path: str | os.PathLike[str] | None = None,
    global_config_path: str | os.PathLike[str] | None = None,
) -> dict[str, Any]:
    """Read direct and inherited project config without mutating any file."""

    project_display = display_project_path(project_path)
    target_config_path = resolve_project_config_path(project_path, config_path)
    text = _read_text_if_exists(target_config_path)
    direct = _find_direct_project_values(text, project_display)
    inheritance = find_inheritance(
        project_path,
        target_config_path=target_config_path,
        global_config_path=Path(global_config_path).expanduser() if global_config_path else DEFAULT_GLOBAL_CONFIG_PATH,
    )
    inherited_values = _effective_inherited_values(inheritance)
    effective_values = dict(inherited_values)
    if direct:
        effective_values.update(direct)

    return {
        "project_path": project_display,
        "config_path": str(target_config_path),
        "config_exists": target_config_path.exists(),
        "direct": direct,
        "inheritance": inheritance,
        "effective": effective_values,
    }


def validate_project_config(
    *,
    config_path: str | os.PathLike[str] | None = None,
    text: str | None = None,
) -> dict[str, Any]:
    """Validate TOML syntax and supported project-level semantics."""

    if text is None:
        if config_path is None:
            raise ProjectConfigError("config_path or text is required")
        text = _read_text_if_exists(Path(config_path).expanduser())
    return validate_config_text(text)


def update_project_table_text(
    text: str,
    project_path: str | os.PathLike[str],
    updates: dict[str, Any],
) -> tuple[str, list[str], bool]:
    """Return updated TOML text, changed keys, and whether a table was inserted."""

    if text.strip():
        tomllib.loads(text)
    target_norm = normalize_path_for_match(project_path)
    lines = text.splitlines(keepends=True)
    newline = _detect_newline(text)
    blocks = _scan_table_blocks(text)
    project_blocks = [
        block
        for block in blocks
        if len(block.path) == 2
        and block.path[0] == "projects"
        and normalize_path_for_match(block.path[1]) == target_norm
    ]
    if len(project_blocks) > 1:
        raise ProjectConfigError("multiple project tables match the same normalized path")

    if not project_blocks:
        header = f"[projects.{toml_key_segment(str(project_path))}]"
        block_lines = [header + newline]
        block_lines.extend(f"{key} = {toml_value(value)}{newline}" for key, value in updates.items())
        prefix = ""
        if text:
            prefix = text
            if not prefix.endswith(("\n", "\r")):
                prefix += newline
            if prefix.strip():
                prefix += newline
        return prefix + "".join(block_lines), list(updates.keys()), True

    block = project_blocks[0]
    doc = tomllib.loads(text) if text.strip() else {}
    target_key = block.path[1]
    current_values = doc.get("projects", {}).get(target_key, {})
    if not isinstance(current_values, dict):
        raise ProjectConfigError("target project entry is not a TOML table")

    assignment_lines = _find_direct_assignment_lines(lines, block)
    replacements: dict[int, str] = {}
    insertions: list[str] = []
    changed_keys: list[str] = []

    for key, value in updates.items():
        if current_values.get(key) == value:
            continue
        changed_keys.append(key)
        rendered = toml_value(value)
        if key in assignment_lines:
            line_index = assignment_lines[key]
            replacements[line_index] = _replace_assignment_value(lines[line_index], key, rendered)
        else:
            insertions.append(f"{key} = {rendered}{newline}")

    if not changed_keys:
        return text, [], False

    for line_index, replacement in replacements.items():
        lines[line_index] = replacement

    if insertions:
        insertion_index = block.end
        while insertion_index > block.start + 1 and lines[insertion_index - 1].strip() == "":
            insertion_index -= 1
        lines[insertion_index:insertion_index] = insertions

    return "".join(lines), changed_keys, False


def validate_config_text(text: str) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        doc = tomllib.loads(text) if text.strip() else {}
    except tomllib.TOMLDecodeError as exc:
        return {"ok": False, "errors": [f"TOML syntax error: {exc}"], "warnings": []}

    projects = doc.get("projects")
    if projects is not None and not isinstance(projects, dict):
        errors.append("[projects] must be a table")
    elif isinstance(projects, dict):
        seen: dict[NormalizedPath, str] = {}
        for project_key, values in projects.items():
            norm = normalize_path_for_match(project_key)
            if norm in seen and seen[norm] != project_key:
                warnings.append(
                    f"project keys {seen[norm]!r} and {project_key!r} normalize to the same path"
                )
            seen[norm] = project_key
            if not isinstance(values, dict):
                errors.append(f"[projects.{project_key!r}] must contain key/value settings")
                continue
            for key, value in values.items():
                if key not in KNOWN_PROJECT_KEYS:
                    continue
                if key == "trust_level" and value not in TRUST_LEVELS:
                    errors.append(f"{project_key}: trust_level must be one of {sorted(TRUST_LEVELS)}")
                if key == "sandbox_mode" and value not in SANDBOX_MODES:
                    errors.append(f"{project_key}: sandbox_mode must be one of {sorted(SANDBOX_MODES)}")
                if key == "approval_policy" and value not in APPROVAL_POLICIES:
                    errors.append(f"{project_key}: approval_policy must be one of {sorted(APPROVAL_POLICIES)}")
                if key == "sandbox_network_access" and not isinstance(value, bool):
                    errors.append(f"{project_key}: sandbox_network_access must be a boolean")

    return {"ok": not errors, "errors": errors, "warnings": warnings}


def find_inheritance(
    project_path: str | os.PathLike[str],
    *,
    target_config_path: Path,
    global_config_path: Path,
) -> list[dict[str, Any]]:
    """Find parent/global project entries that apply to the project path."""

    project_norm = normalize_path_for_match(project_path)
    inherited: list[dict[str, Any]] = []
    for candidate in _ancestor_project_config_paths(project_path, target_config_path):
        inherited.extend(
            _matching_entries_from_file(
                candidate,
                project_norm,
                source_type="project-parent",
            )
        )
    inherited.extend(
        _matching_entries_from_file(
            global_config_path,
            project_norm,
            source_type="global",
        )
    )
    inherited.sort(key=lambda item: item["specificity"], reverse=True)
    for item in inherited:
        item.pop("specificity", None)
    return inherited


def make_unified_diff(before: str, after: str, path_label: str) -> str:
    if before == after:
        return ""
    before_lines = before.splitlines(keepends=True)
    after_lines = after.splitlines(keepends=True)
    return "".join(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile=f"{path_label} (before)",
            tofile=f"{path_label} (after)",
        )
    )


def backup_config_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    backup_path = path.with_name(f"{path.name}.bak-{timestamp}")
    shutil.copy2(path, backup_path)
    return backup_path


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def resolve_project_config_path(
    project_path: str | os.PathLike[str],
    config_path: str | os.PathLike[str] | None = None,
) -> Path:
    if config_path is not None:
        return Path(config_path).expanduser()
    return Path(project_path).expanduser().resolve(strict=False) / PROJECT_CONFIG_RELATIVE_PATH


def display_project_path(project_path: str | os.PathLike[str]) -> str:
    raw = os.path.expandvars(os.path.expanduser(str(project_path)))
    if _looks_windows_path(raw):
        return ntpath.normpath(raw.replace("/", "\\"))
    return str(Path(raw).resolve(strict=False))


def normalize_path_for_match(path_value: str | os.PathLike[str]) -> NormalizedPath:
    raw = os.path.expandvars(os.path.expanduser(str(path_value))).strip()
    if _looks_windows_path(raw):
        norm = ntpath.normcase(ntpath.normpath(raw.replace("/", "\\")))
        if len(norm) > 3:
            norm = norm.rstrip("\\")
        return NormalizedPath("windows", norm)
    resolved = str(Path(raw).resolve(strict=False))
    norm = os.path.normcase(os.path.normpath(resolved))
    if len(norm) > 1:
        norm = norm.rstrip(os.sep)
    return NormalizedPath("posix", norm)


def toml_key_segment(value: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9_-]+", value):
        return value
    if "'" not in value and "\n" not in value and "\r" not in value:
        return "'" + value + "'"
    return json.dumps(value, ensure_ascii=False)


def toml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        if value != value:
            return "nan"
        if value == float("inf"):
            return "inf"
        if value == float("-inf"):
            return "-inf"
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(item) for item in value) + "]"
    raise ProjectConfigError(f"unsupported TOML value type for {value!r}")


def _base_result(project_display: str, config_path: Path, dry_run: bool, apply: bool) -> dict[str, Any]:
    return {
        "project_path": project_display,
        "config_path": str(config_path),
        "dry_run": dry_run,
        "apply": apply,
        "success": False,
        "config_created": False,
        "would_create_config": False,
        "changed": False,
        "changed_keys": [],
        "backup_path": None,
        "errors": [],
        "warnings": [],
    }


def _read_text_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _project_config_unusable_reason(path: Path) -> str | None:
    parent = path.parent
    if parent.exists() and not parent.is_dir():
        return f"project-local config parent is not a directory: {parent}"
    if path.exists() and path.is_dir():
        return f"project-local config path is a directory: {path}"
    return None


def _detect_newline(text: str) -> str:
    match = re.search(r"\r\n|\n|\r", text)
    return match.group(0) if match else "\n"


def _looks_windows_path(value: str) -> bool:
    return bool(re.match(r"^[A-Za-z]:[\\/]", value)) or "\\" in value


def _scan_table_blocks(text: str) -> list[TableBlock]:
    lines = text.splitlines(keepends=True)
    headers: list[tuple[int, tuple[str, ...] | None]] = []
    for index, line in enumerate(lines):
        header = _extract_table_header(line)
        if header is None:
            continue
        kind, content = header
        if kind != "table":
            headers.append((index, None))
            continue
        try:
            headers.append((index, tuple(_parse_table_path(content))))
        except tomllib.TOMLDecodeError:
            headers.append((index, None))

    blocks: list[TableBlock] = []
    for header_index, (line_index, path) in enumerate(headers):
        if path is None:
            continue
        end = headers[header_index + 1][0] if header_index + 1 < len(headers) else len(lines)
        blocks.append(TableBlock(start=line_index, end=end, path=path))
    return blocks


def _extract_table_header(line: str) -> tuple[str, str] | None:
    stripped = line.lstrip()
    leading = len(line) - len(stripped)
    if not stripped.startswith("["):
        return None
    if stripped.startswith("[["):
        kind = "array"
        start = leading + 2
        close = "]]"
    else:
        kind = "table"
        start = leading + 1
        close = "]"

    quote: str | None = None
    escaped = False
    index = start
    while index < len(line):
        char = line[index]
        if quote == '"':
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = None
        elif quote == "'":
            if char == "'":
                quote = None
        else:
            if char == "#":
                return None
            if char == '"':
                quote = '"'
            elif char == "'":
                quote = "'"
            elif close == "]" and char == "]":
                return kind, line[start:index].strip()
            elif close == "]]" and line.startswith("]]", index):
                return kind, line[start:index].strip()
        index += 1
    return None


def _parse_table_path(content: str) -> list[str]:
    marker = "__project_config_marker__"
    data = tomllib.loads(f"[{content}]\n{marker} = true\n")
    found = _find_marker_path(data, marker)
    if not found:
        raise ProjectConfigError(f"could not parse table path: {content}")
    return found[:-1]


def _find_marker_path(value: Any, marker: str, prefix: list[str] | None = None) -> list[str] | None:
    prefix = prefix or []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == marker:
                return prefix + [key]
            found = _find_marker_path(child, marker, prefix + [str(key)])
            if found:
                return found
    return None


def _find_direct_assignment_lines(lines: list[str], block: TableBlock) -> dict[str, int]:
    assignments: dict[str, int] = {}
    for index in range(block.start + 1, block.end):
        line = lines[index]
        eq_index = _find_unquoted_char(line, "=")
        if eq_index is None:
            continue
        key_text = line[:eq_index].strip()
        try:
            key_path = _parse_assignment_key_path(key_text)
        except tomllib.TOMLDecodeError:
            continue
        if len(key_path) == 1:
            assignments.setdefault(key_path[0], index)
    return assignments


def _parse_assignment_key_path(key_text: str) -> tuple[str, ...]:
    marker_value = "true"
    data = tomllib.loads(f"[x]\n{key_text} = {marker_value}\n")
    table = data["x"]
    path: list[str] = []
    current: Any = table
    while isinstance(current, dict) and len(current) == 1:
        key = next(iter(current))
        path.append(str(key))
        current = current[key]
    return tuple(path)


def _replace_assignment_value(line: str, key: str, rendered_value: str) -> str:
    indent = re.match(r"\s*", line).group(0)
    newline = ""
    if line.endswith("\r\n"):
        newline = "\r\n"
        body = line[:-2]
    elif line.endswith(("\n", "\r")):
        newline = line[-1]
        body = line[:-1]
    else:
        body = line
    eq_index = _find_unquoted_char(body, "=")
    if eq_index is None:
        return f"{indent}{key} = {rendered_value}{newline}"
    hash_index = _find_unquoted_char(body, "#", start=eq_index + 1)
    suffix = ""
    if hash_index is not None:
        before_comment = body[:hash_index]
        if before_comment.endswith(" ") or before_comment.endswith("\t"):
            suffix = body[hash_index - 1 :]
        else:
            suffix = " " + body[hash_index:]
    return f"{indent}{key} = {rendered_value}{suffix}{newline}"


def _find_unquoted_char(line: str, target: str, start: int = 0) -> int | None:
    quote: str | None = None
    escaped = False
    for index in range(start, len(line)):
        char = line[index]
        if quote == '"':
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = None
        elif quote == "'":
            if char == "'":
                quote = None
        else:
            if char == target:
                return index
            if char == '"':
                quote = '"'
            elif char == "'":
                quote = "'"
    return None


def _find_direct_project_values(text: str, project_path: str | os.PathLike[str]) -> dict[str, Any]:
    if not text.strip():
        return {}
    doc = tomllib.loads(text)
    projects = doc.get("projects", {})
    if not isinstance(projects, dict):
        return {}
    target_norm = normalize_path_for_match(project_path)
    matches = [
        values
        for key, values in projects.items()
        if isinstance(values, dict) and normalize_path_for_match(key) == target_norm
    ]
    if len(matches) > 1:
        raise ProjectConfigError("multiple project entries match the same normalized path")
    return dict(matches[0]) if matches else {}


def _ancestor_project_config_paths(project_path: str | os.PathLike[str], target_config_path: Path) -> list[Path]:
    project = Path(project_path).expanduser().resolve(strict=False)
    paths: list[Path] = []
    for parent in project.parents:
        candidate = parent / PROJECT_CONFIG_RELATIVE_PATH
        if candidate == target_config_path:
            continue
        if candidate.exists():
            paths.append(candidate)
    return paths


def _matching_entries_from_file(
    config_path: Path,
    project_norm: NormalizedPath,
    *,
    source_type: str,
) -> list[dict[str, Any]]:
    if not config_path.exists() or config_path.is_dir():
        return []
    text = _read_text_if_exists(config_path)
    if not text.strip():
        return []
    try:
        doc = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return [
            {
                "source_type": source_type,
                "config_path": str(config_path),
                "project_key": None,
                "relationship": "unreadable",
                "values": {},
                "error": "TOML syntax error; ignored for inheritance analysis",
                "specificity": -1,
            }
        ]
    projects = doc.get("projects", {})
    if not isinstance(projects, dict):
        return []
    matches: list[dict[str, Any]] = []
    for key, values in projects.items():
        if not isinstance(values, dict):
            continue
        key_norm = normalize_path_for_match(key)
        if _is_same_or_parent_path(key_norm, project_norm):
            relationship = "exact" if key_norm == project_norm else "parent"
            matches.append(
                {
                    "source_type": source_type,
                    "config_path": str(config_path),
                    "project_key": key,
                    "relationship": relationship,
                    "values": dict(values),
                    "explanation": f"{source_type} config entry {key!r} applies to this project as a {relationship} path match.",
                    "specificity": _path_specificity(key_norm),
                }
            )
    return matches


def _is_same_or_parent_path(parent: NormalizedPath, child: NormalizedPath) -> bool:
    if parent.flavor != child.flavor:
        return False
    if parent.value == child.value:
        return True
    separator = "\\" if parent.flavor == "windows" else os.sep
    prefix = parent.value.rstrip(separator) + separator
    return child.value.startswith(prefix)


def _path_specificity(path_value: NormalizedPath) -> int:
    separator = "\\" if path_value.flavor == "windows" else os.sep
    return len([part for part in path_value.value.split(separator) if part])


def _effective_inherited_values(inheritance: list[dict[str, Any]]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for entry in inheritance:
        for key, value in entry.get("values", {}).items():
            values.setdefault(key, value)
    return values


def _parse_cli_value(raw: str) -> Any:
    try:
        return tomllib.loads(f"value = {raw}\n")["value"]
    except tomllib.TOMLDecodeError:
        return raw


def _parse_cli_updates(items: list[str]) -> dict[str, Any]:
    updates: dict[str, Any] = {}
    for item in items:
        if "=" not in item:
            raise ProjectConfigError(f"--set must use key=value, got {item!r}")
        key, raw_value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise ProjectConfigError("--set key must not be empty")
        updates[key] = _parse_cli_value(raw_value.strip())
    return updates


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage project-local TOML config.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    set_parser = subparsers.add_parser("set", help="set project-local config values")
    set_parser.add_argument("project_path")
    set_parser.add_argument("--set", dest="sets", action="append", required=True, help="key=value")
    set_parser.add_argument("--config-path")
    set_parser.add_argument("--global-config-path")
    set_parser.add_argument("--dry-run", action="store_true")
    set_parser.add_argument("--apply", action="store_true")
    set_parser.add_argument("--allow-global-fallback", action="store_true")
    set_parser.add_argument("--inheritance-strategy", choices=["override", "keep"], default="override")

    read_parser = subparsers.add_parser("read", help="read direct and inherited config")
    read_parser.add_argument("project_path")
    read_parser.add_argument("--config-path")
    read_parser.add_argument("--global-config-path")

    validate_parser = subparsers.add_parser("validate", help="validate a project config file")
    validate_parser.add_argument("--config-path", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "set":
            result = set_project_config(
                args.project_path,
                _parse_cli_updates(args.sets),
                dry_run=args.dry_run,
                apply=args.apply,
                config_path=args.config_path,
                allow_global_fallback=args.allow_global_fallback,
                global_config_path=args.global_config_path,
                inheritance_strategy=args.inheritance_strategy,
            )
        elif args.command == "read":
            result = read_project_config(
                args.project_path,
                config_path=args.config_path,
                global_config_path=args.global_config_path,
            )
        else:
            result = validate_project_config(config_path=args.config_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result.get("success", result.get("ok", True)) else 1
    except ProjectConfigError as exc:
        print(json.dumps({"success": False, "errors": [str(exc)]}, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
