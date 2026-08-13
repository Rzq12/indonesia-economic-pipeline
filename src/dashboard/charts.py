import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List


def build_line_chart(data: List[dict], title: str, y_label: str) -> go.Figure:
    df = pd.DataFrame(data)
    fig = px.line(df, x="year", y="value",
                  title=title,
                  labels={"value": y_label, "year": "Year"},
                  markers=True)
    fig.update_traces(line_color="#006071", marker=dict(size=6))
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
        hovermode="x unified",
    )
    return fig


def build_bar_chart(data: List[dict], title: str, y_label: str) -> go.Figure:
    df = pd.DataFrame(data)
    fig = px.bar(df, x="year", y="value",
                 title=title,
                 labels={"value": y_label, "year": "Year"})
    fig.update_traces(marker_color="#007b8f")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif"),
    )
    return fig