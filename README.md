# 🇮🇩 Indonesia Economic Data Pipeline

End-to-end ETL pipeline that extracts Indonesian economic data from the
**World Bank API** (free, no auth), transforms it through a star-schema data
warehouse (PostgreSQL), and serves it via a Streamlit dashboard.

## Architecture

World Bank API → Extract (Python) → Transform (Pandas) → Load (PostgreSQL) → Dashboard (Streamlit)

## Quick Start

```bash
cp .env.example .env
docker compose up -d
```

- Dashboard: http://localhost:8501
- PostgreSQL: localhost:5432

## Tech Stack

- **Extract:** Python requests + World Bank API (no API key needed)
- **Transform:** Pandas, Pydantic validation
- **Load:** SQLAlchemy, PostgreSQL, star schema
- **Orchestration:** Prefect
- **Dashboard:** Streamlit + Plotly
- **Infrastructure:** Docker Compose

## Star Schema

- `dim_year` — temporal dimensions
- `dim_country` — country dimensions (Indonesia + comparison countries)
- `dim_indicator` — World Bank indicators (GDP, inflation, unemployment, population)
- `fact_economic` — measurement facts

## World Bank Indicators

| Code | Name |
|------|------|
| `NY.GDP.MKTP.KD.ZG` | GDP Growth (annual %) |
| `FP.CPI.TOTL.ZG` | Inflation (annual %) |
| `SL.UEM.TOTL.ZS` | Unemployment (% of labor force) |
| `SP.POP.TOTL` | Population |

## Project Structure

```
src/
├── extract/     # World Bank API client
├── transform/   # Data cleaning + validation
├── load/        # SQLAlchemy ORM + bulk loader
├── pipeline/    # Prefect ETL flows
└── dashboard/   # Streamlit app
```