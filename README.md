# Solana ETL Pipeline 
  <img src="https://github.com/Shahupdates/EtlDataPipelineCaseStudy/assets/120000782/e9f27e7d-2467-4cde-92f0-3e31d33371bf" width="500" height="400" />
  <img src="https://github.com/Shahupdates/EtlDataPipelineCaseStudy/assets/120000782/ffcf0ad5-9210-4a64-9854-7ac5ed828e8e" width="500" height="400" /> 
</p>
This repository contains two different ETL (Extract, Transform, Load) pipelines for processing blockchain transaction data from the Solana Blockchain. This project's objective is to build a robust, scalable ETL pipeline to extract data from Solana Blockchain, transform it based on specific business rules, and load it into a PostgreSQL database. The README file explains how to set up and run the project, as does the part2andpart3.md file, which includes troubleshooting, and a retrospect viewpoint.

# Future updates:
* Add the optional aggregated tables
* Extract more data from the etl pipeline version

## GUI Updates (beta, not release):
* Stop Functionality: a "Stop" button has been integrated into the interface. This feature provides the ability to halt the ETL pipeline execution at any point. This enhancement is particularly useful when needing to pause data extraction or transformation without closing the application entirely.
* Console Logging: * the GUI now includes a dedicated console log section. This new feature emulates the console output, delivering live updates about the ETL pipeline progression. 
* Future Improvements: Looking forward, there are plans to display transactions directly from the database on the GUI. This addition would offer an immediate view of the extracted data, eliminating the need for separate database access.

# ETL Pipeline using dbt, Apache Spark, Python, and PostgreSQL
## Objective
Design, develop, optimize, and troubleshoot a big data ETL (Extract, Transform, Load) pipeline using Python, SQL, DBT, and Spark. The ETL pipeline should extract data from Solana Blockchain nodes, transform it, and load the processed data into PostgreSQL for further analysis.

### Prerequisites
Before running this ETL pipeline, ensure that you have the following dependencies installed:
- Python (version 3.7+)
- PostgreSQL
- Pyspark
- dbt (version 0.16.0)
- Access to Solana Blockchain Nodes
- Optional : A Unix-like system with `bash` or `sh` to run shell commands

### Project Structure
* `extract_data.py`: The Python script that implements the ETL pipeline.
* `models\transformation\transform_data.sql`: The DBT model that transforms the data based on the business rules.
* `dbt_project.yml`: The DBT configuration file.
* `profiles.yml`: The DBT profile that contains the PostgreSQL connection details.

### Extract Data from Solana Blockchain
The script extract_data.py contains two functions for extracting data:

* `get_block(slot)`: This function fetches block data for a given slot from Solana Blockchain. The data includes the transactions made in the block.
* `get_latest_blockhash()`: This function fetches the latest blockhash from Solana Blockchain.
  
### Setup and Usage
1. Clone the repository to your local machine: `git clone https://github.com/shahupdates/etldatapipelinecasestudy`
2. Navigate to the project directory: `cd etlpipeline`
3. Install the required Python dependencies: `pip install -r requirements.txt`
4. Configure the PostgreSQL connection in the profiles.yml file located in the .dbt directory below. If you don't have it, just create it and the subsequent profiles.yaml.
``` C:\users\<username>\.dbt\profiles.yaml```
6. Modify the `dev` section with your PostgreSQL credentials.

```yaml
dev:
  target: dev
  outputs:
    dev:
      type: postgres
      host: 127.0.0.1
      port: 5432
      user: postgres
      pass: postgres
      dbname: main_database
      schema: public
```

6. Run the extraction script: `python extract_data.py`
7. Apply transformations using dbt: `dbt run --models transform`
8. Load the transformed data into PostgreSQL: `dbt run --models load`
9. Check the individual code files and SQL queries for more details on each step of the pipeline.

### Configuration
The configuration for the ETL pipeline is defined in the dbt_project.yml file. It specifies the project name, version, and model settings. Modify the file according to your specific requirements.

```python
name: 'transform_data'
version: '1.0.0'
profile: 'dev'

## Configuring directories
source-paths: ["models"]
target-path: "target"
clean-targets: ["target"]

Note:
```To enable your script to take a contract address as a variable and apply it to different contract addresses, 
you can uncomment these lines (a global variable for the contract address and use that in your transaction analysis.) 
                               
# Global variable for contract address
contract_address = 'YourContractAddressHere'

