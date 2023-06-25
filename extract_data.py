import subprocess

import requests
import json
import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number, to_timestamp
from pyspark.sql.window import Window

url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

# Start Spark session
spark = SparkSession.builder \
    .appName("Solana ETL") \
    .config("spark.jars", "postgresql-42.6.0.jar") \
    .getOrCreate()

# PostgreSQL connection details
jdbcUrl = "jdbc:postgresql://localhost/main_database"
table = "public.transactions"
properties = {"user": "postgres", "password": "postgres", "driver": "org.postgresql.Driver"}


def get_block(slot):
    print(f"Getting block for slot: {slot}")
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlock",
            "params": [slot, {"encoding": "json", "transactionDetails": "full", "rewards": False, "maxSupportedTransactionVersion": 0}]
        }
        print(f"Sending request to: {url}")
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"Received response: {response.status_code}")
        response_data = response.json()
        print(f"Response data: {response_data}")
        transactions_list = []  # List to hold all transactions
        if 'result' in response_data:
            result = response_data['result']
            transactions = result['transactions']
            for transaction in transactions:
                message = transaction['transaction']['message']
                meta = transaction['meta']
                for i, account in enumerate(message['accountKeys']):
                    print(f"Checking Magic Eden NFTs for account {account}")
                    magic_nfts = get_magic_nfts(account)
                    print(f"Finished checking Magic Eden NFTs for account {account}")
                    if magic_nfts:
                        pre_balance = meta['preBalances'][i]
                        post_balance = meta['postBalances'][i]
                        if account in message['instructions'][0]['accounts']:
                            amount = post_balance - pre_balance  # Receiver
                        else:
                            amount = pre_balance - post_balance  # Sender
                        transaction_dict = {
                            'address': account,
                            'amount': amount,
                            'timestamp': datetime.datetime.fromtimestamp(result['blockTime']).strftime('%Y-%m-%d %H:%M:%S')
                        }
                        transactions_list.append(transaction_dict)  # Add the dictionary to the list
            return transactions_list, result.get('blockTime')
        else:
            print("Error: No 'result' key found in the response.")
            print(response_data)
            return None, None
    except KeyError as e:
        print("Error: KeyError -", e)
        return None, None
    except Exception as e:
        print("Error:", e)
        return None, None



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


def get_magic_nfts(address):
    magic_endpoint = "https://api-mainnet.magiceden.dev/v2/wallets/{}/tokens"
    magic_response = requests.get(magic_endpoint.format(address))
    if magic_response.status_code == 200:
        tokens = magic_response.json()
        if isinstance(tokens, list) and tokens:
            print(f"Magic Eden NFT(s) found for account {address}.")
            return [token.get('token') for token in tokens]
        elif isinstance(tokens, dict) and tokens.get('token'):
            print(f"Magic Eden NFT found for account {address}.")
            return [tokens.get('token')]
    return None

"""
def transform_data(data):
    print(data[:5])  # print the first 5 items
    filtered_data = [
        {
            'address': record['address'],
            'amount': record['amount'],
            'timestamp': datetime.datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S')
        }
        for record in data
        if datetime.datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S') > datetime.datetime.now() - datetime.timedelta(days=365 * 2)
    ]
    return filtered_data
"""

def load_data(data):
    df = spark.createDataFrame(data, ["address", "amount", "timestamp"])

    # Cast the timestamp column to the appropriate data type
    df = df.withColumn("timestamp", to_timestamp(col("timestamp")))

    # Deduplicate the data based on the address and timestamp columns
    window = Window.partitionBy("address", "timestamp").orderBy(col("amount").desc())
    deduplicated_df = df.withColumn("row_number", row_number().over(window)).where(col("row_number") == 1).drop("row_number")

    deduplicated_df.write.jdbc(url=jdbcUrl, table=table, mode="append", properties=properties)
    print('Data loaded successfully.')

def run_dbt_transformation():
    command = "dbt run --models +transformations.transform_data"
    subprocess.run(command, shell=True)

if __name__ == '__main__':
    print("Getting latest block...")
    latest_block = get_latest_blockhash()
    if latest_block is not None:
        print("Got latest block", latest_block)
        print("Getting transactions for block...")
        transactions, _ = get_block(latest_block)
        if transactions is not None:
            print("Got transactions", transactions)
            print("Loading data...")
            load_data(transactions)
            print("Running dbt transformation...")
            run_dbt_transformation()

    print("Stopping spark...")
    spark.stop()
