import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import re


def onlineShoppingTable():
    df_online = pd.read_csv("online_shopping.csv", encoding="utf-8")

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        specs=[[{"type": "table"}],
               [{"type": "bar"}],
               [{"type": "bar"}]]
    )

    fig.add_trace(
        go.Bar(
            x=df_online["Category"],
            y=df_online["United Kingdom"],
            name="Shifting to online shopping in UK"
        ),
        row=3, col=1
    )

    fig.add_trace(
        go.Bar(
            x=df_online["Category"],
            y=df_online["United States"],
            name="Shifting to online shopping in USA"
        ),
        row=2, col=1
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Category", "Germany", "United Kingdom", "United States"],
                font=dict(family="Courier New, monospace",
                          size=16,
                          color="white"),
                align="left",
                line_color='white',
                fill_color='rgb(99, 110, 250)',
            ),
            cells=dict(
                values=[df_online[k].tolist() for k in df_online.columns[0:]],
                align="left",
                font=dict(family="Courier New, monospace",
                          size=12,
                          color="white"),
                line_color='white',
                fill_color='rgb(101, 133, 194)'
            )
        ),
        row=1, col=1
    )
    fig.update_layout(
        height=1000,
        showlegend=True,
        title_text="Shifting to online shopping due to covid-19 closures",
    )
    fig.update_layout(
        # margin=dict(l=10, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        mapbox_style="dark",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#7f7f7f"
        )

    )

    return fig
