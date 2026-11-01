from collections.abc import Iterator
from itertools import count
from unittest.mock import MagicMock, patch

import pytest

from python_base_toolkit.utils.execute import timed_execution_bool, timed_execution_result


@pytest.fixture(autouse=True)
def fake_clock() -> Iterator[None]:
    """Make time() tick 1s per call and sleep() a no-op so timeouts are instant."""
    clock = count()
    with (
        patch("python_base_toolkit.utils.execute.time", side_effect=lambda: next(clock)),
        patch("python_base_toolkit.utils.execute.sleep"),
    ):
        yield


class TestTimedExecutionBool:
    def test_condition_met_returns_true(self) -> None:
        assert timed_execution_bool(lambda: True, timeout=5) is True, "Should succeed immediately"

    def test_condition_never_met_returns_false(self) -> None:
        assert timed_execution_bool(lambda: False, timeout=3) is False, "Should time out"

    def test_expect_false_with_falsy_result_returns_true(self) -> None:
        assert timed_execution_bool(lambda: 0, timeout=5, expect_true=False) is True, "Falsy result expected"

    def test_retries_until_condition_met(self) -> None:
        func = MagicMock(side_effect=[False, False, True])
        assert timed_execution_bool(func, timeout=10) is True, "Should succeed on 3rd attempt"
        assert func.call_count == 3, f"Expected 3 calls, got {func.call_count}"


class TestTimedExecutionResult:
    def test_condition_met_returns_result(self) -> None:
        assert timed_execution_result(lambda: "ok", timeout=5) == "ok", "Should return func result"

    def test_condition_never_met_returns_none(self) -> None:
        assert timed_execution_result(lambda: None, timeout=3) is None, "Should return None on timeout"
