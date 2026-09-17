"""
Integration test: reading identifiers from the fixture file and
validating each one with the appropriate FormatValidator.
"""

from pathlib import Path

from identifier_reader import read_identifiers_from_file
from validators import VinValidator

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "vins.txt"


def test_fixture_file_has_expected_valid_and_invalid_counts():
    vins = read_identifiers_from_file(FIXTURE_PATH)
    validator = VinValidator()
    results = [validator.validate(v) for v in vins]

    valid_count = sum(1 for r in results if r.is_valid)
    invalid_count = sum(1 for r in results if not r.is_valid)

    # The fixture file was deliberately built with 3 valid and 2 invalid entries
    assert valid_count == 3
    assert invalid_count == 2


def test_invalid_entries_report_a_reason():
    vins = read_identifiers_from_file(FIXTURE_PATH)
    validator = VinValidator()
    results = [validator.validate(v) for v in vins]

    for result in results:
        if not result.is_valid:
            assert len(result.errors) > 0