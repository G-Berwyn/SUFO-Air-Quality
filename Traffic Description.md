# SUFO Traffic

Description of the functions developed to help identify and load data from traffic sensors near an air quality sensor (or any coordinates)

# Included Functions

The functions incuded in this package are:
- get_sensor - Used for getting data from one sensor
- parse_sensor - Get's data for a large time period and saves as a pickle
- locate_traffic_sites - Identified traffic sites within a radius of given coordinates
- plot_sites - Downloads a shapefile and plots the location of traffic sensors

And the requisite functions for these are:
- line_distance - Calculates the line distance between two coordinates
- calculate_bounding_box - Calculates a bounding box for plotting
- replace_missing - Replaces missing data with the mean
- calculate_traffic_diff - Calculates the difference in traffic either side of the CAZ (deprecated)

## get_sensor(site_id,start,end)
Function that will take the specified start and end times, query data for that site and return a Pandas DF with the data. Limited to one month of data due to SUFO restrictions.

Inputs:
- site_id - String of the site ID, for example "S0110" or "UKA00575"
- start - String with the start data in ISO format
- end - String with the end date in ISO format
  
Output: Dataframe with data by row from SUFO

## parse_sensor(site_id,date_start,date_end,path)
Function that will take a larger data range and return the traffic flows saved as a pickle on the specified path.

Inputs:
- site_id - String of the site ID, for example "S0110" or "UKA00575"
- date_start - String with the start data in ISO format
- date_end - String with the end date in ISO format
- path - String with a path to save the pickle onto

Output: A Pandas pickle saved to the specified path. Can be read back into Python.

For reading pickles into R, see this [Stack Overflow post](https://stackoverflow.com/questions/35121192/reading-a-pickle-file-pandas-python-data-frame-in-r)

## locate_traffic_sites(lat, long, radius,start_date,end_date,add_distance = 0)
Function that lists all the traffic sensors within a given radius of the coordinates

Inputs:
- lat - String with the latitude of the point
- long - String with the longitude of the point
- radius - Search radius (in km) from the point, limited to 1km
- start_date - Start of time period to search
- end_date - End of time period to search
- add_distance = 0 - Optional argument off as a default to calculate the distance of each sensor from the original point, set to 1 to calculate.

Output: A dictionary with each sensor as an entry and the sensor coordinates stored as a tuple.

Can be converted into a DF for easier viewing

## plot_sites(lat,long,radius, date_start, date_end, path)
Functions that will plot the locations of Traffic sites in relation to a given point. Function will call *locate_traffic_sites* to identify sensors then plot then on a map. The map is automatically downloaded as a shapefile and saved onto the path

Inputs:
- lat - String with the latitude of the point
- long - String with the longitude of the point
- radius - Search radius (in km) from the point, limited to 1km
- start_date - Start of time period to search
- end_date - End of time period to search
- path - The path to save the map shapefile into

Outputs: matplotlib.pyplot plot

## line_distance(lat1,long1,lat2,long2)
Function that calculates the straight-line distance between two points using the haversine formula

Inputs:
- Lat1 - Latitude of point 1
- Long1 - Longitude of point 1
- Lat2 - Latitude of point 2
- Long2 - Longitude of point 2

Output: Float, distance in Km between the two points

## calculate_bounding_box(lat, lon, radius)
Function that will calculate a suitable bounding box for the map to display all the points 

Inputs:
- lat - Latitude of the point
- lon - Longitude of the points
- radius - Search Radius in Km

Outputs:  north, east, south, west coordinates for the bounding box
