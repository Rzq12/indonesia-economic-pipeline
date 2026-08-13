from prefect import flow
from .tasks import extract_indicator, transform_records, load_to_warehouse

INDICATORS = {
    "gdp": "NY.GDP.MKTP.KD.ZG",
    "inflation": "FP.CPI.TOTL.ZG",
    "unemployment": "SL.UEM.TOTL.ZS",
    "population": "SP.POP.TOTL",
}


@flow(name="indonesia-economic-etl")
def run_etl_pipeline(start_year: int = 2000, end_year: int = 2024):
    """Main ETL pipeline for Indonesian economic data from World Bank."""
    total_loaded = 0

    for name, code in INDICATORS.items():
        raw = extract_indicator(name, code, start_year, end_year)
        clean = transform_records(raw)
        count = load_to_warehouse(clean)
        total_loaded += count
        print(f"  {name}: {count} records")

    print(f"ETL complete: {total_loaded} total records loaded")
    return total_loaded


if __name__ == "__main__":
    run_etl_pipeline()