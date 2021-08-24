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

# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../datasets").resolve()
# df = pd.read_csv(DATA_PATH.joinpath("cleaned_potato.csv"))


virus_list = ["LR","ST","MIX","MOS"]
# year_list = list(np.sort(df["S_YR"].unique()))
year_list = list(range(2000, 2017))
year_list.append("all")
category = ["S_STATE","VARIETY","S_G"]

# def find_virus_columns(virus):
#     return [x for x in df.columns.tolist() if
#             re.compile(r'[SR1|SR2|winter]_P*{virus}V*$'.format(virus=virus)).search(x)]


LEFT_COLUMN = dbc.Jumbotron(
    [
        html.H4(children="Data Selection", className="display-5"),
        html.Hr(className="my-2"),
        dbc.FormGroup(
                        [
                            dbc.Label("Inspection"),
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
                    # options=[
                    #     {"label": col, "value": col} for col in df["VARIETY"].dropna().unique()
                    # ],
                    multi= True)
                    # value= df["VARIETY"].value_counts()[:10].index ),
            ]),
        dbc.FormGroup(
            [
                dbc.Label("Year"),
                dcc.Dropdown(
                    id="sensitive_year",
                    options=[
                        {"label": col, "value": col} for col in year_list
                    ],
                    value="2007",
                ),
            ]
                ),
    ]
)

@app.callback(
    [Output("potato_variety", "options"),
    Output("potato_variety", "value")],
    [
        Input("store-uploaded-data", "data")
    ],
)
def left_column_dropdown(data):
    if data:
        df = pd.DataFrame(data)

    options = [
                  {"label": col, "value": col} for col in df["VARIETY"].dropna().unique()
              ]
    value = df["VARIETY"].value_counts()[:10].index

    return options, value

RIGHT_PLOT = [
    dbc.CardHeader(
        dbc.Row([
            dbc.Col(
                html.H5("Disease by variety"),
                width={"size": 4}
            ),
            dbc.Col(
                [
                    dbc.Button("Help", color="primary",
                               id="Pchi_square-open", className="mr-auto"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Disease Prevalence by Variety"),
                            dbc.ModalBody(
                                "The user selects Inspection, Disease, Variety (multiple choices can be selected simultaneously) and Year and the plot displays the disease prevalence in the y-axis and the potato variety in the x-axis."),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="Pchi_square-close",
                                           className="ml-auto")
                            ),
                        ],
                        id="Pchi_square-message",
                    )],
                width={"size": 2, "offset": 6}
            )
        ]),
        ),
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

                    dcc.Graph(id="sensitivity-graph"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

variety_layout = html.Div(
        [
            dbc.Row([
                dbc.Col(LEFT_COLUMN, md = 4 ,style={"height": "100%"},),
                dbc.Col(
                    dbc.Card(RIGHT_PLOT), md=8, style={"height": "100%"},)
            ], style={"marginTop": 30}, align="center", ),
            html.P(
                "Note: μ=1×10^(-6)",
                className="font-weight-lighter",
                style={"padding-top": '20px', "font-size": '20px', 'font-style': 'italic'}
            ),
        ])


@app.callback(
    Output("sensitivity-graph", "figure"),
    [
        Input("season_inspection_vareity", "value"),
        Input("disease_type_variety", "value"),
        Input("potato_variety", "value"),
        Input("sensitive_year","value"),
        Input("store-uploaded-data", "data")
    ],
)
def sensitivity_graph(season, disease, variety, year, data):
    if data:
        df = pd.DataFrame(data)
    fig = go.Figure()
    #print(frequent_varity)
    frequent_variety = df["VARIETY"].value_counts()[:20].index
    print(frequent_variety)
    if "summer" in season:
        if(year=="all"):
            temp = df[df["VARIETY"].isin(variety)].groupby("VARIETY").sum()[
            ["PLTCT_2", "NO_MOS_2ND", "NO_LR_2ND", "NO_MIX_2ND", "NO_ST_2ND", "NO_BRR_2ND"]]
        else:
             temp = df.loc[df["S_YR"] == int(year)][df["VARIETY"].isin(variety)].groupby("VARIETY").sum()[
            ["PLTCT_2", "NO_MOS_2ND", "NO_LR_2ND", "NO_MIX_2ND", "NO_ST_2ND", "NO_BRR_2ND"]]

        for column in temp.columns[1:]:
            new_column = column.replace("NO", "PCT")
            temp[new_column] = temp[column] / temp.iloc[:, 0]

        disease_type = [x for x in temp.columns if x.find(disease) != -1]

        fig.add_trace(go.Bar(x=temp.index, y=temp[disease_type[1]],
                                 # mode='lines+markers',
                                 name=disease_type[1] + " " + "summer"))

    if "winter" in season:
        if(year=="all"):
            temp = df[df["VARIETY"].isin(variety)].groupby("VARIETY").sum()[
            ["winter_PLANTCT", "winter_MOSN", "winter_LRN", "winter_MXDN"]]
        else:
            temp = df.loc[df["S_YR"] == int(year)][df["VARIETY"].isin(variety)].groupby("VARIETY").sum()[
            ["winter_PLANTCT", "winter_MOSN", "winter_LRN", "winter_MXDN"]]
        for column in temp.columns[1:]:
            new_column = column.replace("N", "_PCT")
            temp[new_column] = temp[column] / temp.iloc[:, 0]

        disease_type = [x for x in temp.columns if x.find(disease) != -1]

        fig.add_trace(go.Bar(x=temp.index, y=temp[disease_type[1]],
                                 # mode='lines+markers',
                                 name=disease_type[1] + " " + "winter"))
    fig.update_layout(showlegend=True)
    fig.update_layout(
        # title="Sensitive/tolerant variety",
        xaxis_title="Potato Variety",
        yaxis_title="Percentage of potato with {}".format(disease),
    )

    fig.update_layout(legend=dict(
        yanchor="top",
        y=-0.45,
        xanchor="center",
        x=0.5
    ))

    # fig.add_annotation(x=4, y=4,
    #                    text="Text annotation without arrow",


    return fig