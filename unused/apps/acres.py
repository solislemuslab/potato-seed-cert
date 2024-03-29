import plotly.graph_objects as go
import re
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import pathlib


# get relative data folder
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../datasets").resolve()
# df = pd.read_csv(DATA_PATH.joinpath("cleaned_potato.csv"))
# df = df.sort_values(by=['AC_REJ'], ascending=False)

virus_list = ["LR", "ST", "MIX", "MOS"]
# year_list = list(np.sort(df["S_YR"].unique()))
year_list = list(range(2000, 2017))
year_list.append("all")
category = ["S_STATE", "VARIETY", "S_G"]


# def find_virus_columns(virus):
#     return [x for x in df.columns.tolist() if
#             re.compile(r'[SR1|SR2|winter]_P*{virus}V*$'.format(virus=virus)).search(x)]
TOP_ROW = dbc.Jumbotron(
    [
        dbc.Row([
            dbc.Col(
                html.H5("Data Selection"),
                width={"size": 4}
            ),

            dbc.Col(
                [
                    dbc.Button("Help", color="primary",
                               id="Pchi_square-open", className="mr-auto"),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Percentage of rejected lots"),
                            dbc.ModalBody(
                                "The user selects the Lot Name for the figure on the left and the Potato Variety for the figure on the right. In both figures, we show the percentage of rejection acres for both summer and winter inspections (different bar color)."),
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
        # html.H4(children="Data Selection", className="display-5"),
        html.Hr(className="my-2"),
        dbc.Row([
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Lot Name"),
                        dcc.Dropdown(
                            id='acres_rejection',
                            # options=[{'label': i, 'value': i}
                            #          for i in sorted(df["LNAME"].dropna().unique())],
                            # value=df["LNAME"].dropna().unique()[:10],
                            multi=True,
                            style={'width': '70%', 'margin-left': '5px'}
                        )
                    ]),
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Label("Potato Variety"),
                        dcc.Dropdown(
                            id='acres_rejection_variety',
                            # options=[{'label': i, 'value': i}
                            #          for i in sorted(df["VARIETY"].dropna().unique())],
                            # value=df["VARIETY"].dropna().unique()[:10],
                            multi=True,
                            style={'width': '70%', 'margin-left': '5px'}
                        )
                    ]),

            ),
        ]),
    ]
)

acres_layout = html.Div([
    html.Br(),


    TOP_ROW,
    dbc.Row([
            dbc.Col(dcc.Graph(id='Acres_rej_bar'), width=6),

            dbc.Col(dcc.Graph(id='Acres_rej_byVariety_bar'), width=6),
            ]),

])


def acres_callback(app):
    @app.callback(
        [Output("acres_rejection", "options"),
         Output("acres_rejection", "value"),
         Output("acres_rejection_variety", "options"),
         Output("acres_rejection_variety", "value")
         ],
        [
            Input("store-uploaded-data", "data")
        ],
    )
    def acre_rejection(data):
        try:
            if data:
                df = pd.DataFrame(data)
                df = df.sort_values(by=['AC_REJ'], ascending=False)
            acre_options = [{'label': i, 'value': i}
                            for i in sorted(df["LNAME"].dropna().unique())]
            # print("acre_options")
            # print(acre_options)
            acre_value = df["LNAME"].dropna().unique()[:10]
            # print(acre_value)
            variety_options = [{'label': i, 'value': i}
                               for i in sorted(df["VARIETY"].dropna().unique())]
            variety_value = df["VARIETY"].dropna().unique()[:10]

            return acre_options, acre_value, variety_options, variety_value
        except:
            acre_options = [{'label': 'Baginksi Farms Inc.',
                             'value': 'Baginksi Farms Inc.'}]
            acre_value = ["A", "B"]
            variety_options = [
                {'label': 'Baginksi Farms Inc.', 'value': 'Baginksi Farms Inc.'}]
            variety_value = ["A", "B"]
            return acre_options, acre_value, variety_options, variety_value
            # pass

    @app.callback(
        Output("Acres_rej_bar", "figure"),
        # Output('Acres_rej_segment', 'figure') ],
        [
            Input("acres_rejection", "value"),
            Input("store-uploaded-data", "data")
        ],
    )
    def acre_rejection(lots, data):
        try:
            if data:
                df = pd.DataFrame(data)
                df = df.sort_values(by=['AC_REJ'], ascending=False)
            temp = df.groupby("LNAME").sum()[
                ["ACRES", "AC_REJ", "winter_ACRES", "winter_AC_REJ"]]
            temp["rej_pct"] = temp["AC_REJ"] / temp["ACRES"]
            temp["winter_rej_pct"] = temp["winter_AC_REJ"] / \
                temp["winter_ACRES"]
            temp = temp[temp.index.isin(lots)]
            # print(temp)
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
                title='Rejected Lots=ACRE_REJ/ACRE_TOTAL',

                yaxis=dict(
                    title='Rejection Percentage',
                    titlefont_size=16,
                    tickfont_size=14,
                ),
                xaxis=dict(
                    title='Potato Lot Name',
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
                # gap between bars of adjacent location coordinates.
                bargap=0.15,
                # gap between bars of the same location coordinate.
                bargroupgap=0.1
            )

            return fig
        except:
            fig = go.Figure()
            return fig

    @app.callback(
        Output("Acres_rej_byVariety_bar", "figure"),
        # Output('Acres_rej_segment', 'figure') ],
        [
            Input("acres_rejection_variety", "value"),
            Input("store-uploaded-data", "data")
        ],
    )
    def acre_rejection(lots, data):
        try:
            if data:
                df = pd.DataFrame(data)
                df = df.sort_values(by=['AC_REJ'], ascending=False)
            temp = df.groupby("VARIETY").sum()[
                ["ACRES", "AC_REJ", "winter_ACRES", "winter_AC_REJ"]]
            # print(temp)
            temp["rej_pct"] = temp["AC_REJ"] / temp["ACRES"]
            temp["winter_rej_pct"] = temp["winter_AC_REJ"] / \
                temp["winter_ACRES"]
            temp = temp[temp.index.isin(lots)]
            # print(temp)
            # print(temp.index)
            # for i in temp["rej_pct"]:
            #    if i != 0:
            #        print("hello")
            #        print(i)
            # print(type(temp['ACRES']))
            # print(temp["ACRES"])
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
                title='Rejected Lots=ACRE_REJ/ACRE_TOTAL',

                yaxis=dict(
                    title='Rejection Percentage',
                    titlefont_size=16,
                    tickfont_size=14,
                ),
                xaxis=dict(
                    title='Potato Variety',
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
                # gap between bars of adjacent location coordinates.
                bargap=0.15,
                # gap between bars of the same location coordinate.
                bargroupgap=0.1
            )

            return fig
        except:
            fig = go.Figure()
            return fig
