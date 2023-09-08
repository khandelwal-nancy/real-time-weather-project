# Databricks notebook source
configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": "61cc0cef-c0cf-413e-99e2-c2df6ffd71d4",
          "fs.azure.account.oauth2.client.secret": "v.a8Q~ZW0q01RwHuCruVL7SLU_23gohqGV5Q-atT",
          "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/89703b51-ec69-4525-bc8d-bfeb3b10756e/oauth2/token"}


# COMMAND ----------

# MAGIC %md
# MAGIC Mount raw container

# COMMAND ----------

dbutils.fs.mount(
  source = "abfss://raw@devadlsstorage01.dfs.core.windows.net/",
  mount_point = "/mnt/raw/",
  extra_configs = configs)

# COMMAND ----------

# MAGIC %md
# MAGIC Mount processed container

# COMMAND ----------

dbutils.fs.mount(
  source = "abfss://processed@devadlsstorage01.dfs.core.windows.net/",
  mount_point = "/mnt/processed/",
  extra_configs = configs)