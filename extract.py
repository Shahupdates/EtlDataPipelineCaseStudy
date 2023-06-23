import logging
import pandas as pd
from solana.account import Account
from solana.publickey import PublicKey
from solana.rpc.api import Client
from pyspark.sql import SparkSession
from sqlalchemy import create_engine
from pyspark.sql import DataFrame
from datetime import datetime, timedelta
from pyspark.sql.functions import col

# setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# setup Solana client
solana_client = Client("https://api.mainnet-beta.solana.com")

# setup Spark
spark = SparkSession.builder.appName('solana_transform').getOrCreate()

# setup PostgreSQL engine
engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/mydatabase')


def extract_data(contract_address: str) -> DataFrame:
    try:
        # Convert the contract address to a PublicKey
        contract_pubkey = PublicKey(contract_address)

        # Request account info from the Solana node
        response = solana_client.get_account_info(contract_pubkey)

        # The actual data will be located in the response['result']['value'] dictionary
        raw_data = response['result']['value']

        # Print raw data to inspect its structure
        print(raw_data)

        # Depending on the structure of raw_data, you might want to flatten it into a format that's suitable for conversion to a DataFrame
        # Here, I'm assuming raw_data is a dictionary. If it's not, you'll need to adjust this part.
        data_df = pd.DataFrame([raw_data])  # Creates a single row DataFrame from the dictionary

        # Convert pandas DataFrame to Spark DataFrame
        spark_df = spark.createDataFrame(data_df)

        return spark_df

    except Exception as e:
        logger.error("Failed to extract data from Solana.", exc_info=True)
        raise e


def transform_data(data: DataFrame, contract_address: str) -> DataFrame:
    try:
        # Filter out any records that are older than two years
        two_years_ago = datetime.now() - timedelta(days=2*365)
        filtered_data = data.filter(col("date") >= two_years_ago)

        # More transformations based on contract_address if needed

        return filtered_data
    except Exception as e:
        logger.error("Failed to transform data.", exc_info=True)
        raise e


def load_data(data: DataFrame, table_name: str):
    try:
        # Write transformed data to PostgreSQL
        data.write \
            .format('jdbc') \
            .option('url', 'jdbc:postgresql://localhost:5432/mydatabase') \
            .option('dbtable', table_name) \
            .option('user', 'username') \
            .option('password', 'password') \
            .mode('overwrite') \
            .save()
    except Exception as e:
        logger.error("Failed to load data into PostgreSQL.", exc_info=True)
        raise e


def run_etl(contract_address: str, table_name: str):
    data = extract_data(contract_address)
    transformed_data = transform_data(data, contract_address)
    load_data(transformed_data, table_name)


if __name__ == "__main__":
    run_etl("Magic Eden Contract Address", "solana_table")
