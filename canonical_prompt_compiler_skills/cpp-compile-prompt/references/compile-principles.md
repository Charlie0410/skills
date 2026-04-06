# Compile Principles

## Stage Identity

- Treat `COMPILE` as target-side lowering from a lawful source-side task to a reusable prompt artifact.
- The active branch owns translation, not source-side canonicalization, release judgment, or prompt repair.
- `SOURCE_SPEC` remains foundational, but the preferred operative input is `[NORMALIZED_SPEC]`.
- If normalized state must be reconstructed internally, keep that work hidden as preparation and keep the visible output stage-pure.

## Artifact Boundaries

- The visible outputs of this stage are:
  - `[COMPILATION_DIAGNOSTICS]`
  - `[COMPILED_PROMPT]`
- Do not emit `NORMALIZE`, `VERIFY`, or `REPAIR` artifacts from this skill.
- Conceptually, the compiled artifact is the reusable canonical prompt; visibly, keep the label `[COMPILED_PROMPT]` to match `compiler.md`.

## Translation-State Diagnostics

- `COMPILATION_DIAGNOSTICS` is a translation-state report, not a release-state report.
- Keep these slots distinct:
  - `COMPLETENESS`: whether the task can be compiled without hiding blocking gaps
  - `TASK_FAMILY`: the operative task archetype after normalization-compatible lowering
  - `INFERRED_DEFAULTS`: reversible low-risk bindings introduced during compilation
  - `MISSING_FIELDS`: high-impact blanks that remain unresolved
  - `CONFLICTS`: requirements that cannot lawfully coexist
  - `ASSUMPTIONS`: narrower provisional bridges carried forward explicitly
  - `SPLIT_RECOMMENDATION`: cases where several tasks or deliverables are compressed together
  - `READINESS`: whether the compiled artifact is ready as-is, blocked, or conditionally usable
- Do not collapse these categories into one generic issues list.

## Closed-World Lowering

- Infer only from the present request, current source or normalized materials, declared inheritance links, and stable repository defaults.
- Do not use open-domain world knowledge to fill task-defining facts.
- Prefer introducing a placeholder over inventing a high-impact value.
- A safe move is often structural:
  - adding the needed field
  - selecting `full` because the task needs explicit control surfaces
- An unsafe move is semantic invention:
  - guessing the reliable evidence class
  - deciding the final deliverable when the request is mixed
  - silently binding the source priority core

## Conservative Handling Of Missingness

- Missing high-impact information should remain visible through placeholders and diagnostics.
- If the task can still be lowered lawfully, compile a bounded artifact and expose the unresolved state.
- If a lawful single-task lowering does not exist, preserve that fact in `CONFLICTS` or `SPLIT_RECOMMENDATION` instead of smoothing it away.
- Compilation may remain usable while still carrying visible unresolved state.

## Manuscript Inheritance

- Treat manuscript consistency as explicit inheritance, not vague style matching.
- Preserve, when requested or clearly inherited:
  - terminology
  - notation
  - units
  - citation style
  - section arrangement
- Keep these inheritance rules inside the compiled prompt contract, not as loose prose reminders.

## Separation From Later Stages

- `COMPILE` should not emit release judgments like pass or fail.
- `COMPILE` should not patch an existing prompt under verification defects.
- If the source-side task is underdetermined, compile conservatively and record why.
- Let later `VERIFY` and `REPAIR` stages handle release judgment and bounded intervention.
