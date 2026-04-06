# Example Request

This example matches the revised `mpl-figure-generator` behavior: create a finished figure directly instead of returning an instruction packet.

```text
<USER_MATERIALS>
<DATA_FILE_PATHS>
examples/random_2d_line/random_line_data.csv
</DATA_FILE_PATHS>

<DATA_STRUCTURE_DESCRIPTION>
CSV with numeric columns `x` and `y`. Use `x` for the horizontal coordinate and `y` for a single 2D line series. Render labels in LaTeX and write units in square brackets.
</DATA_STRUCTURE_DESCRIPTION>

<IMAGE_TYPE>
2D Line
</IMAGE_TYPE>

<DATA_CREATION_INSTRUCTIONS>
Generate the CSV first if it does not already exist.
</DATA_CREATION_INSTRUCTIONS>

<MPL_STYLE_PATH>
skills/mpl-figure-generator/assets/styles/mps_base.mplstyle
</MPL_STYLE_PATH>

<ELEMENT_FORMATTING_SPEC>
Draw one solid line in `#0f4c81` with linewidth `2.0`.
</ELEMENT_FORMATTING_SPEC>

<ADDITIONAL_IMAGE_SPECIFICATIONS>
Disable the grid and title the plot as a LaTeX string.
</ADDITIONAL_IMAGE_SPECIFICATIONS>

<OUTPUT_BASENAME>
random_line_2d
</OUTPUT_BASENAME>
</USER_MATERIALS>
```
