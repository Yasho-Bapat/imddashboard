import geopandas as gpd
import netCDF4 as nc
import numpy as np
import folium
import pandas as pd
import datetime as dt

def temperaturesOn(st_date, end_date, info):
    data = gpd.read_file("D:\Downloads\imd_data\india_shapefile_s.json")
    gdf = gpd.GeoDataFrame(data)

    year = st_date.year
    DIRECTORY = f"D:\Downloads\imd_data\T{info[:3]}"
    filename = f"{DIRECTORY}\{info}{year}.nc"
    
    ncdata = nc.Dataset(filename)
    sday_no = (st_date - dt.datetime(year, 1, 1)).days
    eday_no = (end_date - dt.datetime(year, 1, 1)).days

    temp = ncdata.variables['T'+info[0:3]][:] #TMAX or TMIN
    
    coords = pd.read_csv("D:\Downloads\imd_data\Coordinates.csv")
    latspos = coords['Latitude'].tolist()
    lngspos = coords['Longitude'].tolist()
    subset = temp[sday_no:eday_no+1, latspos, lngspos]
    if info=='MAXT':
        tempdata = np.max(subset, axis=0).tolist() #get max temp for the range passed
    else:
        tempdata = np.min(subset, axis=0).tolist() #get min temp for the range passed
    #can extend this to get mean using np.mean
    
    tempdata = [round(float(value), 3) if value not in ["--", None] else 0 for value in tempdata]
    
    df = pd.DataFrame({'DISTRICT':coords['DISTRICT'], 'STATE':coords['STATE'], 'temp':tempdata})
    avg_temps = df.groupby('DISTRICT')['temp'].mean().round(3).reset_index()
    avg_temps.columns = ['DISTRICT', info]
    # Merge the average temperatures with the GeoDataFrame
    gdf = gdf.merge(avg_temps, on='DISTRICT', how='left')
    gdf = gdf.drop('geometry',axis=1)
    print(gdf)
    #gdf.to_csv("2019_1_1.csv",index=False)
    return gdf