---
name: summarize-daily-progress
description: Summarize Codex daily work from local session JSONL logs, grouped by project, with progress, current state, next steps, blockers, and evidence sessions. Use when Codex is asked to summarize today's work, daily progress, session history, completed tasks, current status, or follow-up work from `.codex/sessions` logs.
---

# Summarize Daily Progress

## Workflow

Run the collector script before reading session JSONL files manually. The
collector filters bootstrap messages, tool output noise, malformed lines, and
empty files into compact JSON that is safe to summarize in chat.

Default command from the repo root:

```powershell
python .\summarize-daily-progress\scripts\collect_session_progress.py --date today
```

Use the JSON to answer in chat. Do not write a report file unless the user asks
for one.

## Date Selection

Treat `today` as the local sessions directory date, not UTC message boundaries.
For example, on local date 2026-05-02, read:

```text
~\.codex\sessions\2026\05\02\*.jsonl
```

For a different day, pass an explicit local date:

```powershell
python .\summarize-daily-progress\scripts\collect_session_progress.py --date 2026-05-01
```

Use `--sessions-root PATH` only when the user points to a non-default sessions
tree. Use `--max-chars-per-project N` when the day has too many sessions for a
compact answer.

## Summarizing

Group the final answer by the `project_root` or `cwd` reported by the collector.
For each project, keep the response concise and include:

1. Progress: what changed or was attempted today.
2. Current state: finished, partially done, waiting, or only planned.
3. Next steps: concrete follow-up actions from the session evidence.
4. Blockers or unknowns: failed checks, missing tools, unresolved decisions, or
   note `None found in the session evidence`.
5. Evidence sessions: cite the session file names or session ids from the JSON.

Prefer factual synthesis over transcript-style retelling. Keep tool details at
the level of meaningful checks or failures; do not paste raw command output.

## Privacy And Noise

Ignore or omit:

1. Developer, system, tool bootstrap, AGENTS.md, and environment-context text.
2. Empty files and malformed JSONL lines, except for reporting counts when useful.
3. Long command output, token counts, rate limits, and raw tool arguments.
4. Secret-looking values. The collector redacts common token, key, password, and
   authorization patterns, but also avoid repeating anything that appears
   credential-like.
