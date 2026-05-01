---
name: cpp-compile-prompt
description: Compile a CPP NORMALIZED_SPEC or source-side task spec into COMPILE-stage artifacts for the Canonical Prompt Protocol. Use when Codex needs to compile or lower a task into a reusable prompt, choose between lite and full CPP templates, emit COMPILATION_DIAGNOSTICS plus COMPILED_PROMPT, preserve manuscript terminology and evidence boundaries, and stay strictly within COMPILE instead of NORMALIZE, VERIFY, or REPAIR.
---

# CPP Compile Prompt

## Overview

Lower a CPP task specification into a reusable target prompt and do only `COMPILE`. Prefer `[NORMALIZED_SPEC]`; if only `SOURCE_SPEC` or an equivalent free-form task description is available, reconstruct an equivalent normalized state internally, but keep the visible output limited to `[COMPILATION_DIAGNOSTICS]` and `[COMPILED_PROMPT]`.

## Workflow

1. Read the minimum authoritative material needed.
   - Read the user request and the current inputs first.
   - Always read the repo-native compiler spec:
     - `CPP_example/prompt_compiler/compiler.md`
   - Read templates as needed:
     - `CPP_example/prompt_compiler/full_template.md`
     - `CPP_example/prompt_compiler/lite_template.md`
   - Read this skill's references as needed:
     - `references/compile-principles.md`
     - `references/tier-selection.md`
   - Do not copy large passages from these files into the output; treat them as rule sources.

2. Establish the authoritative compile-stage input.
   - Treat `[NORMALIZED_SPEC]` as the preferred authoritative compile input.
   - If `[NORMALIZED_SPEC]` is missing but `SOURCE_SPEC`, a free-form task description, or a declared inheritance chain is present, reconstruct an equivalent normalized state internally.
   - That internal reconstruction must follow closed-world inference, preserve high-impact missing fields, and keep conflicts and stage-splitting suggestions explicit.
   - Even when reconstruction is needed, do not additionally emit `[NORMALIZED_SPEC]` unless the user explicitly asks to switch to `NORMALIZE`.

3. Determine task boundaries and compilability.
   - Each compile run should produce one primary task prompt.
   - If the input actually mixes several independent tasks, deliverables, or source policies, keep one primary task and record the decomposition advice in `SPLIT_RECOMMENDATION`.
   - If high-impact fields are missing, task identity conflicts, or evidence boundaries cannot be lawfully bound, do not pretend the task is fully compiled; keep the issue in diagnostics and preserve auditability through placeholders or conservative bindings.

4. Choose the `lite` or `full` template.
   - Use `references/tier-selection.md` to decide.
   - `lite` is for low-interpretation rewriting, compression, restructuring, or classification over trusted material.
   - `full` is for tasks that need source ranking, evidence stratification, manuscript inheritance, conservative insufficiency behavior, or explicit `SOURCE_POLICY` / `FAILSAFE` / `VERIFICATION` control surfaces.
   - If `lite` only remains viable because warnings keep accumulating in scattered prose, upgrade to `full` instead of patching in full-tier rules sentence by sentence.

5. Perform the lowering compile step.
   - Lower the task into the chosen template, bind the stable structure, and preserve unresolved high-impact state.
   - Keep terminology, notation, units, naming, and citation style consistent with the `SOURCE_SPEC` or reconstructed normalized state.
   - Turn "stay consistent with the manuscript" into explicit inheritance dimensions: terminology, notation, units, citation style, and section arrangement.
   - Separate long-lived global rules from task-local rules; if a global rules file already exists, prefer keeping the reference instead of inlining the whole text.
   - Separate instructions from runtime materials; runtime materials must remain inside dedicated payload blocks.
   - In the `full` template, explicitly generate control surfaces such as `SOURCE_POLICY`, `FAILSAFE`, and `VERIFICATION`.
   - Keep the `lite` template lightweight; if those control surfaces become necessary for lawful execution, upgrade to `full`.

6. Emit fixed-order compilation diagnostics.
   - `[COMPILATION_DIAGNOSTICS]` must contain only the following fields, in this exact order:
   - `COMPLETENESS`
   - `TASK_FAMILY`
   - `INFERRED_DEFAULTS`
   - `MISSING_FIELDS`
   - `CONFLICTS`
   - `ASSUMPTIONS`
   - `SPLIT_RECOMMENDATION`
   - `READINESS`
   - These fields record translation-state facts from compilation, not release judgments or repair advice.

7. Emit the compiled prompt.
   - `[COMPILED_PROMPT]` is the visible output label and must stay aligned with `compiler.md`.
   - Conceptually, it can be treated as the `CANONICAL_PROMPT`, but do not rename the visible section.
   - Do not append extra explanatory prose, out-of-mode reports, or hidden reasoning.

## Output Contract

Do not default to pasting the compiled artifacts only in chat. Write the compile-stage artifact to a file first, then respond in chat with the written path and concise status.

Write location and naming:

- If the user provided a primary input file, write the output artifact into that file's same directory.
- If the user provided an explicit output path, use that path.
- If the input exists only in chat, write into the current working directory.
- Default filename: `<source-stem>.compiled-prompt.md`; if no source filename exists, use `compiled-prompt.md`.
- If the target already exists, overwrite only when it is clearly a prior COMPILE-stage artifact or the user requested that path. Otherwise use a timestamped unique filename.

The file content must contain only these two blocks, in this fixed order:

```text
[COMPILATION_DIAGNOSTICS]
COMPLETENESS:
TASK_FAMILY:
INFERRED_DEFAULTS:
MISSING_FIELDS:
CONFLICTS:
ASSUMPTIONS:
SPLIT_RECOMMENDATION:
READINESS:

[COMPILED_PROMPT]
...
```

The final chat response must list the output file path, confirm the write, and summarize readiness. Do not paste the full `[COMPILATION_DIAGNOSTICS]` or `[COMPILED_PROMPT]` unless the user explicitly asks.

- Write `none` for empty but lawful slots.
- Use precise placeholders for required but unbound high-impact values, such as `{{OUTPUT_LANGUAGE}}` or `{{PRIMARY_RELIABLE_SOURCE}}`.
- Do not emit `[NORMALIZED_SPEC]`, `[VERIFY_REPORT]`, `[REPAIR_SUMMARY]`, or `[REPAIRED_PROMPT]`.

## Guardrails

- Treat `COMPILE` as a translation stage, not a review stage or a repair stage.
- Do not silently invent high-impact information such as task identity, final deliverable, core source-priority rules, key required inputs, or the visible return class.
- Low-risk, reversible, and recordable bindings are allowed; record all such bindings under `INFERRED_DEFAULTS` or `ASSUMPTIONS`.
- If there is no single lawful binding, preserve `CONFLICTS` or `SPLIT_RECOMMENDATION` instead of choosing silently.
- Do not let `VERIFY` language leak into `COMPILE` output, and do not mix in `REPAIR`-style opportunistic edits.
- Do not output hidden reasoning.

## References

- Read `references/compile-principles.md` for `COMPILE`-stage boundaries, diagnostic types, closed-world inference, and manuscript inheritance principles.
- Read `references/tier-selection.md` to decide between `lite` and `full` and to identify escalation conditions.
- Always treat the repo's `compiler.md` and template files as the primary specification; this skill's reference files only compress manuscript ideas and do not replace the source spec.
