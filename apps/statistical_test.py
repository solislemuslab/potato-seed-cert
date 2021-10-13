import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import numpy as np
from dash.dependencies import Input, Output,  State
import pandas as pd
from scipy.stats import chi2
from scipy.stats import chi2_contingency
import statsmodels.api as sm
from statsmodels.formula.api import ols
import dash_table
#from app import app
import pathlib

LINEBREAK_STYLE = {
    'border': '3px solid white'
}

# get relative data folder
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../datasets").resolve()
# df = pd.read_csv(DATA_PATH.joinpath("cleaned_potato.csv"))

diseases = ["BLEG_PCT_C", "RHIZOC", "VERT_C",
            "ASTRYELOS", "EBLIGHT"	, "LBLIGHT", "WILT_PCT_C"]
continuous_diseases = ["SR1_MOS", "SR2_MOS", "SR1_LR"]
sources = ["SNAME",
           "GCODE",
           "VARIETY",
           "S_GRW",
           "S_G",
           "S_YR",
           "S_GCODE",
           "S_STATE"]
df_grower = ['Atwater', 'B Kuczmarski', 'Baginski', 'Bjornstad', 'Bula Potato',
             'Bushman', 'Buyan', 'CETS', 'CSS', 'Childstock', 'Crown', 'Diercks', 'Droge', 'Droge Farms', 'Eagle River Se',
             'Ebbesson', 'Enander', 'Fleischman D', 'Gallenberg D', 'Gallenberg Fms', 'Goldeneye', 'Greenleaf Org', 'Guenthner Po',
             'H Miller', 'Haenni Farms', 'Hafner', 'Hanson', 'Hartman', 'Haskett', 'J Gallenberg', 'J Jorde',
             'J Nicholes', 'John Miller', 'Johnson', 'Jonk Seed Farm', 'Jorde Certi', 'Jorde Certifie', 'Jorde Mike', 'Kakes',
             'Kent Farms', 'Kimm Pot', 'Kroeker Farms,', 'LHIlls', 'Larson Farms', 'London', 'London Hill', 'MSU', 'Maine Seed', 'Mangels', 'Manhattan',
             'Mark Kuehl', 'Mark Stremick', 'Martin', 'Mattek', 'McCain', 'Miller Farms J', 'Myrna Stremick', 'Myrna stremick',
             'NDS', 'Neu Ground Lab', 'Nilson Farms', 'PEI Produce', 'Paquin', 'Parkinson Seed', 'Phytocu', 'Rine Ridge',
             'Royce Atwater', 'Salen', 'San Luis', 'Schroeder Bros', 'Schroeder Farm', 'Schutter', 'Scidmore Farms', 'Seed Pro',
             'Seidl', 'Sklarczyk', 'Skogman', 'Sowinski', 'Sping Creek', 'State Farm', 'Steinmann', 'Summit Farms', 'Summit Labs',
             'Sunny Valley', 'Sunnydale', 'Sunrain Variet', 'T Spychalla', 'Technico/Sham',
             'Tetonia', 'Thompson', 'UI/Teutonia', 'UW Breeding', 'Uihlein Fm', 'Val TCulture', 'Van Erkel', 'Wild',
             'Wirz', 'Worley', 'Zeloski -ER', 'Zeloski, Felix']
df_state = ['AK', 'CO', 'ID', 'MB', 'ME', 'MI', 'MN', 'MT', 'NB', 'ND', 'NE',
            'NY', 'PE', 'WI']
df_year = list(range(2000, 2017))

chi_test_columns = ["Null HYpothesis",
                    "Alternative Hypothesis", "Chi-Square score", "df", "P-value"]
anova_columns = ["Null HYpothesis",
                 "Alternative Hypothesis", "F score", "df", "P-value"]

