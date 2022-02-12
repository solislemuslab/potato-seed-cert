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
import jellyfish
import csv
#from app import app

PAGE_SIZE = 5
summer_columns = ["CERT_N",
                  "SNAME",
                  "GCODE",
                  "VARIETY",
                  "S_GRW",
                  "S_G",
                  "S_YR",
                  "S_GCODE",
                  "S_STATE"]
expected_csv_cols = ['Unnamed: 0', 'SummerID', 'CY', 'CERT_N', 'LNAME', 'SNAME', 'GCODE', 'VARIETY', 'VAR', 'V2', 'V3AR', 'S_GRW', 'S_G', 'S_YR', 'S_GCODE', 'S_STATE', 'ACRES', 'I_CLASS', 'I_GEN', 'START_PLTG', 'DONE_PLTG', 'DATE_1ST', 'INSPECTOR', 'INS_TITL', 'DAPS1', 'PLTCT_1', 'NO_LR_1ST', 'SR1_LR', 'NO_MOS_1ST', 'SR1_MOS', 'NO_ST_1ST', 'SR1_ST', 'SR1_TOTV', 'NO_MIX_1ST', 'AC_MIX_1ST', 'SR1_MIX', 'DATE_2ND', 'DAPS2', 'PLTCT_2', 'SR2_LR', 'SR2_MOS', 'SR2_ST', 'SR2_TOTV', 'NO_BRR_2ND', 'SR2_BRR', 'NO_MIX_2ND', 'AC_MIX_2ND', 'SR2_MIX', 'PPA_MIX', 'SRF_LR', 'SRF_MOS', 'SRF_ST', 'SRF_MIX', 'TOTVIR', 'BLEG_PCT_C', 'BLEG_PCT_N', 'RHIZOC', 'VERT_C', 'VERT_N', 'ASTRYELOS', 'EBLIGHT', 'EBLIGHT_N', 'LBLIGHT', 'SCLEROTIN', 'WILT_PCT_C', 'WILT_PCT_N', 'G_AND_VIG', 'INS_CONT', 'WEED_CONT', 'ISOLATION', 'STAND', 'COMMMENTS', 'AC_PASSD', 'AC_REJ', 'S_CLASS', 'S_GEN', 'DN_CLASS', 'PRN_F', 'BR_F', 'PSTV_F', 'LB_F', 'LAST_MOD', 'LAST_TIM', 'STOP', 'SF_HCNOT1', 'SF_HCNOT2', 'SF_HCNOT3', 'SF_HCNOT4',
                     'SF_HCNOT5', 'SF_HCNOT6', 'SF_HCNOT7', 'ADDRESSS', 'CITY', 'STATE', 'ZIP', 'SF_HCNOT8', 'SF_HCNOT9', 'SF_HCNOT10', 'SF_HCNOT11', 'WinterID', 'winter_CERT_N', 'winter_SNAME', 'winter_VAR', 'winter_TYPE', 'winter_ACRES', 'winter_AD_SAMPS', 'winter_AC_PASSD', 'winter_WT_SAMP', 'winter_WT_A', 'winter_LNAME', 'winter_GCODE', 'winter_VARIETY', 'winter_S_GRW', 'winter_S_G', 'winter_S_YR', 'winter_S_GCODE', 'winter_S_STATE', 'winter_I_CLASS', 'winter_I_GEN', 'winter_S_CLASS', 'winter_S_GEN', 'winter_DN_CLASS', 'winter_NS', 'winter_WT_LOC', 'winter_PLANTCT', 'winter_LRN', 'winter_MOSN', 'winter_MXDN', 'winter_LR', 'winter_MOS', 'winter_MIX', 'winter_PSTV', 'winter_BRR', 'winter_ELI_PLTS', 'winter_ELI_PPW', 'winter_ELI_POS', 'winter_ELI_PVY', 'winter_LVS', 'winter_TBR', 'winter_TOTV', 'winter_CLASS', 'winter_GEN', 'winter_PAYING', 'winter_SF_PROG', 'winter_FY', 'winter_DIP', 'winter_AC_REJ', 'winter_CY', 'DAPS1_binned', 'DAPS2_binned', 'NO_LR_2ND', 'NO_MOS_2ND', 'NO_ST_2ND', 'NO_TOTV_2ND']

