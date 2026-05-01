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

Create or update the figure output, any helper script needed for repeatability, the data file when the user explicitly asks for synthetic or demo data, and a companion metadata JSON file.

## Prerequisites

1. Use Matplotlib as the primary plotting backend.
2. Ensure the LaTeX runtime is available before using `assets/styles/mps_base.mplstyle` because the canonical style enables `text.usetex : True`.
3. Require `latex` and `pdflatex` on `PATH`.
4. Require the LaTeX packages `lmodern` and `siunitx`.
5. Stop and report the missing prerequisite if the canonical style cannot run as configured. Do not silently disable LaTeX.
6. Use the existing repository layout unless the user explicitly asks for a different placement.

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
3. `ELEMENT_FORMATTING_SPEC`
4. `ADDITIONAL_IMAGE_SPECIFICATIONS`
5. `OUTPUT_BASENAME`
6. `SAMPLE_ROWS_OR_SCHEMA_SNIPPETS`
7. `RUN_MODE`
8. `DEBUG_VERBOSITY`

Runtime mode fields:

1. `RUN_MODE` defaults to `production` when omitted.
2. Valid `RUN_MODE` values are `production` and `debug`.
3. `production` preserves the clean finished-figure workflow.
4. `debug` exports the clean production figure first, then exports a second annotated debug figure for second-pass adjustment.
5. `DEBUG_VERBOSITY` is used only when `RUN_MODE` is `debug`.
6. Valid `DEBUG_VERBOSITY` values are `1`, `2`, and `3`.
7. `DEBUG_VERBOSITY` defaults to `2` in debug mode when omitted.

## Ease-of-use rules

1. Accept common aliases and normalize them internally:
   * `2D Line`, `line`, `line plot`
   * `2D Symbol`, `symbol`, `scatter`, `symbol/scatter`
   * `2D contour`, `contour`, `contour plot`
   * `Polar Plot`, `polar`, `polar plot`
2. Default `MPL_STYLE_PATH` to `assets/styles/mps_base.mplstyle` when the user does not explicitly override the style.
3. Treat the selected mplstyle file as the factual source for figure size, export format, DPI, and padding defaults. Do not require the user to restate those defaults.
4. Treat `ELEMENT_FORMATTING_SPEC` and `ADDITIONAL_IMAGE_SPECIFICATIONS` as optional artist-level refinements rather than mandatory inputs.
5. Generate a data file only when the user explicitly asks for synthetic, random, demo, or placeholder data. Record the generated data path in metadata.
6. Preserve unresolved placeholders rather than inventing names, schema details, label text, units, styles, or colormaps.
7. Render labels, legend text, and colorbar labels in LaTeX-compatible strings when they appear in the figure.
8. Write units in square brackets, for example `$\\mathrm{Time}\\ [s]$` or `$\\mathrm{Signal}\\ [a.u.]$`.

## Style manager policy

Use `assets/styles/mps_base.mplstyle` as the canonical style manager unless the user explicitly provides another style path.

Rules:

1. Load the canonical mplstyle file before creating the figure.
2. Treat the mplstyle file as the authoritative source for export defaults.
3. Apply any user-requested style override explicitly in code or local `rcParams`.
4. Keep the canonical style active even when artist-level adjustments are added on top.
5. Do not silently replace the canonical style with inferred defaults.

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

Verify the LaTeX prerequisites when the canonical style is in use.
Check whether the required fields are present.
If the plot type is contour or heat-map equivalent, verify that `COLORMAP_NAME` is present.

### Step 2. Normalize inputs

Normalize plot-type aliases to one canonical label.
Normalize file paths exactly as provided.
Default the style path to `assets/styles/mps_base.mplstyle` when the user does not provide one.
Default `RUN_MODE` to `production` when the user does not provide one.
In debug mode, default `DEBUG_VERBOSITY` to `2` when the user does not provide one.
Reject unsupported `RUN_MODE` values.
In debug mode, reject unsupported `DEBUG_VERBOSITY` values instead of guessing.

### Step 3. Resolve the data source

Read the provided data source when files already exist.
Generate the data file first when the user explicitly requests synthetic or demo data and has provided enough schema and path information to do so safely.

