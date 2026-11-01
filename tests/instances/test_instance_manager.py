from unittest.mock import MagicMock

from python_base_toolkit.instances.instance_manager import InstanceManager


class _ContextOnly:
    """Object with __exit__ but no close()."""

    def __init__(self) -> None:
        self.exited = False

    def __enter__(self) -> "_ContextOnly":
        return self

    def __exit__(self, *args: object) -> None:
        self.exited = True


class TestInstanceManager:
    def test_close_all_calls_close(self) -> None:
        manager = InstanceManager()
        resource = MagicMock()
        manager.add(resource)
        manager.close_all()
        resource.close.assert_called_once_with()

    def test_close_all_falls_back_to_exit(self) -> None:
        manager = InstanceManager()
        resource = _ContextOnly()
        manager.add(resource)
        manager.close_all()
        assert resource.exited, "__exit__ should be called when close() is missing"

    def test_close_all_closes_in_reverse_order(self) -> None:
        manager = InstanceManager()
        order: list[str] = []
        first, second = MagicMock(), MagicMock()
        first.close.side_effect = lambda: order.append("first")
        second.close.side_effect = lambda: order.append("second")
        manager.add(first)
        manager.add(second)
        manager.close_all()
        assert order == ["second", "first"], f"Got {order}"

    def test_close_all_failure_does_not_stop_others(self) -> None:
        manager = InstanceManager()
        ok, broken = MagicMock(), MagicMock()
        broken.close.side_effect = RuntimeError("boom")
        manager.add(ok)
        manager.add(broken)
        manager.close_all()
        ok.close.assert_called_once_with()

    def test_context_manager_closes_on_exit(self) -> None:
        resource = MagicMock()
        with InstanceManager() as manager:
            manager.add(resource)
        resource.close.assert_called_once_with()
