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


codes = pd.read_csv('countrycodes.csv')
codes.columns = ['Country', 'c1', 'c2', 'num', 'long', 'lat']
iso_dict = {country: iso.split('"')[1] for country, iso in zip(codes.Country.values, codes.c2.values)}



def check_validity(country, column, df):
    datacountry = df[df['location'] == country]
    datacountry['date'] = pd.to_datetime(datacountry['date'])
    datacountry = datacountry.sort_values(by=['date'], ascending=False)
    datacountry = datacountry[datacountry['total_cases'] > 100]
    try:
        datatomodel = datacountry[[column]]
        datatomodel = datatomodel.dropna()

        if datatomodel.shape[0] > 20 and datatomodel.shape[1] > 0:
            datatomodel = datatomodel.head(20)
        else:
            datatomodel = pd.DataFrame()
    except:
        datatomodel = pd.DataFrame()

    return (datacountry.shape, datatomodel)


def world_map_plot(column, data):
    ukcurve = np.array(check_validity('United Kingdom', column, data)[1][column].tolist())
    ukcurve = savgol_filter(ukcurve, 5, 3)
    distances_from_uk_deaths = {}
    countries_list = data['location'].value_counts()
    countries_list = set(countries_list.index)

    for country in countries_list:
        res = check_validity(country, column, data)
        if res[1].empty:
            continue
        y = np.array(res[1][column].tolist())
        if y.shape[0] == 20:
            y = savgol_filter(y, 5, 3)
            distances_from_uk_deaths[country] = np.sqrt(np.mean((y - ukcurve) ** 2))

    df = pd.DataFrame.from_dict(distances_from_uk_deaths, orient='index').sort_values(by=[0], ascending=True)
    df['country'] = df.index.tolist()
    df['value'] = df[0]
    valid_countries = list(set(iso_dict).intersection(set(df['country'].values)))
    df = df[df.country.isin(valid_countries)]
    df['iso'] = [iso_dict[country] for country in df.country.values]

    fig = px.choropleth(df, locations="iso",
                        color="value")

    fig = go.Figure(data=go.Choropleth(
    locations=df['iso'], # Spatial coordinates
    z = df['value'], # Data to be color-coded
    colorscale = 'reds',
    reversescale=True,
    colorbar_title = "UK-distance",
    zmax=abs(df['value'].max()) * 0.4,
    zmin = 0,
    text=df["country"],
    ))

    fig.update_layout(
        title="Closeness to UK by the distribution (RMSE) of <br> " + column.replace('_', ' ') + ' last 20 days',

    )
    fig.update_geos(
    showcoastlines=True, coastlinecolor="firebrick",
    showland=False, landcolor="dodgerblue",
    showocean=True, oceancolor="#17191a",
    showlakes=False, lakecolor="Blue",
    showrivers=False, rivercolor="Blue"
)

    fig.update_xaxes(
    showticklabels=False,
    showgrid=False,
    zeroline=False,
)

    fig.update_yaxes(
    showticklabels=False,
    showgrid=False,
    zeroline=False,
)

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=30),
        #width=500, 
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    font=dict(
        family="Courier New, monospace",
        size=10,
        color="#7f7f7f"
    )
    )
    fig.update_layout(showlegend=False)
    return fig
