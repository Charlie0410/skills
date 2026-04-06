# Canonical Schema

## Field order

Emit fields in this exact order:

1. `TASK_NAME`
2. `TASK_FAMILY`
3. `DOMAIN`
4. `USER_INTENT`
5. `FINAL_DELIVERABLE`
6. `APPLY_GLOBAL_RULES_FROM`
7. `OUTPUT_LANGUAGE`
8. `AUDIENCE`
9. `SUCCESS_CRITERIA`
10. `AVAILABLE_INPUTS`
11. `REQUIRED_INPUTS`
12. `SOURCE_POLICY`
13. `HARD_CONSTRAINTS`
14. `SOFT_PREFERENCES`
15. `FAILURE_POLICY`
16. `FORMAT_REQUIREMENTS`
17. `OPTIONAL_EXAMPLES`
18. `OPEN_QUESTIONS`

## Field semantics

- `TASK_NAME`: Name the concrete task in a short, stable way.
- `TASK_FAMILY`: Identify the task archetype, such as extraction, rewrite, drafting, evaluation, or protocol compilation.
- `DOMAIN`: State the working domain only when it materially affects terminology, evidence, or format.
- `USER_INTENT`: State what the author is trying to achieve, stripped of rhetorical filler.
- `FINAL_DELIVERABLE`: Name the visible object to be returned at completion.
- `APPLY_GLOBAL_RULES_FROM`: Point to the governing global-rules source, or write `none`.
- `OUTPUT_LANGUAGE`: Bind only when explicit or safely inherited.
- `AUDIENCE`: State the intended consumer when it materially changes acceptable output.
- `SUCCESS_CRITERIA`: State what must be true for the task to count as done.
- `AVAILABLE_INPUTS`: List materials currently available.
- `REQUIRED_INPUTS`: List inputs that must exist for safe execution.
- `SOURCE_POLICY`: State source priority, admissible evidence, excluded evidence, and allowed transforms.
- `HARD_CONSTRAINTS`: List invariants, safety limits, evidence limits, and interface-defining prohibitions.
- `SOFT_PREFERENCES`: List reversible stylistic or ergonomic preferences.
- `FAILURE_POLICY`: State when to stop, downgrade, or ask for more material rather than guess.
- `FORMAT_REQUIREMENTS`: State schema, ordering, length control, and output-shape requirements.
- `OPTIONAL_EXAMPLES`: Include only when a strict or unstable schema benefits from one.
- `OPEN_QUESTIONS`: Keep unresolved but typed residual state visible.

## Formatting conventions

- Use a single scalar line for scalar fields.
- Use flat bullet lists for list-like fields.
- Write `none` for intentionally empty optional fields.
- Use `{{PLACEHOLDER_NAME}}` for unresolved required values.
- Use specific placeholders such as `{{WORD_RANGE}}`, `{{PRIMARY_RELIABLE_SOURCE}}`, `{{FINAL_DELIVERABLE}}`, or `{{OUTPUT_SCHEMA}}`.
- Avoid generic placeholders such as `{{TODO}}` or `{{MISSING}}`.

## OPEN_QUESTIONS tags

Use tagged bullets so unresolved state stays machine-scannable:

- `MISSING:` High-impact value is still absent.
- `ASSUMPTION:` Low-risk default or inheritance was applied.
- `CONFLICT:` Two or more bindings cannot be satisfied together.
- `SPLIT:` One request appears to contain several stages or several artifacts.

## Ambiguity rewrite patterns

- `brief`, `short`, `concise` -> introduce `TARGET_LENGTH` or `WORD_RANGE` inside `FORMAT_REQUIREMENTS`
- `detailed` -> introduce explicit coverage or subsection requirements
- `proper format` -> define schema, output order, or visible return class
- `use sources appropriately` -> define source priority, allowed evidence, excluded evidence, and allowed transforms
- `keep consistent with the manuscript` -> define terminology, notation, unit, citation-style, or section-arrangement inheritance
- `do not hallucinate` -> define forbidden unsupported claims plus conservative `FAILURE_POLICY`

## Worked mini-example

Source-side input:

```text
Write a brief journal-style paragraph from the uploaded materials.
Keep terminology consistent with the manuscript.
Use sources carefully.
```

Normalized shape:

```text
[NORMALIZED_SPEC]
TASK_NAME: draft-results-paragraph
TASK_FAMILY: drafting
DOMAIN: academic writing
USER_INTENT: Draft one journal-style paragraph grounded in the provided materials.
FINAL_DELIVERABLE: one results paragraph
APPLY_GLOBAL_RULES_FROM: none
OUTPUT_LANGUAGE: {{OUTPUT_LANGUAGE}}
AUDIENCE: journal readers in the target field
SUCCESS_CRITERIA:
- Return one publishable paragraph.
- Preserve manuscript terminology.
- Keep every claim inside the declared source policy.
AVAILABLE_INPUTS:
- uploaded materials
- current manuscript
REQUIRED_INPUTS:
- manuscript terminology source
- claim-bearing source materials
SOURCE_POLICY:
- Exact claims require declared reliable evidence.
- Unsupported claims are forbidden.
HARD_CONSTRAINTS:
- Preserve manuscript terminology.
- Do not invent missing claim-bearing facts.
SOFT_PREFERENCES:
- Keep prose compact and journal-like.
FAILURE_POLICY:
- If reliable claim-bearing material is insufficient, stop and request the missing source instead of drafting unsupported claims.
FORMAT_REQUIREMENTS:
- TARGET_LENGTH: {{WORD_RANGE}}
- Return mode should remain compatible with final paragraph delivery.
OPTIONAL_EXAMPLES: none
OPEN_QUESTIONS:
- ASSUMPTION: output language may inherit from the manuscript if the manuscript language is clear.
- MISSING: precise word range for "brief" is unspecified.
- MISSING: reliable evidence class is not yet declared.
```
