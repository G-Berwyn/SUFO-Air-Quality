# SUFO Air Quality
This is a repo for Python tools developed to read Air Quality data and Traffic information from the Sheffield Urban Flows Observatory

These tools were developed for my MSc Data Science dissertation. They are designed to faciliate the reading and formatting data from the *Sheffield Urban Flows Observatory (SUFO)*. Currently the only paramters than can be varied are the site location, the dates, and which pollutant you want. QC values at -30000 are removed from the data.

*get_sensor()* retreives data for a specific site over a time period. This is limited to a month maximum.

*parse_sensor* will take a sensor, a larger date range and path to return a pickled (stored) pandas DF. Use this for for larger date ranges, or simply to create a stored variable.

## Table of Contents
- [Installing](#Installing)
- [Functionality and Pre-requisites](#Functionality-and-Pre-requisites)
- [Features](#Features)
- [Example Usage](#Example-Usage)
- [Authors](#Authors)
  
## Installing
To install, copy the contents of the **SUFO_AQ.py** file to your IDE of choice, and save in a place that the current workspace can access. The module can then be imported into scripts.

## Functionality and Pre-requisites

Requires Python 3 or later. Key modules required are:
- **Pandas** - for manipulating data
- **Requests** - connecting to API
- **datetime** - handling UNIX and ISO timestamps

SUFO_Traffic tools to plot sites will also require
- **osmnx** - Downloading map data
- **geopandas** - Plotting maps
- **shapely** - Annotating maps

To access the SUFO data extraction tool (DXT) you will also need the University of Sheffield VPN.

There are a number of functions, the key functions are described below with further descriptions in their own documents.
- [SUFO Air Quality](AQ Descriptions.md)

### **parse_sensor(site_id,date_start, date_end,pollutant,path)**
Function that will provide data in a pickled Pandas DF with the time and chosen pollutant. This will retrieve data for the specified time period and save data to a pickle on the path
Input:
- Site_id - the site location ID, for example  S0110.
- Date_start - the first date of interest in ISO format, e.g. "2023-07-01T01:0:00"
- Date_end - the end date in ISO format, e.g. "2023-07-01T01:0:00
- pollutant - the pollutant of interest, e.g. PM25
- Path - destination for the pickled DF.

Output: Pickled DF saved to the described path

There is no need to specify the entire column name, for example time rather than data.time


## Features

## Example Usage

The below example will read for sensor S0110 between the specified dates for PM25 and save the file to the specified path on my device.

```python
import SUFO_AQ
import pandas as pd

#
SUFO_AQ.parse_sensor("S0110","2022-10-13T14:50:40", "2022-11-10T17:50:40","time","PM25","G:/My Drive/03 Semester 3/SUFO Data/Pickles/")
pd.read_pickle("G:/My Drive/03 Semester 3/SUFO Data/Pickles/S0110_20221013_20221110_PM25")

```
Depending on your time range and chosen site, it may take a few minutes for the sensor to collect all data.

## Authors
SUFO data extraction tools developed by the *Sheffield Urban Flows Obervatory*.

Repo developed by [G-Berwyn](https://github.com/G-Berwyn)
