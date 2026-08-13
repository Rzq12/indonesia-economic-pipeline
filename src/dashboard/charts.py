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
                  labels={"value": y_label, "year": "Tahun"},
                  markers=True)
    fig.update_traces(line_color=COLORS["primary"], marker=dict(size=6))
    return _base_layout(fig, title, y_label)


def build_bar_chart(data: List[dict], title: str, y_label: str) -> go.Figure:
    df = pd.DataFrame(data)
    fig = px.bar(df, x="year", y="value",
                 title=title,
                 labels={"value": y_label, "year": "Tahun"})
    fig.update_traces(marker_color=COLORS["secondary"])
    return _base_layout(fig, title, y_label)


def build_yoy_chart(data: List[dict], title: str) -> go.Figure:
    df = pd.DataFrame(data)
    fig = go.Figure()
    colors = ["#2ca02c" if (v is not None and v >= 0) else "#d62728" if v is not None else "#999999" for v in df["change"]]
    fig.add_trace(go.Bar(
        x=df["year"],
        y=df["change"],
        name="Perubahan (poin persentase)",
        marker_color=colors,
        text=[f"{v:+.2f}" if v is not None else "" for v in df["change"]],
        textposition="outside",
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="#999999")
    return _base_layout(fig, title, "Perubahan (poin persentase)")


def build_scatter_correlation(data_x: List[dict], data_y: List[dict], title: str) -> go.Figure:
    df_x = pd.DataFrame(data_x)
    df_y = pd.DataFrame(data_y)
    df = pd.merge(df_x, df_y, on="year", suffixes=("_x", "_y"))
    fig = px.scatter(df, x="value_x", y="value_y",
                     title=title,
                     labels={"value_x": "Pertumbuhan Ekonomi (%)", "value_y": "Inflasi (%)"})
    fig.update_traces(marker=dict(size=10, color=COLORS["primary"]))
    return _base_layout(fig, title, "Inflasi (%)")