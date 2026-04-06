# Verify Principles

## Verification As A Gate

- Treat verification as the gate before a prompt artifact is promoted for reuse.
- Promote only validated artifacts; keep draft artifacts local to the current stage.
- A warning that does not change release behavior is not a substitute for real verification.

## Typed Defect Classification

- Separate hard release blockers from softer fit-and-finish notes.
- Use typed buckets instead of generic warning prose:
  - faithfulness loss
  - ambiguity left unresolved
  - overreach
  - missing constraints
  - format defects
  - unsafe assumptions
- Let the defect type explain what failed, not just that something feels off.

## Source And Evidence Discipline

- Check whether the draft preserves the intended evidence boundary from the source-side task.
- In source-sensitive tasks, verify that exact claims are only authorized by reliable evidence classes.
- Treat invented source priority, invented allowed evidence, or invented exclusions as blocking overreach.
- Check boundary discipline: policy lives in policy sections, runtime materials live in payload sections, and examples stay optional unless the contract requires them.

## Conservative Failure

- A lawful draft must say what happens when materials are insufficient whenever the task family requires that control surface.
- Warning language without an actionable stop path is not enough for a source-sensitive or high-risk prompt.
- If the draft weakens or removes conservative failure behavior that the task depends on, fail the artifact rather than excusing the omission.

## Structural Validation

- Verify contract structure before sentence polish.
- Required sections should appear once, in the expected order, with the expected visible labels.
- Prefer structural validation over line-by-line wording diff; a one-line change inside `SOURCE_POLICY` or `FAILSAFE` can matter more than large cosmetic rewrites elsewhere.
- Treat the visible return class and payload envelope as contract surface, not incidental formatting.

## Contract Regression Mindset

- Evaluate the prompt as a reusable interface, not as a one-off prose sample.
- Focus on observable contract behavior:
  - required sections
  - return mode
  - evidence permissions
  - conservative-failure behavior
  - inheritance behavior
- A draft passes when these contract elements still hold, even if wording changed.
- A draft fails when any of these contract elements drift in a way that changes lawful downstream use.
