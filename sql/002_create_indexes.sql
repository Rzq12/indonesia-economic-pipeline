CREATE INDEX IF NOT EXISTS idx_fact_year ON fact_economic(year_id);
CREATE INDEX IF NOT EXISTS idx_fact_country ON fact_economic(country_id);
CREATE INDEX IF NOT EXISTS idx_fact_indicator ON fact_economic(indicator_id);
CREATE INDEX IF NOT EXISTS idx_fact_composite ON fact_economic(year_id, country_id, indicator_id);