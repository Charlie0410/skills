---
name: cpp-package-materials
description: Package local runtime materials required by a CPP .compiled-prompt.md artifact into a zip attachment and manifest. Use when Codex needs to inspect a compiled CPP prompt, identify the logical material IDs it asks the user to submit, bind those IDs to real local files or directories through a materials-map JSON sidecar or --material arguments, and prepare a file-backed materials package without modifying the compiled prompt.
---

# CPP Package Materials

## Overview

Prepare the attachment set for a compiled Canonical Prompt Protocol prompt. This skill only packages runtime materials; it does not normalize, compile, verify, repair, rewrite, or execute the prompt.

## Workflow

1. Read the user's request and identify the primary `*.compiled-prompt.md` file.
   - Treat material names inside the compiled prompt as logical material IDs, not filesystem paths.
   - Do not search the filesystem to guess bindings for those IDs.

2. Read packaging rules as needed.
   - Use `references/material-packaging-rules.md` for candidate extraction, map semantics, zip layout, manifest contents, and failure classification.

3. Run the packager script.

   ```powershell
   python canonical_prompt_compiler_skills\cpp-package-materials\scripts\package_materials.py <compiled-prompt.md> [--map <materials-map.json>] [--material "logical id=path"] [--output <zip-path>] [--manifest <manifest-path>]
   ```

4. Inspect the script summary and, when needed, the sidecar manifest.
   - Default map path: `<compiled-stem>.materials-map.json`.
   - Default zip path: `<compiled-stem>.materials.zip`.
   - Default sidecar manifest path: `<compiled-stem>.materials-manifest.md`.
   - If the map is missing or incomplete, the script writes or updates the map template with empty entries for unresolved logical IDs.

5. Report only the operational summary in chat.
   - Include the zip path, manifest path, included-file count, missing-material count, and whether packaging is blocked.
   - Do not paste the full manifest unless the user asks for it.

## Material Binding

Use a JSON sidecar map to bind logical material IDs to local material paths:

```json
{
  "materials": {
    "runtime load section": "C:/path/to/runtime-load-section.md",
    "experiment table": [
      "C:/path/to/results.csv",
      "C:/path/to/metadata.xlsx"
    ]
  }
}
```

- The key must match the logical material ID extracted from the compiled prompt.
- A value may be one file, one directory, or a list of files and directories.
- Relative paths in the map resolve relative to the map file's directory.
- Relative paths passed through `--material` resolve relative to the current working directory.
- Directory bindings are packaged recursively while skipping `.git/`, `.trash/`, `__pycache__/`, `.pyc`, and `.pyo`.
- URL values are recorded as external references and are not downloaded.

## Output Contract

The package operation must be file-backed.

- Always write a sidecar manifest.
- Write a zip only when at least one local file can be included.
- Include a `MANIFEST.md` inside the zip that lists archive paths without exposing local absolute paths.
- Do not add the compiled prompt itself to the zip by default.
- Record unresolved IDs, empty bindings, missing paths, empty directories, invalid map values, and URL references in the sidecar manifest.
- Treat packaging as blocked when any required logical material ID lacks a packaged local file or when unresolved bindings remain.

## Guardrails

- Do not infer a filesystem path from a logical material ID.
- Do not silently ignore missing, empty, invalid, or external bindings.
- Do not modify the compiled prompt.
- Do not download remote URLs.
- Do not generate an empty zip.
- Keep local absolute paths out of the zip-internal `MANIFEST.md`.

## References

- Read `references/material-packaging-rules.md` when changing extraction, binding, zip, or manifest behavior.
- Use `scripts/package_materials.py` for the actual packaging operation instead of hand-building archives.
