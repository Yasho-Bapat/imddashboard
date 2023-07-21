from datetime import date
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import geopandas as gpd
import numpy as np
import plotly.express as px, pandas as pd
import rain_color_interactive_using_mask as rm
import temperature_plot as t
import plotly.graph_objects as go

'''THIS CODE DESCIRIBES THE WEBPAGE MADE USING DASH.
    FEATURES: choropleth map, date range selector, each district as a button, when district is clicked, DRY days graph is displayed '''

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#----------------------------------------------------------------------------------------------------------------------------------------
# HTML webpage layout
layout = html.Div([
    html.H2("District wise rainfall analysis and visualization tool", style={'text-align': 'center', 'font-family':'Inter'}),
    html.Div([
        dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2012, 1, 1),
        max_date_allowed=date(2022, 12, 31),
        initial_visible_month=date(2022, 1, 15), clearable=True, style={'padding': '20px'}, updatemode='bothdates'),
        dcc.RadioItems(['Total Rainfall', 'Anomalies (deviation from mean)', 'Minimum temperature map', 'Maximum temperature map'], 'Total Rainfall', id = 'rainfall_filter',  labelStyle={'display': 'inline-block', 'marginTop': '5px', 'padding': '0 20px'})
    ],
    style = {'width': '49%'}),
 
    dcc.Graph(id='rainfall_map', figure={}, style={'align': 'left', 'width': '50%', 'height': '900px', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id = 'dry_days', figure = {}),
        dcc.Graph(id = 'wet_days', figure={})
    ], style={'width': '50%', 'display': 'inline-block'})

])
#----------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------
# app callbacks and functions
@callback(
    [
        Output(component_id='rainfall_map', component_property='figure')
    ],
    [
        Input('my-date-picker-range', 'start_date'),
        Input('my-date-picker-range', 'end_date'),
        Input('rainfall_filter', 'value')
    ]
)
def update_graph(start_date, end_date, value):
    print(value)
    data = gpd.read_file("finalised.json" )
    gdf = gpd.GeoDataFrame(data)
    if start_date is not None and end_date is not None:
        print(start_date, end_date)
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')

        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        valid = False
        if (end_date - start_date).days > 0:
            valid = True
        if value == 'Total Rainfall' and valid:
            # Call total rainfall function from rm.py
            final = rm.rainfall(start_date, end_date)
            max = np.amax(final['rain'])
            # Plotting
            fig = px.choropleth_mapbox(final, geojson=data, color="rain", 
                                       locations='DISTRICT_1', featureidkey="properties.DISTRICT_1",
                                       mapbox_style="white-bg", zoom= 3.25, 
                                       center={"lat": 22.5, "lon": 78.96}, 
                                       opacity=0.75, 
                                       title=f"Total rainfall between {start_date_string} and {end_date_string}",  
                                       labels = {'DISTRICT_1': 'District', 'rain': 'Rainfall in mm'}, 
                                       color_continuous_scale=px.colors.sequential.Viridis_r, 
                                       color_continuous_midpoint=0.3*max, 
                                       width= 750, height= 750)
            print('>>success')
            
            # Change font face
            fig.update_layout(clickmode = 'event+select', title_font_family = 'Inter', font_family = 'Inter')
        elif value == 'Anomalies (deviation from mean)':
            # Call anomalies function fron rainfall.py
            #final = rainfall.anomalies(start_date) '''NEED TO UPDATE ACCORDINGLY'''

            # Plotting
            fig = px.choropleth_mapbox(final, geojson=data, color="Rainfall", locations='DISTRICT', featureidkey="properties.DISTRICT", mapbox_style="carto-positron", zoom= 3.25, center={"lat": 22.5, "lon": 78.96}, opacity=0.75, title=f"Deviation from average rainfall on {start_date_string} from 1901")
            print('success')
            
            # Change font face
            fig.update_layout(clickmode = 'event+select', title_font_family = 'Inter', font_family = 'Inter')
        elif value == "Minimum temperature map":
            final = t.temperaturesOn(start_date, end_date, "MINT")
            data = gpd.read_file("D:\Downloads\imd_data\india_shapefile_s.json")

            # Plotting
            fig = px.choropleth_mapbox(final, geojson=data, color="MINT", locations='DISTRICT', featureidkey="properties.DISTRICT", mapbox_style="white-bg", zoom= 3.25, center={"lat": 22.5, "lon": 78.96}, opacity=0.75, title=f"District-wise minimum temperatures on {start_date_string}",color_continuous_scale=px.colors.diverging.RdYlBu_r)
            print('success')
            
            # Change font face
            fig.update_layout(clickmode = 'event+select', title_font_family = 'Inter', font_family = 'Inter')
            fig.update_traces(zmin = 0, zmax = 48)
        elif value == "Maximum temperature map":
            final = t.temperaturesOn(start_date, end_date, "MAXT")
            data = gpd.read_file("D:\Downloads\imd_data\india_shapefile_s.json")

            # Plotting
            fig = px.choropleth_mapbox(final, geojson=data, color="MINT", locations='DISTRICT', featureidkey="properties.DISTRICT", mapbox_style="white-bg", zoom= 3.25, center={"lat": 22.5, "lon": 78.96}, opacity=0.75, title=f"District-wise minimum temperatures on {start_date_string}",color_continuous_scale=px.colors.diverging.RdYlBu_r)
            print('success')
            
            # Change font face
            fig.update_layout(clickmode = 'event+select', title_font_family = 'Inter', font_family = 'Inter')
            fig.update_traces(zmin = 0, zmax = 48)
        return [fig]
    fig = px.choropleth_mapbox(gdf, geojson=data, locations='DISTRICT_1', featureidkey="properties.DISTRICT_1", mapbox_style="carto-positron", zoom= 3.25, center={"lat": 22.5, "lon": 78.96}, opacity=0.75)
    fig.update_layout(clickmode = 'event+select', title_font_family = 'Inter', font_family = 'Inter')
    return [fig]

