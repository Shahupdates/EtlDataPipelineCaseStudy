import time
import requests
import json

url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

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
    params = [address]
    if limit:
        params.append({"limit": limit})
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": params
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_data = response.json()
    return response_data['result']

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

def get_supply():
    data = {
        "jsonrpc":"2.0",
        "id":1,
        "method":"getSupply"
    }
    response = requests.post('http://localhost:8899', json=data)
    return response.json()

def get_token_account_balance(pubkey):
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountBalance",
        "params": [pubkey]
    }
    response = requests.post('http://localhost:8899', json=data)
    return response.json()

def get_token_accounts_by_delegate(pubkey, program_id, encoding='jsonParsed'):
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByDelegate",
        "params": [
            pubkey,
            {
                "programId": program_id
            },
            {
                "encoding": encoding
            }
        ]
    }
    response = requests.post('http://localhost:8899', json=data)
    return response.json()

def get_token_accounts_by_owner(pubkey, mint, encoding='jsonParsed'):
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccountsByOwner",
        "params": [
            pubkey,
            {
                "mint": mint
            },
            {
                "encoding": encoding
            }
        ]
    }
    response = requests.post('http://localhost:8899', json=data)
    return response.json()

def getTokenLargestAccounts(pubkey):
    url = "http://localhost:8899"
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenLargestAccounts",
        "params": [
            pubkey
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# 2. getTokenSupply method
def getTokenSupply(pubkey):
    url = "http://localhost:8899"
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenSupply",
        "params": [
            pubkey
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# 3. getTransaction method
def getTransaction(transaction_signature):
    url = "http://localhost:8899"
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransaction",
        "params": [
            transaction_signature,
            "json"
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# 4. getTransactionCount method
def getTransactionCount():
    url = "http://localhost:8899"
    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc":"2.0",
        "id":1,
        "method":"getTransactionCount"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def call_rpc_method(method, params=None):
    url = "http://localhost:8899"
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
    }
    if params is not None:
        payload["params"] = params
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# getVersion
def get_version():
    return call_rpc_method("getVersion")

# getVoteAccounts
def get_vote_accounts(config=None):
    return call_rpc_method("getVoteAccounts", [config] if config else None)

# isBlockhashValid
def is_blockhash_valid(blockhash, config=None):
    return call_rpc_method("isBlockhashValid", [blockhash, config] if config else [blockhash])

# minimumLedgerSlot
def minimum_ledger_slot():
    return call_rpc_method("minimumLedgerSlot")

# requestAirdrop
def request_airdrop(pubkey, lamports, config=None):
    return call_rpc_method("requestAirdrop", [pubkey, lamports, config] if config else [pubkey, lamports])

# sendTransaction
def send_transaction(transaction, config=None):
    return call_rpc_method("sendTransaction", [transaction, config] if config else [transaction])

# simulateTransaction
def simulate_transaction(transaction, config=None):
    return call_rpc_method("simulateTransaction", [transaction, config] if config else [transaction])



# Using the functions
blockhash, last_valid_block_height = get_latest_blockhash()
print(f"Blockhash: {blockhash}")
print(f"Last Valid Block Height: {last_valid_block_height}")
time.sleep(1)
commitment, total_stake = get_block_commitment(5)
print(f"Commitment: {commitment}")
print(f"Total Stake: {total_stake}")
time.sleep(1)
blocks = get_blocks(5, 10)
print(f"Blocks: {blocks}")
time.sleep(1)
blocksWithLimit = get_blocksWithLimit(5, 3)
print(f"Blocks: {blocksWithLimit}")
time.sleep(1)
block_time, error = get_block_time(5)
if error:
    print(f"Error: {error}")
else:
    print(f"Block Time: {block_time}")
time.sleep(1)
# Using the new functions
cluster_nodes = get_cluster_nodes()
print(f"Cluster Nodes: {cluster_nodes}")
time.sleep(1)
epoch_info = get_epoch_info()
print(f"Epoch Info: {epoch_info}")
time.sleep(1)
epoch_schedule = get_epoch_schedule()
print(f"Epoch Schedule: {epoch_schedule}")
time.sleep(1)
fee_for_message = get_fee_for_message("AQABAgIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAQAA")
print(f"Fee for Message: {fee_for_message}")
time.sleep(1)
first_available_block = get_first_available_block()
print(f"First Available Block: {first_available_block}")
time.sleep(1)
# Using the new functions
inflation_governor = get_inflation_governor()
print(f"Inflation Governor: {inflation_governor}")
time.sleep(1)
inflation_rate = get_inflation_rate()
print(f"Inflation Rate: {inflation_rate}")
time.sleep(1)
leader_schedule = get_leader_schedule()
print(f"Leader Schedule: {leader_schedule}")
time.sleep(1)
# Using the new functions
max_retransmit_slot = get_max_retransmit_slot()
print(f"Max Retransmit Slot: {max_retransmit_slot}")
time.sleep(1)
max_shred_insert_slot = get_max_shred_insert_slot()
print(f"Max Shred Insert Slot: {max_shred_insert_slot}")
time.sleep(1)
minimum_balance_for_rent_exemption = get_minimum_balance_for_rent_exemption(50)
print(f"Minimum Balance For Rent Exemption: {minimum_balance_for_rent_exemption}")
time.sleep(1)
multiple_accounts = get_multiple_accounts(["vines1vzrYbzLMRdu58ou5XTby4qAqVRLmqo36NKPTg", "4fYNw3dojWmQ4dXtSGE9epjRGy9pFSx62YypT7avPYvA"])
print(f"Multiple Accounts: {multiple_accounts}")
time.sleep(1)
# Test get_recent_performance_samples function
recent_performance_samples = get_recent_performance_samples(5)
print(f"Recent Performance Samples: {recent_performance_samples}")
time.sleep(1)
# Test get_recent_prioritization_fees function
recent_prioritization_fees = get_recent_prioritization_fees(["So11111111111111111111111111111111111111112"])
print(f"Recent Prioritization Fees: {recent_prioritization_fees}")
time.sleep(1)
# Test get_signatures_for_address function
signatures_for_address = get_signatures_for_address("4Nd1mBQtrMJVYVfKf2PJy9NZUZdTAsp7D4xWLs4gDB4T")
print(f"Signatures For Address: {signatures_for_address}")
time.sleep(1)
# Test get_signature_statuses function
signature_statuses = get_signature_statuses(["4fW2UzNVA7gE1HUnBoRWcHY8YbXgN9GXPzqbS4Q4HSGyNtZRmzHnv2LVULGEX3KMk4tPXQaG9gSow27j7BqKMJhP"])
print(f"Signature Statuses: {signature_statuses}")
time.sleep(1)
# Test get_slot function
slot = get_slot()
print(f"Slot: {slot}")
time.sleep(1)
# Test get_slot_leader function
slot_leader = get_slot_leader()
print(f"Slot Leader: {slot_leader}")
time.sleep(1)
# Test get_supply function
supply = get_supply()
print(f"Supply: {supply}")
time.sleep(1)
# Test get_token_account_balance function
token_account_balance = get_token_account_balance("So11111111111111111111111111111111111111112")
print(f"Token Account Balance: {token_account_balance}")
time.sleep(1)
# Test get_token_accounts_by_delegate function
token_accounts_by_delegate = get_token_accounts_by_delegate("So11111111111111111111111111111111111111112", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
print(f"Token Accounts By Delegate: {token_accounts_by_delegate}")
time.sleep(1)
# Test get_token_accounts_by_owner function
token_accounts_by_owner = get_token_accounts_by_owner("So11111111111111111111111111111111111111112", "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
print(f"Token Accounts By Owner: {token_accounts_by_owner}")
time.sleep(1)
# Test getTokenLargestAccounts function
token_largest_accounts = getTokenLargestAccounts("So11111111111111111111111111111111111111112")
print(f"Token Largest Accounts: {token_largest_accounts}")
time.sleep(1)
# Test getTokenSupply function
token_supply = getTokenSupply("So11111111111111111111111111111111111111112")
print(f"Token Supply: {token_supply}")
time.sleep(1)
# Test getTransaction function
transaction = getTransaction("4fW2UzNVA7gE1HUnBoRWcHY8YbXgN9GXPzqbS4Q4HSGyNtZRmzHnv2LVULGEX3KMk4tPXQaG9gSow27j7BqKMJhP")
print(f"Transaction: {transaction}")
time.sleep(1)
# Test getTransactionCount function
transaction_count = getTransactionCount()
print(f"Transaction Count: {transaction_count}")
time.sleep(1)
# Test call_rpc_method function
rpc_response = call_rpc_method("getTransactionCount")
print(f"RPC Response: {rpc_response}")
time.sleep(1)
# Test get_genesis_hash function
genesis_hash = get_genesis_hash()
print(f"Genesis Hash: {genesis_hash}")
time.sleep(1)
# Test get_health function
health = get_health()
print(f"Health: {health}")
