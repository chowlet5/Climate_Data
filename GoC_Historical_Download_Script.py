import pandas as pd
from dateutil import rrule
from datetime import datetime


#List of column names to keep when exporting data to csv
columnKeep = ['Date/Time','Wind Dir (10s deg)','Wind Dir Flag','Wind Spd (km/h)','Wind Spd Flag']

#Create a dictionary which holds all of the station ID + start/end dates to perform multiple download cycles
# Format key = station_ID. value = [station_name, start_date, end_date]
downloadList = {50093: ['London A','Mar2012','Aug2020'],
                4789: ['London Intl Airport','Jan2010','Mar2012'],
                53678: ['Toronto Buttonville A','May2015','Jan2019']}


# function that eturns a dataframe of climate data
def getHourlyData(stationID, year, month):
    #The base URL is from the"README" provide by ENVIRONMENT AND CLIMATE CHANGE CANADA
    # "README" Document: https://drive.google.com/drive/folders/1WJCDEU34c60IfOnG4rv5EPZ4IhhW9vZH
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    # The query URL from the"README" provide by ENVIRONMENT AND CLIMATE CHANGE CANADA
    # timeframe=1 is for hourly data,  timeframe=2 is for daily data and, timeframe=3 is for monthly data
    #We format the query string to add our request
    query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
    # Combine the base_url and query_url
    api_endpoint = base_url + query_url
    # pandas "read_csv" can use a url as a filepath. 
    return pd.read_csv(api_endpoint)

for key in downloadList.keys():
    stationID = key
    start_date = datetime.strptime(downloadList[key][1], '%b%Y')
    end_date = datetime.strptime(downloadList[key][2], '%b%Y')
    #Create an empty list
    frames = []
    #rrule.rrule creates a recurrence rule, basically a list of months and year. 
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        #We use the function we created earlier to get our data for the current month and year
        df = getHourlyData(stationID, dt.year, dt.month)
        #add the dataframe to the list
        frames.append(df[columnKeep])
    #combine all of the individual dataframes into a single dataframe
    weather_data = pd.concat(frames)
    #change the Date/Time column to use a datetime format
    weather_data['Date/Time'] = pd.to_datetime(weather_data['Date/Time'])
    
    #Get station name from dictionary
    stationName = downloadList[key][0]
    
    #Change start/end date to be string using format: Month_Abbreviated Year
    start_date = start_date.strftime('%b%Y')
    end_date = end_date.strftime('%b%Y')
    
    #Save the climate data as a csv file
    weather_data.to_csv(f'{stationName}_{start_date}_{end_date}.csv')