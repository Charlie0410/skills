---
name: aca-slide-pptx-gen
description: Generate one 16:9 academic main-content PowerPoint slide as a .pptx using OfficeCLI from user-provided research text, figures, data, formulas, and reference context. Use when Codex must create an academic presentation content slide as a real .pptx file rather than HTML; decline cover pages, table-of-contents pages, and thank-you pages as out of scope.
---

# aca-slide-pptx-gen

## Purpose

Use this skill to create one academic presentation main-content slide as a real `.pptx` file. The slide must fit a single 16:9 widescreen canvas and must use OfficeCLI as the PowerPoint creation, editing, and validation layer.

This skill inherits the academic content discipline of `aca-slide-gen`, but changes the deliverable from one self-contained HTML document to one `.pptx` containing one content slide.

## Scope

Create only academic main-content slides. Decline or redirect requests for cover pages, table-of-contents pages, and thank-you pages.

Default to a new one-slide `.pptx`. If the user gives an existing `.pptx`, inspect it first and either append one new content slide or replace the requested slide only when the request is explicit.

## Required Inputs

Extract the input contract described in `references/input-contract.md`. Required minimum content is:

- `section_title`: short section label placed at the upper-left.
- `topic`: the main slide topic or message.
- `text` or equivalent structured academic content.

Optional planning fields include `central_claim`, `evidence_priority`, `chart_task`, `accessibility_level`, `label_policy`, `color_constraints`, and `audience_context`.

Ask only for the minimum missing material when required content is absent or unsupported.

## Source Policy

Treat the user's supplied topic, text, figures, data, formulas, and reference context as authoritative. Preserve claims, terminology, notation, units, formulas, figure labels, experimental conditions, and academic framing.

Do not invent paper claims, numeric results, chart values, labels, formulas, figure details, or conclusions. Use clearly labeled placeholders only when the user provided enough descriptive source material but no usable asset or data file.

Treat `central_claim` as source-supported planning guidance. It may become visible slide text when it fits the source and layout, but complex academic slides are not required to use a full-sentence visible claim title.

## OfficeCLI Requirements

Use OfficeCLI for `.pptx` creation and validation. Do not use `python-pptx`, browser screenshot conversion, HTML-to-PPTX conversion, or hand-written OOXML as the primary path.

Before building, verify OfficeCLI is available:

```powershell
officecli --version
```

If `officecli` is not on PATH, check the standard local install path before declaring it unavailable:

```powershell
C:\Users\charlie\AppData\Local\OfficeCli\officecli.exe --version
```

If it is missing from both locations, install from the official OfficeCLI installer or tell the user that generation is blocked until `officecli` is available:

```powershell
irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex
```

When any OfficeCLI property name, enum, or value format is uncertain, run help instead of guessing:

```powershell
officecli help pptx
officecli help pptx shape
officecli help pptx connector
officecli help pptx picture
officecli help pptx table
officecli help pptx chart
officecli help pptx equation
officecli help pptx notes
```

Detailed OfficeCLI build rules are in `references/officecli-pptx-build-rules.md`.

## Workflow

1. Confirm the request is for an academic main-content slide.
2. Decline cover pages, table-of-contents pages, and thank-you pages with a concise scope statement.
3. Extract `section_title`, `topic`, `text`, `figures`, `data`, `formulas`, `reference_context`, `language`, `layout_preference`, `emphasis_requests`, optional output path, and any optional planning fields from the input contract.
4. Identify one central information unit from the supplied material. Use `central_claim` when source-supported; otherwise derive a neutral topic, question, or concise message without inventing a conclusion.
5. Choose one main evidence object: a figure, chart, table, formula, mechanism diagram, or compact evidence block. Use `evidence_priority` when supplied.
6. Compress visible text around the central unit: main evidence first, compact annotations second, one qualifier or takeaway third, and source-supported speaker notes for detail.
7. Choose the layout using `references/layout-and-style-spec.md`.
8. Build a one-slide `.pptx` through OfficeCLI using `layout=blank`.
9. Add section title, separator line, main evidence, compact annotations, formulas, captions, and speaker notes.
10. Apply explicit font, size, color, fill, and position properties to every shape.
11. Run the verification checklist in `references/verification-checklist.md`.
12. Return the `.pptx` path and the verification results.

## Visual Rules

Use a 16:9 PowerPoint canvas: `33.87cm x 19.05cm`.

