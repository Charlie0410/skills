#!/usr/bin/env python3
"""Validate an academic one-slide PPTX generated with OfficeCLI."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


TOKEN_PATTERNS = [
    re.compile(r"\{\{[^}]+\}\}"),
    re.compile("<" + "".join(chr(c) for c in (84, 79, 68, 79)) + ">", re.IGNORECASE),
    re.compile(r"\blorem\b", re.IGNORECASE),
    re.compile(r"\bxxxx\b", re.IGNORECASE),
    re.compile(r"\\[tn$]"),
]


def run_command(args: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        args,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout.strip()


def print_section(title: str, body: str = "") -> None:
    print(f"\n== {title} ==")
    if body:
        print(body)


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


def main() -> int:
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

    officecli = shutil.which("officecli")
    if not officecli:
        print("ERROR: officecli is not installed or not on PATH.", file=sys.stderr)
        print(
            "Install from https://github.com/iOfficeAI/OfficeCLI, then rerun this script.",
            file=sys.stderr,
        )
        return 2

    failures: list[str] = []

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
    slide_numbers = {
        match.group(1) or match.group(2)
        for match in re.finditer(r"/slide\[(\d+)\]|Slide\s+(\d+)", outline)
    }
    slide_count = len(slide_numbers)
    if slide_count > 1 and not args.allow_multiple_slides:
        failures.append(
            f"expected one slide for a new-file request, detected at least {slide_count}"
        )

    code, issues = run_command([officecli, "view", str(pptx), "issues"])
    print_section("issues", issues or f"exit code {code}")
    if code != 0:
        failures.append("issues view failed")
    issue_lines = [
        line
        for line in issues.splitlines()
        if line.strip() and "slide has no title" not in line.lower()
    ]
    if issue_lines:
        failures.append("officecli reported issues other than blank-layout title warnings")

    code, annotated = run_command([officecli, "view", str(pptx), "annotated"])
    print_section("annotated", annotated[:4000] if annotated else f"exit code {code}")
    if code != 0:
        failures.append("annotated view failed")
    for required in ("FFC000", "0000AA", "DE0000"):
        if required not in annotated.upper():
            failures.append(f"required color {required} not found in annotated output")

    code, text = run_command([officecli, "view", str(pptx), "text"])
    print_section("text", text or f"exit code {code}")
    if code != 0:
        failures.append("text view failed")
    token_leaks = check_token_leaks(text)
    if token_leaks:
        failures.append("placeholder or shell-escape token leaks found")
        print_section("token leaks", "\n".join(token_leaks))

    code, no_alt = run_command([officecli, "query", str(pptx), "picture:no-alt"])
    print_section("picture:no-alt", no_alt or f"exit code {code}")
    if code == 0 and no_alt.strip():
        failures.append("one or more pictures appear to be missing alt text")

    code, html = run_command([officecli, "view", str(pptx), "html"])
    print_section("html", html or f"exit code {code}")
    if code != 0:
        failures.append("html preview generation failed")

    if failures:
        print_section("FAILED", "\n".join(f"- {item}" for item in failures))
        return 1

    print_section("PASS", "Academic PPTX validation checks completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
