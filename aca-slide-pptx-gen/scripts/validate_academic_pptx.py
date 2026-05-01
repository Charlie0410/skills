#!/usr/bin/env python3
"""Validate an academic one-slide PPTX generated with OfficeCLI."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


CANVAS_WIDTH_CM = 33.87
CANVAS_HEIGHT_CM = 19.05
MIN_VISIBLE_FONT_PT = 18.0
PREFERRED_BODY_FONT_PT = 24.0
DEFAULT_OFFICECLI = Path(r"C:\Users\charlie\AppData\Local\OfficeCli\officecli.exe")

TOKEN_PATTERNS = [
    re.compile(r"\{\{[^}]+\}\}"),
    re.compile("<" + "".join(chr(c) for c in (84, 79, 68, 79)) + ">", re.IGNORECASE),
    re.compile(r"\blorem\b", re.IGNORECASE),
    re.compile(r"\bxxxx\b", re.IGNORECASE),
    re.compile(r"\\[tn$]"),
]

BULLET_RE = re.compile(r"^\s*(?:[-*•‣▪◦]|\d+[.)])\s+")
NAME_RE = re.compile(r"\bname=([^\s]+)")
SIZE_RE = re.compile(r"\bsize=(\d+(?:\.\d+)?)pt\b", re.IGNORECASE)


def run_command(args: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        args,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout.strip()


def print_section(title: str, body: str = "") -> None:
    print(f"\n== {title} ==")
    if body:
        print(body)


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def resolve_officecli() -> str | None:
    candidates: list[str] = []
    env_path = os.environ.get("OFFICECLI_PATH")
    if env_path:
        candidates.append(env_path)
    path_match = shutil.which("officecli")
    if path_match:
        candidates.append(path_match)
    candidates.append(str(DEFAULT_OFFICECLI))

    for candidate in candidates:
        expanded = os.path.expandvars(os.path.expanduser(candidate))
        candidate_path = Path(expanded)
        if candidate_path.is_file():
            return str(candidate_path)
        which_match = shutil.which(candidate)
        if which_match:
            return which_match
    return None


def has_validate_success(output: str) -> bool:
    lowered = output.lower()
    return (
        "no errors found" in lowered
        or "validation passed" in lowered
        or re.search(r"\bvalid\b", lowered) is not None and "error" not in lowered
    )


def check_token_leaks(text: str) -> list[str]:
    findings: list[str] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern in TOKEN_PATTERNS:
            if pattern.search(line):
                findings.append(f"line {line_no}: {line}")
                break
    return findings


def parse_slide_count(outline: str) -> int:
    summary = re.search(r"\|\s*(\d+)\s+slides?\b", outline, re.IGNORECASE)
    if summary:
        return int(summary.group(1))
    slide_numbers = {
        match.group(1) or match.group(2)
        for match in re.finditer(r"/slide\[(\d+)\]|Slide\s+(\d+)", outline)
    }
    return len(slide_numbers)


def check_text_density(text: str) -> list[str]:
    warnings: list[str] = []
    bullet_count = sum(1 for line in text.splitlines() if BULLET_RE.match(line))
    if bullet_count > 5:
        warnings.append(f"visible bullet count is high ({bullet_count}); target 3-5 bullets")

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for index, paragraph in enumerate(paragraphs, start=1):
        compact = " ".join(paragraph.split())
        if len(compact) > 320:
            warnings.append(
                f"paragraph block {index} is long ({len(compact)} characters); move detail to notes"
            )

    for line_no, line in enumerate(text.splitlines(), start=1):
        compact = " ".join(line.split())
        if len(compact) > 180:
            warnings.append(
                f"line {line_no} is long ({len(compact)} characters); check projected readability"
            )
    return warnings


def parse_length_cm(value: str) -> float | None:
    match = re.fullmatch(r"(-?\d+(?:\.\d+)?)(cm|in|pt)?", value.strip(), re.IGNORECASE)
    if not match:
        return None
    amount = float(match.group(1))
    unit = (match.group(2) or "cm").lower()
    if unit == "cm":
        return amount
    if unit == "in":
        return amount * 2.54
    if unit == "pt":
        return amount * 2.54 / 72.0
    return None


def parse_geometry(line: str) -> dict[str, float]:
    geometry: dict[str, float] = {}
    for key in ("x", "y", "width", "height"):
        match = re.search(rf"\b{key}=(-?\d+(?:\.\d+)?(?:cm|in|pt)?)\b", line, re.IGNORECASE)
        if match:
            parsed = parse_length_cm(match.group(1))
            if parsed is not None:
                geometry[key] = parsed
    return geometry


def check_geometry(lines: list[str]) -> list[str]:
    failures: list[str] = []
    for line in lines:
        geometry = parse_geometry(line)
        if not {"x", "y", "width", "height"}.issubset(geometry):
            continue
        x = geometry["x"]
        y = geometry["y"]
        width = geometry["width"]
        height = geometry["height"]
        label = line.split()[0]
        if x < -0.01 or y < -0.01:
            failures.append(f"{label} starts outside the canvas")
        if width < -0.01 or height < -0.01:
            failures.append(f"{label} has negative width or height")
        if x + width > CANVAS_WIDTH_CM + 0.01:
            failures.append(f"{label} exceeds slide width ({x + width:.2f}cm)")
        if y + height > CANVAS_HEIGHT_CM + 0.01:
            failures.append(f"{label} exceeds slide height ({y + height:.2f}cm)")
    return failures


def shape_name(line: str) -> str | None:
    match = NAME_RE.search(line)
    if match:
        return match.group(1)
    return None


def has_text_payload(line: str) -> bool:
    quoted = re.search(r'"([^"]*)"', line)
    return bool(quoted and quoted.group(1).strip())


def check_shape_rules(shape_query: str) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    lines = [line for line in shape_query.splitlines() if line.strip()]
    names = {name for line in lines if (name := shape_name(line))}

    if lines and "SectionTitle" not in names:
        failures.append("required named shape SectionTitle was not found")

    if lines and not ({"MainClaim", "CentralClaim"} & names):
        warnings.append("no named MainClaim/CentralClaim shape found; confirm the central message is clear")

    if lines and "EvidenceVisual" not in names:
        warnings.append("no named EvidenceVisual shape found; confirm the main evidence object is identifiable")

    if lines and not any(name.startswith("Caption") for name in names):
        warnings.append("no named Caption shape found; confirm evidence captions are present when needed")

    for line in lines:
        if not has_text_payload(line):
            continue
        size_match = SIZE_RE.search(line)
        if size_match:
            size = float(size_match.group(1))
            name = shape_name(line) or line.split()[0]
            if size < MIN_VISIBLE_FONT_PT:
                failures.append(f"{name} uses {size:g}pt text below the 18pt visible floor")
            if name.startswith("Body") and size < PREFERRED_BODY_FONT_PT:
                warnings.append(f"{name} uses {size:g}pt body text; prefer 24pt+")

    for line in lines:
        name = shape_name(line)
        if not name or not name.startswith("Caption"):
            continue
        if "italic=true" not in line.lower():
            warnings.append(f"{name} is not marked italic in OfficeCLI query output")
        fill_match = re.search(r"\bfill=([^\s]+)", line, re.IGNORECASE)
        if fill_match and fill_match.group(1).lower() not in {"none", "transparent"}:
            warnings.append(f"{name} has fill={fill_match.group(1)}; captions default to no fill")
    return failures, warnings


def check_connector_rules(connector_query: str) -> list[str]:
    warnings: list[str] = []
    lines = [line for line in connector_query.splitlines() if line.strip()]
    if not lines:
        warnings.append("no connector found; confirm the header separator exists")
        return warnings

    separator_candidates = [
        line
        for line in lines
        if "linewidth=2pt" in line.lower()
        and (width := parse_geometry(line).get("width")) is not None
        and width >= 31.0
    ]
    if not separator_candidates:
        warnings.append("no connector spans the safe width with linewidth=2pt")
    return warnings


def main() -> int:
    configure_stdio()

    parser = argparse.ArgumentParser(
        description="Run focused OfficeCLI checks for an academic one-slide PPTX."
    )
    parser.add_argument("pptx", help="Path to the generated .pptx file")
    parser.add_argument(
        "--allow-multiple-slides",
        action="store_true",
        help="Allow decks with more than one slide when modifying an existing deck.",
    )
    args = parser.parse_args()

    pptx = Path(args.pptx)
    if pptx.suffix.lower() != ".pptx":
        print(f"ERROR: expected a .pptx file, got: {pptx}", file=sys.stderr)
        return 2
    if not pptx.exists():
        print(f"ERROR: file does not exist: {pptx}", file=sys.stderr)
        return 2

    officecli = resolve_officecli()
    if not officecli:
        print(
            "ERROR: officecli was not found via OFFICECLI_PATH, PATH, or "
            f"{DEFAULT_OFFICECLI}.",
            file=sys.stderr,
        )
        print(
            "Install from https://github.com/iOfficeAI/OfficeCLI, then rerun this script.",
            file=sys.stderr,
        )
        return 2

    failures: list[str] = []
    warnings: list[str] = []

    code, output = run_command([officecli, "close", str(pptx)])
    print_section("close", output or f"exit code {code}")

    code, output = run_command([officecli, "validate", str(pptx)])
    print_section("validate", output or f"exit code {code}")
    if code != 0 or not has_validate_success(output):
        failures.append("schema validation did not report a clean pass")

    code, outline = run_command([officecli, "view", str(pptx), "outline"])
    print_section("outline", outline or f"exit code {code}")
    if code != 0:
        failures.append("outline view failed")
    slide_count = parse_slide_count(outline)
    if slide_count != 1 and not args.allow_multiple_slides:
        failures.append(
            f"expected one slide for a new-file request, detected {slide_count}"
        )

    code, issues = run_command([officecli, "view", str(pptx), "issues"])
    print_section("issues", issues or f"exit code {code}")
    if code != 0:
        failures.append("issues view failed")
    issue_lines = []
    for line in issues.splitlines():
        stripped = line.strip()
        if not re.match(r"^\[[A-Z]\d+\]", stripped):
            continue
        if "slide has no title" in stripped.lower():
            continue
        issue_lines.append(stripped)
    if issue_lines:
        failures.append("officecli reported issues other than blank-layout title warnings")

    code, annotated = run_command([officecli, "view", str(pptx), "annotated"])
    print_section("annotated", annotated[:4000] if annotated else f"exit code {code}")
    if code != 0:
        failures.append("annotated view failed")

    code, text = run_command([officecli, "view", str(pptx), "text"])
    print_section("text", text or f"exit code {code}")
    if code != 0:
        failures.append("text view failed")
    token_leaks = check_token_leaks(text)
    if token_leaks:
        failures.append("placeholder or shell-escape token leaks found")
        print_section("token leaks", "\n".join(token_leaks))
    warnings.extend(check_text_density(text))

    geometry_lines: list[str] = []

    code, shape_query = run_command([officecli, "query", str(pptx), "shape"])
    print_section("query shape", shape_query or f"exit code {code}")
    if code != 0:
        warnings.append("shape query failed; skipped named-shape, font-size, and shape-bounds checks")
    else:
        shape_failures, shape_warnings = check_shape_rules(shape_query)
        failures.extend(shape_failures)
        warnings.extend(shape_warnings)
        geometry_lines.extend(shape_query.splitlines())

    code, connector_query = run_command([officecli, "query", str(pptx), "connector"])
    print_section("query connector", connector_query or f"exit code {code}")
    if code != 0:
        warnings.append("connector query failed; skipped separator-bounds checks")
    else:
        warnings.extend(check_connector_rules(connector_query))
        geometry_lines.extend(connector_query.splitlines())

    code, picture_query = run_command([officecli, "query", str(pptx), "picture"])
    print_section("query picture", picture_query or f"exit code {code}")
    if code != 0:
        warnings.append("picture query failed; skipped picture-bounds checks")
    else:
        geometry_lines.extend(picture_query.splitlines())

    failures.extend(check_geometry(geometry_lines))

    code, no_alt = run_command([officecli, "query", str(pptx), "picture:no-alt"])
    print_section("picture:no-alt", no_alt or f"exit code {code}")
    if code == 0 and no_alt.strip():
        failures.append("one or more pictures appear to be missing alt text")

    code, html = run_command([officecli, "view", str(pptx), "html"])
    print_section("html", html or f"exit code {code}")
    if code != 0:
        failures.append("html preview generation failed")

    if warnings:
        print_section("WARNINGS", "\n".join(f"- {item}" for item in warnings))

    if failures:
        print_section("FAILED", "\n".join(f"- {item}" for item in failures))
        return 1

    print_section("PASS", "Academic PPTX validation checks completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
