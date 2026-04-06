# Repair Principles

## Stage Identity And Authority

- `REPAIR` is the only CPP stage allowed to edit a compiled prompt directly.
- Its authoritative inputs are `SOURCE_SPEC`, `DRAFT_PROMPT`, and `VERIFY_REPORT`.
- The stage remains narrow: patch bounded defects; do not renegotiate task identity or invent source-side facts.
- The stage output is a concise intervention record plus the next prompt candidate.

## Verify Before Repair

- Repair only after a typed `VERIFY_REPORT` exists.
- Do not merge judging and editing into one opaque action.
- Let the report define defect ownership and repair priority.
- If the report is missing or mismatched, stop or return to verification rather than fabricating a repair target.

## Local Revision Before Global Integration

- Prefer the smallest artifact region that still owns the defect.
- Section-local repair preserves traceability and reduces accidental contract drift.
- Fix local defects before they are buried under later integration or append-only patching.
- If the defect crosses task boundaries or parent structure, escalation is more honest than a broad rewrite.

## Repair Order

- Restore contractual compliance before stylistic improvement.
- Hard defects come first:
  - lost hard constraints
  - widened evidence permissions
  - broken return shape
  - missing conservative-failure behavior
  - missing required labels or sections
- Soft polish comes later and only if it does not expand authority or rewrite stable sections.
- A correct placeholder is better than a fluent invention.

## Closed-World And Missingness Discipline

- Absence is never permission to guess high-impact values.
- Remove unsafe assumptions when the source does not authorize them.
- Carry forward unresolved missing items or conflicts explicitly.
- A repair may demote an unsafe default back into a placeholder or unresolved item.

## Preserve Structured Separation

- Keep policy, workflow, output contract, and runtime materials in their own sections or blocks.
- Do not let examples, reviewer comments, or payload text acquire directive force.
- Use one core role plus at most one bounded domain specialization; move output or evidence rules out of persona text.
- Avoid append-only clause accumulation that buries governing instructions inside local patches.

## Provenance And Summary Discipline

- `REPAIR_SUMMARY` should be short, typed, and limited to what changed and what remains unresolved.
- The point is to make the delta inspectable and support rollback or regression comparison.
- Do not rewrite the verification report in narrative form.
- Preserve enough lineage that a later reviewer can tell whether a defect came from source omissions, compile drift, or local repair choices.

## Escalation Triggers

- Escalate when the fix would require new high-impact task facts.
- Escalate when the visible return class, task family, or admissible evidence boundary would change.
- Escalate when a nominally local defect is really a concealed multi-task or stage-splitting problem.
- Escalate when repeated repair without new information would only restate the same unsafe assumption.

## Manuscript Inheritance And Maintenance

- Treat manuscript consistency as explicit inheritance of terminology, notation, units, citation style, and section arrangement.
- Preserve stable contract surfaces across revisions:
  - task objective
  - evidence permissions
  - visible return class
  - conservative failure behavior
- A local repair that changes these surfaces is not a patch-like fix; it is a migration or redesign decision.
- Prefer artifact-based diffs over prose memory when deciding what changed.
