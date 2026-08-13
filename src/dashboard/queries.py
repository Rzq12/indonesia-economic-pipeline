from sqlalchemy import text
from src.load.database import get_session


def _trend_query(category: str, limit: int | None = None) -> list[dict]:
    session = get_session()
    query = """
        SELECT y.year, f.value
        FROM fact_economic f
        JOIN dim_year y ON f.year_id = y.year_id
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        WHERE i.category = :category
        ORDER BY y.year
    """
    if limit:
        query += " LIMIT :limit"
        result = session.execute(text(query), {"category": category, "limit": limit})
    else:
        result = session.execute(text(query), {"category": category})
    return [{"year": r[0], "value": r[1]} for r in result]


def get_inflation_trend():
    return _trend_query("inflation")


def get_gdp_trend():
    return _trend_query("gdp")


def get_unemployment_trend():
    return _trend_query("employment")


def get_population_trend():
    return _trend_query("population")


def get_latest_values() -> list[dict]:
    session = get_session()
    result = session.execute(text("""
        SELECT i.category, i.name, f.value, y.year, f.source_url
        FROM fact_economic f
        JOIN dim_year y ON f.year_id = y.year_id
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        WHERE f.country_id = (SELECT country_id FROM dim_country WHERE code = 'IDN')
          AND y.year = (SELECT MAX(year) FROM dim_year)
    """))
    return [dict(r._mapping) for r in result]


def get_year_over_year(category: str) -> list[dict]:
    session = get_session()
    result = session.execute(text("""
        SELECT y.year, f.value,
               LAG(f.value) OVER (ORDER BY y.year) as prev_value,
               ROUND(((f.value - LAG(f.value) OVER (ORDER BY y.year)) / NULLIF(LAG(f.value) OVER (ORDER BY y.year), 0) * 100)::numeric, 2) as yoy_pct
        FROM fact_economic f
        JOIN dim_year y ON f.year_id = y.year_id
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        WHERE i.category = :category
        ORDER BY y.year
    """), {"category": category})
    return [dict(r._mapping) for r in result]


def get_summary_stats():
    session = get_session()
    result = session.execute(text("""
        SELECT
            i.category,
            i.name as indicator_name,
            COUNT(*) as records,
            ROUND(AVG(f.value)::numeric, 2) as avg_value,
            ROUND(MIN(f.value)::numeric, 2) as min_value,
            ROUND(MAX(f.value)::numeric, 2) as max_value
        FROM fact_economic f
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        WHERE f.country_id = (SELECT country_id FROM dim_country WHERE code = 'IDN')
        GROUP BY i.category, i.name
        ORDER BY i.category
    """))
    return [dict(r._mapping) for r in result]


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