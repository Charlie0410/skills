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

- Section title: `x=1.2cm`, `y=0.8cm`, `width=31.47cm`, `height=1.3cm`
- Section title font: `Calibri` for English, `Microsoft YaHei` for Chinese, `size=34`, `bold=true`, `color=111111`, `fill=none`
- Rule: connector line at `x=1.2cm`, `y=2.15cm`, `width=31.47cm`, `height=0cm`, `color=1F2937`, `linewidth=2pt`
- Main content region: `x=1.2cm`, `y=2.35cm`, `width=31.47cm`, `height=15.7cm`

The section title carries the slide's large visible title. The separator spans the full safe content width.

## Content Hierarchy

Plan each slide around one central information unit and one dominant evidence object. The default visible hierarchy is:

1. `SectionTitle`: large upper-left slide title.
2. `MainClaim` or equivalent message region: compact source-supported claim, question, or concise topic when appropriate.
3. `EvidenceVisual`: one main figure, chart, table, formula, mechanism diagram, or compact evidence block.
4. `EvidenceAnnotation`: labels, arrows, callouts, or highlighted values close to the evidence.
5. `Qualifier`: one short source-supported condition, limitation, or takeaway.

Do not give background, method, result, and conclusion equal visual weight on one slide. Move explainable details to speaker notes instead of shrinking visible text.

## Typography

Set font properties explicitly. Do not rely on theme defaults.

- Visible text floor: `18pt`. If content needs smaller text, reduce content or ask to split.
- Section title: `32pt` to `40pt`.
- Main claim/title when visible: `18pt` to `22pt`; complex slides may use a shorter visible topic or question.
- Panel heading: `24pt` to `32pt`.
- Normal body text: prefer `24pt` to `32pt`.
- Compact qualifiers and figure labels: `18pt` to `22pt`.
- Captions: `18pt+`, italic, no background fill by default.
- Formula text: `22pt` to `30pt`, preferably `Cambria Math` or a math-friendly serif; central equations should be larger than ordinary body text.

Chinese text must use `微软雅黑` or `Microsoft YaHei`. English text must use `Calibri`. Use left alignment for prose and line spacing around `1.3x` to `1.5x` for body text.

## Colors And Contrast

Use a white background unless the user provides a template or style requirement.

Default light academic colors:

- Background: `FFFFFF`
- Main text: `111827`
- Muted text: `64748B`
- Primary emphasis: `0B5CAD`
- Critical emphasis: `C2410C`
- Separator: `1F2937`

Legacy colors `FFC000`, `0000AA`, and `DE0000` may be used only when a supplied template, prior deck, or user request requires them. They are not required defaults.

Normal text and background contrast should be at least `4.5:1`. Large text and essential graphical objects should contrast at least `3:1` against adjacent colors.

Apply emphasis colors sparingly. Do not encode meaning by color alone; pair color with direct labels, marker shape, line style, pattern, annotation text, or grouping. Avoid red-green opposition as the only distinction.

## Evidence Rules

Charts require chart-ready data, complete variable names, units, categories, and clear labels. Choose the chart type from `chart_task`: category comparison, trend, relationship, distribution, composition, process, or key numeric result. Prefer direct labels on or near plotted objects; use a nearby legend only when direct labels would overcrowd the chart.

Tables should keep only columns needed for the central message. Use tables for compact exact-value comparisons; use charts when the viewer needs to compare magnitude, trend, or distribution. Put units in headers and highlight only one or two source-supported values.

Formula-focused slides should give the central equation readable size, whitespace, and nearby definitions or assumptions. Preserve original LaTeX when OfficeCLI equation conversion is uncertain.

Images should use original high-resolution or vector sources when available. Crop to the evidence-bearing region, avoid decorative images, set alt text, and repeat important embedded text in alt text or nearby accessible text.

## Preset Layouts

### `oral_light_assertion_evidence`

Default for most academic content slides:

- Main claim or message region: `x=1.2cm`, `y=2.35cm`, `width=31.47cm`, `height=2.8cm`
- Evidence region: `x=1.2cm`, `y=5.45cm`, `width=31.47cm`, `height=10.1cm`
- Caption/qualifier region: `x=1.2cm`, `y=15.9cm`, `width=31.47cm`, `height=2.15cm`

Use one dominant evidence object. Keep annotations close to the object they explain.

### `comparison_direct_label`

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

Keep each visual panel aligned with its explanation. Use direct labels or near legends. Reduce wording before reducing readability.

### `formula_evidence`

Use when a formula or derivation is the primary evidence:

- Message region: `x=1.2cm`, `y=2.35cm`, `width=31.47cm`, `height=2.6cm`
- Equation region: `x=3.0cm`, `y=5.3cm`, `width=20.5cm`, `height=6.5cm`
- Definitions region: `x=24.2cm`, `y=5.3cm`, `width=8.47cm`, `height=6.5cm`
- Qualifier region: `x=1.2cm`, `y=12.8cm`, `width=31.47cm`, `height=5.25cm`

Definitions and assumptions must sit near the equation and remain `18pt+`.

### `table_to_takeaway`

Use when a compact table supports one result:

- Message region: `x=1.2cm`, `y=2.35cm`, `width=31.47cm`, `height=2.6cm`
- Table region: `x=1.2cm`, `y=5.2cm`, `width=21.0cm`, `height=10.15cm`
- Takeaway region: `x=23.0cm`, `y=5.2cm`, `width=9.67cm`, `height=10.15cm`
- Caption/qualifier region: `x=1.2cm`, `y=15.75cm`, `width=31.47cm`, `height=2.3cm`

Drop nonessential columns rather than shrinking table text below the visible text floor.

### `2x2 Grid Style`

Use only when content truly has a ranked importance hierarchy.

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

## Shape Rules

Name important shapes at creation, for example `SectionTitle`, `MainClaim`, `EvidenceVisual`, `EvidenceAnnotation1`, `Caption1`, `Qualifier`, and `Notes`. OfficeCLI 1.0.67 connectors do not accept a stable `name` property; query connectors by ID when validating the separator.

Use stable `@name=` paths for follow-up edits when OfficeCLI supports them. Use `@id=` only after querying the current document.

If a text box needs a background color, set the fill on that text shape itself. Do not place a separate background rectangle behind text.

Related list items in the same visual block must be a single text shape with `list=bullet`, not one textbox per bullet.

Ensure every shape satisfies:

```text
x >= 0
y >= 0
x + width <= 33.87cm
y + height <= 19.05cm
```
