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
            result = response_data['result']
            transactions = result['transactions']
            for transaction in transactions:
                message = transaction['transaction']['message']
                meta = transaction['meta']
                for i, account in enumerate(message['accountKeys']):
                    # Check if the account has Magic Eden NFTs
                    magic_nfts = get_magic_nfts(account)
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
