# Changelog

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
