import plotly.graph_objects as go  # or plotly.express as px

fig = go.Figure()  # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

import dash
import dash_core_components as dcc
import dash_html_components as html

from tables import onlineShoppingTable
from tables import actionsTable

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

appTest.layout = html.Div([html.Div([dcc.Graph(figure=onlineShoppingTable())], className='box1'),
                           html.Div([dcc.Graph(figure=actionsTable())], className='box1')
                           ])

appTest.run_server(host='127.0.0.1', port='8000', debug=True, use_reloader=False)
