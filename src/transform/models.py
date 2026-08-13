from pydantic import BaseModel


class CleanedRecord(BaseModel):
    indicator_code: str
    indicator_name: str
    category: str  # 'gdp', 'inflation', 'employment', 'population', 'trade'
    country_code: str
    country_name: str
    year: int
    value: float
    unit: str
    source_url: str