# Databricks notebook source
import os
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType
from pyspark.sql.functions import concat, col, from_json, input_file_name, regexp_extract, to_timestamp

# COMMAND ----------

source_base_path = "/mnt/raw/forecast_data/"
archive_base_path = "/mnt/raw/archive_forecast_data/"
json_path = "/mnt/raw/forecast_data/*/*/*.json"

schema_name = "processedforecast"
table_name = "weatherforecast"
cities = ['London', 'Mexico', 'Sydney', 'Mumbai', 'California']

# COMMAND ----------

# Define schema for JSON data
jsonSchema = StructType([StructField("temperature", 
StructType([StructField("value", DoubleType(), True)]), True),
StructField("visibility", StructType([StructField("value", DoubleType(), True)]), True),
StructField("uvIndex", IntegerType(), True),
StructField("uvIndexPhrase", StringType(), True),
StructField("relativeHumidity", IntegerType(), True),
StructField("iconCode", StringType(), True),
StructField("iconPhrase", StringType(), True),
StructField("date", TimestampType(), True)
])

# COMMAND ----------

# Load the JSON files and apply the schema
json_df = spark.read.option("multiLine", True).json(json_path,schema=jsonSchema).withColumn("TempInCelcius", col("temperature.value")).withColumn("VisibilityInKm", col("visibility.value")).withColumn("city", regexp_extract(input_file_name(), r"forecast_data_(\w+)_(.*?)\.json", 1))

# COMMAND ----------

# Select the desired columns 
parsed_df= json_df.select("TempInCelcius", "relativeHumidity", "VisibilityInKm", "uvIndex", "uvIndexPhrase", "iconCode", "date", "city").distinct()

# COMMAND ----------

# Write your DataFrame into a temporary table
parsed_df.createOrReplaceTempView("temp_weather_forecast")

# COMMAND ----------

# Load the data from temporary table to forecast weather table
spark.sql("INSERT OVERWRITE TABLE processedforecast.weatherforecast PARTITION (`date`) SELECT * from temp_weather_forecast")

# COMMAND ----------

# Archiving the processed files
for city in cities:
    # file_paths = dbutils.fs.ls(f'{folder_path}{city}/')
    source_path = f"{source_base_path}{city}/"
    archive_path = f"{archive_base_path}{city}/"
    
    # Use dbutils.fs.ls to list files in the source directory for the city
    source_files = dbutils.fs.ls(source_path)
    for source_file in source_files:
        file_name = os.path.basename(source_file.path)
        archive_file = f"{archive_path}{file_name}"
        dbutils.fs.mv(source_file.path, archive_file, recurse=True)

# COMMAND ----------

dbutils.notebook.exit("success")