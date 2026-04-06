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
CSV_PATH = OUTPUT_DIR / "random_line_data.csv"
TIFF_PATH = OUTPUT_DIR / "random_line_2d.tiff"
METADATA_PATH = OUTPUT_DIR / "random_line_2d.metadata.json"


def build_series(seed: int = 20260404, points: int = 120) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    rows: list[tuple[float, float]] = []

    for index in range(points):
        x_value = index * 0.1
        baseline = 0.55 * math.sin(x_value) + 0.03 * index
        noise = rng.uniform(-0.08, 0.08)
        y_value = baseline + noise
        rows.append((round(x_value, 3), round(y_value, 4)))

    return rows


def write_csv(rows: list[tuple[float, float]]) -> None:
    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["x", "y"])
        writer.writerows(rows)


def build_plot(rows: list[tuple[float, float]]) -> None:
    x_values = [row[0] for row in rows]
    y_values = [row[1] for row in rows]

    plt.style.use(str(STYLE_PATH))
    figure, axis = plt.subplots()
    axis.plot(x_values, y_values, color="#0f4c81", linewidth=2.0, linestyle="-")
    axis.set_xlabel(r"$\mathrm{Time}\ [a.u.]$")
    axis.set_ylabel(r"$\mathrm{Signal}\ [a.u.]$")
    axis.set_title(r"$\mathrm{Random\ Generated\ 2D\ Line}$")
    axis.grid(False)
    figure.tight_layout()

    figure.savefig(TIFF_PATH)
    plt.close(figure)


def write_metadata(rows: list[tuple[float, float]]) -> None:
    payload = {
        "plot_data_source_paths": [str(CSV_PATH.relative_to(REPO_ROOT)).replace("\\", "/")],
        "figure_creation_timestamp": datetime.now(timezone.utc).isoformat(),
        "image_type": "2D Line",
        "image_dimensions": "4.72 in x 3.94 in",
        "mpl_style_path": str(STYLE_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "fullstyle_path_or_spec": "None beyond the canonical mplstyle manager.",
        "element_formatting_spec": "Single series using a solid #0f4c81 line with linewidth 2.0 and LaTeX-rendered labels with square-bracketed units.",
        "output_basename": "random_line_2d",
        "output_figure_path": str(TIFF_PATH.relative_to(REPO_ROOT)).replace("\\", "/"),
        "export_format": "tiff",
        "export_dpi": 300,
        "row_count": len(rows),
        "x_field": "x",
        "y_field": "y",
        "random_seed": 20260404,
    }

    with METADATA_PATH.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_series()
    write_csv(rows)
    build_plot(rows)
    write_metadata(rows)


if __name__ == "__main__":
    main()
