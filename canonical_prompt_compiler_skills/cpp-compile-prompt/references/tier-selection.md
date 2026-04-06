# Tier Selection

## Core Rule

- `lite` and `full` are not cosmetic variants.
- `lite` assumes the main risk is surface drift.
- `full` assumes the main risk is evidential overreach, missing control surfaces, or failure to stop when materials are insufficient.
- Choose the lighter tier only when it still preserves the task's actual safety and evidence contract.

## Choose Lite When

- The task mostly rewrites, compresses, reformats, or classifies trusted material.
- The output can be checked line by line with little interpretation.
- The author already controls the factual content.
- The task does not need explicit source ranking, approximation discipline, or conservative insufficiency handling.

Typical patterns:

- highlight rewriting
- concise conclusion extraction from trusted text
- reference-format normalization
- low-risk restructuring of already trusted materials

## Choose Full When

- The task must rank or separate sources.
- The task must distinguish reliable evidence from approximate-only evidence.
- The task must preserve manuscript terminology or other inheritance dimensions while synthesizing.
- The task must refuse unsupported claims or sometimes return an insufficiency branch.
- The prompt needs explicit `SOURCE_POLICY`, `FAILSAFE`, or `VERIFICATION` sections to remain lawful and reviewable.

Typical patterns:

- evidence-sensitive drafting
- synthesis across manuscript fragments and references
- terminology or notation audits
- tasks where some materials are qualitative-only or excluded

## Escalate From Lite To Full When

- source priority has to be repeated in several scattered sentences
- precise values must be separated from approximate readings
- some files are usable only for qualitative context
- the safest legal outcome is sometimes an explicit insufficiency report
- manuscript inheritance needs more than a casual reminder

At that point, named control surfaces are cleaner and safer than patching a lite template with warnings.

## Section-Level Implications

- `lite` may omit:
  - `SOURCE_POLICY`
  - `FAILSAFE`
  - `VERIFICATION`
- `full` should include these sections when the task's legality or reviewability depends on them.
- Do not smuggle full-tier behavior into `lite` by adding ad hoc prose fragments everywhere.
- If those sections are operationally required, the task is a `full` compile.

## Pair Maintenance

- When both tiers are plausible, prefer the narrowest lawful one.
- If the task later accumulates evidence handling, insufficiency rules, or inheritance controls, promote it from `lite` to `full`.
- A shorter prompt is not a better compile if it hides the true control surface.
