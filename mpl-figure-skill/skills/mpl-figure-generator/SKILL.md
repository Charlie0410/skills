---
name: mpl-figure-generator
description: Direct Matplotlib scientific figure generation with the bundled mplstyle, companion metadata JSON, and optional synthetic data creation. Use when Codex should create or update finished 2D line, 2D symbol or scatter, 2D contour, or polar figures from explicit data requirements, especially when LaTeX-rendered labels, square-bracketed units, and style-driven export defaults are required.
---

# Purpose

Generate finished plot artifacts rather than instruction packets.

Treat `assets/styles/mps_base.mplstyle` as the default source of truth for:

1. Figure size
2. Export DPI
3. Export format
4. Export bounding-box behavior
5. Export padding
6. Font family
7. LaTeX text rendering

TIFF export compression is a mandatory export-layer rule, not an mplstyle setting. Any generated `.tif` or `.tiff` production or debug artifact must be saved with Pillow LZW compression through Matplotlib `savefig` `pil_kwargs`.

Create or update the figure output, any helper script needed for repeatability, the data file when the user explicitly asks for synthetic or demo data, and a companion metadata JSON file.

## Prerequisites

1. Use Matplotlib as the primary plotting backend.
2. Ensure the LaTeX runtime is available before using `assets/styles/mps_base.mplstyle` because the canonical style enables `text.usetex : True`.
3. Require `latex` and `pdflatex` on `PATH`.
4. Require the LaTeX packages `lmodern` and `siunitx`.
5. Stop and report the missing prerequisite if the canonical style cannot run as configured. Do not silently disable LaTeX.
6. Use the existing repository layout unless the user explicitly asks for a different placement.
7. For TIFF output, require a Matplotlib/Pillow TIFF writer that accepts `pil_kwargs={"compression": "tiff_lzw"}`. Stop and report the missing TIFF LZW capability instead of saving an uncompressed TIFF.

## Runtime inputs

Required fields:

1. `DATA_FILE_PATHS`
2. `DATA_STRUCTURE_DESCRIPTION`
3. `IMAGE_TYPE`

Conditional field:

1. `COLORMAP_NAME` is mandatory when `IMAGE_TYPE` is `2D contour` or another contour or heat-map equivalent.

Optional fields:

1. `DATA_CREATION_INSTRUCTIONS`
2. `MPL_STYLE_PATH`
3. `MPL_STYLE_PRESET`
4. `MPL_STYLE_CHAIN`
5. `ELEMENT_FORMATTING_SPEC`
6. `ADDITIONAL_IMAGE_SPECIFICATIONS`
7. `OUTPUT_BASENAME`
8. `SAMPLE_ROWS_OR_SCHEMA_SNIPPETS`
9. `RUN_MODE`
10. `DEBUG_VERBOSITY`

Runtime mode fields:

1. `RUN_MODE` defaults to `production` when omitted.
2. Valid `RUN_MODE` values are `production` and `debug`.
3. `production` preserves the clean finished-figure workflow.
4. `debug` exports the clean production figure first, then exports a second annotated debug figure for second-pass adjustment.
5. `DEBUG_VERBOSITY` is used only when `RUN_MODE` is `debug`.
6. Valid `DEBUG_VERBOSITY` values are `1`, `2`, and `3`.
7. `DEBUG_VERBOSITY` defaults to `2` in debug mode when omitted.
8. `DEBUG_VERBOSITY` controls metadata detail depth and debug-image annotation density. It must not reduce which visible figure objects are reported in metadata.

## Ease-of-use rules

1. Accept common aliases and normalize them internally:
   * `2D Line`, `line`, `line plot`
   * `2D Symbol`, `symbol`, `scatter`, `symbol/scatter`
   * `2D contour`, `contour`, `contour plot`
   * `Polar Plot`, `polar`, `polar plot`
2. Default the active style chain to `assets/styles/mps_base.mplstyle` when the user does not explicitly select a style.
3. Accept registered style presets from `assets/style_registry.yaml` through `MPL_STYLE_PRESET` or an ordered `MPL_STYLE_CHAIN`.
4. Treat the active mplstyle chain as the factual source for figure size, export format, DPI, and padding defaults. Do not require the user to restate those defaults.
5. Treat `ELEMENT_FORMATTING_SPEC` and `ADDITIONAL_IMAGE_SPECIFICATIONS` as optional artist-level refinements rather than mandatory inputs.
6. Generate a data file only when the user explicitly asks for synthetic, random, demo, or placeholder data. Record the generated data path in metadata.
7. Preserve unresolved placeholders rather than inventing names, schema details, label text, units, styles, or colormaps.
8. Render labels, legend text, and colorbar labels in LaTeX-compatible strings when they appear in the figure.
9. Write units in square brackets, for example `$\\mathrm{Time}\\ [s]$` or `$\\mathrm{Signal}\\ [a.u.]$`.

