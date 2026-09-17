"""Unit Tests for TinValidator"""

from validators import TinValidator

# A valid TIN: plant "MN", size code "8H", manufacturer code "0123",
# week "20", year "23"
VALID_TIN = "MN8H01232023"


def test_valid_tin_passes():
    result = TinValidator().validate(VALID_TIN)
    assert result.is_valid
    assert result.errors == []


def test_valid_tin_with_lowercase_and_whitespace_is_normalized():
    result = TinValidator().validate("  mn8h01232023  ")
    assert result.is_valid
    assert result.value == VALID_TIN


def test_wrong_length_is_rejected():
    result = TinValidator().validate("MN8H012320235")  # 13 characters, one too many
    assert not result.is_valid
    assert any("12" in e for e in result.errors)


def test_non_alphanumeric_date_code_is_rejected():
    # The last four characters must be digits (week + year), not letters
    result = TinValidator().validate("MN8H0123AB23")
    assert not result.is_valid
    assert any("Invalid TIN format" in e for e in result.errors)


def test_week_out_of_range_is_rejected():
    # There is no week 65 in a year (valid range is 01-53)
    result = TinValidator().validate("MN8H01236523")
    assert not result.is_valid
    assert any("week" in e for e in result.errors)


def test_result_is_falsy_when_invalid():
    result = TinValidator().validate("TOO-SHORT")
    assert not result


def test_result_is_truthy_when_valid():
    result = TinValidator().validate(VALID_TIN)
    assert result


def test_format_name_is_set_correctly():
    result = TinValidator().validate(VALID_TIN)
    assert result.format_name == "TIN"