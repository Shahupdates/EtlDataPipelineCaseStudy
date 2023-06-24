import requests
import json

url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

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

def has_magic_nfts(address):
    magic_endpoint = "https://api-mainnet.magiceden.dev/v2/wallets/{}/tokens"
    magic_response = requests.get(magic_endpoint.format(address))
    return magic_response.status_code == 200

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
                # Check if the address has Magic Eden NFTs
                if has_magic_nfts(address):
                    unique_addresses.add(address)

# Print unique addresses
for address in unique_addresses:
    print(address)