## Style manager policy

Use `assets/styles/mps_base.mplstyle` as the canonical default style manager. Registered SciencePlots styles are optional overlays and must not replace the default unless the user explicitly selects them.

Rules:

1. Load the active style chain before creating the figure.
2. With no style field, load only `assets/styles/mps_base.mplstyle`.
3. With `MPL_STYLE_PRESET`, load `assets/styles/mps_base.mplstyle` and then the registered preset from `assets/style_registry.yaml`.
4. With `MPL_STYLE_CHAIN`, load `assets/styles/mps_base.mplstyle` and then each registered preset in the user-provided order.
5. Keep `MPL_STYLE_PATH` as an explicit file-path override. If it appears with `MPL_STYLE_PRESET` or `MPL_STYLE_CHAIN`, ask the user to rewrite the request as one ordered `MPL_STYLE_CHAIN` instead of guessing merge order.
6. Treat the final active mplstyle chain as the authoritative source for export defaults.
7. Apply any user-requested style override explicitly in code or local `rcParams`.
8. Do not silently replace the canonical style with inferred defaults.
9. Record the active `style_chain`, resolved style paths, and registered preset use in metadata.

## Supported plot families

Guaranteed first-class handling:

1. `2D Line`
2. `2D Symbol`
3. `2D contour`
4. `Polar Plot`

Handling notes:

1. `2D Line` requires explicit x and y mappings. Require grouping rules only when multiple series exist.
2. `2D Symbol` requires explicit coordinate mapping and any requested marker semantics, size encoding, or color encoding.
3. `2D contour` requires explicit x, y, and z semantics plus an explicit `COLORMAP_NAME`.
4. `Polar Plot` requires explicit angular variable, radial variable, and angular unit conventions when relevant.

If the requested plot type is outside this list, preserve it as a user-specified type and do not coerce it into the nearest supported type unless the user explicitly asks for such a conversion.

## Workflow

Follow this order:

### Step 1. Check prerequisites and input completeness

Verify the LaTeX prerequisites when the final active style chain has `text.usetex : True`.
Check whether the required fields are present.
If the plot type is contour or heat-map equivalent, verify that `COLORMAP_NAME` is present.

### Step 2. Normalize inputs

Normalize plot-type aliases to one canonical label.
Normalize file paths exactly as provided.
Default the style path to `assets/styles/mps_base.mplstyle` when the user does not provide one.
Resolve `MPL_STYLE_PRESET` and `MPL_STYLE_CHAIN` only against registered IDs in `assets/style_registry.yaml`.
Reject unknown registered style IDs instead of treating them as file paths.
Reject simultaneous `MPL_STYLE_PATH` and registered style fields unless the user has explicitly provided an ordered chain.
Default `RUN_MODE` to `production` when the user does not provide one.
In debug mode, default `DEBUG_VERBOSITY` to `2` when the user does not provide one.
Reject unsupported `RUN_MODE` values.
In debug mode, reject unsupported `DEBUG_VERBOSITY` values instead of guessing.

### Step 3. Resolve the data source

Read the provided data source when files already exist.
Generate the data file first when the user explicitly requests synthetic or demo data and has provided enough schema and path information to do so safely.

### Step 4. Inspect style facts

Read the active mplstyle file or chain and treat the final resolved style as the source of truth for:

1. Figure dimensions
2. Export format
3. Export DPI
4. Bounding-box behavior
5. Padding
6. Font and TeX settings

### Step 5. Build the figure

Load and preprocess the data.
Construct the requested Matplotlib figure.
Apply the active style chain plus any explicit artist-level overrides.
Format labels in LaTeX-compatible strings and write units in square brackets.

### Step 6. Export outputs

Export the clean production figure using the format and DPI dictated by the active mplstyle unless the user explicitly overrides those settings.

When the output suffix or effective export format is `tif` or `tiff`, save with:

```python
figure.savefig(output_path, pil_kwargs={"compression": "tiff_lzw"})
```

Do not silently fall back to an uncompressed TIFF if LZW compression is unavailable.

When `RUN_MODE` is `production`, stop after writing the clean figure and companion metadata.

When `RUN_MODE` is `debug`:

