
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


virus_list = ["LR", "ST", "MIX", "MOS"]
# year_list = list(np.sort(df["S_YR"].unique()))
year_list = list(range(2000, 2017))
year_list.append("all")
category = ["S_STATE", "VARIETY", "S_G"]


# def find_virus_columns(virus):
#     return [x for x in df.columns.tolist() if
#             re.compile(r'[SR1|SR2|winter]_P*{virus}V*$'.format(virus=virus)).search(x)]


LEFT_COLUMN = dbc.Jumbotron(
    [
        html.H4(children="Data Selection", className="display-5"),
        html.Hr(className="my-2"),
        dbc.FormGroup(
            [
                dbc.Label("State"),
                dcc.Dropdown(
                    id='multi_state',
                    # options=[{'label': i, 'value': i}
                    #          for i in sorted(df["S_STATE"].dropna().unique())],
                    value=['MB', 'CO'],
                    multi=True,
                    style={'width': '90%', 'margin-left': '5px'},
                    placeholder="Select states", ),
            ]),
        dbc.FormGroup(
            [
                dbc.Label("Inspection"),
                dcc.Dropdown(
                    id='parallel_inspection',
                    options=[{'label': i, 'value': i} for i in ["1ST", "2ND"]],
                    value=['1ST'],
                    style={'width': '90%', 'margin-left': '5px'},
                ),
            ]),
        dbc.FormGroup(
            [
                dbc.Label("Year"),
                dcc.Dropdown(
                    id="parallel_year",
                    options=[
                        {"label": col, "value": col} for col in year_list
                    ],
                    value="all",
                    style={'width': '90%', 'margin-left': '5px'},
                ),
            ]
        ),
    ]
)

@app.callback(
    Output("multi_state", "options"),
    [
     Input("store-uploaded-data", "data")
     ]
)
def dropdown_option(data):
    if data:
        df = pd.DataFrame(data)

    options = [{'label': i, 'value': i}
               for i in sorted(df["S_STATE"].dropna().unique())]

    return options

