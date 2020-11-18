import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from urllib.request import urlopen
import json
import numpy as np
from dash.dependencies import Input, Output,  State
import pandas as pd
import xlrd
import base64
import io
import flask
import os
import dash_table
from app import app

dataframe = ""
summer_columns = ["CERT_N",
                      "SNAME",
                      "GCODE",
                      "VARIETY",
                      "S_GRW",
                      "S_G",
                      "S_YR",
                      "S_GCODE",
                      "S_STATE"]

winter_columns = ["winter_{}".format(x) for x in summer_columns]


homepage = html.Div([
    # dcc.Upload(
    #     id='upload-data',
    #     children = html.Button('Upload File')),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '30%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    # dbc.Col(
    #         dcc.Dropdown(
    #             id="target_column",
    #             options=[
    #                 {"label": col, "value": col} for col in summer_columns
    #             ],
    #             value= "SNAME"
    #         ),
    #         md = 4
    #     ),
    html.Div(id='output-data-upload'),
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    global df
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        dataframe = df.copy()
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    summer_columns = ["CERT_N",
                      "SNAME",
                      "GCODE",
                      "VARIETY",
                      "S_GRW",
                      "S_G",
                      "S_YR",
                      "S_GCODE",
                      "S_STATE"]

    winter_columns = ["winter_{}".format(x) for x in summer_columns]

    errors = []
    rows = []
    for i, column in enumerate(summer_columns):
        error = len(df[df[summer_columns[i]] != df[winter_columns[i]]])
        errors.append(error)

        msg = " at row "
        indices = df[df[summer_columns[i]] != df[winter_columns[i]]].index.tolist()
        for index in indices:
            msg = msg + str(index) + " "
        rows.append(msg)

    warning_msg = ""
    for i in range(len(summer_columns)):
        msg = "{summer} doesn't match {winter}".format(summer=summer_columns[i], winter=winter_columns[i])
        msg += " at row "
        indices = df[df[summer_columns[i]] != df[winter_columns[i]]].index.tolist()
        for index in indices:
            msg = msg + str(index) + " "

        msg += "\n"

        warning_msg += msg
    all_card_content = []
    for i in range(len(summer_columns)):
        card_content =[
        dbc.CardHeader(summer_columns[i]),
        dbc.ListGroup(
            [
                dbc.ListGroupItem("Number of errors: " + str(errors[i])),
                dbc.ListGroupItem("Index of errors: " + rows[i] ),
            ],
            flush=True,
        )]
        # card_content = [
        #     dbc.CardHeader(summer_columns[i]),
        #     dbc.CardBody(
        #         [
        #             html.H5("Card title", className="card-title"),
        #             html.P(
        #                 str(errors[i]),
        #                 className="card-text",
        #             ),
        #         ]
        #     ),
        # ]
        all_card_content.append(card_content)

    cards = html.Div(
        [dbc.Row(
                [
                    dbc.Col(dbc.Card(all_card_content[0], color="primary"), width={"size": 3, "order": 1, "offset": 1}),
                    dbc.Col(dbc.Card(all_card_content[1], color="secondary"), width={"size": 3, "order": 12, "offset": 1}),
                    dbc.Col(dbc.Card(all_card_content[2], color="info"), width={"size": 3, "order": "last", "offset": 1}),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(all_card_content[3], color="success"), width={"size": 3, "order": 1, "offset": 1}),
                    dbc.Col(dbc.Card(all_card_content[4], color="warning"), width={"size": 3, "order": 12, "offset": 1}),
                    dbc.Col(dbc.Card(all_card_content[5], color="danger"), width={"size": 3, "order": 123, "offset": 1}),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(all_card_content[6], color="light"), width={"size": 3, "order": 1, "offset": 1}),
                    dbc.Col(dbc.Card(all_card_content[7], color="dark"), width={"size": 3, "order": 12, "offset": 1}),
                    dbc.Col(dbc.Card(all_card_content[8], color="dark"), width={"size": 3, "order": 123, "offset": 1})
                ]
            ),
        ]
    )

    # index = summer_columns.index(target_column)
    # indices = df[df[summer_columns[index]] != df[winter_columns[index]]].index.tolist()


    return html.Div([
        dcc.Store(id='memory-output'),
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children= filename,
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mt-4 mb-5")
        ]),
        # html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records')[:5],
            columns=[{'name': i, 'id': i} for i in df.columns],
            style_header={'backgroundColor': '#25597f', 'color': 'white'},
            style_cell={
                'backgroundColor': 'white',
                'color': 'black',
                'fontSize': 13,
                'font-family': 'Nunito Sans'}
        ),

        html.Hr(),  # horizontal line
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Warning',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        cards,
        html.Hr(),

        dbc.Col(
            dcc.Dropdown(
                id="target_column",
                options=[
                    {"label": col, "value": col} for col in summer_columns
                ],
                value="SNAME"
            ),
            md=4
        ),

        dash_table.DataTable(
            id='problematic_table',

            # columns=[{"name": i, "id": i} for i in df.columns],
            style_data_conditional=[{
            'if': {'column_editable': False},
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        }],
                                   style_header_conditional = [{
            'if': {'column_editable': False},
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        }],
        ),

        html.A(id='download-link', children='Download File'),
        # dash_table.DataTable(
        #     id = "problematic rows",
        #     data = df.to_dict("records")[indices],
        #     columns=[{'name': i, 'id': i} for i in df.columns],
        #     style_header={'backgroundColor': '#25597f', 'color': 'white'},
        #     style_cell={
        #         'backgroundColor': 'white',
        #         'color': 'black',
        #         'fontSize': 13,
        #         'font-family': 'Nunito Sans'}
        # ),
        # For debugging, display the raw contents provided by the web browser
        # html.Div('Warning'),
        # dcc.Markdown(
        #     style={"background-color": "red", "border": "solid 1px black"},
        #     children = warning_msg)
        # html.Pre(contents + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])

