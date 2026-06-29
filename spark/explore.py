import pandas as pd

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
df = pd.read_parquet(url)

print("ROWS, COLUMNS:", df.shape)
print("\nCOLUMN NAMES + TYPES:")
print(df.dtypes)
print("\nFIRST 3 ROWS:")
print(df.head(3).to_string())

print("\nQUICK STATS on key numeric columns:")
print(df[["passenger_count", "trip_distance", "fare_amount", "tip_amount", "total_amount"]].describe().to_string())