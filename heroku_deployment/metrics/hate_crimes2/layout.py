import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
from dash.dependencies import Input, Output
from textwrap import dedent

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
city_data = pd.read_csv('data/city_data.csv')
city_data = city_data[['City', 'State', 'Grade', 'Hate Crime Trend', 'Notes', 'Crime Data Source']]
city_opts = create_opts(df.city.unique().tolist())
state_opts = create_opts(df.state.unique().tolist())
grade_opts = create_opts(df.grade.unique().tolist())
trend_opts = create_opts(df.trend.unique().tolist())
pop_opts = create_opts(['0-100000','100001-250000','250001-500000','500001-1000000','1000001-5000000','5000001+'])

def aggr_func(groups, count, df):
    df1 = pd.DataFrame(df.groupby(groups)[count].median()).reset_index()
    return df1

graph_layout =  dbc.Col([
                    dcc.Graph(
                        id='hate-crimes-graph2'
                    )
                ]
            )

filters = dbc.Container([
                html.Div([
                    dcc.Checklist(
                        id = 'hate-crimes-compare-all2',
                        options= [{'label': 'Compare to All','value':1}],
                        values = [1]
                    )
                ]),
                html.Div([
                    html.Label('City:'),
                    dcc.Dropdown(
                        id='city-select2',
                        options=city_opts,
                        value='All',
                        clearable=False
                    ),
                ]),
                html.Div([
                    html.Label('State:'),
                    dcc.Dropdown(
                        id='state-select2',
                        options=state_opts,
                        value='All',
                        clearable=False
                    ),
                ]),

                html.Div([
                    html.Label('Grade:'),
                    dcc.Dropdown(
                        id='grade-select2',
                        options=grade_opts,
                        value='All',
                        clearable=False
                    )
                ]),
            
                html.Div([
                    html.Label('Trend:'),
                    dcc.Dropdown(
                        id='trend-select2',
                        options=trend_opts,
                        value='All',
                        clearable=False
                    )
                ]),
                html.Div([
                    html.Label('Population:'),
                    dcc.Dropdown(
                        id='pop-select2',
                        options=pop_opts,
                        value='All',
                        clearable=False
                    )
                ]),
            ])


@app.callback(
    Output('hate-crimes-graph2', 'figure'),
    [Input('hate-crimes-compare-all2', 'values'),
     Input('city-select2', 'value'),
     Input('state-select2','value'),
     Input('grade-select2','value'),
     Input('trend-select2','value'),
     Input('pop-select2','value')])

def update_figure(compare_all_list, selected_city, selected_state, selected_grade, selected_trend, selected_pop):
    filtered_df = df.copy()
    cohort_name = ''
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['city']==selected_city]
        cohort_name = cohort_name + 'City:' + selected_city.upper() + ' '
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['state']==selected_state]
        cohort_name = cohort_name + 'State (median):' + selected_state.upper() + ' '
    if selected_grade != 'All':
        filtered_df = filtered_df[filtered_df['grade']==selected_grade]
        cohort_name = cohort_name + 'Grade (median):' + selected_grade.upper() + ' '
    if selected_trend != 'All':
        filtered_df = filtered_df[filtered_df['trend']==selected_trend]
        cohort_name = cohort_name + 'Trend (median):' + selected_trend.capitalize() + ' '
    if selected_pop != 'All':
        cohort_name = cohort_name + 'Population (median):' + selected_pop.capitalize() + ' '
        alist = selected_pop.split('-')
        if len(alist)==1:
            a = int(''.join(i for i in alist[0] if i.isdigit()))
            filtered_df = filtered_df[filtered_df['population']==a]
        else:
            a1 = int(alist[0])
            a2 = int(alist[1])
            filtered_df = filtered_df[(filtered_df['population']>=a1)&(filtered_df['population']<=a2)]
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
