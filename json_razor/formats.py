import json

import yaml


def load(text, fmt):
    if fmt == "json":
        return json.loads(text)
    if fmt == "yaml":
        return yaml.safe_load(text)
    raise ValueError(f"Unknown format: {fmt}")


def dump(data, fmt):
    if fmt == "json":
        return json.dumps(data, indent=2)
    if fmt == "yaml":
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
    raise ValueError(f"Unknown format: {fmt}")


def load_ndjson(text):
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def dump_ndjson(records):
    return "\n".join(json.dumps(r) for r in records)
