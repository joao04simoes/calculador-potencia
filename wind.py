import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def wind(date, roundedlist):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # URL for the Open-Meteo API
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"

    # Dictionary to hold dataframes for each location
    location_dataframes = {}

    # Loop over each unique location in roundedlist
    for lat, long in roundedlist:
        params = {
            "latitude": lat,
            "longitude": long,
            "minutely_15": ["wind_speed_10m", "wind_direction_10m"],
            "wind_speed_unit": "ms",
            "start_date": date.date(),
            "end_date": date.date()
        }

        # Make the API request
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Process the data for minutely_15 (interval data)
        minutely_15 = response.Minutely15()
        minutely_15_wind_speed_10m = minutely_15.Variables(0).ValuesAsNumpy()
        minutely_15_wind_direction_10m = minutely_15.Variables(
            1).ValuesAsNumpy()

        # Create a DataFrame for the current location
        minutely_15_data = {
            "date": pd.date_range(
                start=pd.to_datetime(minutely_15.Time(), unit="s", utc=True),
                end=pd.to_datetime(minutely_15.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=minutely_15.Interval()),
                inclusive="left"
            ),
            "wind_speed_10m": minutely_15_wind_speed_10m,
            "wind_direction_10m": minutely_15_wind_direction_10m
        }
        minutely_15_dataframe = pd.DataFrame(data=minutely_15_data)

        # Add the DataFrame to the dictionary with coordinates as the key
        location_dataframes[(lat, long)] = minutely_15_dataframe

    return location_dataframes


def WindSpeedAndDir(dataPoint, i, location_dataframes):
    timestamp = pd.Timestamp(dataPoint[i].time,)
    rounded_timestamp = timestamp - \
        pd.Timedelta(minutes=timestamp.minute %
                     15, seconds=timestamp.second, microseconds=timestamp.microsecond)

    selected_hour = rounded_timestamp
    minutely_15_dataframe = location_dataframes[(
        round(dataPoint[i].lat, 2)), (round(dataPoint[i].long, 2))]
    minutely_15_dataframe["date"] = pd.to_datetime(
        minutely_15_dataframe["date"], utc=True)  # Ensure 'date' is in datetime format
    minutely_15_data_single_hour = minutely_15_dataframe[minutely_15_dataframe["date"]
                                                         == selected_hour]

    # date_value = minutely_15_data_single_hour["date"].values[0]
    wind_speed_value = minutely_15_data_single_hour["wind_speed_10m"].values[0]
    wind_direction_value = minutely_15_data_single_hour["wind_direction_10m"].values[0]
    return (wind_direction_value, wind_speed_value)
