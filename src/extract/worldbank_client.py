import requests
from typing import List

from .models import RawEconomicRecord

WB_BASE_URL = "https://api.worldbank.org/v2"


class WorldBankClient:
    def __init__(self):
        self.session = requests.Session()

    def fetch_indicator(
        self, country_code: str, indicator_code: str, start_year: int, end_year: int
    ) -> List[RawEconomicRecord]:
        url = f"{WB_BASE_URL}/country/{country_code}/indicator/{indicator_code}"
        params = {"format": "json", "per_page": 500, "date": f"{start_year}:{end_year}"}
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if len(data) < 2 or data[1] is None:
            return []
        return self._parse_response(data, indicator_code, country_code)

    def _parse_response(
        self, data: list, indicator_code: str, country_code: str
    ) -> List[RawEconomicRecord]:
        indicator_name = data[1][0].get("indicator", {}).get("value", indicator_code) if data[1] else indicator_code
        country_name = data[1][0].get("country", {}).get("value", country_code) if data[1] else country_code

        records = []
        for item in data[1]:
            if item.get("value") is None:
                continue
            records.append(RawEconomicRecord(
                indicator_code=indicator_code,
                indicator_name=indicator_name,
                country_code=item.get("countryiso3code", country_code),
                country_name=country_name,
                year=int(item["year"]),
                value=float(item["value"]),
                unit="%",
                source_url=f"{WB_BASE_URL}/country/{country_code}/indicator/{indicator_code}",
            ))
        return records