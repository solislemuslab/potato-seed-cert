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


df = pd.read_excel("2003-2016 Seed Potato Cert data v20191204_NO FL lines_Rioux 5AUG2020.xlsx", sheet_name="2003-2016 Seed Potato Cert")
virus_list = ["LR","ST","MIX","MOS"]
year_list = list(np.sort(df["S_YR"].unique()))
year_list.append("all")
group_colors = {"control": "light blue", "reference": "red"}

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div(
    children=[
        # Error Message
        html.Div(id="error-message"),
        # Top Banner
        html.Div(
            className="study-browser-banner row",
            children=[
                html.H2(className="h2-title", children="ANIMAL STUDY BROWSER"),
                html.H2(className="h2-title-mobile", children="ANIMAL STUDY BROWSER"),
            ],
        ),
        # Body of the App
        html.Div(
            className="row app-body",
            children=[
                # User Controls
                html.Div(
                    className="four columns card",
                    children=[
                        html.Div(
                            className="bg-white user-control",
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("Test Articles"),
                                        dcc.Dropdown(
                                            id="state_number",
                                            options=[
                                                {"label": col, "value": col} for col in range(1, 20)
                                            ],
                                            value=10,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("Choose the type of plot"),
                                        dcc.Dropdown(
                                            id="variety_number",
                                            options=[
                                                {"label": col, "value": col} for col in range(1, 20)
                                            ],
                                            value=10,
                                        ),
                                    ],
                                ),
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
                                        html.H6("CSV File"),
                                        dcc.Dropdown(
                                            id="virus",
                                            options=[
                                                {"label": col, "value": col} for col in virus_list
                                            ],
                                            value="LR",
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                # Graph
                html.Div(
                    className="eight columns card-left",
                    children=[
                        html.Div(
                            className="bg-white",
                            children=[
                                html.H5("Animal data plot"),
                                dcc.Graph(id="variety-graph"),
                            ],
                        )
                    ],
                ),
                dcc.Store(id="error", storage_type="memory"),
            ],
        ),
    ]
)

@app.callback(
    Output("variety-graph", "figure"),
    [
        Input("variety_number", "value"),
        Input("virus", "value"),
        Input("year", "value"),
    ],
)
def plot_virus_by_variety(variety_number, virus, year="all"):
    virus_columns = find_virus_columns(virus)
    if year == "all":
        temp = df
    else:
        temp = df[df["S_YR"] == year]

    frequent_variety = temp["VARIETY"].value_counts()[:variety_number].index.tolist()
    temp = temp[temp["VARIETY"].isin(frequent_variety)].groupby("VARIETY").mean()[virus_columns]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 0],
                         text=np.round(temp.iloc[:, 0], 3),
                         textposition='outside',
                         name=temp.columns[0],
                         marker_color='rgb(55, 83, 109)',
                         orientation='h'
                         ))
    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 1],
                         text=np.round(temp.iloc[:, 1], 3),
                         textposition='outside',
                         name=temp.columns[1],
                         marker_color='rgb(26, 118, 255)',
                         orientation='h'
                         ))

    fig.add_trace(go.Bar(y=temp.index,
                         x=temp.iloc[:, 2],
                         text=np.round(temp.iloc[:, 2], 3),
                         textposition='outside',
                         name=temp.columns[2],
                         marker_color='crimson',
                         orientation='h'
                         ))

    fig.update_layout(
        title='US Export of Plastic Scrap',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='USD (millions)',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            y=0,
            x=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )
    return fig

def find_virus_columns(virus):
    return [x for x in df.columns.tolist() if
            re.compile(r'[SR1|SR2|winter]_P*{virus}V*$'.format(virus=virus)).search(x)]


if __name__ == "__main__":
    app.run_server(debug=False)