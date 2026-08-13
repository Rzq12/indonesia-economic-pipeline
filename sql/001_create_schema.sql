-- Dimension tables
CREATE TABLE IF NOT EXISTS dim_year (
    year_id SERIAL PRIMARY KEY,
    year    INTEGER NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_country (
    country_id SERIAL PRIMARY KEY,
    code       VARCHAR(3) NOT NULL UNIQUE,
    name       VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_indicator (
    indicator_id SERIAL PRIMARY KEY,
    wb_code      VARCHAR(30) NOT NULL UNIQUE,
    name         VARCHAR(200) NOT NULL,
    category     VARCHAR(50) NOT NULL,
    unit         VARCHAR(50) NOT NULL
);

-- Fact table (natural key = year + country + indicator for idempotent upserts)
CREATE TABLE IF NOT EXISTS fact_economic (
    fact_id      SERIAL PRIMARY KEY,
    year_id      INTEGER NOT NULL REFERENCES dim_year(year_id),
    country_id   INTEGER NOT NULL REFERENCES dim_country(country_id),
    indicator_id INTEGER NOT NULL REFERENCES dim_indicator(indicator_id),
    value        DOUBLE PRECISION NOT NULL,
    source_url   TEXT,
    ingested_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (year_id, country_id, indicator_id)
);