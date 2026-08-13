from typing import List
from sqlalchemy.dialects.postgresql import insert
from src.load.database import get_session
from src.load.models import DimYear, DimCountry, DimIndicator, FactEconomic
from src.transform.models import CleanedRecord


class DatabaseLoader:
    def __init__(self):
        self.session = get_session()

    def load_dim_year(self, records: List[CleanedRecord]) -> dict[int, int]:
        years = {r.year for r in records}
        stmt = insert(DimYear).values([{"year": y} for y in years])
        stmt = stmt.on_conflict_do_nothing(index_elements=["year"])
        self.session.execute(stmt)
        self.session.commit()

        rows = self.session.query(DimYear).all()
        return {r.year: r.year_id for r in rows}

    def load_dim_country(self, records: List[CleanedRecord]) -> dict[str, int]:
        countries = {(r.country_code, r.country_name) for r in records}
        stmt = insert(DimCountry).values([
            {"code": c[0], "name": c[1]} for c in countries
        ])
        stmt = stmt.on_conflict_do_nothing(index_elements=["code"])
        self.session.execute(stmt)
        self.session.commit()

        rows = self.session.query(DimCountry).all()
        return {r.code: r.country_id for r in rows}

    def load_dim_indicator(self, records: List[CleanedRecord]) -> dict[str, int]:
        indicators = {(r.indicator_code, r.indicator_name, r.category, r.unit) for r in records}
        stmt = insert(DimIndicator).values([
            {"wb_code": i[0], "name": i[1], "category": i[2], "unit": i[3]}
            for i in indicators
        ])
        stmt = stmt.on_conflict_do_nothing(index_elements=["wb_code"])
        self.session.execute(stmt)
        self.session.commit()

        rows = self.session.query(DimIndicator).all()
        return {r.wb_code: r.indicator_id for r in rows}

    def load_facts(
        self,
        records: List[CleanedRecord],
        year_map: dict,
        country_map: dict,
        indicator_map: dict,
    ) -> int:
        rows = []
        for r in records:
            rows.append({
                "year_id": year_map[r.year],
                "country_id": country_map[r.country_code],
                "indicator_id": indicator_map[r.indicator_code],
                "value": r.value,
                "source_url": r.source_url,
            })
        stmt = insert(FactEconomic).values(rows)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=["year_id", "country_id", "indicator_id"]
        )
        self.session.execute(stmt)
        self.session.commit()
        return len(rows)