import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from urllib.request import urlopen
import json
import numpy as np
from dash.dependencies import Input, Output
import pandas as pd
import xlrd
import base64


from Layout import homepage_layout, virus_layout, sidebar_layout, CONTENT_STYLE, weather_layout

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)
server = app.server

PAGES = [
    {'children': 'Home', 'href': '/', 'id': 'home'},
    {'children': 'Virus', 'href': '/Virus', 'id': 'correlation-page'}
]

app.layout = html.Div([ dcc.Location(id="url"), sidebar_layout,
#                     dcc.Link('Navigate to "/"', href='/'),
    #                     html.Br(),
    #                     dcc.Link('Navigate to "/page-2"', href='/page-2'),
    # dcc.Location(id='url', refresh=False),
    #                     dcc.Link('Navigate to "/"', href='/'),
    #                     html.Br(),
    #                     dcc.Link('Navigate to "/page-2"', href='/page-2'),
                        html.Div(id="page-content", style=CONTENT_STYLE)])

@app.callback(Output("page-content", "children"),
             [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == '/':
        return homepage_layout
    elif pathname == "/virus":
        return virus_layout
    elif pathname == "/weather":
        return weather_layout

if __name__ == '__main__':
    app.run_server(debug=False)