homepage = html.Div([
    dbc.Card([
        dbc.CardHeader(html.H4("Filter Data"),),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("State"),
                            dcc.Dropdown(
                                id="state_type",
                                options=[{"label": "All", "value": "All"}] + [
                                    {"label": col, "value": col} for col in df_state
                                ],
                                value="All", ),
                        ]),
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Year"),
                            dcc.Dropdown(
                                id="year",
                                options=[{"label": "All", "value": "All"}] + [
                                    {"label": col, "value": col} for col in df_year
                                ],
                                value="All", ),
                        ])
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Grower"),
                            dcc.Dropdown(
                                id="grower",
                                options=[{"label": "All", "value": "All"}] + [
                                    {"label": col, "value": col} for col in df_grower
                                ],
                                value="All"),
                        ]),
                ),
            ]
            )
        ]),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.H5("Pearson's Chi-Squared Test:"),
            width={"size": 4}
        ),

        dbc.Col(
            [
                dbc.Button("Help", color="primary",
                           id="Pchi_square-open", className="mr-auto"),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Pearson's Chi-Square Test"),
                        dbc.ModalBody(
                            "The Pearson's chi-square test tests whether there is any association between two factors to be selected by the user: Disease and Source variable (e.g. source grower S_G). The user can filter the data based on State, Year and Grower and select a significance threshold for the test (usually 0.05). The observation table will display the counts of the two factors with the first column corresponding to the levels of the Disease variable and all other columns corresponding to the levels of the source variable. At the bottom, the chi-square test result will select which hypothesis is preferred by the data (null hypothesis of independence or alternative hypothesis of association), the chi-square score, degrees of freedom (df) and p-value. If the p-value is less than the selected significance level, then the null hypothesis is rejected."),
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
    html.Br(),
    dbc.Row([
            dbc.Col(dbc.Card(
                [
                    dbc.FormGroup(
                        [
                            dbc.Label("Disease (Discrete) "),
                            dcc.Dropdown(
                                id="row-name",
                                options=[
                                    {"label": col, "value": col} for col in sorted(diseases)
                                ],
                                value="LBLIGHT", ),
                        ]),
                    dbc.FormGroup(
                        [
                            dbc.Label("Source variable"),
                            dcc.Dropdown(
                                id="col-name",
                                options=[
                                    {"label": col, "value": col} for col in sorted(sources)
                                ],
                                value="S_G", ),
                        ]),
                    dbc.FormGroup(
                        [
                            dbc.Label("Significance level"),
                            html.Br(),
                            dcc.Slider(
                                id="slider-chisquare",
                                min=0,
                                max=1,
                                step=0.01,
                                marks={
                                    0: '0',
                                    0.2: "0.2",
                                    0.4: "0.4",
                                    0.6: "0.6",
                                    0.8: "0.8",
                                    1: '1',
                                },
                                value=0.05,
                                tooltip={'always_visible': True,
                                         "placement": 'top'}
                            ),
                        ]),

                ], body=True, style={'height': '60vh'}), md=4),
            dbc.Col(
                children=[
                    dbc.Card(
                        [
                            html.H5("Observation Table"),
                            html.Br(),
                            dash_table.DataTable(
                                id="observation",
                                page_action='native',
                                page_size=15,
                                sort_action='native',
                                sort_mode='single',
                                sort_by=[],
                                style_cell={  # ensure adequate header width when text is shorter than cell's text
                                    'minWidth': 95, 'maxWidth': 95, 'width': 95, 'padding': '5px'
                                },
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto'
                                },
                                css=[{
                                    'selector': '.dash-spreadsheet td div',
                                    'rule': '''
                           line-height: 15px;
                           max-height: 30px; min-height: 30px; height: 30px;
                       display: block;
                       overflow-y: auto;
                       .dash-spreadsheet .row {
                          flex-wrap: nowrap;
                        };
                   '''
                                }],
                                style_table={'overflowX': 'auto'},
                            )],
                        body=True, style={'height': '60vh'}), ],

                md=8),

            ],
            align="center", ),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            [
                html.H5("Chi-square Test Result "),
                html.Div(id="chi-summary"),
            ],
            width={"size": 9, "offset": 1}
        ),
    ]
    ),
    html.Br(),
    html.Hr(style=LINEBREAK_STYLE),
    dbc.Row([
        dbc.Col(
            html.H5("ANOVA Test:"),
            width={"size": 4}
        ),
        dbc.Col(
            [
                dbc.Button("Help", color="primary",
                           id="anova-open", className="mr-auto"),
                dbc.Modal(
                    [
                        dbc.ModalHeader("ANOVA Test"),
                        dbc.ModalBody("The ANOVA test tests whether there are differences in the disease prevalence means for the factors in the source variable. The user selects Disease and Source variable (e.g. source grower S_G). The user can filter the data based on State, Year and Grower and select a significance threshold for the test (usually 0.05). The ANOVA test result will select which hypothesis is preferred by the data (null hypothesis of independence or alternative hypothesis of association), the F score, degrees of freedom (df) and p-value. If the p-value is less than the selected significance level, then the null hypothesis is rejected."),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="anova-close",
                                       className="ml-auto")
                        ),
                    ],
                    id="anova-message",
                )],
            width={"size": 2, "offset": 6}
        )
    ]),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.FormGroup(
                            [
                                dbc.Label("Disease (Continuous)"),
                                dcc.Dropdown(
                                    id="anova-row-name",
                                    options=[
                                        {"label": col, "value": col} for col in sorted(continuous_diseases)
                                    ],
                                    value="SR1_MOS", ),
                            ]),
                        dbc.FormGroup(
                            [
                                dbc.Label("Source variable"),
                                dcc.Dropdown(
                                    id="anova-col-name",
                                    options=[
                                        {"label": col, "value": col} for col in sorted(sources)
                                    ],
                                    value="S_G", ),
                                html.Br(),
                                dbc.FormGroup(
                                    [
                                        dbc.Label("Significance level"),
                                        html.Br(),
                                        dcc.Slider(
                                            id="slider-anova",
                                            min=0,
                                            max=1,
                                            step=0.01,
                                            marks={
                                                0: '0',
                                                0.2: "0.2",
                                                0.4: "0.4",
                                                0.6: "0.6",
                                                0.8: "0.8",
                                                1: '1',
                                            },
                                            value=0.05,
                                            tooltip={'always_visible': True,
                                                     "placement": 'top'}
                                        ),
                                    ]),
                            ]),

                    ], body=True, style={'height': '55vh'}), md=4),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            html.H5("ANOVA Test Result "),
                            html.Div(id="anova-summary"),
                        ],
                        body=True, style={'height': '55vh'},)
                ],
            ),
        ])
])

