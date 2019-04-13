import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.graph_objs as go
import os

from init import app

def create_opts(unique_values):
    cleanlist = [x for x in unique_values if str(x) != 'nan']
    cleanlist.sort()
    cleanlist.insert(0,'All')
    opts = []
    for s in cleanlist:
        val = {'label':s, 'value':s}
        opts.append(val)
    return opts

df = pd.read_csv('data/cities_forecasts.csv') 
city_opts = create_opts(df.city.unique().tolist())
state_opts = create_opts(df.state.unique().tolist())
grade_opts = create_opts(df.grade.unique().tolist())
trend_opts = create_opts(df.trend.unique().tolist())

def aggr_func(groups, count, df):
    df1 = pd.DataFrame(df.groupby(groups)[count].median()).reset_index()
    return df1

graph_layout =  dbc.Col([
                    html.H3("Monthly Hate Crimes"),
                    dcc.Graph(
                        id='hate-crimes-graph'
                    )
                ]
            )

filters = dbc.Container([
                html.Div([
                    dcc.Checklist(
                        id = 'hate-crimes-compare-all',
                        options= [{'label': 'Compare to All','value':1}],
                        values = [1]
                    )
                ]),
                html.Div([
                    html.Label('City:'),
                    dcc.Dropdown(
                        id='city-select',
                        options=city_opts,
                        value='All',
                        clearable=False
                    ),
                ]),
                html.Div([
                    html.Label('State:'),
                    dcc.Dropdown(
                        id='state-select',
                        options=state_opts,
                        value='All',
                        clearable=False
                    ),
                ]),

                html.Div([
                    html.Label('Grade:'),
                    dcc.Dropdown(
                        id='grade-select',
                        options=grade_opts,
                        value='All',
                        clearable=False
                    )
                ]),
            
                html.Div([
                    html.Label('Trend:'),
                    dcc.Dropdown(
                        id='trend-select',
                        options=trend_opts,
                        value='All',
                        clearable=False
                    )
                ]),
            ])

@app.callback(
    Output('hate-crimes-graph', 'figure'),
    [Input('hate-crimes-compare-all', 'values'),
     Input('city-select', 'value'),
     Input('state-select','value'),
     Input('grade-select','value'),
     Input('trend-select','value')])

def update_figure(compare_all_list, selected_city, selected_state, selected_grade, selected_trend):
    filtered_df = df.copy()
    cohort_name = ''
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['city']==selected_city]
        cohort_name = cohort_name + 'City:' + selected_city.upper() + ' '
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['state']==selected_state]
        cohort_name = cohort_name + 'State:' + selected_state.upper() + ' '
    if selected_grade != 'All':
        filtered_df = filtered_df[filtered_df['grade']==selected_grade]
        cohort_name = cohort_name + 'Grade:' + selected_grade.upper() + ' '
    if selected_trend != 'All':
        filtered_df = filtered_df[filtered_df['trend']==selected_trend]
        cohort_name = cohort_name + 'Trend:' + selected_trend.capitalize() + ' '
    filtered_df = aggr_func('ds','yhat', filtered_df)
    full_df = aggr_func('ds','yhat', df)

    trace1 = go.Scatter(
        x=filtered_df['ds'], 
        y=filtered_df['yhat'], 
        mode='lines',
        name='Filtered Results',
        text=[cohort_name],
        textposition='top center')

    trace2 = go.Scatter(
        x=full_df['ds'], 
        y=full_df['yhat'], 
        mode='lines',
        name = 'All (Median)')

    if len(compare_all_list)==1:
        traces = [trace1, trace2]
    else:
        traces = [trace1]

    return {
        'data': traces,
        'layout': go.Layout(
            title=cohort_name,
            xaxis={'title': 'Year'},
            yaxis={'title': 'Total Monthly Hate Crimes'},
        )
    }
