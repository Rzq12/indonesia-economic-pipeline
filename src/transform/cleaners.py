from src.extract.models import RawEconomicRecord
from src.transform.models import CleanedRecord

CATEGORY_MAP = {
    "NY.GDP.MKTP.KD.ZG": "gdp",
    "FP.CPI.TOTL.ZG": "inflation",
    "SL.UEM.TOTL.ZS": "employment",
    "SP.POP.TOTL": "population",
    "NE.EXP.GNFS.ZS": "trade",
    "BX.KLT.DINV.WD.GD.ZS": "trade",
}


def clean_record(raw: RawEconomicRecord) -> CleanedRecord:
    if raw.value is None:
        raise ValueError(f"Null value for {raw.indicator_name} ({raw.year})")

    category = CATEGORY_MAP.get(raw.indicator_code, "other")

    return CleanedRecord(
        indicator_code=raw.indicator_code.strip(),
        indicator_name=raw.indicator_name.strip(),
        category=category,
        country_code=raw.country_code.strip(),
        country_name=raw.country_name.strip(),
        year=raw.year,
        value=raw.value,
        unit=raw.unit.strip(),
        source_url=raw.source_url,
    )