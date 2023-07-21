from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
layout = html.Div([
    html.H1("Welcome to IMD Pune's web-based gridded data visualization tool.", style={'text-align': 'center', 'font-family':'Inter', 'padding':'70px 0'}),
    html.H3("Select a link to start visualizing India's GeoSpatial Data.",style={'text-align': 'center', 'font-family':'Inter', 'color': '#757b7c'})
])