import logging
from unittest.mock import patch

from python_base_toolkit.utils.pretty_print import log_in_format


class TestLogInFormat:
    def test_logs_indented_sorted_json_at_level(self) -> None:
        with patch("python_base_toolkit.utils.pretty_print.logger") as logger:
            log_in_format({"b": 1, "a": 2}, log_level=logging.WARNING, indent=2)
        logger.warning.assert_called_once_with("\n%s", '{\n  "a": 2,\n  "b": 1\n}')

    def test_custom_default_used_for_unknown_types(self) -> None:
        with patch("python_base_toolkit.utils.pretty_print.logger") as logger:
            log_in_format({"x": {1}}, default=list, indent=None)
        logger.info.assert_called_once_with("\n%s", '{"x": [1]}')
