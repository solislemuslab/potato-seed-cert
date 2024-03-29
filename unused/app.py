import dash
import dash_bootstrap_components as dbc

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import xlrd
# import plotly.graph_objs as go
import functools
import re
import plotly.graph_objects as go
from apps.acres import acres_callback
from apps.prevalent_disease import callback_predis
from apps.variety import callback_variety
from apps.state_comparison import callback_statecomparison
from apps.statistical_test import callback_stat
from apps.upload import callback_upload
from apps import prevalent_disease, variety, acres, navbar, state_comparison, upload, statistical_test, faq

FA = "https://use.fontawesome.com/releases/v5.8.1/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FA])

server = app.server
app.config.suppress_callback_exceptions = True
callback_upload(app)
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 55,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "black",
    "font-color": "white"
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 55,
    "left": "-16rem",
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "black",
    "font-color": "white"
}


# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": "2rem",
    "padding": "4rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "4rem 1rem",
    "background-color": "#f8f9fa",
}

LINEBREAK_STYLE = {
    'border': '1px solid white'
}

Data_Import = [
    html.Li(
        # use Row and Col components to position the chevrons
        dbc.Row(
            [
                dbc.Col("Data Import", className='text-light'),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3",  style={'color': 'white'}), width="auto"
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-4",
    ),
    # we use the Collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink("Data Import", href="/data-import",
                        className='text-light', active="exact"),
        ],
        id="submenu-4-collapse",
    ),
    html.Br()
]

Visualization = [
    html.Li(
        # use Row and Col components to position the chevrons
        dbc.Row(
            [
                dbc.Col("Data Visualization", className='text-light'),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3",  style={'color': 'white'}), width="auto"
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-1",
    ),
    # we use the Collapse component to hide and reveal the navigation links
    dbc.Collapse(
        [
            dbc.NavLink("Disease Prevalence",
                        href="/disease-prevalence/1", className='text-light', active="exact"),
            # dbc.NavLink("Disease-Prevalence-2",
            #             href="/disease-prevalence/2", className='text-light'),
            dbc.NavLink("Source Comparison",
                        href="/state-comparison/1", className='text-light', active="exact"),
            # dbc.NavLink("State-Comparison-2",
            #             href="/state-comparison/2", className='text-light'),
            dbc.NavLink("Acre Rejection", href="/acre-rejection/1",
                        className='text-light', active="exact"),
            # dbc.NavLink("Acre-Rejection-2", href="/acre-rejection/2",
            #             className='text-light'),
            dbc.NavLink("Variety", href="/Variety/1",
                        className='text-light', active="exact"),
            # dbc.NavLink("Variety-2", href="/Variety/2",
            #             className='text-light'),
        ],
        id="submenu-1-collapse",
    ),
    html.Br()
]

Statistical_Test = [
    html.Li(
        dbc.Row(
            [
                dbc.Col("Statistical Test", className='text-light'),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3",  style={'color': 'white'}), width="auto"
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-2",
    ),
    dbc.Collapse(
        [
            dbc.NavLink("Statistical test", href="/stat-test",
                        className='text-light', active="exact"),
        ],
        id="submenu-2-collapse",
    ),
    html.Br()
]

GET_HELP = [
    html.Li(
        dbc.Row(
            [
                dbc.Col("Get help", className='text-light'),
                dbc.Col(
                    html.I(className="fas fa-chevron-right mr-3",  style={'color': 'white'}), width="auto"
                ),
            ],
            className="my-1",
        ),
        style={"cursor": "pointer"},
        id="submenu-3",
    ),
    dbc.Collapse(
        [
            dbc.NavLink("FAQ", href="/faq",
                        className='text-light', active="exact"),
        ],
        id="submenu-3-collapse",
    ),
    html.Br()
]


sidebar = html.Div(
    [
        html.H3("Menu",
                className="display-5 text-light"),
        html.Hr(style=LINEBREAK_STYLE),
        # html.P(
        #     "A sidebar with collapsible navigation links", className="lead"
        # ),
        dbc.Nav(Data_Import +
                Visualization +
                Statistical_Test +
                GET_HELP,
                vertical=True,),
    ],
    style=SIDEBAR_STYLE,
    id="sidebar",
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick


app.layout = html.Div([dcc.Store(id='side_click'),
                       dcc.Location(id="url"),
                       navbar.navbar,
                       sidebar,
                       dcc.Store(id='store-uploaded-data'),
                       content])

# this function is used to toggle the is_open property of each Collapse


def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# this function applies the "open" class to rotate the chevron
def set_navitem_class(is_open):
    if is_open:
        return "open"
    return ""


for i in [1, 2, 3, 4]:
    app.callback(
        Output(f"submenu-{i}-collapse", "is_open"),
        [Input(f"submenu-{i}", "n_clicks")],
        [State(f"submenu-{i}-collapse", "is_open")],
    )(toggle_collapse)

    app.callback(
        Output(f"submenu-{i}", "className"),
        [Input(f"submenu-{i}-collapse", "is_open")],
    )(set_navitem_class)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ['/', '/data-import']:
        # return layout.homepage
        return upload.homepage
    if pathname in ["/disease-prevalence/1"]:
        return prevalent_disease.prevalent_disease_block
    elif pathname == "/disease-prevalence/2":
        return html.P("This is the content of page 1.2. Yay!")
    elif pathname == "/acre-rejection/1":
        return acres.acres_layout
    elif pathname == "/acre-rejection/2":
        return html.P("No way! This is page 2.2!")
    elif pathname == "/Variety/1":
        return variety.variety_layout
    elif pathname == "/Variety/2":
        return html.P("No way! This is page 3.2!")
    elif pathname == "/state-comparison/1":
        return state_comparison.state_comparison_layout
    elif pathname == "/state-comparison/2":
        return html.P("No way! This is page 3.2!")
    elif pathname == "/stat-test":
        return statistical_test.homepage
    elif pathname == "/faq":
        return faq.homepage
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


acres_callback(app)
callback_statecomparison(app)
callback_predis(app)
callback_variety(app)
callback_stat(app)
if __name__ == "__main__":
    app.run_server(port=8000, debug=True)
