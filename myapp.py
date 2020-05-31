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

app = dash.Dash(external_stylesheets=[
    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap-grid.min.css"])

df1 = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
df1['date'] = pd.to_datetime(df1['date'])
DATA = df1

df1uk = df1[df1['location'] == 'United Kingdom']
df1uk = df1uk.sort_values(by=['date'], ascending=False)
# United States
df1us = df1[df1['location'] == 'United States']
df1us = df1us.sort_values(by=['date'], ascending=False)

df1pl = df1[df1['location'] == 'Poland']
df1pl = df1pl.sort_values(by=['date'], ascending=False)
dfplus = df1pl.append(df1us)

SpecialDates = pd.read_csv('special_dates.csv', encoding="utf-8")

datadeaths = pd.read_csv('daths.csv', encoding="utf-8")

datadeaths.columns = ['week', 'nocov', 'all', 'cov']


def plot_map():
    px.set_mapbox_access_token(
        "pk.eyJ1IjoiYXdhcm5vIiwiYSI6ImNrOXB6cHAxZzBmajgzZXFjd2Q1YWI5ODkifQ.b49An9SsEpKsdIv9oy62ug")
    df = pd.read_csv('codes.csv')
    df['cases'] = pd.Series([136873, 4149, 13627, 11468])
    fig = px.scatter_mapbox(df, lat="lat", lon="long",
                            size="cases", size_max=50, zoom=4, hover_name='ctry19nm')
    fig.update_layout(
        margin=dict(l=10, r=0, t=0, b=0),
        width=350, height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        mapbox_style="dark",

    )
    return fig


def plot_map_eng(date='cases'):
    px.set_mapbox_access_token(
        "pk.eyJ1IjoiYXdhcm5vIiwiYSI6ImNrOXB6cHAxZzBmajgzZXFjd2Q1YWI5ODkifQ.b49An9SsEpKsdIv9oy62ug")
    df = pd.read_csv('codesEng.csv')
    df['cases'] = df[date]
    fig = px.scatter_mapbox(df, lat="lat", lon="long",
                            size="cases", size_max=50, zoom=4, hover_name='ctry19nm')
    fig.update_layout(
        margin=dict(l=10, r=0, t=0, b=0),
        width=350, height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        mapbox_style="dark",

    )
    return fig


def mini_plot(df, column):
    fig = px.bar(df, x='date', y=column, labels={'date': '', column: ''})
    # fig.add_trace(go.Scatter(x=df['date'], y=df[column], mode='lines'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        width=100, height=50,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
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
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return fig


def plot_distribution(df, df2, column='new_cases'):
    df_temp = df.append(df2)
    fig = px.bar(df_temp, x='date', y=column, color='location', barmode='group')
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        width=400, height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Courier New, monospace",
            size=12,
            color="#7f7f7f"
        )
    )
    return fig


def deaths_ratio(data):
    df = data.copy()
    df['nocov'] = [int(unidecode.unidecode(word).replace(' ', '')) for word in df['nocov'].values]
    df['all'] = [int(unidecode.unidecode(word).replace(' ', '')) for word in df['all'].values]
    df['cov'] = [int(unidecode.unidecode(word).replace(' ', '')) for word in df['cov'].values]
    df['diff'] = np.array(df['nocov']) - np.array(df['all'])
    weeks = df.week.values

    fig = go.Figure(data=[
        go.Bar(name='Other deaths', x=weeks, y=df['diff'].values.tolist(), opacity=0.7),
        go.Bar(name='Deaths connected with Covid-19', x=weeks, y=df['cov'].values.tolist(), opacity=0.85)

    ])
    # Change the bar mode

    fig.update_layout(barmode='stack')
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        width=700, height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Courier New, monospace",
            size=10,
            color="#7f7f7f"
        )
    )
    return fig


sign_dict = {'-': 'green', '+': 'red'}

mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=0, r=0, b=0, t=0),
    hovermode="closest",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
        mapbox_style="dark"
    ),
)

