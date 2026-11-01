import hashlib
import zipfile
from pathlib import Path

import pytest

from python_base_toolkit.utils.file_utils import FileUtils


@pytest.fixture(name="text_file")
def fixture_text_file(tmp_path: Path) -> Path:
    path = tmp_path / "sample.txt"
    path.write_text("hello world", encoding="utf-8")
    return path


class TestFileCompression:
    def test_gzip_then_ungzip_roundtrip(self, text_file: Path) -> None:
        gz_path = FileUtils.file_compression.gzip_file(str(text_file))
        assert gz_path == f"{text_file}.gz", f"Got {gz_path}"
        text_file.unlink()

        out = FileUtils.file_compression.ungzip_file(gz_path)
        assert Path(out).read_text(encoding="utf-8") == "hello world", "Content must survive roundtrip"

    def test_ungzip_without_gz_suffix_appends_decompressed(self, text_file: Path, tmp_path: Path) -> None:
        gz_path = FileUtils.file_compression.gzip_file(str(text_file), str(tmp_path / "archive"))
        out = FileUtils.file_compression.ungzip_file(gz_path)
        assert out.endswith("archive_decompressed"), f"Got {out}"

    def test_gzip_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            FileUtils.file_compression.gzip_file(str(tmp_path / "missing.txt"))

    def test_ungzip_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            FileUtils.file_compression.ungzip_file(str(tmp_path / "missing.gz"))

    def test_ungzip_invalid_gzip_raises_os_error(self, text_file: Path) -> None:
        with pytest.raises(OSError, match="decompressing"):
            FileUtils.file_compression.ungzip_file(str(text_file))

    def test_compress_then_extract_directory(self, tmp_path: Path) -> None:
        src = tmp_path / "data"
        src.mkdir()
        (src / "a.txt").write_text("a", encoding="utf-8")

        tarball = FileUtils.file_compression.compress_directory(str(src))
        assert tarball == f"{src}.tar.gz", f"Got {tarball}"

        out_dir = FileUtils.file_compression.extract_archive(tarball, str(tmp_path / "out"))
        assert (Path(out_dir) / "data" / "a.txt").read_text(encoding="utf-8") == "a", "Extracted file missing"

    def test_extract_tar_gz_default_output_strips_double_extension(self, tmp_path: Path) -> None:
        src = tmp_path / "pkg"
        src.mkdir()
        (src / "f.txt").write_text("x", encoding="utf-8")
        tarball = FileUtils.file_compression.compress_directory(str(src), str(tmp_path / "bundle.tar.gz"))

        out_dir = FileUtils.file_compression.extract_archive(tarball)
        assert out_dir == str(tmp_path / "bundle"), f"Got {out_dir}"

    def test_extract_zip(self, tmp_path: Path) -> None:
        archive = tmp_path / "z.zip"
        with zipfile.ZipFile(archive, "w") as zf:
            zf.writestr("inner.txt", "zipped")

        out_dir = FileUtils.file_compression.extract_archive(str(archive))
        assert (Path(out_dir) / "inner.txt").read_text(encoding="utf-8") == "zipped", "Zip content missing"

    def test_compress_missing_directory_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            FileUtils.file_compression.compress_directory(str(tmp_path / "nope"))

    def test_extract_missing_archive_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            FileUtils.file_compression.extract_archive(str(tmp_path / "nope.zip"))

    def test_extract_unsupported_format_raises(self, text_file: Path) -> None:
        with pytest.raises(ValueError, match="Unsupported archive format"):
            FileUtils.file_compression.extract_archive(str(text_file))


class TestFileHash:
    @pytest.mark.parametrize(
        ("method", "algorithm"),
        [("file_md5", "md5"), ("file_sha1", "sha1"), ("file_sha256", "sha256")],
    )
    def test_hash_matches_hashlib(self, text_file: Path, method: str, algorithm: str) -> None:
        expected = hashlib.new(algorithm, b"hello world").hexdigest()
        result = getattr(FileUtils.file_hash, method)(str(text_file), chunk_size=4)
        assert result == expected, f"{method} -> {result}, expected {expected}"


