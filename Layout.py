import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from urllib.request import urlopen
import json
import numpy as np
from dash.dependencies import Input, Output
import pandas as pd
import xlrd
import base64
from callback import df,  encoded_image, encoded_image_03, encoded_image_05, encoded_image_10, mobility, covid_by_census,\
    policy

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# save all the parameters of the pages for easy accessing
PAGES = [
    {'children': 'Home', 'href': '/', 'id': 'home'},
    {'children': 'Correlation', 'href': '/correlation', 'id': 'correlation-page'}
]

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

homepage_layout = html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Markdown([
                                "##### Mobility Types\n",
                                "**Grocery & pharmacy**\n",
                                "Mobility trends for places like grocery markets, food warehouses, \
                                    farmers markets, specialty food shops, drug stores, and pharmacies.\n",
                                "**Parks**\n",
                                "Mobility trends for places like local parks, national parks, public beaches,\
                                    marinas, dog parks, plazas, and public gardens.\n",
                                "**Transit stations**\n",
                                "Mobility trends for places like public transport hubs such as subway, bus, and train stations.\n",
                                "**Retail & recreation**\n",
                                "Mobility trends for places like restaurants, cafes, shopping centers, \
                                    theme parks, museums, libraries, and movie theaters.\n",
                                "**Residential**\n", "Mobility trends for places of residence.\n",
                                "**Workplaces**\n", "Mobility trends for places of work."

                            ])),
                            dbc.Col(dcc.Markdown([
                                "##### Correlation Coefficients between Daily Cases and Mobility\n",
                                "It is the number that describes how people reacted to the reported daily cases "\
                                    "in the previous days. It takes values between -1 and 1. A positive value indicates that "\
                                        "as the reported daily cases increased, people's mobility decreased in the following day.\n",
                                "##### Data resources\n",
                                "[Google COVID-19 Community Mobility Reports](https://www.google.com/covid19/mobility/index.html?hl=en)\n",
                                "[John Hopkins Daily Reports](https://github.com/CSSEGISandData/COVID-19)\n",
                                "[New York Times COVID-19 Reports](https://github.com/nytimes/covid-19-data)"
                            ])),
                        ]
                    )
                ]
)


# the layout of the correlation page
virus_layout = html.Div(children=[
        html.Hr()
        ])


sidebar_layout = html.Div(
    [
        html.Div([
                    dbc.Row([html.H4("Potato")
                            ])
                    ]),
        html.Hr(),
        html.P(
            "Catalog", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", id="home")
            ],
            vertical=False,
            pills=True,
        ),
        dbc.Nav(
            [
                dbc.NavLink("Visualization", href="/virus", id="correlation-page")
            ],
            vertical=False,
            pills=True,
        ),
        dbc.Nav(
            [
                dbc.NavLink("Week 10/05", href="/weather", id="weather-page")
            ],
            vertical=False,
            pills=True,
        )
    ],
    style=SIDEBAR_STYLE
)

# weather_layout = html.Div([
#     html.Div([
#         html.Div(
#           dcc.Graph(id='g1',
#                     figure=fig_03,
#                     className="six columns",
#                     style={"width":500, "margin": 0, 'display': 'inline-block'}
#                 ),
#         html.Div(
#           dcc.Graph(id='g2',
#                     figure={'data': [{'y': [1, 2, 3]}]}),
#                     className="six columns",
#                     style={"width":500, "margin": 0, 'display': 'inline-block'}
#                 ),
#     ], className="row")
# ])

# weather_layout = html.Div([
#         html.Div([
#             html.Div(dcc.Graph(figure=fig_03))
#         ])
#         ],
#     CONTENT_STYLE)

#

# weather_layout = html.Div(className='row',
#                           style = {"display":"flex"},
#         children = [
#                 # html.Div(html.H3("Wisconsin Mobility Trend Analysis -- during covid19"),
#                 # dcc.Markdown(
#                 #                 "The mobility trend reveals how people are driving during the special period.\n",
#                 #                 "The darker the color indicates more movements while lighter indicates less movements.\n"
#                 #               ),
#                 html.Div([
#                  html.H5("March"),
#                  html.Img(src='data:image/png;base64,{}'.format(encoded_image_03), style={'width': '250px'})
#
#                 ]),
#                 html.Div([
#                  html.H5("May"),
#                  html.Img(src='data:image/png;base64,{}'.format(encoded_image_05), style={'width': '250px'})
#
#                 ]),
#                 html.Div([
#                  html.H5("October"),
#                  html.Img(src='data:image/png;base64,{}'.format(encoded_image_10), style={'width': '250px'})
#
#                 ])
#
#         ])

weather_layout = html.Div(
    [
    html.H3("Wisconsin Mobility Trend Analysis -- during covid19"),
    dcc.Markdown([
                                "The mobility trend reveals how people are driving during the special period.\n",
                                "The darker the color indicates more movements while lighter indicates less movements.\n"
                              ]),
        dbc.Row(
            [
                dbc.Col(html.Div([
                 html.H5("March"),
                 html.Img(src='data:image/png;base64,{}'.format(encoded_image_03), style={'width': '250px'})

                ])),
                dbc.Col(html.Div([
                    html.H5("May"),
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image_05), style={'width': '250px'})

                ])),
                dbc.Col(html.Div([
                    html.H5("October"),
                    html.Img(src='data:image/png;base64,{}'.format(encoded_image_10), style={'width': '250px'})

                ]))
            ],
            align="start"),

        html.Hr(),

        html.Div([
            html.H5('Daily Confirmed Cases'),
            html.Img(src='data:image/png;base64,{}'.format(policy), style={'width': '550px'})

        ]),

        html.Div(dcc.Markdown([
            "The blue vertical lines represent the state-wise policies \n",
            "The red vertical lines represent the two protest occured in the May and late Auguest.\n",
            "It can be seen that covid cases per day increase significantly a few weeks followed by protest"
        ])
        ),

        html.Hr(),

        html.Div(
            dcc.Markdown([
                "The data shows how visitors to (or time spent in) categorized places change compared to our baseline days.\n",
                "A baseline day represents a normal value for that day of the week.\n",
                "The baseline day is the median value from the 5‑week period Jan 3 – Feb 6, 2020.\n",
                "For each region-category, the baseline isn’t a single value—it’s 7 individual values.\n"
                "Avoid comparing day-to-day changes. Especially weekends with weekdays."
            ])
        ),
        html.Div([
            html.H5('Mobility Trend'),
            html.Img(src='data:image/png;base64,{}'.format(mobility), style={'width': '550px'})

        ]),

        html.Hr(),
        ])
# html.Div(className='row',
#          style : {'display' : 'flex'},
#              children=[
#         html.Div(
#             dcc.Graph(id='value-index'),
#             className='col s12 m6',
#
#             ),
#         html.Div(
#             dcc.Graph(id='rental-index'),
#             className='col s12 m6',
#             )
#         ]
# )
#
