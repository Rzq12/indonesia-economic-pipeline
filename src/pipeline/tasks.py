from prefect import task
from typing import List
from src.extract.worldbank_client import WorldBankClient
from src.extract.models import RawEconomicRecord
from src.transform.cleaners import clean_record
from src.transform.validators import validate_batch
from src.transform.models import CleanedRecord
from src.load.loader import DatabaseLoader


@task(retries=3, retry_delay_seconds=10)
def extract_indicator(
    name: str, code: str, start_year: int, end_year: int
) -> List[RawEconomicRecord]:
    client = WorldBankClient()
    return client.fetch_indicator("ID", code, start_year, end_year)


@task
def transform_records(raw: List[RawEconomicRecord]) -> List[CleanedRecord]:
    cleaned = []
    for record in raw:
        try:
            cleaned.append(clean_record(record))
        except ValueError as e:
            print(f"Skipping: {e}")
    validation = validate_batch(cleaned)
    print(f"Transform: {validation['valid']}/{validation['total']} valid")
    return cleaned


@task
def load_to_warehouse(records: List[CleanedRecord]) -> int:
    loader = DatabaseLoader()
    year_map = loader.load_dim_year(records)
    country_map = loader.load_dim_country(records)
    indicator_map = loader.load_dim_indicator(records)
    count = loader.load_facts(records, year_map, country_map, indicator_map)
    print(f"Loaded {count} fact records")
    return count