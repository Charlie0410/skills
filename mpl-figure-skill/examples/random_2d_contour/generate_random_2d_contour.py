from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
import math
from pathlib import Path
import random

import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parent
STYLE_PATH = REPO_ROOT / "skills" / "mpl-figure-generator" / "assets" / "styles" / "mps_base.mplstyle"
CSV_PATH = OUTPUT_DIR / "random_contour_data.csv"
TIFF_PATH = OUTPUT_DIR / "random_contour_2d.tiff"
METADATA_PATH = OUTPUT_DIR / "random_contour_2d.metadata.json"
TIFF_LZW_PIL_KWARGS = {"compression": "tiff_lzw"}

X_MIN = -3.0
X_MAX = 3.0
Y_MIN = -2.5
Y_MAX = 2.5
GRID_X = 18
GRID_Y = 14
RANDOM_SEED = 20260404
CONTOUR_LEVELS = 16


def save_figure(figure, output_path: Path) -> None:
    save_kwargs = {}
    if output_path.suffix.lower() in {".tif", ".tiff"}:
        save_kwargs["pil_kwargs"] = TIFF_LZW_PIL_KWARGS

    figure.savefig(output_path, **save_kwargs)


def scalar_field(x_value: float, y_value: float) -> float:
    ridge = 1.15 * math.exp(-0.32 * ((x_value - 0.75) ** 2 + (y_value + 0.45) ** 2))
    wave = 0.85 * math.sin(1.35 * x_value) * math.cos(1.65 * y_value)
    saddle = -0.12 * x_value * y_value
    return ridge + wave + saddle


def build_rows(
    seed: int = RANDOM_SEED,
    grid_x: int = GRID_X,
    grid_y: int = GRID_Y,
) -> list[tuple[float, float, float]]:
    rng = random.Random(seed)
    rows: list[tuple[float, float, float]] = []
    x_step = (X_MAX - X_MIN) / (grid_x - 1)
    y_step = (Y_MAX - Y_MIN) / (grid_y - 1)

    for x_index in range(grid_x):
        for y_index in range(grid_y):
            base_x = X_MIN + x_index * x_step
            base_y = Y_MIN + y_index * y_step

            x_value = base_x
            y_value = base_y

            if 0 < x_index < grid_x - 1:
                x_value += rng.uniform(-0.33 * x_step, 0.33 * x_step)
            if 0 < y_index < grid_y - 1:
                y_value += rng.uniform(-0.33 * y_step, 0.33 * y_step)

            z_value = scalar_field(x_value, y_value) + rng.uniform(-0.08, 0.08)
            rows.append((round(x_value, 4), round(y_value, 4), round(z_value, 5)))

    rows.sort(key=lambda row: (row[0], row[1]))
    return rows


def write_csv(rows: list[tuple[float, float, float]]) -> None:
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["x", "y", "z"])
        writer.writerows(rows)


def build_plot(rows: list[tuple[float, float, float]]) -> None:
    x_values = [row[0] for row in rows]
    y_values = [row[1] for row in rows]
    z_values = [row[2] for row in rows]

    plt.style.use(str(STYLE_PATH))
    figure, axis = plt.subplots()
    filled = axis.tricontourf(
        x_values,
        y_values,
        z_values,
        levels=CONTOUR_LEVELS,
        cmap="jet",
    )
    axis.tricontour(
        x_values,
        y_values,
        z_values,
        levels=CONTOUR_LEVELS,
        colors="black",
        linewidths=0.35,
        alpha=0.55,
    )
    colorbar = figure.colorbar(filled, ax=axis)
    axis.set_xlabel(r"$x [-]$")
    axis.set_ylabel(r"$y [-]$")
    colorbar.set_label(r"$z [-]$")
    axis.set_xlim(X_MIN, X_MAX)
    axis.set_ylim(Y_MIN, Y_MAX)
    figure.tight_layout()

    save_figure(figure, TIFF_PATH)
    plt.close(figure)


def write_metadata(rows: list[tuple[float, float, float]]) -> None:
    payload = {
        "plot_data_source_paths": [str(CSV_PATH.relative_to(REPO_ROOT)).replace("\\", "/")],
        "figure_creation_timestamp": datetime.now(timezone.utc).isoformat(),
        "image_type": "2D contour",
        "image_dimensions": "4.72 in x 3.94 in",
        "mpl_style_path": str(STYLE_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "fullstyle_path_or_spec": "None beyond the canonical mplstyle manager.",
        "element_formatting_spec": "Filled triangulated contour using the jet colormap with 16 levels, thin black contour lines, and LaTeX field-name labels.",
        "output_basename": "random_contour_2d",
        "output_figure_path": str(TIFF_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "export_format": "tiff",
        "export_compression": "tiff_lzw",
        "export_dpi": 300,
        "row_count": len(rows),
        "x_field": "x",
        "y_field": "y",
        "z_field": "z",
        "colormap_name": "jet",
        "contour_level_count": CONTOUR_LEVELS,
        "random_seed": RANDOM_SEED,
    }

    with METADATA_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    write_csv(rows)
    build_plot(rows)
    write_metadata(rows)


if __name__ == "__main__":
    main()
