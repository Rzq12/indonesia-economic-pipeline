# 🇮🇩 Indonesia Economic Data Pipeline

End-to-end ETL pipeline that extracts Indonesian economic data from the
**World Bank API** (free, no auth), transforms it through a star-schema data
warehouse (PostgreSQL), and serves it via a Streamlit dashboard.

## Architecture

World Bank API → Extract (Python) → Transform (Pandas) → Load (PostgreSQL) → Dashboard (Streamlit)

## Tech Stack

- **Extract:** Python requests + World Bank API (no API key needed)
- **Transform:** Pandas, Pydantic validation
- **Load:** SQLAlchemy, PostgreSQL, star schema
- **Orchestration:** Prefect
- **Dashboard:** Streamlit + Plotly

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

---

## Running Locally (Docker Compose)

```bash
cp .env.example .env
docker compose up -d
```

- Dashboard: http://localhost:8501
- PostgreSQL: localhost:5432

## Cloud Deployment (Supabase + GitHub Actions + Streamlit Cloud)

The production setup splits into three free services:

| Component | Service | Notes |
|-----------|---------|-------|
| PostgreSQL | **Supabase** | Free tier, managed |
| ETL pipeline | **GitHub Actions** | Cron daily 01:00 UTC |
| Dashboard | **Streamlit Cloud** | Free, auto-redeploys on push |

### Database Connection

Use the **connection pooler** host, not the direct connection — the direct
host (`db.<ref>.supabase.co`) is IPv6-only and unreachable from GitHub
Actions and Streamlit Cloud runners.

```
DATABASE_URL = postgresql://postgres.<PROJECT_REF>:<PASSWORD>@aws-0-<REGION>.pooler.supabase.com:5432/postgres
```

Notes:

- Username is `postgres.<PROJECT_REF>` (the project ref is part of the
  username, not `postgres` alone).
- URL-encode the password if it contains special characters (`?`, `&`, `#`,
  `%`, `/`, `:`, `@`, or spaces).

### Setup Steps

1. **Supabase** — create a project, note the project ref and region, and copy
   the **Session pooler** connection string (Project → Connect).
2. **GitHub Actions** — set the repo secret:
   ```bash
   gh secret set DATABASE_URL
   ```
   The workflow `.github/workflows/etl.yml` runs the schema init
   (`scripts/init_db.py`) then the ETL flow, daily at 01:00 UTC.
3. **Streamlit Cloud** — deploy `src/dashboard/app.py`, then set the
   `DATABASE_URL` secret in **App settings → Secrets** (TOML format).

### Schema Management

`sql/001_create_schema.sql` and `sql/002_create_indexes.sql` use
`IF NOT EXISTS` and a `UNIQUE (year_id, country_id, indicator_id)` constraint
so the daily pipeline is idempotent. `scripts/init_db.py` applies them for
managed hosts (Supabase/Neon) that lack `docker-entrypoint-initdb.d`.