Place `section_title` at the upper-left. Add a horizontal separation line directly below it.

Use `微软雅黑` or `Microsoft YaHei` for Chinese text. Use `Calibri` for English text. For mixed-language content, split text into separate shapes or runs when practical so each language can use the correct font.

Use concise figure captions. Captions are separate text shapes, at least `18pt`, italic, source-supported, and normally use no background fill.

Use emphasis sparingly for important terms, measured values, conclusions, or formulas specified by the user. Do not encode meaning by color alone; pair color with direct labels, shape, line style, marker, annotation text, or grouping.

If a text box needs a background color, apply the fill on that text shape itself. Do not create a separate background rectangle behind the text.

For related list items in the same visual block, use one textbox with OfficeCLI bullet formatting. Do not create one textbox per bullet.

Keep decoration sparse. Prioritize readability, whitespace, consistent spacing, and clear hierarchy.

## Layout Rules

Use the detailed geometry in `references/layout-and-style-spec.md`. The main layout choices are:

- `oral_light_assertion_evidence`: default for most academic content slides. Use one central information unit, one main evidence object, compact annotations, and source-supported notes.
- `2x2 Grid style`: use when content has a ranked importance hierarchy. Put the most important content in the upper-right quadrant and the second-most important content in the lower-right quadrant.
- `2xn Grid style` or `comparison_direct_label`: use for parallel results, comparison panels, or figure-text pairs. Put figures, charts, or visual result panels in row 1 and matched explanations in row 2.
- `formula_evidence`: use when one central equation or derivation is the primary evidence.
- `table_to_takeaway`: use when a compact table supports a single result or takeaway.
- `other`: use a sparse academic layout when it better fits the content, such as one hero figure plus explanation panel, left evidence plus right conclusion, formula-centered derivation, or comparison table plus takeaway.

## PPTX Output Contract

Return one `.pptx` file unless the user explicitly asks to update an existing deck.

The `.pptx` must include:

- Exactly one new academic content slide for a new-file request.
- Widescreen 16:9 geometry.
- A blank custom slide layout.
- Section title at upper-left.
- Horizontal separator below the section title.
- One central information unit and one dominant evidence object unless the user explicitly requests a comparison layout.
- All visible slide content inside the canvas.
- Explicit fonts and font sizes on every text shape.
- Captions at `18pt+`, italic, and no background fill by default.
- Speaker notes derived only from the supplied source material.

## Formulas, Figures, Tables, and Charts

Preserve LaTeX source faithfully. Prefer OfficeCLI `equation` when it supports the required expression. If equation syntax is uncertain, run `officecli help pptx equation`. If reliable equation generation is not possible, place the formula as text in a dedicated formula shape using a math-friendly font and preserve the original delimiters.

Insert user-provided images with OfficeCLI `picture`. Set alt text in a follow-up command after insertion. If no image asset is available, create a clearly labeled figure placeholder from the provided figure description.

Prefer original high-resolution or vector images. Crop images to the evidence-bearing region, preserve source figure labels and conditions, and repeat essential embedded image text in alt text or nearby accessible text.

Use OfficeCLI `table` for compact comparisons and `chart` only when the user supplied chart-ready values. Charts require complete variable names, units, categories, and direct labels or near legends. If data is insufficient, use a textual placeholder and state the minimum missing data in the final response.

Keep tables to columns needed for the central message. Move dense supplementary values to speaker notes or ask whether to split the slide.

## Verification

Run the narrowest reliable checks before returning:

```powershell
python .\aca-slide-pptx-gen\scripts\validate_academic_pptx.py <output.pptx>
```

The script resolves OfficeCLI from `OFFICECLI_PATH`, PATH, or `C:\Users\charlie\AppData\Local\OfficeCli\officecli.exe`. It checks schema validation, one-slide count, geometry bounds, token leaks, picture alt text, named academic shapes, caption style, visible text below `18pt` when exposed by OfficeCLI, and HTML preview generation. It reports source-design judgments such as density and sparse direct labeling as warnings when they are not reliably machine-checkable.

If OfficeCLI is not installed, do not claim the `.pptx` was generated or verified. State that the skill is installed but PPTX generation requires OfficeCLI.

## Output Language

Use the language requested by the user. When no language is specified, infer it from the supplied academic content and request. This controls slide content and interaction language, not the required typography rules.
