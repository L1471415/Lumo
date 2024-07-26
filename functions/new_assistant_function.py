''' Module containg functions that Lumo is able to call in conversation with a user'''

from datetime import datetime
import calendar

import requests

import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

import wikipedia

from config.config_variables import api_credentials, measurement_units

geocoder = Nominatim(user_agent="lumo_voice_assistant")
tf = TimezoneFinder()


def get_time(location:str) -> dict:
    '''Method to find the time at a given location

        Parameters:
            location (str): The name of the location to find the time at

        Returns:
            Dict: {
                "location": geolocated_location_address
                "datetime": formatted_timestamp
            }
    '''

    if not location:
        location = "Troy NY"

    geolocated_location = geocoder.geocode(location)

    if not geolocated_location:
        return {"time_request_error": f"Location {location} was not found. Try a different location"}

    timezone = pytz.timezone(tf.timezone_at(lat=geolocated_location.latitude, lng=geolocated_location.longitude))

    current_time_at_location = datetime.now(timezone)

    formatted_timestamp = current_time_at_location.strftime("%a %Y-%m-%d %H:%M:%S")

    return {
        "location": geolocated_location.address,
        "datetime": formatted_timestamp
    }


def get_weather(location:str = None) -> dict:
    '''Method to find the weather forecast at a given location

        Parameters:
            location (str): The name of the location to find the forecast for

        Returns:
            Dict: {
                "location": geolocated_location_address
                "daily": Dict containing the weather forcast over the next week (by day)
                    Dict contains: "temp", "high", "low", "weather"
                "hourly": Dict containing the weather forecast over the next 12 hours (by hour)
                    Dict contains: "temp", "weather", "precipitation_chance"
            }
    '''
    if not location:
        location = 'Troy NY'

    geolocated_location = geocoder.geocode(location)

    weather_forecast = _get_forecast_by_coordinates(geolocated_location.latitude, geolocated_location.longitude)

    weather_forecast["location"] = geolocated_location.address

    return weather_forecast


def _get_forecast_by_coordinates(latitude:float, longitude:float) -> dict:
    '''Helper function to get the weather forecast at a location specified by latitude and longitude

        Parameters:
            latitude (float): The latitude of the location
            longitude (float): the longitude of the location

        Returns:
            Dict: {
                "daily": Dict containing the weather forcast over the next week (by day)
                    Dict contains: "temp", "high", "low", "weather"
                "hourly": Dict containing the weather forecast over the next 12 hours (by hour)
                    Dict contains: "temp", "weather", "precipitation_chance"
            }
    '''
    response = requests.get(
        (
            "https://api.openweathermap.org/data/3.0/onecall?"
            f"lat={latitude}"
            f"&lon={longitude}"
            f"&appid={api_credentials['openweathermap']['appid']}"
            f"&units={measurement_units}"
            "&exclude=minutely,alerts"
        ), timeout=5
    )

    if not response.ok:
        return {"weather_request_error": "Response failed. Please try again at a later time."}

    response_json = response.json()

    daily_forecast = {}

    current_day_of_week = datetime.now().weekday()

    for day in range(0, 8):
        day_string = calendar.day_name[(day + current_day_of_week) % 7]
        if day == 0:
            day_string = "Today"

        cur_day_weather = response_json['daily'][day]

        daily_forecast[day_string] = {
            "temp": cur_day_weather['temp']['day'],  # Get the average temp for the day
            "high": cur_day_weather['temp']['max'],
            "low": cur_day_weather['temp']['min'],
            "weather": cur_day_weather['summary']
        }

    hourly_forecast = {}

    current_hour = datetime.now().hour

    for hour in range(0, 12):
        hour_string = f"{current_hour + hour}00"

        cur_hour_weather = response_json['hourly'][hour]

        hourly_forecast[hour_string] = {
            "temp": cur_hour_weather['temp'],
            "weather": cur_hour_weather['weather'][0]['description'],
            "precipitation_chance": cur_hour_weather['pop']
        }

    return {
        "daily": daily_forecast,
        "hourly": hourly_forecast
    }


def search_wikipedia(query:str):
    '''Function to search wikipedia for a given query

        Parameters:
            query (str): What to search wikipedia for
    '''

    possible_page = wikipedia.search(query, results=1)

    if len(possible_page) < 1:
        return {
            "wikipedia_search_error": f"No pages matching query {query} found!"
        }

    page_name = possible_page[0]
    page_summary = wikipedia.summary(page_name)

    return {
        "page": page_name,
        "summary": page_summary
    }


if __name__ == "__main__":
    while True:
        print(get_weather(input("Location: ")))
