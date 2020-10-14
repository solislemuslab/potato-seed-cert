import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output
import pandas as pd
import xlrd



df = pd.read_excel("2003-2016 Seed Potato Cert data v20191204_NO FL lines_Rioux 5AUG2020.xlsx", sheet_name="2003-2016 Seed Potato Cert")
print(df.head())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

features = df.columns
print(features)

virus = df.columns[df.columns.str.contains("SR1")]

frequent_state = df["S_STATE"].value_counts()[:8].index.to_list()

first_inspection_virus = df.columns[df.columns.str.contains("SR1")].tolist()
second_inspection_virus = df.columns[df.columns.str.contains("SR2")].tolist()

years = sorted(df["S_YR"].value_counts()[:-2].index)
year_options = []
for year in years:
    year_options.append({"label":str(year),"value":year})


app.layout = html.Div([
    html.Div([
        dcc.Dropdown(id='year',
                     options=year_options,
                     value=years[0])
    ]),
    html.Div([
        dcc.Dropdown(id='yaxis',
                     options= [{"label":i,"value":i} for i in first_inspection_virus],
                     value="SR1_LR")
    ]),
    dcc.Graph(id='feature-graphic')
])

@app.callback(
    Output("feature-graphic","figure"),
    [Input("year","value"),
    Input("yaxis",'value')]
)
def update_figure(year, yaxis_name):
    firstIns_df = df[(df["S_STATE"].isin(frequent_state)) & (df["S_YR"] == year)].groupby("S_STATE").mean()[first_inspection_virus]
    firstIns_df = firstIns_df.reset_index()

    fig = go.Figure(data=[
        go.Bar(name='LR', y=firstIns_df["S_STATE"], x=firstIns_df[yaxis_name], orientation='h')
        # go.Bar(name='MOS', y=firstIns_df["S_STATE"], x=firstIns_df["SR1_MOS"], orientation='h'),
        # go.Bar(name='MIX', y=firstIns_df["S_STATE"], x=firstIns_df["SR1_MIX"], orientation='h'),
    ])

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    # fig.update_xaxes(title=xaxis_column_name,
    #                  )

    fig.update_yaxes(title="S_STATE")
    fig.update_xaxes(title=yaxis_name)

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)

