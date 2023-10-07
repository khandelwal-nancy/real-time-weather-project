# Databricks notebook source
import requests
import json
import datetime 
from datetime import datetime
from urllib.parse import quote

# COMMAND ----------

# Azure Maps API endpoint
azure_maps_geocoding_endpoint = "https://atlas.microsoft.com/search/address/json"
azure_maps_forecast_endpoint = "https://atlas.microsoft.com/weather/forecast/hourly/json"
# Your Azure Maps Subscription Key
azure_maps_sub_key = "C_LKmgUZOgHEHy3zx_pNfp1SyBcFvU5MpedQyKcit0Q"

# City name you want to get weather data for
cities = ['London', 'Mexico', 'Sydney', 'Mumbai', 'California']
directory_path = "/mnt/raw/forecast_data/"

# CURRENT TIMESTAMP
timestamp = datetime.now().strftime("%Y%m%d_%H%M")

# COMMAND ----------

# Iterate through the list of cities
for city in cities:
    # Step 1: Geocoding to get coordinates for each city
    geocoding_params = {
        "api-version": "1.0",
        "query": city,
        "subscription-key": azure_maps_sub_key
    }

    response = requests.get(azure_maps_geocoding_endpoint, params=geocoding_params)
    geocoding_data = response.json()

    # Extract latitude and longitude from the geocoding result
    latitude = geocoding_data["results"][0]["position"]["lat"]
    longitude = geocoding_data["results"][0]["position"]["lon"]

    # Step 2: Request weather data for each city from your weather data provider
    forecast_params = {
        "api-version": "1.0",
        "query": f"{latitude},{longitude}",
        "duration": 12,
        "subscription-key": azure_maps_sub_key
    }

    forecast_response = requests.get(azure_maps_forecast_endpoint, params=forecast_params)
    forecast_data = forecast_response.json()
    
    for data in forecast_data["forecasts"]:
        forecasted_datetime = datetime.fromisoformat(data["date"])
        forecasted_datetime_str = forecasted_datetime.strftime("%Y-%m-%d_%H_%M_%S")
        data_to_load = json.dumps(data, indent=2)

        input_path= f"{directory_path}{city}/{city}_{timestamp}/forecast_data_{city}_{forecasted_datetime_str}.json"
        # Write json files to DBFS
        dbutils.fs.put(input_path, data_to_load, overwrite=True)
    print(f"Forecasting data loaded for {city}")

# COMMAND ----------

dbutils.notebook.exit("success")