# Verification Checklist

Before returning the `.pptx`, verify:

- The request is for an academic main-content slide.
- The output is a `.pptx`, not HTML.
- A new-file request produced exactly one slide.
- The slide is 16:9 widescreen.
- The slide uses a blank custom layout.
- The section title appears at the upper-left.
- A horizontal separator appears under the section title.
- Chinese text uses `微软雅黑` or `Microsoft YaHei`.
- English text uses `Calibri`.
- Captions use fill `FFC000` and text `000000`.
- Emphasis colors `0000AA` and `DE0000` are used only where justified.
- LaTeX formulas are preserved or converted faithfully.
- Unsupported facts, figures, data, formulas, and labels were not invented.
- All visible content stays inside the `33.87cm x 19.05cm` canvas.
- Text is readable and not clipped.
- Every real picture has alt text.
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
officecli view <output.pptx> html
officecli query <output.pptx> "picture:no-alt"
```

If any check reports a real issue, fix the file and rerun the checklist.

## Acceptable Warnings

`Slide has no title` can be acceptable for a custom `layout=blank` slide because the title is a named shape rather than a PowerPoint title placeholder.

Chart schema warnings may be OfficeCLI-version-specific. Treat them as acceptable only after checking that the chart renders correctly in `view html` and the target presentation viewer.

## Final Response

Report:

- The `.pptx` path.
- The checks run and their results.
- Any skipped checks and the reason.
- Any source limitations, placeholders, or unsupported requested elements.
