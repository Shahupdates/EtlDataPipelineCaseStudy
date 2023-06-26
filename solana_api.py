import asyncio

import requests
import json
import datetime

from extract_data import ignored_accounts, get_magic_nfts_async

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
                        transaction_data = await self.process_transaction_data(transaction, result)  # Add 'await' here
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

    def process_transaction_data(self, transaction, result):
        message = transaction['transaction']['message']
        meta = transaction['meta']
        tasks = []
        for i, account in enumerate(message['accountKeys']):
            if account not in ignored_accounts:  # Exclude ignored accounts
                print(f"Checking Magic Eden NFTs for account {account}")
                tasks.append(get_magic_nfts_async(i, account))
        for future in asyncio.as_completed(tasks):
            i, magic_nfts = await future
            if magic_nfts:
                account = message['accountKeys'][i]
                print(f"Finished checking Magic Eden NFTs for account {account}")
                pre_balance = meta['preBalances'][i]
                post_balance = meta['postBalances'][i]
                if account in message['instructions'][0]['accounts']:
                    amount = post_balance - pre_balance  # Receiver
                else:
                    amount = pre_balance - post_balance  # Sender
                amount_sol = amount / 1_000_000_000  # convert lamports to SOL
                transaction_dict = {
                    'address': account,
                    'amount': amount,
                    'amount_sol': amount_sol,
                    'timestamp': datetime.datetime.fromtimestamp(result['blockTime']).strftime('%Y-%m-%d %H:%M:%S')
                }
                return transaction_dict
        return None
