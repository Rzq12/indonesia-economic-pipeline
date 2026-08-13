from src.transform.models import CleanedRecord
from src.transform.validators import validate_record, validate_batch


def test_validate_record_valid():
    record = CleanedRecord(
        indicator_code="NY.GDP.MKTP.KD.ZG",
        indicator_name="GDP growth",
        category="gdp",
        country_code="IDN",
        country_name="Indonesia",
        year=2023,
        value=5.05,
        unit="%",
        source_url="https://api.worldbank.org",
    )
    is_valid, error = validate_record(record)
    assert is_valid
    assert error is None


def test_validate_record_invalid_year():
    record = CleanedRecord(
        indicator_code="NY.GDP.MKTP.KD.ZG",
        indicator_name="GDP growth",
        category="gdp",
        country_code="IDN",
        country_name="Indonesia",
        year=1990,
        value=5.05,
        unit="%",
        source_url="https://api.worldbank.org",
    )
    is_valid, error = validate_record(record)
    assert not is_valid
    assert "Invalid year" in error


def test_validate_record_gdp_out_of_range():
    record = CleanedRecord(
        indicator_code="NY.GDP.MKTP.KD.ZG",
        indicator_name="GDP growth",
        category="gdp",
        country_code="IDN",
        country_name="Indonesia",
        year=2023,
        value=100.0,
        unit="%",
        source_url="https://api.worldbank.org",
    )
    is_valid, error = validate_record(record)
    assert not is_valid
    assert "GDP value out of range" in error


def test_validate_batch():
    records = [
        CleanedRecord(
            indicator_code="NY.GDP.MKTP.KD.ZG",
            indicator_name="GDP growth",
            category="gdp",
            country_code="IDN",
            country_name="Indonesia",
            year=2023,
            value=5.05,
            unit="%",
            source_url="https://api.worldbank.org",
        ),
        CleanedRecord(
            indicator_code="NY.GDP.MKTP.KD.ZG",
            indicator_name="GDP growth",
            category="gdp",
            country_code="IDN",
            country_name="",
            year=2023,
            value=5.05,
            unit="%",
            source_url="https://api.worldbank.org",
        ),
    ]
    result = validate_batch(records)
    assert result["total"] == 2
    assert result["valid"] == 1
    assert result["invalid"] == 1