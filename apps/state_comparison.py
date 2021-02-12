
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



state_comparison_layout = html.Div(
        [dbc.Row([
                dbc.Col(html.Div(
                                dbc.Card(
                                    html.H3(children='Comparison across state',
                                        className="text-center text-light bg-dark"), body=True, color="dark"),
                                ),
                        style = {"width": "100%",  "align-items": "center", "justify-content": "center"},
                        width= {"size": 8, "offset": 2})
                ]),

        html.Br(),
        dbc.Row([
                dbc.Col(html.Div(
                    dash_table.DataTable(
                        id="parallel-graph-table",

                        style_header={'backgroundColor': '#25597f', 'color': 'white'},
                        style_cell={
                            'backgroundColor': 'white',
                            'color': 'black',
                            'fontSize': 13,
                            'font-family': 'Nunito Sans'}
                    ),
                        ),
                    style={"width": "100%", "align-items": "center", "justify-content": "center"},
                    width={"size": 8, "offset": 4})
                ]),
            dbc.Row([
                dbc.Col(dbc.Card(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("State"),
                                dcc.Dropdown(
                                    id='multi_state',
                                    options=[{'label': i, 'value': i} for i in sorted(df["S_STATE"].dropna().unique())],
                                    value=['WI', 'CO'],
                                    multi=True,
                                    style={'width': '70%', 'margin-left': '5px'},
                                    placeholder="Select states", ),
                            ]),
                        dbc.FormGroup(
                            [
                                dbc.Label("Inspection"),
                                dcc.Dropdown(
                                    id='parallel_inspection',
                                    options=[{'label': i, 'value': i} for i in ["1ST", "2ND"]],
                                    value=['1ST'],
                                    style={'width': '70%', 'margin-left': '5px'},
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
                                ),
                            ]
                        ),
                    ], body=True)),

                dbc.Col([
                    dcc.Graph(id="parallel-graph")], md=8), ]),
        ])


@app.callback(
    [Output("parallel-graph-table", "data"),
    Output("parallel-graph-table", "columns"),
    Output("parallel-graph", "figure")],
    [Input("multi_state", "value"),
     Input("parallel_inspection", "value")]
)
def parallel_plot(state, inspection):
    number_column = list(df.columns[df.columns.str.startswith("NO")])
    number_column = number_column + ["PLTCT_1", "PLTCT_2"]
    number_column
    temp = df.copy()
    # frequent_state = temp["S_STATE"].value_counts()[:10].index.to_list()
    temp = temp.groupby("S_STATE").sum()[number_column]
    temp

    for column in temp.columns:
        #     print(column)
        if "1ST" in column:

            new_column = column.replace("NO", "PCT")
            print(new_column)
            temp[new_column] = temp[column] / temp["PLTCT_1"]
        elif "2ND" in column:

            new_column = column.replace("NO", "PCT")
            #         print(new_column)
            temp[new_column] = temp[column] / temp["PLTCT_2"]
    first_ins = ["PCT_LR_1ST", "PCT_MOS_1ST", "PCT_ST_1ST", "PCT_MIX_1ST"]
    second_ins = ["PCT_LR_2ND", "PCT_MOS_2ND", "PCT_ST_2ND", "PCT_MIX_2ND", "PCT_TOTV_2ND", "PCT_BRR_2ND"]


    print(temp)

    first_ins = ["PCT_LR_1ST", "PCT_MOS_1ST", "PCT_ST_1ST", "PCT_MIX_1ST"]
    second_ins = ["PCT_LR_2ND", "PCT_MOS_2ND", "PCT_ST_2ND", "PCT_MIX_2ND", "PCT_TOTV_2ND", "PCT_BRR_2ND"]

    if inspection == "1ST":
        temp = temp.loc[state, first_ins].reset_index()
        fig = go.Figure(data=
        go.Parcoords(
            line=dict(color=temp["PCT_MOS_1ST"],
                      colorscale=[[0, 'purple'], [0.5, 'lightseagreen'], [1, 'gold']]),
            dimensions=list([
                dict(range=[temp["PCT_LR_1ST"].min() * 0.5, temp["PCT_LR_1ST"].max() * 1.2],
                     #                 constraintrange = [4,8],
                     label='LR', values=temp["PCT_LR_1ST"]),
                dict(range=[temp["PCT_MOS_1ST"].min() * 0.5, temp["PCT_MOS_1ST"].max() * 1.2],
                     label='MOS', values=temp["PCT_MOS_1ST"]),
                dict(range=[temp["PCT_ST_1ST"].min() * 0.5, temp["PCT_ST_1ST"].max() * 1.2],
                     label="ST", values=temp["PCT_ST_1ST"]),
                dict(range=[temp["PCT_MIX_1ST"].min() * 0.5, temp["PCT_MIX_1ST"].max() * 1.2],
                     label='MIX', values=temp["PCT_MIX_1ST"])
            ])
        )
        )
    else:
        temp = temp.loc[state, second_ins].reset_index()
        fig = go.Figure(data=
        go.Parcoords(
            line=dict(color=temp["PCT_MOS_2ND"],
                      colorscale=[[0, 'purple'], [0.5, 'lightseagreen'], [1, 'gold']]),
            dimensions=list([
                dict(range=[temp["PCT_LR_2ND"].min() * 0.5, temp["PCT_LR_2ND"].max() * 1.2],
                     #                 constraintrange = [4,8],
                     label='LR', values=temp["PCT_LR_2ND"]),
                dict(range=[temp["PCT_MOS_2ND"].min() * 0.5, temp["PCT_MOS_2ND"].max() * 1.2],
                     label='MOS', values=temp["PCT_MOS_2ND"]),
                dict(range=[temp["PCT_ST_2ND"].min() * 0.5, temp["PCT_ST_2ND"].max() * 1.2],
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

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    fig.update_layout(showlegend=True)

    # fig.update_traces(mode="markers+lines")
    return data, columns, fig

