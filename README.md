# To run the dashboard
1. Install all the requirements from the requirements.txt file from folder imd_dashboard
2. Run the index.py file after doing the following:

In dash_app.py: line 53 - ensure argument is the correct file path.
		   line 109- change argument to india_shapefile_s.json (according to path in server)
		   lines 134-139 - ensure approrpriate file paths.
		   line 172 - ensure appropriate file path

In ncvis.py: line 12 - change filepath -- DON'T CHANGE {year}
In rain_color_interactive_using_mask.py:
	line 10 - ensure appropriate root directory for data
	line 14 - ensure appropriate directory (should be under /home/data/IMD_gridded_data/rf I think)
	line 37 - ensure appropriate file path

In temperature_plot.py - 
	lines 9, 13, 22 - ensure appropriate file paths
