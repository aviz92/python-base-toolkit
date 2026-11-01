import json

import pytest

from python_base_toolkit.base_structures.base_enum import BaseEnum, BaseStrEnum


class Color(BaseEnum):
    RED = "red"
    GREEN = "green"


class Size(BaseStrEnum):
    SMALL = "small"
    LARGE = "large"


class TestEnumMixin:
    def test_str_returns_value(self) -> None:
        assert str(Color.RED) == "red", f"Got {str(Color.RED)!r}"

    def test_repr_returns_value(self) -> None:
        assert repr(Color.GREEN) == "green", f"Got {repr(Color.GREEN)!r}"

    def test_to_list_returns_values(self) -> None:
        assert Color.to_list() == ["red", "green"], f"Got {Color.to_list()}"

    def test_values_matches_to_list(self) -> None:
        assert Color.values() == Color.to_list(), f"Got {Color.values()}"

    def test_names_returns_member_names(self) -> None:
        assert Color.names() == ["RED", "GREEN"], f"Got {Color.names()}"

    def test_to_dict_maps_names_to_values(self) -> None:
        assert Color.to_dict() == {"RED": "red", "GREEN": "green"}, f"Got {Color.to_dict()}"

    def test_to_json_is_valid_json_of_dict(self) -> None:
        assert json.loads(Color.to_json()) == Color.to_dict(), f"Got {Color.to_json()}"

    @pytest.mark.parametrize(("name", "expected"), [("RED", True), ("BLUE", False), ("red", False)])
    def test_has_name_returns_expected(self, name: str, expected: bool) -> None:
        assert Color.has_name(name) is expected, f"has_name({name!r}) should be {expected}"

    @pytest.mark.parametrize(("value", "expected"), [("red", True), ("blue", False), ("RED", False)])
    def test_has_value_returns_expected(self, value: str, expected: bool) -> None:
        assert Color.has_value(value) is expected, f"has_value({value!r}) should be {expected}"

    def test_from_value_substring_returns_matching_members(self) -> None:
        result = Color.from_value("re")
        assert result == [Color.RED, Color.GREEN], f"Got {result}"

    def test_from_value_no_match_returns_empty(self) -> None:
        assert not Color.from_value("blue"), "Expected no matches"


class TestBaseStrEnum:
    def test_member_equals_plain_string(self) -> None:
        assert Size.SMALL == "small", "StrEnum member should compare equal to its value"

    def test_json_dumps_member_directly(self) -> None:
        assert json.dumps(Size.LARGE) == '"large"', f"Got {json.dumps(Size.LARGE)}"