# Then, modify the if statement within the get_block function
if account not in ignored_accounts and account == contract_address:

```



## Configuring models
models:
  transform_data:
    materialized: view
```

## Python-only ETL Pipeline

### Features
- Retrieves the latest blockhash from the Solana Blockchain.
- Retrieves transactions for unique addresses involved in the latest block.
- Filters out the non magic-eden holding addresses.
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

# ETL Pipeline Documentation

This document provides an overview of the ETL (Extract, Transform, Load) pipeline designed to process blockchain transaction data from the Solana Blockchain. It includes information about the pipeline's functionality, instructions for running it, collaboration strategies, performance optimization techniques, and a troubleshooting guide.

## Table of Contents
- [ETL Pipeline Overview](#etl-pipeline-overview)
- [Running the ETL Pipeline](#running-the-etl-pipeline)
- [Collaboration with Data Science and Business Teams](#collaboration-with-data-science-and-business-teams)
- [Performance Optimization](#performance-optimization)
- [Troubleshooting Guide](#troubleshooting-guide)

## ETL Pipeline Overview
The ETL pipeline processes blockchain transaction data from the Solana Blockchain. It consists of the following stages:

1. **Extraction**: Retrieves transaction data from the Solana Blockchain using the Solana Blockchain API. The extraction script, `extract_data.py`, connects to the API, retrieves the latest block hash, and extracts addresses from the block hash.

2. **Transformation**: Applies transformations to the extracted data to meet specific business rules and requirements. The transformation logic is defined in the `transformation.sql` file located in the `models/transform` directory. It includes rules such as filtering out records older than two years and extracting data only from Magic Eden contracts. The transformations are executed using DBT (Data Build Tool).

3. **Loading**: Loads the transformed data into a PostgreSQL database using Apache Spark. The data is written to the `transformed_addresses` table in the `myschema` schema.

## Running the ETL Pipeline
To run the ETL pipeline, follow these steps:

1. **Clone the Repository**: Clone the repository to your local machine: `git clone https://github.com/shahupdates/etldatapipelinecasestudy`
2. **Navigate to the Project Directory**: Go to the project directory: `cd etlpipeline`
3. **Install Python Dependencies**: Install the required Python dependencies: `pip install -r requirements.txt`
4. **Configure PostgreSQL Connection**: Open the `profiles.yml` file located in the `.dbt` directory located at ``` C:\users\<username>\.dbt\profiles.yaml``` and modify the `dev` section with your PostgreSQL credentials: If you don't have it, just create it and the subsequent profiles.yaml.

```yaml
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

5. Extraction: Run the extraction script to retrieve data from the Solana Blockchain: python extract_data.py
6. Transformation: Apply the transformations using DBT: dbt run --models transform
7. Loading: Load the transformed data into the PostgreSQL database: dbt run --models load
8. Check the individual code files and SQL queries for more details on each step of the pipeline.
    
# Collaboration with Data Science and Business Teams
To collaborate with data science and business teams and adjust the ETL pipeline to meet their needs, consider the following strategies:

* Regular Meetings: Schedule regular meetings to understand data requirements, discuss challenges, and gather feedback.

* Requirement Gathering: Engage in thorough requirement gathering sessions to capture specific data needs, formats, and business rules.

* Flexibility and Customization: Design the ETL pipeline to be flexible and customizable, allowing adjustments based on specific requirements. Use configuration files or command-line arguments to modify pipeline behavior.

* Iterative Development: Adopt an iterative development approach to incrementally enhance the pipeline based on evolving requirements and feedback.

# Performance Optimization
* Identifying and optimizing performance bottlenecks in the ETL pipeline can greatly improve its efficiency. Here are some strategies to consider:

* Data Partitioning: Partition large datasets based on key attributes to distribute the processing load and improve parallelism.

* Indexing: Properly index the database tables used in the pipeline to accelerate data retrieval and transformation operations.

* Query Optimization: Analyze and optimize SQL queries used in the pipeline to reduce execution time. Use query optimization techniques such as query rewriting, join order optimization, and index hints.

* Parallel Processing: Leverage parallel processing frameworks and techniques, such as Apache Spark, to process data in parallel and exploit the full potential of distributed computing.

* Hardware Optimization: Optimize hardware resources, such as increasing memory or using faster storage systems, to improve overall pipeline performance.

* Caching: Implement caching mechanisms to store intermediate results and avoid redundant computations.

# Troubleshooting Guide
* If the ETL pipeline encounters issues during execution, follow these steps to troubleshoot the problem:

* Check Logs: Review the pipeline logs for error messages or warnings. Logs can provide valuable information about the root cause of the issue.

* Verify Dependencies: Ensure that all required dependencies, libraries, and software versions are properly installed and configured.

* Test Components Independently: Isolate each component of the pipeline (extraction, transformation, loading) and test them independently to identify the specific stage where the issue occurs.

* Debug Code: Use debugging techniques to identify any logical or syntax errors in the pipeline code. Inspect variables, log intermediate results, and apply step-by-step debugging if necessary.

* Monitor Resources: Monitor resource utilization (CPU, memory, disk I/O) during pipeline execution to identify any resource bottlenecks.

* Review Documentation: Consult the pipeline documentation, code comments, and any relevant documentation of the tools and technologies used in the pipeline for insights into common issues and troubleshooting tips.

* Seek Support: If the issue persists, reach out to relevant support channels, such as community forums or official documentation, to seek assistance from the community or the tool's maintainers.

  
# ETL Pipeline Documentation

This document provides an overview of the ETL (Extract, Transform, Load) pipeline for processing blockchain transaction data from the Solana Blockchain. It includes explanations of the pipeline's functionality, decisions made during development, instructions for running the pipeline, and strategies for collaboration with data science and business teams.

## 1. ETL Pipeline Overview

The ETL pipeline is designed to extract transaction data from the Solana Blockchain, apply transformations based on specific business rules, and load the transformed data into a PostgreSQL database. The pipeline consists of three main stages: Extraction, Transformation, and Loading.

- **Extraction**: The extraction stage involves retrieving transaction data from the Solana Blockchain. The extract_data.py script connects to the Solana Blockchain API, retrieves the latest block hash (update: or block data for a given slot ('get_block(slot)'), extracts addresses from the block hash, and prints the unique addresses involved in the transactions ('get_latest_blockhash()').

- **Transformation**: The transformation stage applies business rules to the extracted data. It involves two components:
    - DBT Transformation: The transformation logic is defined in the transformation.sql file located in the models/transform directory. It applies specific rules such as filtering data from Magic Eden contracts and excluding records older than two years. To run the transformation, execute the following command: `dbt run --models transform`.
    - Python Script Transformation: The Python script filters out transaction records older than two years and inserts the filtered transactions into a specified PostgreSQL database table.
- **Loading**: The loading stage involves loading the transformed data into a PostgreSQL database. The transformed data is written to the transformed_addresses table in the myschema schema.

## 2. Decisions Made

During the development of the ETL pipeline, the following decisions were made:

- Choice of Technologies: The pipeline utilizes Python, PostgreSQL, Spark, and DBT. Python is used for data extraction, transformation, and loading. PostgreSQL is used as the database for storing the transformed data. Spark is used for loading the data into the database. DBT is used for applying business rules and transformations.
- Data Filtering Criteria: The decision was made to filter out transaction records older than two years during the transformation stage. This criterion can be adjusted as per specific requirements.
- Integration with PostgreSQL and Spark: The ETL pipeline integrates with a PostgreSQL database for data storage. It establishes a connection to the database and inserts filtered transaction records into the specified table using Spark.
- Code Organization: The pipeline code is organized into separate scripts and directories based on their functionalities. This separation enhances maintainability and allows for easy customization and troubleshooting.

## 3. Running the ETL Pipeline

To run the ETL pipeline, follow these steps:

- Clone the Repository: Clone the repository to your local machine using the following command: `git clone https://github.com/shahupdates/etldatapipelinecasestudy`.
- Navigate to the Project Directory: Open a terminal and navigate to the project directory using the following command: `cd etlpipeline`.
- Install Dependencies: Install the required Python dependencies by running the following command: `pip install -r requirements.txt`.
- Configure PostgreSQL Connection: Open the profiles.yml file located in the .dbt directory. Modify the dev section with your PostgreSQL credentials:

```yaml
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

- Extraction: Run the extraction script by executing the following command: `python extract_data.py`.
- Transformation: Apply the transformations using DBT by running the following command: `dbt run --models transform`.
- Loading: Load the transformed data into the PostgreSQL database using Spark by executing the following command: `dbt run --models transform`.

## 4. Collaboration with Data Science and Business Teams

To collaborate with data science and business teams and adjust the ETL pipeline to meet their needs, the following strategies can be employed:

- Regular Meetings: Schedule regular meetings with data science and business teams to understand their data requirements, discuss any issues or challenges they face, and gather feedback on the existing ETL pipeline.
- Requirement Gathering: Engage in thorough requirement gathering sessions to capture the specific data needs of the teams. This includes understanding the desired data formats, frequency of updates, desired transformations, and any specific business rules to be applied.
- Flexibility and Customization: Design the ETL pipeline to be flexible and customizable to accommodate different data requirements. Use configuration files, command-line arguments, or environment variables to adjust pipeline settings and behavior.
- Iterative Development: Adopt an iterative development approach to incorporate feedback and address evolving needs. Break down the pipeline into smaller modules or stages that can be independently developed, tested, and deployed. This allows for incremental improvements and easier maintenance.
- Documentation and Knowledge Sharing: Maintain comprehensive documentation that explains the pipeline's functionalities, data sources, transformations, and database schema. Share this documentation with the data science and business teams to ensure a common understanding of the pipeline's capabilities and limitations.

## 5. Performance Optimization

To optimize the performance of the ETL pipeline, consider the following potential bottlenecks and corresponding solutions:

- Data Extraction: If data extraction from the Solana Blockchain API is slow, optimize the API calls by implementing caching mechanisms, batching requests, or exploring alternative API endpoints with higher throughput.
- Transformation Logic: If the transformation stage is time-consuming, analyze the SQL queries and transformations in the DBT models. Ensure efficient indexing, minimize unnecessary computations, and utilize parallel processing where applicable.
- Database Performance: If the database loading process is slow, optimize the PostgreSQL database configuration, including appropriate indexing, partitioning, and clustering strategies. Consider optimizing Spark configurations for better data loading performance.
- Hardware and Resources: Assess the hardware resources available for running the ETL pipeline. Consider scaling up hardware resources, such as increasing CPU cores, memory, or utilizing distributed computing environments, to handle larger datasets and improve overall performance.
- Parallelization and Scaling: Explore parallel processing techniques, such as distributing workload across multiple machines or utilizing multi-threading, to improve the speed of data extraction, transformation, and loading stages.
- Monitoring and Profiling: Implement monitoring and profiling mechanisms to identify performance bottlenecks. Measure and analyze execution times for each stage and component of the pipeline. Use profiling tools to identify specific areas for optimization.

## 6. Troubleshooting Guide

If the ETL pipeline fails during the transformation stage, follow these troubleshooting steps:

- Check Log and Error Messages: Review the error messages or logs generated during the pipeline execution. Identify any specific error messages or exceptions that provide insights into the cause of the failure.
- Verify Data Inputs: Ensure that the data inputs, such as the latest block hash or API responses, are valid and accessible. Verify the availability and consistency of data sources.
- Review Transformation Logic: Examine the transformation logic implemented in the DBT models or Python scripts. Verify the correctness of the applied business rules, filtering criteria, and data manipulation operations.
- Validate Database Configuration: Validate the PostgreSQL database configuration, including the connection parameters, access privileges, and table schema. Ensure the necessary permissions are granted for executing transformations and loading data.
- Test with Sample Data: Test the ETL pipeline with a small sample of data to isolate the issue and identify the specific step or component causing the failure. Use dummy data or subsets of the original dataset for debugging purposes.
- Enable Debugging and Logging: Enable additional debugging and logging mechanisms within the pipeline code to capture more detailed information about the intermediate steps, data transformations, and database interactions.
- Seek Expert Assistance: If the troubleshooting steps do not resolve the issue, seek assistance from experienced developers or database administrators who can provide insights and guidance in resolving the problem.

By following these troubleshooting steps and systematically identifying the root cause of the failure, it is possible to resolve issues and ensure the smooth execution of the ETL pipeline.

# Summary

This document has provided an overview of the ETL pipeline for processing blockchain transaction data from the Solana Blockchain. It explained the pipeline's functionality, discussed decisions made during development, provided instructions for running the pipeline, discussed strategies for collaboration with data science and business teams, proposed solutions for optimizing performance bottlenecks, and outlined a troubleshooting guide. By following this documentation, users can effectively understand, run, and maintain the ETL pipeline while addressing data needs and achieving optimal performance.
