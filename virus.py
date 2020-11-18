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
                dbc.Label("Number of states"),
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

controls_3 = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Grower Number"),
                dcc.Dropdown(
                    id="grower_number",
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
                        dbc.Tab(label="Variety", tab_id="tab-2" ),
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

@app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return controls_1
    elif at == "tab-2":
        return controls_2
    elif at == "tab-3":
        return controls_3
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
        dbc.Row([
                dbc.Col(dbc.Card(html.H3(children='Comparison across inspection',
                                         className="text-center text-light bg-dark"), body=True, color="dark")
                , className="mt-4 mb-4", width= {"size": 8, "offset": 2} )
            ],align="center",),
        page_layout,
        dbc.Row([
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
                                {"label": col, "value": col} for col in ["summer", "winter", "summer and winter"]
                            ],
                            value= "summer",),
                    ]),
                dbc.FormGroup(
                    [
                        dbc.Label("Disease"),
                        dcc.Dropdown(
                            id="disease_type",
                            options=[
                                {"label": col, "value": col} for col in ["MOS","LR","MIX","ST","BRR"]
                            ],
                            value="LR",),
                    ]),
                dbc.FormGroup(
                    [
                        dbc.Label("State"),
                        dcc.Dropdown(
                            id="state_type",
                            options=[
                                {"label": col, "value": col} for col in sorted(df["S_STATE"].dropna().unique())
                            ],
                            value="WI",),
                    ]),
                dbc.FormGroup(
                    [
                        dbc.Label("Variety"),
                        dcc.Dropdown(
                            id="disease_potato_variety",
                            options=[
                                {"label": col, "value": col} for col in df["VARIETY"].dropna().unique()
                            ],
                            multi= True,
                            value= df["VARIETY"].value_counts()[:3].index ),
                    ]),
            ],body=True,)),
            dbc.Col(dcc.Graph(id="prevalence-graph"), md=8),
            ],
            align="center",),
        dbc.Row([
                dbc.Col(html.Div(
                                dbc.Card(
                                    html.H3(children='Sensitive and tolerant variety',
                                        className="text-center text-light bg-dark"), body=True, color="dark"),
                                ),
                        style = {"width": "100%",  "align-items": "center", "justify-content": "center"},
                        width= {"size": 8, "offset": 2})
                ]),


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

                ], body=True, )),
            dbc.Col(dcc.Graph(id="sensitivity-graph"), md=8),
        ],
            align="center", ),

        dbc.Row([
                dbc.Col(html.Div(
                                dbc.Card(
                                    html.H3(children='Comparison across state',
                                        className="text-center text-light bg-dark"), body=True, color="dark"),
                                ),
                        style = {"width": "100%",  "align-items": "center", "justify-content": "center"},
                        width= {"size": 8, "offset": 2})
                ]),
        dbc.Row([
            dbc.Col(dbc.Card(
                [
                    dbc.FormGroup(
                        [
                            dbc.Label("Season"),
                            dcc.Dropdown(
                                id='multi_state',
                                options=[{'label': i, 'value': i} for i in sorted(df["S_STATE"].dropna().unique())],
                                value=['WI', 'CO'],
                                multi=True,
                                style={'width': '70%', 'margin-left': '5px'},
                                placeholder="Select states", ),
                        ])],body=True)),

            dbc.Col(dcc.Graph(id="parallel-graph"), md=8),]),
        dbc.Row([
            dbc.Col(html.Div(
                dbc.Card(html.H3(children='Acres Rejection',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
            , className="mb-4"),style = {"width": "100%",  "align-items": "center", "justify-content": "center"},
            width= {"size": 8, "offset": 2}),

            ]),

        dcc.Dropdown(
            id='acres_rejection',
            options=[{'label': i, 'value': i} for i in sorted(df["LNAME"].dropna().unique())],
            value= df["LNAME"].dropna().unique()[:10],
            multi=True,
            style={'width': '70%', 'margin-left': '5px'}
        ),
        dbc.Row([
            dbc.Col(dcc.Graph(id='Acres_rej_bar'), width=6),
            dbc.Col(dcc.Graph(id='total_line_cases_or_deaths'), width=6)
        ]),
        ],

    fluid=True,
)


@app.callback(
    Output("state-graph", "figure"),
    [
        Input("state_number", "value"),
        Input("state_virus", "value"),
        Input("state_year", "value")
    ],
)
def state_plot(state_number, state_virus, state_year):
    number_column = list(df.columns[df.columns.str.startswith("NO")])
    number_column = number_column + ["PLTCT_1", "PLTCT_2", "S_YR", "CY"]
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
        title='Disease comparison across inspection',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='State',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(
            title='Percentage of potato with disease',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=1.0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )

    return fig


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

@app.callback(
    Output("sensitivity-graph", "figure"),
    [
        Input("season_inspection_vareity", "value"),
        Input("disease_type_variety", "value"),
        Input("potato_variety", "value"),
    ],
)
def prevalent_disease(season, disease, variety):
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

@app.callback(
    Output("parallel-graph", "figure"),
    [
        Input("multi_state", "value"),
    ],
)
def parallel_plot(state):
    number_column = list(df.columns[df.columns.str.startswith("NO")])
    number_column = number_column + ["PLTCT_1", "PLTCT_2"]
    number_column
    temp = df.copy()
    frequent_state = temp["S_STATE"].value_counts()[:10].index.to_list()
    temp = temp[temp["S_STATE"].isin(frequent_state)].groupby("S_STATE").sum()[number_column]
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
    temp = temp.loc[state]
    print(temp)
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
    return fig


@app.callback(
    Output("Acres_rej_bar", "figure"),
    [
        Input("acres_rejection", "value"),
    ],
)
def parallel_plot(lots):
    temp = df.groupby("LNAME").sum()[["ACRES", "AC_REJ", "winter_ACRES", "winter_AC_REJ"]]
    temp["rej_pct"] = temp["AC_REJ"] / temp["ACRES"]
    temp["winter_rej_pct"] = temp["winter_AC_REJ"] / temp["winter_ACRES"]
    temp = temp[temp.index.isin(lots)]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=temp.index,
        y=temp["rej_pct"],
        name='Summer',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=temp.index,
        y=temp["winter_rej_pct"],
        name='Winter',
        marker_color='lightsalmon'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)

    fig.update_layout(
        title='Rejected Lots',

        yaxis=dict(
            title='Rejection Percentage',
            titlefont_size=16,
            tickfont_size=14,
        ),
        xaxis=dict(
            title='Potato lots',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=1,
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