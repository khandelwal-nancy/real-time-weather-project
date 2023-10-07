# Databricks notebook source
table_name = "weatherforecast"
schema_name = "processedforecast"
sql_server_table_name = "dbo.weatherforecast"

# COMMAND ----------

jdbc_url = "jdbc:sqlserver://dev-server001.database.windows.net:1433;database=dev-adw"
connection_properties = {
    "user": "devadmin",
    "password": "Nancy@2023",
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# COMMAND ----------

# Read data from weatherforecast table intoa Dataframe
df = spark.read.table(f'{schema_name}.{table_name}')

# COMMAND ----------

# Load table in SQL Server
df.write.jdbc(url=jdbc_url, table=sql_server_table_name, mode="overwrite", properties=connection_properties)

# COMMAND ----------

dbutils.notebook.exit("success")