# Figure Request Template

Fill this template and hand it to Codex together with the `mpl-figure-generator` skill.

The canonical style file already defines the default figure size, export format, export DPI, and LaTeX text rendering. Do not repeat those defaults unless you want to override them or select one of the registered SciencePlots overlays. TIFF outputs are automatically saved with LZW compression.

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

<RUN_MODE>
{{production_OR_debug_OR_EMPTY_FOR_production}}
</RUN_MODE>

<DEBUG_VERBOSITY>
{{1_2_3_OR_EMPTY_FOR_default_2_IN_debug_MODE}}
</DEBUG_VERBOSITY>

<DATA_CREATION_INSTRUCTIONS>
{{LEAVE_EMPTY_IF_DATA_ALREADY_EXISTS}}
</DATA_CREATION_INSTRUCTIONS>

<MPL_STYLE_PATH>
{{LEAVE_EMPTY_TO_USE_assets/styles/mps_base.mplstyle}}
</MPL_STYLE_PATH>

<MPL_STYLE_PRESET>
{{REGISTERED_STYLE_ID_OR_EMPTY}}
</MPL_STYLE_PRESET>

<MPL_STYLE_CHAIN>
{{COMMA_SEPARATED_REGISTERED_STYLE_IDS_OR_EMPTY}}
</MPL_STYLE_CHAIN>

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
4. `RUN_MODE`: optional. Leave empty for `production`; use `debug` to also create an annotated debug figure and complete visible-object metadata.
5. `DEBUG_VERBOSITY`: optional. Used only in debug mode; valid values are `1`, `2`, and `3`, with default `2`. It controls attribute detail depth and debug-image annotation density; every level should include all visible semantic objects in metadata. Use `3` when you want a zoom-oriented position/reference overlay in the debug image.
6. `DATA_CREATION_INSTRUCTIONS`: use only when you want Codex to generate synthetic or demo data.
7. `MPL_STYLE_PATH`: leave empty to accept the canonical style manager. Do not combine it with registered style fields unless you explicitly restate the desired order as `MPL_STYLE_CHAIN`.
8. `MPL_STYLE_PRESET`: optional registered style ID such as `science`, `nature`, `vibrant`, or `no-latex`.
9. `MPL_STYLE_CHAIN`: optional comma-separated registered style IDs applied after the canonical style, for example `science, no-latex, vibrant`.
10. `ELEMENT_FORMATTING_SPEC`: use only for extra artist-level overrides such as colors, line styles, markers, or annotations.
11. `COLORMAP_NAME`: required for `2D contour`.
12. State units explicitly so Codex can render labels in LaTeX with square-bracketed units such as `$\\mathrm{Temperature}\\ [K]$`.

## Runtime prerequisite

The canonical style requires a working LaTeX installation with `latex`, `pdflatex`, `lmodern`, and `siunitx`.

TIFF output requires Matplotlib/Pillow support for `pil_kwargs={"compression": "tiff_lzw"}`. The skill should report the missing capability rather than silently saving an uncompressed TIFF.

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

### Debug mode

```text
<RUN_MODE>
debug
</RUN_MODE>

<DEBUG_VERBOSITY>
2
</DEBUG_VERBOSITY>
```

In debug mode, use `debug_elements` metadata to refer to visible objects by stable IDs such as `title`, `legend`, `legend_entry_1`, `x_label`, `series_1`, `colorbar_label`, `x_tick_labels`, `grid_lines`, `spines`, or fallback `artist_1`. Levels 1 and 2 label the main IDs in the debug image. Level 3 uses a dense, small-font, zoom-oriented position/reference overlay, while metadata remains the complete object index.

### Registered SciencePlots style overlay

```text
<MPL_STYLE_PRESET>
nature
</MPL_STYLE_PRESET>
```

### Registered style chain

```text
<MPL_STYLE_CHAIN>
science, no-latex, vibrant
</MPL_STYLE_CHAIN>
```
