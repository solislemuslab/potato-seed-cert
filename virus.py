import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import xlrd
# import plotly.graph_objs as go
import functools
import re
import plotly.graph_objects as go
from app import app


df = pd.read_excel("2003-2016 Seed Potato Cert data v20191204_NO FL lines_Rioux 5AUG2020.xlsx", sheet_name="2003-2016 Seed Potato Cert")
virus_list = ["LR","ST","MIX","MOS"]
year_list = list(np.sort(df["S_YR"].unique()))
year_list.append("all")
category = ["S_STATE","VARIETY","S_G"]

def find_virus_columns(virus):
    return [x for x in df.columns.tolist() if
            re.compile(r'[SR1|SR2|winter]_P*{virus}V*$'.format(virus=virus)).search(x)]


#
#
# @app.callback(
#     Output("button-clicks", "children"), [Input("button-link", "n_clicks")]
# )
# @app.callback(Output("page-content", "children"),
#              [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname == '/':
#         return homepage_layout
#     elif pathname == "/correlation":
#         return correlation_layout
#     elif pathname == "/weather":
#         return weather_layout

controls_1 = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Category"),
                dcc.Dropdown(
                    id="category",
                    options=[
                        {"label": col, "value": col} for col in category
                    ],
                    value="S_STATE",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("State Number"),
                dcc.Dropdown(
                    id="state_number",
                    options=[
                        {"label": col, "value": col} for col in range(1,20)
                    ],
                    value=10,
                ),
            ]
        ),

        dbc.FormGroup(
            [
                dbc.Label("Virus"),
                dcc.Dropdown(
                    id="state_virus",
                    options=[
                        {"label": col, "value": col} for col in virus_list
                    ],
                    value="LR",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Year"),
                dcc.Dropdown(
                    id="state_year",
                    options=[
                        {"label": col, "value": col} for col in year_list
                    ],
                    value="all",
                ),
            ]
        ),
    ],
    body=True,
)

controls_2 = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Variety Number"),
                dcc.Dropdown(
                    id="variety_number",
                    options=[
                        {"label": col, "value": col} for col in range(1,20)
                    ],
                    value=10,
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Virus"),
                dcc.Dropdown(
                    id="variety_virus",
                    options=[
                        {"label": col, "value": col} for col in virus_list
                    ],
                    value="LR",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Year"),
                dcc.Dropdown(
                    id="variety_year",
                    options=[
                        {"label": col, "value": col} for col in year_list
                    ],
                    value="all",
                ),
            ]
        ),
    ],
    body=True,
)

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="State", tab_id="tab-1"),
                dbc.Tab(label="Variety", tab_id="tab-2"),
            ],
            id="tabs",
            active_tab="tab-1",
        ),
        html.Div(id="content"),
    ]
)

@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return controls_1
    elif at == "tab-2":
        return controls_2
    return html.P("This shouldn't ever be displayed...")

virus_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(tabs, md=4),
                dbc.Col(dcc.Graph(id="state-graph"), md=8),
            ],
            align="center",
        ),

    ],
    fluid=True,
)


@app.callback(
    Output("state-graph", "figure"),
    [
        Input("category", "value"),
        Input("state_number", "value"),
        Input("state_virus", "value"),
        Input("state_year", "value")
    ],
)
def plot_virus_by_state(category, state_number, virus, year):
    virus_columns = find_virus_columns(virus)
    if year == "all":
        temp = df
    else:
        temp = df[df["S_YR"] == year]
    frequent_state = temp[category].value_counts()[:state_number].index.to_list()
    temp = temp[temp[category].isin(frequent_state)].groupby(category).mean()[virus_columns]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 0],
                         text=np.round(temp.iloc[:, 0], 3),
                         textposition='outside',
                         name=temp.columns[0],
                         marker_color='rgb(55, 83, 109)',
                         orientation='h'
                         ))
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 1],
                         text=np.round(temp.iloc[:, 1], 3),
                         textposition='outside',
                         name=temp.columns[1],
                         marker_color='rgb(26, 118, 255)',
                         orientation='h'
                         ))

    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 2],
                         text=np.round(temp.iloc[:, 2], 3),
                         textposition='outside',
                         name=temp.columns[2],
                         marker_color='crimson',
                         orientation='h'
                         ))

    fig.update_layout(
        title='Virus across {}'.format(category),
        xaxis_tickfont_size=14,
        yaxis=dict(
            title=category,
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            y=0,
            x=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    return fig