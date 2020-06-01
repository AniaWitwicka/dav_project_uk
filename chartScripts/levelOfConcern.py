import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d


def levelOfConcern(mode='total_cases'):
    df1 = pd.read_csv('datasets/owid-covid-data.csv')
    df1['date'] = pd.to_datetime(df1['date'])
    df1uk = df1[df1['location'] == 'United Kingdom']
    #df1uk = df1uk.iloc[:-4:4]
    df1uk = df1uk.sort_values(by=['date'], ascending=False)

    df_con = pd.read_csv("datasets/levelOfConcern.csv", encoding="utf-8")

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=df_con["date"], y=df_con["United Kingdom"],
                             mode='lines',
                             name='Level of concern'), secondary_y=True)


    fig.add_trace(go.Scatter(x=df_con["date"], y=gaussian_filter1d(np.array(df_con["United Kingdom"].values), sigma=3),
                             mode='lines',
                             name='Smoothed level of concern', marker_color='#2ca02c'), secondary_y=True)


    fig.add_trace(
        go.Bar(name='United Kingdom' +  mode.split('_')[0] + ' ' + mode.split('_')[1], x=df1uk[df1uk.date >= '2020-03-24']["date"], y=df1uk[mode],
               opacity=0.90, marker_color='#ce4c36'))




    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Daily new cases in UK", secondary_y=False)
    fig.update_yaxes(title_text="Level of Concern (from 0 to 10)", range=[5, 10], secondary_y=True)
 
    fig.update_layout(
        height=400,
        showlegend=True,
        title_text="Level of concern about the COVID-19",
        margin=dict(l=20, r=10, t=40, b=10),
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
