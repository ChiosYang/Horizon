import pytest

from src.configuration.patch import (
    ConfigPatchError,
    apply_json_patch,
    parse_json_pointer,
)


def test_patch_add_replace_remove_does_not_mutate_input():
    original = {
        "sources": ["rss", "github"],
        "filtering": {"threshold": 6.0, "legacy": True},
    }

    result = apply_json_patch(
        original,
        [
            {"op": "add", "path": "/sources/-", "value": "reddit"},
            {"op": "replace", "path": "/filtering/threshold", "value": 7.5},
            {"op": "remove", "path": "/filtering/legacy"},
        ],
    )

    assert result == {
        "sources": ["rss", "github", "reddit"],
        "filtering": {"threshold": 7.5},
    }
    assert original["sources"] == ["rss", "github"]
    assert original["filtering"]["threshold"] == 6.0


def test_patch_move_reorders_array_using_post_remove_index():
    result = apply_json_patch(
        {"sources": ["a", "b", "c"]},
        [{"op": "move", "from": "/sources/0", "path": "/sources/2"}],
    )

    assert result["sources"] == ["b", "c", "a"]


def test_patch_supports_escaped_object_keys():
    result = apply_json_patch(
        {"a/b": {"x~y": 1}},
        [{"op": "replace", "path": "/a~1b/x~0y", "value": 2}],
    )

    assert result == {"a/b": {"x~y": 2}}
    assert parse_json_pointer("/a~1b/x~0y") == ["a/b", "x~y"]


def test_patch_can_replace_document_root():
    result = apply_json_patch(
        {"old": True},
        [{"op": "replace", "path": "", "value": {"new": True}}],
    )

    assert result == {"new": True}


@pytest.mark.parametrize(
    ("operation", "code"),
    [
        ({"op": "replace", "path": "/missing", "value": 1}, "path_not_found"),
        (
            {"op": "add", "path": "/items/2", "value": 1},
            "array_index_out_of_range",
        ),
        ({"op": "replace", "path": "/items/0"}, "missing_value"),
        ({"op": "copy", "path": "/x", "from": "/y"}, "unsupported_operation"),
        ({"op": "remove", "path": "bad"}, "invalid_pointer"),
    ],
)
def test_invalid_patch_operations_return_stable_safe_codes(operation, code):
    with pytest.raises(ConfigPatchError) as exc_info:
        apply_json_patch({"items": []}, [operation])

    assert exc_info.value.code == code


def test_patch_rejects_moving_value_into_its_descendant():
    with pytest.raises(ConfigPatchError) as exc_info:
        apply_json_patch(
            {"parent": {"child": {}}},
            [{"op": "move", "from": "/parent", "path": "/parent/child/new"}],
        )

    assert exc_info.value.code == "move_into_child"
