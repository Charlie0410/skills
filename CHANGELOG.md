# Changelog

## 2026-05-02 Improve Academic PPTX, MPL Figure, And Progress Skills

This change strengthens academic PPTX slide generation, expands MPL figure style/debug guidance, and adds a daily progress summary skill.

### Features

- Added optional academic PPTX planning fields, assertion-evidence layout presets, stricter readable typography defaults, compact caption rules, and a larger section-title hierarchy.
- Expanded the PPTX validator with OfficeCLI fallback resolution, geometry checks, token leak detection, text density warnings, named-shape checks, caption-style checks, 18pt font-floor checks, and picture alt-text enforcement.
- Added MPL figure SciencePlots preset registration, bundled selected SciencePlots styles, TIFF LZW export rules, and richer `DEBUG_VERBOSITY=3` position/reference overlays.
- Added `summarize-daily-progress` for compact daily progress summaries from local Codex session JSONL logs.

### Documentation

- Updated PPTX skill, input contract, layout/style rules, OfficeCLI examples, and verification checklist around one central information unit, one main evidence object, compact annotations, source-supported notes, and explicit font/color/fill properties.
- Updated MPL figure README, request template, style registry, and examples for registered style chains, TIFF compression metadata, complete debug metadata coverage, and zoom-oriented level 3 debug TIFFs.
- Added the academic PPTX quality screening notes used to prioritize the rule updates.

### Verification

- Ran `python -m py_compile` for the PPTX validator, daily-progress collector, and MPL example generators: passed.
- Ran `python aca-slide-pptx-gen/scripts/validate_academic_pptx.py --help`: passed.
- Ran `python summarize-daily-progress/scripts/collect_session_progress.py --help`: passed.
- Ran `python -m json.tool aca-slide-pptx-gen/assets/layout-presets.json`: passed.
- Loaded `mpl-figure-generator/assets/style_registry.yaml` with PyYAML and verified all registered SciencePlots paths from the manifest exist: passed.
- Ran `git diff --check`: passed, with CRLF conversion warnings only.
- Skipped end-to-end PPTX and Matplotlib artifact generation; this pass changed skill rules, validators, examples, and bundled style assets.

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