1. Save the clean production figure before adding diagnostic overlays.
2. Build a diagnostic annotation layer on the same figure after the clean export succeeds.
3. Save the annotated debug figure as `<OUTPUT_BASENAME>.debug.<style_format>`.
4. Preserve the style-driven export format, DPI, bounding-box behavior, padding, and TIFF LZW compression policy for both images.
5. Use high-contrast callout boxes and connector lines for debug labels.
6. Use `usetex=False` for debug annotation text so labels that contain property strings do not break LaTeX-enabled production styles.
7. Keep `DEBUG_VERBOSITY` 1 and 2 debug images readable by labeling the main semantic IDs.
8. Treat `DEBUG_VERBOSITY` 3 as a zoom-oriented diagnostic image that may use small dense labels for position adjustment.

Create a companion metadata JSON file that records at least:

1. Plot data source path(s)
2. Figure creation timestamp
3. Plot type
4. Style path
5. Output figure path
6. Run mode
7. Style chain
8. Resolved style paths
9. Registered style preset, when used
10. Export compression, when the output format uses compression

In debug mode, also record:

1. Debug verbosity
2. Debug figure path
3. Debug elements and their stable user-addressable IDs
4. Debug object count
5. Debug coverage summary, including absent common object categories
6. Unclassified visible artists, when any visible object cannot be assigned a semantic ID

#### Debug element naming

Debug metadata must cover every visible semantic object in the figure at every `DEBUG_VERBOSITY` level. Use stable semantic IDs for user-addressable Matplotlib elements. Prefer names that a user can refer to in a follow-up request without knowing Matplotlib internals.

`DEBUG_VERBOSITY` changes how many attributes are recorded for each object and how much diagnostic information appears in the debug image; it must never omit visible objects from metadata such as titles, legends, tick labels, spines, grid lines, colorbars, annotations, or series.

Common IDs include:

1. `figure`
2. `main_axes`, `axes_2`, and later numbered axes
3. `title`, `subtitle`, and axes-specific titles when present
4. `x_label`, `y_label`, `z_label`, and colorbar labels
5. `legend`, `legend_title`, `legend_entry_1`, `legend_entry_2`, and later legend entries
6. `colorbar`, `colorbar_label`, and numbered colorbar tick label groups
7. `series_1`, `series_2`, and later numbered line series
8. `scatter_1`, `scatter_2`, and later numbered scatter groups
9. `contour_fill`, `contour_lines`, and contour label groups
10. `image_1`, `patch_1`, `reference_line_1`, and later numbered visible non-series artists
11. `annotation_1`, `text_1`, and later numbered annotations or free text
12. `x_tick_labels`, `y_tick_labels`, `x_tick_lines`, `y_tick_lines`, `grid_lines`, and `spines`
13. `artist_1`, `artist_2`, and later fallback IDs for visible artists that cannot be classified semantically

For repeated low-level objects, group them semantically in metadata rather than omitting them. For example, `x_tick_labels` should record count and label text; `grid_lines` should record count and visual style; `spines` should record visible sides and style. Use per-object IDs for low-level members only when needed to make a user follow-up request unambiguous.

If a common object category is absent, such as no `legend` or no `colorbar`, do not invent a placeholder object. Record the absence in the debug coverage summary.

At `DEBUG_VERBOSITY` 1 and 2, the annotated debug image should label the main semantic objects and stable IDs, while the metadata remains the complete source of truth for all visible objects.

At `DEBUG_VERBOSITY` 3, the annotated debug image should label every user-addressable semantic object and grouped low-level category with small, high-contrast, zoom-friendly labels. Do not expand repeated low-level groups into every individual Matplotlib artist unless per-member IDs are needed to make a follow-up edit unambiguous.

#### Debug verbosity

Use `DEBUG_VERBOSITY` to control how much diagnostic information appears in callouts and metadata. All levels must include the same complete visible semantic object coverage:

1. `1`: complete object coverage with element ID, element type, parent object, visible flag, and concise semantic role.
2. `2`: level 1 coverage plus key user-facing attributes such as text or label, color, linewidth, linestyle, marker, colormap, alpha, and axes association.
3. `3`: level 2 coverage plus dense in-figure position diagnostics, position or extents, z-order, transform and layout notes, collection sizes, contour levels or counts, legend entry details, colorbar or mappable details, and grouped low-level member summaries where available.

For `DEBUG_VERBOSITY` 3 callouts, include compact position fields where available: stable ID, element type, parent axes or figure, anchor or center in figure fraction, axes-fraction position when applicable, data position or data extents when applicable, bbox or extents, transform shorthand, z-order, and count, levels, or entries for grouped objects.

