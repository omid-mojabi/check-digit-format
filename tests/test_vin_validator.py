"""Unit Tests for vin_validator"""

import pytest

from vin_validator import validate_vin

# Valid VINs (correct check digit) for successful scenario testing
VALID_VINS = [
    "1M8GDM9AXKP042788",  # An Standard Sample for testin Check Digit Algorithm
    "1HGCM82633A004352",
    "JH4KA7561PC008269",
]


@pytest.mark.parametrize("vin", VALID_VINS)
def test_valid_vin_passes(vin):
    result = validate_vin(vin)
    assert result.is_valid
    assert result.errors == []


def test_valid_vin_with_lowercase_is_normalized():
    # Make lowercase letters into uppercase before using
    result = validate_vin("1m8gdm9axkp042788")
    assert result.is_valid
    assert result.vin == "1M8GDM9AXKP042788"


def test_valid_vin_with_surrounding_whitespace():
    result = validate_vin("  1M8GDM9AXKP042788  ")
    assert result.is_valid


@pytest.mark.parametrize(
    "vin,expected_len",
    [
        ("1M8GDM9AXKP04278", 16),   # It has one less character
        ("1M8GDM9AXKP0427888", 18),  # It has one extra character
        ("", 0),
        ("ABC", 3),
    ],
)
def test_wrong_length_is_rejected(vin, expected_len):
    result = validate_vin(vin)
    assert not result.is_valid
    assert any(str(expected_len) in e for e in result.errors)


@pytest.mark.parametrize("bad_char", ["I", "O", "Q"])
def test_forbidden_letters_are_rejected(bad_char):
    # These characters are prohibited in the VIN standard to avoid confusion with numbers
    vin = "1M8GDM9AXKP04278" + bad_char  # 17 characters with the forbidden letter at the end
    result = validate_vin(vin)
    assert not result.is_valid
    assert any("Invalid" in e for e in result.errors)


def test_wrong_check_digit_is_rejected():
    # Test the same valid VIN with an incorrect check digit
    tampered = "1M8GDM9A0KP042788"  # The value at the ninth position has changed from X to 0
    result = validate_vin(tampered)
    assert not result.is_valid
    assert any("check digit" in e for e in result.errors)


def test_check_digit_can_be_skipped():
    # Some non-North American VINs do not follow this check-digit standard
    tampered = "1M8GDM9A0KP042788"
    result = validate_vin(tampered, check_digit=False)
    assert result.is_valid


def test_non_alphanumeric_characters_are_rejected():
    vin = "1M8GDM9A-KP042788"
    result = validate_vin(vin)
    assert not result.is_valid


def test_result_is_falsy_when_invalid():
    result = validate_vin("TOO-SHORT")
    assert not result  # __bool__ must return is_valid.


def test_result_is_truthy_when_valid():
    result = validate_vin("1M8GDM9AXKP042788")
    assert result
