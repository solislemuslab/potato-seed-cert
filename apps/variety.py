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

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_csv(DATA_PATH.joinpath("cleaned_potato.csv"))


virus_list = ["LR","ST","MIX","MOS"]
year_list = list(np.sort(df["S_YR"].unique()))
year_list.append("all")
category = ["S_STATE","VARIETY","S_G"]

def find_virus_columns(virus):
    return [x for x in df.columns.tolist() if
            re.compile(r'[SR1|SR2|winter]_P*{virus}V*$'.format(virus=virus)).search(x)]

variety_layout = html.Div(
        [dbc.Row([
            dbc.Col(html.Div(
                            dbc.Card(
                                html.H3(children='Sensitive and tolerant variety',
                                    className="text-center text-light bg-dark"), body=True, color="dark"),
                            ),
                    style = {"width": "100%",  "align-items": "center", "justify-content": "center"},
                    width= {"size": 8, "offset": 2})
            ]),

        html.Br(),
        dbc.Row([
            dbc.Col(dbc.Card(
                [
                    dbc.FormGroup(
                        [
                            dbc.Label("Season"),
                            dcc.Dropdown(
                                id="season_inspection_vareity",
                                options=[
                                    {"label": col, "value": col} for col in ["summer", "winter", "summer and winter"]
                                ],
                                value="summer", ),
                        ]),
                    dbc.FormGroup(
                        [
                            dbc.Label("Disease"),
                            dcc.Dropdown(
                                id="disease_type_variety",
                                options=[
                                    {"label": col, "value": col} for col in ["MOS", "LR", "MIX", "ST", "BRR"]
                                ],
                                value="LR", ),
                        ]),
                    dbc.FormGroup(
                        [
                            dbc.Label("Variety"),
                            dcc.Dropdown(
                                id="potato_variety",
                                options=[
                                    {"label": col, "value": col} for col in df["VARIETY"].dropna().unique()
                                ],
                                multi= True,
                                value= df["VARIETY"].value_counts()[:10].index ),
                        ]),
                    dbc.FormGroup(
                        [
                            dbc.Label("Year"),
                            dcc.Dropdown(
                                id="sensitive_year",
                                options=[
                                    {"label": col, "value": col} for col in year_list
                                ],
                                value="all",
                            ),
                        ]
                            ),


                ], body=True, )),
            dbc.Col(dcc.Graph(id="sensitivity-graph"), md=8),
        ],
            align="center", ),])


@app.callback(
    Output("sensitivity-graph", "figure"),
    [
        Input("season_inspection_vareity", "value"),
        Input("disease_type_variety", "value"),
        Input("potato_variety", "value"),
    ],
)
def sensitivity_graph(season, disease, variety):
    fig = go.Figure()
    frequent_variety = df["VARIETY"].value_counts()[:20].index

    if "summer" in season:
        temp = df[df["VARIETY"].isin(variety)].groupby("VARIETY").sum()[
            ["PLTCT_2", "NO_MOS_2ND", "NO_LR_2ND", "NO_MIX_2ND", "NO_ST_2ND", "NO_BRR_2ND"]]

        for column in temp.columns[1:]:
            new_column = column.replace("NO", "PCT")
            temp[new_column] = temp[column] / temp.iloc[:, 0]

        disease_type = [x for x in temp.columns if x.find(disease) != -1]

        fig.add_trace(go.Scatter(x=temp.index, y=temp[disease_type[1]],
                                 mode='lines+markers',
                                 name=disease_type[1] + " " + "summer"))

    if "winter" in season:
        temp = df[df["VARIETY"].isin(variety)].groupby("VARIETY").sum()[
            ["winter_PLANTCT", "winter_MOSN", "winter_LRN", "winter_MXDN"]]

        for column in temp.columns[1:]:
            new_column = column.replace("N", "_PCT")
            temp[new_column] = temp[column] / temp.iloc[:, 0]

        disease_type = [x for x in temp.columns if x.find(disease) != -1]

        fig.add_trace(go.Scatter(x=temp.index, y=temp[disease_type[1]],
                                 mode='lines+markers',
                                 name=disease_type[1] + " " + "winter"))
    fig.update_layout(showlegend=True)
    fig.update_layout(
        title="Sensitive/tolerant variety",
        xaxis_title="Potato Variety",
        yaxis_title="Percentage of potato with {}".format(disease),

    )
    return fig

