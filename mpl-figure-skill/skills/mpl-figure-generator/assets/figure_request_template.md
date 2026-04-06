# Figure Request Template

Fill this template and hand it to Codex together with the `mpl-figure-generator` skill.

The canonical style file already defines the default figure size, export format, export DPI, and LaTeX text rendering. Do not repeat those defaults unless you want to override them.

```text
<USER_MATERIALS>
<DATA_FILE_PATHS>
{{EXISTING_DATA_PATHS_OR_TARGET_PATHS_FOR_GENERATED_DATA}}
</DATA_FILE_PATHS>

<DATA_STRUCTURE_DESCRIPTION>
{{SCHEMA_FIELD_MEANINGS_UNITS_AND_REQUIRED_X_Y_OR_Z_MAPPINGS}}
</DATA_STRUCTURE_DESCRIPTION>

<IMAGE_TYPE>
{{IMAGE_TYPE}}
</IMAGE_TYPE>

<DATA_CREATION_INSTRUCTIONS>
{{LEAVE_EMPTY_IF_DATA_ALREADY_EXISTS}}
</DATA_CREATION_INSTRUCTIONS>

<MPL_STYLE_PATH>
{{LEAVE_EMPTY_TO_USE_assets/styles/mps_base.mplstyle}}
</MPL_STYLE_PATH>

<ELEMENT_FORMATTING_SPEC>
{{OPTIONAL_ARTIST_LEVEL_OVERRIDES}}
</ELEMENT_FORMATTING_SPEC>

<COLORMAP_NAME>
{{COLORMAP_NAME_OR_EMPTY}}
</COLORMAP_NAME>

<ADDITIONAL_IMAGE_SPECIFICATIONS>
{{OPTIONAL_LAYOUT_OR_ANNOTATION_NOTES}}
</ADDITIONAL_IMAGE_SPECIFICATIONS>

<OUTPUT_BASENAME>
{{OUTPUT_BASENAME_OR_EMPTY}}
</OUTPUT_BASENAME>

<SAMPLE_ROWS_OR_SCHEMA_SNIPPETS>
{{OPTIONAL_SAMPLE_ROWS_OR_EMPTY}}
</SAMPLE_ROWS_OR_SCHEMA_SNIPPETS>
</USER_MATERIALS>
```

## Minimal field notes

1. `DATA_FILE_PATHS`: provide one or more explicit paths. When asking for synthetic data, provide the target path that Codex should create.
2. `DATA_STRUCTURE_DESCRIPTION`: provide schema, field meanings, units, grouping rules, and explicit x, y, or z mappings.
3. `IMAGE_TYPE`: provide `2D Line`, `2D Symbol`, `2D contour`, `Polar Plot`, or another explicit plot type.
4. `DATA_CREATION_INSTRUCTIONS`: use only when you want Codex to generate synthetic or demo data.
5. `MPL_STYLE_PATH`: leave empty to accept the canonical style manager.
6. `ELEMENT_FORMATTING_SPEC`: use only for extra artist-level overrides such as colors, line styles, markers, or annotations.
7. `COLORMAP_NAME`: required for `2D contour`.
8. State units explicitly so Codex can render labels in LaTeX with square-bracketed units such as `$\\mathrm{Temperature}\\ [K]$`.

## Runtime prerequisite

The canonical style requires a working LaTeX installation with `latex`, `pdflatex`, `lmodern`, and `siunitx`.

## Quick examples

### 2D Line with existing CSV

```text
<IMAGE_TYPE>
2D Line
</IMAGE_TYPE>
```

### 2D Line with synthetic data

```text
<DATA_CREATION_INSTRUCTIONS>
Generate a single synthetic CSV with 100 rows and columns `x` and `y`.
</DATA_CREATION_INSTRUCTIONS>
```

### 2D contour

```text
<IMAGE_TYPE>
2D contour
</IMAGE_TYPE>

<COLORMAP_NAME>
viridis
</COLORMAP_NAME>
```
