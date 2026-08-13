import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List

COLORS = {
    "gdp": "#1f77b4",
    "inflation": "#ff7f0e",
    "employment": "#2ca02c",
    "population": "#d62728",
    "primary": "#006071",
    "secondary": "#007b8f",
    "background": "white",
    "grid": "#f0f0f0",
}

def _base_layout(fig: go.Figure, title: str, y_label: str) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color="#333333")),
        plot_bgcolor=COLORS["background"],
        paper_bgcolor=COLORS["background"],
        font=dict(family="Inter, sans-serif", size=12),
        hovermode="x unified",
        margin=dict(t=50, b=30, l=40, r=20),
        xaxis=dict(gridcolor=COLORS["grid"]),
        yaxis=dict(gridcolor=COLORS["grid"], title=y_label),
    )
    return fig


def build_line_chart(data: List[dict], title: str, y_label: str) -> go.Figure:
    df = pd.DataFrame(data)
    fig = px.line(df, x="year", y="value",
                  title=title,
                  labels={"value": y_label, "year": "Year"},
                  markers=True)
    fig.update_traces(line_color=COLORS["primary"], marker=dict(size=6))
    return _base_layout(fig, title, y_label)


def build_bar_chart(data: List[dict], title: str, y_label: str) -> go.Figure:
    df = pd.DataFrame(data)
    fig = px.bar(df, x="year", y="value",
                 title=title,
                 labels={"value": y_label, "year": "Year"})
    fig.update_traces(marker_color=COLORS["secondary"])
    return _base_layout(fig, title, y_label)


def build_area_chart(data: List[dict], title: str, y_label: str) -> go.Figure:
    df = pd.DataFrame(data)
    fig = px.area(df, x="year", y="value",
                  title=title,
                  labels={"value": y_label, "year": "Year"},
                  color_discrete_sequence=[COLORS["secondary"]])
    fig.update_traces(fill="tozeroy", opacity=0.3)
    return _base_layout(fig, title, y_label)


def build_multi_line_chart(data_dict: dict[str, List[dict]], title: str) -> go.Figure:
    fig = go.Figure()
    for name, data in data_dict.items():
        df = pd.DataFrame(data)
        fig.add_trace(go.Scatter(
            x=df["year"],
            y=df["value"],
            mode="lines+markers",
            name=name,
            line=dict(width=2),
            marker=dict(size=5),
        ))
    return _base_layout(fig, title, "Value")


def build_yoy_chart(data: List[dict], title: str) -> go.Figure:
    df = pd.DataFrame(data)
    fig = go.Figure()
    colors = ["#2ca02c" if (v is not None and v >= 0) else "#d62728" if v is not None else "#999999" for v in df["yoy_pct"]]
    fig.add_trace(go.Bar(
        x=df["year"],
        y=df["yoy_pct"],
        name="YoY Change (%)",
        marker_color=colors,
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="#999999")
    return _base_layout(fig, title, "YoY Change (%)")


def build_kpi_card(title: str, value: str, delta: str, delta_color: str) -> None:
    """Streamlit metric card - placeholder for Streamlit native st.metric"""
    pass


def build_comparison_chart(categories: List[str], values: List[float], title: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=COLORS["secondary"],
        text=[f"{v:.2f}%" for v in values],
        textposition="outside",
    ))
    return _base_layout(fig, title, "Value (%)")


def build_scatter_correlation(data_x: List[dict], data_y: List[dict], title: str) -> go.Figure:
    df_x = pd.DataFrame(data_x)
    df_y = pd.DataFrame(data_y)
    df = pd.merge(df_x, df_y, on="year", suffixes=("_x", "_y"))
    fig = px.scatter(df, x="value_x", y="value_y",
                     title=title,
                     labels={"value_x": "GDP Growth (%)", "value_y": "Inflation (%)"})
    fig.update_traces(marker=dict(size=10, color=COLORS["primary"]))
    return _base_layout(fig, title, "Inflation (%)")