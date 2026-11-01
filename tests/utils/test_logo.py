import pytest

from python_base_toolkit.utils.logo import create_logo


class TestCreateLogo:
    def test_returns_multiline_ascii_art(self) -> None:
        logo = create_logo("Hi")
        assert len(logo.splitlines()) > 1, f"Expected multi-line art, got {logo!r}"

    def test_unknown_font_raises(self) -> None:
        with pytest.raises(Exception, match="font"):
            create_logo("Hi", font="no-such-font")
