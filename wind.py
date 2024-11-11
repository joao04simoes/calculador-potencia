import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def wind(date, lat, long):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    print(date.date())
    print(date)
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": ["wind_speed_10m", "wind_direction_10m"],
        "wind_speed_unit": "ms",
        "start_date": date.date(),
        "end_date": date.date()
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_wind_speed_10m = hourly.Variables(0).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(1).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_dataframe = pd.DataFrame(data=hourly_data)

    # Filter to get data only for the specified hour, e.g., 12:00 PM
    # Specify the exact hour you need in UTC format
    selected_hour = date
    hourly_dataframe["date"] = pd.to_datetime(
        hourly_dataframe["date"], utc=True)  # Ensure 'date' is in datetime format
    hourly_data_single_hour = hourly_dataframe[hourly_dataframe["date"]
                                               == selected_hour]

    date_value = hourly_data_single_hour["date"].values[0]
    wind_speed_value = hourly_data_single_hour["wind_speed_10m"].values[0]
    wind_direction_value = hourly_data_single_hour["wind_direction_10m"].values[0]

    return (wind_speed_value, wind_direction_value)
