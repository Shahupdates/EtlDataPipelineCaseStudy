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
            result = response_data['result']
            # Including the blockTime in the returned result
            transactions = []
            for transaction in result.get('transactions', []):
                transaction_info = transaction['transaction']
                meta = transaction.get('meta', {})
                # Calculate the amount from preBalances and postBalances
                amount = sum(meta.get('postBalances', [])) - sum(meta.get('preBalances', []))
                # Create a new transaction record
                transactions.append({
                    'timestamp': result.get('blockTime'),
                    'address': transaction_info['message']['accountKeys'][0],
                    'amount': amount,
                })
            return transactions, result.get('blockTime')
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
        record for record in data if datetime.datetime.fromtimestamp(int(record['timestamp'])) >
                                   datetime.datetime.now() - datetime.timedelta(days=365 * 2)
    ]
    return filtered_data

def load_data(data):
    # Assuming you have a table named 'transactions' with appropriate columns in your PostgreSQL database
    insert_query = "INSERT INTO public.transactions (address, timestamp, amount) VALUES (%s, to_timestamp(%s), %s)"
    for record in data:
        cursor.execute(insert_query, (record['address'], record['timestamp'], record['amount']))
    conn.commit()
    print('Data loaded successfully.')


def close_connection():
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed.")


if __name__ == '__main__':
    latest_block = get_latest_blockhash()
    if latest_block is not None:
        transactions, _ = get_block(latest_block)
        if transactions is not None:
            data = transform_data(transactions)
            load_data(data)
    close_connection()
