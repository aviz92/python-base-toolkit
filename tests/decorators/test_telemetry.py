from unittest.mock import ANY, patch

from python_base_toolkit.decorators.telemetry import report_func_telemetry


class TestReportFuncTelemetry:
    def test_no_args_returns_result(self) -> None:
        @report_func_telemetry
        def answer() -> int:
            return 42

        assert answer() == 42, "Decorated function result must be returned"

    def test_kwargs_only_returns_result(self) -> None:
        @report_func_telemetry
        def greet(name: str = "x") -> str:
            return f"hi {name}"

        assert greet(name="avi") == "hi avi", "Keyword args must be forwarded"

    def test_preserves_function_name(self) -> None:
        @report_func_telemetry
        def my_func() -> None:
            return None

        assert my_func.__name__ == "my_func", f"Got {my_func.__name__}"

    def test_positional_args_returns_result(self) -> None:
        @report_func_telemetry
        def add(a: int, b: int) -> int:
            return a + b

        assert add(1, 2) == 3, "Positional args must be supported"

    def test_reports_function_and_call_arguments(self) -> None:
        def add(a: int, b: int, *, scale: int = 1) -> int:
            return (a + b) * scale

        with patch("python_base_toolkit.decorators.telemetry.report_telemetry", autospec=True) as report:
            assert report_func_telemetry(add)(1, 2, scale=3) == 9, "Result must be returned"
        report.assert_called_once_with(
            func=add, start_time=ANY, end_time=ANY, call_args=(1, 2), call_kwargs={"scale": 3}
        )

    def test_kwargs_named_like_report_params_do_not_collide(self) -> None:
        @report_func_telemetry
        def describe(func: str, start_time: int) -> str:
            return f"{func}@{start_time}"

        assert describe(func="x", start_time=1) == "x@1", "Caller kwargs must not clash with telemetry params"
