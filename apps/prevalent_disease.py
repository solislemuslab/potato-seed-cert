import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pathlib
from app import app

import re
import plotly.graph_objects as go

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# owner: shivp Kaggle. Source: https://data.mendeley.com/datasets
# dataset was modified. Original data: https://www.kaggle.com/shivkp/customer-behaviour
df = pd.read_csv(DATA_PATH.joinpath("cleaned_potato.csv"))

virus_list = ["LR","ST","MIX","MOS"]
year_list = list(np.sort(df["S_YR"].unique()))
year_list.append("all")
category = ["S_STATE","VARIETY","S_G"]

def find_virus_columns(virus):
    return [x for x in df.columns.tolist() if
            re.compile(r'[SR1|SR2|winter]_P*{virus}V*$'.format(virus=virus)).search(x)]


prevalent_disease_block = html.Div([dbc.Row([
                dbc.Col(dbc.Card(html.H3(children='Disease Prevalence',
                                         className="text-center text-light bg-dark"), body=True, color="dark")
                , className="mt-4 mb-4", width= {"size": 8, "offset": 2})
        ],align="center",),
            dbc.Row([
                dbc.Col(dbc.Card(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("Season"),
                                dcc.Dropdown(
                                    id="season_inspection",
                                    options=[
                                        {"label": col, "value": col} for col in
                                        ["summer", "winter", "summer and winter"]
                                    ],
                                    value="summer", ),
                            ]),
                        dbc.FormGroup(
                            [
                                dbc.Label("Disease"),
                                dcc.Dropdown(
                                    id="disease_type",
                                    options=[
                                        {"label": col, "value": col} for col in ["MOS", "LR", "MIX", "ST", "BRR"]
                                    ],
                                    value="LR", ),
                            ]),
                        dbc.FormGroup(
                            [
                                dbc.Label("State"),
                                dcc.Dropdown(
                                    id="state_type",
                                    options=[
                                        {"label": col, "value": col} for col in sorted(df["S_STATE"].dropna().unique())
                                    ],
                                    value="WI", ),
                            ]),
                        dbc.FormGroup(
                            [
                                dbc.Label("Variety"),
                                dcc.Dropdown(
                                    id="disease_potato_variety",
                                    options=[
                                        {"label": col, "value": col} for col in df["VARIETY"].dropna().unique()
                                    ],
                                    multi=True,
                                    value=df["VARIETY"].value_counts()[:3].index),
                            ]),
                    ], body=True, )),
                dbc.Col(dcc.Graph(id="prevalence-graph"), md=8),
            ],
                align="center", ),
        ])

@app.callback(
    Output("prevalence-graph", "figure"),
    [
        Input("season_inspection", "value"),
        Input("disease_type", "value"),
        Input("state_type", "value"),
        Input("disease_potato_variety", "value")
    ],
)
def prevalent_disease(season, disease, state, variety):
    print('a')
    fig = go.Figure()

    if "summer" in season:
        temp = df[(df["S_STATE"] == state) & (df["VARIETY"].isin(variety))].groupby("CY").sum()[
            ["PLTCT_2", "NO_MOS_2ND", "NO_LR_2ND", "NO_MIX_2ND", "NO_ST_2ND", "NO_BRR_2ND"]]

        for column in temp.columns[1:]:
            new_column = column.replace("NO", "PCT")
            temp[new_column] = temp[column] / temp.iloc[:, 0]

        disease_type = [x for x in temp.columns if x.find(disease) != -1]

        fig.add_trace(go.Scatter(x=temp.index, y=temp[disease_type[1]],
                                 mode='lines+markers',
                                 name=disease_type[1] + " " + "summer"))

    if "winter" in season:

        temp = df[(df["S_STATE"] == state) & (df["VARIETY"].isin(variety))].groupby("S_YR").sum()[
            ["winter_PLANTCT", "winter_MOSN", "winter_LRN", "winter_MXDN"]]
        for column in temp.columns[1:]:
            new_column = column.replace("N", "_PCT")
            temp[new_column] = temp[column] / temp.iloc[:, 0]

        disease_type = [x for x in temp.columns if x.find(disease) != -1]

        fig.add_trace(go.Scatter(x=temp.index, y=temp[disease_type[1]],
                                 mode='lines+markers',
                                 name=disease_type[1] + " " + "winter"))

    # fig.add_trace(go.Scatter(x=temp.index, y=temp[disease_type[1]],
    #                          mode='lines+markers',
    #                          name='lines+markers'))
    fig.update_layout(showlegend=True)
    fig.update_layout(
        title="Prevalent Disease",
        xaxis_title="Year",
        yaxis_title="Percentage of potato with {}".format(disease),

    )
    return fig