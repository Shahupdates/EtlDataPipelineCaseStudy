# ETL Pipeline Documentation
This repository contains an ETL (Extract, Transform, Load) pipeline for processing blockchain transaction data from Solana Blockchain. The pipeline extracts data from the blockchain, applies transformation based on business rules, and loads the transformed data into PostgreSQL.
## Prerequisites
Before running the ETL pipeline, ensure that you have the following dependencies installed:

* Python (version X.X.X)
* PostgreSQL (version X.X.X)
* Spark (version X.X.X)


# Setup
1. Clone the repository to your local machine: ``` git clone https://github.com/your-username/etlpipeline.git ```
2. Navigate to the project directory: ``` cd etlpipeline ```

3. Install the required Python dependencies: ``` pip install -r requirements.txt ```

4. Configure the PostgreSQL connection in the profiles.yml file located in the .dbt directory. Modify the dev section with your PostgreSQL credentials:
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

## Extraction
The extraction script extract_data.py retrieves data from the Solana Blockchain. It performs the following steps:

* Connects to the Solana Blockchain API.
* Retrieves the latest block hash.
* Extracts addresses from the block hash.
* Prints the unique addresses.
* To run the extraction script, execute the following command: ``` python extract_data.py ```

## Transformation
The transformation logic is defined in the transformation.sql file located in the models/transform directory. It applies the following business rules:

* Only extracts data from Magic Eden contracts.
* Filters out records older than two years.
* To run the transformation, execute the following command: ``` dbt run --models transform ```

## Loading
The loading process involves loading the transformed data into PostgreSQL using Spark. The transformed data is written to the transformed_addresses table in the myschema schema.

To load the data, execute the following command: ``` dbt run --models transform ```

## Configuration
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

## Additional Information
For more details on the ETL pipeline, refer to the individual code files and SQL queries. Feel free to explore and customize the pipeline according to your specific requirements.

```
extract_data.py
models/transform/transformation.sql
dbt_project.yml
```

## License
Read License.txt for license information and proper usage.
