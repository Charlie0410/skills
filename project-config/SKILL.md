---
name: project-config
description: Manage project-local TOML configuration for a specified project path without editing global config. Use when Codex needs to create, read, update, validate, dry-run, or apply project-scoped settings such as trust_level, sandbox_mode, approval_policy, sandbox_network_access, or future project-level parameters, especially on Windows paths and when inherited parent project settings may already apply.
---

# Project Config

## Scope

Use this skill to manage configuration for one explicit project path. The skill defaults to a project-local compatibility file:

```text
<project-root>/.tooling/config.toml
```

This location is a compatibility strategy. Do not assume upstream tools already natively read it. Keep the path centralized as `PROJECT_CONFIG_RELATIVE_PATH` in `scripts/project_config.py` so it can be changed later.

Do not modify global config by default. Treat global config, project-local config, and backup files as separate classes:

- Global config: read-only context, normally `~/.codex/config.toml`.
- Project-local config: the only default write target, normally `<project>/.tooling/config.toml`.
- Backup file: timestamped copy made beside the project-local config before an apply write.

Only discuss a global fallback when `allow_global_fallback=True` and project-local config cannot be used. Even then, return a proposal and do not write global config automatically.

## Interface

Prefer the Python API in `scripts/project_config.py` for deterministic edits:

```python
from project_config import set_project_config

set_project_config(project_path, {"trust_level": "trusted"}, dry_run=True)
set_project_config(project_path, {"trust_level": "trusted"}, apply=True)
```

CLI examples:

```bash
python scripts/project_config.py set "C:\Users\charlie\data\codespace\repo" --set trust_level=trusted --dry-run
python scripts/project_config.py set "C:\Users\charlie\data\codespace\repo" --set trust_level=trusted --apply
python scripts/project_config.py read "C:\Users\charlie\data\codespace\repo"
python scripts/project_config.py validate --config-path "C:\Users\charlie\data\codespace\repo\.tooling\config.toml"
```

Supported functions:

- `set_project_config(project_path, updates, dry_run=False, apply=False, config_path=None, allow_global_fallback=False, global_config_path=None, inheritance_strategy="override", validate=True)`
- `read_project_config(project_path, config_path=None, global_config_path=None)`
- `validate_project_config(config_path=None, text=None)`

Input parameters:

- `project_path`: required project path. Normalize for matching, but preserve existing TOML key spelling when updating an existing entry.
- `updates`: dict of project-level keys and TOML scalar/list values, for example `{"trust_level": "trusted"}`.
- `dry_run`: return the proposed text diff and metadata; do not write.
- `apply`: atomically write the project-local config. If neither `dry_run` nor `apply` is set, behave as dry-run.
- `config_path`: optional override for the project-local config file path.
- `allow_global_fallback`: allow a non-writing global fallback proposal only if project-local config is unusable.
- `global_config_path`: optional read-only global config path used for inheritance analysis.
- `inheritance_strategy`: `"override"` writes a more specific project entry; `"keep"` avoids writing when inherited values already satisfy the request.
- `validate`: parse generated TOML and run semantic checks before reporting success or writing.

Output fields:

- `config_path`: actual project-local config file path hit by the operation.
- `config_created` / `would_create_config`: whether the project-local file was or would be created.
- `success`, `changed`, `changed_keys`: operation outcome and keys changed.
- `diff`: unified diff in dry-run mode or for reporting proposed changes.
- `backup_path`: backup file path for apply writes to existing files.
- `validation`: TOML syntax and semantic validation result.
- `inheritance`: parent/global entries that currently apply to the project path.
- `inheritance_options`: choices to keep inherited values or write a more specific override.

## Behavior

When setting values:

1. Resolve the target project-local config path.
2. Read existing config if present.
3. Parse TOML with `tomllib`.
4. Locate `[projects.'...']` entries by normalized path comparison.
5. Update the matching project table or append a new `[projects.'<project path>']` table.
6. Preserve unrelated comments, sections, ordering, and existing project key display text.
7. Validate the generated TOML.
8. In dry-run mode, return a unified diff only.
9. In apply mode, back up the old file if present, then atomically replace the project-local file.

The updater is structural for the project table it edits: it parses TOML, scans table headers, parses assignment keys, and serializes TOML values. It does not use global full-file string replacement. Because the standard library `tomllib` is read-only and does not preserve formatting itself, the script uses a small line-preserving patcher for the target table and leaves unrelated text untouched.

## Inheritance

Report inherited coverage when a parent path entry already applies to the target project. The script checks:

- parent project-local config files at ancestor `.tooling/config.toml` paths;
- the read-only global config path, when it exists.

If a parent or global entry has `[projects.'<parent path>']` and the target path is inside that parent, the result includes an inheritance explanation. Use:

- `inheritance_strategy="keep"` to keep inherited values when they satisfy the requested updates;
- `inheritance_strategy="override"` to write a more specific `[projects.'<target path>']` entry.

## Windows And TOML Rules

Normalize paths for matching with case-insensitive Windows semantics when a value looks like a Windows path. Keep the original existing TOML key spelling when updating; use the normalized display path only for new tables.

Use single-quoted TOML path keys when possible:

```toml
[projects.'C:\Users\charlie\data\codespace\repo']
trust_level = "trusted"
```

Single-quoted TOML keys avoid backslash escaping. If the path contains a single quote or line break, fall back to a JSON-style double-quoted TOML key with proper escaping. Never build a table header by raw concatenation without TOML key serialization.

## Validation And Errors

Validation checks TOML syntax and known project-level semantics:

- `trust_level`: `trusted` or `untrusted`
- `sandbox_mode`: `read-only`, `workspace-write`, or `danger-full-access`
- `approval_policy`: `untrusted`, `on-failure`, `on-request`, or `never`
- `sandbox_network_access`: boolean

Unknown keys are allowed for future extension. Invalid TOML, duplicate normalized project entries, unusable project-local paths, unsupported value types, and failed writes should return structured errors and avoid writing.

Repeated apply calls with the same request must be idempotent: no duplicate table, no duplicate key, no backup, and no rewrite when the file is already in the requested state.
