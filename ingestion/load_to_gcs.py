import requests
from google.cloud import storage

BUCKET = "project-60776627-9a3f-49ac-9b1-raw"
MONTHS = [("2023", "01"), ("2023", "02"), ("2023", "03")]
SOURCE = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month}.parquet"

client = storage.Client()

for year, month in MONTHS:
    resp = requests.get(SOURCE.format(year=year, month=month))
    resp.raise_for_status()
    dest_path = f"taxi/yellow/year={year}/month={month}/yellow_tripdata_{year}-{month}.parquet"
    blob = client.bucket(BUCKET).blob(dest_path)
    blob.upload_from_string(resp.content, content_type="application/octet-stream")
    size_mb = len(resp.content) / 1024 / 1024
    print(f"uploaded {year}-{month} -> {dest_path} ({size_mb:.1f} MB)")