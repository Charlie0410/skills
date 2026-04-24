# aca-slide-gen

This package contains a Codex skill for generating single-slide academic presentation pages as self-contained 16:9 HTML documents.

## Contents

- `SKILL.md`: required Codex skill manifest and operating instructions.
- `assets/slide-template.html`: reusable HTML scaffold with the required canvas, typography, caption, and emphasis styles.
- `references/input-contract.md`: field-level input specification.
- `references/layout-and-style-spec.md`: layout and visual specification.
- `references/verification-checklist.md`: pre-return checks.
- `scripts/validate_slide_html.py`: dependency-free validation helper for generated slide HTML.

## Basic validation

Run:

```bash
python scripts/validate_slide_html.py assets/slide-template.html
```

The validator checks for required structural, typography, color, and dependency markers. It does not replace visual inspection for dense slides.
