from unittest.mock import MagicMock, patch

import pytest
import requests

from python_base_toolkit.utils.shorten_url import BASE_TINY_URL, shorten_url


class TestShortenUrl:
    def test_returns_response_text_and_encodes_url(self) -> None:
        response = MagicMock(text="https://tinyurl.com/abc")
        with patch("python_base_toolkit.utils.shorten_url.requests.get", return_value=response) as get:
            result = shorten_url("https://example.com/a b?x=1")

        assert result == "https://tinyurl.com/abc", f"Got {result}"
        get.assert_called_once_with(f"{BASE_TINY_URL}?url=https%3A%2F%2Fexample.com%2Fa+b%3Fx%3D1", timeout=5)

    def test_http_error_propagates(self) -> None:
        response = MagicMock()
        response.raise_for_status.side_effect = requests.HTTPError("500")
        with patch("python_base_toolkit.utils.shorten_url.requests.get", return_value=response):
            with pytest.raises(requests.HTTPError):
                shorten_url("https://example.com")
