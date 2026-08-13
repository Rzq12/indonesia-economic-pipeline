from src.extract.models import RawEconomicRecord
from src.transform.cleaners import clean_record


def test_clean_record_maps_category():
    raw = RawEconomicRecord(
        indicator_code="NY.GDP.MKTP.KD.ZG",
        indicator_name="GDP growth (annual %)",
        country_code="IDN",
        country_name="Indonesia",
        year=2023,
        value=5.05,
        unit="%",
        source_url="https://api.worldbank.org",
    )
    cleaned = clean_record(raw)
    assert cleaned.value == 5.05
    assert cleaned.year == 2023
    assert cleaned.category == "gdp"


def test_clean_record_unknown_category():
    raw = RawEconomicRecord(
        indicator_code="XX.UNKNOWN.CODE",
        indicator_name="Unknown",
        country_code="IDN",
        country_name="Indonesia",
        year=2023,
        value=1.0,
        unit="%",
        source_url="https://api.worldbank.org",
    )
    cleaned = clean_record(raw)
    assert cleaned.category == "other"


def test_clean_record_null_value_raises():
    raw = RawEconomicRecord(
        indicator_code="NY.GDP.MKTP.KD.ZG",
        indicator_name="GDP growth (annual %)",
        country_code="IDN",
        country_name="Indonesia",
        year=2023,
        value=None,
        unit="%",
        source_url="https://api.worldbank.org",
    )
    try:
        clean_record(raw)
        assert False, "Should have raised"
    except ValueError:
        pass