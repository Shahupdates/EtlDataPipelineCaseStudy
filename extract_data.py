import os
import requests
import json
from pyspark.sql import SparkSession
from subprocess import run

url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

def get_latest_blockhash():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getLatestBlockhash",
        "params": [{"commitment": "processed"}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']['value']['blockhash'], response_data['result']['value']['lastValidBlockHeight']

def get_addresses_from_blockhash(blockhash):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlockCommitment",
        "params": [blockhash]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    if 'result' in response_data:
        return response_data['result']
    else:
        print(f"Error retrieving addresses from block hash {blockhash}: {response_data.get('error')}")
        return []

# Set the working directory to the main folder
os.chdir("etlpipeline")

# Create a SparkSession
spark = SparkSession.builder \
    .appName("ETL") \
    .getOrCreate()

# Get the most recent block hash
latest_blockhash, _ = get_latest_blockhash()

# Unique addresses involved in the transactions
unique_addresses = set()

# If we have a recent block hash, get the addresses
if latest_blockhash is not None:
    addresses = get_addresses_from_blockhash(latest_blockhash)
    print(f"Addresses for block hash: {latest_blockhash}")

    for address in addresses:
        unique_addresses.add(address)

# Print the unique addresses
print("Unique addresses:")
for address in unique_addresses:
    print(address)

# Run the dbt transformation
run(["dbt", "run", "--models", "transform"])

# Load the transformed data into PostgreSQL using Spark
if unique_addresses:
    df = spark.createDataFrame([(address,) for address in unique_addresses], ["address"])

    # Define PostgreSQL connection properties
    db_host = "127.0.0.2"
    db_name = "postgres"
    db_user = "postgres"
    db_password = "postgres"
    table_name = "transformed_addresses"

    # Write the DataFrame to PostgreSQL
    df.write.format("jdbc").options(
        url=f"jdbc:postgresql://{db_host}/{db_name}",
        driver="org.postgresql.Driver",
        dbtable=table_name,
        user=db_user,
        password=db_password
    ).mode("append").save()
else:
    print("No addresses available for the latest block hash.")