### Step 4. Inspect style facts

Read the selected mplstyle file and treat it as the source of truth for:

1. Figure dimensions
2. Export format
3. Export DPI
4. Bounding-box behavior
5. Padding
6. Font and TeX settings

### Step 5. Build the figure

Load and preprocess the data.
Construct the requested Matplotlib figure.
Apply the canonical style plus any explicit artist-level overrides.
Format labels in LaTeX-compatible strings and write units in square brackets.

### Step 6. Export outputs

Export the clean production figure using the format and DPI dictated by the active mplstyle unless the user explicitly overrides those settings.

When `RUN_MODE` is `production`, stop after writing the clean figure and companion metadata.

When `RUN_MODE` is `debug`:

1. Save the clean production figure before adding diagnostic overlays.
2. Build a diagnostic annotation layer on the same figure after the clean export succeeds.
3. Save the annotated debug figure as `<OUTPUT_BASENAME>.debug.<style_format>`.
4. Preserve the style-driven export format, DPI, bounding-box behavior, and padding for both images.
5. Use high-contrast callout boxes and connector lines for debug labels.
6. Use `usetex=False` for debug annotation text so labels that contain property strings do not break LaTeX-enabled production styles.
7. Keep the debug image human-readable; put exhaustive low-level detail in metadata rather than overcrowding the figure.

Create a companion metadata JSON file that records at least:

1. Plot data source path(s)
2. Figure creation timestamp
3. Plot type
4. Style path
5. Output figure path
6. Run mode

In debug mode, also record:

1. Debug verbosity
2. Debug figure path
3. Debug elements and their stable user-addressable IDs

#### Debug element naming

Use stable semantic IDs for user-addressable Matplotlib elements. Prefer names that a user can refer to in a follow-up request without knowing Matplotlib internals.

Common IDs include:

1. `figure`
2. `main_axes`
3. `x_label`
4. `y_label`
5. `title`
6. `legend`
7. `colorbar`
8. `colorbar_label`
9. `series_1`, `series_2`, and later numbered line series
10. `scatter_1`, `scatter_2`, and later numbered scatter groups
11. `contour_fill`
12. `contour_lines`
13. `annotation_1`, `annotation_2`, and later numbered annotations

Group repetitive low-level objects by default, including ticks, tick labels, grid lines, spines, and contour polygons. Provide per-object IDs only when the user explicitly asks for that level of detail.

#### Debug verbosity

Use `DEBUG_VERBOSITY` to control how much diagnostic information appears in callouts and metadata:

1. `1`: element ID and element type.
2. `2`: level 1 plus key user-facing attributes such as text or label, color, linewidth, linestyle, marker, colormap, alpha, and axes association.
3. `3`: level 2 plus position or extents, z-order, transform and layout notes, contour levels or counts, collection sizes, and colorbar or mappable details where available.

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
5. Missing prerequisite: LaTeX runtime or required packages for the canonical style
6. Unsupported `RUN_MODE` value
7. Unsupported `DEBUG_VERBOSITY` value in debug mode

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

## File usage inside this skill

Read the following files when useful:

1. `assets/figure_request_template.md` for the user-facing input template
2. `assets/style_registry.yaml` for canonical plot-type aliases, style-owned defaults, and field rules
3. `assets/styles/mps_base.mplstyle` for the canonical base style manager
4. `references/source-compile.md` for the original design context when historical intent matters

## Verification checklist

Before finishing, confirm internally that:

1. The required inputs are present before generating a figure.
2. `COLORMAP_NAME` is present for contour or heat-map equivalent requests.
3. The selected style path exists.
4. The LaTeX prerequisites required by the active style are available.
5. Labels are written in LaTeX-compatible strings when labels are generated or updated.
6. Units use square brackets when units appear in labels.
7. The output file uses the style-driven format and DPI unless the user explicitly overrides them.
8. The metadata JSON file exists and records the data source path(s) and creation timestamp.
9. The metadata JSON records `run_mode` for every generated figure.
10. In debug mode, both the clean image and `.debug.` image exist.
11. In debug mode, metadata records `debug_verbosity`, `debug_figure_path`, and `debug_elements`.
