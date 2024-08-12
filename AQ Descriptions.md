# SUFO Air Quality

Below is a description of all the functions included in the SUFO AQ package and how they should be used. The key functions are **get_sensor** and **parse_sensor**

# Included Functions
- get_sensor
- parse_sensor
- qual_calc
- sites_qual_eval
- calculate_aq_diff

## get_sensor(site_id, start,end)
Function that will take the specified start and end times, query data for that site and return a Pandas DF with the data.
Limited to one month of data due to SUFO restrictions.

Inputs:
- site_id - String of the site ID, for example "S0110" or "UKA00575"
- start - String with the start data in ISO format
- end - String with the end date in ISO format
 
Output: Dataframe with data by row from SUFO

Example Usage:

```python
import SUFO_AQ
import pandas as pd

SUFO_AQ.get_sensor("S0110","2022-10-13T14:50:40", "2022-11-10T17:50:40")

```

## parse_sensor(site_id, date_start, date_end, time_col, pollutant, path, moving_average = 0, file_type = "pkl")
Function that will get data for a large time period for a given site. The function will get data for the specified pollutant and save a pickle on the specified path

Inputs:
- site_id - String of the site ID, for example "S0110" or "UKA00575"
- date_start - String with the start data in ISO format
- date_end - String with the end date in ISO format
- time_col - String with the name of the time column, usually "time"
- pollutant - String with your pollutant of interest, e.g "NO2"
- path = String with the filepath to save your pickles
- moving_average - Int, by default 0 but can include, recommended to re-sample data later using daily or hourly.
- file_type - The type of file you want to save, by default this is a pickle (pkl) but can also be "csv". No other are currently supported.

Output: A Pandas pickle saved to the specified path. Can be read back into Python.

For reading pickles into R, see this [Stack Overflow post](https://stackoverflow.com/questions/35121192/reading-a-pickle-file-pandas-python-data-frame-in-r)

Example usage:

```python
import SUFO_AQ
import pandas as pd

SUFO_AQ.parse_sensor("S0110","2022-10-13T14:50:40", "2022-11-10T17:50:40","time","PM25","G:/My Drive/03 Semester 3/SUFO Data/Pickles/")
pd.read_pickle("G:/My Drive/03 Semester 3/SUFO Data/Pickles/S0110_20221013_20221110_PM25")

```

The following functions will likely not be required but are included for compeleteness:

## qual_calc(site_id,date_start,date_end,pollutant,path)
Function that will calculate the number of missing values, eraliest date and latest date for a particular site

Inputs:
- site_id - String of the site ID, for example "S0110" or "UKA00575"
- date_start - String with the start data in ISO format
- date_end - String with the end date in ISO format
- pollutant - String with your pollutant of interest, e.g "NO2"
- path = String with the filepath to where your pickles have been saved

The function will load the pickle for the specified site, dates and pollutant before calculating the quality metrics

Output: List with the number of missing values, earliest data point and latest data point

## sites_qual_eval(sites_list, start_date, end_date, pollutant, path)
Function that will iterate through a list of sites and call qual_calc to calcualte the data quality for each, will return a DF with the metrics

Inputs:
- sites_lsit - List with the desired sites
- start_date - String with the start data in ISO format
- end_date - String with the end date in ISO format
- pollutant - String with your pollutant of interest, e.g "NO2"
- path = String with the filepath to where your pickles have been saved

Output: DF with the each site in its own row, and columns for the number of missing values, earliest data point and latest data point



