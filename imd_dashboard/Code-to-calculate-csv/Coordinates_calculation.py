import geopandas as gpd
import netCDF4 as nc
import numpy as np
import pandas as pd
import datetime as dt
import time as t

data = gpd.read_file("C:/Users/Shardul/Downloads/imd_data/shapefile/india_shapefile.json")
gdf = gpd.GeoDataFrame(data)
ncdata = nc.Dataset("C:/Users/Shardul/Downloads/imd_data/temperature/MAXT/MAXT2001.nc")
lngs = ncdata.variables['LONGITUDE'][:]
lats = ncdata.variables['LATITUDE'][:]

points_x = gdf['geometry'].apply(lambda geom: list(geom.exterior.xy[1])).explode().tolist()
points_y = gdf['geometry'].apply(lambda geom: list(geom.exterior.xy[0])).explode().tolist()
dist = gdf['DISTRICT_1'].repeat(gdf['geometry'].apply(lambda geom: len(geom.exterior.xy[0]))).tolist()
state = gdf['STATE_NAME'].repeat(gdf['geometry'].apply(lambda geom: len(geom.exterior.xy[0]))).tolist()

roundedx = [round(x * 2) / 2 for x in points_x]
roundedy = [round(y * 2) / 2 for y in points_y]

lngspos = list()
latspos = list()
for x in roundedx:
    try:
        latspos.append(int(np.where(lats == x)[0]))
    except:
        latspos.append(int(np.where(lats == 7.5)[0]))
lngspos = [int(np.where(lngs == y)[0]) for y in roundedy]

df = pd.DataFrame({'DISTRICT':dist, 'STATE':state, 'Latitude':latspos, 'Longitude':lngspos})
df.to_csv("C:/Users/Shardul/Downloads/imd_data/temperature/Coordinates.csv")
