import sys
from unittest.mock import patch

from python_base_toolkit.utils.venv_details import get_venv_details


class TestGetVenvDetails:
    def test_reports_interpreter_and_venv(self) -> None:
        with patch.dict("os.environ", {"VIRTUAL_ENV": "/tmp/venv"}):
            details = get_venv_details()
        assert details == {
            "python_executable_path": sys.executable,
            "python_version": sys.version,
            "venv_path": "/tmp/venv",
        }, f"Got {details}"

    def test_venv_path_none_when_not_set(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            assert get_venv_details()["venv_path"] is None, "No VIRTUAL_ENV -> None"
