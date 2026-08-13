import streamlit as st
from src.dashboard.queries import get_inflation_trend, get_gdp_trend, get_summary_stats
from src.dashboard.charts import build_line_chart, build_bar_chart

st.set_page_config(
    page_title="Indonesia Economic Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("🇮🇩 Indonesia Economic Data Pipeline")
st.caption("ETL Pipeline + Data Warehouse — World Bank Open Data")

# Summary Stats
st.subheader("Data Summary")
stats = get_summary_stats()
if stats:
    cols = st.columns(len(stats))
    for i, stat in enumerate(stats):
        with cols[i]:
            st.metric(
                label=stat["indicator_name"],
                value=f"{stat['avg_value']}%",
                delta=f"{stat['records']} records",
            )

# Charts
col1, col2 = st.columns(2)

with col1:
    data = get_inflation_trend()
    if data:
        st.plotly_chart(
            build_line_chart(data, "Indonesia Inflation Rate (%)", "Inflation (%)"),
            use_container_width=True,
        )
    else:
        st.info("No data yet. Run the ETL pipeline first.")

with col2:
    data = get_gdp_trend()
    if data:
        st.plotly_chart(
            build_bar_chart(data, "Indonesia GDP Growth (%)", "GDP Growth (%)"),
            use_container_width=True,
        )
    else:
        st.info("No data yet. Run the ETL pipeline first.")

st.divider()
st.caption("Data source: World Bank Open Data · Pipeline: Prefect · Warehouse: PostgreSQL")