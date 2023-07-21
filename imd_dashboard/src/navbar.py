from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Gridded Data", href="/page1")),
                dbc.NavItem(dbc.NavLink("Interactive District-wise Visualization ", href="/page2")),
            ] ,
            brand="IMD Pune",
            brand_href="https://www.imdpune.gov.in/",
            color="dark",
            dark=True,
        ), 
    ])

    return layout