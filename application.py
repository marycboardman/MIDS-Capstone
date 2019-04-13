import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.graph_objs as go

from init import app, application

from metrics.hate_crimes import layout as hc_lay

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
    ],
    className="mt-4",
)

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Hate Crimes over Time", href='/'),
        dbc.DropdownMenuItem("Abstract and Instructions", href='/instructions'),
        dbc.DropdownMenuItem("Overview of Problem", href='/overview'),
        dbc.DropdownMenuItem("Methodology: Ratings", href='/ratings'),
        dbc.DropdownMenuItem("Methodology: Time Series", href='/time-series'),
        dbc.DropdownMenuItem("Data Sources", href='/sources'),
        dbc.DropdownMenuItem("Recommendations", href='/recommendations'),
        dbc.DropdownMenuItem("Results: All Cities", href='/allcities'),
        dbc.DropdownMenuItem("Conclusions", href='/conclusions'),
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
    elif pathname == '/overview':
        return all_lay.layout
    elif pathname == '/instructions':
        return all_lay.layout
    elif pathname == '/ratings':
        return all_lay.layout
    elif pathname == '/time-series':
        return all_lay.layout
    elif pathname == '/sources':
        return all_lay.layout
    elif pathname == '/recommendations':
        return all_lay.layout
    elif pathname == '/allcities':
        return all_lay.layout
    elif pathname == '/conclusions':
        return all_lay.layout
    elif pathname == '/acknowledgements':
        return all_lay.layout

if __name__ == '__main__':
    application.run(debug=False, port=8080)

