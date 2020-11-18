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

df = pd.read_csv("cleaned_potato.csv")
virus_list = ["LR", "ST", "MIX", "MOS"]
year_list = list(np.sort(df["S_YR"].unique()))
year_list.append("all")
category = ["S_STATE", "VARIETY", "S_G"]


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
                        {"label": col, "value": col} for col in range(1, 20)
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
                        {"label": col, "value": col} for col in range(1, 20)
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

controls_3 = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Grower Number"),
                dcc.Dropdown(
                    id="grower_number",
                    options=[
                        {"label": col, "value": col} for col in range(1, 20)
                    ],
                    value=10,
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Virus"),
                dcc.Dropdown(
                    id="grower_virus",
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
                    id="grower_year",
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

page_layout = dbc.Row(
    [
        dbc.Col(html.Div(
            [
                dbc.Tabs(
                    [
                        dbc.Tab(label="State", tab_id="tab-1"),
                        dbc.Tab(label="Variety", tab_id="tab-2"),
                        dbc.Tab(label="Grower", tab_id="tab-3"),
                    ],
                    id="tabs",
                    active_tab="tab-1",
                ),
                html.Div(id="content"),
            ]), md=4),
        dbc.Col(dcc.Graph(id="state-graph"), md=8),
    ],
    align="center",
)


# tabs = html.Div(
#     [
#         dbc.Tabs(
#             [
#                 dbc.Tab(label="State", tab_id="tab-1", href="/Virus/State"),
#                 dbc.Tab(label="Variety", tab_id="tab-2", href = "/Virus/Variety" ),
#                 dbc.Tab(label="Grower", tab_id="tab-3", href = "/Virus/Grower"),
#             ],
#             id="tabs",
#             active_tab="tab-1",
#         ),
#         html.Div(id="content"),
#     ]
# )

# @app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
# def switch_tab(at):
#     if at == "tab-1":
#         return controls_1
#     elif at == "tab-2":
#         return controls_2
#     elif at == "tab-3":
#         return controls_3
#     return html.P("This shouldn't ever be displayed...")

# @app.callback(Output("tabs-example-content", "children"), [Input("tabs", "active_tab")])
# def switch_tab(at):
#     if at == "tab-1":
#         return dbc.Row(
#         [
#             dbc.Col(html.Div(
#             [
#                 html.Div(id="content", children = controls_1),
#             ]), md=4),
#             dbc.Col(dcc.Graph(id="state-graph"), md=8),
#         ],
#             align="center",
#         )
#     elif at == "tab-2":
#         return dbc.Row(
#         [
#             dbc.Col(html.Div(
#             [
#                 dbc.Tabs(
#                     [
#                         dbc.Tab(label="State", tab_id="tab-1"),
#                         dbc.Tab(label="Variety", tab_id="tab-2"),
#                         dbc.Tab(label="Grower", tab_id="tab-3"),
#                     ],
#                     id="tabs",
#                     active_tab="tab-2",
#                 ),
#                 html.Div(id="content", children = controls_2),
#             ]), md=4),
#             dbc.Col(dcc.Graph(id="variety-graph"), md=8),
#         ],
#             align="center",
#         )
#     elif at == "tab-3":
#         return dbc.Row(
#         [
#             dbc.Col(html.Div(
#             [
#                 dbc.Tabs(
#                     [
#                         dbc.Tab(label="State", tab_id="tab-1"),
#                         dbc.Tab(label="Variety", tab_id="tab-2"),
#                         dbc.Tab(label="Grower", tab_id="tab-3"),
#                     ],
#                     id="tabs",
#                     active_tab="tab-3",
#                 ),
#                 html.Div(id="content", children = controls_3),
#             ]), md=4),
#             dbc.Col(dcc.Graph(id="grower-graph"), md=8),
#         ],
#             align="center",
#         )
#     return html.P("This shouldn't ever be displayed...")
@app.callback(Output("content", "children"),
              [Input("tabs", "active_tab")])
def switch_tab(tabs):
    if tabs == "tab-1":

        return controls_1


    elif tabs == "tab-2":

        return controls_2
    elif tabs == "tab-3":
        return controls_3
    print("d")
    return html.P("This shouldn't ever be displayed...")


@app.callback(Output("state-graph", "figure"),
              [Input("tabs", "active_tab"),
               Input("content", "children")
               ])
def switch_tab_graph(tabs, content):
    if tabs == "tab-1":
        return state_plot(state_number, state_virus, state_year)


    elif tabs == "tab-2":
        print("b")
        return variety_plot(variety_number, variety_virus, variety_year)
    elif tabs == "tab-3":
        print("c")
        return grower_plot(grower_number, grower_virus, grower_year)
    print("d")
    return html.P("This shouldn't ever be displayed...")
# virus_layout = dbc.Container(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(tabs, md=4),
#                 dbc.Col(dcc.Graph(id="state-graph"), md=8),
#             ],
#             align="center",
#         ),
#
#     ],
#     fluid=True,
# )

virus_layout = dbc.Container(
    [
        page_layout

    ],
    fluid=True,
)


def state_plot(state_number, state_virus, state_year="all"):
    number_column = list(df.columns[df.columns.str.startswith("NO")])
    number_column = number_column + ["PLTCT_1", "PLTCT_2"]
    temp = df.copy()
    frequent_state = temp["S_STATE"].value_counts()[:state_number].index.to_list()
    temp = temp[temp["S_STATE"].isin(frequent_state)].groupby("S_STATE").sum()[number_column]
    temp

    if state_year == "all":
        temp = temp
    else:
        temp = temp[temp["S_YR"] == state_year]

    for column in temp.columns:
        print(column)
        if "1ST" in column:
            #         print(column)
            new_column = column.replace("NO", "PCT")
            print(new_column)
            temp[new_column] = temp[column] / temp["PLTCT_1"]
        elif "2ND" in column:

            new_column = column.replace("NO", "PCT")
            #         print(new_column)
            temp[new_column] = temp[column] / temp["PLTCT_2"]
    temp = temp[temp.columns[(temp.columns.str.contains("PCT")) & (temp.columns.str.contains(state_virus))]]
    print(temp)
    fig = go.Figure()
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 0],
                         text=np.round(temp.iloc[:, 0], 5),
                         textposition='outside',
                         name=temp.columns[0],
                         marker_color='rgb(55, 83, 109)',
                         orientation="h"
                         ))
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 1],
                         text=np.round(temp.iloc[:, 1], 5),
                         textposition='outside',
                         name=temp.columns[1],
                         marker_color='rgb(26, 118, 255)',
                         orientation="h"
                         ))

    # fig.add_trace(go.Bar(x=temp.index,
    #                 y = temp.iloc[:,2],
    #                 text=np.round(temp.iloc[:,2],3),
    #                 textposition='outside',
    #                 name=temp.columns[2],
    #                 marker_color='crimson'
    #                 ))

    fig.update_layout(
        title='US Export of Plastic Scrap',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='USD (millions)',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    return fig


def variety_plot(variety_number, variety_virus, variety_year="all"):
    number_column = list(df.columns[df.columns.str.startswith("NO")])
    number_column = number_column + ["PLTCT_1", "PLTCT_2"]
    temp = df.copy()
    frequent_state = temp["VARIETY"].value_counts()[:variety_number].index.to_list()
    temp = temp[temp["VARIETY"].isin(frequent_state)].groupby("VARIETY").sum()[number_column]
    temp

    if variety_year == "all":
        temp = temp
    else:
        temp = temp[temp["S_YR"] == variety_year]

    for column in temp.columns:
        print(column)
        if "1ST" in column:
            #         print(column)
            new_column = column.replace("NO", "PCT")
            print(new_column)
            temp[new_column] = temp[column] / temp["PLTCT_1"]
        elif "2ND" in column:

            new_column = column.replace("NO", "PCT")
            #         print(new_column)
            temp[new_column] = temp[column] / temp["PLTCT_2"]
    temp = temp[temp.columns[(temp.columns.str.contains("PCT")) & (temp.columns.str.contains(variety_virus))]]
    print(temp)
    fig = go.Figure()
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 0],
                         text=np.round(temp.iloc[:, 0], 5),
                         textposition='outside',
                         name=temp.columns[0],
                         marker_color='rgb(55, 83, 109)',
                         orientation="h"
                         ))
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 1],
                         text=np.round(temp.iloc[:, 1], 5),
                         textposition='outside',
                         name=temp.columns[1],
                         marker_color='rgb(26, 118, 255)',
                         orientation="h"
                         ))

    # fig.add_trace(go.Bar(x=temp.index,
    #                 y = temp.iloc[:,2],
    #                 text=np.round(temp.iloc[:,2],3),
    #                 textposition='outside',
    #                 name=temp.columns[2],
    #                 marker_color='crimson'
    #                 ))

    fig.update_layout(
        title='US Export of Plastic Scrap',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='USD (millions)',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    return fig


def grower_plot(grower_number, grower_virus, grower_year="all"):
    number_column = list(df.columns[df.columns.str.startswith("NO")])
    number_column = number_column + ["PLTCT_1", "PLTCT_2"]
    temp = df.copy()
    frequent_grower = temp["S_G"].value_counts()[:grower_number].index.to_list()
    temp = temp[temp["S_G"].isin(frequent_grower)].groupby("S_G").sum()[number_column]
    temp

    if grower_year == "all":
        temp = temp
    else:
        temp = temp[temp["S_YR"] == grower_year]

    for column in temp.columns:
        print(column)
        if "1ST" in column:
            #         print(column)
            new_column = column.replace("NO", "PCT")
            print(new_column)
            temp[new_column] = temp[column] / temp["PLTCT_1"]
        elif "2ND" in column:

            new_column = column.replace("NO", "PCT")
            #         print(new_column)
            temp[new_column] = temp[column] / temp["PLTCT_2"]
    temp = temp[temp.columns[(temp.columns.str.contains("PCT")) & (temp.columns.str.contains(grower_virus))]]
    print(temp)
    fig = go.Figure()
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 0],
                         text=np.round(temp.iloc[:, 0], 5),
                         textposition='outside',
                         name=temp.columns[0],
                         marker_color='rgb(55, 83, 109)',
                         orientation="h"
                         ))
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 1],
                         text=np.round(temp.iloc[:, 1], 5),
                         textposition='outside',
                         name=temp.columns[1],
                         marker_color='rgb(26, 118, 255)',
                         orientation="h"
                         ))

    # fig.add_trace(go.Bar(x=temp.index,
    #                 y = temp.iloc[:,2],
    #                 text=np.round(temp.iloc[:,2],3),
    #                 textposition='outside',
    #                 name=temp.columns[2],
    #                 marker_color='crimson'
    #                 ))

    fig.update_layout(
        title='US Export of Plastic Scrap',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='USD (millions)',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    return fig
