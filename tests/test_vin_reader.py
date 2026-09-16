"""Unit Tests for vin_reader"""

import pytest

from vin_reader import read_vins_from_file


def test_reads_simple_vins(tmp_path):
    input_file = tmp_path / "vins.txt"
    input_file.write_text("1M8GDM9AXKP042788\n1HGCM82633A004352\n")

    result = read_vins_from_file(input_file)

    assert result == ["1M8GDM9AXKP042788", "1HGCM82633A004352"]


def test_skips_empty_lines(tmp_path):
    input_file = tmp_path / "vins.txt"
    input_file.write_text("1M8GDM9AXKP042788\n\n\n1HGCM82633A004352\n")

    result = read_vins_from_file(input_file)

    assert result == ["1M8GDM9AXKP042788", "1HGCM82633A004352"]


def test_skips_comment_lines(tmp_path):
    input_file = tmp_path / "vins.txt"
    input_file.write_text(
        "# This is a sample Test\n"
        "1M8GDM9AXKP042788\n"
        "# The next row is a comment\n"
        "1HGCM82633A004352\n"
    ,encoding="utf-8")

    result = read_vins_from_file(input_file)

    assert result == ["1M8GDM9AXKP042788", "1HGCM82633A004352"]


def test_strips_surrounding_whitespace(tmp_path):
    input_file = tmp_path / "vins.txt"
    input_file.write_text("  1M8GDM9AXKP042788  \n\t1HGCM82633A004352\t\n")

    result = read_vins_from_file(input_file)

    assert result == ["1M8GDM9AXKP042788", "1HGCM82633A004352"]


def test_empty_file_returns_empty_list(tmp_path):
    input_file = tmp_path / "empty.txt"
    input_file.write_text("")

    result = read_vins_from_file(input_file)

    assert result == []


def test_raises_when_file_does_not_exist(tmp_path):
    missing_file = tmp_path / "does_not_exist.txt"

    with pytest.raises(FileNotFoundError):
        read_vins_from_file(missing_file)


def test_reads_the_provided_fixture_file():
    # The fixtures/vins.txt file contains a mix of valid and invalid VINs
    # This test checks only that the lines are read correctly, not the content validation
    from pathlib import Path

    fixture_path = Path(__file__).parent / "fixtures" / "vins.txt"
    result = read_vins_from_file(fixture_path)

    assert len(result) > 0
    assert all(isinstance(vin, str) for vin in result)
