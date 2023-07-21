import netCDF4 as nc
import numpy as np
import numpy.ma as ma
import os
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def get_dry_days(arr):
    values = []
    dry_calc = np.zeros(716, dtype=int)               //Put number of districts in place of 716
    for filename in os.listdir(MASK_FILES):
        file_path = os.path.join(MASK_FILES, filename)
        maskdata = nc.Dataset(file_path)
        mask_coord = maskdata.variables['mask'][:]
        #lat = maskdata.variables['latitude'][:]
        values.append(ma.sum(arr * mask_coord)/np.sum(mask_coord)) //use formula
    dry_calc = np.less(values, 0.1).astype(int)
    return dry_calc

MASK_FILES = r"C:/Users/Shardul/Downloads/imd_data/mask files"
DIRECTORY = r"C:/Users/Shardul/Downloads/imd_data/rainfall"
gdf = pd.read_csv("C:/Users/Shardul/Downloads/PS1/dry_wet_final.csv")
#print(gdf.iloc[127])

for filename in os.listdir(DIRECTORY):
    file_path = os.path.join(DIRECTORY, filename)
    year = filename[-7:-3]
    print(year)
    ncdata = nc.Dataset(file_path)
    rain = ncdata.variables['RAINFALL'][:]
    dry_days = np.zeros(716, dtype=int)          //Put number of districts in place of 716
    for i,reduced_rain in enumerate(rain):
        print(i)
        masked_reduced_rain = ma.masked_invalid(reduced_rain)
        dry_days += get_dry_days(masked_reduced_rain)
    gdf[f'{year} Dry Days'] = dry_days
gdf.to_csv("dry_wet_final.csv",index=False)   //this csv file will contain all dry days for all years for 1901 to 2022
