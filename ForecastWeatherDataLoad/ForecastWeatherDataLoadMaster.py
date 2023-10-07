# Databricks notebook source
# Master Notebook - Forecast Data Processing

try:
    # 1. Load Forecast Data
    dbutils.notebook.run("./ForecastDataLoad", 3600)

    # 2. Process Forecast Data
    dbutils.notebook.run("./ForecastDataProcessing", 3600)

    # 3. Load Processed Forecast Data to SQL Server
    dbutils.notebook.run("./LoadForecastToSQLServer", 3600)
                         
except Exception as e:
    # If an exception occurs, exit the notebook with an error message
    dbutils.notebook.exit(f"Notebook didn't run successfully: {str(e)}")

# All notebooks have run successfully
dbutils.notebook.exit("success")
