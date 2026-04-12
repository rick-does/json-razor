import pytest
from json_razor.core import collapse


def test_array_collapse():
    data = [{"id": 1}, {"id": 2}, {"id": 3}]
    assert collapse(data) == [{"id": 1}]


def test_array_keep_n():
    data = [{"id": 1}, {"id": 2}, {"id": 3}]
    assert collapse(data, keep=2) == [{"id": 1}, {"id": 2}]


def test_mixed_type_array():
    data = [1, "hello", {"id": 1}, None]
    result = collapse(data)
    types = {type(x) for x in result}
    assert types == {int, str, dict, type(None)}
    assert len(result) == 4


def test_single_item_array_unchanged():
    data = [{"id": 1}]
    assert collapse(data) == [{"id": 1}]


def test_empty_array_preserved():
    assert collapse([]) == []


def test_empty_object_preserved():
    assert collapse({}) == {}


def test_null_preserved():
    assert collapse(None) is None


def test_nested_array_collapse():
    data = {"items": [{"a": 1}, {"a": 2}, {"a": 3}]}
    assert collapse(data) == {"items": [{"a": 1}]}


def test_string_truncation():
    long = "x" * 200
    result = collapse(long, truncate=100)
    assert result == "x" * 100 + "..."


def test_string_no_truncation_when_short():
    s = "hello"
    assert collapse(s, truncate=100) == "hello"


def test_depth_limit():
    data = {"a": [1, 2, 3]}
    result = collapse(data, depth=1)
    assert result == {"a": [1, 2, 3]}


def test_bool_not_confused_with_int():
    data = [True, False, 1, 0]
    result = collapse(data)
    types = {type(x) for x in result}
    assert bool in types
    assert int in types


def test_object_keys_preserved():
    data = {"name": "foo", "age": 30, "items": [1, 2, 3]}
    result = collapse(data)
    assert "name" in result
    assert "age" in result
    assert result["items"] == [1]


def test_ndjson_style():
    records = [{"id": i, "val": i * 2} for i in range(100)]
    result = collapse(records)
    assert len(result) == 1
    assert result[0] == {"id": 0, "val": 0}
