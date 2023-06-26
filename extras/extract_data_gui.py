import sys
import tkinter as tk
from tkinter import messagebox, ttk
from threading import Thread
from contextlib import redirect_stdout
import subprocess
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
            # Including the blockTime in the returned result
            result = response_data['result']
            transactions = result['transactions']
            for transaction in transactions:
                message = transaction['transaction']['message']
                meta = transaction['meta']
                for i, account in enumerate(message['accountKeys']):
                    # Calculate amount based on whether account is a sender or a receiver
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
        if isinstance(tokens, list):
            return [token.get('token') for token in tokens]
        elif isinstance(tokens, dict):
            return [tokens.get('token')]
    return None

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
    df = spark.createDataFrame(data, ["address", "amount", "timestamp"])

    # Cast the timestamp column to the appropriate data type
    df = df.withColumn("timestamp", to_timestamp(col("timestamp")))

    # Deduplicate the data based on the address and timestamp columns
    window = Window.partitionBy("address", "timestamp").orderBy(col("amount").desc())
    deduplicated_df = df.withColumn("row_number", row_number().over(window)).where(col("row_number") == 1).drop("row_number")

    deduplicated_df.write.jdbc(url=jdbcUrl, table=table, mode="append", properties=properties)
    print('Data loaded successfully.')

def run_dbt_transformation():
    command = "dbt run --models +transformations.transform_data"
    subprocess.run(command, shell=True)

def print_to_console(text):
    console.insert(tk.END, str(text) + '\n')
    console.see(tk.END)  # Auto-scroll to the end

class IORedirector(object):
    def __init__(self, text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    def write(self, str):
        self.text_area.insert(tk.END, str)
        self.text_area.see(tk.END)  # Auto-scroll to the end

    def flush(self):
        pass

def run_etl_pipeline():
    print("ETL pipeline execution started")
    latest_block = get_latest_blockhash()
    if latest_block is not None:
        transactions, _ = get_block(latest_block)
        if transactions is not None:
            load_data(transactions)
            run_dbt_transformation()
    print("ETL pipeline execution completed")

def start_etl_pipeline():
    global thread
    thread = Thread(target=run_etl_pipeline)
    thread.start()

def stop_etl_pipeline():
    if thread.is_alive():
        print("Stopping ETL pipeline...")
        spark.stop()  # Assume spark is a globally available SparkSession
        thread.join()
        print("ETL pipeline stopped")

root = tk.Tk()
root.geometry('600x400')
root.title("Solana ETL Pipeline")

frame = ttk.Frame(root, padding="10 10 10 10")
frame.pack(fill='both', expand=True)

style = ttk.Style(root)
style.configure("TButton",
                foreground="midnight blue",
                background="gold",
                padding=10,
                relief="raised",
                font=('Helvetica', 14, 'bold'))

start_button = ttk.Button(frame, text="Start ETL Pipeline", command=start_etl_pipeline)
start_button.pack(side=tk.LEFT, fill='both', expand=True)

stop_button = ttk.Button(frame, text="Stop ETL Pipeline", command=stop_etl_pipeline)
stop_button.pack(side=tk.LEFT, fill='both', expand=True)

console = tk.Text(frame)
console.pack(fill='both', expand=True)

sys.stdout = StdoutRedirector(console)

root.mainloop()

if __name__ == '__main__':
    latest_block = get_latest_blockhash()
    if latest_block is not None:
        transactions, _ = get_block(latest_block)
        if transactions is not None:
            load_data(transactions)
            run_dbt_transformation()

    spark.stop()


