from pathlib import Path

from python_base_toolkit.utils.pycache import delete_pycache_folder


class TestDeletePycacheFolder:
    def test_removes_pycache_except_ignored(self, tmp_path: Path) -> None:
        (tmp_path / "pkg" / "__pycache__").mkdir(parents=True)
        (tmp_path / ".venv" / "lib" / "__pycache__").mkdir(parents=True)

        delete_pycache_folder(tmp_path)

        assert not (tmp_path / "pkg" / "__pycache__").exists(), "Project __pycache__ should be removed"
        assert (tmp_path / ".venv" / "lib" / "__pycache__").exists(), ".venv is ignored by default"

    def test_custom_ignored_dirs(self, tmp_path: Path) -> None:
        (tmp_path / "keep" / "__pycache__").mkdir(parents=True)

        delete_pycache_folder(tmp_path, ignored_dirs={"keep"})

        assert (tmp_path / "keep" / "__pycache__").exists(), "Custom ignored dir must be kept"
