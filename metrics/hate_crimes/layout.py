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
                html.Div([
                    html.Label('Population:'),
                    dcc.Dropdown(
                        id='pop-select',
                        options=pop_opts,
                        value='All'
                    )
                ]),
            ])

intro_layout = html.Div([
    dcc.Markdown(dedent('''
        # Introduction and Overview

        People motivated enough by hate to commit a hate crime have more access than ever before to a potential victim’s home, place of work, and other personal information. This could lead to an increased risk of hate crimes where there is both a growing trend of hate crimes and an increased ability to dox someone. Understanding where this intersection lies is critical to identifying if and where these issues exist. Conversely, identifying best practices can also provide guidance for the municipalities who are missing the mark in terms of victim protection. 

        While there are many possible stakeholders, in this project, we are focusing on elected officials in municipalities as primary stakeholders, with police departments and the FBI as secondary stakeholders. We assume elected officials will be the most responsive to the optics of either low or heightened risk. Police departments may not have the same priorities, as they often have many crimes to investigate with limited resources. Also, while investigating hate crimes is a priority for the FBI, they are a large federal bureaucracy that, by definition, is likely to be more slow-moving than a municipal government. 
    ''')) 
])

ts_layout = html.Div([
    dcc.Markdown(dedent('''

        # Methodology: Time Series Model

        ## This is an <h2> tag

        ###### This is an <h6> tag
    ''')) 
])

allcities_layout = html.Div([
    html.H3('All Cities'),
    html.Div([
        dt.DataTable(id='my-datatable',
        columns=[{'name': i, 'id': i} for i in city_data.columns],
        data = city_data.to_dict('rows'),
        style_table={'overflowX': 'scroll'},
        style_cell={
            'text-align': 'left',
            'minWidth': '0px', 'maxWidth': '220px',
            'whiteSpace': 'normal'
        },
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        )
    ]),
    html.Div(id='allcities-content'),
])



@app.callback(
    Output('hate-crimes-graph', 'figure'),
    [Input('hate-crimes-compare-all', 'values'),
     Input('city-select', 'value'),
     Input('state-select','value'),
     Input('grade-select','value'),
     Input('trend-select','value'),
     Input('pop-select','value')])

def update_figure(compare_all_list, selected_city, selected_state, selected_grade, selected_trend, selected_pop):
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
    if selected_pop != 'All':
        cohort_name = cohort_name + 'Population:' + selected_pop.capitalize() + ' '
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
