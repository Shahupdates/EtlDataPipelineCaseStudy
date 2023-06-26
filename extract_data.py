import aiohttp
import asyncio
import json
import datetime
import time
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

        # Set a limit for how many blocks to process in one go
        num_blocks_to_process = 10
        for i in range(num_blocks_to_process):
            latest_block = await solana_api.get_latest_blockhash()
            if latest_block is not None:
                transactions, _ = await solana_api.get_block(latest_block)
                if transactions is not None:
                    deduplicated_df = spark_operations.load_data(transactions)

                    spark_operations.calculate_dau(deduplicated_df)
                    spark_operations.calculate_daily_transaction_volume(deduplicated_df)
                    spark_operations.run_dbt_transformation()

            # Yield progress updates as a percentage
            yield (i+1) / num_blocks_to_process * 100

        spark_operations.stop_spark()

