---
name: cpp-repair-prompt
description: Apply bounded REPAIR-stage corrections to a verified CPP draft prompt using SOURCE_SPEC, DRAFT_PROMPT, and VERIFY_REPORT. Use when Codex needs to repair a compiled CPP prompt after VERIFY has identified local defects, restore contract compliance, emit REPAIR_SUMMARY plus REPAIRED_PROMPT, preserve manuscript inheritance and defect provenance, and stay strictly within REPAIR instead of re-running NORMALIZE, COMPILE, or VERIFY.
---

# CPP Repair Prompt

## Overview

Patch a compiled CPP draft prompt and do only `REPAIR`. Consume the current `SOURCE_SPEC`, `DRAFT_PROMPT`, and `VERIFY_REPORT`, restore the smallest lawful set of local defects, and preserve explicit unresolved items when the defect really belongs to source revision, task splitting, or a fresh verification pass.

## Workflow

1. Read the minimum authoritative material needed.
   - Read the user request, `SOURCE_SPEC`, `DRAFT_PROMPT`, and `VERIFY_REPORT` first.
   - Always read the repo-native compiler spec:
     - `CPP_example/prompt_compiler/compiler.md`
   - Read the relevant template files as needed:
     - `CPP_example/prompt_compiler/full_template.md`
     - `CPP_example/prompt_compiler/lite_template.md`
   - Read explicitly referenced manuscript or global-rule files only when they are needed to preserve inherited terminology, notation, units, citation style, section arrangement, or source-policy overrides.
   - Read `references/repair-principles.md` as the compact rule source for manuscript-derived repair expectations.
   - Treat these files as rule sources; do not quote them into the output.

2. Establish repair authority and target.
   - `REPAIR` consumes a compiled prompt candidate plus a prior `VERIFY_REPORT`; it does not start from a free-form task request.
   - Treat `SOURCE_SPEC` as the task anchor, `DRAFT_PROMPT` as the editable target, and `VERIFY_REPORT` as the bounded defect list.
   - If `VERIFY_REPORT` is missing, out of schema, or clearly belongs to another draft, do not invent a replacement report; ask for the right artifact or switch back to `VERIFY`.
   - Identify whether the draft is operating as a `lite` or `full` profile, and preserve that profile unless the report shows a profile-level omission that can be repaired without changing task identity.

3. Repair locally, not globally.
   - Apply the smallest patch set that removes the highest-priority blocking defects first.
   - Prefer section-local edits, field restoration, ordering fixes, explicit placeholders, or control-surface repair over whole-prompt regeneration.
   - Keep unaffected sections, inherited rules, and naming stable unless a local edit necessarily touches them.
   - Treat "consistent with the manuscript" as explicit inheritance of terminology, notation, units, citation style, and section arrangement.
   - Keep instructions, policy, and runtime materials separated; do not let payload text become operative control text during repair.

4. Decide what may be repaired and what must be escalated.
   - Lawful local repairs include omitted field labels, wrong block order, missing but already-implied control surfaces, leaked runtime materials, over-constrained wording, stale placeholders that can be reinstated correctly, or drift that can be corrected without changing the source-side task.
   - Escalate instead of smoothing over when the defect requires new high-impact facts, task-family changes, new source permissions, conflicting source instructions, hidden multi-task decomposition, or a different visible return class.
   - If repeated repair would only recycle the same unsafe assumption under new wording, keep the issue unresolved and route it back to source revision or task splitting.

5. Preserve closed-world discipline.
   - Use only the current `SOURCE_SPEC`, `VERIFY_REPORT`, declared inheritance links, explicit library defaults, and the existing draft as authority.
   - Do not use open-domain knowledge to fill missing task facts.
   - If a missing value can remain lawfully unbound, restore or keep a placeholder rather than inventing content.
   - Repair may correct unsafe assumptions by removing them, weakening them back to placeholders, or relocating them into explicit unresolved items.

6. Emit provenance-preserving repair outputs.
   - `[REPAIR_SUMMARY]` must contain only the following fields, in this exact order:
   - `FIXES_APPLIED`
   - `UNRESOLVED_ITEMS`
   - Keep the summary shorter than the incoming `VERIFY_REPORT`; it records intervention state, not a second verification essay.
   - `[REPAIRED_PROMPT]` is the next release candidate. It may need a later `VERIFY` pass, but this skill should not append one.

## Output Contract

Do not default to pasting the repaired artifacts only in chat. Write the REPAIR-stage artifact to a file first, then respond in chat with the written path and concise status.

Write location and naming:

- If the user provided a primary input file, write the output artifact into that file's same directory.
- If the user provided an explicit output path, use that path.
- If the input exists only in chat, write into the current working directory.
- Default filename: `<source-stem>.repaired-prompt.md`; if no source filename exists, use `repaired-prompt.md`.
- If the target already exists, overwrite only when it is clearly a prior REPAIR-stage artifact or the user requested that path. Otherwise use a timestamped unique filename.

The file content must contain only these two blocks, in this fixed order:

```text
[REPAIR_SUMMARY]
FIXES_APPLIED:
UNRESOLVED_ITEMS:

[REPAIRED_PROMPT]
...
```

The final chat response must list the output file path, confirm the write, and summarize unresolved items. Do not paste the full `[REPAIR_SUMMARY]` or `[REPAIRED_PROMPT]` unless the user explicitly asks.

- Write `none` for empty but lawful slots.
- Keep labels and field order exactly aligned with `compiler.md`.
- Do not emit `[NORMALIZED_SPEC]`, `[COMPILATION_DIAGNOSTICS]`, `[COMPILED_PROMPT]`, or `[VERIFY_REPORT]`.
- Do not append explanatory prose before or after the two blocks inside the output file.

## Guardrails

- Treat `REPAIR` as bounded intervention, not as hidden recompilation from scratch.
- Correct hard defects before soft polishing.
- Preserve task objective, admissible evidence, visible return class, and conservative failure behavior unless the only lawful action is escalation.
- Do not renegotiate task identity, widen source permissions, or silently change the output contract.
- Keep defect ownership visible: source-side omissions stay unresolved, compilation drift is repaired locally if possible, and structural incompatibility is escalated rather than disguised.
- Do not output hidden reasoning.

## References

- Read `references/repair-principles.md` for manuscript-derived repair rules covering verify-before-repair, local revision before global integration, provenance-preserving summaries, escalation conditions, manuscript inheritance, and anti-drift maintenance.
- Always treat `CPP_example/prompt_compiler/compiler.md` and the CPP template files as the primary stage specification; the reference file compresses manuscript ideas but does not replace the source spec.
