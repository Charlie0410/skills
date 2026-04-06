# Protocol Principles

## Source-side mindset

- Treat `SOURCE_SPEC` as source code, not as a polished prompt.
- Recover task identity, deliverable shape, evidence boundary, and failure behavior before worrying about fluency.
- Preserve author intent, but do not preserve ambiguity as free prose when a typed field is needed.

## Intermediate representation

- Treat `NORMALIZED_SPEC` as a contract-bearing intermediate object.
- Keep three kinds of state visible:
- fixed field inventory
- resolved bindings
- unresolved states
- Normalize toward canonicalization, not paraphrase. Two semantically equivalent source descriptions should converge on the same normalized structure.

## Closed-world inference

- Infer only from the current `SOURCE_SPEC`, declared inheritance links, or stable repository/library defaults.
- Do not use open-domain world knowledge to patch task-defining facts.
- Prefer field presence over unsafe field value guessing.
- A safe move is often "introduce a slot"; an unsafe move is "invent the value."

## Evidence model

- Separate reliable evidence, approximate-only evidence, and excluded evidence.
- Let reliable evidence support exact values, exact wording, or direct claim attribution.
- Let approximate evidence support only bounded qualitative or approximate statements.
- Let excluded evidence support no formal claim unless later revalidated.
- When the source request says "use sources carefully," rewrite that into explicit evidence permissions and exclusions.

## Conservative failure

- Encode non-success behavior explicitly.
- When required evidence is missing, insufficient, contradictory, or below the requested claim resolution, prefer a conservative `FAILURE_POLICY` over fluent completion.
- Ask for the minimum additional material that would unblock safe execution.
- Do not let a polished artifact hide missing support.

## Constraint typing

- Classify requirements by operational effect, not by tone.
- Hard constraints define validity, safety, evidence limits, or interface compliance.
- Soft preferences rank otherwise lawful variants.
- Keep the two classes separate so later conflict resolution stays predictable.

## Conflict precedence

- Apply this precedence order when a lawful winner exists:
- hard constraint
- explicit local value
- inherited default
- inferred default
- placeholder
- Inside the same class, prefer task-local over family-level over library-level defaults.
- If there is no unique lawful winner, preserve the conflict instead of silently choosing.

## Stage splitting

- Do not collapse planning, drafting, verification, repair, and packaging into one normalized object unless the source spec explicitly wants a multi-stage task.
- When several independent artifacts or stages are mixed together, preserve a `SPLIT:` note in `OPEN_QUESTIONS`.
- Normalize one task per prompt whenever possible.

## Manuscript inheritance

- Inherit manuscript consistency through explicit dimensions:
- terminology
- notation
- units
- citation style
- section arrangement
- Do not rewrite "consistent with the manuscript" as a vague style-matching instruction.
- Convert it into named inheritance rules tied to the current task.
