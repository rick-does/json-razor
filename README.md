# JSON's Razor — Cut the fat

[![tests](https://github.com/rick-does/json-razor/actions/workflows/tests.yml/badge.svg)](https://github.com/rick-does/json-razor/actions/workflows/tests.yml)

Reduces JSON, YAML, and NDJSON volume by collapsing repeated structures while preserving the schema, making the schema easier for you to see.

Large structured data files are hard to parse — not because the structure is complex, but because repetition obscures it. A list of 10,000 objects with identical shape tells you nothing more than a list of 1. JSON's Razor collapses that repetition to its minimum essential form: one representative example of each repeated structure, at every level of nesting.

The output is valid, parseable data in the same format as input — not a summary, not a schema definition. It just has far less volume.

---

## Install

```bash
pip install json-razor
```

---

## Usage

```bash
cat big.json | json-razor                    # stdin → stdout
json-razor big.json                          # file input → stdout
json-razor big.json -o small.json            # file input → file output
json-razor big.yaml                          # auto-detected as YAML
json-razor app.log --format ndjson           # NDJSON log file
```

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--keep N` | 1 | Number of examples to keep per repeated structure |
| `--depth N` | unlimited | Stop collapsing below this nesting depth |
| `--format` | auto | Force format: `json`, `yaml`, or `ndjson` |
| `--truncate N` | 100 | Max string length before truncating |

---

## How it works

**Arrays** — collapsed to one item. Mixed-type arrays keep one of each distinct type.

```json
// input
[{"id": 1, "name": "alice"}, {"id": 2, "name": "bob"}, {"id": 3, "name": "carol"}]

// output
[{"id": 1, "name": "alice"}]
```

**Mixed types** — one representative per JSON type (null, bool, number, string, array, object).

```json
// input
[1, "hello", {"id": 1}, null, true, [1, 2, 3]]

// output
[1, "hello", {"id": 1}, null, true, [1]]
```

**Nested structures** — collapsed recursively at every level.

**NDJSON** — collapsed across lines; one representative line kept.

**Nulls and empty values** — always preserved (`null`, `[]`, `{}`).

**Long strings** — truncated to a configurable preview.

---

## Supported formats

| Format | Auto-detected from |
|--------|--------------------|
| JSON | `.json` |
| YAML | `.yaml`, `.yml` |
| NDJSON | `.ndjson` |
