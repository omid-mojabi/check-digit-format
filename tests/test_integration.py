"""
Integration test: Reading VINs from the fixture file and validating each one.

This test replicates the actual application flow: input file -> reading -> validation.
"""

from pathlib import Path

from vin_reader import read_vins_from_file
from vin_validator import validate_vin

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "vins.txt"


def test_fixture_file_has_expected_valid_and_invalid_counts():
    vins = read_vins_from_file(FIXTURE_PATH)
    results = [validate_vin(v) for v in vins]

    valid_count = sum(1 for r in results if r.is_valid)
    invalid_count = sum(1 for r in results if not r.is_valid)

    # The fixture file has been created with 3 valid and 2 invalid cases
    assert valid_count == 3
    assert invalid_count == 2


def test_invalid_entries_report_a_reason():
    vins = read_vins_from_file(FIXTURE_PATH)
    results = [validate_vin(v) for v in vins]

    for result in results:
        if not result.is_valid:
            assert len(result.errors) > 0
