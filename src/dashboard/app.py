import streamlit as st
import pandas as pd
from src.dashboard.queries import (
    get_inflation_trend, get_gdp_trend, get_unemployment_trend,
    get_population_trend, get_summary_stats, get_latest_values,
    get_year_over_year, get_indicator_categories
)
from src.dashboard.charts import (
    build_line_chart, build_bar_chart, build_area_chart,
    build_multi_line_chart, build_yoy_chart, build_scatter_correlation
)

st.set_page_config(
    page_title="Indonesia Economic Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #006071 0%, #007b8f 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 0.9rem;
    }
    .kpi-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #006071;
    }
    .kpi-delta {
        font-size: 0.8rem;
        color: #2ca02c;
    }
    .section-divider {
        border-top: 1px solid #e0e0e0;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🇮🇩 Indonesia Economic Data Pipeline</h1>
    <p>ETL Pipeline + Data Warehouse — World Bank Open Data · 2000–2024</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Filters")
years = list(range(2000, 2025))
year_range = st.sidebar.slider("Year Range", 2000, 2024, (2000, 2024))
selected_indicator = st.sidebar.selectbox(
    "Indicator", ["All", "GDP Growth", "Inflation", "Unemployment", "Population"]
)
st.sidebar.divider()
st.sidebar.caption("Data source: World Bank Open Data")

# Latest Values (KPI Cards)
st.subheader(f"Latest Values ({year_range[1]})")
latest = get_latest_values()
if latest:
    kpi_cols = st.columns(len(latest))
    for i, item in enumerate(latest):
        with kpi_cols[i]:
            category = item["category"]
            if category == "population":
                value_str = f"{item['value']/1e6:.1f}M"
            else:
                value_str = f"{item['value']:.2f}%"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{item['name']}</div>
                <div class="kpi-value">{value_str}</div>
                <div class="kpi-delta">Latest: {item['year']}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No data yet. Run the ETL pipeline first.")

st.divider()

# Main Charts
st.subheader("Economic Indicators")
col1, col2 = st.columns(2)

show_gdp = selected_indicator in ["All", "GDP Growth"]
show_inflation = selected_indicator in ["All", "Inflation"]
show_unemployment = selected_indicator in ["All", "Unemployment"]
show_population = selected_indicator in ["All", "Population"]

with col1:
    if show_gdp:
        data = get_gdp_trend()
        if data:
            st.plotly_chart(
                build_line_chart(data, "GDP Growth (%)", "GDP Growth (%)"),
                use_container_width=True,
            )
        else:
            st.info("No data yet. Run the ETL pipeline first.")
    else:
        st.info("Indicator filtered out")

with col2:
    if show_inflation:
        data = get_inflation_trend()
        if data:
            st.plotly_chart(
                build_line_chart(data, "Inflation Rate (%)", "Inflation (%)"),
                use_container_width=True,
            )
        else:
            st.info("No data yet. Run the ETL pipeline first.")
    else:
        st.info("Indicator filtered out")

col3, col4 = st.columns(2)

with col3:
    if show_unemployment:
        data = get_unemployment_trend()
        if data:
            st.plotly_chart(
                build_area_chart(data, "Unemployment Rate (%)", "Unemployment (%)"),
                use_container_width=True,
            )
        else:
            st.info("No data yet. Run the ETL pipeline first.")
    else:
        st.info("Indicator filtered out")

with col4:
    if show_population:
        data = get_population_trend()
        if data:
            st.plotly_chart(
                build_bar_chart(data, "Population (Millions)", "Population (M)"),
                use_container_width=True,
            )
        else:
            st.info("No data yet. Run the ETL pipeline first.")
    else:
        st.info("Indicator filtered out")

st.divider()

# Year-over-Year Analysis
st.subheader("Year-over-Year Change Analysis")
yoy_cols = st.columns(2)

with yoy_cols[0]:
    yoy_data = get_year_over_year("gdp")
    if yoy_data:
        st.plotly_chart(
            build_yoy_chart(yoy_data, "GDP YoY Change (%)"),
            use_container_width=True,
        )

with yoy_cols[1]:
    yoy_data = get_year_over_year("inflation")
    if yoy_data:
        st.plotly_chart(
            build_yoy_chart(yoy_data, "Inflation YoY Change (%)"),
            use_container_width=True,
        )

st.divider()

# Correlation Analysis
st.subheader("GDP vs Inflation Correlation")
gdp_data = get_gdp_trend()
inflation_data = get_inflation_trend()
if gdp_data and inflation_data:
    st.plotly_chart(
        build_scatter_correlation(gdp_data, inflation_data, "GDP Growth vs Inflation"),
        use_container_width=True,
    )

st.divider()
st.caption("Data source: World Bank Open Data · Pipeline: Prefect · Warehouse: PostgreSQL")