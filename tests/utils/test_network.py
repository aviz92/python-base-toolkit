from unittest.mock import patch

import pytest

from python_base_toolkit.consts.operating_system import Platform
from python_base_toolkit.utils.network import (
    check_ping_status,
    get_ip_version,
    is_ip_address,
    normalize_connection_string,
    normalize_http_url,
    parse_ifconfig_to_json,
)

IFCONFIG_MACOS = """\
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
\tether a4:83:e7:12:34:56
\tinet6 fe80::1c2b:3d4e:5f60:7182%en0 prefixlen 64 secured scopeid 0xb
\tinet 192.168.1.10 netmask 0xffffff00 broadcast 192.168.1.255
lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
\tinet 127.0.0.1 netmask 255.0.0.0
"""


class TestIpHelpers:
    @pytest.mark.parametrize(("ip", "expected"), [("10.0.0.1", True), ("::1", True), ("nope", False)])
    def test_is_ip_address(self, ip: str, expected: bool) -> None:
        assert is_ip_address(ip) is expected, f"is_ip_address({ip!r})"

    @pytest.mark.parametrize(("ip", "expected"), [("10.0.0.1", 4), ("::1", 6), ("nope", None)])
    def test_get_ip_version(self, ip: str, expected: int | None) -> None:
        assert get_ip_version(ip) == expected, f"get_ip_version({ip!r})"


class TestNormalize:
    @pytest.mark.parametrize(
        ("ip", "port", "expected"),
        [("10.0.0.1", 80, "10.0.0.1:80"), ("10.0.0.1", None, "10.0.0.1:"), ("::1", 443, "[::1]:443")],
    )
    def test_connection_string(self, ip: str, port: int | None, expected: str) -> None:
        assert normalize_connection_string(ip, port) == expected, f"Wrong result for {ip}, {port}"

    def test_connection_string_invalid_ip_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid IP address"):
            normalize_connection_string("bad")

    @pytest.mark.parametrize(("https", "expected"), [(True, "https://[::1]:8443"), (False, "http://[::1]:8443")])
    def test_http_url(self, https: bool, expected: str) -> None:
        assert normalize_http_url("::1", 8443, https=https) == expected, f"https={https}"


class TestParseIfconfig:
    def test_parses_interfaces(self) -> None:
        result = parse_ifconfig_to_json(IFCONFIG_MACOS)
        assert result["en0"] == {
            "mac_address": "a4:83:e7:12:34:56",
            "ipv6_address": "fe80::1c2b:3d4e:5f60:7182",
            "ipv6_prefixlen": "64",
            "ipv4_address": "192.168.1.10",
            "ipv4_netmask": 24,
        }, f"Got {result['en0']}"

    def test_decimal_netmask_converted_to_prefix(self) -> None:
        result = parse_ifconfig_to_json(IFCONFIG_MACOS)
        assert result["lo0"]["ipv4_netmask"] == 8, f"Got {result['lo0']}"

    def test_empty_output_returns_empty_dict(self) -> None:
        assert not parse_ifconfig_to_json(""), "No interfaces expected"


class TestCheckPingStatus:
    @pytest.mark.parametrize("platform", [Platform.LINUX, Platform.MACOS, Platform.WINDOWS])
    @pytest.mark.parametrize(("exit_code", "expected"), [(0, True), (1, False)])
    def test_returns_based_on_exit_code(self, platform: str, exit_code: int, expected: bool) -> None:
        with patch("python_base_toolkit.utils.network.os.system", return_value=exit_code) as system:
            assert check_ping_status(platform, "10.0.0.1", 2) is expected, f"{platform} exit={exit_code}"
        system.assert_called_once()

    @pytest.mark.parametrize(
        ("platform", "command"),
        [
            (Platform.LINUX, "ping -c 2 10.0.0.1"),
            (Platform.MACOS, "ping -c 2 10.0.0.1"),
            (Platform.WINDOWS, "ping -n 2 10.0.0.1"),
        ],
    )
    def test_uses_platform_ping_count_flag(self, platform: str, command: str) -> None:
        with patch("python_base_toolkit.utils.network.os.system", return_value=0) as system:
            check_ping_status(platform, "10.0.0.1", 2)
        system.assert_called_once_with(command)

    def test_os_error_returns_false(self) -> None:
        with patch("python_base_toolkit.utils.network.os.system", side_effect=OSError("boom")):
            assert check_ping_status(Platform.LINUX, "10.0.0.1") is False, "Exceptions should yield False"

    def test_unsupported_platform_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported platform"):
            check_ping_status("Solaris", "10.0.0.1")  # type: ignore[arg-type]
