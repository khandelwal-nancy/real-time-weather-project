# Databricks notebook source
# pip install azure.eventhub

# COMMAND ----------

# Import required libraries
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
from datetime import datetime, timezone, timedelta
import json
import requests
import asyncio
import nest_asyncio

# COMMAND ----------

nest_asyncio.apply()

# COMMAND ----------

# Replace with your Event Hubs connection string and Event Hub name
connection_string = "Endpoint=sb://az-eventhub-01.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=qFHQ3j8LP3HPH5B2y1sYqL8haEs+CG3bR+AEhJoQjws="
event_hub_name = "weatherdata-eventhub"
api_endpoint = 'https://api.openweathermap.org/data/2.5/weather'
api_key = '1f1f54c1fc3974302388025f706c2102'
cities = ['London', 'Mexico', 'Sydney', 'Mumbai', 'California']

# COMMAND ----------

def fetch_weather_data(city):
    api_url = f'{api_endpoint}?q={city}&appid={api_key}&units=metric'
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch weather data for {city}. Error: {response.status_code}")
        return None

# COMMAND ----------

async def send_data_to_eventhu(cities, connection_string, event_hub_name):
    producer_client = EventHubProducerClient.from_connection_string(connection_string, eventhub_name=event_hub_name)
    try:
        # Fetch weather data for multiple cities synchronously
        weather_data = [fetch_weather_data(city) for city in cities]
        async with producer_client:
            data_batch =await producer_client.create_batch()
            for data in weather_data:
                # Filter the desired keys from the weather_data dictionary
                # filter_data = {key:data[key] for key in keys_to_include if key in data}
                # print(data["dt"], data["timezone"])
                data["dt"] = (datetime.fromtimestamp(data["dt"], tz=timezone.utc) + timedelta(seconds=data["timezone"])).strftime("%Y-%m-%d %H:%M:%S")
                # print(data["dt"])
                data_batch.add(EventData(json.dumps(data)))
                print("added data for", data["name"])
            await producer_client.send_batch(data_batch)
        print("Data sent successfully!")

    except Exception as e:
        print("Error sending data:", str(e))

    finally:
        # Close the producer client
        await producer_client.close()


# COMMAND ----------

loop = asyncio.get_event_loop()
loop.run_until_complete(send_data_to_eventhu(cities, connection_string, event_hub_name))
# asyncio.run(send_data_to_eventhu(cities, connection_string, event_hub_name))

# COMMAND ----------

# from azure.eventhub import EventHubConsumerClient

# # Function to process received events
# def on_event(partition_context, event):
#     print("Received event from partition: {}".format(partition_context.partition_id))
#     print("Event data: {}".format(event.body_as_str()))

# # Create a consumer client
# consumer_client = EventHubConsumerClient.from_connection_string(connection_string, consumer_group="$Default", eventhub_name=event_hub_name)

# # Start receiving events from all partitions
# with consumer_client:
#     consumer_client.receive(on_event=on_event, starting_position="-1")
