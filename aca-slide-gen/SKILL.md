---
name: aca-slide-gen
description: Generate one self-contained 16:9 academic main-content presentation slide as HTML from user-provided research text, figures, data, formulas, and reference context. Use for PowerPoint-style academic content slides. Decline cover pages, table-of-contents pages, and thank-you pages as out of scope.
---

# aca-slide-gen

## Purpose

Use this skill to create one academic presentation main-content slide as a complete, self-contained HTML document. The slide must fit a single 16:9 canvas and must use the user’s supplied academic content faithfully.

This skill is scoped to main-content slides only. It must decline or redirect requests for cover pages, table-of-contents pages, and thank-you pages.

## Expected inputs

Accept user requests expressed in prose or in structured fields. Extract the following input contract when available:

```json
{
  "section_title": "required string, short section label placed at the upper-left",
  "topic": "required string, main slide topic or message",
  "text": "required unless equivalent structured content is supplied",
  "figures": "optional array or description of image paths, figure descriptions, references, or placement requests",
  "data": "optional tables, numeric values, result summaries, or chart-ready data",
  "formulas": "optional LaTeX formulas or math notation",
  "reference_context": "optional manuscript excerpts, paper context, report notes, terminology constraints, notation, units, or style constraints",
  "language": "optional output language; infer from request and source content when absent",
  "layout_preference": "optional: 2x2 Grid style, 2xn Grid style, or other",
  "emphasis_requests": "optional terms, claims, results, formulas, or visual elements requiring emphasis"
}
```

Required minimum content is `section_title`, `topic`, and either `text` or equivalent structured content. If the request lacks enough academic content to produce a faithful slide, ask only for the minimum missing material.

## Source policy

Treat user-provided topic, text, figures, data, formulas, and reference context as the authoritative content source.

Preserve factual claims, terminology, notation, units, formulas, and academic framing. Do not invent paper claims, numeric results, figure labels, chart values, experimental conditions, formula terms, or conclusions.

Use figure placeholders only when the user provides enough descriptive content and no image asset is available. Label placeholders clearly, for example `Figure placeholder: [provided figure description]`.

Use a textual representation or clearly labeled placeholder when the user asks for a chart or visual comparison without enough data. If explanation is allowed, state the minimum missing data needed.

Keep LaTeX source intact. When external dependencies are disallowed or unspecified, preserve formulas inside `$...$`, `\(...\)`, or `\[...\]` delimiters and optionally wrap them in semantic containers such as `<div class="formula">`. Use MathJax or another external renderer only when the user explicitly permits external dependencies.

## Workflow

1. Confirm the request is for an academic main-content slide.
2. Decline cover pages, table-of-contents pages, and thank-you pages with a concise scope statement.
3. Extract `section_title`, `topic`, `text`, `figures`, `data`, `formulas`, `reference_context`, `language`, `layout_preference`, and `emphasis_requests`.
4. Identify the slide’s central message from the supplied material.
5. Select the layout:
   - `2x2 Grid style` for content with a ranked importance hierarchy.
   - `2xn Grid style` for parallel results, comparisons, or figure-text pairs.
   - `other` when a sparse academic layout better fits the content.
6. Compose one self-contained HTML document with embedded CSS.
7. Keep all content inside one 16:9 visible canvas.
8. Apply the required visual rules.
9. Internally run the verification checklist.
10. Return only the complete HTML document unless the user explicitly asks for explanation.

## Required visual rules

Place `section_title` at the upper-left of the slide. Add a horizontal separation line directly below it.

Use `微软雅黑` for Chinese text. Use `Calibri` for English text. For mixed-language content, use `lang` attributes or local spans so Chinese and English text can use the required fonts.

Use concise figure captions. Style captions with background `#ffc000` and text color `#000000`.

Use `#0000AA` and `#DE0000` as the available emphasis colors. Apply emphasis sparingly to important terms, measured values, conclusions, or formulas specified by the user.

Use sparse decoration. Prioritize readability, whitespace, consistent spacing, and clear hierarchy.

## Layout rules

### 2x2 Grid style

Use a four-quadrant layout when the content has a clear importance hierarchy. Treat quadrants as:

- Quadrant 1: upper-left, supplementary content.
- Quadrant 2: upper-right, most important content.
- Quadrant 3: lower-left, supplementary content.
- Quadrant 4: lower-right, second-most important content.

