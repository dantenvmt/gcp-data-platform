from pyspark.sql import SparkSession
from pyspark.sql import functions as F

PROJECT = "project-60776627-9a3f-49ac-9b1"
BUCKET = "project-60776627-9a3f-49ac-9b1-raw"
INPUT_PATH = f"gs://{BUCKET}/taxi/yellow/year=2023/month=*/*.parquet"
OUTPUT_TABLE = f"{PROJECT}.raw.trips_by_hour"


spark = SparkSession.builder.appName("taxi-clean-aggregate").getOrCreate()
spark.conf.set("spark.sql.parquet.enableVectorizedReader", "false")

# The columns we actually use, each cast to a fixed type so every month matches.
SELECTED = [
    F.col("tpep_pickup_datetime").cast("timestamp").alias("tpep_pickup_datetime"),
    F.col("tpep_dropoff_datetime").cast("timestamp").alias("tpep_dropoff_datetime"),
    F.col("passenger_count").cast("double").alias("passenger_count"),
    F.col("trip_distance").cast("double").alias("trip_distance"),
    F.col("fare_amount").cast("double").alias("fare_amount"),
    F.col("tip_amount").cast("double").alias("tip_amount"),
    F.col("total_amount").cast("double").alias("total_amount"),
]

months = ["01", "02", "03"]
trips = None
for m in months:
    path = f"gs://{BUCKET}/taxi/yellow/year=2023/month={m}/*.parquet"
    df = spark.read.parquet(path).select(*SELECTED)   # read 1 month, keep+cast our 7 columns
    trips = df if trips is None else trips.union(df)   # stack onto the running total

print("Raw rows:", trips.count())

clean = trips.filter( (F.col("fare_amount") > 0) 
             & (F.col("trip_distance") > 0) & (F.col("trip_distance") < 100) 
             & (F.col("passenger_count")> 0 ) 
             & (F.col("total_amount") > 0)
             & (F.col("tpep_dropoff_datetime") > F.col("tpep_pickup_datetime"))
             & (F.col("tpep_pickup_datetime") >= "2023-01-01")
             & (F.col("tpep_pickup_datetime") < "2023-04-01")
)

enriched = clean.withColumn('pickup_date', F.to_date("tpep_pickup_datetime")).withColumn('pickup_hour', F.hour('tpep_pickup_datetime'))


summary = enriched.groupby('pickup_date', 'pickup_hour').agg(
    F.count("*").alias("trip_count"),
    F.round(F.avg("fare_amount"),2).alias("avg_fare"),
    F.round(F.avg("tip_amount"),2).alias("avg_tip"),
    F.round(F.avg("trip_distance"),2).alias("avg_distance"),
    F.round(F.avg(F.col("tip_amount")/F.col("fare_amount") *100),2).alias("avg_tip_pct")
)

summary.write.format("bigquery").option("table", OUTPUT_TABLE).option("writeMethod", "direct").mode("overwrite").save()
spark.stop()