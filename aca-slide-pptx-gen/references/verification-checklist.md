# Verification Checklist

Before returning the `.pptx`, verify:

- The request is for an academic main-content slide.
- The output is a `.pptx`, not HTML.
- A new-file request produced exactly one slide.
- The slide is 16:9 widescreen.
- The slide uses a blank custom layout.
- The section title appears at the upper-left.
- A horizontal separator spans the safe content width under the section title and uses `linewidth=2pt`.
- The slide is organized around one central information unit.
- One dominant evidence object carries the slide unless the user requested a comparison layout.
- Compact annotations connect the evidence to the central message.
- Chinese text uses `微软雅黑` or `Microsoft YaHei`.
- English text uses `Calibri`.
- Visible text is `18pt+`.
- Normal body text is preferably `24pt+`.
- Captions are `18pt+`, italic, source-supported, and have no background fill by default.
- Emphasis colors are used only where justified and never as the sole semantic encoding.
- Normal text/background contrast is at least `4.5:1`; large text and essential graphics are at least `3:1`.
- Charts have chart-ready data, complete variable names, units, and direct labels or near legends.
- Tables keep only columns needed for the central message.
- LaTeX formulas are preserved or converted faithfully.
- Central formulas are readable and have nearby definitions or assumptions.
- Unsupported facts, figures, data, formulas, and labels were not invented.
- All visible content stays inside the `33.87cm x 19.05cm` canvas.
- Text is readable and not clipped.
- Every real picture has alt text.
- Important embedded text in pictures is repeated in alt text or nearby accessible text.
- Every figure placeholder is explicitly labeled as a placeholder.
- Speaker notes exist and are source-supported.

## Required Commands

Run the bundled validator:

```powershell
python .\aca-slide-pptx-gen\scripts\validate_academic_pptx.py <output.pptx>
```

The validator wraps these OfficeCLI checks when available:

```powershell
officecli close <output.pptx>
officecli validate <output.pptx>
officecli view <output.pptx> issues
officecli view <output.pptx> annotated
officecli view <output.pptx> text
officecli query <output.pptx> shape
officecli query <output.pptx> connector
officecli view <output.pptx> html
officecli query <output.pptx> "picture:no-alt"
```

If any check reports a real issue, fix the file and rerun the checklist.

## Acceptable Warnings

`Slide has no title` can be acceptable for a custom `layout=blank` slide because the title is a named shape rather than a PowerPoint title placeholder.

Chart schema warnings may be OfficeCLI-version-specific. Treat them as acceptable only after checking that the chart renders correctly in `view html` and the target presentation viewer.

Density warnings, missing direct chart labels, sparse shape naming, or long paragraph warnings may require human review. Fix them when they indicate an actual readability or source-fidelity problem.

## Final Response

Report:

- The `.pptx` path.
- The checks run and their results.
- Any skipped checks and the reason.
- Any source limitations, placeholders, or unsupported requested elements.
