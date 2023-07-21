import geopandas as gpd
import netCDF4 as nc
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

DIRECTORY1 = r"C:/Users/Shardul/Downloads/imd_data/temperature/MAXT"
DIRECTORY2 = r"C:/Users/Shardul/Downloads/imd_data/temperature/MINT"
data = gpd.read_file("C:/Users/Shardul/Downloads/imd_data/shapefile/india_shapefile.json")
gdf = gpd.GeoDataFrame(data)
gdf=gdf.drop('geometry',axis=1)

for year in range(1970,2022):                   //Range of years as per data
    filename_MAX = f"{DIRECTORY1}/MAXT{year}.nc"
    filename_MIN = f"{DIRECTORY2}/MINT{year}.nc"
    print(year)
    ncdata_max = nc.Dataset(filename_MAX)
    ncdata_min = nc.Dataset(filename_MIN)

    temp_max = ncdata_max.variables['TMAX'][:]
    temp_min = ncdata_min.variables['TMIN'][:]
    
    coords = pd.read_csv("C:/Users/Shardul/Downloads/imd_data/temperature/Coordinates.csv")
    latspos = coords['Latitude'].tolist()
    lngspos = coords['Longitude'].tolist()

    //Enter range of days in subset_max and subset_min:
    //  1. Winter -> 0 to 59
    //  2. Pre-monsoon -> 59 to 153
    //  3. Southwest-monsoon -> 153 to 275
    //  4. Post-monsoon -> 275 to 365
    
    subset_max = temp_max[:, latspos, lngspos] 
    subset_min=temp_min[:, latspos, lngspos]
    tempdata = np.mean((subset_max+subset_min)/2, axis=0).tolist()
    
    tempdata = [round(float(value), 3) if value not in ["--", None] else 0 for value in tempdata]
    
    df = pd.DataFrame({'DISTRICT':coords['DISTRICT'], 'STATE':coords['STATE'], 'temp':tempdata})
    avg_temps = df.groupby('DISTRICT')['temp'].mean().round(3).reset_index()
    avg_temps.columns = ['DISTRICT', f"{year}"]
    gdf = gdf.merge(avg_temps, on='DISTRICT', how='left')
gdf.to_csv("post-monsoon_avgs.csv",index=False)     //name can be changed manually in this line as per range passed
