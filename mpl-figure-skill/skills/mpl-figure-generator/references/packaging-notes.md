# Packaging Notes

This skill started as an instruction-packet compiler and was later revised into a direct figure-generation skill, now published under the clearer name `mpl-figure-generator`.

Current packaging decisions:

1. Keep the historical source prompt in `references/source-compile.md` for traceability only.
2. Use `SKILL.md` to define the direct plotting workflow, runtime prerequisites, and validation rules.
3. Keep the canonical mplstyle file under `assets/styles/` and treat it as the default source of truth for figure size and export settings.
4. Keep the user-facing request template under `assets/figure_request_template.md`.
5. Require a LaTeX runtime because the canonical style enables `text.usetex`.

Recommended future edits:

1. Add a second style file only if there is a real need for an alternate export preset.
2. Keep new plot families behind explicit schema rules before advertising them in the trigger description.
3. Add reference examples for recurring label conventions if the current square-bracket unit rule proves too implicit for new users.
