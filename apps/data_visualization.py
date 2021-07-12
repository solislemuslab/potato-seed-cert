from app import app

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
import pathlib

from apps import prevalent_disease, acres, navbar, variety, state_comparison, upload, statistical_test


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'Blue',
    'padding': '6px'
}

data_visualization_layout = html.Div([
    html.H3("Datas visualization"),
    html.Br(),
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='State Comparison', value='tab-1', className='custom-tab',
                selected_className='custom-tab--selected', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Prevalent Disease', value='tab-2', className='custom-tab',
                selected_className='custom-tab--selected', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Sensitive Variety', value='tab-3', className='custom-tab',
                selected_className='custom-tab--selected'),
        dcc.Tab(label='Acre Rejection', value='tab-4', className='custom-tab',
                selected_className='custom-tab--selected'),
    ], parent_className='custom-tabs',
        className='custom-tabs-container', style=tabs_styles),
    html.Div(id='tabs-content-inline')

])
# data_visualization_layout = html.Div([
#    html.H3("Data visualization"),
#    html.Br(),
#    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
#        dcc.Tab(label='State Comparison1', value='tab-1',
#                style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='Prevalent Disease', value='tab-2',
#                style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='Sensitive Variety', value='tab-3',
#                style=tab_style, selected_style=tab_selected_style),
#        dcc.Tab(label='Acre Rejection', value='tab-4',
#                style=tab_style, selected_style=tab_selected_style),
#    ], style=tabs_styles),
#    html.Div(id='tabs-content-inline')

# ])


@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return state_comparison.state_comparison_layout
    elif tab == 'tab-2':
        return prevalent_disease.prevalent_disease_block
    elif tab == 'tab-3':
        return variety.variety_layout
    elif tab == 'tab-4':
        return acres.acres_layout
