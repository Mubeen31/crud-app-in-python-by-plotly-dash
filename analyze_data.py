import dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
from datetime import datetime
import pandas as pd
import pyrebase
from data import config

firebase = pyrebase.initialize_app(config)
db = firebase.database()

print(db.child('-NS10u5zd0CuZI7dRPiN').remove())
