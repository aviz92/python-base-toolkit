import re

import pytest

from python_base_toolkit.utils.generate_id import (
    generate_id,
    generate_id_by_date,
    generate_id_by_date_and_time,
    generate_id_by_time,
)


class TestGenerateId:
    def test_default_length_is_eight_uppercase(self) -> None:
        id_ = generate_id()
        assert re.fullmatch(r"[A-Z]{8}", id_), f"Got {id_!r}"

    @pytest.mark.parametrize("length", [0, 1, 32])
    def test_custom_length(self, length: int) -> None:
        assert len(generate_id(length)) == length, f"Expected length {length}"


class TestGenerateIdByTimestamp:
    @pytest.mark.parametrize(
        ("func", "length"),
        [(generate_id_by_date, 8), (generate_id_by_time, 12), (generate_id_by_date_and_time, 20)],
    )
    def test_returns_digits_of_expected_length(self, func: object, length: int) -> None:
        id_ = func()  # type: ignore[operator]
        assert id_.isdigit() and len(id_) == length, f"{func.__name__} -> {id_!r}"  # type: ignore[attr-defined]
