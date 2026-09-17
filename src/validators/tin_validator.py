"""
DOT Tire Identification Number (TIN) Validation

A DOT TIN is the identifier molded into the sidewall of a tire, as
required by the US Department of Transportation (NHTSA) and used
worldwide by tire manufacturers to identify the plant, tire size, and
manufacturing date.

Unlike a VIN, a TIN has no mathematical check digit. Instead, this
validator checks:

1. Format check: fixed length and allowed characters
2. Date code check: the last four characters must be a valid
   week-of-year (01-53) followed by a two-digit year

Note: real-world TINs historically varied in length (10 to 13
characters) depending on the tire's manufacturing date and whether
optional manufacturer codes were used. This validator implements a
simplified, fixed 12-character format for demonstration purposes:

    [2 chars: plant code][2 chars: tire size code]
    [4 chars: manufacturer code][2 digits: week][2 digits: year]

TinValidator implements the common FormatValidator interface, so it
can be used polymorphically alongside other format validators such
as VinValidator.
"""

from __future__ import annotations

import re

from .base import FormatValidator, ValidationResult

TIN_LENGTH = 12

# First 8 characters: plant code + size code + manufacturer code (uppercase letters and digits)
# Last 4 characters: 2-digit week + 2-digit year (the manufacturing date code)
_TIN_PATTERN = re.compile(r"^[A-Z0-9]{8}(\d{2})(\d{2})$")


class TinValidator(FormatValidator):
    """
    Validates DOT Tire Identification Numbers (TIN) using a simplified,
    fixed-length format with a manufacturing date-code check.
    """

    format_name = "TIN"

    def validate(self, raw: str) -> ValidationResult:
        """
        Validates a TIN string.

        Args:
            raw: Input string (surrounding whitespace is ignored)

        Returns:
            ValidationResult with error details if invalid
        """
        tin = raw.strip().upper()
        errors: list[str] = []

        if len(tin) != TIN_LENGTH:
            errors.append(f"TIN length must be {TIN_LENGTH} characters; current length: {len(tin)}")

        match = _TIN_PATTERN.match(tin) if len(tin) == TIN_LENGTH else None

        if len(tin) == TIN_LENGTH and match is None:
            errors.append(
                "Invalid TIN format: expected 8 alphanumeric characters followed by a 4-digit date code"
            )

        # The date code (week + year) can only be checked if the format matched
        if match is not None:
            week = int(match.group(1))
            if not (1 <= week <= 53):
                errors.append(f"Invalid manufacturing week '{match.group(1)}': must be between 01 and 53")

        return ValidationResult(value=tin, format_name=self.format_name, is_valid=not errors, errors=errors)