from datetime import date as dates
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import geopandas as gpd
import netCDF4 as nc
import numpy as np
import plotly.express as px, pandas as pd
import datetime as dt
from shapely.geometry import Point
import dash_bootstrap_components as dbc
import ncvis


# -------------------------------------------------------------------------------------------
# HTML layout
layout = html.Div([
    html.H2("Gridded Data visualization", style={'text-align': 'center', 'font-family':'Inter'}),
    html.Div([
        dcc.DatePickerSingle(
            id = 'date-picker',
            min_date_allowed=dates(2012, 1, 1),
            max_date_allowed=dates(2022, 12, 31),
            initial_visible_month=dates(2022, 1, 1), clearable=True,
            date=dates(2021, 1, 1), style={'padding' : '20px'}
        )
    ]),
    dcc.Graph(id='landing-graph', figure={}, style={'width': '47%', 'height': '650px', 'align':'center'})
])

@callback(
    Output('landing-graph', 'figure'),
    Input('date-picker', 'date')
)

def update_graph(date):
    return ncvis.rainfallLanding(date)

