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
            "Q: How can I get help? ",
            className="lead",
        ),
        html.P(
            "A: Check out the WI Fast Stats google user group where people post questions/answers. You can join to post questions: https://groups.google.com/g/wi-fast-stats "
        ),
        html.Hr(className="my-2"),

        html.P(
            "Q: I found a bug or error in the code, how can I report it?",
            className="lead",
        ),
        html.P(
            "A: You should file an issue in the github repo: https://github.com/crsl4/fast-stats/issues",
        ),
        html.Hr(className="my-2"),

        html.P(
            "Q: How can I provide positive (or constructive) feedback?",
            className="lead",
        ),
        html.P(
            "A: Users feedback is very important to us! Please use this form"
        ),
        html.Hr(className="my-2"),

        html.P(
            "Q: If I use the website and web apps in my work, how do I cite them?",
            className="lead",
        ),
        html.P(
            "A: If you use the website or web apps in your work, we ask that you cite this paper"
        ),
        html.Hr(className="my-2"),

        html.P(
            "Q: Cool website! Is this a free template?",
            className="lead",
        ),
        html.P(
            'A: The design and development of the website is by "WebThemez" '
            '(http://webthemez.com) who made it available under a Creative Commons Attribution 3.0 license.'
        ),
        html.Hr(className="my-2"),

    ]
)