Preserve this hierarchy even if CSS grid coordinates vary.

### 2xn Grid style

Use this layout for parallel results, comparison panels, or figure-result pairs.

- Row 1: figures, charts, diagrams, or visual result panels.
- Row 2: text explanations, labels, findings, or concise captions.

Keep each column visually matched across both rows. Use the number of columns required by the supplied material. Reduce text density before reducing readability.

### Other layouts

Use another sparse academic layout when it better serves the supplied content, such as:

- single hero figure plus explanation panel
- left evidence panel plus right conclusion panel
- formula-centered derivation slide
- comparison table plus takeaway banner

All variants must obey the visual rules and source policy.

## HTML output contract

Return exactly one complete HTML document per slide.

The document must include:

- `<!doctype html>` and a single `<html>` root.
- Embedded CSS inside `<style>`.
- A fixed 16:9 slide canvas, preferably `1600px × 900px` or `1280px × 720px`.
- A semantic slide container, for example `<main class="slide">`.
- A section title at the upper-left.
- A horizontal separator under the title.
- All slide content inside the visible canvas.
- No external dependencies unless the user explicitly permits them.

Recommended base CSS pattern:

```css
html, body {
  margin: 0;
  padding: 0;
  background: #f3f3f3;
}
body {
  font-family: Calibri, Arial, sans-serif;
}
.slide {
  width: 1600px;
  height: 900px;
  aspect-ratio: 16 / 9;
  box-sizing: border-box;
  margin: 0 auto;
  background: #ffffff;
  color: #111111;
  overflow: hidden;
  padding: 46px 58px 44px;
}
:lang(zh), .zh {
  font-family: "微软雅黑", "Microsoft YaHei", sans-serif;
}
:lang(en), .en {
  font-family: Calibri, Arial, sans-serif;
}
.section-title {
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 0.2px;
}
.title-rule {
  height: 2px;
  background: #1f2937;
  margin: 14px 0 28px;
}
.caption {
  background: #ffc000;
  color: #000000;
  font-size: 20px;
  font-weight: 700;
  padding: 6px 10px;
}
.em-blue { color: #0000AA; }
.em-red { color: #DE0000; }
.formula {
  font-family: Cambria Math, "Times New Roman", serif;
  white-space: pre-wrap;
}
```

## Clarification and failure policy

Ask a concise clarification question only when required content is missing or unsupported by the provided source material.

Clarify when:

- Required slide content is absent.
- The requested page is a cover page, table-of-contents page, or thank-you page.
- A claim, number, formula, figure label, or chart is requested without source support.
- A requested chart or visual comparison lacks sufficient data.
- The supplied content cannot fit into one readable 16:9 slide without user-approved reduction or splitting.

Ask only for the minimum missing material. Do not ask for optional fields unless they are needed for the requested output.

## Verification checklist

Before returning HTML, internally check:

- The request is for an academic main-content slide.
- The output is exactly one complete HTML document.
- The canvas is 16:9.
- The section title appears at the upper-left.
- A horizontal separator appears under the section title.
- Chinese text uses `微软雅黑`.
- English text uses `Calibri`.
- Figure captions use background `#ffc000` and text `#000000`.
- Emphasis colors `#0000AA` and `#DE0000` are available in the CSS.
- LaTeX formulas are preserved or renderable under the stated dependency policy.
- Decoration is sparse.
- The chosen layout matches the supplied content.
- Unsupported facts, figures, data, formulas, and labels have not been invented.
- All content remains inside the visible slide canvas.

## Output language

Use the language requested by the user. When no language is specified, infer it from the user’s supplied content and request. This language rule controls slide content and interaction. It does not override the typography rules.

## Example behavior

For a request with `section_title: Method`, topic `Supersonic inlet flow-field comparison`, four supplied simulation images, short result notes, and `layout_preference: 2xn Grid style`, produce one 16:9 HTML slide with the section title at upper-left, a separator below it, four aligned visual panels in the first row, and concise explanatory text aligned below each panel.

For a request with `section_title: Key Finding`, topic `Temperature recovery mechanism`, one primary conclusion, three supporting observations, a LaTeX expression for total temperature, and `layout_preference: 2x2 Grid style`, place the primary conclusion in Quadrant 2, the secondary formula or result in Quadrant 4, and supporting context in Quadrants 1 and 3.