For `DEBUG_VERBOSITY` 3 reference guides, draw figure-fraction grid guides at `0`, `0.25`, `0.5`, `0.75`, and `1`, axes bounding boxes, axes center and corner reference points, anchor points for labeled objects, and connector lines from labels to anchors or bboxes.

### Step 7. Verify results

Verify that the figure file exists and that the metadata JSON was written.
When practical, inspect the output file metadata or image dimensions to confirm the export settings were applied.

## Response behavior

If the materials are sufficient and the prerequisites are satisfied:

1. Generate the figure artifacts directly.
2. Return a short status summary with the created file paths, run mode, and any explicit overrides that were applied.

If the materials are insufficient or a prerequisite is missing:

1. Do not fabricate the plot.
2. Report only the missing inputs or missing prerequisites.

## Missing-input checklist

1. Missing required field: `DATA_FILE_PATHS`
2. Missing required field: `DATA_STRUCTURE_DESCRIPTION`
3. Missing required field: `IMAGE_TYPE`
4. Missing required field: `COLORMAP_NAME` for contour or heat-map equivalent plots
5. Missing prerequisite: LaTeX runtime or required packages for the active style chain
6. Missing TIFF LZW compression support for TIFF output
7. Unsupported `RUN_MODE` value
8. Unsupported `DEBUG_VERBOSITY` value in debug mode
9. Unknown `MPL_STYLE_PRESET` or `MPL_STYLE_CHAIN` entry
10. Ambiguous style request combining `MPL_STYLE_PATH` with registered style fields

## Hard constraints

1. Do not guess missing required inputs.
2. Do not invent schema details, file paths, label text, units, colormaps, or output names.
3. Do not silently disable LaTeX when the canonical style requires it.
4. Keep Matplotlib as the primary visualization framework.
5. Prefer the canonical style manager file unless the user explicitly overrides it.
6. Treat export defaults as style-driven rather than prompt-driven.
7. Write the metadata JSON file whenever a figure is generated.
8. In debug mode, save the clean production figure before adding debug overlays.
9. Do not let debug annotations change the scientific plot semantics.
10. Do not infer or spell-correct registered style IDs.
11. Save every `.tif` or `.tiff` output with LZW compression through `pil_kwargs={"compression": "tiff_lzw"}`.
12. Do not fall back to uncompressed TIFF output when LZW compression fails.
13. In debug mode, record every visible semantic object in metadata regardless of `DEBUG_VERBOSITY`.
14. Do not omit title, legend, colorbar, annotations, ticks, tick labels, grid lines, spines, or visible fallback artists from debug metadata when they are present.
15. At `DEBUG_VERBOSITY` 3, include dense small-font position and reference overlays for user-addressable semantic objects and grouped low-level categories.
16. Do not label every repeated low-level Matplotlib artist in the level 3 image unless that is needed to make a user follow-up request unambiguous.

## File usage inside this skill

Read the following files when useful:

1. `assets/figure_request_template.md` for the user-facing input template
2. `assets/style_registry.yaml` for canonical plot-type aliases, registered style presets, TIFF compression rules, style-owned defaults, and field rules
3. `assets/styles/mps_base.mplstyle` for the canonical base style manager
4. `assets/styles/scienceplots/style_manifest.csv` when checking bundled SciencePlots style provenance
5. `references/source-compile.md` for the original design context when historical intent matters

## Verification checklist

Before finishing, confirm internally that:

1. The required inputs are present before generating a figure.
2. `COLORMAP_NAME` is present for contour or heat-map equivalent requests.
3. The selected style path exists.
4. Every registered style ID resolves to a bundled `.mplstyle` file.
5. The LaTeX prerequisites required by the active style chain are available.
6. Labels are written in LaTeX-compatible strings when labels are generated or updated.
7. Units use square brackets when units appear in labels.
8. The output file uses the style-driven format and DPI unless the user explicitly overrides them.
9. Every `.tif` or `.tiff` output was saved with LZW compression.
10. The metadata JSON file exists and records the data source path(s) and creation timestamp.
11. The metadata JSON records `run_mode` for every generated figure.
12. The metadata JSON records `style_chain` and resolved style paths for every generated figure.
13. The metadata JSON records `export_compression: tiff_lzw` for TIFF outputs.
14. In debug mode, both the clean image and `.debug.` image exist.
15. In debug mode, metadata records `debug_verbosity`, `debug_figure_path`, `debug_elements`, `debug_object_count`, `debug_coverage_summary`, and `debug_unclassified_artists`.
16. In debug mode, `debug_elements` includes every visible semantic object at every verbosity level.
17. With `DEBUG_VERBOSITY` 3, the debug image includes zoom-friendly position callouts and reference guides for semantic objects and grouped low-level categories.
