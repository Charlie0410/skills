#!/usr/bin/env python3
"""Basic checks for aca-slide-gen HTML output.

This script is intentionally conservative and dependency-free. It checks for
required markers, embedded CSS, 16:9 canvas hints, font and color rules, and
external dependencies. It cannot prove visual fit; render inspection is still
required for dense slides.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def check_html(text: str, allow_external: bool = False) -> dict[str, object]:
    checks: dict[str, bool] = {}
    lower = text.lower()

    checks["has_doctype"] = "<!doctype html" in lower
    checks["has_html_root"] = bool(re.search(r"<html\b", text, re.IGNORECASE)) and bool(re.search(r"</html>", text, re.IGNORECASE))
    checks["has_embedded_css"] = bool(re.search(r"<style\b[^>]*>.*?</style>", text, re.IGNORECASE | re.DOTALL))
    checks["has_slide_container"] = bool(re.search(r"class=[\"'][^\"']*\bslide\b", text, re.IGNORECASE))
    checks["has_section_title_marker"] = "section-title" in text or "section_title" in text
    checks["has_separator_marker"] = "title-rule" in text or "separator" in lower or "border-bottom" in lower
    checks["has_16_9_hint"] = bool(re.search(r"aspect-ratio\s*:\s*16\s*/\s*9", text, re.IGNORECASE)) or (
        bool(re.search(r"width\s*:\s*(1600|1280)px", text, re.IGNORECASE))
        and bool(re.search(r"height\s*:\s*(900|720)px", text, re.IGNORECASE))
    )
    checks["has_chinese_font"] = "微软雅黑" in text or "Microsoft YaHei" in text
    checks["has_english_font"] = "Calibri" in text
    checks["has_caption_background"] = "#ffc000" in lower
    checks["has_caption_text_color"] = "#000000" in lower
    checks["has_blue_emphasis"] = "#0000aa" in lower
    checks["has_red_emphasis"] = "#de0000" in lower
    checks["external_dependencies_allowed_or_absent"] = allow_external or not bool(
        re.search(r"<(script|link|img)\b[^>]*(https?://|//)", text, re.IGNORECASE)
    )

    failed = [name for name, passed in checks.items() if not passed]
    return {
        "passed": not failed,
        "failed_checks": failed,
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate basic aca-slide-gen HTML requirements.")
    parser.add_argument("html_file", type=Path, help="Path to generated slide HTML")
    parser.add_argument("--allow-external", action="store_true", help="Allow external dependencies in script, link, or image URLs")
    args = parser.parse_args()

    if not args.html_file.exists():
        print(json.dumps({"passed": False, "error": "file not found"}, indent=2), file=sys.stderr)
        return 2

    text = args.html_file.read_text(encoding="utf-8")
    result = check_html(text, allow_external=args.allow_external)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
