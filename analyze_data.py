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

retrieve_data = db.get()
df = pd.DataFrame.from_dict(retrieve_data.val(), orient='index')
df = df.reset_index()
df.rename(columns={'index': 'id'}, inplace=True)
print(df)
