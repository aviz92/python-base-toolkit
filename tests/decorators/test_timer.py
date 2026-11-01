from python_base_toolkit.decorators.timer import Timer, timer


class TestTimer:
    def test_context_manager_sets_elapsed_time(self) -> None:
        with Timer("block") as t:
            pass
        assert t.elapsed_time is not None and t.elapsed_time >= 0, f"Got {t.elapsed_time}"

    def test_context_manager_end_after_start(self) -> None:
        with Timer() as t:
            pass
        assert t.end_time >= t.start_time, "end_time must not precede start_time"


class TestTimerDecorator:
    def test_returns_wrapped_function_result(self) -> None:
        @timer
        def add(a: int, b: int) -> int:
            return a + b

        assert add(2, 3) == 5, "Decorated function result must be returned"

    def test_preserves_function_name(self) -> None:
        @timer
        def my_func() -> None:
            return None

        assert my_func.__name__ == "my_func", f"Got {my_func.__name__}"
