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
from app import app
import pathlib

LINEBREAK_STYLE = {
    'border': '3px solid white'
}

homepage = dbc.Jumbotron(
    [
        html.H3("FAQ", className="display-5"),
        html.Br(),
                html.P(
            "Q: How can I learn to use the dashboard? ",
            className="lead",
        ),
        html.P(
            "A: You can check out the documentation (https://github.com/solislemuslab/potato-seed-cert/blob/master/DOCS.md)."
        ),
        html.Hr(className="my-2"),

        html.P(
            "Q: How can I get help? ",
            className="lead",
        ),
        html.P(
            "A: Make sure to check out the documentation (https://github.com/solislemuslab/potato-seed-cert/blob/master/DOCS.md). Also, check out the Potato Seed Dashboard google user group where people post questions/answers. You can join to post questions: https://groups.google.com/g/potato-seed-dashboard "
        ),
        html.Hr(className="my-2"),

        html.P(
            "Q: Is the Potato Seed Dashboard open-source? Where can I find the code?",
            className="lead",
        ),
        html.P(
            "A: Yes, the Potato Seed Dashboard is open source and you can find all the code in the GitHub repository here: (https://github.com/solislemuslab/potato-seed-cert)."
        ),
        html.Hr(className="my-2"),

        html.P(
            "Q: I found a bug or error in the dashboard, how can I report it?",
            className="lead",
        ),
        html.P(
            "A: You should file an issue in the github repo: https://github.com/solislemuslab/potato-seed-cert/issues",
        ),
        html.Hr(className="my-2"),

        html.P(
            "Q: How can I provide positive (or constructive) feedback?",
            className="lead",
        ),
        html.P(
            "A: Users feedback is very important to us! Please use this form: https://docs.google.com/forms/d/e/1FAIpQLSficG2nYBjuAoIuetYC-5CRm339ZEZ_-uewd_d_3nVeGFMXUA/viewform"
        ),
        html.Hr(className="my-2"),

    ]
)