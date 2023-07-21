from dash import html, dcc
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output

# Connect to main app.py file
# Connect to your app pages
import dash_app as da, dash_landing_page as dl, landingpage as lp

# Connect the navbar to the index
import navbar

# define the navbar
nav = navbar.Navbar()

# Define the index page layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width"}], suppress_callback_exceptions=True)
app.layout = html.Div([dcc.Location(id='url', refresh=False), nav, html.Div(id='page-content', children=[])])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/page1':
        return dl.layout
    if pathname == '/page2':
        return da.layout
    if pathname == '/':
        return lp.layout
    else:
        return "404 Page Error! Please choose a link"

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)