# @app.callback(
#     [Output("state_type", "options"),
#      Output("year", "options"),
#      Output("grower", "options")],
#     [
#      Input("store-uploaded-data", "data")
#      ]
# )
# def dropdown_option(data):
#     if data:
#         df = pd.DataFrame(data)
#
#     state_options = [{"label": "All", "value": "All"}] + [
#         {"label": col, "value": col} for col in sorted(df["S_STATE"].dropna().unique())
#     ]
#
#     year_options = [{"label": "All", "value": "All"}] + [
#         {"label": col, "value": col} for col in sorted(df["S_YR"].dropna().unique())
#     ]
#
#     grower_options = [{"label": "All", "value": "All"}] + [
#         {"label": col, "value": col} for col in sorted(df["S_G"].dropna().unique())
#     ]
#
#     return state_options, year_options, grower_options
#


def callback_stat(app):
    @app.callback(
        Output("Pchi_square-message", "is_open"),
        [Input("Pchi_square-open", "n_clicks"),
         Input("Pchi_square-close", "n_clicks")],
        [State("Pchi_square-message", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        Output("anova-message", "is_open"),
        [Input("anova-open", "n_clicks"), Input("anova-close", "n_clicks")],
        [State("anova-message", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        [
            Output("observation", "data"),
            Output("observation", "columns"),
        ],
        [
            Input("row-name", "value"),
            Input("col-name", "value"),
            Input("state_type", "value"),
            Input("year", "value"),
            Input("grower", "value"),
            Input("store-uploaded-data", "data")
        ],
    )
    def Observed_Contingency_Table(row, col, state, year, grower, data):
        if data:
            df = pd.DataFrame(data)
        # temp = df[(df["S_STATE"].isin([state])) & (df["VARIETY"].isin([variety])) & (df["S_G"].isin([grower])) ]
        temp = df.copy()
        if state != "All":
            temp = temp[(temp["S_STATE"].isin([state]))]
        if year != "All":
            temp = temp[(temp["S_YR"].isin([year]))]
        if grower != "All":
            temp = temp[(temp["S_G"].isin([grower]))]
        # temp = temp[(temp["VARIETY"].isin([variety]))]
        # temp = df[(df["S_STATE"].isin([state]))  & (df["S_G"].isin([grower]))]
        temp = temp.groupby([row, col]).size(
        ).unstack().fillna(0).reset_index()
        data = temp.to_dict('records')
        columns = [{"name": str(i), "id": str(i)} for i in temp.columns]
        return data, columns

    @app.callback(
        Output("chi-summary", "children"),
        [
            Input("row-name", "value"),
            Input("col-name", "value"),
            Input("slider-chisquare", "value"),
            Input("state_type", "value"),
            Input("year", "value"),
            Input("grower", "value"),
            Input("store-uploaded-data", "data")
        ],
    )
    def chi_square_test(row, col, significance_level, state, year, grower, data):
        if data:
            df = pd.DataFrame(data)
        temp = df.copy()
        if state != "All":
            temp = temp[(temp["S_STATE"].isin([state]))]
        if year != "All":
            temp = temp[(temp["S_YR"].isin([year]))]
        if grower != "All":
            temp = temp[(temp["S_G"].isin([grower]))]
        temp = temp.groupby([row, col]).size().unstack().fillna(0)
        chi, pval, dof, exp = chi2_contingency(temp)
        chi_test_columns = [
            "Null HYpothesis", "Alternative Hypothesis", "Chi-Square score", "df", "P-value"]
        columns = [{"name": i, "id": i} for i in chi_test_columns]
        data = ["independence", "Association",
                np.round(chi, 4), dof, np.round(pval, 4)]
        data = pd.DataFrame(data, index=chi_test_columns).T.to_dict("record")

        return dash_table.DataTable(
            id='chi-summary-table',
            data=data,
            columns=columns,
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'Alternative Hypothesis',
                        # since using .format, escape { with {{
                        'filter_query': '{{P-value}} <= {}'.format(significance_level)
                    },
                    'backgroundColor': '#85144b',
                    'color': 'white'
                },
                {
                    'if': {
                        'column_id': 'Null HYpothesis',
                        # since using .format, escape { with {{
                        'filter_query': '{{P-value}} > {}'.format(significance_level)
                    },
                    'backgroundColor': '#85144b',
                    'color': 'white'
                },
            ]
        )

    @app.callback(
        Output("anova-summary", "children"),
        [
            Input("anova-row-name", "value"),
            Input("anova-col-name", "value"),
            Input("slider-anova", "value"),
            Input("state_type", "value"),
            Input("year", "value"),
            Input("grower", "value"),
            Input("store-uploaded-data", "data")
        ],
    )
    def anova_test(row, col, significance_level, state, year, grower, data):
        if data:
            df = pd.DataFrame(data)
        temp = df.copy()
        if state != "All":
            temp = temp[(temp["S_STATE"].isin([state]))]
        if year != "All":
            temp = temp[(temp["S_YR"].isin([year]))]
        if grower != "All":
            temp = temp[(temp["S_G"].isin([grower]))]
        model = ols("{} ~ {}".format(row, col), data=temp[[row, col]]).fit()
        columns = [{"name": i, "id": i} for i in anova_columns]
        data = ["independence", "Association", np.round(
            model.fvalue, 4), model.df_model, np.round(model.f_pvalue, 4)]
        data = pd.DataFrame(data, index=anova_columns).T.to_dict("record")
        print(data)

        return dash_table.DataTable(
            id='anova-summary-table',
            data=data,
            columns=columns,
            style_data_conditional=[
                {
                    'if': {
                        'column_id': 'Alternative Hypothesis',
                        'filter_query': '{{P-value}} <= {}'.format(significance_level)
                    },
                    'backgroundColor': '#85144b',
                    'color': 'white'
                },
                {
                    'if': {
                        'column_id': 'Null HYpothesis',
                        'filter_query': '{{P-value}} > {}'.format(significance_level)
                    },
                    'backgroundColor': '#85144b',
                    'color': 'white'
                },
            ]
        )
