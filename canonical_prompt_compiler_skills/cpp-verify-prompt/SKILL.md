---
name: cpp-verify-prompt
description: Verify a compiled CPP draft prompt against its SOURCE_SPEC, prompt profile, and protocol grammar. Use when Codex needs to review a CPP prompt artifact at the VERIFY stage, emit a [VERIFY_REPORT], check faithfulness to source intent, detect ambiguity left unresolved, constraint loss, overreach, missing control surfaces, unsafe assumptions, or format defects, and stay strictly within VERIFY rather than COMPILE or REPAIR.
---

# CPP Verify Prompt

## Overview

Evaluate a compiled CPP prompt artifact and do only `VERIFY`. Read the current `SOURCE_SPEC`, the candidate `DRAFT_PROMPT`, and the authoritative CPP spec, then decide whether the draft still matches source intent, inherited constraints, evidence boundaries, and the required prompt structure.

## Workflow

1. Read the minimum authoritative material needed.
   - Read the user request, `SOURCE_SPEC`, and `DRAFT_PROMPT` first.
   - Always read the repo-native compiler spec:
     - `CPP_example/prompt_compiler/compiler.md`
   - Read the relevant template files as needed:
     - `CPP_example/prompt_compiler/full_template.md`
     - `CPP_example/prompt_compiler/lite_template.md`
   - Read explicitly referenced manuscript or global-rule files only when they are needed to judge inherited terminology, evidence boundaries, or local overrides.
   - Read `references/verify-principles.md` as the compact rule source for manuscript-derived verification expectations.
   - Treat these files as rule sources; do not quote them into the output.

2. Establish the verification target.
   - `VERIFY` consumes a compiled draft prompt artifact, not a source-side normalization or compilation request.
   - Identify whether the draft is operating as a `full` or `lite` profile by its visible structure and control surfaces.
   - If the draft mixes several profiles, collapses multiple stages, or omits the information needed to identify its profile, record that as a defect instead of guessing.

3. Check source faithfulness before stylistic quality.
   - Compare the draft against the current `SOURCE_SPEC`, inherited global rules, and any explicitly inherited manuscript constraints.
   - Treat task identity drift, lost hard constraints, weakened evidence limits, changed visible return shape, and broken manuscript inheritance as `FAITHFULNESS_ISSUES`.
   - Treat unresolved placeholders, vague control surfaces, or missing upstream context that still blocks safe judgment as `AMBIGUITY_LEFT`.
   - Treat invented source hierarchy, invented stop conditions, invented required inputs, invented return modes, or invented permissions as `OVERREACH`.
   - Treat profile-required but absent controls as `MISSING_CONSTRAINTS`.
   - Treat a provisional low-risk default that hardened into a high-impact commitment as an `UNSAFE_ASSUMPTION`.

4. Validate structure and boundary discipline.
   - Check required block presence, order, single occurrence, and visible labels against the applicable prompt template.
   - For `full` drafts, verify that `SOURCE_POLICY`, `FAILSAFE`, and `VERIFICATION` exist when the task is source-sensitive or high-risk.
   - For `lite` drafts, keep the structure lean; if lawful execution actually depends on `SOURCE_POLICY`, `FAILSAFE`, or `VERIFICATION`, record the mismatch as a defect instead of treating the draft as compliant.
   - Check that long-lived rules stay in policy sections or inherited rule references.
   - Check that runtime materials stay inside payload blocks rather than leaking into executable policy text.
   - Check that optional exemplars remain optional unless the source or schema makes them necessary.
   - Record structural, ordering, duplication, or envelope defects under `FORMAT_DEFECTS`.

5. Decide release status and bounded repair priority.
   - Use `FAIL` when any hard-constraint loss, blocking structure defect, unsafe high-impact invention, missing required control surface, or missing conservative-failure behavior makes the draft not lawfully reusable.
   - Use `PASS_WITH_NOTES` when the task contract still holds but soft-preference drift, weaker manuscript fit, or non-blocking cleanup remains.
   - Use `PASS` only when no blocking or notable issues remain.
   - Write `REPAIR_PRIORITY` as the smallest bounded fixes in descending severity order; do not rewrite the prompt.

## Output Contract

Return only this block, in this exact order:

```text
[VERIFY_REPORT]
STATUS: {PASS | FAIL | PASS_WITH_NOTES}
FAITHFULNESS_ISSUES:
AMBIGUITY_LEFT:
OVERREACH:
MISSING_CONSTRAINTS:
FORMAT_DEFECTS:
UNSAFE_ASSUMPTIONS:
REPAIR_PRIORITY:
```

- Write `none` for empty but lawful slots.
- Keep the field order exactly aligned with `compiler.md`.
- Do not append extra explanatory prose before or after the report.
- Do not emit `[NORMALIZED_SPEC]`, `[COMPILATION_DIAGNOSTICS]`, `[COMPILED_PROMPT]`, `[REPAIR_SUMMARY]`, or `[REPAIRED_PROMPT]`.

## Guardrails

- Treat `VERIFY` as a release-gate stage, not as a rewrite, compile, or repair stage.
- Do not silently fix, regenerate, or recompile the draft prompt.
- Prefer structural and evidence-boundary checks over line-by-line prose comparison.
- Judge hard constraints before soft preferences; hard defects block release, soft drift becomes notes.
- If the upstream materials are too incomplete for a faithful judgment, fail conservatively and record the unresolved state instead of guessing.
- Do not invent missing source facts, source rankings, failure thresholds, or return semantics during verification.
- Keep manuscript consistency explicit through named inheritance dimensions such as terminology, notation, units, citation style, and section arrangement.
- Do not output hidden reasoning.

## References

- Read `references/verify-principles.md` for manuscript-derived verification rules covering release gating, source discipline, conservative failure, typed defect classification, and contract-level validation.
- Always treat `CPP_example/prompt_compiler/compiler.md` and the CPP template files as the primary stage specification; the reference file compresses manuscript ideas but does not replace the source spec.
