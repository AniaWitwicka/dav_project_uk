# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
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

app2 = dash.Dash(external_stylesheets=[
    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap-grid.min.css"])

df1 = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
df1['date'] = pd.to_datetime(df1['date'])
DATA = df1

df1uk = df1[df1['location'] == 'United Kingdom']
df1uk = df1uk.sort_values(by=['date'], ascending=False)

nav = dbc.Nav(
    [dbc.NavItem(dbc.NavLink("Total Cases", active=True, href="#")),
     dbc.NavItem(dbc.NavLink("Predictions", active=True, href="#")),
     dbc.NavItem(dbc.NavLink("Deaths", active=True, href="#")),
     dbc.NavItem(dbc.NavLink("Worldwide Covid", active=True, href="#"))],
    fill=True)

app2.layout = html.Div([
    html.Div(
        dbc.Row(
            [dbc.Col(
                html.Div(
                    [
                        html.Img(
                            src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Flag_of_the_United_Kingdom_%283-5%29.svg/1280px-Flag_of_the_United_Kingdom_%283-5%29.svg.png",
                            style={
                                "height": "70px",
                                "width": "auto",
                            },
                        ),

                    ],

                ), width=2),
                dbc.Col(
                    dbc.Row(
                        [
                            dbc.Row(html.H1(
                                "Coronavirus - UK " + '(' + str(date.today()) + ')',
                            ),
                            ),
                        ]
                    ), width=3),

                dbc.Col(
                    html.Div(
                        [html.H6(df1uk.iloc[0]['total_cases']),
                         html.P('+' + str(df1uk.iloc[0]['total_cases'] - df1uk.iloc[1]['total_cases']),
                                style={'color': 'red'}), html.P("Total cases"),
                         ],

                        className='box1'
                    ),
                    width=2,
                ),

                dbc.Col(
                    html.Div(
                        [html.H6(df1uk.iloc[0]['total_deaths']),
                         html.P('+' + str(df1uk.iloc[0]['total_deaths'] - df1uk.iloc[1]['total_deaths']),
                                style={'color': 'red'}), html.P("Total deaths")],
                        className='box1'
                    ),
                    width=2),

                dbc.Col(
                    html.Div(
                        html.Div(
                            [html.H6(round(df1uk.iloc[0]['total_cases_per_million'])), html.P('+' + str(
                                round(df1uk.iloc[0]['total_cases_per_million'] - df1uk.iloc[1][
                                    'total_cases_per_million'])), style={'color': 'red'}),
                             html.P("total cases per million")],
                            className='box1'
                        ),
                    ), width=2),
            ])),
    html.Div(
        dbc.Row(
            [dbc.Col(
                html.Div(
                    html.Div(
                        [dbc.NavItem(dbc.NavLink("Total Cases", active=True, href="#",
                                                 style={'font-family': 'monospace'}))]
                    ), className='box1'
                ), width=3),

                dbc.Col(
                    html.Div(
                        html.Div(
                            [dbc.NavItem(dbc.NavLink("Deaths", active=True, href="#",
                                                     style={'font-family': 'monospace'}))]
                        ), className='box1'
                    ), width=3),
                dbc.Col(
                    html.Div(
                        html.Div(
                            [dbc.NavItem(dbc.NavLink("Worldwide Covid", active=True, href="#",
                                                     style={'font-family': 'monospace'}))]
                        ), className='box1'
                    ), width=3),

                dbc.Col(
                    html.Div(
                        html.Div(
                            [dbc.NavItem(dbc.NavLink("Predictions", active=True, href="#",
                                                     style={'font-family': 'monospace'}))]
                        ), className='box1'
                    ), width=2),
            ]
        )
    )
])

if __name__ == "__main__":
    app2.run_server(host='127.0.0.1', port='8000', debug=True)
