from pathlib import Path
from unittest.mock import patch

from python_base_toolkit.scripts.remove_build_files import clean_build_artifacts


class TestCleanBuildArtifacts:
    def test_removes_build_dist_and_egg_info_only(self, tmp_path: Path) -> None:
        for name in ("build", "dist", "pkg.egg-info", "src", ".git"):
            (tmp_path / name).mkdir()

        with patch("python_base_toolkit.scripts.remove_build_files.get_project_path_by_file", return_value=tmp_path):
            clean_build_artifacts()

        remaining = sorted(p.name for p in tmp_path.iterdir())
        assert remaining == [".git", "src"], f"Got {remaining}"
