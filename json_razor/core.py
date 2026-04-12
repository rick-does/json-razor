def collapse(data, keep=1, depth=None, truncate=100, _depth=0):
    if depth is not None and _depth >= depth:
        return data

    if isinstance(data, str):
        if truncate is not None and len(data) > truncate:
            return data[:truncate] + "..."
        return data

    if isinstance(data, bool) or data is None or isinstance(data, (int, float)):
        return data

    if isinstance(data, list):
        if len(data) == 0:
            return []

        buckets = {}
        for item in data:
            key = _type_key(item)
            if key not in buckets:
                buckets[key] = []
            buckets[key].append(item)

        result = []
        for items in buckets.values():
            for item in items[:keep]:
                result.append(collapse(item, keep, depth, truncate, _depth + 1))
        return result

    if isinstance(data, dict):
        if len(data) == 0:
            return {}
        return {k: collapse(v, keep, depth, truncate, _depth + 1) for k, v in data.items()}

    return data


def _type_key(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    return type(value).__name__
