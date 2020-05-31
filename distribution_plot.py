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

# Multi-dropdown options
from controls import column_dropdown_options
from pie_plot import pie_plot
from world_map_plot import world_map_plot
from time_series import predict_series


def change_layout(fig, hidexax=True, name='new_cases'):
    if hidexax:
        xlabel = ''
    else:
        xlabel = 'date'
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        title=name.split('_')[0] + ' ' + name.split('_')[1],
        xaxis_title=xlabel,
        yaxis_title=name.split('_')[0] + ' ' + name.split('_')[1] ,
        width=500,
        height=150,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        mapbox_style="dark",
        font=dict(
            family="Courier New, monospace",
            size=8,
            color="#7f7f7f"
        )

    )

    if hidexax:
        fig.update_xaxes(
            showticklabels=False,
        )
    return fig


def general_statistics(df, countries=['France', 'Poland']):
    if type(countries) != type([0]):
        countries = [countries]

    countries = ['United Kingdom'] + countries
    print(countries)
    df_temp = df[df['location'].isin(countries)]
    df_temp = df_temp[df_temp['total_cases'] > 0]

    fig1 = px.bar(df_temp, x='date', y='new_cases', color='location', opacity=0.7)
    fig1 = change_layout(fig1, name='new_cases')

    fig2 = px.line(df_temp, x='date', y='total_cases', color='location')
    fig2 = change_layout(fig2, name='total_cases')

    fig3 = px.bar(df_temp, x='date', y='new_deaths', color='location')
    fig3 = change_layout(fig3, name='new_deaths')

    fig4 = px.line(df_temp, x='date', y='total_deaths', color='location')
    fig4 = change_layout(fig4, hidexax=False, name='total_deaths')

    return [fig1, fig2, fig3, fig4]
    
    
