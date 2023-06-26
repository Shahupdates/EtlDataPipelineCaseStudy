import asyncio

import aiohttp
import requests
import json
import datetime

url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

ignored_accounts = set([
    'SysvarC1ock11111111111111111111111111111111',
    'SysvarS1otHashes111111111111111111111111111',
    'ComputeBudget111111111111111111111111111111',
    'Vote111111111111111111111111111111111111111',
    '11111111111111111111111111111111'
])

class SolanaAPI:
    def __init__(self, session):
        self.session = session
        self.magic_nfts_cache = {}

    async def get_magic_nfts_async(self, i, address):
        # If address already checked, fetch the response from cache
        if address in self.magic_nfts_cache:
            return i, self.magic_nfts_cache[address]

        magic_endpoint = f"https://api-mainnet.magiceden.dev/v2/wallets/{address}/tokens"
        async with aiohttp.ClientSession() as session:
            async with session.get(magic_endpoint) as resp:
                if resp.status == 200:
                    tokens = await resp.json()
                    # Store the response in cache
                    if isinstance(tokens, list) and tokens:
                        self.magic_nfts_cache[address] = [token.get('token') for token in tokens]
                        print(f"Magic Eden NFT(s) found for account {address}.")
                        return i, self.magic_nfts_cache[address]
                    elif isinstance(tokens, dict) and tokens.get('token'):
                        self.magic_nfts_cache[address] = [tokens.get('token')]
                        print(f"Magic Eden NFT found for account {address}.")
                        return i, self.magic_nfts_cache[address]

                    # Store negative response in cache
                    self.magic_nfts_cache[address] = None
        return i, None

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
                        transaction_data = await self.process_transaction_data(transaction, result)
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

    async def process_transaction_data(self, transaction, result):
        message = transaction['transaction']['message']
        meta = transaction['meta']
        tasks = []
        for i, account in enumerate(message['accountKeys']):
            if account not in ignored_accounts:  # Exclude ignored accounts
                print(f"Checking Magic Eden NFTs for account {account}")
                tasks.append(self.get_magic_nfts_async(i,
                                                       account))  # I assumed this is an async function. If not, you should make it async.
        results = await asyncio.gather(*tasks)  # wait for all tasks to finish
        for i, magic_nfts in enumerate(results):
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


