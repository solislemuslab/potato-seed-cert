#from app import app

from tokenize import String
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
#year_list = list(range(2000, 2017))
# year_list.append("all")
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
                dbc.Label("S_GRW"),
                dcc.Dropdown(
                    id='multi_state',
                    # options=[{'label': i, 'value': i}
                    #          for i in sorted(df["S_STATE"].dropna().unique())],
                    value=['State Farm', 'Kamps Seed Farm'],
                    multi=True,
                    style={'width': '90%', 'margin-left': '5px'},
                    placeholder="Select states", ),
            ]),
        dbc.FormGroup(
            [
                dbc.Label("Inspection"),
                dcc.Dropdown(
                    id='parallel_inspection',
                    options=[{'label': i, 'value': i}
                             for i in ["1ST", "2ND", "Winter"]],
                    value=['1ST'],
                    style={'width': '90%', 'margin-left': '5px'},
                ),
            ]),
        dbc.FormGroup(
            [
                dbc.Label("Year Type"),
                dcc.Dropdown(
                    id='year_type',
                    # options=[{'label': i, 'value': i}
                    #          for i in sorted(df["S_STATE"].dropna().unique())],
                    options=[{'label': i, 'value': i}
                             for i in ["S_YR", "winter_CY"]],
                    value=['S_Year'],
                    style={'width': '90%', 'margin-left': '5px'},
                    placeholder="Select states", ),
            ]),
        dbc.FormGroup(
            [
                dbc.Label("Year"),
                dcc.Dropdown(
                    id="parallel_year",
                    # options=[
                    #    {"label": col, "value": col} for col in year_list
                    # ],
                    value="all",
                    style={'width': '90%', 'margin-left': '5px'},
                ),
            ]
        ),
    ]
)

