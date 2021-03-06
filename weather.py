#Packages for weather API 
import requests
import json
import pandas as pd
from requests import api

'''
Function returns a DataFrame of 5 day weather forecast
of the city provided in argument
@param: cityName
'''
#Function to retrieve weather data
def fetchWeather(cityName):
    #API key for openweathermap
    api_key = '411d19dc84c08c5a4c9d6e3ca8dc6951'
    url = 'https://api.openweathermap.org/data/2.5/forecast?q=%s&appid=%s' % (cityName, api_key) 
    response = requests.get(url).text
    response_json = json.loads(response)
    if response_json['cod'] == '404':
        return pd.DataFrame()
    #Retrieving relevant data from the JSON response
    weather_list = []
    columns = ['Date', 'Temperature', 'Feels Like', 'Min Temperature', 'Max Temperature', 'Description', 'Weather']
    for day in response_json['list']:
        weather_list.append([day['dt_txt'], day['main']['temp'], day['main']['feels_like'], day['main']['temp_min'], day['main']['temp_max'], day['weather'][0]['description'], day['weather'][0]['main']])
    temps = ['Temperature', 'Feels Like', 'Min Temperature', 'Max Temperature']
    weather_df = pd.DataFrame(data = weather_list, columns=columns)
    for col in temps:
        #Conversion to Farhenheit
        weather_df[col] = 1.8*(weather_df[col] - 273) + 32
    #Extracting date from datetime column 
    weather_df['date_column'] = pd.to_datetime(weather_df['Date']).dt.date
    #Aggregate the resulting df to retrieve max, min, average conditions for the day along with the most common weather description 
    result=weather_df.groupby('date_column').agg({'Max Temperature':'max','Min Temperature':'min','Temperature':'mean','Description':lambda x: pd.Series.mode(x).iat[0]})
    result.reset_index(level=0, inplace=True)
    return result
'''
Function returns the weather mode
of the dataframe provided in argument based on the description column
@param: fetchWeather dataframe (df)
'''
#Check the most common weather mode for the day
def weather_mode(df):
    a= df['Description'].mode()[0]
    if 'cloud' in a.lower():
        return "clouds"
    elif 'rain' in a.lower():
        return "rain"
    elif 'sun' in a.lower():
        return "sunny"
    elif 'snow' in a.lower():
        return "snow"
    else:
        return "default"   
    
