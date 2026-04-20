# CLAUDE.md — json-razor

## Public Name & Tagline

**JSON's Razor** — Cut the fat.

The name is a deliberate play on Occam's Razor — the principle of parsimony. JSON is also a homophone for the name Jason, which was the original intent of the JSON creators (Douglas Crockford et al.) when they named the format. Most people missed the joke and pronounce it "Jay-SAWN." JSON's Razor quietly restores that intent.

**One-line description:** Reduces JSON, YAML, and NDJSON volume by collapsing repeated structures while preserving the schema, making the schema easier for you to read.

---

## What It Does

Large structured data files are hard for humans to parse — not because the structure is complex, but because repetition obscures it. A list of 10,000 objects with identical shape tells you nothing more than a list of 1. JSON's Razor collapses that repetition to its minimum essential form: one representative example of each repeated structure, at every level of nesting.

The output is valid, schema-preserving data — not a summary, not a schema definition. Downstream pipeline tools can still parse it. It just has far less volume.

**Core principle:** Keep what is essential. Remove what is repeated. Preserve the shape.

---

## Supported Formats

- **JSON** — primary format, auto-detected from `.json` extension or explicit `--format json`
- **YAML** — auto-detected from `.yaml`/`.yml` extension or explicit `--format yaml`
- **NDJSON** — Newline Delimited JSON. Each line is a complete JSON object. Common in structured logs (Docker, Kubernetes, CloudWatch). Collapse across lines — keep one representative line. Auto-detected from `.ndjson` extension or explicit `--format ndjson`

XML excluded — too much complexity for too little DevEx relevance.

---

## Core Mechanic

Recursively collapse repeated structures:

- **Arrays** — keep one item, drop the rest. If mixed types, keep one of each distinct type.
- **Objects of repeated shape** — keep one key-value pair, drop the rest.
- **Single-item arrays** — pass through unchanged.
- **Null / empty values** — preserve as-is (`null`, `[]`, `{}`). They carry structural information and must remain valid for pipeline use.
- **Long strings** — truncate to a preview (configurable length).

---

## Edge Cases

- Mixed-type arrays: `[1, "string", {"id": 1}, null]` → keep one of each distinct type
- Circular references: depth limit prevents infinite recursion
- Single-item arrays: nothing to collapse, pass through
- NDJSON: collapse across lines, not within a single object

---

## Configuration

```
--keep N        # number of examples to keep per repeated structure (default: 1)
--depth N       # stop collapsing below this nesting depth
--format        # explicit format override: json | yaml | ndjson
--truncate N    # max string length before truncating (default: 100)
```

---

## Input / Output

```bash
cat big.json | json-razor                    # stdin → stdout
json-razor big.json                          # file input → stdout
json-razor big.json -o small.json            # file input → file output
json-razor big.yaml --format yaml            # explicit format
json-razor app.log --format ndjson           # NDJSON log file
```

Fully pipeable. Output is always valid, parseable data in the same format as input.

---

## Delivery

- **PyPI:** `json-razor` package, `json-razor` command
- **Standalone executable:** PyInstaller, cross-platform (Win/Mac/Linux)

---

## Current State

- Package is live on PyPI: `pip install json-razor` works
- GitHub repo: `git@github.com:rick-does/json-razor.git` (branch: `main`)
- Current version: `0.1.2` (in `pyproject.toml`)
- Trusted publishing configured on PyPI — no API tokens needed for future releases

---

## Project Structure

```
json_razor/
  __init__.py       # exposes collapse()
  core.py           # recursive collapse logic, _type_key()
  formats.py        # load/dump for json, yaml, ndjson
  cli.py            # argparse CLI entry point
tests/
  test_core.py      # 14 unit tests
  samples/          # sample input files for manual testing
    simple.json
    nested.json
    mixed.json
    events.json
    services.yaml
    app.ndjson
.github/workflows/
  tests.yml         # runs pytest on push/PR to main
  release.yml       # publishes to PyPI + builds executables on version tag
pyproject.toml      # package config, entry point, dependencies
```

---

## Releasing

1. Bump `version` in `pyproject.toml`
2. Commit and push
3. Tag and push:

```bash
git tag v0.x.x
git push origin v0.x.x
```

This triggers `release.yml` which:
- Publishes the new version to PyPI via trusted publishing (OIDC, no secrets needed)
- Builds standalone executables for Linux, macOS, and Windows via PyInstaller
- Attaches all three binaries to the GitHub release

**Do not** run `twine upload` manually again — that was only needed for the initial name claim.

---

## Library Stack

| Format | Library |
|--------|---------|
| JSON | `json` (stdlib) |
| YAML | `PyYAML` |
| NDJSON | line-by-line `json` (stdlib) |

---

## Related

- **[json-razor-action](https://github.com/rick-does/json-razor-action)** — GitHub Action wrapper. Published on the Actions Marketplace. Use as `rick-does/json-razor-action@v1`.

---

## Rules

- Never add comments or docstrings to code that wasn't changed
- Never add features beyond what was asked
- Don't create new files to document changes — edit existing files or nothing
