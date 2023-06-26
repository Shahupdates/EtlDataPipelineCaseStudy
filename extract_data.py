import aiohttp
import asyncio
import json
import datetime
from spark_operations import SparkOperations
from solana_api import SolanaAPI
from magic_eden_api import MagicEdenAPI

ignored_accounts = set([
    'SysvarC1ock11111111111111111111111111111111',
    'SysvarS1otHashes111111111111111111111111111',
    'ComputeBudget111111111111111111111111111111',
    'Vote111111111111111111111111111111111111111',
    '11111111111111111111111111111111'
])

async def process_data():
    async with aiohttp.ClientSession() as session:
        solana_api = SolanaAPI(session)
        magic_eden_api = MagicEdenAPI(session)
        spark_operations = SparkOperations()

        latest_block = await solana_api.get_latest_blockhash()
        if latest_block is not None:
            transactions, _ = await solana_api.get_block(latest_block)
            if transactions is not None:
                deduplicated_df = spark_operations.load_data(transactions)

                spark_operations.calculate_dau(deduplicated_df)
                spark_operations.calculate_daily_transaction_volume(deduplicated_df)
                spark_operations.run_dbt_transformation()

        spark_operations.stop_spark()

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
