# OfficeCLI PPTX Build Rules

These rules adapt OfficeCLI's generic `.pptx` skill to a one-slide academic content slide.

## Preflight

Verify OfficeCLI:

```powershell
officecli --version
```

When syntax is uncertain, run help first:

```powershell
officecli help pptx
officecli help pptx shape
officecli help pptx picture
officecli help pptx table
officecli help pptx chart
officecli help pptx equation
officecli help pptx notes
```

OfficeCLI help for the installed version is authoritative.

## New One-Slide File

Use this sequence:

```powershell
officecli create output.pptx
officecli open output.pptx
officecli add output.pptx / --type slide --prop layout=blank --prop background=FFFFFF
officecli add output.pptx "/slide[1]" --type shape --prop name=SectionTitle --prop text="Methods" --prop x=1.2cm --prop y=0.8cm --prop width=31.47cm --prop height=0.8cm --prop font=Calibri --prop size=18 --prop bold=true --prop color=111111 --prop fill=none
officecli add output.pptx "/slide[1]" --type shape --prop name=TitleRule --prop preset=rect --prop x=1.2cm --prop y=1.85cm --prop width=31.47cm --prop height=0.04cm --prop fill=1F2937 --prop line=none
```

Continue adding content shapes, pictures, tables, charts, formulas, and notes. Then:

```powershell
officecli close output.pptx
officecli validate output.pptx
officecli view output.pptx issues
officecli view output.pptx annotated
officecli view output.pptx html
```

Do not run `validate` while the file is still open in resident mode.

## Existing PPTX

If the user supplies an existing `.pptx`:

1. Run `officecli view file.pptx outline`.
2. Run `officecli view file.pptx annotated`.
3. Preserve the existing theme, master, and conventions when they do not conflict with the academic rules.
4. Append or replace only the requested slide.
5. Re-run validation and visual checks after modification.

## Shapes and Text

Create text with `shape`. Set explicit `x`, `y`, `width`, `height`, `font`, `size`, `color`, `fill`, and alignment. Name important shapes at creation.

Use separate shapes or runs for mixed Chinese/English when different fonts are required. For multi-line text, prefer separate paragraphs or a JSON batch with real `\n` values. Verify with `officecli view output.pptx text` that no literal `\n`, `\t`, or escaped `$` leaked.

## Pictures

Add pictures only from existing paths:

```powershell
officecli add output.pptx "/slide[1]" --type picture --prop src="figure.png" --prop x=1.2cm --prop y=2.6cm --prop width=10cm --prop height=6cm
officecli set output.pptx "/slide[1]/picture[1]" --prop alt="Short factual figure description from the user source"
```

Do not set `alt` during `add picture`; OfficeCLI requires a follow-up `set` for reliable alt text.

If no image file exists, create a placeholder shape labeled `Figure placeholder: ...` from the user-provided description.

## Captions

Use separate caption shapes:

```powershell
officecli add output.pptx "/slide[1]" --type shape --prop name=Caption1 --prop text="Fig. 1. Pressure distribution" --prop x=1.2cm --prop y=8.8cm --prop width=10cm --prop height=0.7cm --prop font=Calibri --prop size=12 --prop bold=true --prop color=000000 --prop fill=FFC000
```

Caption text must be concise and source-supported.

## Charts and Tables

Use `chart` only when chart-ready values and categories are supplied. Run `officecli help pptx chart` before using a chart type or data format that is not already known.

Use `table` for compact numeric comparisons, ablation summaries, taxonomies, or method/result matrices. Keep table text readable and avoid dense spreadsheet-like slides.

## Formulas

Prefer OfficeCLI `equation` if the installed version supports the required syntax:

```powershell
officecli help pptx equation
```

If equation generation is uncertain, create a formula text shape, preserve the original LaTeX delimiters, and use a math-friendly font such as `Cambria Math`.

## Speaker Notes

Add notes to every generated content slide:

```powershell
officecli add output.pptx "/slide[1]" --type notes --prop text="Concise speaking notes derived only from the supplied source."
```

Notes may summarize source material but must not introduce unsupported claims.

## Stable Addressing

OfficeCLI paths are 1-based. Use quoted paths:

```powershell
"/slide[1]"
```

Prefer `@name=` paths for follow-up edits:

```powershell
officecli set output.pptx "/slide[1]/shape[@name=MainClaim]" --prop color=0000AA
```

For connectors or cases where `@name=` is unsupported, query IDs first and then use `@id=`.

## Shell Pitfalls

- Quote PowerShell paths containing brackets.
- Use hex colors without `#`.
- Do not guess property names; run `officecli help`.
- Avoid unescaped shell expansion in text containing `$`.
- Do not treat `view issues` message `Slide has no title` as a defect when using `layout=blank`.
- Close PowerPoint, WPS, or Keynote before editing a file they have open.
