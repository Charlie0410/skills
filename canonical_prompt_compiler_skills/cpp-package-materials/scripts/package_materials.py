#!/usr/bin/env python3
"""Package local materials referenced by a compiled CPP prompt."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKIP_DIRS = {".git", ".trash", "__pycache__"}
SKIP_SUFFIXES = {".pyc", ".pyo"}
URL_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://")
TAG_BLOCK_RE = re.compile(
    r"<(REFERENCE_MATERIALS|TRUSTED_CONTEXT|UNTRUSTED_INPUT)>\s*(.*?)\s*</\1>",
    re.IGNORECASE | re.DOTALL,
)
LIST_MARKER_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)]|[A-Za-z][.)])\s+")
CHECKBOX_RE = re.compile(r"^\[[ xX]\]\s+")


@dataclass
class Binding:
    value: Any
    base_dir: Path
    origin: str


@dataclass
class IncludedFile:
    material_id: str
    source_path: Path
    archive_path: str
    size: int


@dataclass
class MaterialStatus:
    material_id: str
    bindings: list[str] = field(default_factory=list)
    included: list[IncludedFile] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    external: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    @property
    def has_packaged_file(self) -> bool:
        return bool(self.included)

    @property
    def has_unresolved_binding(self) -> bool:
        return bool(self.missing or self.external or self.skipped)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package local materials required by a CPP .compiled-prompt.md file."
    )
    parser.add_argument("compiled_prompt", type=Path, help="Compiled prompt markdown file.")
    parser.add_argument("--map", dest="map_path", type=Path, help="Materials map JSON file.")
    parser.add_argument(
        "--material",
        action="append",
        default=[],
        metavar="ID=PATH",
        help="Additional logical material binding. May be repeated.",
    )
    parser.add_argument("--output", type=Path, help="Output zip path.")
    parser.add_argument("--manifest", type=Path, help="Output sidecar manifest path.")
    return parser.parse_args(argv)


def compiled_base_name(path: Path) -> str:
    name = path.name
    suffix = ".compiled-prompt.md"
    if name.endswith(suffix):
        return name[: -len(suffix)]
    if name.endswith(".md"):
        return name[:-3]
    return path.stem


def default_paths(compiled_prompt: Path) -> tuple[Path, Path, Path]:
    base = compiled_base_name(compiled_prompt)
    parent = compiled_prompt.parent
    return (
        parent / f"{base}.materials-map.json",
        parent / f"{base}.materials.zip",
        parent / f"{base}.materials-manifest.md",
    )


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8")


def add_ordered(target: OrderedDict[str, None], value: str) -> None:
    if value and value not in target:
        target[value] = None


def is_relevant_label(label: str) -> bool:
    normalized = label.upper().replace(" ", "_").replace("-", "_")
    return (
        "MATERIAL" in normalized
        or normalized in {"RUNTIME_PAYLOAD", "REQUIRED_INPUTS", "AVAILABLE_INPUTS"}
        or normalized == "MINIMUM_ADDITIONAL_MATERIALS_NEEDED"
    )


def is_new_section(line: str) -> bool:
    stripped = line.strip()
    if re.match(r"^#{1,6}\s+\S", stripped):
        return True
    return bool(re.match(r"^[A-Z][A-Z0-9 _-]{2,}:\s*$", stripped))


def looks_like_candidate_line(line: str) -> bool:
    stripped = line.strip()
    return bool(
        LIST_MARKER_RE.match(stripped)
        or stripped.startswith("|")
        or "|" in stripped
        or CHECKBOX_RE.match(stripped)
    )


def normalize_candidate(line: str) -> str | None:
    text = line.strip()
    if not text:
        return None
    if text.startswith("```") or text in {"---", "..."}:
        return None
    if re.fullmatch(r"</?[A-Za-z_][A-Za-z0-9_-]*>", text):
        return None

    text = LIST_MARKER_RE.sub("", text).strip()
    text = CHECKBOX_RE.sub("", text).strip()
    if "|" in text:
        parts = [part.strip() for part in text.strip("|").split("|") if part.strip()]
        if parts:
            text = parts[0]
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.strip("`*_ \t\r\n")
    text = text.rstrip(".,;")
    if ":" in text:
        prefix, suffix = text.split(":", 1)
        if prefix.upper() in {"MISSING", "REQUIRED", "MATERIAL", "INPUT"} and suffix.strip():
            text = suffix.strip()

    lowered = text.lower()
    if lowered in {"none", "n/a", "na", "not applicable", "not provided", "to be provided"}:
        return None
    if re.fullmatch(r"\{\{[^{}]+\}\}", text):
        return None
    if len(text) > 200:
        return None
    return text or None


def extract_material_ids(text: str) -> list[str]:
    candidates: OrderedDict[str, None] = OrderedDict()

    for match in TAG_BLOCK_RE.finditer(text):
        for line in match.group(2).splitlines():
            candidate = normalize_candidate(line)
            if candidate:
                add_ordered(candidates, candidate)

    active = False
    for line in text.splitlines():
        stripped = line.strip()
        label_match = re.match(r"^(?:#{1,6}\s*)?([A-Za-z][A-Za-z0-9 _-]*):\s*(.*)$", stripped)
        if label_match:
            label = label_match.group(1).strip()
            remainder = label_match.group(2).strip()
            if is_relevant_label(label):
                active = True
                candidate = normalize_candidate(remainder)
                if candidate:
                    add_ordered(candidates, candidate)
                continue
            if active and is_new_section(stripped):
                active = False

        if not active:
            continue
        if is_new_section(stripped):
            active = False
            continue
        if looks_like_candidate_line(stripped):
            candidate = normalize_candidate(stripped)
            if candidate:
                add_ordered(candidates, candidate)

    return list(candidates.keys())


def load_materials_map(path: Path) -> tuple[OrderedDict[str, Any], bool]:
    if not path.exists():
        return OrderedDict(), False
    try:
        data = json.loads(read_text(path), object_pairs_hook=OrderedDict)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in materials map {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Materials map must be a JSON object: {path}")
    materials = data.get("materials", OrderedDict())
    if not isinstance(materials, dict):
        raise ValueError(f"Materials map field 'materials' must be an object: {path}")
    return OrderedDict(materials), True


def parse_cli_materials(values: list[str], cwd: Path) -> OrderedDict[str, list[Binding]]:
    bindings: OrderedDict[str, list[Binding]] = OrderedDict()
    for raw in values:
        if "=" not in raw:
            raise ValueError(f"--material must use ID=PATH syntax: {raw}")
        name, path_value = raw.split("=", 1)
        name = name.strip()
        path_value = path_value.strip()
        if not name:
            raise ValueError(f"--material is missing a logical material ID: {raw}")
        bindings.setdefault(name, []).append(Binding(path_value, cwd, "--material"))
    return bindings


def normalize_map_bindings(
    materials_map: OrderedDict[str, Any], map_path: Path
) -> OrderedDict[str, list[Binding]]:
    bindings: OrderedDict[str, list[Binding]] = OrderedDict()
    base_dir = map_path.parent
    for material_id, value in materials_map.items():
        if isinstance(value, list):
            values = value if value else [""]
        else:
            values = [value]
        bindings[material_id] = [Binding(item, base_dir, str(map_path)) for item in values]
    return bindings


def merge_bindings(
    map_bindings: OrderedDict[str, list[Binding]],
    cli_bindings: OrderedDict[str, list[Binding]],
) -> OrderedDict[str, list[Binding]]:
    merged: OrderedDict[str, list[Binding]] = OrderedDict()
    for material_id, bindings in map_bindings.items():
        merged[material_id] = list(bindings)
    for material_id, bindings in cli_bindings.items():
        merged.setdefault(material_id, []).extend(bindings)
    return merged


def is_url(value: str) -> bool:
    return bool(URL_RE.match(value.strip()))


def resolve_path(value: str, base_dir: Path) -> Path:
    expanded = os.path.expandvars(os.path.expanduser(value))
    path = Path(expanded)
    if not path.is_absolute():
        path = base_dir / path
    return path


def safe_material_segment(material_id: str) -> str:
    value = material_id.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = value.strip(".-_")
    return value or "material"


def archive_path_for(material_id: str, relative_path: Path, used: set[str]) -> str:
    parts = [part for part in relative_path.parts if part not in {"", "."}]
    rel = "/".join(parts) if parts else relative_path.name
    rel = rel.replace("\\", "/")
    base = f"materials/{safe_material_segment(material_id)}/{rel}"
    candidate = base
    counter = 2
    while candidate in used:
        path = Path(base)
        suffix = path.suffix
        stem = str(path.with_suffix("")) if suffix else base
        candidate = f"{stem}_{counter}{suffix}"
        candidate = candidate.replace("\\", "/")
        counter += 1
    used.add(candidate)
    return candidate


def iter_packable_files(directory: Path) -> list[tuple[Path, Path]]:
    results: list[tuple[Path, Path]] = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [item for item in dirs if item not in SKIP_DIRS]
        root_path = Path(root)
        for filename in files:
            file_path = root_path / filename
            if file_path.suffix.lower() in SKIP_SUFFIXES:
                continue
            rel_path = file_path.relative_to(directory)
            results.append((file_path, rel_path))
    return results


def process_materials(
    material_ids: list[str], bindings: OrderedDict[str, list[Binding]]
) -> tuple[list[MaterialStatus], list[IncludedFile]]:
    statuses: list[MaterialStatus] = []
    included_files: list[IncludedFile] = []
    used_archive_paths: set[str] = set()

    for material_id in material_ids:
        status = MaterialStatus(material_id)
        material_bindings = bindings.get(material_id, [])
        if not material_bindings:
            status.missing.append("no binding found")
            statuses.append(status)
            continue

        for binding in material_bindings:
            value = binding.value
            if not isinstance(value, str):
                status.missing.append(f"invalid non-string binding from {binding.origin}")
                continue
            raw_value = value.strip()
            status.bindings.append(raw_value)
            if not raw_value:
                status.missing.append(f"empty binding from {binding.origin}")
                continue
            if is_url(raw_value):
                status.external.append(raw_value)
                continue

            resolved = resolve_path(raw_value, binding.base_dir)
            if not resolved.exists():
                status.missing.append(f"path not found: {resolved}")
                continue
            if resolved.is_file():
                archive_path = archive_path_for(material_id, Path(resolved.name), used_archive_paths)
                included = IncludedFile(material_id, resolved.resolve(), archive_path, resolved.stat().st_size)
                status.included.append(included)
                included_files.append(included)
                continue
            if resolved.is_dir():
                packable = iter_packable_files(resolved)
                if not packable:
                    status.skipped.append(f"directory contains no packable files: {resolved}")
                    continue
                for file_path, rel_path in packable:
                    archive_path = archive_path_for(material_id, rel_path, used_archive_paths)
                    included = IncludedFile(
                        material_id,
                        file_path.resolve(),
                        archive_path,
                        file_path.stat().st_size,
                    )
                    status.included.append(included)
                    included_files.append(included)
                continue

            status.skipped.append(f"path is neither file nor directory: {resolved}")

        if not status.has_packaged_file and not status.has_unresolved_binding:
            status.missing.append("no packable local file found")
        statuses.append(status)

    return statuses, included_files


def missing_material_count(statuses: list[MaterialStatus]) -> int:
    return sum(1 for status in statuses if not status.has_packaged_file)


def blocked(statuses: list[MaterialStatus], included_files: list[IncludedFile]) -> bool:
    if not statuses:
        return True
    if not included_files:
        return True
    return any(not status.has_packaged_file or status.has_unresolved_binding for status in statuses)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_map_template(
    map_path: Path,
    materials_map: OrderedDict[str, Any],
    material_ids: list[str],
) -> bool:
    changed = False
    template: OrderedDict[str, Any] = OrderedDict()
    for key, value in materials_map.items():
        template[key] = value
    for material_id in material_ids:
        if material_id not in template:
            template[material_id] = ""
            changed = True
    if not map_path.exists():
        changed = True
    if not changed:
        return False
    ensure_parent(map_path)
    content = json.dumps({"materials": template}, indent=2, ensure_ascii=False)
    map_path.write_text(content + "\n", encoding="utf-8")
    return True


def render_status_lines(status: MaterialStatus, include_local_paths: bool) -> list[str]:
    lines: list[str] = []
    for item in status.included:
        if include_local_paths:
            lines.append(
                f"| `{status.material_id}` | `{item.source_path}` | `{item.archive_path}` | {item.size} |"
            )
        else:
            lines.append(f"| `{status.material_id}` | `{item.archive_path}` | {item.size} |")
    return lines


def render_unresolved(statuses: list[MaterialStatus]) -> list[str]:
    lines: list[str] = []
    for status in statuses:
        reasons = []
        reasons.extend(status.missing)
        reasons.extend([f"external reference: {url}" for url in status.external])
        reasons.extend(status.skipped)
        if not status.has_packaged_file and not reasons:
            reasons.append("no packaged local file")
        for reason in reasons:
            lines.append(f"- `{status.material_id}`: {reason}")
    if not lines:
        lines.append("- none")
    return lines


def render_sidecar_manifest(
    compiled_prompt: Path,
    map_path: Path,
    zip_path: Path | None,
    statuses: list[MaterialStatus],
    included_files: list[IncludedFile],
    blocked_value: bool,
    map_template_written: bool,
) -> str:
    generated = datetime.now(timezone.utc).isoformat()
    external_count = sum(len(status.external) for status in statuses)
    lines = [
        "# CPP Materials Manifest",
        "",
        f"- Generated: `{generated}`",
        f"- Compiled prompt: `{compiled_prompt.resolve()}`",
        f"- Materials map: `{map_path.resolve()}`",
        f"- Map template written: `{'yes' if map_template_written else 'no'}`",
        f"- Zip file: `{zip_path.resolve() if zip_path else 'not generated'}`",
        f"- Logical materials: `{len(statuses)}`",
        f"- Included files: `{len(included_files)}`",
        f"- Missing materials: `{missing_material_count(statuses)}`",
        f"- External references: `{external_count}`",
        f"- Blocked: `{'yes' if blocked_value else 'no'}`",
        "",
        "## Included Files",
        "",
    ]
    if included_files:
        lines.append("| Logical material ID | Local source path | Archive path | Bytes |")
        lines.append("| --- | --- | --- | --- |")
        for status in statuses:
            lines.extend(render_status_lines(status, include_local_paths=True))
    else:
        lines.append("none")

    lines.extend(["", "## Missing Or Unresolved", ""])
    lines.extend(render_unresolved(statuses))
    lines.append("")
    return "\n".join(lines)


def render_internal_manifest(
    compiled_prompt: Path,
    statuses: list[MaterialStatus],
    included_files: list[IncludedFile],
    blocked_value: bool,
) -> str:
    generated = datetime.now(timezone.utc).isoformat()
    lines = [
        "# CPP Materials Package Manifest",
        "",
        f"- Generated: `{generated}`",
        f"- Compiled prompt file: `{compiled_prompt.name}`",
        f"- Logical materials: `{len(statuses)}`",
        f"- Included files: `{len(included_files)}`",
        f"- Missing materials: `{missing_material_count(statuses)}`",
        f"- Blocked: `{'yes' if blocked_value else 'no'}`",
        "",
        "## Included Files",
        "",
    ]
    if included_files:
        lines.append("| Logical material ID | Archive path | Bytes |")
        lines.append("| --- | --- | --- |")
        for status in statuses:
            lines.extend(render_status_lines(status, include_local_paths=False))
    else:
        lines.append("none")

    lines.extend(["", "## Missing Or Unresolved", ""])
    lines.extend(render_unresolved(statuses))
    lines.append("")
    return "\n".join(lines)


def write_zip(zip_path: Path, included_files: list[IncludedFile], internal_manifest: str) -> None:
    ensure_parent(zip_path)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for item in included_files:
            archive.write(item.source_path, item.archive_path)
        archive.writestr("MANIFEST.md", internal_manifest)


def build_material_id_list(
    extracted_ids: list[str],
    materials_map: OrderedDict[str, Any],
    cli_bindings: OrderedDict[str, list[Binding]],
) -> list[str]:
    ids: OrderedDict[str, None] = OrderedDict()
    for material_id in extracted_ids:
        add_ordered(ids, material_id)
    for material_id in cli_bindings:
        add_ordered(ids, material_id)
    if not ids:
        for material_id in materials_map:
            add_ordered(ids, material_id)
    return list(ids.keys())


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    compiled_prompt = args.compiled_prompt.resolve()
    if not compiled_prompt.exists():
        print(f"ERROR: compiled prompt not found: {compiled_prompt}", file=sys.stderr)
        return 2
    if not compiled_prompt.is_file():
        print(f"ERROR: compiled prompt is not a file: {compiled_prompt}", file=sys.stderr)
        return 2

    default_map, default_zip, default_manifest = default_paths(compiled_prompt)
    map_path = (args.map_path or default_map).resolve()
    output_path = (args.output or default_zip).resolve()
    manifest_path = (args.manifest or default_manifest).resolve()

    try:
        materials_map, map_exists = load_materials_map(map_path)
        cli_bindings = parse_cli_materials(args.material, Path.cwd())
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    text = read_text(compiled_prompt)
    extracted_ids = extract_material_ids(text)
    material_ids = build_material_id_list(extracted_ids, materials_map, cli_bindings)

    map_bindings = normalize_map_bindings(materials_map, map_path)
    bindings = merge_bindings(map_bindings, cli_bindings)
    statuses, included_files = process_materials(material_ids, bindings)
    is_blocked = blocked(statuses, included_files)

    map_needs_template = (not map_exists) or any(material_id not in materials_map for material_id in material_ids)
    map_template_written = False
    if map_needs_template:
        map_template_written = write_map_template(map_path, materials_map, material_ids)

    internal_manifest = render_internal_manifest(compiled_prompt, statuses, included_files, is_blocked)
    zip_written = False
    if included_files:
        write_zip(output_path, included_files, internal_manifest)
        zip_written = True

    sidecar_manifest = render_sidecar_manifest(
        compiled_prompt,
        map_path,
        output_path if zip_written else None,
        statuses,
        included_files,
        is_blocked,
        map_template_written,
    )
    ensure_parent(manifest_path)
    manifest_path.write_text(sidecar_manifest, encoding="utf-8")

    print(f"ZIP: {output_path if zip_written else 'not generated'}")
    print(f"MANIFEST: {manifest_path}")
    print(f"MAP_TEMPLATE_WRITTEN: {'yes' if map_template_written else 'no'}")
    print(f"LOGICAL_MATERIALS: {len(statuses)}")
    print(f"INCLUDED_FILES: {len(included_files)}")
    print(f"MISSING_MATERIALS: {missing_material_count(statuses)}")
    print(f"BLOCKED: {'yes' if is_blocked else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
