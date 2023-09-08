# real-time-weather-project

## Overview

The Real-Time Weather Dashboard is a project that provides real-time weather information and forecasts for multiple cities. 
It fetches current weather data from the OpenWeatherMap API and 12-hour weather forecasts from the Azure Maps API. 
The data is processed, stored, and presented in an interactive Power BI dashboard.

## Objectives

- Collect real-time weather data for multiple cities.
- Process and store the data efficiently.
- Create an interactive Power BI dashboard to visualize the weather information.
- Automate data collection and updating of the dashboard.

## Project Components

1. **EventHubProducer Notebook**:
   - Fetches current weather data from OpenWeatherMap.
   - Sends data to the Azure Event Hub for further processing.

2. **Capture_Stream_Job1 (Azure Stream Analytics)**:
   - Captures data from the Event Hub.
   - Filters and processes data.
   - Loads data into the SQL Database.

3. **ADF Pipeline (EventHubProducer)**:
   - Triggers the EventHubProducer Notebook to run at regular intervals.

4. **ForecastDataLoad Notebook**:
   - Retrieves 12-hour weather forecasts from Azure Maps API.
   - Saves forecasts as separate JSON files for each city.

5. **ForecastDataProcessing Notebook**:
   - Processes forecast data and saves it in Databricks' "weatherforecast" table.

6. **LoadForecastToSQLServer Notebook**:
   - Loads data from the "weatherforecast" table to SQL Server's "dbo.weatherforecast" table.

7. **Power BI Dashboard**:
   - Visualizes real-time weather data and 12-hour forecasts.
   - Provides slicers to filter data by city.

## Data Flow

1. Current weather data is fetched from OpenWeatherMap API and sent to Azure Event Hub.

2. Azure Stream Analytics captures and processes the data, then loads it into SQL Database.

3. 12-hour weather forecasts are retrieved from Azure Maps API and saved as JSON files.

4. ForecastDataProcessing Notebook processes the forecast data and stores it in the "weatherforecast" table.

5. LoadForecastToSQLServer Notebook loads data into the "dbo.weatherforecast" table on SQL Server.

6. Power BI Dashboard visualizes the data, allowing users to interactively explore weather information.

## Usage

- To update weather data, the EventHubProducer Notebook runs periodically via the ADF pipeline.
- Forecast data can be refreshed using the ForecastDataLoad Notebook.
- The Power BI Dashboard provides real-time weather insights for selected cities.

## Technologies Used

- Databricks
- Azure Stream Analytics
- Azure SQL Database
- Azure Data Factory
- Power BI
- OpenWeatherMap API
- Azure Maps API

## Author

[Your Name]

## License

This project is open-source and available under the [MIT License](LICENSE).
