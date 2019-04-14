import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.graph_objs as go

from init import app, application

from metrics.hate_crimes import layout as hc_lay
from metrics.hate_crimes2 import layout as hc_lay2
from metrics.hate_crimes3 import layout as hc_lay3

all_lay = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([
                    hc_lay.filters
                    ],
                    md=4,
                ),

                hc_lay.graph_layout,
            ],
            no_gutters=True,
            align='center'
        ),  
        dbc.Row(
            [
                dbc.Col([
                    hc_lay2.filters
                    ],
                    md=4,
                ),

                hc_lay2.graph_layout,
            ],
            no_gutters=True,
            align='center'
        ), 
        dbc.Row(
            [
                dbc.Col([
                    hc_lay3.filters
                    ],
                    md=4,
                ),

                hc_lay3.graph_layout,
            ],
            no_gutters=True,
            align='center'
        ), 
    ],
    className="mt-4",
)

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Data Exploration Tool", href='/'),
        dbc.DropdownMenuItem("Introduction and Overview", href='/introduction'),
        dbc.DropdownMenuItem("Methodology: Time Series Model", href='/time-series'),
        dbc.DropdownMenuItem("Methodology: Doxing Risk Assessment", href='/doxing-risk'),
        dbc.DropdownMenuItem("Data Sources: All Cities", href='/all-cities'),
        dbc.DropdownMenuItem("Key Insights", href='/key-insights'),
        dbc.DropdownMenuItem("Recommendations", href='/recommendations'),
        dbc.DropdownMenuItem("Author Bios", href='/author-bios'),
        dbc.DropdownMenuItem("Acknowledgements", href='/acknowledgements')
		],
    nav=True,
    in_navbar=True,
    label="Menu",
)

logo = dbc.Navbar(
    dbc.Container(
        [
        dbc.Col(
            [
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
            ],
            align="start",
			width=2,
            ),
        dbc.Col(
            [
            html.H3('Doxing and Hate Crimes: Identifying Risk at the Intersection', style={'color': 'white'})
            ],
            align="center",
			width=10
            ),
        ]
    ),
    color="#145bce",
    dark=True,
    className="mb-5",
)

app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            logo,
            html.Div(id='page-content')
            ], style={'font-family':'Lato'})


# the same function (toggle_navbar_collapse) is used in all three callbacks

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(Output('page-content','children'),
[Input('url','pathname')])
def render_page(pathname):
    if pathname == '/':
        return all_lay
    elif pathname == '/introduction':
        return hc_lay.intro_layout
    elif pathname == '/time-series':
        return hc_lay.ts_layout
    elif pathname == '/doxing-risk':
        return all_lay.layout
    elif pathname == '/all-cities':
        return hc_lay.allcities_layout
    elif pathname == '/key-insights':
        return all_lay.layout
    elif pathname == '/recommendations':
        return all_lay.layout
    elif pathname == '/author-bios':
        return all_lay.layout
    elif pathname == '/acknowledgements':
        return all_lay.layout

if __name__ == '__main__':
    application.run(debug=False, port=8080)

