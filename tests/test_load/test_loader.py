import pytest
from unittest.mock import patch, MagicMock
from src.transform.models import CleanedRecord
from src.load.loader import DatabaseLoader


@pytest.fixture
def sample_records():
    return [
        CleanedRecord(
            indicator_code="NY.GDP.MKTP.KD.ZG",
            indicator_name="GDP growth (annual %)",
            category="gdp",
            country_code="IDN",
            country_name="Indonesia",
            year=2023,
            value=5.05,
            unit="%",
            source_url="https://api.worldbank.org",
        ),
        CleanedRecord(
            indicator_code="FP.CPI.TOTL.ZG",
            indicator_name="Inflation, consumer prices (annual %)",
            category="inflation",
            country_code="IDN",
            country_name="Indonesia",
            year=2023,
            value=3.67,
            unit="%",
            source_url="https://api.worldbank.org",
        ),
    ]


def test_load_dim_year(sample_records, session):
    with patch("src.load.loader.get_session", return_value=session):
        loader = DatabaseLoader()
        year_map = loader.load_dim_year(sample_records)
        assert 2023 in year_map
        assert isinstance(year_map[2023], int)


def test_load_dim_country(sample_records, session):
    with patch("src.load.loader.get_session", return_value=session):
        loader = DatabaseLoader()
        country_map = loader.load_dim_country(sample_records)
        assert "IDN" in country_map


def test_load_dim_indicator(sample_records, session):
    with patch("src.load.loader.get_session", return_value=session):
        loader = DatabaseLoader()
        indicator_map = loader.load_dim_indicator(sample_records)
        assert "NY.GDP.MKTP.KD.ZG" in indicator_map
        assert "FP.CPI.TOTL.ZG" in indicator_map


def test_load_facts(sample_records, session):
    with patch("src.load.loader.get_session", return_value=session):
        loader = DatabaseLoader()
        year_map = loader.load_dim_year(sample_records)
        country_map = loader.load_dim_country(sample_records)
        indicator_map = loader.load_dim_indicator(sample_records)
        count = loader.load_facts(sample_records, year_map, country_map, indicator_map)
        assert count == 2