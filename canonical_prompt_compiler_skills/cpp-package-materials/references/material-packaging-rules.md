# Material Packaging Rules

## Purpose

`cpp-package-materials` converts a compiled CPP prompt's requested runtime materials into a local zip attachment and manifest. It treats material names in the compiled prompt as logical material IDs and binds them to real paths only through a materials map or explicit command-line binding.

## Candidate Material IDs

Extract logical material IDs from the compiled prompt conservatively:

- Prefer entries inside `<REFERENCE_MATERIALS>`, `<TRUSTED_CONTEXT>`, and `<UNTRUSTED_INPUT>` payload blocks.
- Also inspect labeled material/input sections such as `RUNTIME_PAYLOAD:`, `REQUIRED_INPUTS:`, `AVAILABLE_INPUTS:`, `REFERENCE_MATERIALS:`, and `Minimum additional materials needed:`.
- Normalize list markers, table rows, Markdown links, backticks, and surrounding punctuation.
- Skip placeholders, ellipses, `none`, `n/a`, raw XML-like tag lines, and code fence markers.
- Preserve the extracted display text as the logical material ID. Do not reinterpret it as a path.

If extraction misses an ID, pass an explicit `--material "logical id=path"` binding. If no IDs are extracted but a map exists, map keys may be treated as the candidate set.

## Materials Map

Default map path:

```text
<compiled-stem>.materials-map.json
```

Map shape:

```json
{
  "materials": {
    "runtime load section": "C:/path/to/runtime-load-section.md",
    "experiment table": [
      "C:/path/to/results.csv",
      "C:/path/to/metadata.xlsx"
    ]
  }
}
```

Rules:

- `materials` must be a JSON object.
- Each key is a logical material ID.
- Each value may be a string path, a directory path, or an array of string paths.
- Empty strings, empty arrays, nulls, and non-string values are unresolved and must be recorded.
- Relative paths in the JSON map resolve relative to the map file directory.
- Relative paths supplied through `--material` resolve relative to the current working directory.
- `--material` bindings supplement map bindings for the same logical ID.
- URL-like values are external references. Record them; do not download them.

When the map is absent or lacks extracted IDs, write or update a map template with empty entries for missing IDs.

## Packaged Files

Package only existing local files from resolved bindings.

Directory bindings:

- Recurse through child files.
- Preserve paths relative to the bound directory.
- Skip directories named `.git`, `.trash`, and `__pycache__`.
- Skip files ending in `.pyc` or `.pyo`.
- Record an empty or fully skipped directory as unresolved.

Zip layout:

```text
materials/<safe-logical-id>/<relative-file-path>
MANIFEST.md
```

Archive path rules:

- Derive `<safe-logical-id>` from the logical material ID using lowercase ASCII letters, digits, dots, underscores, and hyphens.
- Replace other characters with `-`.
- Add numeric suffixes when two files would produce the same archive path.
- Do not include local absolute paths in archive names or the zip-internal `MANIFEST.md`.
- Do not include the compiled prompt in the zip unless a future user explicitly requests that behavior.

## Manifest

Always write a sidecar manifest beside the compiled prompt unless `--manifest` provides another path. The sidecar manifest may include local paths because it is for local audit and debugging.

The zip-internal `MANIFEST.md` must include:

- compiled prompt filename, not absolute path;
- generation timestamp;
- logical material IDs;
- archive paths and byte counts;
- unresolved IDs and reasons;
- external references without download claims.

The sidecar manifest must additionally include:

- compiled prompt path;
- materials map path;
- zip path or `not generated`;
- included-file count;
- missing-material count;
- external-reference count;
- blocked status.

## Blocking Rules

Packaging is blocked when:

- no logical material IDs were found and no map supplied fallback IDs;
- a logical material ID has no packaged local file;
- a binding is empty, invalid, missing on disk, a URL, or a directory with no packable files;
- no local files can be packaged.

A blocked run can still write a manifest and map template. Do not generate an empty zip.