winter_columns = ["winter_{}".format(x) for x in summer_columns]
error_columns = ["error_{}".format(x) for x in summer_columns]
rejection_column = ["AC_REJ", "winter_AC_REJ"]
combined_columns = []
for i in range(len(summer_columns)):
    combined_columns.append(summer_columns[i])
    combined_columns.append(winter_columns[i])


card_content = [
    # dbc.CardHeader("Table"),
    dbc.CardBody(
        [
            html.P("User data (.csv/xlsx/txt format)",
                   className='font-weight-bolder', style={"padding-top": '2px', "font-size": '25px'}),
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
                    # 'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.P(
                "Please choose a csv/xlsx/txt file from your device. The four tabs below will show a summary of the database and potential errors to address prior to data analysis and visualization. Note that clicking on a given tab might take a couple of seconds to load.",
                className="font-weight-lighter", style={"padding-top": '20px', "font-size": '20px', 'font-style': 'italic'}
            ),

            html.Div([
                dcc.Tabs(
                    id="tabs-with-classes",
                    value='tab-1',
                    parent_className='custom-tabs',
                    className='custom-tabs-container',
                    children=[
                        dcc.Tab(
                            label='Data Table',
                            value='tab-1',
                            className='custom-tab',
                            selected_className='custom-tab--selected'
                        ),
                        dcc.Tab(
                            label='Errors Summary',
                            value='tab-2',
                            className='custom-tab',
                            selected_className='custom-tab--selected'
                        ),
                        dcc.Tab(
                            label='Errors Structure',
                            value='tab-3', className='custom-tab',
                            selected_className='custom-tab--selected'
                        ),
                        dcc.Tab(
                            label='Errors Analysis',
                            value='tab-4',
                            className='custom-tab',
                            selected_className='custom-tab--selected'
                        ),
                    ]),
                html.Div(id='tabs-content-classes'),
                html.Br(),
                html.Br(), ])
        ]
    ),
]

homepage = html.Div([
    # dcc.Store(id='store-uploaded-data'),
    dbc.Row(
        [
            dbc.Col(dbc.Card(card_content, color="light", outline=True)),
        ]
    ),
])

# Parse the uploaded data file


def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
    except Exception as e:
        # print(e)
        return html.Div([
            'There was an error processing this file.'

        ])
    return df


