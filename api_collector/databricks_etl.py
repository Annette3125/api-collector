import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean


# Create session

spark = SparkSession.builder \
    .appName("StockDataETL") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# specify input file

input_path = "data/new/stock_data_latest.csv"
output_path = "data/processed"

# read csv

df = spark.read.option("header", True).csv(input_path, inferSchema=True)

print("Original data:")
df.show(5)

# filter only valid values
clean_df = df.filter(
    (col("open") >= 0) &
    (col("high") >= 0) &
    (col("low") >= 0) &
    (col("close") >= 0)
)

# count average price per day

result_df = clean_df.withColumn(
"avg_price", (col("open") + col("high") + col("low") + col("close")) / 4
)

# group by symbol

agg_df = result_df.groupBy("symbol").agg(mean("avg_price").alias("mean_price"))

print(" Aggregated results:")
agg_df.show()

# save Parquet format
os.makedirs(output_path, exist_ok=True)
agg_df.write.mode("overwrite").parquet(output_path + "stock_summary.parquet")

print("Saved processed data to:", output_path)

spark.stop()

