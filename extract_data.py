import requests
import json
import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number
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
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlock",
            "params": [slot, {"encoding": "json", "transactionDetails": "full", "rewards": False, "maxSupportedTransactionVersion": 0}]
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        transactions_list = []  # List to hold all transactions
        if 'result' in response_data:
            # Including the blockTime in the returned result
            result = response_data['result']
            transactions = result['transactions']
            for transaction in transactions:
                message = transaction['transaction']['message']
                meta = transaction['meta']
                for i, account in enumerate(message['accountKeys']):
                    # Calculate amount based on whether account is a sender or a receiver
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
        if isinstance(tokens, list):
            return [token.get('token') for token in tokens]
        elif isinstance(tokens, dict):
            return [tokens.get('token')]
    return None

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


def load_data(data):
    df = spark.createDataFrame(data, ["address", "amount", "timestamp"])

    # Remove duplicates based on the address and timestamp columns
    deduplicated_df = df.dropDuplicates(["address", "timestamp"])

    deduplicated_df.write.jdbc(url=jdbcUrl, table=table, mode="append", properties=properties)
    print('Data loaded successfully.')


if __name__ == '__main__':
    latest_block = get_latest_blockhash()
    if latest_block is not None:
        transactions, _ = get_block(latest_block)
        if transactions is not None:
            data = transform_data(transactions)
            load_data(data)

    spark.stop()