@callback(
    Output('dry_days', 'figure'),
    Output('wet_days', 'figure'),
    Input('rainfall_map', 'clickData'), 
    Input('rainfall_filter', 'value')
)
def display_click_data(clickData, value):
    districtname = clickData['points'][0]['location'].upper()
    print(districtname)
    print(clickData)
    if value == "Minimum temperature map" or value == "Maximum temperature map":
        df = pd.read_csv(r"D:\Downloads\imd_data\yearly_avg_temp.csv")
        wdf = pd.read_csv(r"D:\Downloads\imd_data\winter_avgs.csv")
        predf = pd.read_csv(r"D:\Downloads\imd_data\pre-monsoon_avgs.csv")
        postdf = pd.read_csv(r"D:\Downloads\imd_data\post-monsoon_avgs.csv")
        mdf = pd.read_csv(r"D:\Downloads\imd_data\southwest-monsoon_avgs.csv")
        print(df[df['DISTRICT'] == districtname])

        #creating a copy of the dataframe with only required district's data
        tdf = df[df['DISTRICT'] == districtname]
        wdf = wdf[wdf['DISTRICT'] == districtname]
        predf = predf[predf['DISTRICT'] == districtname]
        postdf = postdf[postdf['DISTRICT'] == districtname]
        mdf = mdf[mdf['DISTRICT'] == districtname]
        

        tdf = tdf.drop(['FID', 'DISTRICT', 'STATE'], axis=1)
        wdf = wdf.drop(['FID', 'DISTRICT', 'STATE'], axis=1)
        predf = predf.drop(['FID', 'DISTRICT', 'STATE'], axis=1)
        postdf = postdf.drop(['FID', 'DISTRICT', 'STATE'], axis=1)
        mdf = mdf.drop(['FID', 'DISTRICT', 'STATE'], axis=1)

        ys = wdf.columns


        tdf = tdf.melt(var_name = 'Year', value_name = 'Average Temperature')
        wdf = wdf.melt(var_name = 'Year', value_name = 'Average Temperatures')

        tempfig = px.line(tdf, x='Year', y='Average Temperature', markers=True, title=f'Average temperature in {districtname.capitalize()} since 1970')
        tempfig.update_layout(font_family = 'Inter', title_font_family = 'Inter')

        winterfig = px.line(wdf, x='Year', y='Average Temperatures', title=f'Average seasonal temperatures in {districtname.capitalize()} since 1970')
        winterfig.add_trace(go.Scatter(x=ys, y=predf.iloc[0].tolist(), mode = 'lines', name='Pre-monsoon'))
        winterfig.add_trace(go.Scatter(x=ys, y=mdf.iloc[0].tolist(), mode = 'lines', name='Monsoon'))
        winterfig.add_trace(go.Scatter(x=ys, y=postdf.iloc[0].tolist(), mode = 'lines', name='Post-monsoon'))
        winterfig.update_layout(font_family = 'Inter', title_font_family = 'Inter')

        return tempfig, winterfig
    else:
        df = pd.read_csv("D:\Downloads\imd_data\dry_wet_days.csv")
        print(df[df['DISTRICT'] == districtname])
        ddf = df[df['DISTRICT'] == districtname]
        wdf = df[df['DISTRICT'] == districtname]

        
        # keeping only dry days values columns in ddf (dry df) and wet days columns in wdf (wet df)
        for col in ddf.columns:
            if ('Dry Days' not in col):
                ddf = ddf.drop([col], axis = 1)
                wdf = wdf.rename(columns = {col:col[:4]})
            else:
                wdf = wdf.drop([col], axis = 1)
                ddf = ddf.rename(columns = {col:col[:4]})
        wdf = wdf.drop(['FID', 'DIST', 'STAT'], axis = 1)

        # reshaping the df into a single column for years and corresponding values
        ddf = ddf.melt(var_name='Year', value_name='Dry Days') 
        wdf = wdf.melt(var_name = 'Year', value_name = 'Wet Days')
        dryfig = px.line(ddf, x='Year', y='Dry Days', markers=True, title=f'Dry days in {districtname.capitalize()} over the years')
        
        wetfig = px.line(wdf, x = 'Year', y = 'Wet Days', markers=True, title = f'Wet days in {districtname.capitalize()} over the years')
        print(ddf.values)
        
        dryfig.update_layout(font_family = 'Inter', title_font_family = 'Inter')
        wetfig.update_layout(font_family = 'Inter', title_font_family = 'Inter')
        return dryfig, wetfig

