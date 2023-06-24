import requests
import json
import psycopg2
import datetime

url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

# PostgreSQL connection details
conn = psycopg2.connect(
    host='127.0.0.1',
    port='5432',
    database='main_database',
    user='postgres',
    password='postgres'
)
cursor = conn.cursor()


def get_block(slot):
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlock",
            "params": [slot, {"encoding": "json", "transactionDetails": "full", "rewards": False,
                             "maxSupportedTransactionVersion": 0}]
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()
        if 'result' in response_data:
            # Including the blockTime in the returned result
            return response_data['result'], response_data['result'].get('blockTime')
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
    filtered_data = [
        record for record in data if datetime.datetime.fromtimestamp(int(record['timestamp'])) >
                                   datetime.datetime.now() - datetime.timedelta(days=365 * 2)
    ]
    return filtered_data


def load_data(data):
    # Assuming you have a table named 'transactions' with appropriate columns in your PostgreSQL database
    insert_query = "INSERT INTO public.transactions (address, timestamp, amount) VALUES (%s, %s, %s)"

    # Iterate through the transformed data and execute the insert query for each record
    for record in data:
        cursor.execute(insert_query, (record['address'], record['timestamp'], record['amount']))

    # Commit the changes and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()


# Get the most recent block hash
latest_blockhash = get_latest_blockhash()

# Unique addresses involved in the transactions
unique_addresses = set()

# If we have a recent block hash, get its details
if latest_blockhash is not None:
    block_data = get_block(latest_blockhash)
    if block_data is not None:
        # Loop through each transaction in the block and get the addresses involved in the transaction
        addresses = [address for transaction in block_data['transactions'] for address in
                     transaction['transaction']['message']['accountKeys']]

        # Process only a subset of addresses to avoid rate limits
        addresses = addresses[:50]  # adjust this number based on your needs

        for address in addresses:
            magic_nfts = get_magic_nfts(address)
            if magic_nfts is not None:
                unique_addresses.add(address)

# Get the unique addresses
unique_addresses = list(unique_addresses)

# Transform the data
transformed_data = transform_data(unique_addresses)

# Load the transformed data into PostgreSQL
load_data(transformed_data)

# Print unique addresses
for address in unique_addresses:
    print(address)