# @app.callback(Output('problematic rows', 'data'),
#               [Input('target_column', 'value'),
#               Input('upload-data', 'contents')],
#               [State('upload-data', 'filename'),
#                State('upload-data', 'last_modified')]
#               )
# def problematic_table(target_column, list_of_contents, list_of_names, list_of_dates):
#
#
#
#     index = summer_columns.index(target_column)
#     print(index)
#     indices = df[df[summer_columns[index]] != df[winter_columns[index]]].index.tolist()
#     print(indices)
#     return df.to_dict("records")[indices]
#


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [
                State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@app.callback(Output('download-link', 'href'),
              [Input('target_column', 'value')])
def update_href(dropdown_value):
    target_indices = summer_columns.index(dropdown_value)
    result_df = df[df[summer_columns[target_indices]] != df[winter_columns[target_indices]]  ]
    relative_filename = '{}-download.xlsx'.format(dropdown_value)

    absolute_filename = os.path.join(os.getcwd(), relative_filename)
    writer = pd.ExcelWriter(absolute_filename)
    result_df.to_excel(writer, 'Sheet1')
    writer.save()
    return '/{}'.format(relative_filename)

@app.callback(Output('problematic_table', 'data'),
              [Input('target_column', 'value')])
def update_href(dropdown_value):
    print(dropdown_value)
    target_indices = summer_columns.index(dropdown_value)
    result_df = df[df[summer_columns[target_indices]] != df[winter_columns[target_indices]]  ]
    return result_df.to_dict('records')[:5]

@app.callback(Output('problematic_table', 'columns'),
              [Input('target_column', 'value')])
def highlight_columns(dropdown_value):
    target_indices = summer_columns.index(dropdown_value)
    result_df = df[df[summer_columns[target_indices]] != df[winter_columns[target_indices]]]
    target_indices = summer_columns.index(dropdown_value)
    winter_dropdown = winter_columns[target_indices]
    return [{'id': c, 'name': c, 'editable': (c != dropdown_value and c != winter_dropdown)} for c in result_df.columns]


@app.server.route('/downloads/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return flask.send_from_directory(
        os.path.join(root_dir, 'downloads'), path
    )
