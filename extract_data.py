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
