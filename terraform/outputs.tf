output "raw_bucket" {
  value = google_storage_bucket.raw.name
}

output "datasets" {
  value = [
    google_bigquery_dataset.raw.dataset_id,
    google_bigquery_dataset.staging.dataset_id,
    google_bigquery_dataset.marts.dataset_id,
  ]
}

output "pipeline_service_account" {
  value = google_service_account.pipeline-runner.email
}
