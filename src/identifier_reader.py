"""
Reading identifier strings from an input text file.

This reader is format-agnostic: it simply reads lines of text and
knows nothing about VIN, TIN, or any other specific format. Validating
the content of each line is the responsibility of the appropriate
FormatValidator (see the `validators` package).

File format: One identifier per line. Blank lines and lines starting
with # (comments) are ignored.
"""

from __future__ import annotations

from pathlib import Path


def read_identifiers_from_file(file_path: str | Path) -> list[str]:
    """
    Reads identifier strings from a text file.

    Args:
        file_path: Path to the input file

    Returns:
        A list of strings exactly as they appear in the file, without
        trimming or case conversion—that is the validator's responsibility.

    Raises:
        FileNotFoundError: If the file does not exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    identifiers: list[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            identifiers.append(stripped)

    return identifiers