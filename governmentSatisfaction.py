import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd

def govSatisfaction(special_dates):
    df_gov = pd.read_csv("govSatisfaction.csv", encoding="utf-8")
    fig = go.Figure(data=[
        go.Bar(name='Germany', x=df_gov["date"], y=df_gov["Germany"], opacity=0.85),
        go.Bar(name='USA', x=df_gov["date"], y=df_gov["United States"], opacity=0.85),
        go.Bar(name='United Kingdom', x=df_gov["date"], y=df_gov["United Kingdom"], opacity=0.85),
    ])
    fig.update_layout(
        height=1000,
        showlegend=True,
        title_text="Satisfaction with the national government's response to the COVID-19 / coronavirus pandemic in the United States, United Kingdom and Germany 2020 (as of May 24)",
        # margin=dict(l=10, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        mapbox_style="dark",
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#7f7f7f"
        ),
    )
    # UK providing 100,000 COVID-19 tests a day
    special_dates = special_dates.append({"date":'2020-05-01', "event": "UK providing 100,000 COVID-19 tests a day", "value":0, "type": 1}, ignore_index=True)
    special_dates = special_dates.sort_values(by=['date'])

    x1 = [d for d in special_dates['date'].values[4:12]]
    fig.add_trace(go.Scatter(x=x1, y=[0 for d in special_dates['date'].values[4:12]],
                             text=['{}'.format(i) for i in special_dates['event'].values[4:12]],
                             hovertemplate=
                             '<br>date: %{x}<br>' +
                             '<b>%{text}</b>',
                             mode='markers', name='events',
                             marker=dict(
                                 color='navy',
                                 size=15,
                                 line=dict(
                                     color='MediumPurple',
                                     width=1
                                 )))
                  )


    return fig
