import netCDF4 as nc
import geopandas as gpd
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def rainfallLanding(date):
    date = pd.to_datetime(date)
    year = date.year
    data = nc.Dataset(f"D:\Downloads\imd_data\Rain0p25\IMD0p25{year}.nc") 
    #data = nc.Dataset(r"D:\Downloads\RF25_ind2022_rfp25.nc")
    epoch = f'{year}-01-01'
    epoch = pd.to_datetime(epoch)
    time_location = date - epoch

    min = np.amax(data.variables['RAINFALL'][time_location.days])

    trace = go.Heatmap(x=data.variables['LONGITUDE'], y = data.variables['LATITUDE'], z=data.variables['RAINFALL'][time_location.days], colorscale=[[0, '#ffffff'], [0.5, '#8f9bc9'], [1, '#4d004b']], zmin=(1-1.2*min), zmax=min, zmid = np.mean(data.variables['RAINFALL'][time_location.days]), zauto=False, zsmooth='fast')

    layout = go.Layout(title=f'Rainfall in India on {date}')
    fig = go.Figure(data=[trace], layout=layout)
    return fig