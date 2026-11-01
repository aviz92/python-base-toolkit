from dataclasses import dataclass
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from pathlib import Path

import pandas as pd
import pytest
from pydantic import BaseModel

from python_base_toolkit.utils.data_serialization import default_serialize, to_json_serializable


class _Color(Enum):
    RED = "red"


class _Model(BaseModel):
    x: int


@dataclass
class _Point:
    x: int
    y: int


class TestDefaultSerialize:
    @pytest.mark.parametrize(
        ("obj", "expected"),
        [
            (_Model(x=1), {"x": 1}),
            (int, "int"),
            (_Color.RED, "red"),
            ({1}, [1]),
            ((1, 2), [1, 2]),
            (datetime(2026, 1, 2, 3, 4, 5), "2026-01-02T03:04:05"),
            (date(2026, 1, 2), "2026-01-02"),
            (time(3, 4, 5), "03:04:05"),
            (Decimal("1.5"), 1.5),
            (Path("/a/b"), "/a/b"),
            (_Point(1, 2), {"x": 1, "y": 2}),
            (pd.NA, None),
        ],
    )
    def test_supported_type_returns_serialized(self, obj: object, expected: object) -> None:
        result = default_serialize(obj)
        assert result == expected, f"default_serialize({obj!r}) -> {result!r}, expected {expected!r}"

    def test_dataclass_type_is_serialized_as_name(self) -> None:
        assert default_serialize(_Point) == "_Point", "Dataclass *type* should serialize to its name"

    def test_unsupported_type_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="not serializable"):
            default_serialize(object())


class TestToJsonSerializable:
    def test_nested_structure_is_converted(self) -> None:
        data = {"when": date(2026, 1, 2), "tags": {"a"}, "model": _Model(x=3), "n": 1}
        result = to_json_serializable(data)
        assert result == {"when": "2026-01-02", "tags": ["a"], "model": {"x": 3}, "n": 1}, f"Got {result}"

    def test_unsupported_value_raises_type_error(self) -> None:
        with pytest.raises(TypeError):
            to_json_serializable({"bad": object()})
