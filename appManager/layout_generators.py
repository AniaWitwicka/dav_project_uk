# Import required libraries
import datetime as dt

import dash_core_components as dcc
import dash_html_components as html
import numpy as np

import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import unidecode
import dash_bootstrap_components as dbc
from chartScripts.distribution_plot import general_statistics
from chartScripts.levelOfConcern import levelOfConcern
from chartScripts.tables import onlineShoppingTable
from chartScripts.governmentSatisfaction import govSatisfaction
from chartScripts.world_map_plot import world_map_plot
from chartScripts.time_series import predict_series
from appManager.controls import column_dropdown_options

'''Importing plots'''
from chartScripts.pie_plot import pie_plot


'''Navbar features'''
NAVBAR_NAMES = ['Basic statistics', 'Curiosities', 'Analytics']
NAVBAR_IDS = ['navbar' + str(i)  for i in range(len(NAVBAR_NAMES))]
NAVBAR_CLASSES = ['box1' for _ in range(len(NAVBAR_NAMES))]


def navbar(names=NAVBAR_NAMES, ids=NAVBAR_IDS, classes=NAVBAR_CLASSES):
    layout = []
    for name, idname, classname in zip(names, ids, classes):
        navitem = html.Button(name, id=idname)
        layout.append(navitem)
    return layout


def statistics_column(df, countries=['France', 'Poland']):
    figures = general_statistics(df, countries=countries)
    stats = []
    for i, figure in enumerate(figures):
        plot = dcc.Graph(figure=figure, id='stats' + str(i))
        stats.append(plot)
    return html.Div(children=stats, id='base_stats')


def plot_map():
    px.set_mapbox_access_token(
        "pk.eyJ1IjoiYXdhcm5vIiwiYSI6ImNrOXB6cHAxZzBmajgzZXFjd2Q1YWI5ODkifQ.b49An9SsEpKsdIv9oy62ug")
    df = pd.read_csv('datasets/codes.csv')
    df['cases'] = pd.Series([136873, 4149, 13627, 11468])
    fig = px.scatter_mapbox(df, lat="lat", lon="long",
                            size="cases", size_max=50, zoom=4, hover_name='ctry19nm')
    fig.update_layout(
        margin=dict(l=0, r=0, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        mapbox_style="dark",
        width=650, height=550,

    )
    return fig


def plot_map_eng(date='cases'):
    px.set_mapbox_access_token(
        "pk.eyJ1IjoiYXdhcm5vIiwiYSI6ImNrOXB6cHAxZzBmajgzZXFjd2Q1YWI5ODkifQ.b49An9SsEpKsdIv9oy62ug")
    df = pd.read_csv('datasets/codesEng.csv')
    df['cases'] = df[date]
    fig = px.scatter_mapbox(df, lat="lat", lon="long",
                            size="cases", size_max=50, zoom=4, hover_name='ctry19nm')
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        #width=200, height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        mapbox_style="dark",

    )
    return fig

def deaths_ratio(data):
    df = data.copy()
    df['nocov'] = [int(unidecode.unidecode(word).replace(' ', '')) for word in df['nocov'].values]
    df['all'] = [int(unidecode.unidecode(word).replace(' ', '')) for word in df['all'].values]
    df['cov'] = [int(unidecode.unidecode(word).replace(' ', '')) for word in df['cov'].values]
    df['diff'] = np.array(df['nocov']) - np.array(df['all'])
    weeks = df.week.values
    weeks = ['w' + w.split(' ')[1] for w in weeks]

    fig = go.Figure(data=[
        go.Bar(name='Other deaths', x=weeks, y=df['diff'].values.tolist(), opacity=0.7),
        go.Bar(name='Deaths connected with Covid-19', x=weeks, y=df['cov'].values.tolist(), opacity=0.85)

    ])
    # Change the bar mode

    fig.update_layout(barmode='stack')
    fig.update_xaxes(title_text="week")
    fig.update_layout(
        title_text="Deaths connected with Covid-19",
        margin=dict(l=10, r=10, t=40, b=40),
        #width=700,
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="Courier New, monospace",
            size=10,
            color="#7f7f7f"
        )
    )
    return fig


