import pandas as pd
import datetime
from dateutil import rrule
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re
#from fuzzywuzzy import fuzz

# Call Environment Canada API
# Returns a dataframe of data
def getHourlyData(stationID, year, month):
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
    api_endpoint = base_url + query_url
    return pd.read_csv(api_endpoint, skiprows=0)



stationID = 5097
start_date = datetime.strptime('Jan1953', '%b%Y')
end_date = datetime.strptime('Jun2019', '%b%Y')

frames = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    df = getHourlyData(stationID, dt.year, dt.month)
    frames.append(df)

weather_data = pd.concat(frames)
weather_data['Date/Time'] = pd.to_datetime(weather_data['Date/Time'])
weather_data['Temp (°C)'] = pd.to_numeric(weather_data['Temp (°C)'])

output_folder= r'climate_data/SWL'

weather_data.to_csv(rf'{output_folder}/Pearson 1953-2013.csv')
