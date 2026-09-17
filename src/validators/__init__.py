"""
Format validators package.

Exposes the common FormatValidator interface and its concrete
implementations. New formats can be added by creating a new module
with a FormatValidator subclass and registering it in the VALIDATORS
dict below.
"""

from .base import FormatValidator, ValidationResult
from .tin_validator import TinValidator
from .vin_validator import VinValidator

# Registry mapping a short format key to its validator class.
# This lets calling code select a validator by name (e.g. from a CLI
# argument or config file) without importing each class directly.
VALIDATORS: dict[str, type[FormatValidator]] = {
    "vin": VinValidator,
    "tin": TinValidator,
}

__all__ = [
    "FormatValidator",
    "ValidationResult",
    "VinValidator",
    "TinValidator",
    "VALIDATORS",
]