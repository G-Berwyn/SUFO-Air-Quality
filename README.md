# SUFO Air Quality
 Repo for Python tools developed to read Air Quality data from the Sheffield Urban Flows Observatory

These tools were developed for my MSc Data Science dissertation. They are designed to faciliate the reading and formatting data from the *Sheffield Urban Flows Observatory (SUFO)*. 

## Table of Contents
- [Functionality and Pre-requisites](#Functionality-and-Pre-requisites)
- [Features](#Features)
- [Example Usage](#Example-Usage)
- [Authors](#Authors)

## Functionality and Pre-requisites

Requires Python 3 or later. Key modules required are:
- **Pandas** - for manipulating data
- **Requests** - connecting to API
- **datetime** - handling UNIX and ISO timestamps

To access the SUFO data extraction tool (DXT) you will also either need a VPN or be on University Eduroam.

Currently there are two key functions. One to retrieve the data from a specific sensor as a DataFrame, and another to return data for a specific sensor over a defined period as a single DF.

### **get_sensor** 
Function that will call the SUFO DXT API to get data for the specified Site ID and time frame.
Inputs:
-  Site_id - the site location ID, for example  S0110.
-  Start - the specified start time in ISO format, e.g. "2023-07-01T01:0:00"
-  End - the specified end time in ISO format

Output: DF containing data for the specified parameters

### **parse_sensor***
Function that will provide data in a pickled Pandas DF with the time and chosen pollutant
Input:
- Site_id - the site location ID, for example  S0110.
- Date_start - the first date of interest in ISO format, e.g. "2023-07-01T01:0:00"
- Date_end - the end date in ISO format, e.g. "2023-07-01T01:0:00"
- pollutant - the pollutant of interest, e.g. PM25
- moving_avg - optional argument, if set > 0 will append a column with the moving average for the pollutant.

## Features

## Example Usage

## Authors
SUFO data extraction tools developed by the *Sheffield Urban Flows Obervatory*
Repo developed by [G-Berwyn](https://github.com/G-Berwyn)]
