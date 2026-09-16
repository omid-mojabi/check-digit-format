"""
Reading VINs from an input text file.

File format: One VIN per line. Blank lines and lines starting with #
(comments) are ignored.
"""

from __future__ import annotations

from pathlib import Path


def read_vins_from_file(file_path: str | Path) -> list[str]:
    """
    Reads VINs from a text file

    Args:
        file_path: Path to the input file

    Returns:
       A list of VIN strings exactly as they appear in the file 
       without trimming or case conversion—that is the validator's responsibility

    Raises:
        FileNotFoundError: If the file does not exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    vins: list[str] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            vins.append(stripped)

    return vins
