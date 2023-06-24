# ETL Pipeline Documentation

This repository contains two different ETL (Extract, Transform, Load) pipelines for processing blockchain transaction data from the Solana Blockchain.

## ETL Pipeline using dbt, Apache Spark, Python, and PostgreSQL

### Features
- Extracts data from the Solana Blockchain.
- Applies transformations based on business rules using dbt.
- Loads the transformed data into PostgreSQL using Apache Spark.

### Prerequisites
Before running this ETL pipeline, ensure that you have the following dependencies installed:
- Python (version X.X.X)
- PostgreSQL (version X.X.X)
- Apache Spark (version X.X.X)
- dbt (version X.X.X)

### Setup and Usage
1. Clone the repository to your local machine: `git clone https://github.com/your-username/etlpipeline.git`
2. Navigate to the project directory: `cd etlpipeline`
3. Install the required Python dependencies: `pip install -r requirements.txt`
4. Configure the PostgreSQL connection in the profiles.yml file located in the .dbt directory. Modify the `dev` section with your PostgreSQL credentials.
```
default:
  outputs:
    dev:
      type: postgres
      host: 127.0.0.2
      port: 5432
      user: postgres
      pass: postgres
      dbname: postgres
      schema: myschema
  target: dev
```
6. Run the extraction script: `python extract_data.py`
7. Apply transformations using dbt: `dbt run --models transform`
8. Load the transformed data into PostgreSQL: `dbt run --models load`
9. Check the individual code files and SQL queries for more details on each step of the pipeline.

### Configuration
The configuration for the ETL pipeline is defined in the dbt_project.yml file. It specifies the project name, version, and model settings. Modify the file according to your specific requirements.
```
name: 'my_new_project'
version: '1.0.0'

profile: 'default'

source-paths: ["models"]
analysis-paths: ["analysis"]
test-paths: ["tests"]
data-paths: ["data"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_modules"

models:
  my_new_project:
    enabled: true
    materialized: view
    sql: models/transform/transformation.sql
```
## Python-only ETL Pipeline

### Features
- Retrieves the latest blockhash from the Solana Blockchain.
- Retrieves transactions for unique addresses involved in the latest block.
- Filters out records older than two years.
- Inserts the filtered transactions into a PostgreSQL database.

### Prerequisites
Before running the Python-only ETL pipeline, ensure that you have the following dependencies installed:
- Python 3.x
- `psycopg2` library for PostgreSQL connectivity (`pip install psycopg2`)
- `requests` library for making API requests (`pip install requests`)

### Usage
1. Install the required libraries mentioned in the prerequisites.
2. Configure the PostgreSQL database connection parameters.
3. Run the script: `python main.py`
4. Check the script output for the retrieved addresses and the status of the data insertion.

### Notes
- The Python script uses the Solana Blockchain API to fetch transaction data. Ensure a stable internet connection and proper API access.
- It is recommended to schedule and automate the script execution for periodic data updates.

## Functionality

This Python script provides several functions to interact with the Solana Blockchain and perform various operations:

- `get_latest_blockhash()`: Retrieves the latest blockhash from the Solana Blockchain.
- `get_block_commitment(slot)`: Retrieves the commitment and total stake information for a specific block.
- `get_blocks(start_slot, end_slot)`: Retrieves a range of blocks between the specified start and end slots.
- `get_blocksWithLimit(start_slot, limit)`: Retrieves a limited number of blocks starting from the specified slot.
- `get_block_time(slot)`: Retrieves the block time (timestamp) for a specific slot.
- `get_cluster_nodes()`: Retrieves information about the nodes in the Solana cluster.
- `get_epoch_info()`: Retrieves information about the current epoch.
- `get_epoch_schedule()`: Retrieves the epoch schedule information.
- `get_fee_for_message(message)`: Retrieves the fee for a specific message.
- `get_first_available_block()`: Retrieves the slot of the first available block.
- `get_genesis_hash()`: Retrieves the genesis hash of the Solana Blockchain.
- `get_health()`: Retrieves the health status of the Solana cluster.
- `get_inflation_governor()`: Retrieves information about the inflation governor.
- `get_inflation_rate()`: Retrieves the current inflation rate.
- `get_leader_schedule()`: Retrieves the leader schedule for the current epoch.
- `get_max_retransmit_slot()`: Retrieves the maximum retransmit slot.
- `get_max_shred_insert_slot()`: Retrieves the maximum shred insert slot.
- `get_minimum_balance_for_rent_exemption(size)`: Retrieves the minimum balance required for rent exemption based on the specified size.
- `get_multiple_accounts(pubkeys)`: Retrieves information about multiple accounts using their public keys.
- `get_recent_performance_samples(limit=None)`: Retrieves recent performance samples.
- `get_recent_prioritization_fees(addresses=None)`: Retrieves recent prioritization fees for specified addresses.
- `get_signatures_for_address(address, limit=None)`: Retrieves signatures for a specific address.
- `get_signature_statuses(signatures, search_transaction_history=None)`: Retrieves the status of multiple signatures.
- `get_slot(commitment=None, min_context_slot=None)`: Retrieves the current slot or minimum context slot.
- `get_slot_leader(commitment=None, min_context_slot=None)`: Retrieves the slot leader for the current slot or minimum context slot.
- `get_transactions_for_address(address)`: Retrieves confirmed signatures for a specific address.
- `get_block(slot)`: Retrieves the block data for a specific slot.

### PostgreSQL Database Integration

The script also integrates with a PostgreSQL database for data storage. It establishes a connection to the database and inserts filtered transaction records into the specified table.

To configure the PostgreSQL database connection, update the following variables in the script:

- `db_host`: Host of the PostgreSQL database.
- `db_name`: Name of the PostgreSQL database.
- `db_user`: Username for accessing the PostgreSQL database.
- `db_password`: Password for accessing the PostgreSQL database.
- `table_name`: Name of the table to store transaction records.

Make sure to install the `psycopg2` library (`pip install psycopg2`) for PostgreSQL connectivity.

## Additional Information
For more details on the ETL pipelines, refer to the individual code files and SQL queries. Feel free to explore and customize the pipelines according to your specific requirements.

## License
This project is licensed under this license:
Copyright (C) - All Rights Reserved.

THE CONTENTS OF THIS PROJECT ARE PROPRIETARY AND CONFIDENTIAL. UNAUTHORIZED COPYING, TRANSFERRING OR REPRODUCTION OF THE CONTENTS OF THIS PROJECT, VIA ANY MEDIUM IS STRICTLY PROHIBITED.

The receipt or possession of the source code and/or any parts thereof does not convey or imply any right to use them for any purpose other than the purpose for which they were provided to you.

The software is provided "AS IS", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and non infringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