def callback_upload(app):
    @app.callback([Output('tabs-content-classes', 'children'), Output('store-uploaded-data', 'data')],
                  [Input('tabs-with-classes', 'value'),
                   Input('upload-data', 'contents'),
                   Input('upload-data', 'filename')])
    def render_content(tab, contents, filename):
        if contents:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)

            if tab == 'tab-1':
                lst = []
                for col in df.columns:
                    lst.append(col)
                if((lst == expected_csv_cols) is False):
                    return html.Div([
                        html.P(
                            ["There was an error processing this file, please check the ",
                             html.A(children="data-format.md",
                                    href="https://github.com/solislemuslab/potato-seed-cert/blob/master/Data-Format.md"),
                                " and verify the colum names in your file."
                             ], className="font-weight-bolder", style={"padding-top": '20px', "font-size": '20px', 'font-style': 'italic', "color": 'red'}
                        )
                    ]), df.to_dict('records')

                return html.Div([
                    html.Br(),
                    dash_table.DataTable(
                        id="data-preview",
                        data=df.to_dict('records'),
                        columns=[{'name': i, 'id': i} for i in df.columns],
                        filter_action='native',
                        page_action='native',
                        page_size=15,
                        virtualization=True,
                        sort_action='custom',
                        sort_mode='single',
                        sort_by=[],
                        style_cell={  # ensure adequate header width when text is shorter than cell's text
                            'minWidth': 95, 'maxWidth': 95, 'width': 95
                        },
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto'
                        }
                    ),

                    html.Br(),
                    html.Br(),
                    # html.P(
                    #    "Please click the button below if you want to fill all missing data",
                    #    className='font-weight-bolder', style={"padding-top": '20px', "font-size": '20px', "color": 'blue', 'font-weight': 'bold', 'font-style': 'italic'}
                    # ),
                    # dbc.Button(children="fix me",  color="primary",
                    #           outline=True, id="fix-button", className="mr-1", block=True),''',
                    html.Br()
                ]), df.to_dict('records')
            elif tab == 'tab-2':
                lst = []
                for col in df.columns:
                    lst.append(col)
                if((lst == expected_csv_cols) is False):
                    return html.Div([
                        html.P(
                            ["There was an error processing this file, please check the ",
                             html.A(children="data-format.md",
                                    href="https://github.com/solislemuslab/potato-seed-cert/blob/master/Data-Format.md"),
                                " and verify the colum names in your file."
                             ], className="font-weight-bolder", style={"padding-top": '20px', "font-size": '20px', 'font-style': 'italic', "color": 'red'}
                        )
                    ]), df.to_dict('records')
                return html.Div([
                    html.P(
                        "Error Summary",
                        className='font-weight-bolder', style={"padding-top": '20px', "font-size": '30px', 'text-align': 'center', 'font-weight': 'bold'}
                    ),
                    html.Br(),
                    dash_table.DataTable(
                        id="error-summary",
                        page_action='native',
                        sort_action='custom',
                        sort_mode='single',
                        sort_by=[],
                        style_cell={  # ensure adequate header width when text is shorter than cell's text
                            'minWidth': 95, 'maxWidth': 95, 'width': 95
                        }
                    ),
                    html.P(
                        "Column Name corresponds to the variable name with identified errors (mismatches between winter and summer entries or missing value). Number of errors counts the number of mismatches between winter/summer and number of missing values. Number of missing values only counts the number of missing entries in this column. Index of errors shows the row indeces where the errors are found for this column. The button below will fill the missing data with the information from another inspection (winter/summer). Note that these checks only refer to columns that should be the same in both winter and summer (e.g. SNAME).",
                        className="font-weight-lighter", style={"padding-top": '20px', "font-size": '20px', 'font-style': 'italic'}
                    ),
                    html.P(
                        "Please click the button below if you want to fill all missing entries",
                        className='font-weight-bolder', style={"padding-top": '20px', "font-size": '20px', "color": 'blue', 'font-weight': 'bold', 'font-style': 'italic'}
                    ),
                    dbc.Button(children="fix me",  color="primary",
                               outline=True, id="fix-button", className="mr-1", block=True),

                ]), df.to_dict('records')
            elif tab == 'tab-3':
                lst = []
                for col in df.columns:
                    lst.append(col)
                if((lst == expected_csv_cols) is False):
                    return html.Div([
                        html.P(
                            ["There was an error processing this file, please check the ",
                             html.A(children="data-format.md",
                                    href="https://github.com/solislemuslab/potato-seed-cert/blob/master/Data-Format.md"),
                                " and verify the colum names in your file."
                             ], className="font-weight-bolder", style={"padding-top": '20px', "font-size": '20px', 'font-style': 'italic', "color": 'red'}
                        ),
                    ]), df.to_dict('records')
                return html.Div([
                    dbc.Row(
                        dbc.Col(
                            dcc.Graph(id="error-structure-graph"),
                            width={"size": 10, "offset": 1},
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            dcc.Graph(id="missing-structure-graph"),
                            width={"size": 10, "offset": 1},
                        )
                    ),
                    html.Br(),
                    html.P(
                        "Figure on top represents the location of errors in the database: x-axis represents the row index, y-axis represents the column name and the black rectangles corresponds to errors. Figure on bottom represents the same figure, but with missingness.",
                        className="font-weight-lighter", style={"padding-top": '20px', "font-size": '20px', 'font-style': 'italic'}
                    ),
                    html.P(
                        "Please click the button below if you want to fill all missing entries",
                        className='font-weight-bolder', style={"padding-top": '20px', "font-size": '20px', "color": 'blue', 'font-weight': 'bold', 'font-style': 'italic'}
                    ),
                    dbc.Button(children="fix me",  color="primary",
                               outline=True, id="fix-button", className="mr-1", block=True),

                ]), df.to_dict('records')
            elif tab == 'tab-4':
                lst = []
                for col in df.columns:
                    lst.append(col)
                if((lst == expected_csv_cols) is False):
                    return html.Div([
                        html.P(
                            ["There was an error processing this file, please check the ",
                             html.A(children="data-format.md",
                                    href="https://github.com/solislemuslab/potato-seed-cert/blob/master/Data-Format.md"),
                                " and verify the colum names in your file."
                             ], className="font-weight-bolder", style={"padding-top": '20px', "font-size": '20px', 'font-style': 'italic', "color": 'red'}
                        ),
                    ]), df.to_dict('records')
                return html.Div([
                    html.P(
                        "Similarity between Two Similar Column Names(in %)",
                        className='font-weight-bolder', style={"padding-top": '20px', "font-size": '30px', 'text-align': 'center', 'font-weight': 'bold'}
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label(
                                                    "Columns(in Summer and Winter)"),
                                                dcc.Dropdown(
                                                    id="similar_columns",
                                                    options=[
                                                        {"label": col, "value": col} for col in ["VARIETY", "S_G"]
                                                    ],
                                                    value="VARIETY",
                                                    placeholder="Select a Column",),

                                            ]), ),
                                     dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Text"),
                                                dbc.Input(
                                                    id="suscipious-input", placeholder="Type something...", type="text"),
                                            ]), ),
                                     dbc.Col(
                                        dbc.FormGroup(
                                            [
                                                dbc.Label("Frequency"),
                                                dbc.Input(
                                                    id="suscipious-frequency", type="number"),
                                            ]), ),
                                     ]
                                ),
                                html.Br(),
                                dbc.Row(
                                    dbc.Col(

                                        dash_table.DataTable(
                                            id='similar_string_table',
                                            editable=True,
                                            virtualization=True,
                                            page_action='native',
                                            page_size=15,
                                            style_cell={  # ensure adequate header width when text is shorter than cell's text
                                                'minWidth': 95, 'maxWidth': 95, 'width': 95
                                            },
                                            # style_data_conditional=[{
                                            #     'if': {'column_editable': False},
                                            #     'backgroundColor': 'rgb(30, 30, 30)',
                                            #     'color': 'white'
                                            # }],
                                            style_header_conditional=[{
                                                'if': {'column_editable': False},
                                                'backgroundColor': 'rgb(30, 30, 30)',
                                                'color': 'white'
                                            }],
                                        ),
                                    )
                                ),
                                html.P(
                                    "Table above shows the potential errors found for a given column name (e.g. VARIETY). Each row represents a potential error. The first two columns correspond to the summer and winter variable, and the third column corresponds to the jaro distance which measures how similar the entries are. If you want to replace one entry with the correct one, please type the erroneous entry in the first box below and the correct one in the second box. At the bottom, you will find the `Details of errors` which is a subset of the database with errors. You can download this subset database to inspect with the Export button.",
                                    className="font-weight-lighter", style={"padding-top": '20px', "font-size": '20px'}
                                ),
                                html.Br(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.FormGroup(
                                                [
                                                    dbc.Label(
                                                        "Erroneous entry"),
                                                    dbc.Input(
                                                        id="error_input", placeholder="Type the value that should be replaced", type="text"),
                                                ]), ),
                                        dbc.Col(
                                            dbc.FormGroup(
                                                [
                                                    dbc.Label("Correct entry"),
                                                    dbc.Input(
                                                        id="correct_input", placeholder="Type the correct one", type="text"),
                                                ]), ),
                                        dbc.Button(children="comfirm",  color="primary",
                                                   outline=True, id="fixerror-button", className="mr-1", block=True),
                                    ]
                                ),
                                html.Br(), ]
                        ),
                    ),
                    html.Br(),
                    html.Br(),

                    html.Hr(),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.P(
                                            "Details of the Errors",
                                            className='font-weight-bolder', style={"padding-top": '20px', "font-size": '30px', 'text-align': 'center', 'font-weight': 'bold'}
                                        ),
                                        html.Div(dcc.Dropdown(
                                            id="target_column",
                                            options=[
                                                {"label": col, "value": col} for col in summer_columns
                                            ] + [
                                                {"label": col, "value": col} for col in rejection_column
                                            ],
                                            value="SNAME"
                                        ), style={"width": "30%"}, ),
                                        html.Br(),
                                        dash_table.DataTable(
                                            id='problematic_table',
                                            virtualization=True,
                                            export_format="csv",
                                            page_action='native',
                                            page_size=15,
                                            sort_action='custom',
                                            sort_mode='single',
                                            sort_by=[],
                                            style_cell={  # ensure adequate header width when text is shorter than cell's text
                                                'minWidth': 95, 'maxWidth': 95, 'width': 95
                                            },
                                            style_data_conditional=[{
                                                'if': {'column_editable': False},
                                                'backgroundColor': 'rgb(30, 30, 30)',
                                                'color': 'white'
                                            }],
                                            style_header_conditional=[{
                                                'if': {'column_editable': False},
                                                'backgroundColor': 'rgb(30, 30, 30)',
                                                'color': 'white'
                                            }],
                                        ),
                                        html.Br(),
                                        # dbc.Button([
                                        #     html.A(id='download-link',
                                        #            children='Download File'),
                                        # ],
                                        #     outline=True, color="warning", className="mr-1")
                                    ]
                                ),
                            ),
                            width=12,
                        ),
                    ]),
                    html.Br(),
                    html.P(
                        "Please click the button below if you want to fill all missing data",
                        className='font-weight-bolder', style={"padding-top": '20px', "font-size": '20px', "color": 'blue', 'font-weight': 'bold', 'font-style': 'italic'}
                    ),
                    dbc.Button(children="fix me",  color="primary",
                               outline=True, id="fix-button", className="mr-1", block=True),


                ]), df.to_dict('records')

        else:
            return None, None

    def to_string(filter):
        operator_type = filter.get('type')
        operator_subtype = filter.get('subType')

        if operator_type == 'relational-operator':
            if operator_subtype == '=':
                return '=='
            else:
                return operator_subtype
        elif operator_type == 'logical-operator':
            if operator_subtype == '&&':
                return '&'
            else:
                return '|'
        elif operator_type == 'expression' and operator_subtype == 'value' and type(filter.get('value')) == str:
            return '"{}"'.format(filter.get('value'))
        else:
            return filter.get('value')

    def construct_filter(derived_query_structure, df, complexOperator=None):

        # there is no query; return an empty filter string and the
        # original dataframe
        if derived_query_structure is None:
            return ('', df)

        # the operator typed in by the user; can be both word-based or
        # symbol-based
        operator_type = derived_query_structure.get('type')

        # the symbol-based representation of the operator
        operator_subtype = derived_query_structure.get('subType')

        # the LHS and RHS of the query, which are both queries themselves
        left = derived_query_structure.get('left', None)
        right = derived_query_structure.get('right', None)

        # the base case
        if left is None and right is None:
            return (to_string(derived_query_structure), df)

        # recursively apply the filter on the LHS of the query to the
        # dataframe to generate a new dataframe
        (left_query, left_df) = construct_filter(left, df)

        # apply the filter on the RHS of the query to this new dataframe
        (right_query, right_df) = construct_filter(right, left_df)

        # 'datestartswith' and 'contains' can't be used within a pandas
        # filter string, so we have to do this filtering ourselves
        if complexOperator is not None:
            right_query = right.get('value')
            # perform the filtering to generate a new dataframe
            if complexOperator == 'datestartswith':
                return ('', right_df[right_df[left_query].astype(str).str.startswith(right_query)])
            elif complexOperator == 'contains':
                return ('', right_df[right_df[left_query].astype(str).str.contains(right_query)])

        if operator_type == 'relational-operator' and operator_subtype in ['contains', 'datestartswith']:
            return construct_filter(derived_query_structure, df, complexOperator=operator_subtype)

        # construct the query string; return it and the filtered dataframe
        return ('{} {} {}'.format(
            left_query,
            to_string(
                derived_query_structure) if left_query != '' and right_query != '' else '',
            right_query
        ).strip(), right_df)

    # Number of errors in each subgroup

    @app.callback([Output('error-summary', 'data'),
                   Output('error-summary', 'columns')],
                  [
        Input('error-summary', 'sort_by'),
        Input("store-uploaded-data", "data"),
        Input("fix-button", "n_clicks")
    ])
    def error_table(sort_by, data,  n_clicks):
        # if contents:
        try:
            df = pd.DataFrame(data)
            if len(sort_by):
                df = df.sort_values(
                    sort_by[0]['column_id'],
                    ascending=sort_by[0]['direction'] == 'asc',
                    inplace=False
                )
            else:
                # No sort is applied
                df = df

            if n_clicks is None or n_clicks % 2 == 0:
                pass
            elif n_clicks % 2 == 1:
                for i in range(0, len(combined_columns), 2):
                    df[combined_columns[i]] = df[combined_columns[i]].fillna(
                        df[combined_columns[i + 1]])
                    df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                        df[combined_columns[i + 1]])

                for i in range(1, len(combined_columns), 2):
                    df[combined_columns[i]] = df[combined_columns[i]].fillna(
                        df[combined_columns[i - 1]])
                    df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                        df[combined_columns[i - 1]])

            errors = []
            missing_values = []
            rows = []
            for i, column in enumerate(summer_columns):
                missing = len(df[(df[summer_columns[i]].isnull())
                                 | (df[winter_columns[i]].isnull())])
                missing_values.append(missing)

                error = len(df[df[summer_columns[i]] != df[winter_columns[i]]])
                errors.append(error)

                msg = " at row "
                indices = df[df[summer_columns[i]] !=
                             df[winter_columns[i]]].index.tolist()
                for index in indices:
                    msg = msg + str(index) + " "
                rows.append(msg)

            error_df = pd.DataFrame(
                {'Column Name': summer_columns,
                 'Number of errors': errors,
                 'Number of missing values': missing_values,
                 'Index of erros': rows,
                 })

            data = error_df.to_dict('rows')
            columns = [{'name': i, 'id': i} for i in error_df.columns]

            return data, columns
        except:
            pass

    # Table paging and sorting

    @app.callback(
        Output('data-preview', 'data'),
        [
            Input('data-preview', 'sort_by'),
            Input('upload-data', 'contents'),
            Input('upload-data', 'filename'),
            Input("data-preview", "derived_filter_query_structure")
        ]
    )
    def page_and_sort(sort_by, contents, filename, derived_query_structure):
        if contents:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)

        if len(sort_by):
            dff = df.sort_values(
                sort_by[0]['column_id'],
                ascending=sort_by[0]['direction'] == 'asc',
                inplace=False
            )
        else:
            # No sort is applied
            dff = df

        (pd_query_string, df_filtered) = construct_filter(
            derived_query_structure, dff)

        if pd_query_string != '':
            df_filtered = df_filtered.query(pd_query_string)

        return df_filtered.to_dict('records')

    # Heatmap to examine the distribution of errors

    @app.callback(
        Output('error-structure-graph', "figure"),
        [
            Input("store-uploaded-data", "data"),
            Input("fix-button", "n_clicks")
        ]
    )
    def error_structure(data, n_clicks):
        try:
            if data:
                df = pd.DataFrame(data)

            if n_clicks is None or n_clicks % 2 == 0:
                pass
            elif n_clicks % 2 == 1:
                for i in range(0, len(combined_columns), 2):
                    df[combined_columns[i]] = df[combined_columns[i]].fillna(
                        df[combined_columns[i + 1]])
                    df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                        df[combined_columns[i + 1]])

                for i in range(1, len(combined_columns), 2):
                    df[combined_columns[i]] = df[combined_columns[i]].fillna(
                        df[combined_columns[i - 1]])
                    df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                        df[combined_columns[i - 1]])

            for i in range(len(summer_columns)):
                df[error_columns[i]] = df[summer_columns[i]
                                          ] != df[winter_columns[i]]

            fig = px.imshow(df[error_columns].T, color_continuous_scale=px.colors.sequential.Greys,
                            title="Errors Structure")
            fig.update_layout(title_font={'size': 27}, xaxis=dict(
                title="row index", titlefont_size=16,
                tickfont_size=14,), title_x=0.5)

            return fig
        except:
            pass

    # Heatmap to examine the distribution of missing values

    @app.callback(
        Output('missing-structure-graph', "figure"),
        [
            Input("store-uploaded-data", "data"),
            Input("fix-button", "n_clicks")
        ]
    )
    def missing_structure(data, n_clicks):
        try:
            if data:
                df = pd.DataFrame(data)

            if n_clicks is None or n_clicks % 2 == 0:
                pass
            elif n_clicks % 2 == 1:
                for i in range(0, len(combined_columns), 2):
                    df[combined_columns[i]] = df[combined_columns[i]].fillna(
                        df[combined_columns[i + 1]])
                    df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                        df[combined_columns[i + 1]])

                for i in range(1, len(combined_columns), 2):
                    df[combined_columns[i]] = df[combined_columns[i]].fillna(
                        df[combined_columns[i - 1]])
                    df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                        df[combined_columns[i - 1]])

            for i in range(len(summer_columns)):
                df[error_columns[i]] = df[[summer_columns[i], winter_columns[i]]
                                          ].isnull().apply(lambda x: any(x), axis=1)

            fig = px.imshow(df[error_columns].T, color_continuous_scale=px.colors.sequential.Greys,
                            title="Missing Structure")
            fig.update_layout(title_font={'size': 27}, xaxis=dict(
                title="row index", titlefont_size=16,
                tickfont_size=14,), title_x=0.5)

            return fig
        except:
            pass

    @app.callback([Output('fix-button', 'children'), ],
                  [
        Input('fix-button', 'n_clicks'),

    ])
    def error_table(nclicks):
        if nclicks == None or nclicks % 2 == 0:
            return ["FIX ERRORS"]
        else:
            return ["Undo"]

    @app.callback([Output('fixerror-button', 'children'), ],
                  [
        Input('fixerror-button', 'n_clicks'),

    ])
    def error_table2(nclicks):
        if nclicks == None or nclicks % 2 == 0:
            return ["FIX ERRORS"]
        else:
            return ["Undo"]

    @app.callback([Output('similar_string_table', 'data'),
                   Output('similar_string_table', 'columns'), ],
                  [Input('similar_columns', 'value'),
                   Input("store-uploaded-data", "data"),
                   ])
    def error_highlight_table(dropdown_value, data):
        try:
            if data:
                df = pd.DataFrame(data)

            a = dropdown_value
            b = "winter_{a}".format(a=dropdown_value)

            # Fill missing value
            for i in range(0, len(combined_columns), 2):
                df[combined_columns[i]] = df[combined_columns[i]].fillna(
                    df[combined_columns[i + 1]])
                df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                    df[combined_columns[i + 1]])

            for i in range(1, len(combined_columns), 2):
                df[combined_columns[i]] = df[combined_columns[i]].fillna(
                    df[combined_columns[i - 1]])
                df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                    df[combined_columns[i - 1]])

            # Check all unique mismatches
            temp = df.loc[df[a] != df[b], [a, b]].drop_duplicates()
            # Calculate similarity
            temp["jaro_distance"] = temp.apply(
                lambda x: jellyfish.jaro_distance(x[a], x[b]), axis=1)
            # sort by similarity
            temp = temp.sort_values(by="jaro_distance", ascending=False)

            columns = [{'id': c, 'name': c, } for c in temp.columns]

            return temp.to_dict('records'), columns
        except:
            pass

    # Generate the table with highlighted errors

    @app.callback([Output('problematic_table', 'data'),
                   Output('problematic_table', 'columns'), ],
                  [Input('target_column', 'value'),
                   Input("store-uploaded-data", "data"),
                   Input('problematic_table', 'sort_by'),
                   Input("problematic_table", "derived_filter_query_structure"),
                   Input("fix-button", "n_clicks")
                   ])
    def error_highlight_table(dropdown_value, data, sort_by, derived_query_structure, n_clicks):
        try:
            if data:
                df = pd.DataFrame(data)
            if n_clicks is None or n_clicks % 2 == 0:
                pass
            elif n_clicks % 2 == 1:
                for i in range(0, len(combined_columns), 2):
                    df[combined_columns[i]] = df[combined_columns[i]].fillna(
                        df[combined_columns[i + 1]])
                    df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                        df[combined_columns[i + 1]])

                for i in range(1, len(combined_columns), 2):
                    df[combined_columns[i]] = df[combined_columns[i]].fillna(
                        df[combined_columns[i - 1]])
                    df[combined_columns[i]] = df[combined_columns[i]].mask(df[combined_columns[i]] == 0).fillna(
                        df[combined_columns[i - 1]])

            if dropdown_value in summer_columns:
                target_indices = summer_columns.index(dropdown_value)
                winter_dropdown = winter_columns[target_indices]
                result_df = df[df[summer_columns[target_indices]]
                               != df[winter_columns[target_indices]]]
                result_cols = ["SummerID", "CY", "CERT_N",
                               dropdown_value, winter_dropdown]

                # data = result_df.to_dict('records')

                columns = [{'id': c, 'name': c, 'editable': (
                    c != dropdown_value and c != winter_dropdown)} for c in result_cols]
            elif dropdown_value in rejection_column:
                result_df = df[df[dropdown_value] < 0]
                # data = result_df.to_dict('records')
                columns = [{'id': c, 'name': c, 'editable': (c != dropdown_value)} for c in
                           result_df.columns]

            if len(sort_by):
                dff = result_df.sort_values(
                    sort_by[0]['column_id'],
                    ascending=sort_by[0]['direction'] == 'asc',
                    inplace=False
                )
            else:
                # No sort is applied
                dff = result_df

            (pd_query_string, df_filtered) = construct_filter(
                derived_query_structure, dff)

            if pd_query_string != '':
                df_filtered = df_filtered.query(pd_query_string)

            return df_filtered[result_cols].to_dict('records'), columns
        except:
            pass

    @app.callback(Output('suscipious-frequency', 'value'),
                  [Input('similar_columns', 'value'),
                   Input("suscipious-input", "value"),
                   Input("store-uploaded-data", "data"),
                   ])
    def calculate_frequency(summer_column, input, data):
        try:
            df = pd.DataFrame(data)
            target_indices = summer_columns.index(summer_column)
            winter_column = winter_columns[target_indices]

            target = input

            if target not in df[summer_column].unique() and target not in df[winter_column].unique():
                return 0
            elif target not in df[summer_column].unique():
                return df[winter_column].value_counts()[target]
            elif target not in df[winter_column].unique():
                return df[summer_column].value_counts()[target]
            else:
                return df[summer_column].value_counts()[target] + df[summer_column].value_counts()[target]
        except:
            pass

    @app.server.route('/downloads/<path:path>')
    def serve_static(path):
        root_dir = os.getcwd()
        return flask.send_from_directory(
            os.path.join(root_dir, 'downloads'), path
        )
