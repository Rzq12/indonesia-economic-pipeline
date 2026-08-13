from sqlalchemy import text
from src.load.database import get_session

CATEGORY_UNITS = {
    "gdp": "%",
    "inflation": "%",
    "employment": "%",
    "population": "people",
}

CATEGORY_LABELS = {
    "gdp": "GDP Growth",
    "inflation": "Inflation",
    "employment": "Unemployment",
    "population": "Population",
}


def _trend_query(
    category: str,
    start_year: int | None = None,
    end_year: int | None = None,
) -> list[dict]:
    session = get_session()
    query = """
        SELECT y.year, MAX(f.value) AS value
        FROM fact_economic f
        JOIN dim_year y ON f.year_id = y.year_id
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        WHERE i.category = :category
    """
    params = {"category": category}
    if start_year is not None:
        query += " AND y.year >= :start_year"
        params["start_year"] = start_year
    if end_year is not None:
        query += " AND y.year <= :end_year"
        params["end_year"] = end_year
    query += " GROUP BY y.year ORDER BY y.year"
    result = session.execute(text(query), params)
    return [{"year": r[0], "value": r[1]} for r in result]


def get_inflation_trend(start_year=None, end_year=None):
    return _trend_query("inflation", start_year, end_year)


def get_gdp_trend(start_year=None, end_year=None):
    return _trend_query("gdp", start_year, end_year)


def get_unemployment_trend(start_year=None, end_year=None):
    return _trend_query("employment", start_year, end_year)


def get_population_trend(start_year=None, end_year=None):
    return _trend_query("population", start_year, end_year)


def get_latest_values(year: int) -> list[dict]:
    session = get_session()
    result = session.execute(text("""
        SELECT i.category, i.name, MAX(f.value) AS value, y.year, MAX(f.source_url) AS source_url
        FROM fact_economic f
        JOIN dim_year y ON f.year_id = y.year_id
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        WHERE f.country_id = (SELECT country_id FROM dim_country WHERE code = 'IDN')
          AND y.year = :year
        GROUP BY i.category, i.name, y.year
        ORDER BY i.category
    """), {"year": year})
    return [dict(r._mapping) for r in result]


def get_year_over_year(
    category: str,
    start_year: int | None = None,
    end_year: int | None = None,
) -> list[dict]:
    session = get_session()
    query = """
        SELECT y.year,
               MAX(f.value) AS value,
               ROUND((MAX(f.value) - LAG(MAX(f.value)) OVER (ORDER BY y.year))::numeric, 2) as change
        FROM fact_economic f
        JOIN dim_year y ON f.year_id = y.year_id
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        WHERE i.category = :category
    """
    params = {"category": category}
    if start_year is not None:
        query += " AND y.year >= :start_year"
        params["start_year"] = start_year
    if end_year is not None:
        query += " AND y.year <= :end_year"
        params["end_year"] = end_year
    query += " GROUP BY y.year ORDER BY y.year"
    result = session.execute(text(query), params)
    return [dict(r._mapping) for r in result]


def get_summary_stats(start_year=None, end_year=None) -> list[dict]:
    session = get_session()
    query = """
        SELECT
            i.category,
            i.name as indicator_name,
            COUNT(DISTINCT y.year) as records,
            ROUND(AVG(f.value)::numeric, 2) as avg_value,
            ROUND(MIN(f.value)::numeric, 2) as min_value,
            ROUND(MAX(f.value)::numeric, 2) as max_value
        FROM fact_economic f
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        JOIN dim_year y ON f.year_id = y.year_id
        WHERE f.country_id = (SELECT country_id FROM dim_country WHERE code = 'IDN')
    """
    params = {}
    if start_year is not None:
        query += " AND y.year >= :start_year"
        params["start_year"] = start_year
    if end_year is not None:
        query += " AND y.year <= :end_year"
        params["end_year"] = end_year
    query += " GROUP BY i.category, i.name ORDER BY i.category"
    result = session.execute(text(query), params)
    return [dict(r._mapping) for r in result]


def get_year_bounds() -> tuple[int, int]:
    session = get_session()
    result = session.execute(text("SELECT MIN(year), MAX(year) FROM dim_year"))
    row = result.fetchone()
    return int(row[0]), int(row[1])


def get_indicator_categories():
    session = get_session()
    result = session.execute(text("""
        SELECT DISTINCT i.category, i.name
        FROM dim_indicator i
        ORDER BY i.category
    """))
    return [dict(r._mapping) for r in result]


def get_country_list():
    session = get_session()
    result = session.execute(text("""
        SELECT code, name
        FROM dim_country
        ORDER BY name
    """))
    return [dict(r._mapping) for r in result]