RIGHT_PLOT = [
    dbc.CardHeader(
        dbc.Row([
                dbc.Col(
                    html.H5("Source comparison"),
                    width={"size": 4}
                ),

                dbc.Col(
                    [
                        dbc.Button("Help", color="primary",
                                   id="Pchi_square-open", className="mr-auto"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("State Comparison Plot"),
                                dbc.ModalBody(
                                    "The user selects State (multiple choices can be selected simultaneously), Inspection and Year, and the plot displays different y-axes (one per disease) with the disease prevalence. Different colored lines correspond to different states. Below we display a table with each selected state per row with the disease prevalence of all diseases as well as the color of the line in the last column."),
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


def callback_statecomparison(app):
    @app.callback(
        Output("multi_state", "options"),
        #Output("parallel_year", "options")
        # ],
        [
            Input("store-uploaded-data", "data")
        ]
    )
    def dropdown_option(data):
        try:
            if data:
                df = pd.DataFrame(data)
            #print("we have data1")
            # print(len(df.columns[11]))
            # print(df["S_GRW"].values)
            #df["S_GRW"] = df["S_GRW"].values.astype('string')
            #print("we have data2")
            options = [{'label': i, 'value': i}
                       for i in df["S_GRW"].dropna().unique()]
            #temp = df.loc[df["S_YR"] == int(year)].copy()
            options2 = [{'label': i, 'value': i}
                        for i in list(np.sort(df["S_YR"].unique()))]
            #year_list = list(np.sort(df["S_YR"].unique()))
            # print("dropdown_option")
            #print("we have data3")
            #print("options are: ")
            # print(options)

            return options
        except:
            #print("we don't have data")
            options = [{'label': '0', 'value': '0'}]
            options2 = [{'label': '0', 'value': '0'}]
            return options

    @app.callback(
        Output("parallel_year", "options"),
        [
            Input("store-uploaded-data", "data"),
            Input("multi_state", "value"),
            Input("year_type", "value")
        ]
    )
    def dropdown_option2(data, state, type):
        try:
            if data:
                df = pd.DataFrame(data)
            #print("we have data1")
            # print(len(df.columns[11]))
            # print(df["S_GRW"].values)
            #df["S_GRW"] = df["S_GRW"].values.astype('string')
            #print("we have data2")
            #print("now we have data")
            # print(state)
            temp = df.loc[df["S_GRW"] == state[0]].copy()

            #print("now we have temp")
            # rint(temp)
            if type == "S_YR":
                options2 = [{'label': i, 'value': i}
                            for i in list(np.sort(temp["S_YR"].unique()))]
                for s in state:
                    temp_s = df.loc[df["S_GRW"] == s].copy()
                    temp_s_Y = list(np.sort(temp_s["S_YR"].unique()))
                    for y in temp_s_Y:

                        if {'label': y, 'value': y} not in options2:
                            options2.append({'label': y, 'value': y})
                print(
                    "now we start to print final version of options2 in state comparison")
                print(options2)
            else:
                options2 = [{'label': i, 'value': i}
                            for i in list(np.sort(temp["winter_CY"].unique()))]
                for s in state:
                    temp_s = df.loc[df["S_GRW"] == s].copy()
                    temp_s_Y = list(np.sort(temp_s["winter_CY"].unique()))
                    for y in temp_s_Y:
                        #print("y is: ")
                        # print(y)
                        if {'label': y, 'value': y} not in options2:
                            options2.append({'label': y, 'value': y})
            #print("now we have option2")
            # print(options2)

            #year_list = list(np.sort(df["S_YR"].unique()))
            # print("dropdown_option")
            #print("we have data3")
            #print("options are: ")
            # print(options)

            return options2
        except:
            #print("we don't have data")
            options2 = [{'label': '0', 'value': '0'}]
            return options2

    @app.callback(
        [Output("parallel-graph-table", "data"),
         Output("parallel-graph-table", "columns"),
         Output("parallel-graph", "figure")],
        [Input("multi_state", "value"),
         Input("parallel_inspection", "value"),
         Input("year_type", "value"),
         Input("parallel_year", "value"),
         Input("store-uploaded-data", "data")
         ]
    )
    def parallel_plot(state, inspection, type, year, data):
        orig_state = state.copy()
        colors = ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "orange",
                  "darkviolet", "royalblue", "pink", "purple", "maroon", "silver", "lime"]
        colorscales = {np.linspace(0, 1, num=len(colors))[
            i]: color for i, color in enumerate(colors)}
        try:
            if data:
                df = pd.DataFrame(data)

            if type == "S_YR":
                if(year != "all"):
                    number_column = list(df.loc[df["S_YR"] == int(
                        year)].columns[df.columns.str.startswith("NO")])

                else:
                    number_column = list(
                        df.columns[df.columns.str.startswith("NO")])
                number_column = number_column + \
                    ["PLTCT_1", "PLTCT_2", "winter_LR",
                        "winter_MOS", "winter_MIX", "winter_PSTV"]

                if(year == "all"):
                    temp = df.copy()
                else:
                    temp = df.loc[df["S_YR"] == int(year)].copy()
            else:
                if(year != "all"):
                    number_column = list(df.loc[df["winter_CY"] == int(
                        year)].columns[df.columns.str.startswith("NO")])

                else:
                    number_column = list(
                        df.columns[df.columns.str.startswith("NO")])
                number_column = number_column + \
                    ["PLTCT_1", "PLTCT_2", "winter_LR",
                        "winter_MOS", "winter_MIX", "winter_PSTV"]

                if(year == "all"):
                    temp = df.copy()
                else:
                    temp = df.loc[df["winter_CY"] == int(year)].copy()
            # Encode each state to a number for coloring purpose
            unique_states = temp["S_GRW"].unique()
            #print("type is: ")
            # print(type(unique_states[0]))

            #unique_states = [str(x) for x in unique_states]
            # Remove errors in state, such as 2016
            #print("Unique_state is: ")
            # print(unique_states)
            unique_states = [
                state for state in unique_states if isinstance(state, str)]
            #print("New Unique_state is: ")
            # print(unique_states)
            # unique_states = [
            #   state for state in unique_states]
            # Construct a dictionary to assign an unique id to each state
            state_id = {state: np.linspace(0, 1, len(colors))[
                i] for i, state in enumerate(unique_states)}
            #print("State_id is: ")
            # print(state_id)
            temp = temp.groupby("S_GRW").sum()[number_column]
           # print("temp is: ")
            # print(temp)

            for column in temp.columns:
                if "1ST" in column:
                    new_column = column.replace("NO", "PCT")
                    temp[new_column] = temp[column] / temp["PLTCT_1"]
                elif "2ND" in column:
                    new_column = column.replace("NO", "PCT")
                    temp[new_column] = temp[column] / temp["PLTCT_2"]
                elif "winter" in column:
                    temp[column] = temp[column] / 100

            first_ins = ["PCT_LR_1ST", "PCT_MOS_1ST",
                         "PCT_ST_1ST", "PCT_MIX_1ST", "winter_LR", "winter_MOS", "winter_MIX", "winter_PSTV"]
            second_ins = ["PCT_LR_2ND", "PCT_MOS_2ND", "PCT_ST_2ND",
                          "PCT_MIX_2ND", "PCT_TOTV_2ND", "PCT_BRR_2ND"]

            # Add the state with minimum and maximum ID to fix the max id and min id value (Not dynamic)
            state = list(set(state))
            #+ ["CO", "MB"]

            scaled_color = [[np.linspace(0, 1, num=len(colors))[i], color]
                            for i, color in enumerate(colors)]

            # print(scaled_color)
            # maxval=[]
            # for st in unique_states:
            #    temp = temp.loc[st, first_ins].reset_index()
            #    temp["State_id"] = temp["S_STATE"].map(state_id)
            if inspection == "1ST":
                temp = temp.loc[state, first_ins].reset_index()
                temp["State_id"] = temp["S_GRW"].map(state_id)
                temp["line_color"] = temp["State_id"].map(colorscales)
                maxval = max(temp["PCT_LR_1ST"].max(), temp["PCT_MOS_1ST"].max(),
                             temp["PCT_ST_1ST"].max(
                ), temp["PCT_MIX_1ST"].max())
                minval = min(temp["PCT_LR_1ST"].min(), temp["PCT_MOS_1ST"].min(),
                             temp["PCT_ST_1ST"].min(
                ), temp["PCT_MIX_1ST"].min(),
                )

                # print(temp)
                fig = go.Figure(data=go.Parcoords(
                    line=dict(color=(temp["State_id"]),
                              colorscale=scaled_color),
                    # [[0, 'blue'], [0.5, 'lightseagreen'], [1, 'gold']]
                    dimensions=list([
                        # dict(range=[temp["PCT_LR_1ST"].min() * 0.5, temp["PCT_LR_1ST"].max() * 1.2],
                        #                 constraintrange = [4,8],
                        dict(range=[minval, maxval],
                             label='LR', values=temp["PCT_LR_1ST"]),
                        # dict(range=[temp["PCT_MOS_1ST"].min() * 0.5, temp["PCT_MOS_1ST"].max() * 1.2],
                        dict(range=[minval, maxval],
                             label='MOS', values=temp["PCT_MOS_1ST"]),
                        # dict(range=[temp["PCT_ST_1ST"].min(), temp["PCT_ST_1ST"].max()+0.5],
                        dict(range=[minval, maxval],
                             label="ST", values=temp["PCT_ST_1ST"]),
                        # dict(range=[temp["PCT_MIX_1ST"].min() * 0.5, temp["PCT_MIX_1ST"].max() * 1.2],
                        dict(range=[minval, maxval],
                             label='MIX', values=temp["PCT_MIX_1ST"]),

                    ])
                )
                )
            elif inspection == "2ND":
                temp = temp.loc[state, second_ins].reset_index()
                temp["State_id"] = temp["S_GRW"].map(state_id)
                temp["line_color"] = temp["State_id"].map(colorscales)
                #print(temp["PCT_MOS_2ND"].min(), temp["PCT_MOS_2ND"].max())
                # print(temp)
                maxval = max(temp["PCT_LR_2ND"].max(), temp["PCT_MOS_2ND"].max(),
                             temp["PCT_ST_2ND"].max(), temp["PCT_MIX_2ND"].max(), temp["PCT_TOTV_2ND"].max(), temp["PCT_BRR_2ND"].max())
                minval = min(temp["PCT_LR_2ND"].min(), temp["PCT_MOS_2ND"].min(),
                             temp["PCT_ST_2ND"].min(), temp["PCT_MIX_2ND"].min(), temp["PCT_TOTV_2ND"].min(), temp["PCT_BRR_2ND"].min())

                fig = go.Figure(data=go.Parcoords(
                    line=dict(color=(temp["State_id"]),
                              colorscale=scaled_color),
                    # [[0, 'blue'], [0.5, 'lightseagreen'], [1, 'gold']]
                    dimensions=list([
                        # dict(range=[temp["PCT_LR_2ND"].min() * 0.5, temp["PCT_LR_2ND"].max() * 1.2],
                        #                 constraintrange = [4,8],
                        #     label='LR', values=temp["PCT_LR_2ND"]),
                        dict(range=[minval, maxval],
                             #                 constraintrange = [4,8],
                             label='LR', values=temp["PCT_LR_2ND"]),
                        # dict(range=[temp["PCT_MOS_2ND"].min() * 0.5, temp["PCT_MOS_2ND"].max() * 1.2],
                        dict(range=[minval, maxval],
                             label='MOS', values=temp["PCT_MOS_2ND"]),
                        # dict(range=[temp["PCT_ST_2ND"].min(), temp["PCT_ST_2ND"].max() + 0.5],
                        dict(range=[minval, maxval],
                             label="ST", values=temp["PCT_ST_2ND"]),
                        # dict(range=[temp["PCT_MIX_2ND"].min() * 0.5, temp["PCT_MIX_2ND"].max() * 1.2],
                        dict(range=[minval, maxval],
                             label='MIX', values=temp["PCT_MIX_2ND"]),
                        # dict(range=[temp["PCT_TOTV_2ND"].min() * 0.5, temp["PCT_TOTV_2ND"].max() * 1.2],
                        dict(range=[minval, maxval],
                             label="TOTV", values=temp["PCT_TOTV_2ND"]),
                        # dict(range=[temp["PCT_BRR_2ND"].min() * 0.5, temp["PCT_BRR_2ND"].max()],
                        dict(range=[minval, maxval],
                             label="BRR", values=temp["PCT_BRR_2ND"]),
                    ])
                )
                )
            else:
                temp = temp.loc[state, first_ins].reset_index()
                temp["State_id"] = temp["S_GRW"].map(state_id)
                temp["line_color"] = temp["State_id"].map(colorscales)
                maxval = max(temp["winter_LR"].max(), temp["winter_MOS"].max(),
                             temp["winter_MIX"].max(), temp["winter_PSTV"].max())
                minval = min(temp["winter_LR"].min(), temp["winter_MOS"].min(),
                             temp["winter_MIX"].min(), temp["winter_PSTV"].min())

                # print(temp)
                fig = go.Figure(data=go.Parcoords(
                    line=dict(color=(temp["State_id"]),
                              colorscale=scaled_color),
                    # [[0, 'blue'], [0.5, 'lightseagreen'], [1, 'gold']]
                    dimensions=list([
                        dict(range=[minval, maxval],
                             label='Winter_LR', values=temp["winter_LR"]),
                        dict(range=[minval, maxval],
                             label='Winter_MOS', values=temp["winter_MOS"]),
                        dict(range=[minval, maxval],
                             label='Winter_MIX', values=temp["winter_MIX"]),
                        dict(range=[minval, maxval],
                             label='Winter_ST', values=temp["winter_PSTV"])

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
            #print("in state comparison")
            # print(data)
            # print("column")
            # print(columns)
            return data, columns, fig
        except:
            data = [{'S_GRW': 'State Farm', 'PCT_LR_2ND': 0.0, 'PCT_MOS_2ND': 0.00044198617922425323, 'PCT_ST_2ND': 0.0,
                     'PCT_MIX_2ND': 0.0, 'PCT_TOTV_2ND': 0.00044198617922425323, 'PCT_BRR_2ND': 0.0, 'State_id': 1.0, 'line_color': 'lime'}]
            columns = [{'name': 'S_GRW', 'id': 'S_GRW'}]
            fig = go.Figure()
            return data, columns, fig
