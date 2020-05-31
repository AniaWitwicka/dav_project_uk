import dash
import dash_bootstrap_components as dbc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
fig1 = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada', width=800, height=100)


app.layout = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("A single column"))),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig), width=6),
                dbc.Col(dcc.Graph(figure=fig), width=3),
                dbc.Col(dcc.Graph(figure=fig), width=3),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig), width=6),
                dbc.Col(dcc.Graph(figure=fig), width=3),
                dbc.Col(dcc.Graph(figure=fig), width=3),
            ]
        ),
       dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=fig1), width=6),
                dbc.Col(dcc.Graph(figure=fig1), width=2),
                dbc.Col(dcc.Graph(figure=fig1), width=2),
                dbc.Col(dcc.Graph(figure=fig1), width=2),
            ],
        className="h-5"),
    ]
)
if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port='8050', debug=True)

