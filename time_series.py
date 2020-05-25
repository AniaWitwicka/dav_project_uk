# Import required libraries
import dash
import datetime as dt
from datetime import date, datetime

import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from dateutil.relativedelta import relativedelta
import numpy as np
import random

import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from fbprophet import Prophet
import datetime
from scipy.signal import savgol_filter
import unidecode
import dash_bootstrap_components as dbc 


def plot_time_series(df, special_dates):
    fig = px.scatter(special_dates, x="date", y="value", hover_name="event")
    fig.update_layout(hovermode="x unified")
    fig2 = px.line(df, x='date', y='total_cases', title='Time Series -coronavirus UK', hover_name="total_cases")
    fig.add_trace(fig2.data[0])
    fig.update_layout(hovermode="x unified")
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(
        margin=dict(l=10, r=0, t=0, b=0),
        width=500, height=200,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig




def predict_series(df, date, special_dates, n=100):
    testdf = df.copy()
    date = date[:10]
    date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    n = [i for i, d in enumerate(df.date) if d > date_time_obj]
    if not n:
        n = df.shape[0]
    else:
        n = df.shape[0] - n[-1]
    series = pd.DataFrame({'ds': df.date.values, 'y': df.total_cases.values})
    series_train = series.tail(n).copy()
    m = Prophet()
    m.fit(series_train)
    future = m.make_future_dataframe(periods=df.shape[0] - n + 20)
    future.tail()

    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(df.shape[0] - n + 6 + 20)

    x = [pd.Timestamp(d, tz=None).to_pydatetime() for d in series['ds'].values]
    x1 = [pd.Timestamp(d, tz=None).to_pydatetime() for d in special_dates['date'].values]
    x2 = [pd.Timestamp(d, tz=None).to_pydatetime() for d in forecast['ds'].values]
    x3 = [pd.Timestamp(d, tz=None).to_pydatetime() for d in testdf['date'].values]
    trace1 = go.Scatter(x=x1, y=special_dates['value'].values,
                        text=['{}'.format(i) for i in special_dates['event'].values],
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

    trace2 = go.Scatter(x=x, y=series['y'].values, mode='lines', name='original', line=dict(color='dodgerblue', width=4), opacity=0.5)

    trace3 = go.Scatter(x=x2, y=forecast['yhat'].values, mode='lines',
                        name='predicted', line=dict(color='firebrick', width=3, dash='dash'), opacity=0.7)
    trace4 = go.Scatter(x=x3, y=testdf['total_tests'].values, mode='lines', name='original', line=dict(color='green', width=3))

    fig = go.Figure()
    fig.add_trace(trace2)
    fig.add_trace(trace3)
    #fig.add_trace(trace4)
    fig.add_trace(trace1)
    fig.update_layout(
        title="Prediction from " + date)

    fig.update_layout(xaxis_range=[datetime.datetime(2020, 1, 1),
                                   datetime.datetime(2020, 6, 1)],
                      xaxis={'type': 'date'},
                      )

    fig.update_layout(hovermode='x unified')
    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=30),
        width=600, height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family="Courier New, monospace",
        size=10,
        color="#7f7f7f",
    ))

    fig.update_xaxes(
    showgrid=False,
)
    
    return fig




