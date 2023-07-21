# To run the dashboard
1. Install all the requirements from the requirements.txt file from folder imd_dashboard
2. Unzip 'the mask_files.zip file from imd_dashboard/data and use these as we have ordered them according to districts
3. Run the index.py file after doing the following:

In dash_app.py: <br>*line 53* - ensure argument is the correct file path. <br>
		*line 109*- change argument to india_shapefile_s.json (according to path in server) <br>
		*lines 134-139* - ensure approrpriate file paths. <br>
		*line 172* - ensure appropriate file path <br>

In ncvis.py: <br>*line 12* - change filepath -- DON'T CHANGE {year}
In rain_color_interactive_using_mask.py: <br>
	*line 10* - ensure appropriate root directory for data <br>
	*line 14* - ensure appropriate directory (should be under /home/data/IMD_gridded_data/rf I think) <br>
	*line 37* - ensure appropriate file path <br>

In temperature_plot.py - 
	*lines 9, 13, 22* - ensure appropriate file paths
