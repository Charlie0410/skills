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
  "central_claim": "optional source-supported planning sentence or research question; not automatically required as a visible title",
  "evidence_priority": "optional ranked figures, data, formulas, tables, or claims that should carry the slide",
  "chart_task": "optional analytic task: category_comparison, trend, relationship, distribution, composition, process, or key_numeric_result",
  "accessibility_level": "optional: standard or strict",
  "label_policy": "optional preference: direct_labels, near_legend, or both",
  "color_constraints": "optional institutional colors, forbidden colors, or color accessibility constraints",
  "audience_context": "optional viewing distance, venue, projector, classroom, or other readability constraints",
  "language": "optional output language; infer from request and source content when absent",
  "layout_preference": "optional: oral_light_assertion_evidence, comparison_direct_label, formula_evidence, table_to_takeaway, 2x2 Grid style, 2xn Grid style, or other",
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
- A chart or visual comparison lacks chart-ready data, complete variable names, units, categories, or labels.
- The supplied content cannot be reduced to one central information unit without changing meaning.
- The user asks for a conclusion sentence but the supplied source supports only a descriptive topic or research question.
- The required visual contains too much embedded text to remain readable after cropping and scaling.
- The supplied content cannot fit into one readable 16:9 slide without user-approved reduction or splitting.
- The slide can fit only by using visible text below `18pt`.
- The user asks to modify an existing `.pptx` but does not identify the file or target slide.

Do not ask for optional fields unless they are needed for the requested output.

## Source Handling

Use only supplied source material. If the user gives manuscript text, preserve terminology and notation. If the user gives figure paths, verify that the files exist before inserting them. If a figure is described but no image exists, create a placeholder with the exact provided description.

For ambiguous or overlong content, reduce density by prioritizing the central information unit, then the strongest supporting evidence, then necessary conditions or caveats. Move detailed explanation into speaker notes when it is source-supported but not visually essential. Do not alter the factual meaning to make content fit.
