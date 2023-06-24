import time
import requests
import json
import psycopg2
from datetime import datetime, timedelta
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder \
    .appName("ETL") \
    .getOrCreate()



# PostgreSQL database configuration
db_host = "127.0.0.2"
db_name = "postgres"
db_user = "postgres"
db_password = "postgres"
table_name = "your_table_name"

url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

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

def get_block_commitment(slot):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlockCommitment",
        "params": [slot]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']['commitment'], response_data['result']['totalStake']

def get_blocks(start_slot, end_slot):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlocks",
        "params": [start_slot, end_slot]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_blocksWithLimit(start_slot, limit):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlocksWithLimit",
        "params": [start_slot, limit]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_block_time(slot):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBlockTime",
        "params": [slot]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    if 'error' in response_data:
        return None, response_data['error']['message']
    else:
        return response_data['result'], None

def get_cluster_nodes():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getClusterNodes"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_epoch_info():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getEpochInfo"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_epoch_schedule():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getEpochSchedule"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_fee_for_message(message):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getFeeForMessage",
        "params": [message, {"commitment": "processed"}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']['value'] if 'value' in response_data['result'] else None

def get_first_available_block():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getFirstAvailableBlock"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_genesis_hash():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getGenesisHash"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_health():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getHealth"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result'] if 'result' in response_data else response_data['error']


def get_inflation_governor():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getInflationGovernor"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_inflation_rate():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getInflationRate"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_leader_schedule():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getLeaderSchedule"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_max_retransmit_slot():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMaxRetransmitSlot"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_max_shred_insert_slot():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMaxShredInsertSlot"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_minimum_balance_for_rent_exemption(size):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMinimumBalanceForRentExemption",
        "params": [size]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_multiple_accounts(pubkeys):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getMultipleAccounts",
        "params": [pubkeys]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_recent_performance_samples(limit=None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getRecentPerformanceSamples",
        "params": [limit] if limit else []
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_recent_prioritization_fees(addresses=None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getRecentPrioritizationFees",
        "params": [addresses] if addresses else []
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_signatures_for_address(address, limit=None):
    try:
        params = [
            address,
            {
                "limit": limit
            }
        ]
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": params
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

def get_signature_statuses(signatures, search_transaction_history=None):
    params = [signatures]
    if search_transaction_history is not None:
        params.append({"searchTransactionHistory": search_transaction_history})
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignatureStatuses",
        "params": params
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_slot(commitment=None, min_context_slot=None):
    config = {}
    if commitment:
        config["commitment"] = commitment
    if min_context_slot:
        config["minContextSlot"] = min_context_slot
    params = [config] if config else []
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot",
        "params": params
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_slot_leader(commitment=None, min_context_slot=None):
    config = {}
    if commitment:
        config["commitment"] = commitment
    if min_context_slot:
        config["minContextSlot"] = min_context_slot
    params = [config] if config else []
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlotLeader",
        "params": params
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

def get_transactions_for_address(address):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedSignaturesForAddress2",
        "params": [address, {"limit": 100}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    if 'result' in response_data:
        return response_data['result']
    else:
        print(f"Error retrieving transactions for address {address}: {response_data.get('error')}")
        return []


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
            block_data = response_data['result']
            block_time = block_data.get('blockTime', None)
            if block_time is not None:
                block_data['timestamp'] = block_time
            return block_data
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


# Get the most recent block hash
latest_blockhash = get_latest_blockhash()

# Unique addresses involved in the transactions
unique_addresses = set()

# If we have a recent block hash, get its details
if latest_blockhash is not None:
    block_data = get_block(latest_blockhash)
    if block_data is not None:
        # Loop through each transaction in the block
        for transaction in block_data['transactions']:
            # Get the addresses involved in the transaction
            for address in transaction['transaction']['message']['accountKeys']:
                unique_addresses.add(address)


def filter_records(records):
    filtered_records = []
    current_time = datetime.now()
    two_years_ago = current_time - timedelta(days=365 * 2)

    for record in records:
        if 'blockTime' in record and record['blockTime'] is not None:
            # Extract the blockTime field as the timestamp
            timestamp = datetime.fromtimestamp(record['blockTime'])

            if timestamp >= two_years_ago:
                filtered_records.append(record)

    return filtered_records


# Create a cursor to execute SQL queries
cursor = conn.cursor()

# Create the table if it doesn't exist
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (transaction_id TEXT, address TEXT)"
cursor.execute(create_table_query)
conn.commit()

# Get transactions for the unique addresses
for address in unique_addresses:
    transactions = get_transactions_for_address(address)
    print(f"Transactions for address: {address}")

    # Filter out records older than two years
    filtered_transactions = filter_records(transactions)

    for transaction in filtered_transactions:
        # Retrieve the transaction ID from the 'signature' field
        transaction_id = transaction['signature']

        # Insert each transaction into the PostgreSQL table
        insert_query = f"INSERT INTO {table_name} (transaction_id, address) VALUES (%s, %s)"
        values = (transaction_id, address)
        cursor.execute(insert_query, values)
        conn.commit()

# Close the cursor and the database connection
cursor.close()
conn.close()
