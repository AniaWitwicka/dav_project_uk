# Import required libraries
import dash
from datetime import date

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import dash_bootstrap_components as dbc

from layout_generators import navbar, firstpage, statistics_column, plot_map, plot_map_eng, secondpage, thirdpage
from chartScripts.pie_plot import pie_plot
from chartScripts.levelOfConcern import levelOfConcern
from chartScripts.governmentSatisfaction import govSatisfaction
from chartScripts.world_map_plot import world_map_plot
from chartScripts.time_series import predict_series

app2 = dash.Dash(suppress_callback_exceptions=True, external_stylesheets=[
    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap-grid.min.css"])

datadeaths = pd.read_csv('datasets/daths.csv', encoding="utf-8")

datadeaths.columns = ['week', 'nocov', 'all', 'cov']
SpecialDates = pd.read_csv('datasets/special_dates.csv', encoding="utf-8")
'''data'''
df = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')

df1 = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
df1['date'] = pd.to_datetime(df1['date'])
DATA = df1

df1uk = df1[df1['location'] == 'United Kingdom']
df1uk = df1uk.sort_values(by=['date'], ascending=False)

app2.layout = html.Div([
    dcc.Location(id='url', refresh=False),
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
                            dbc.Row(html.H2(
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
        dbc.Row(html.Div(navbar(), className='box1')
        )
    ),
    html.Div(firstpage(df), id='page-content', className='box1',

             )
])

'''Calbacks'''


@app2.callback(
    Output(component_id='base_stats', component_property='children'),
    [Input(component_id='countries_selector', component_property='value')],
)
def update_output_div(value):
    return statistics_column(df, countries=value)


@app2.callback(
    Output(component_id='page-content', component_property='children'),
    [Input('navbar0', 'n_clicks_timestamp'), Input('navbar1', 'n_clicks_timestamp'), Input('navbar2', 'n_clicks_timestamp')],
)
def update_output_div1(time1, time2, time3):
    if not time1 and not time2 and not time3:
        raise dash.exceptions.PreventUpdate
    if not time1:
        time1 = 0
    if not time2:
        time2 = 0
    if not time3:
        time3 = 0

    if time1 > time2 and time1 > time3:
        return firstpage(df)
    elif time2 > time1 and time2 > time3:
        return secondpage(df, datadeaths)
    else:
        return thirdpage(df1, df1uk, SpecialDates)



# column-dropdown-distribution

dates = ["2020-02-29", "2020-03-07", "2020-03-15", "2020-03-22", "2020-03-29", "2020-04-04", "2020-04-12", "2020-04-20",
         "2020-04-28", "2020-05-04", "2020-05-06", "2020-05-08", "2020-05-10"]


@app2.callback(dash.dependencies.Output('map_graph', 'figure'),
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


@app2.callback(dash.dependencies.Output('pie_graph', 'figure'),
              [dash.dependencies.Input('date_slider2', 'value')])
def pieChartUpdate(value):
    return pie_plot(dates[int(format(value))])



@app2.callback(dash.dependencies.Output('concerns_and_satisfaction', 'figure'),
              [dash.dependencies.Input('concerns_satisfaction', 'value')])
def pieChartUpdate(value):
    if value == 'concerns':
        return levelOfConcern()
    else:
        return govSatisfaction()

@app2.callback(
    dash.dependencies.Output('time_series_graph', 'figure'),
    [dash.dependencies.Input('predict', 'n_clicks')],
    [dash.dependencies.State('single-date-picker-range', 'date')])
def update_output(n_clicks, date):
    return predict_series(df1uk, date, SpecialDates)


@app2.callback(
    dash.dependencies.Output('world_map_graph', 'figure'),
    [dash.dependencies.Input('show', 'n_clicks')],
    [dash.dependencies.State('column-dropdown', 'value')])
def update_output1(n_clicks, value):
    print(value, 'VALUE')
    fig = world_map_plot(value, df1)
    return fig


white_button_style = {'background-color': 'transparent'}

red_button_style = {'background-color': '#76b4e3'}

#
@app2.callback(Output('navbar0', 'style'),
              [Input('navbar0', 'n_clicks_timestamp'), Input('navbar1', 'n_clicks_timestamp'), Input('navbar2', 'n_clicks_timestamp')])
def change_button_style(time1, time2, time3):
    if not time1 and not time2 and not time3:
        return red_button_style
    if not time1:
        time1 = 0
    if not time2:
        time2 = 0
    if not time3:
        time3 = 0

    if time1 > time2 and time1 > time3:

        return red_button_style

    else:

        return white_button_style
#
@app2.callback(Output('navbar1', 'style'),
              [Input('navbar0', 'n_clicks_timestamp'), Input('navbar1', 'n_clicks_timestamp'), Input('navbar2', 'n_clicks_timestamp')])
def change_button_style(time1, time2, time3):
    if not time1 and not time2 and not time3:
        raise dash.exceptions.PreventUpdate
    if not time1:
        time1 = 0
    if not time2:
        time2 = 0
    if not time3:
        time3 = 0

    if time2 > time3 and time2 > time1:

        return red_button_style

    else:

        return white_button_style

@app2.callback(Output('navbar2', 'style'),
               [Input('navbar0', 'n_clicks_timestamp'), Input('navbar1', 'n_clicks_timestamp'),
                Input('navbar2', 'n_clicks_timestamp')])
def change_button_style(time1, time2, time3):
    if not time1 and not time2 and not time3:
        raise dash.exceptions.PreventUpdate
    if not time1:
        time1 = 0
    if not time2:
        time2 = 0
    if not time3:
        time3 = 0

    if time3 > time2 and time3 > time1:

        return red_button_style

    else:

        return white_button_style

if __name__ == "__main__":
    app2.run_server(host='127.0.0.1', port='8000', debug=True)
