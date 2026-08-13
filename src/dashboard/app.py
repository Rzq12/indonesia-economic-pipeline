import os
import sys
from pathlib import Path

# Make `src` importable regardless of launch method (Docker, Streamlit Cloud, local)
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import streamlit as st

# Load secrets into env before any DB access (Streamlit Cloud); fall back to env var
try:
    if "DATABASE_URL" in st.secrets:
        os.environ["DATABASE_URL"] = st.secrets["DATABASE_URL"]
except Exception:
    pass  # no secrets file configured — use os.environ (Docker/local)

from src.dashboard.queries import (
    get_inflation_trend, get_gdp_trend, get_unemployment_trend,
    get_population_trend, get_latest_values,
    get_year_over_year, get_year_bounds,
)
from src.dashboard.charts import (
    build_line_chart, build_bar_chart,
    build_yoy_chart, build_scatter_correlation,
)

st.set_page_config(
    page_title="Indonesia Economic Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

CATEGORY_LABELS = {
    "gdp": "Pertumbuhan Ekonomi (GDP)",
    "inflation": "Inflasi",
    "employment": "Pengangguran",
    "population": "Jumlah Penduduk",
}

CATEGORY_COLORS = {
    "gdp": "#1f77b4",
    "inflation": "#ff7f0e",
    "employment": "#2ca02c",
    "population": "#d62728",
}

CATEGORY_DESC = {
    "gdp": "Seberapa cepat ekonomi Indonesia tumbuh dari tahun ke tahun.",
    "inflation": "Kenaikan rata-rata harga barang dan jasa yang dibayar konsumen.",
    "employment": "Persentase angkatan kerja yang sedang mencari pekerjaan.",
    "population": "Total penduduk Indonesia yang tercatat.",
}

ICONS = {
    "gdp": "📈",
    "inflation": "💹",
    "employment": "🧑‍💼",
    "population": "👥",
}


def format_value(category: str, value: float) -> str:
    if category == "population":
        return f"{value / 1_000_000:,.1f} juta"
    return f"{value:,.2f}%"


def format_delta(category: str, delta_abs: float | None) -> str:
    if delta_abs is None:
        return "Tidak ada data pembanding"
    if category == "population":
        sign = "+" if delta_abs >= 0 else ""
        return f"{sign}{delta_abs / 1_000_000:,.1f} juta"
    sign = "+" if delta_abs >= 0 else ""
    return f"{sign}{delta_abs:,.2f} poin"


def get_kpi_data(year: int) -> list[dict]:
    latest = get_latest_values(year)
    if not latest:
        return []
    previous = get_latest_values(year - 1)
    prev_map = {p["category"]: p["value"] for p in previous}

    result = []
    for item in latest:
        cat = item["category"]
        cur = item["value"]
        prev = prev_map.get(cat)
        if prev:
            delta_abs = cur - prev
        else:
            delta_abs = None
        result.append({**item, "delta_abs": delta_abs})
    return result


def render_kpi_card(item: dict) -> None:
    cat = item["category"]
    delta_abs = item["delta_abs"]
    if delta_abs is not None and delta_abs >= 0:
        arrow = "▲"
        color = "#2ca02c"
    elif delta_abs is not None:
        arrow = "▼"
        color = "#d62728"
    else:
        arrow = "—"
        color = "#999999"

    st.markdown(
        f"""
        <div style="
            background: white;
            border: 1px solid #e5e7eb;
            border-top: 4px solid {CATEGORY_COLORS[cat]};
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            min-height: 150px;
        ">
            <div style="font-size: 1.6rem; line-height: 1;">{ICONS[cat]}</div>
            <div style="
                font-size: 0.72rem;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                color: #6b7280;
                margin-top: 0.4rem;
                font-weight: 600;
            ">{CATEGORY_LABELS[cat]}</div>
            <div style="
                font-size: 1.7rem;
                font-weight: 700;
                color: #111827;
                margin-top: 0.2rem;
            ">{format_value(cat, item["value"])}</div>
            <div style="font-size: 0.78rem; color: {color}; margin-top: 0.25rem; font-weight: 600;">
                {arrow} {format_delta(cat, delta_abs)} <span style="color:#9ca3af; font-weight:400;">vs tahun sebelumnya</span>
            </div>
            <div style="font-size: 0.72rem; color: #6b7280; margin-top: 0.35rem; line-height: 1.35;">
                {CATEGORY_DESC[cat]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state() -> None:
    st.warning("Tidak ada data untuk rentang tahun yang dipilih. Coba perlebar rentang tahun atau klik Reset Filter.")


def build_insights(
    gdp_data, inflation_data, unemployment_data, population_data,
    start_year, end_year,
) -> list[str]:
    insights = []

    def latest_year(data):
        return data[-1]["year"] if data else None

    def first_year(data):
        return data[0]["year"] if data else None

    for label, data, unit in [
        ("GDP", gdp_data, "persen"),
        ("Inflasi", inflation_data, "persen"),
        ("Pengangguran", unemployment_data, "persen"),
        ("Populasi", population_data, "jiwa"),
    ]:
        if not data:
            continue
        current = data[-1]["value"]
        if len(data) >= 2:
            previous = data[-2]["value"]
            change = current - previous
            if unit == "jiwa":
                change_desc = f"{abs(change)/1_000_000:,.1f} juta"
            else:
                change_desc = f"{abs(change):,.2f} poin persentase"
            direction = "naik" if change > 0 else "turun"
            insights.append(
                f"{label} {direction} sebesar {change_desc} dibanding tahun sebelumnya "
                f"({data[-2]['year']} → {data[-1]['year']})."
            )

        max_point = max(data, key=lambda r: r["value"])
        min_point = min(data, key=lambda r: r["value"])
        if unit == "jiwa":
            max_str = f"{max_point['value']/1_000_000:,.1f} juta"
            min_str = f"{min_point['value']/1_000_000:,.1f} juta"
        else:
            max_str = f"{max_point['value']:,.2f}%"
            min_str = f"{min_point['value']:,.2f}%"
        insights.append(
            f"{label} tertinggi tercatat {max_str} pada {max_point['year']}, "
            f"terendah {min_str} pada {min_point['year']}."
        )

    return insights


# Load data bounds
try:
    min_year, max_year = get_year_bounds()
except Exception:
    st.error("Tidak dapat terhubung ke database. Pastikan pipeline sudah berjalan.")
    st.stop()

# Sidebar filters
st.sidebar.markdown("### 🔍 Filter Data")
year_range = st.sidebar.slider(
    "Rentang Tahun",
    min_year, max_year,
    (min_year, max_year),
    step=1,
)
start_year, end_year = year_range

selected_indicators = st.sidebar.multiselect(
    "Indikator",
    options=list(CATEGORY_LABELS.keys()),
    format_func=lambda c: CATEGORY_LABELS[c],
    default=list(CATEGORY_LABELS.keys()),
)

if st.sidebar.button("🔄 Reset Filter", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Sumber data: World Bank Open Data")

# Header
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #006071 0%, #007b8f 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    ">
        <h1 style="margin:0; font-size:1.9rem; font-weight:700;">📊 Dashboard Ekonomi Indonesia</h1>
        <p style="margin:0.5rem 0 0 0; opacity:0.9; font-size:0.95rem;">
            Memahami kondisi ekonomi Indonesia dalam angka yang mudah dibaca.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Active filter banner
st.markdown(
    f"""
    <div style="
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        border-radius: 8px;
        padding: 0.7rem 1rem;
        margin-bottom: 1.5rem;
        font-size: 0.9rem;
        color: #075985;
    ">
        <strong>Menampilkan data:</strong> {start_year} – {end_year}
        &nbsp;·&nbsp; Indikator: {', '.join([CATEGORY_LABELS[c] for c in selected_indicators]) or 'Tidak ada'}
    </div>
    """,
    unsafe_allow_html=True,
)

if not selected_indicators:
    st.info("Pilih minimal satu indikator di sidebar untuk melihat data.")
    st.stop()

# Load filtered data
gdp_data = get_gdp_trend(start_year, end_year) if "gdp" in selected_indicators else []
inflation_data = get_inflation_trend(start_year, end_year) if "inflation" in selected_indicators else []
unemployment_data = get_unemployment_trend(start_year, end_year) if "employment" in selected_indicators else []
population_data = get_population_trend(start_year, end_year) if "population" in selected_indicators else []

has_any_data = any([gdp_data, inflation_data, unemployment_data, population_data])

# Overview KPI cards
st.markdown("### 🎯 Ringkasan Terbaru")
st.markdown("Nilai terakhir pada tahun yang dipilih, dibandingkan tahun sebelumnya.")

if has_any_data:
    kpi_data = get_kpi_data(end_year)
    if kpi_data:
        kpi_data = [item for item in kpi_data if item["category"] in selected_indicators]
        if kpi_data:
            kpi_cols = st.columns(len(kpi_data))
            for col, item in zip(kpi_cols, kpi_data):
                with col:
                    render_kpi_card(item)
        else:
            render_empty_state()
    else:
        render_empty_state()
else:
    render_empty_state()

st.divider()

# Trends
st.markdown("### 📉 Perkembangan dari Waktu ke Waktu")
st.markdown("Bagaimana setiap indikator berubah sepanjang rentang tahun yang dipilih.")

chart_rows = []
if gdp_data:
    chart_rows.append(("gdp", gdp_data, "Pertumbuhan Ekonomi (GDP)", "GDP (%)"))
if inflation_data:
    chart_rows.append(("inflation", inflation_data, "Inflasi Tahunan", "Inflasi (%)"))
if unemployment_data:
    chart_rows.append(("employment", unemployment_data, "Tingkat Pengangguran", "Pengangguran (%)"))
if population_data:
    chart_rows.append(("population", population_data, "Jumlah Penduduk", "Penduduk (juta)"))

if chart_rows:
    for i in range(0, len(chart_rows), 2):
        cols = st.columns(2)
        batch = chart_rows[i:i+2]
        for col, (cat, data, title, ylabel) in zip(cols, batch):
            with col:
                if cat == "population":
                    pop_data = [{"year": r["year"], "value": r["value"] / 1_000_000} for r in data]
                    chart = build_bar_chart(pop_data, title, ylabel)
                else:
                    chart = build_line_chart(data, title, ylabel)
                st.plotly_chart(chart, use_container_width=True)
else:
    render_empty_state()

st.divider()

# Year-over-year change
st.markdown("### 🔄 Perubahan dari Tahun ke Tahun")
st.markdown("Batang hijau berarti naik, batang merah berarti turun dibanding tahun sebelumnya.")

yoy_items = []
if gdp_data:
    yoy_items.append(("gdp", get_year_over_year("gdp", start_year, end_year), "Perubahan Pertumbuhan Ekonomi"))
if inflation_data:
    yoy_items.append(("inflation", get_year_over_year("inflation", start_year, end_year), "Perubahan Inflasi"))

if yoy_items:
    yoy_cols = st.columns(len(yoy_items))
    for col, (cat, yoy_data, title) in zip(yoy_cols, yoy_items):
        with col:
            if yoy_data:
                st.plotly_chart(
                    build_yoy_chart(yoy_data, title),
                    use_container_width=True,
                )

st.divider()

# Correlation
if gdp_data and inflation_data:
    st.markdown("### 🔗 Hubungan GDP dan Inflasi")
    st.markdown("Setiap titik mewakili satu tahun, menunjukkan apakah pertumbuhan ekonomi dan inflasi bergerak bersama.")
    st.plotly_chart(
        build_scatter_correlation(
            gdp_data, inflation_data,
            "Hubungan Pertumbuhan Ekonomi dan Inflasi",
        ),
        use_container_width=True,
    )

st.divider()

# Automatic insights
insights = build_insights(
    gdp_data, inflation_data, unemployment_data, population_data,
    start_year, end_year,
)
if insights:
    st.markdown("### 💡 Apa Artinya?")
    st.markdown("Ringkasan otomatis dari data yang sedang ditampilkan.")
    for insight in insights[:8]:
        st.markdown(f"- {insight}")

st.divider()
st.caption("Sumber data: World Bank Open Data · Data bersifat tahunan (2000–2024) · Nilai 0% berarti data tidak tersedia pada tahun tersebut.")