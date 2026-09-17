"""Unit Tests for VinValidator"""

import pytest

from validators import VinValidator

# Valid VINs (correct check digit) for successful scenario testing
VALID_VINS = [
    "1M8GDM9AXKP042788",  # A standard sample for testing the check-digit algorithm
    "1HGCM82633A004352",
    "JH4KA7561PC008269",
]


@pytest.mark.parametrize("vin", VALID_VINS)
def test_valid_vin_passes(vin):
    result = VinValidator().validate(vin)
    assert result.is_valid
    assert result.errors == []


def test_valid_vin_with_lowercase_is_normalized():
    # Lowercase letters are converted to uppercase before validation
    result = VinValidator().validate("1m8gdm9axkp042788")
    assert result.is_valid
    assert result.value == "1M8GDM9AXKP042788"


def test_valid_vin_with_surrounding_whitespace():
    result = VinValidator().validate("  1M8GDM9AXKP042788  ")
    assert result.is_valid


@pytest.mark.parametrize(
    "vin,expected_len",
    [
        ("1M8GDM9AXKP04278", 16),   # One character short
        ("1M8GDM9AXKP0427888", 18),  # One character too many
        ("", 0),
        ("ABC", 3),
    ],
)
def test_wrong_length_is_rejected(vin, expected_len):
    result = VinValidator().validate(vin)
    assert not result.is_valid
    assert any(str(expected_len) in e for e in result.errors)


@pytest.mark.parametrize("bad_char", ["I", "O", "Q"])
def test_forbidden_letters_are_rejected(bad_char):
    # These characters are prohibited in the VIN standard to avoid confusion with numbers
    vin = "1M8GDM9AXKP04278" + bad_char  # 17 characters with the forbidden letter at the end
    result = VinValidator().validate(vin)
    assert not result.is_valid
    assert any("Invalid" in e for e in result.errors)


def test_wrong_check_digit_is_rejected():
    # The same valid VIN, but with an incorrect check digit
    tampered = "1M8GDM9A0KP042788"  # The value at the ninth position changed from X to 0
    result = VinValidator().validate(tampered)
    assert not result.is_valid
    assert any("check digit" in e for e in result.errors)


def test_check_digit_can_be_skipped():
    # Some non-North American VINs do not follow this check-digit standard
    tampered = "1M8GDM9A0KP042788"
    result = VinValidator(check_digit=False).validate(tampered)
    assert result.is_valid


def test_non_alphanumeric_characters_are_rejected():
    vin = "1M8GDM9A-KP042788"
    result = VinValidator().validate(vin)
    assert not result.is_valid


def test_result_is_falsy_when_invalid():
    result = VinValidator().validate("TOO-SHORT")
    assert not result  # __bool__ must return is_valid.


def test_result_is_truthy_when_valid():
    result = VinValidator().validate("1M8GDM9AXKP042788")
    assert result