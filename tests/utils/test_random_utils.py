import ipaddress
import string

import pytest

from python_base_toolkit.utils.random_utils import (
    create_random_text,
    generate_random_ip,
    generate_random_ipv4,
    generate_random_ipv6,
    generate_random_password,
    generate_random_string,
)

SPECIAL_CHARACTERS = "!@#%^*"


class TestGenerateRandomString:
    def test_default_length_and_charset(self) -> None:
        value = generate_random_string()
        allowed = set(string.ascii_letters + string.digits)
        assert len(value) == 8 and set(value) <= allowed, f"Got {value!r}"

    def test_custom_charset(self) -> None:
        value = generate_random_string(20, charset="ab")
        assert len(value) == 20 and set(value) <= {"a", "b"}, f"Got {value!r}"


class TestGenerateRandomPassword:
    @pytest.mark.parametrize("length", [3, 8, 32])
    def test_password_rules(self, length: int) -> None:
        password = generate_random_password(length)
        assert len(password) == length, f"Expected length {length}, got {len(password)}"
        assert password[0] in string.ascii_uppercase, f"Must start with uppercase: {password!r}"
        assert any(c in string.ascii_lowercase for c in password), f"Needs lowercase: {password!r}"
        assert any(c in string.digits + SPECIAL_CHARACTERS for c in password), f"Needs digit/special: {password!r}"


class TestGenerateRandomIp:
    def test_ipv4_is_valid_unicast_range(self) -> None:
        ip = ipaddress.ip_address(generate_random_ipv4())
        assert ip.version == 4 and 1 <= ip.packed[0] <= 223, f"Got {ip}"

    def test_ipv6_is_valid_global_prefix(self) -> None:
        ip = ipaddress.ip_address(generate_random_ipv6())
        assert ip.version == 6 and 0x2000 <= int(ip) >> 112 <= 0x3FFF, f"Got {ip}"

    @pytest.mark.parametrize("version", [4, 6])
    def test_generate_random_ip_dispatches_by_version(self, version: int) -> None:
        ip = ipaddress.ip_address(generate_random_ip(version))
        assert ip.version == version, f"Expected IPv{version}, got {ip}"

    def test_unsupported_version_raises(self) -> None:
        with pytest.raises(ValueError, match="Unsupported IP version"):
            generate_random_ip(5)


class TestCreateRandomText:
    def test_length_within_bounds(self) -> None:
        text = create_random_text(10, 20)
        assert 10 <= len(text) <= 20 and text.isalpha(), f"Got length {len(text)}"

    def test_fixed_length(self) -> None:
        assert len(create_random_text(5, 5)) == 5, "min == max should fix the length"
