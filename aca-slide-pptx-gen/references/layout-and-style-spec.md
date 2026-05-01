# Layout and Style Spec

## Canvas

Use PowerPoint widescreen dimensions:

- Width: `33.87cm`
- Height: `19.05cm`
- Safe outer margin: at least `1.0cm`
- Default content gap: at least `0.5cm`

Use OfficeCLI `layout=blank` for custom academic slides.

## Common Header

Place the section title and rule on every slide:

- Section title: `x=1.2cm`, `y=0.8cm`, `width=31.47cm`, `height=0.8cm`
- Section title font: `Calibri` for English, `Microsoft YaHei` for Chinese, `size=18`, `bold=true`, `color=111111`, `fill=none`
- Rule: `x=1.2cm`, `y=1.85cm`, `width=31.47cm`, `height=0.04cm`, `fill=1F2937`, `line=none`
- Main content region: `x=1.2cm`, `y=2.35cm`, `width=31.47cm`, `height=15.7cm`

## Typography

Set font properties explicitly. Do not rely on theme defaults.

- Academic title or main claim: `26pt` to `34pt`
- Panel heading: `18pt` to `22pt`
- Body text: `15pt` to `20pt`
- Captions: `12pt` to `15pt`
- Formula text: `18pt` to `26pt`, preferably `Cambria Math` or a math-friendly serif

Chinese text must use `微软雅黑` or `Microsoft YaHei`. English text must use `Calibri`.

## Colors

Use a white background unless the user provides a template or style requirement.

Required colors:

- Caption fill: `FFC000`
- Caption text: `000000`
- Blue emphasis: `0000AA`
- Red emphasis: `DE0000`
- Main text: `111111`
- Muted text: `4B5563`
- Separator: `1F2937`

Apply emphasis colors sparingly. Do not create a one-hue decorative palette.

## 2x2 Grid Style

Use for content with a ranked importance hierarchy.

Content region:

- Left column `x=1.2cm`, `width=15.18cm`
- Right column `x=17.49cm`, `width=15.18cm`
- Top row `y=2.35cm`, `height=7.35cm`
- Bottom row `y=10.7cm`, `height=7.35cm`
- Gap: `1.11cm` horizontal, `1.0cm` vertical

Semantic hierarchy:

- Quadrant 1, upper-left: supplementary content.
- Quadrant 2, upper-right: most important content.
- Quadrant 3, lower-left: supplementary content.
- Quadrant 4, lower-right: second-most important content.

Preserve this hierarchy even if exact coordinates are adjusted.

## 2xn Grid Style

Use for parallel results, comparisons, or figure-text pairs.

Rows:

- Visual row: `y=2.35cm`, `height=9.2cm`
- Text row: `y=12.05cm`, `height=6.0cm`
- Caption can sit inside the bottom of each visual panel or above the text row.

Column formula:

```text
usable_width = 31.47 - (n - 1) * 0.6
column_width = usable_width / n
column_x[i] = 1.2 + i * (column_width + 0.6)
```

Keep each visual panel aligned with its explanation. Reduce wording before reducing readability.

## Other Layouts

Use another sparse academic layout when it better fits the content:

- Hero figure plus right explanation panel.
- Left evidence panel plus right conclusion panel.
- Formula-centered derivation with side notes.
- Comparison table plus takeaway banner.

All variants must keep the header, rule, font requirements, caption styling, source policy, and 16:9 bounds.

## Shape Rules

Name important shapes at creation, for example `SectionTitle`, `TitleRule`, `MainClaim`, `Figure1`, `Caption1`, `Notes`.

Use stable `@name=` paths for follow-up edits when OfficeCLI supports them. Use `@id=` only after querying the current document.

Ensure every shape satisfies:

```text
x >= 0
y >= 0
x + width <= 33.87cm
y + height <= 19.05cm
```
