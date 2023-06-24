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
    if 'result' in response_data and 'value' in response_data['result']:
        blockhash = response_data['result']['value'].get('blockhash')
        lastValidBlockHeight = response_data['result']['value'].get('lastValidBlockHeight')
        if blockhash and lastValidBlockHeight:
            return blockhash, lastValidBlockHeight
    print("Error: Unexpected API response format.")
    return None, None

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

# ADDITION: Check if a wallet address has Magic Eden NFTs
def has_magic_nfts(address):
    magic_endpoint = "https://api-mainnet.magiceden.dev/v2/wallets/{}/tokens"
    magic_response = requests.get(magic_endpoint.format(address))
    return magic_response.status_code == 200


def get_signatures_for_address(address, limit=1000):
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                address,
                {
                    "limit": limit
                }
            ]
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()

        if 'result' in response_data:
            return response_data['result']
        else:
            print(f"Error for address {address}: No 'result' key found in the response.")
            print(response_data)
            return None
    except KeyError as e:
        print(f"Error for address {address}: KeyError -", e)
        return None
    except Exception as e:
        print(f"Error for address {address}:", e)
        return None


def get_block(slot):
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlock",
            "params": [slot, {"encoding": "json", "transactionDetails": "full", "rewards": False, "maxSupportedTransactionVersion": 0}]
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        if 'result' in response_data:
            return response_data['result']
        else:
            print("Error: No 'result' key found in the response.")
            print(response_data)
            return None
    except KeyError as e:
        print("Error: KeyError -", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None

def get_latest_blockhash():
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getLatestBlockhash"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        if 'result' in response_data:
            return response_data['result']['context']['slot']
        else:
            print("Error: No 'result' key found in the response.")
            print(response_data)
            return None
    except KeyError as e:
        print("Error: KeyError -", e)
        return None
    except Exception as e:
        print("Error:", e)
        return None


script_dir = os.path.dirname(os.path.realpath(__file__))
nested_etl_dir = os.path.join(script_dir, "etlpipeline")
os.chdir(nested_etl_dir)

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
        # Check if the address has Magic Eden NFTs
        if has_magic_nfts(address):
            unique_addresses.add(address)

# Get and print signatures for each unique address
for address in unique_addresses:
    print(f"Address: {address}")
    signatures = get_signatures_for_address(address)

    if signatures:
        print("Signatures:")
        for signature in signatures:
            print(signature)
    print()

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
