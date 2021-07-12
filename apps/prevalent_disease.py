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
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../datasets").resolve()
# df = pd.read_csv(DATA_PATH.joinpath("cleaned_potato.csv"))

virus_list = ["LR", "ST", "MIX", "MOS"]
# year_list = list(np.sort(df["S_YR"].unique()))
year_list = list(range(2000, 2017))
year_list.append("all")
category = ["S_STATE", "VARIETY", "S_G"]

# def find_virus_columns(virus):
#     return [x for x in df.columns.tolist() if
#             re.compile(r'[SR1|SR2|winter]_P*{virus}V*$'.format(virus=virus)).search(x)]


# left_column = dbc.Card(
#                     [
#                         dbc.FormGroup(
#                             [
#                                 dbc.Label("Season"),
#                                 dcc.Dropdown(
#                                     id="season_inspection",
#                                     options=[
#                                         {"label": col, "value": col} for col in
#                                         ["summer", "winter", "summer and winter"]
#                                     ],
#                                     value="summer", ),
#                             ]),
#                         dbc.FormGroup(
#                             [
#                                 dbc.Label("Disease"),
#                                 dcc.Dropdown(
#                                     id="disease_type",
#                                     options=[
#                                         {"label": col, "value": col} for col in ["MOS", "LR", "MIX", "ST", "BRR"]
#                                     ],
#                                     value="LR", ),
#                             ]),
#                         dbc.FormGroup(
#                             [
#                                 dbc.Label("State"),
#                                 dcc.Dropdown(
#                                     id="state_type",
#                                     # options=[
#                                     #     {"label": col, "value": col} for col in sorted(df["S_STATE"].dropna().unique())
#                                     # ],
#                                     value="WI", ),
#                             ]),
#                         dbc.FormGroup(
#                             [
#                                 dbc.Label("Variety"),
#                                 dcc.Dropdown(
#                                     id="disease_potato_variety",
#                                     options=[
#                                         {"label": col, "value": col} for col in df["VARIETY"].dropna().unique()
#                                     ],
#                                     multi=True,
#                                     value=df["VARIETY"].value_counts()[:3].index),
#                             ]),
#                     ], body=True, style={'height':'70vh'})

LEFT_COLUMN = dbc.Jumbotron(
    [
        html.H4(children="Select bank & dataset size", className="display-5"),
        html.Hr(className="my-2"),
        dbc.FormGroup(
            [
                dbc.Label("Select Inspection Season"),
                # html.P(
                #             "(Lower is faster. Higher is more precise)",
                #             style={"fontSize": 10, "font-weight": "lighter"},
                #         ),
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
                dbc.Label("Select Disease Type"),
                dcc.Dropdown(
                    id="disease_type",
                    options=[
                       {"label": col, "value": col} for col in ["MOS", "LR", "MIX", "ST", "BRR"]
                    ],
                    value=["LR", "ST"],
                    multi=True
                ),
            ]),
        dbc.FormGroup(
            [
                dbc.Label("Select State"),
                dcc.Dropdown(
                    id="state_type",
                    # options=[
                    #     {"label": col, "value": col} for col in sorted(df["S_STATE"].dropna().unique())
                    # ],
                    value="WI", ),
            ]),
        dbc.FormGroup(
            [
                dbc.Label("Select Potato Variety"),
                dcc.Dropdown(
                    id="disease_potato_variety",
                    # options=[
                    #     {"label": col, "value": col} for col in df["VARIETY"].dropna().unique()
                    # ],
                    multi=True)
                # value=df["VARIETY"].value_counts()[:3].index),
            ]),
    ],
)


@app.callback(
    [Output("state_type", "options"),
     Output("disease_potato_variety", "options"),
     Output("disease_potato_variety", "value"),

     ],
    [
        Input("store-uploaded-data", "data")
    ]
)
def dropdown_option(data):
    if data:
        df = pd.DataFrame(data)

    state_options = [
        {"label": col, "value": col} for col in sorted(df["S_STATE"].dropna().unique())
    ]
    variety_options = [
        {"label": col, "value": col} for col in df["VARIETY"].dropna().unique()
    ]
    variety_value = df["VARIETY"].value_counts()[:3].index

    return state_options, variety_options, variety_value


RIGHT_PLOT = [
    dbc.CardHeader(html.H5("Prevalent Disease")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams_comp",
                        color="warning",
                        style={"display": "none"},
                    ),

                    dcc.Graph(id="prevalence-graph",
                              config={"displayModeBar": False},),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]


prevalent_disease_block = html.Div([
    dbc.Row([
        dbc.Col(LEFT_COLUMN, align="center", md=4),
        dbc.Col(
            dbc.Card(RIGHT_PLOT), md=8)
    ],
        style={"marginTop": 30}, align="center", ),
])


@app.callback(
    Output("prevalence-graph", "figure"),
    [
        Input("season_inspection", "value"),
        Input("disease_type", "value"),
        Input("state_type", "value"),
        Input("disease_potato_variety", "value"),
        Input("store-uploaded-data", "data")
    ],
)
def prevalent_disease(season, disease, state, variety, data):
    fig = go.Figure()
    if data:
        df = pd.DataFrame(data)

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

    fig.update_layout(
        # title="Prevalent Disease",
        autosize=True,
        height=480,
        width=680,
        xaxis_title="Year",
        yaxis_title="Percentage of potato with {}".format(disease),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        xaxis={
            "autorange": True,
            "showline": True,
        },
        yaxis={
            "autorange": True,
            "showgrid": True,
            "showline": True,
            "type": "linear",
            # "zeroline": False,
        },

    )

    return fig
