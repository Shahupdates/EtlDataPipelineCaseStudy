import requests
import json
import datetime

url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

class SolanaAPI:
    def __init__(self, session):
        self.session = session

    async def get_block(self, slot):
        print(f"Getting block for slot: {slot}")
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBlock",
                "params": [slot, {"encoding": "json", "transactionDetails": "full", "rewards": False,
                                  "maxSupportedTransactionVersion": 0}]
            }
            print(f"Sending request to: {url}")
            async with self.session.post(url, headers=headers, data=json.dumps(payload)) as response:
                print(f"Received response: {response.status}")
                response_data = await response.json()
                print(f"Response data: {response_data}")
                transactions_list = []  # List to hold all transactions
                if 'result' in response_data:
                    result = response_data['result']
                    transactions = result['transactions']
                    for transaction in transactions:
                        transaction_data = self.process_transaction_data(transaction, result)
                        if transaction_data:
                            transactions_list.append(transaction_data)
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

    async def get_latest_blockhash(self):
        print("Getting latest block...")
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getLatestBlockhash"
            }
            async with self.session.post(url, headers=headers, data=json.dumps(payload)) as response:
                response_data = await response.json()
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
