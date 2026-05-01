# Codex Matplotlib Figure Skill

This repository uses the standard `skills/` layout and is intended to be installed as a plain skill repository.

- `skills/mpl-figure-generator/SKILL.md`
- `skills/mpl-figure-generator/assets/...`
- `skills/mpl-figure-generator/references/...`

The skill is named `mpl-figure-generator` to reflect its actual behavior: generate finished Matplotlib figures directly.

## What changed

1. The canonical mplstyle file is now the default source of truth for figure size, export format, export DPI, and save behavior.
2. The skill now generates figure artifacts directly.
3. The canonical style requires LaTeX and declares that requirement explicitly.
4. Labels are expected to use LaTeX-compatible strings, with units written in square brackets.

## Runtime prerequisites

The default style at `skills/mpl-figure-generator/assets/styles/mps_base.mplstyle` requires:

1. `latex` on `PATH`
2. `pdflatex` on `PATH`
3. The LaTeX packages `lmodern` and `siunitx`

If those prerequisites are missing, the skill should report the problem instead of silently disabling the style.

## Run modes

Existing requests remain production requests by default. Leave `RUN_MODE` empty, or set it to `production`, to create the clean finished figure and companion metadata.

Set `RUN_MODE` to `debug` to also create `<OUTPUT_BASENAME>.debug.<style_format>`, an annotated figure with stable element IDs such as `series_1`, `x_label`, `legend`, and `colorbar_label`. Debug metadata records `run_mode`, `debug_verbosity`, `debug_figure_path`, and `debug_elements`. `DEBUG_VERBOSITY` accepts `1`, `2`, or `3` and defaults to `2` in debug mode.

## Install

After publishing to GitHub:

```bash
npx skills add <owner/repo>
```

To install only this skill:

```bash
npx skills add <owner/repo> --skill mpl-figure-generator
```

To validate discovery from the local repository:

```bash
npx skills add . --list
```

To reinstall the local repository non-interactively for the global agent targets:

```bash
npx skills add . --yes --global
```

## Repository layout

```text
.
|-- README.md
`-- skills/
    `-- mpl-figure-generator/
        |-- SKILL.md
        |-- assets/
        |   |-- figure_request_template.md
        |   |-- style_registry.yaml
        |   `-- styles/
        |       `-- mps_base.mplstyle
        `-- references/
            |-- packaging-notes.md
            `-- source-compile.md
```

## Skill contents

- `skills/mpl-figure-generator/SKILL.md`
  Main skill contract, including triggers, prerequisites, input rules, workflow, and verification.
- `skills/mpl-figure-generator/assets/figure_request_template.md`
  Request template for plotting tasks and optional synthetic-data requests.
- `skills/mpl-figure-generator/assets/style_registry.yaml`
  Plot aliases, field rules, style-owned defaults, and label rules.
- `skills/mpl-figure-generator/assets/styles/mps_base.mplstyle`
  Canonical plotting style and export preset.
- `skills/mpl-figure-generator/references/source-compile.md`
  Historical source material retained for traceability.
- `skills/mpl-figure-generator/references/packaging-notes.md`
  Packaging decisions and maintenance notes.

## Invocation example

```text
Use the mpl-figure-generator skill.
Generate the requested figure directly and save the output artifacts in the repository.
```

Then provide the `<USER_MATERIALS>` block from `assets/figure_request_template.md`.
