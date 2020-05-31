# Import required libraries

import plotly.express as px


# Multi-dropdown options


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
    
    
