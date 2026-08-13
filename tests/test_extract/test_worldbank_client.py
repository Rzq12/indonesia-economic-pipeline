import pytest
from unittest.mock import Mock, patch
from src.extract.worldbank_client import WorldBankClient
from src.extract.models import RawEconomicRecord


@pytest.fixture
def client():
    return WorldBankClient()


def test_fetch_indicator_returns_records(client):
    mock_response = [
        {},
        [{
            "indicator": {"id": "NY.GDP.MKTP.KD.ZG", "value": "GDP growth (annual %)"},
            "country": {"id": "ID", "value": "Indonesia"},
            "countryiso3code": "IDN",
            "date": "2023",
            "value": "5.05",
        }],
    ]
    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = Mock()
        records = client.fetch_indicator("ID", "NY.GDP.MKTP.KD.ZG", 2023, 2023)
        assert len(records) == 1
        assert records[0].value == 5.05
        assert records[0].indicator_name == "GDP growth (annual %)"
        assert records[0].country_code == "IDN"
        assert records[0].year == 2023


def test_fetch_indicator_skips_null_values(client):
    mock_response = [
        {},
        [{
            "indicator": {"id": "FP.CPI.TOTL.ZG", "value": "Inflation"},
            "country": {"id": "ID", "value": "Indonesia"},
            "countryiso3code": "IDN",
            "date": "2023",
            "value": None,
        }],
    ]
    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = Mock()
        records = client.fetch_indicator("ID", "FP.CPI.TOTL.ZG", 2023, 2023)
        assert len(records) == 0


def test_fetch_indicator_empty_response(client):
    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value.json.return_value = [{}, None]
        mock_get.return_value.raise_for_status = Mock()
        records = client.fetch_indicator("ID", "XX.YYY", 2023, 2023)
        assert len(records) == 0