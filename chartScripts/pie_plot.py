import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def pie_plot(date='2020 -04-26'):
    casesDF = pd.read_csv('datasets/coronavirus-cases_latest.csv', delimiter=',', encoding='utf-8')
    deathsDF = pd.read_csv('datasets/coronavirus-deaths_latest.csv', delimiter=',', encoding='utf-8')
    casesDF = casesDF.rename(columns={"Area name":"AreaName", "Area type": "AreaType", 'Specimen date':"SpecimenDate",
                                      "Cumulative lab-confirmed cases": "CumulativeLabConfirmedCases",
                                      "Previously reported cumulative cases":"PreviouslyReportedCumulativeCases",
                                      'Change in cumulative cases': 'ChangeInCumulativeCases'})
    casesDF = casesDF.drop('Area code', axis =1)
    localDF = casesDF[casesDF.AreaType == "Region"]
    localDF['SpecimenDate'] = localDF['SpecimenDate'].astype('datetime64[ns]')
    # 2020-04-26
    colors = ['#6c7991','#6585c2' , '#034f84', '#023a61' , '#f7cac9', '#d19e9d' , '#a14940', '#f7786b', '#cf4436']

    #fig = px.pie(localDF[localDF.SpecimenDate == '2020 -04-26'], values='CumulativeLabConfirmedCases', names='AreaName', title='Percentage of cases in Regions of UK on 2020-04-26')
    labels = localDF[localDF.SpecimenDate == date]['AreaName'].values
    casessum = localDF[localDF.SpecimenDate == date]['CumulativeLabConfirmedCases'].values.sum()
    values = [round((x / casessum) * 100) for x in localDF[localDF.SpecimenDate == date]['CumulativeLabConfirmedCases'].values]
    
    fig = go.Figure(data=[go.Pie(labels=labels,
                             values=values)])

    fig.update_traces(hoverinfo='label+percent', textinfo='percent', textfont_size=8, hole=.3,
                   marker=dict(colors=colors, line=dict(color='#17191a', width=3)))

    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=50),
        #width=300, height=600,
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
