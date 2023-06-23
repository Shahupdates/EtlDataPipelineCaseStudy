from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from datetime import datetime, timedelta

# Start a SparkSession
spark = SparkSession.builder.appName('solana').getOrCreate()

# Assume the data is a list of dictionaries
data = fetch_solana_data('node_address')

# Create a DataFrame
df = spark.createDataFrame(data)

# Business rules: Magic Eden contracts & not older than 2 years
df_transformed = df.filter(
    (col('contract') == 'Magic Eden') &
    (col('timestamp') > datetime.now() - timedelta(days=2*365))
)

df_transformed.write.format('jdbc').options(
      url='jdbc:postgresql://localhost:5432/your_database',
      driver='org.postgresql.Driver',
      dbtable='your_table',
      user='your_username',
      password='your_password').mode('append').save()
