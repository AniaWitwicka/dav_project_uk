import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

from chartScripts.governmentSatisfaction import govSatisfaction
from chartScripts.levelOfConcern import levelOfConcern

SpecialDates = pd.read_csv('datasets/special_dates.csv', encoding="utf-8")

appTest = dash.Dash(external_stylesheets=[
    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap-grid.min.css"])
layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=0, r=0, b=0, t=0),
    hovermode="closest",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
)

appTest.layout = html.Div([
    # html.Div([dcc.Graph(figure=onlineShoppingTable())], className='box1'),
    #                        html.Div([dcc.Graph(figure=actionsTable())], className='box1'),
    html.Div([dcc.Graph(figure=govSatisfaction(special_dates=SpecialDates))], className='box1'),
    html.Div([dcc.Graph(figure=levelOfConcern())], className='box1')

])

appTest.run_server(host='127.0.0.1', port='8000', debug=True, use_reloader=False)
