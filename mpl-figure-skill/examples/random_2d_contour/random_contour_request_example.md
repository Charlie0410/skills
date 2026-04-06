# Example Request

This example matches the revised `mpl-figure-generator` behavior: create a finished figure directly instead of returning an instruction packet.

```text
<USER_MATERIALS>
<DATA_FILE_PATHS>
examples/random_2d_contour/random_contour_data.csv
</DATA_FILE_PATHS>

<DATA_STRUCTURE_DESCRIPTION>
CSV with numeric columns `x`, `y`, and `z`. Use `x` and `y` as planar coordinates and `z` as the scalar field for a 2D contour plot.
</DATA_STRUCTURE_DESCRIPTION>

<IMAGE_TYPE>
2D contour
</IMAGE_TYPE>

<DATA_CREATION_INSTRUCTIONS>
Generate the CSV first if it does not already exist, using synthetic random demo data.
</DATA_CREATION_INSTRUCTIONS>

<MPL_STYLE_PATH>
skills/mpl-figure-generator/assets/styles/mps_base.mplstyle
</MPL_STYLE_PATH>

<ELEMENT_FORMATTING_SPEC>
Render a filled contour with the `jet` colormap, 16 contour levels, and thin black contour lines.
</ELEMENT_FORMATTING_SPEC>

<COLORMAP_NAME>
jet
</COLORMAP_NAME>

<ADDITIONAL_IMAGE_SPECIFICATIONS>
Use LaTeX field-name labels for the axes and colorbar.
</ADDITIONAL_IMAGE_SPECIFICATIONS>

<OUTPUT_BASENAME>
random_contour_2d
</OUTPUT_BASENAME>
</USER_MATERIALS>
```
