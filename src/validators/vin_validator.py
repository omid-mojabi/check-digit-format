"""
Vehicle Identification Number (VIN) Validation

A standard VIN consists of 17 characters, comprising uppercase English
letters (excluding I, O, and Q) and numbers. This validator performs
two types of checks:

1. Format check: Length and allowed characters
2. Check Digit verification: Based on the standard NHTSA algorithm
   applicable to vehicles manufactured in North America (9th position
   of the VIN)

VinValidator implements the common FormatValidator interface, so it can
be used polymorphically alongside other format validators such as
TinValidator.
"""

from __future__ import annotations

import re

from .base import FormatValidator, ValidationResult

VIN_LENGTH = 17

# The letters I, O, and Q are not allowed in the VIN because they resemble the numbers 1 and 0
VIN_PATTERN = re.compile(r"^[A-HJ-NPR-Z0-9]{17}$")

# Table of numerical values for each character, used to calculate the check digit
_TRANSLITERATION = {
    **{str(d): d for d in range(10)},
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
    "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
}

# Weight of each position: position 9 is the check digit itself and has no weight
_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]


def _check_digit(vin: str) -> str:
    """Calculates the standard check digit based on the other 16 characters of the VIN"""
    total = 0
    for char, weight in zip(vin, _WEIGHTS):
        total += _TRANSLITERATION[char] * weight
    remainder = total % 11
    return "X" if remainder == 10 else str(remainder)


class VinValidator(FormatValidator):
    """
    Validates Vehicle Identification Numbers (VIN) according to the
    17-character standard, including the NHTSA check-digit algorithm.
    """

    format_name = "VIN"

    def __init__(self, *, check_digit: bool = True) -> None:
        """
        Args:
            check_digit: If True, the check digit at the ninth position
                is also verified. Some non-North American VINs do not
                follow this standard; in such cases, this check can be
                disabled.
        """
        self.check_digit = check_digit

    def validate(self, raw: str) -> ValidationResult:
        """
        Validates a VIN string.

        Args:
            raw: Input string (surrounding whitespace is ignored)

        Returns:
            ValidationResult with error details if invalid
        """
        vin = raw.strip().upper()
        errors: list[str] = []

        if len(vin) != VIN_LENGTH:
            errors.append(f"VIN length must be {VIN_LENGTH} characters; current length: {len(vin)}")

        if not VIN_PATTERN.match(vin):
            invalid_chars = sorted(set(vin) - set("ABCDEFGHJKLMNPRSTUVWXYZ0123456789"))
            if invalid_chars:
                errors.append(f"Invalid characters found: {', '.join(invalid_chars)}")
            elif len(vin) == VIN_LENGTH:
                # The length is correct, but the pattern doesn't match
                errors.append("Invalid VIN format")

        # The check digit can only be calculated if the length and characters are correct
        if self.check_digit and not errors:
            expected = _check_digit(vin)
            actual = vin[8]
            if actual != expected:
                errors.append(
                    f"Invalid check digit: the ninth position is '{actual}', but it should be '{expected}'"
                )

        return ValidationResult(value=vin, format_name=self.format_name, is_valid=not errors, errors=errors)