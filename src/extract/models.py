from pydantic import BaseModel


class RawEconomicRecord(BaseModel):
    indicator_code: str
    indicator_name: str
    country_code: str
    country_name: str
    year: int
    value: float
    unit: str
    source_url: str