import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def pie_plot(date='2020 -04-26'):
    casesDF = pd.read_csv('coronavirus-cases_latest.csv',delimiter=',',encoding='utf-8')
    deathsDF = pd.read_csv('coronavirus-deaths_latest.csv',delimiter=',',encoding='utf-8')
    casesDF = casesDF.rename(columns={"Area name":"AreaName", "Area type": "AreaType", 'Specimen date':"SpecimenDate",
                                      "Cumulative lab-confirmed cases": "CumulativeLabConfirmedCases",
                                      "Previously reported cumulative cases":"PreviouslyReportedCumulativeCases",
                                      'Change in cumulative cases': 'ChangeInCumulativeCases'})
    casesDF = casesDF.drop('Area code', axis =1)
    localDF = casesDF[casesDF.AreaType == "Region"]
    localDF['SpecimenDate'] = localDF['SpecimenDate'].astype('datetime64[ns]')
    # 2020-04-26
    colors = ['#92a8d1','#6585c2' , '#034f84', '#023a61' , '#f7cac9', '#d19e9d' , '#f7786b', '#f7786b', '#cf4436']

    #fig = px.pie(localDF[localDF.SpecimenDate == '2020 -04-26'], values='CumulativeLabConfirmedCases', names='AreaName', title='Percentage of cases in Regions of UK on 2020-04-26')

    fig = go.Figure(data=[go.Pie(labels=localDF[localDF.SpecimenDate == date]['AreaName'].values,
                             values=localDF[localDF.SpecimenDate == date]['CumulativeLabConfirmedCases'].values)])

    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=8, hole=.3,
                   marker=dict(colors=colors, line=dict(color='#17191a', width=3)))

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        width=300, height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
        family="Courier New, monospace",
        size=14,
        color="#7f7f7f",
 
    )
    )
    fig.update_layout(showlegend=True)
    fig.update_layout(legend=dict(x=0, y=1.5))
    return fig
