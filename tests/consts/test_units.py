import pytest

from python_base_toolkit.consts.units import binary_units, time_units


class TestBinaryUnits:
    @pytest.mark.parametrize(
        ("unit", "expected"),
        [
            (binary_units.KiB, 2**10),
            (binary_units.MiB, 2**20),
            (binary_units.GiB, 2**30),
            (binary_units.TiB, 2**40),
            (binary_units.PiB, 2**50),
            (binary_units.EiB, 2**60),
        ],
    )
    def test_binary_multiples_are_powers_of_two(self, unit: int, expected: int) -> None:
        assert unit == expected, f"Got {unit}, expected {expected}"

    @pytest.mark.parametrize(
        ("unit", "expected"),
        [(binary_units.KB, 10**3), (binary_units.GB, 10**9), (binary_units.TB, 10**12), (binary_units.EB, 10**18)],
    )
    def test_decimal_multiples_are_powers_of_ten(self, unit: int, expected: int) -> None:
        assert unit == expected, f"Got {unit}, expected {expected}"


class TestTimeUnits:
    @pytest.mark.parametrize(
        ("unit", "seconds"),
        [
            (time_units.Minute, 60),
            (time_units.Hour, 3600),
            (time_units.Day, 86400),
            (time_units.Week, 604800),
            (time_units.Month, 2592000),
            (time_units.Year, 31536000),
        ],
    )
    def test_units_in_seconds(self, unit: int, seconds: int) -> None:
        assert unit == seconds, f"Got {unit}, expected {seconds}"

    def test_sub_second_units_ordered(self) -> None:
        ordered = [time_units.Pico_Second, time_units.Nano_Second, time_units.Micro_Second, time_units.Milli_Second]
        assert ordered == sorted(ordered) and ordered[-1] < time_units.Second, "Sub-second units out of order"
