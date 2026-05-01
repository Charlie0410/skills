# Input Contract

Accept user requests expressed in prose or structured fields. Extract these fields when available:

```json
{
  "section_title": "required string, short section label placed at the upper-left",
  "topic": "required string, main slide topic or message",
  "text": "required unless equivalent structured content is supplied",
  "figures": "optional array of image paths, figure descriptions, references, or placement requests",
  "data": "optional tables, numeric values, result summaries, or chart-ready data",
  "formulas": "optional LaTeX formulas, Office equation text, or math notation",
  "reference_context": "optional manuscript excerpts, paper context, report notes, terminology constraints, notation, units, or style constraints",
  "language": "optional output language; infer from request and source content when absent",
  "layout_preference": "optional: 2x2 Grid style, 2xn Grid style, or other",
  "emphasis_requests": "optional terms, claims, results, formulas, or visual elements requiring emphasis",
  "output_path": "optional .pptx path; otherwise choose a concise filename from the topic"
}
```

Required minimum content is `section_title`, `topic`, and either `text` or equivalent structured content.

## Clarify When

Ask one concise question only when:

- Required slide content is absent.
- The requested page is a cover page, table-of-contents page, or thank-you page.
- A claim, number, formula, figure label, chart, or conclusion is requested without source support.
- A chart or visual comparison lacks sufficient data.
- The supplied content cannot fit into one readable 16:9 slide without user-approved reduction or splitting.
- The user asks to modify an existing `.pptx` but does not identify the file or target slide.

Do not ask for optional fields unless they are needed for the requested output.

## Source Handling

Use only supplied source material. If the user gives manuscript text, preserve terminology and notation. If the user gives figure paths, verify that the files exist before inserting them. If a figure is described but no image exists, create a placeholder with the exact provided description.

For ambiguous or overlong content, reduce density by prioritizing the central message, then the strongest supporting evidence. Do not alter the factual meaning to make content fit.
