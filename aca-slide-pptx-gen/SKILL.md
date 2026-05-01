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

Ask only for the minimum missing material when required content is absent or unsupported.

## Source Policy

Treat the user's supplied topic, text, figures, data, formulas, and reference context as authoritative. Preserve claims, terminology, notation, units, formulas, figure labels, experimental conditions, and academic framing.

Do not invent paper claims, numeric results, chart values, labels, formulas, figure details, or conclusions. Use clearly labeled placeholders only when the user provided enough descriptive source material but no usable asset or data file.

## OfficeCLI Requirements

Use OfficeCLI for `.pptx` creation and validation. Do not use `python-pptx`, browser screenshot conversion, HTML-to-PPTX conversion, or hand-written OOXML as the primary path.

Before building, verify OfficeCLI is available:

```powershell
officecli --version
```

If it is missing, install from the official OfficeCLI installer or tell the user that generation is blocked until `officecli` is available:

```powershell
irm https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.ps1 | iex
```

When any OfficeCLI property name, enum, or value format is uncertain, run help instead of guessing:

```powershell
officecli help pptx
officecli help pptx shape
officecli help pptx chart
officecli help pptx equation
officecli help pptx notes
```

Detailed OfficeCLI build rules are in `references/officecli-pptx-build-rules.md`.

## Workflow

1. Confirm the request is for an academic main-content slide.
2. Decline cover pages, table-of-contents pages, and thank-you pages with a concise scope statement.
3. Extract `section_title`, `topic`, `text`, `figures`, `data`, `formulas`, `reference_context`, `language`, `layout_preference`, `emphasis_requests`, and optional output path.
4. Identify the slide's central message from the supplied material.
5. Choose the layout using `references/layout-and-style-spec.md`.
6. Build a one-slide `.pptx` through OfficeCLI using `layout=blank`.
7. Add section title, separator line, visual evidence, text, formulas, captions, and speaker notes.
8. Apply explicit font, size, color, fill, and position properties to every shape.
9. Run the verification checklist in `references/verification-checklist.md`.
10. Return the `.pptx` path and the verification results.

## Visual Rules

Use a 16:9 PowerPoint canvas: `33.87cm x 19.05cm`.

Place `section_title` at the upper-left. Add a horizontal separation line directly below it.

Use `微软雅黑` or `Microsoft YaHei` for Chinese text. Use `Calibri` for English text. For mixed-language content, split text into separate shapes or runs when practical so each language can use the correct font.

Use concise figure captions. Create captions as separate shapes with fill `FFC000` and text color `000000`.

Use `0000AA` and `DE0000` as the available emphasis colors. Apply emphasis sparingly to important terms, measured values, conclusions, or formulas specified by the user.

Keep decoration sparse. Prioritize readability, whitespace, consistent spacing, and clear hierarchy.

## Layout Rules

Use the detailed geometry in `references/layout-and-style-spec.md`. The main layout choices are:

- `2x2 Grid style`: use when content has a ranked importance hierarchy. Put the most important content in the upper-right quadrant and the second-most important content in the lower-right quadrant.
- `2xn Grid style`: use for parallel results, comparison panels, or figure-text pairs. Put figures, charts, or visual result panels in row 1 and matched explanations in row 2.
- `other`: use a sparse academic layout when it better fits the content, such as one hero figure plus explanation panel, left evidence plus right conclusion, formula-centered derivation, or comparison table plus takeaway.

## PPTX Output Contract

Return one `.pptx` file unless the user explicitly asks to update an existing deck.

The `.pptx` must include:

- Exactly one new academic content slide for a new-file request.
- Widescreen 16:9 geometry.
- A blank custom slide layout.
- Section title at upper-left.
- Horizontal separator below the section title.
- All visible slide content inside the canvas.
- Explicit fonts and font sizes on every text shape.
- Captions with fill `FFC000` and text `000000`.
- Speaker notes derived only from the supplied source material.

## Formulas, Figures, Tables, and Charts

Preserve LaTeX source faithfully. Prefer OfficeCLI `equation` when it supports the required expression. If equation syntax is uncertain, run `officecli help pptx equation`. If reliable equation generation is not possible, place the formula as text in a dedicated formula shape using a math-friendly font and preserve the original delimiters.

Insert user-provided images with OfficeCLI `picture`. Set alt text in a follow-up command after insertion. If no image asset is available, create a clearly labeled figure placeholder from the provided figure description.

Use OfficeCLI `table` for compact comparisons and `chart` only when the user supplied chart-ready values. If data is insufficient, use a textual placeholder and state the minimum missing data in the final response.

## Verification

Run the narrowest reliable checks before returning:

```powershell
python .\aca-slide-pptx-gen\scripts\validate_academic_pptx.py <output.pptx>
```

The script checks OfficeCLI availability, schema validation, text token leaks, issue output, annotated output, and HTML preview generation when OfficeCLI is installed.

If OfficeCLI is not installed, do not claim the `.pptx` was generated or verified. State that the skill is installed but PPTX generation requires OfficeCLI.

## Output Language

Use the language requested by the user. When no language is specified, infer it from the supplied academic content and request. This controls slide content and interaction language, not the required typography rules.
