# Layout and style specification

## Canvas

Use one fixed 16:9 canvas. Preferred dimensions are `1600px × 900px`; `1280px × 720px` is acceptable when requested by the user. Keep all content within the visible slide canvas.

## Typography

Use `Calibri` for English text. Use `微软雅黑` for Chinese text. For mixed-language text, apply `lang` attributes or local classes to preserve the required fonts.

## Required title treatment

The section title must appear at the upper-left. A horizontal separator must appear below the section title.

## Captions and emphasis

Figure captions must use background `#ffc000` and text color `#000000`.

Emphasis colors must include `#0000AA` and `#DE0000`. Apply them only to meaningful terms, measured values, results, conclusions, or user-specified emphasis requests.

## Layout selection

### 2x2 Grid style

Use for hierarchical content. Quadrant priority is fixed:

1. Quadrant 2: most important content.
2. Quadrant 4: second-most important content.
3. Quadrants 1 and 3: supplementary content.

### 2xn Grid style

Use for parallel comparisons and figure-result pairs. Row 1 contains visual result panels. Row 2 contains aligned text explanations, findings, labels, or captions.

### Other layouts

Allowed alternatives include a hero figure with explanation panel, evidence-conclusion split, formula-centered derivation, and comparison table with takeaway banner. These variants must stay sparse and academic.
