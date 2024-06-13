#SUFO_AQ

#Series of functions to aid in the retrieval of data from SUFO.

def get_sensor(site_id, start, end):
    # Function that will call the API to get data for the specified ID and time frame. Ensure that VPN is on, or connected to eduroam.

    ## Function connects to the API by creating a request from the input parameters. By default the data will load at the lowest possible frequency.
    ## The JSON is loaded and converted to a DF with all columns.
    import requests
    import pandas as pd
    from datetime import datetime

    #Add a warning for if the date is too long
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    if (end_dt - start_dt).days > 35:
        raise ValueError("Large timeframe, ensure you are requesting no more than one month")

    #Create the URL
    url = "https://ufdev21.shef.ac.uk/sufobin/sufoDXT?Tfrom=" + start + "&Tto=" + end +"&bySite=" + site_id + "&freqInMin=1&qcopt=prunedata&udfnoval=-32768&udfbelow=-32769&udfabove=-32767&hrtFormat=iso8601&tabCont=rich&gdata=byPairId&src=data&op=getdata&fmt=jsonrows&output=zip&tok=generic&spatial=none"
    
    #Query the website
    response = requests.get(url)
    response.raise_for_status() 

    #If there is no data, then the request responds with a HTML, so .json() will fail, use try:except to catch this
    try:
        response = requests.get(url)
        response.raise_for_status()  #error if issue
        request_data = response.json()

        #Now parse the JSON and convert to DF
        #Take the data from the nested element
        #Check the number of bundles 
        if request_data["nBundles"] != 1:
            raise ValueError("More than one sensor in data")
        
        json_data = request_data["bundles"][0]["dataByRow"]

        #convert into a temporary df
        json_df = pd.DataFrame(json_data)
        # Modify column names to remove anything before the first "."
        json_df.columns = json_df.columns.str.split('.').str[1]

        return json_df
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except ValueError:  #ValueError will occur for JSON parse failure
        print("No data for specified parameters")
        return None
    

def parse_sensor(site_id,date_start, date_end,time_col,pollutant,path, moving_avg = 0):
    #Function that accesses the data and saves a pickled pandas DF with the data. 

    ## This function takes two elements from the dates list (one start, one end) and loops through the list. Data is retrieved using
    ## Get sensor, then parsed to only include the desired column and timestamp. Data is then pickled to the specified folder
    ## where it can be read into different scripts.
    ## Moving average is an optional parameter, the defualt value is 0 and no column will be added, anything above will give you data
    import datetime
    import SUFO_AQ
    import pandas as pd

    start_dt = datetime.datetime.fromisoformat(date_start)
    end_dt = datetime.datetime.fromisoformat(date_end)

    n_days = (end_dt - start_dt).days

    #If less than 35, we don't need the dict and the function can just pickle straight away
    if n_days <= 35:
        df = SUFO_AQ.get_sensor(site_id,date_start,date_end)
        if df is None:
            return None

        ##Check the target columns exist
        if (time_col not in df.columns):
            raise KeyError(f"Column {time_col} not found in data")

        if (pollutant not in df.columns):
            raise KeyError(f"Column {pollutant} not found in data")
        
        #Add ISO time, converting the UNIX column specified
        df['ISO_time'] = df[time_col].apply(lambda x: datetime.datetime.utcfromtimestamp(x).isoformat())

        #Convert target column to numeric
        df[pollutant] = df[pollutant].astype('float64')

        #If the option is selected, add a column with the moving average
        if moving_avg > 0:
            ma_col = pollutant + ".MA." + str(moving_avg)
            df[ma_col] = df[pollutant].rolling(window = moving_avg).mean()
            all_data_df= df[[time_col, "ISO_time",pollutant,ma_col]]
        else:
            all_data_df= df[[time_col, "ISO_time",pollutant]]
    else:
        # Create a list to store the entire months
        dates_list = []
        
        # Start with the initial month
        current_date = start_dt.replace(day=1)  # Start from the 1st day of the month

        while current_date <= end_dt:
            # Add the current month to the list
            dates_list.append(current_date.strftime("%Y-%m-%dT%H:%M:%S"))

            # Move to the next month
            current_date += datetime.timedelta(days=30)  # Add 30 days (approximately one month)

            # Ensure we're still within bounds of the end
            if current_date.month > end_dt.month and current_date.year >= end_dt.year:
                current_date = end_dt 
        
        #Create empty dict to store output
        all_data_dict = {}

        for x in range(len(dates_list) - 1):
            #Get the sensor data
            df = SUFO_AQ.get_sensor(site_id,dates_list[x],dates_list[x+1])

            ##Check the target columns exist
            if (time_col not in df.columns):
                raise KeyError(f"Column {time_col} not found in data")

            if (pollutant not in df.columns):
                raise KeyError(f"Column {pollutant} not found in data")
            
            #Add ISO time, converting the UNIX column specified
            df['ISO_time'] = df[time_col].apply(lambda x: datetime.datetime.utcfromtimestamp(x).isoformat())

            #Convert target column to numeric
            df[pollutant] = df[pollutant].astype('float64')

            # Take just the two columns and store in a dictionary
            df_name = dates_list[x].split("T")[0]

            #If the option is selected, add a column with the moving average
            if moving_avg > 0:
                ma_col = pollutant + ".MA." + str(moving_avg)
                df[ma_col] = df[pollutant].rolling(window = moving_avg).mean()
                all_data_dict[df_name] = df[[time_col, "ISO_time",pollutant,ma_col]]
            else:
                all_data_dict[df_name] = df[[time_col, "ISO_time",pollutant]]

        #Now we'll output a DF with them concetenated
        frames = [all_data_dict[key] for key in list(all_data_dict.keys())]
        all_data_df = pd.concat(frames)

    #Finally pickle
    fname = site_id + "_" + date_start[:10].replace('-', '_')
    all_data_df.to_pickle(path + fname)