def first_page_second_column():
    col = dbc.Col([html.Div([
        html.H6('Cases by region'),
        html.Div(
            [
                dcc.Graph(figure=pie_plot(), id="pie_graph", style={"height": 600}),
                dcc.Slider(
                    id='date_slider2',
                    min=0,
                    max=4,
                    value=2,
                    marks={
                        4: {'label': '05-10'},
                        3: {'label': '05-04'},
                        2: {'label': '04-12'},
                        1: {'label': '03-22'},
                        0: {'label': '02-29'},
                    }
                )
            ]
        )], style={"align": 'center'}, className='box1')], width=2
    )
    return col


def first_page_third_column():
    col = dbc.Col(
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
                     0: {'label': '02-29'},
                 }
             )],

        ), width=5
    )
    return col

'''First page generator '''
def firstpage(df):
    countries = set(df.location.values)
    countries_selector = dcc.Dropdown(
    options=[{'label': country, 'value': country} for country in countries],
    multi=True,
    value="United Kingdom",
    id="countries_selector"
)
    stats_title = html.H5('Basic Statistics')

    statistics_col = dbc.Col([html.Div([stats_title,countries_selector, statistics_column(df)] , className='box1')]  , width=4)

    second_col = first_page_second_column()
    third_col = first_page_third_column()
    content = dbc.Row([statistics_col, second_col, third_col])
    content = html.Div(content, className='box1')
    return content



'''Second page generator '''
def secondpage(df, datadeaths):
    fig1 = dcc.Graph(figure=deaths_ratio(datadeaths), id="death_ratio_map_graph")
    fig2 = dcc.Graph(figure=levelOfConcern(), id="concerns_and_satisfaction")
    fig3 = dcc.Graph(figure=onlineShoppingTable(), id="online_shopping")
    fig4 = dcc.Graph(figure=govSatisfaction(), id="gov_satisfaction")
    countries = set(df.location.values)
    countries_selector = dcc.Dropdown(
    options=[{'label': country, 'value': country} for country in countries],
    multi=True,
    value="United Kingdom",
    id="countries_selector"
)
    stats_title = html.H5('Curiosities')

    statistics_col = dbc.Col([html.Div([stats_title,countries_selector, statistics_column(df)] , className='box1')]  , width=6)

    second_col = first_page_second_column()
    third_col = first_page_third_column()

    mode_selector = dcc.RadioItems(
        options=[
            {'label': 'concerns', 'value': 'concerns'},
            {'label': 'satisfaction', 'value': 'government satisfaction'},
        ],
        value='concerns',
        labelStyle={'display': 'inline-block'},
        id='concerns_satisfaction'
    )
    col1 = dbc.Col(html.Div([fig1, mode_selector, fig2], className='box1'), width=6)
    col2 = dbc.Col(fig3)
    content = dbc.Row([col1, col2])
    return content


def thirdpage(df, df1uk, SpecialDates):
        col1 =  dbc.Col(
            html.Div(
                [html.H6('Time series prediction'),
                 dcc.DatePickerSingle(
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
            ), className='box1'

            , width=6)
        col2 = dbc.Col(
            html.Div(
                [html.H6('Similar countries'),
                 dcc.Dropdown(
                    id='column-dropdown',
                    options=column_dropdown_options(),
                    value='total_cases_per_million'),
                    html.Button('Show', id='show', n_clicks=0),
                    dcc.Graph(figure=world_map_plot('total_cases_per_million', df), id="world_map_graph")],
                # className='mini_container'

            ) ,width=6

        )
        content = dbc.Row([col1, col2])
        return content



