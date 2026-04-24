# aca-slide-gen input contract

The skill accepts prose requests and structured fields. It must extract this logical contract:

| Field | Required | Description |
| --- | --- | --- |
| `section_title` | Yes | Short section label placed at the upper-left of the slide. |
| `topic` | Yes | Main slide topic or message. |
| `text` | Conditional | Required unless equivalent structured content is supplied. |
| `figures` | No | Image paths, figure descriptions, figure references, or placement requests. |
| `data` | No | Tables, numeric values, result summaries, or chart-ready data. |
| `formulas` | No | LaTeX formulas or other math notation. |
| `reference_context` | No | Source context constraining facts, notation, terminology, units, or style. |
| `language` | No | Output language. Infer from request and source content when absent. |
| `layout_preference` | No | `2x2 Grid style`, `2xn Grid style`, or `other`. |
| `emphasis_requests` | No | User-specified items needing visual emphasis. |

Minimum viable request: `section_title`, `topic`, and `text` or equivalent structured academic content.

If the user supplies reference context, treat it as the source for terminology, facts, notation, and units. Never infer unsupported numerical values, claims, labels, formulas, or figure contents.
