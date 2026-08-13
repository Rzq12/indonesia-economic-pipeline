from sqlalchemy import text
from src.load.database import get_session


def get_inflation_trend():
    session = get_session()
    result = session.execute(text("""
        SELECT y.year, f.value
        FROM fact_economic f
        JOIN dim_year y ON f.year_id = y.year_id
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        WHERE i.category = 'inflation'
        ORDER BY y.year
    """))
    return [{"year": r[0], "value": r[1]} for r in result]


def get_gdp_trend():
    session = get_session()
    result = session.execute(text("""
        SELECT y.year, f.value
        FROM fact_economic f
        JOIN dim_year y ON f.year_id = y.year_id
        JOIN dim_indicator i ON f.indicator_id = i.indicator_id
        WHERE i.category = 'gdp'
        ORDER BY y.year DESC
        LIMIT 10
    """))
    return [{"year": r[0], "value": r[1]} for r in result]


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
    """))
    return [dict(r._mapping) for r in result]