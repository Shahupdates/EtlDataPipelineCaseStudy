from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number, to_timestamp
from pyspark.sql.window import Window

class SparkOperations:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("Solana ETL") \
            .config("spark.jars", "postgresql-42.6.0.jar") \
            .getOrCreate()

        self.jdbcUrl = "jdbc:postgresql://localhost/main_database"
        self.table = "public.transactions"
        self.properties = {"user": "postgres", "password": "postgres", "driver": "org.postgresql.Driver"}

    def load_data(self, data):
        df = self.spark.createDataFrame(data, ["address", "amount", "amount_sol", "timestamp"])

        df = df.withColumn("timestamp", to_timestamp(col("timestamp")))

        window = Window.partitionBy("address", "timestamp").orderBy(col("amount").desc())
        deduplicated_df = df.withColumn("row_number", row_number().over(window)).where(col("row_number") == 1).drop("row_number")

        deduplicated_df.write.jdbc(url=self.jdbcUrl, table=self.table, mode="append", properties=self.properties)
        print('Data loaded successfully.')

        return deduplicated_df

    def calculate_dau(self, df):
        df.createOrReplaceTempView("transactions")
        dau = self.spark.sql("""
            SELECT
                date(timestamp) AS date,
                count(distinct address) AS dau
            FROM transactions
            GROUP BY date(timestamp)
        """)
        dau.write.jdbc(url=self.jdbcUrl, table="public.daily_active_users", mode="overwrite", properties=self.properties)
        print('Daily active users data loaded successfully.')

    def calculate_daily_transaction_volume(self, df):
        df.createOrReplaceTempView("transactions")
        daily_tx_volume = self.spark.sql("""
            SELECT
                date(timestamp) AS date,
                sum(amount_sol) AS daily_tx_volume
            FROM transactions
            GROUP BY date(timestamp)
        """)
        daily_tx_volume.write.jdbc(url=self.jdbcUrl, table="public.daily_transaction_volume", mode="overwrite", properties=self.properties)
        print('Daily transaction volume data loaded successfully.')

    def run_dbt_transformation(self):
        command = "dbt run --models +transformations.transform_data"
        subprocess.run(command, shell=True)

    def stop_spark(self):
        self.spark.stop()