# Create app layout
app.layout = html.Div([
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
            ]
        ), className='box1'
    )
    ,
    dbc.Row([
        dbc.Col(
            html.Div(
                [html.H5("cases - map"),
                 html.Button('UK', id='uk_map', n_clicks=0),
                 html.Button('England', id='eng_map', n_clicks=0),
                 dcc.Graph(figure=plot_map(), id="map_graph"),
                 dcc.Slider(
                     id='date_slider',
                     min=0,
                     max=12,
                     value=2,
                     marks={
                         12: {'label': '05-10'},
                         11: {'label': '05-08'},
                         10: {'label': '05-06'},
                         9: {'label': '05-04'},
                         8: {'label': '04-28'},
                         7: {'label': '04-28'},
                         6: {'label': '04-12'},
                         5: {'label': '04-12'},
                         4: {'label': '03-29'},
                         3: {'label': '03-22'},
                         2: {'label': '03-15'},
                         1: {'label': '03-07'},
                         0: {'label': '02-29'},
                     }
                 )],

            ), width=3
        ),
        dbc.Col(
            html.Div(
                [dcc.DatePickerSingle(
                    id='single-date-picker-range',
                    min_date_allowed=df1uk.date.min(),
                    max_date_allowed=df1uk.date.max(),
                    initial_visible_month=df1uk.date.max(),
                    date=df1uk.date.max(), style={'background-color': 'red', 'color': 'red'}
                ),
                    html.Button('Predict', id='predict', n_clicks=0),
                    dcc.Graph(figure=predict_series(df1uk, str(dt.datetime.now()), SpecialDates, n=df1uk.shape[0]),
                              id="time_series_graph"),
                ],
                # className='mini_container'
            )

            , width={"size": 4, "offset": 1}),

        dbc.Col(
            html.Div(
                [dcc.Dropdown(
                    id='column-dropdown-distribution',
                    options=column_dropdown_options(),
                    value='total_cases_per_million'),
                    html.H5("cases - distribution"),
                    html.Button('Show', id='show2', n_clicks=0),
                    dcc.Graph(figure=plot_distribution(df1uk, dfplus), id="distribution_graph")],
            )
            , width={"size": 3, "offset": 1})],
        className="h-3"
    ),
    dbc.Row([
        dbc.Col(
            html.Div(
                [
                    dcc.Graph(figure=deaths_ratio(datadeaths), id="death_ratio_map_graph")],

            )
            , width=4),
        dbc.Col(
            html.Div(
                [
                    dcc.Graph(figure=pie_plot(), id="pie_graph"),
                    dcc.Slider(
                        id='date_slider2',
                        min=0,
                        max=12,
                        value=2,
                        marks={
                            12: {'label': '05-10'},
                            11: {'label': '05-08'},
                            10: {'label': '05-06'},
                            9: {'label': '05-04'},
                            8: {'label': '04-28'},
                            7: {'label': '04-28'},
                            6: {'label': '04-12'},
                            5: {'label': '04-12'},
                            4: {'label': '03-29'},
                            3: {'label': '03-22'},
                            2: {'label': '03-15'},
                            1: {'label': '03-07'},
                            0: {'label': '02-29'},
                        }
                    )
                ]
            ),
            # className='mini_container',
            width={"size": 3, "offset": 1}
        ),

        dbc.Col(
            html.Div(
                [dcc.Dropdown(
                    id='column-dropdown',
                    options=column_dropdown_options(),
                    value='total_cases_per_million'),
                    html.Button('Show', id='show', n_clicks=0),
                    dcc.Graph(figure=world_map_plot('total_cases_per_million', df1), id="world_map_graph")],
                # className='mini_container'

            ), width={"size": 3, "offset": 2}

        )

    ]),

], className='box1')


@app.callback(
    dash.dependencies.Output('time_series_graph', 'figure'),
    [dash.dependencies.Input('predict', 'n_clicks')],
    [dash.dependencies.State('single-date-picker-range', 'date')])
def update_output(n_clicks, date):
    return predict_series(df1uk, date, SpecialDates)


@app.callback(
    dash.dependencies.Output('world_map_graph', 'figure'),
    [dash.dependencies.Input('show', 'n_clicks')],
    [dash.dependencies.State('column-dropdown', 'value')])
def update_output1(n_clicks, value):
    print(value, 'VALUE')
    fig = world_map_plot(value, df1)
    return fig


@app.callback(dash.dependencies.Output('distribution_graph', 'figure'),
              [dash.dependencies.Input('show2', 'n_clicks')],
              [dash.dependencies.State('column-dropdown-distribution', 'value')])
def update_output1(n_clicks, value):
    print(value, 'VALUE distribution')
    fig = plot_distribution(df1uk, dfplus, value)
    return fig


# column-dropdown-distribution

dates = ["2020-02-29", "2020-03-07", "2020-03-15", "2020-03-22", "2020-03-29", "2020-04-04", "2020-04-12", "2020-04-20",
         "2020-04-28", "2020-05-04", "2020-05-06", "2020-05-08", "2020-05-10"]


@app.callback(dash.dependencies.Output('map_graph', 'figure'),
              [Input('uk_map', 'n_clicks'),
               Input('eng_map', 'n_clicks'),
               dash.dependencies.Input('date_slider', 'value')])
def changeMap(btn1, btn2, value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'uk_map' in changed_id:
        fig = plot_map()
    elif 'eng_map' in changed_id:
        print(value)
        print(changed_id)
        fig = plot_map_eng(dates[int(format(value))])
    else:
        print(changed_id)
        fig = plot_map_eng(dates[int(format(value))])
    return fig


@app.callback(dash.dependencies.Output('pie_graph', 'figure'),
              [dash.dependencies.Input('date_slider2', 'value')])
def pieChartUpdate(value):
    return pie_plot(dates[int(format(value))])


# Main
if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port='8050', debug=True)
