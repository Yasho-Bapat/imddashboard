import geopandas as gpd
import datetime as dt
import netCDF4 as nc
import numpy as np
import folium
import os
import numpy.ma as ma


DIRECTORY = r'D:\Downloads\imd_data\rainfall' # 


def get_district_rainfall(arr):
    MASK_FILES = r"D:\Downloads\imd_data\mask_files"
    values = []
    for filename in os.listdir(MASK_FILES):
        print(filename)
        file_path = os.path.join(MASK_FILES, filename)
        maskdata = nc.Dataset(file_path)
        mask_coord = maskdata.variables['mask'][:]
        lat = maskdata.variables['latitude'][:]
        #print(maskdata)
        values.append(float(np.round(np.sum(arr * mask_coord)/(np.sum(mask_coord)),3)))
    return values


def rainfall(start_date, end_date):
    print('starting scan')
    year = start_date.year

    filename = f"{DIRECTORY}\IMD0p25{year}.nc"
    print(filename)
    ncdata = nc.Dataset(filename)
    
    sday_no = (start_date - dt.datetime(year, 1, 1)).days
    eday_no = (end_date - dt.datetime(year, 1, 1)).days

    data = gpd.read_file("D:\Downloads\india_shapefile.json")
    ncdata = nc.Dataset(filename, 'r')
    gdf = gpd.GeoDataFrame(data)
    rain = ncdata.variables['RAINFALL'][:]
    print('>> data read')

    reduced_rain = np.sum(rain[sday_no:eday_no], axis=0) #give start date and end date here
    print('>> reduced_rain calculated')
    masked_reduced_rain = ma.masked_invalid(reduced_rain)
    masked_reduced_rain = ma.masked_where(reduced_rain.any() == "--", reduced_rain)
    masked_reduced_rain = np.round(masked_reduced_rain, 3)
    print('>> masked arg calculated')
    gdf['rain']=get_district_rainfall(masked_reduced_rain)
    
    #gdf = gdf.drop('geometry',axis=1)
    gdf.to_csv("tesing_2019.csv",index=False)
    return gdf
    '''
m = folium.Map(location = [20.5, 78.96], zoom_start=5)
fdata = "C:/Users\Shardul\Downloads\imd_data\shapefile\india_shapefile.json"

custom_scale = (gdf['rain'].quantile((0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1))).tolist()
choropleth_layer = folium.Choropleth(geo_data = fdata, 
                  name = "chloropleth", 
                  data = gdf, 
                  columns = ["DISTRICT_1", "rain"], 
                  fill_color='GnBu', 
                  key_on = "feature.properties.DISTRICT_1",
                  threshold_scale=custom_scale,
                  fill_opacity=0.9, 
                  line_opacity=0.2,
                  legend_name='Rainfall in mm').add_to(m)

tooltip_layer = folium.GeoJsonTooltip(
    fields=['DISTRICT_1','STATE_NAME'],  
    aliases=['District:', 'State:'],  
    labels=True,
    sticky=False)
choropleth_layer.geojson.add_child(tooltip_layer)
m.show_in_browser()'''

