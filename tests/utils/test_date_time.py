from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from python_base_toolkit.utils.date_time import datetime_now_with_timezone, get_current_date_time_str


class TestDatetimeNowWithTimezone:
    def test_default_is_utc(self) -> None:
        now = datetime_now_with_timezone()
        assert now.tzinfo == ZoneInfo("UTC"), f"Got tzinfo {now.tzinfo}"

    def test_custom_timezone_applied(self) -> None:
        tz = ZoneInfo("Asia/Jerusalem")
        now = datetime_now_with_timezone(tz)
        assert now.tzinfo == tz, f"Got tzinfo {now.tzinfo}"

    def test_non_zoneinfo_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="Expected"):
            datetime_now_with_timezone("UTC")  # type: ignore[arg-type]


class TestGetCurrentDateTimeStr:
    def test_default_format_is_parseable(self) -> None:
        value = get_current_date_time_str()
        parsed = datetime.strptime(value, "%Y-%m-%d_%H%M%S")
        assert parsed.year >= 2024, f"Unexpected value {value}"

    def test_custom_format_is_used(self) -> None:
        value = get_current_date_time_str(date_time_format="%Y")
        assert len(value) == 4 and value.isdigit(), f"Got {value!r}"
