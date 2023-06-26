import subprocess
import aiohttp
import asyncio
import requests
import json
import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number, to_timestamp
from pyspark.sql.window import Window

url = "https://api.mainnet-beta.solana.com"
headers = {"Content-Type": "application/json"}

# Start Spark session
spark = SparkSession.builder \
    .appName("Solana ETL") \
    .config("spark.jars", "postgresql-42.6.0.jar") \
    .getOrCreate()

# PostgreSQL connection details
jdbcUrl = "jdbc:postgresql://localhost/main_database"
table = "public.transactions"
properties = {"user": "postgres", "password": "postgres", "driver": "org.postgresql.Driver"}

ignored_accounts = set([
    'SysvarC1ock11111111111111111111111111111111',
    'SysvarS1otHashes111111111111111111111111111',
    'ComputeBudget111111111111111111111111111111',
    'Vote111111111111111111111111111111111111111',
    '11111111111111111111111111111111'
])


async def get_block(slot):
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
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(f"Received response: {response.status_code}")
        response_data = response.json()
        print(f"Response data: {response_data}")
        transactions_list = []  # List to hold all transactions
        if 'result' in response_data:
            result = response_data['result']
            transactions = result['transactions']
            for transaction in transactions:
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
                            'timestamp': datetime.datetime.fromtimestamp(result['blockTime']).strftime(
                                '%Y-%m-%d %H:%M:%S')
                        }
                        transactions_list.append(transaction_dict)  # Add the dictionary to the list
                        load_data([transaction_dict])  # Load data immediately
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
        if isinstance(tokens, list) and tokens:
            print(f"Magic Eden NFT(s) found for account {address}.")
            return [token.get('token') for token in tokens]
        elif isinstance(tokens, dict) and tokens.get('token'):
            print(f"Magic Eden NFT found for account {address}.")
            return [tokens.get('token')]
    return None


magic_nfts_cache = {}


async def get_magic_nfts_async(i, address):
    # If address already checked, fetch the response from cache
    if address in magic_nfts_cache:
        return i, magic_nfts_cache[address]

    magic_endpoint = f"https://api-mainnet.magiceden.dev/v2/wallets/{address}/tokens"
    async with aiohttp.ClientSession() as session:
        async with session.get(magic_endpoint) as resp:
            if resp.status == 200:
                tokens = await resp.json()
                # Store the response in cache
                if isinstance(tokens, list) and tokens:
                    magic_nfts_cache[address] = [token.get('token') for token in tokens]
                    print(f"Magic Eden NFT(s) found for account {address}.")
                    return i, magic_nfts_cache[address]
                elif isinstance(tokens, dict) and tokens.get('token'):
                    magic_nfts_cache[address] = [tokens.get('token')]
                    print(f"Magic Eden NFT found for account {address}.")
                    return i, magic_nfts_cache[address]

                # Store negative response in cache
                magic_nfts_cache[address] = None
    return i, None


"""
def transform_data(data):
    print(data[:5])  # print the first 5 items
    filtered_data = [
        {
            'address': record['address'],
            'amount': record['amount'],
            'timestamp': datetime.datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S')
        }
        for record in data
        if datetime.datetime.strptime(record['timestamp'], '%Y-%m-%d %H:%M:%S') > datetime.datetime.now() - datetime.timedelta(days=365 * 2)
    ]
    return filtered_data
"""


def load_data(data):
    df = spark.createDataFrame(data, ["address", "amount", "amount_sol", "timestamp"])

    # Cast the timestamp column to the appropriate data type
    df = df.withColumn("timestamp", to_timestamp(col("timestamp")))

    # Deduplicate the data based on the address and timestamp columns
    window = Window.partitionBy("address", "timestamp").orderBy(col("amount").desc())
    deduplicated_df = df.withColumn("row_number", row_number().over(window)).where(col("row_number") == 1).drop("row_number")

    deduplicated_df.write.jdbc(url=jdbcUrl, table=table, mode="append", properties=properties)
    print('Data loaded successfully.')

    # Return the deduplicated dataframe
    return deduplicated_df


def run_dbt_transformation():
    command = "dbt run --models +transformations.transform_data"
    subprocess.run(command, shell=True)


def calculate_dau(df):
    df.createOrReplaceTempView("transactions")
    dau = spark.sql("""
        SELECT
            date(timestamp) AS date,
            count(distinct address) AS dau
        FROM transactions
        GROUP BY date(timestamp)
    """)
    dau.write.jdbc(url=jdbcUrl, table="public.daily_active_users", mode="overwrite", properties=properties)
    print('Daily active users data loaded successfully.')


def calculate_daily_transaction_volume(df):
    df.createOrReplaceTempView("transactions")
    daily_tx_volume = spark.sql("""
        SELECT
            date(timestamp) AS date,
            sum(amount_sol) AS daily_tx_volume
        FROM transactions
        GROUP BY date(timestamp)
    """)
    daily_tx_volume.write.jdbc(url=jdbcUrl, table="public.daily_transaction_volume", mode="overwrite", properties=properties)
    print('Daily transaction volume data loaded successfully.')


async def main():
    print("Getting latest block...")
    latest_block = get_latest_blockhash()
    if latest_block is not None:
        print("Got latest block", latest_block)
        print("Getting transactions for block...")
        transactions, _ = await get_block(latest_block)
        if transactions is not None:
            print("Got transactions", transactions)
            print("Loading data...")
            deduplicated_df = load_data(transactions)

            print("Calculating daily active users...")
            calculate_dau(deduplicated_df)

            print("Calculating daily transaction volume...")
            calculate_daily_transaction_volume(deduplicated_df)

            print("Running dbt transformation...")
            run_dbt_transformation()

    print("Stopping spark...")
    spark.stop()


if __name__ == '__main__':
    asyncio.run(main())
