import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/"),
        dbc.DropdownMenuItem("Virus", href="/Virus"),
        dbc.DropdownMenuItem("Disease", href="/Disease"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Potato Dash", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

app.layout = html.Div([
    navbar,
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
    html.Div(id='output-data-upload'),
])


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
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

    return html.Div([

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


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



if __name__ == '__main__':
    app.run_server(debug=False)