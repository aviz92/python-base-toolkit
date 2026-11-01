from pathlib import Path

import pytest

from python_base_toolkit.utils.path_utils import get_project_path_by_file, get_project_path_by_name


class TestGetProjectPathByName:
    def test_finds_package_directory(self) -> None:
        result = get_project_path_by_name("python_base_toolkit")
        assert Path(result).name == "python_base_toolkit", f"Got {result}"

    def test_unknown_project_raises(self) -> None:
        with pytest.raises(FileNotFoundError, match="not found"):
            get_project_path_by_name("definitely-not-a-real-project-xyz")


class TestGetProjectPathByFile:
    def test_default_markers_find_ancestor(self) -> None:
        result = get_project_path_by_file()
        assert (result / "pyproject.toml").exists() or (result / ".git").exists(), f"Got {result}"

    def test_missing_markers_raises(self) -> None:
        with pytest.raises(FileNotFoundError, match="markers"):
            get_project_path_by_file({"no-such-marker-file-xyz"})