class TestFileIO:
    def test_write_then_read_text(self, tmp_path: Path) -> None:
        path = str(tmp_path / "t.txt")
        FileUtils.file_io.write_text("שלום", path)
        assert FileUtils.file_io.read_text(path) == "שלום", "Unicode text must roundtrip"

    def test_write_then_read_json(self, tmp_path: Path) -> None:
        path = str(tmp_path / "d.json")
        data = {"a": 1, "b": ["x"]}
        FileUtils.file_io.write_json(data, path)
        assert FileUtils.file_io.read_json(path) == data, "JSON must roundtrip"

    def test_write_then_read_yaml(self, tmp_path: Path) -> None:
        path = str(tmp_path / "d.yaml")
        data = {"a": 1, "b": ["x"]}
        FileUtils.file_io.write_yaml(data, path)
        assert FileUtils.file_io.read_yaml(path) == data, "YAML must roundtrip"

    def test_write_then_read_csv(self, tmp_path: Path) -> None:
        path = str(tmp_path / "d.csv")
        rows = [{"name": "a", "n": "1"}, {"name": "b", "n": "2"}]
        FileUtils.file_io.write_csv(rows, path)
        assert FileUtils.file_io().read_csv(path) == rows, "CSV must roundtrip"

    def test_write_csv_empty_data_creates_nothing(self, tmp_path: Path) -> None:
        path = tmp_path / "empty.csv"
        FileUtils.file_io.write_csv([], str(path))
        assert not path.exists(), "No file should be written for empty data"

    def test_safe_open_binary_mode_returns_bytes(self, text_file: Path) -> None:
        with FileUtils.file_io.safe_open(str(text_file), "rb") as f:
            assert f.read() == b"hello world", "Binary mode must return bytes"

    def test_is_binary_file_detects_null_byte(self, tmp_path: Path, text_file: Path) -> None:
        binary = tmp_path / "b.bin"
        binary.write_bytes(b"ab\0cd")
        assert FileUtils.file_io.is_binary_file(str(binary)), "Null byte means binary"
        assert not FileUtils.file_io.is_binary_file(str(text_file)), "Plain text is not binary"

    def test_is_file_empty(self, tmp_path: Path, text_file: Path) -> None:
        empty = tmp_path / "e.txt"
        empty.touch()
        assert FileUtils.file_io.is_file_empty(str(empty)), "Empty file should be detected"
        assert not FileUtils.file_io.is_file_empty(str(text_file)), "Non-empty file is not empty"


class TestFileManipulation:
    def test_remove_emojis_strips_emoji_and_whitespace(self) -> None:
        result = FileUtils.file_manipulation.remove_emojis("hi 🚀 there 😀 ")
        assert result == "hi  there", f"Got {result!r}"


class TestFilePath:
    def test_ensure_dir_creates_nested(self, tmp_path: Path) -> None:
        target = tmp_path / "a" / "b"
        FileUtils.file_path.ensure_dir(str(target))
        assert target.is_dir(), "Directory should be created"

    def test_ensure_dir_existing_is_noop(self, tmp_path: Path) -> None:
        assert FileUtils.file_path.ensure_dir(str(tmp_path)) == str(tmp_path), "Should return the path"

    def test_file_exists(self, text_file: Path, tmp_path: Path) -> None:
        assert FileUtils.file_path.file_exists(str(text_file)), "Existing file"
        assert not FileUtils.file_path.file_exists(str(tmp_path)), "Directory is not a file"

    @pytest.mark.parametrize(("path", "expected"), [("a/b.txt", "txt"), ("a/b.tar.gz", "gz"), ("a/b", "")])
    def test_get_file_extension(self, path: str, expected: str) -> None:
        assert FileUtils.file_path.get_file_extension(path) == expected, f"Wrong extension for {path}"

    @pytest.mark.parametrize(("with_ext", "expected"), [(True, "b.txt"), (False, "b")])
    def test_get_filename(self, with_ext: bool, expected: str) -> None:
        assert FileUtils.file_path.get_filename("a/b.txt", with_ext) == expected, f"with_extension={with_ext}"

    def test_get_relative_path(self) -> None:
        assert FileUtils.file_path.get_relative_path("/a/b/c", "/a") == "b/c", "Relative path mismatch"

    def test_list_files_non_recursive_with_extension(self, tmp_path: Path) -> None:
        (tmp_path / "a.py").touch()
        (tmp_path / "b.txt").touch()
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "c.py").touch()

        result = FileUtils.file_path.list_files(str(tmp_path), extension=".py")
        assert result == [str(tmp_path / "a.py")], f"Got {result}"

    def test_list_files_recursive(self, tmp_path: Path) -> None:
        (tmp_path / "a.py").touch()
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "c.py").touch()

        result = sorted(FileUtils.file_path.list_files(str(tmp_path), extension=".py", recursive=True))
        assert result == sorted([str(tmp_path / "a.py"), str(tmp_path / "sub" / "c.py")]), f"Got {result}"


class TestFileSystem:
    def test_copy_file(self, text_file: Path, tmp_path: Path) -> None:
        dst = tmp_path / "copy.txt"
        FileUtils.file_system.copy_file(str(text_file), str(dst))
        assert dst.read_text(encoding="utf-8") == "hello world" and text_file.exists(), "Copy keeps source"

    def test_move_file(self, text_file: Path, tmp_path: Path) -> None:
        dst = tmp_path / "moved.txt"
        FileUtils.file_system.move_file(str(text_file), str(dst))
        assert dst.exists() and not text_file.exists(), "Move removes source"

    def test_delete_file(self, text_file: Path) -> None:
        FileUtils.file_system.delete_file(str(text_file))
        assert not text_file.exists(), "File should be deleted"

    def test_delete_missing_file_is_noop(self, tmp_path: Path) -> None:
        FileUtils.file_system.delete_file(str(tmp_path / "missing.txt"))

    def test_file_size(self, text_file: Path) -> None:
        assert FileUtils.file_system.file_size(str(text_file)) == 11, "'hello world' is 11 bytes"
