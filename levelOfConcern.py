import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd


def levelOfConcern():
    df1 = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
    df1['date'] = pd.to_datetime(df1['date'])
    df1uk = df1[df1['location'] == 'United Kingdom']
    df1uk = df1uk.sort_values(by=['date'], ascending=False)

    df_con = pd.read_csv("levelOfConcern.csv", encoding="utf-8")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_con["date"], y=df_con["United Kingdom"],
                             mode='lines',
                             name='Level of concern'), secondary_y=True)
    fig.add_trace(
        go.Bar(name='United Kingdom new cases', x=df1uk[df1uk.date >= '2020-03-24']["date"], y=df1uk["new_cases"],
               opacity=0.60),)
    fig.add_trace(
        go.Bar(name='United Kingdom new deaths', x=df1uk[df1uk.date >= '2020-03-24']["date"], y=df1uk["new_deaths"],
               opacity=0.60),)
    fig.add_trace(
        go.Bar(name='United Kingdom total deaths', x=df1uk[df1uk.date >= '2020-03-24']["date"], y=df1uk["total_deaths"],
               opacity=0.60),)
    fig.add_trace(
        go.Bar(name='United Kingdom total cases', x=df1uk[df1uk.date >= '2020-03-24']["date"], y=df1uk["total_cases"],
               opacity=0.60),
    )

    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Daily new cases in UK", secondary_y=False)
    fig.update_yaxes(title_text="Level of Concern (from 0 to 10)", secondary_y=True)

    fig.update_layout(
        height=1000,
        showlegend=True,
        title_text="Level of concern about the COVID-19 / coronavirus pandemic in the United States, United Kingdom and Germany 2020 (as of May 28)",
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

    return fig
