# Changelog

## 2026-05-02 Add CPP Packaging And MPL Debug Mode

This change adds CPP materials packaging, MPL figure debug output guidance, and README usage coverage for every skill in the workspace.

### Features

- Added `canonical_prompt_compiler_skills/cpp-package-materials/` with skill instructions, UI metadata, packaging rules, and a deterministic `package_materials.py` helper.
- Added JSON sidecar material maps so compiled-prompt material names are treated as logical IDs rather than filesystem paths.
- Added manifest behavior for included files, missing bindings, missing paths, empty directories, and URL references without generating empty zip files.
- Added `RUN_MODE=debug` guidance to `mpl-figure-generator`, including debug figure naming, stable element IDs, debug verbosity levels, and debug metadata requirements.

### Documentation

- Updated `README.md` to describe the CPP skill flow as `normalize`, `compile`, `package`, `verify`, and `repair`.
- Added a README section describing when and how to use all 10 discovered skills.
- Updated the MPL figure skill README, request template, and style registry with production and debug run-mode fields.

### Verification

- Ran `python -m py_compile` for `package_materials.py`: passed.
- Ran `package_materials.py --help`: passed.
- Ran mapped-file and missing-binding packaging fixtures under `.trash/`: passed.
- Ran `rg --files -g SKILL.md` and checked README coverage for all 10 skill names: passed.

## 2026-05-01 Add Academic PPTX Slide Skill

This change adds a PPTX-producing academic slide skill and updates CPP prompt compiler skills to write stage artifacts to files by default.

### Features

- Added `aca-slide-pptx-gen/` for generating one-slide academic `.pptx` artifacts with OfficeCLI-based build and verification rules.
- Added layout presets, OfficeCLI build references, input contracts, verification guidance, and a focused PPTX validation helper.
- Updated CPP normalize, compile, verify, and repair skills so their default artifacts are written to same-directory files instead of only returned in chat.

### Documentation

- Updated `README.md` to list `aca-slide-gen/`, `aca-slide-pptx-gen/`, and `project-config/`.
- Updated CPP skill `agents/openai.yaml` prompts to mention file-backed artifacts.
- Added `.gitignore` entries for `.trash/` and Python bytecode artifacts.

### Verification

- Ran `quick_validate.py` for `aca-slide-pptx-gen`: passed.
- Ran `quick_validate.py` for all four CPP prompt compiler skills: passed.
- Ran `validate_academic_pptx.py --help`: passed.
- Ran `python -m json.tool aca-slide-pptx-gen/assets/layout-presets.json`: passed.
- Skipped end-to-end OfficeCLI PPTX generation because `officecli` is not installed or not on PATH.
