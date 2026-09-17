"""
Base abstractions for format validators.

This module defines the common interface that every format-specific
validator (VIN, TIN, etc.) implements. Using a shared interface allows
calling code to validate any supported format polymorphically, without
needing to know which concrete validator class handles it.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """
    The result of validating an identifier string.

    This class is shared by all format validators (VIN, TIN, etc.) so
    that calling code can handle results uniformly, regardless of
    which format was actually validated.
    """

    value: str
    format_name: str
    is_valid: bool
    errors: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.is_valid


class FormatValidator(ABC):
    """
    Abstract base class for all identifier format validators.

    Each concrete subclass (e.g. VinValidator, TinValidator) implements
    the `validate` method according to its own format rules. This is
    the polymorphic entry point: calling code can hold a reference of
    type FormatValidator and call `.validate(raw)` without caring which
    concrete format it actually is.
    """

    #: Human-readable name of the format, stored in ValidationResult.format_name
    format_name: str = "unknown"

    @abstractmethod
    def validate(self, raw: str) -> ValidationResult:
        """
        Validates a raw identifier string.

        Args:
            raw: The raw input string (not yet normalized).

        Returns:
            A ValidationResult describing whether the input is valid,
            and if not, why.
        """
        raise NotImplementedError