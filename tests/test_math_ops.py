import datetime
import math
import sys

import pytest

from techlang.interpreter import run


def _single_output(code: str) -> str:
    return run(code).strip()


def _output_lines(code: str):
    return run(code).strip().splitlines()


def test_trigonometric_commands_produce_expected_values():
    assert float(_single_output("math_sin 30")) == pytest.approx(0.5, rel=1e-6)
    assert float(_single_output("math_cos 60")) == pytest.approx(0.5, rel=1e-6)
    assert float(_single_output("math_tan 45")) == pytest.approx(1.0, rel=1e-6)


def test_inverse_trigonometric_commands_return_degrees():
    assert float(_single_output("math_asin 1")) == pytest.approx(90.0, rel=1e-6)
    assert float(_single_output("math_acos 0")) == pytest.approx(90.0, rel=1e-6)
    assert float(_single_output("math_atan 1")) == pytest.approx(45.0, rel=1e-6)


def test_domain_errors_are_reported_for_inverse_trig():
    output = _output_lines("math_asin 2")
    assert "[Error: math_asin domain is [-1, 1]]" in output

    output = _output_lines("math_acos -2")
    assert "[Error: math_acos domain is [-1, 1]]" in output


def test_rounding_helpers_return_integers():
    assert _single_output("math_round 3.6") == "4"
    assert _single_output("math_floor 3.6") == "3"
    assert _single_output("math_ceil 3.2") == "4"


def test_angle_conversion_helpers():
    assert float(_single_output("math_deg2rad 180")) == pytest.approx(math.pi, rel=1e-9)
    assert float(_single_output("math_rad2deg 3.141592653589793")) == pytest.approx(180.0, rel=1e-6)


def test_date_helpers_emit_utc_iso_strings():
    iso = _single_output("now")
    parsed = datetime.datetime.fromisoformat(iso)
    assert parsed.tzinfo is not None
    assert parsed.tzinfo.utcoffset(parsed) == datetime.timedelta(0)



def test_format_date_with_custom_pattern():
    formatted = _single_output('format_date 0 "%Y-%m-%d"')
    assert formatted == "1970-01-01"


def test_format_date_handles_out_of_range_timestamp():
    output = _output_lines("format_date 9999999999999999999999")
    assert "[Error: format_date timestamp out of range]" in output


@pytest.mark.skipif(
    sys.version_info < (3, 11),
    reason="Python 3.10 strftime behavior differs across platforms"
)
def test_format_date_reports_invalid_pattern():
    # Test that invalid format strings are caught
    output = _output_lines('format_date 0 "%"')
    assert any("Invalid format string" in line or "Error" in line for line in output)