RIGHT_PLOT = [
    dbc.CardHeader(
        dbc.Row([
            dbc.Col(
                html.H5("State comparison"),
                width={"size": 4}
            ),

            dbc.Col(
                [
                    dbc.Button("Help", color="primary",
                               id="Pchi_square-open", className="mr-auto"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Person's Chi-Square Test"),
                            dbc.ModalBody(
                                "This is the content of the Person's Chi-Square Test"),
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

                    dcc.Graph(id="parallel-graph"),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

state_comparison_layout = html.Div(
    [
        dbc.Row([
                dbc.Col(LEFT_COLUMN, align="center", md=4),
                dbc.Col(
                    dbc.Card(RIGHT_PLOT), md=8)
                ], style={"marginTop": 30}, align="center", ),
        html.Br(),
        dbc.Row([
                dbc.Col(html.Div(
                    dash_table.DataTable(
                        id="parallel-graph-table",

                        style_header={
                            'backgroundColor': '#25597f', 'color': 'white'},
                        style_cell={
                            'backgroundColor': 'white',
                            'color': 'black',
                            'fontSize': 13,
                            'font-family': 'Nunito Sans'}
                    ),
                ),
                    style={"width": "100%", "align-items": "center",
                           "justify-content": "center"},
                    width={"size": 8, "offset": 1})
                ]),
        html.P(
            "Note: μ=1×10^(-6)，n=1×10^(-9)",
            className="font-weight-lighter", style={"padding-top": '20px', "font-size": '20px', 'font-style': 'italic'}
        ),
    ],

)


@app.callback(
    [Output("parallel-graph-table", "data"),
     Output("parallel-graph-table", "columns"),
     Output("parallel-graph", "figure")],
    [Input("multi_state", "value"),
     Input("parallel_inspection", "value"),
     Input("parallel_year","value"),
     Input("store-uploaded-data", "data")
     ]
)
def parallel_plot(state, inspection,year, data):
    orig_state = state.copy()
    colors = ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "orange", "darkviolet", "royalblue", "pink", "purple", "maroon", "silver", "lime"]
    colorscales = {np.linspace(0, 1, num = len(colors))[i]: color for i, color in enumerate(colors)}
    if data:
        df = pd.DataFrame(data)

    if(year!="all"):
        number_column = list(df.loc[df["S_YR"] == int(year)].columns[df.columns.str.startswith("NO")])

    else:
        number_column = list(df.columns[df.columns.str.startswith("NO")])
    number_column = number_column + ["PLTCT_1", "PLTCT_2"]

    if(year=="all"):
        temp=df.copy()
    else:
        temp = df.loc[df["S_YR"] == int(year)].copy()

    # Encode each state to a number for coloring purpose
    unique_states = temp["S_STATE"].unique()
    # Remove errors in state, such as 2016
    unique_states = [state for state in unique_states if isinstance(state, str)]

    # Construct a dictionary to assign an unique id to each state
    state_id = {state: np.linspace(0, 1, len(colors))[i] for i, state in enumerate(unique_states)}

    print(state_id)

    temp = temp.groupby("S_STATE").sum()[number_column]

    for column in temp.columns:
        if "1ST" in column:
            new_column = column.replace("NO", "PCT")
            temp[new_column] = temp[column] / temp["PLTCT_1"]
        elif "2ND" in column:
            new_column = column.replace("NO", "PCT")
            temp[new_column] = temp[column] / temp["PLTCT_2"]

    first_ins = ["PCT_LR_1ST", "PCT_MOS_1ST", "PCT_ST_1ST", "PCT_MIX_1ST"]
    second_ins = ["PCT_LR_2ND", "PCT_MOS_2ND", "PCT_ST_2ND",
                  "PCT_MIX_2ND", "PCT_TOTV_2ND", "PCT_BRR_2ND"]

    # Add the state with minimum and maximum ID to fix the max id and min id value (Not dynamic)
    state = list(set(state + ["CO", "MB"]))

    scaled_color = [[np.linspace(0, 1, num=len(colors))[i], color] for i, color in enumerate(colors)]

    print(scaled_color)

    if inspection == "1ST":
        print(temp)
        temp = temp.loc[state, first_ins].reset_index()
        temp["State_id"] = temp["S_STATE"].map(state_id)
        temp["line_color"] = temp["State_id"].map(colorscales)
        print(temp)
        fig = go.Figure(data=go.Parcoords(
            line=dict(color=(temp["State_id"]),
                      colorscale = scaled_color),
            # [[0, 'blue'], [0.5, 'lightseagreen'], [1, 'gold']]
            dimensions=list([
                dict(range=[temp["PCT_LR_1ST"].min() * 0.5, temp["PCT_LR_1ST"].max() * 1.2],
                     #                 constraintrange = [4,8],
                     label='LR', values=temp["PCT_LR_1ST"]),
                dict(range=[temp["PCT_MOS_1ST"].min() * 0.5, temp["PCT_MOS_1ST"].max() * 1.2],
                     label='MOS', values=temp["PCT_MOS_1ST"]),
                dict(range=[temp["PCT_ST_1ST"].min(), temp["PCT_ST_1ST"].max()+0.5],
                     label="ST", values=temp["PCT_ST_1ST"]),
                dict(range=[temp["PCT_MIX_1ST"].min() * 0.5, temp["PCT_MIX_1ST"].max() * 1.2],
                     label='MIX', values=temp["PCT_MIX_1ST"])
            ])
        )
        )
    else:
        temp = temp.loc[state, second_ins].reset_index()
        temp["State_id"] = temp["S_STATE"].map(state_id)
        temp["line_color"] = temp["State_id"].map(colorscales)
        print(temp)
        fig = go.Figure(data=go.Parcoords(
            line=dict(color=(temp["State_id"]),
                      colorscale=scaled_color),
            # [[0, 'blue'], [0.5, 'lightseagreen'], [1, 'gold']]
            dimensions=list([
                dict(range=[temp["PCT_LR_2ND"].min() * 0.5, temp["PCT_LR_2ND"].max() * 1.2],
                     #                 constraintrange = [4,8],
                     label='LR', values=temp["PCT_LR_2ND"]),
                dict(range=[temp["PCT_MOS_2ND"].min() * 0.5, temp["PCT_MOS_2ND"].max() * 1.2],
                     label='MOS', values=temp["PCT_MOS_2ND"]),
                dict(range=[temp["PCT_ST_2ND"].min(), temp["PCT_ST_2ND"].max() + 0.5],
                     label="ST", values=temp["PCT_ST_2ND"]),
                dict(range=[temp["PCT_MIX_2ND"].min() * 0.5, temp["PCT_MIX_2ND"].max() * 1.2],
                     label='MIX', values=temp["PCT_MIX_2ND"]),
                dict(range=[temp["PCT_TOTV_2ND"].min() * 0.5, temp["PCT_TOTV_2ND"].max() * 1.2],
                     label="TOTV", values=temp["PCT_TOTV_2ND"]),
                dict(range=[temp["PCT_BRR_2ND"].min() * 0.5, temp["PCT_BRR_2ND"].max() * 1.2],
                     label="BRR", values=temp["PCT_BRR_2ND"]),
            ])
        )
        )

    # temp = temp[temp["S_STATE"].isin(orig_state)]
    data = temp.to_dict('records')
    columns = [{'name': i, 'id': i} for i in temp.columns]

    # return data, columns

    # fig = go.Figure(data=
    # go.Parcoords(
    #     line=dict(color=temp["PCT_MOS_1ST"],
    #               colorscale=[[0, 'purple'], [0.5, 'lightseagreen'], [1, 'gold']]),
    #     dimensions=list([
    #         dict(range=[temp["PCT_LR_1ST"].min() * 0.5, temp["PCT_LR_1ST"].max() * 1.2],
    #              #                 constraintrange = [4,8],
    #              label='LR', values=temp["PCT_LR_1ST"]),
    #         dict(range=[temp["PCT_MOS_1ST"].min() * 0.5, temp["PCT_MOS_1ST"].max() * 1.2],
    #              label='MOS', values=temp["PCT_MOS_1ST"]),
    #         dict(range=[temp["PCT_ST_1ST"].min() * 0.5, temp["PCT_ST_1ST"].max() * 1.2],
    #              label="ST", values=temp["PCT_ST_1ST"]),
    #         dict(range=[temp["PCT_MIX_1ST"].min() * 0.5, temp["PCT_MIX_1ST"].max() * 1.2],
    #              label='MIX', values=temp["PCT_MIX_1ST"])
    #     ])
    # )
    # )

    # fig.update_layout(
    #     plot_bgcolor='white',
    #     paper_bgcolor='white'
    # )

    # fig.update_traces(mode="markers+lines")
    return data, columns, fig
