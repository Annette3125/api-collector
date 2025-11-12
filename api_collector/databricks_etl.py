import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean


def run_spark_etl(input_path: str, output_path: str) -> None:
    """Mini ETL job that reads CSV, cleans data and saves Parquet summary."""
    spark = (
        SparkSession.builder.appName("StockDataETL")
        .config("spark.driver.memory", "2g")
        .getOrCreate()
    )

    if not os.path.exists(input_path):
        print(f"[WARN] Input not found: {input_path}")
        return

    df = spark.read.option("header", True).csv(input_path, inferSchema=True)
    print("Original data:")
    df.show(5)

    clean_df = df.filter(
        (col("open") >= 0)
        & (col("high") >= 0)
        & (col("low") >= 0)
        & (col("close") >= 0)
    )

    result_df = clean_df.withColumn(
        "avg_price", (col("open") + col("high") + col("low") + col("close")) / 4
    )

    agg_df = result_df.groupBy("symbol").agg(mean("avg_price").alias("mean_price"))

    print("Aggregated results:")
    agg_df.show()

    os.makedirs(output_path, exist_ok=True)
    agg_df.write.mode("overwrite").parquet(
        os.path.join(output_path, "stock_summary.parquet")
    )

    print(f"Saved processed data to: {output_path}")
    spark.stop()


if __name__ == "__main__":
    input_path = "data/new/stock_data_latest.csv"
    output_path = "data/processed"
    run_spark_etl(input_path, output_path)
