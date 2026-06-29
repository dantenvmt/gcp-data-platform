locals {
    pipeline_sa = "serviceAccount:${google_service_account.pipeline-runner.email}"
}

resource "google_project_iam_member" "sa_dataproc_worker" {
    project = var.project_id
    role = "roles/dataproc.worker"
    member = local.pipeline_sa
}

resource "google_project_iam_member" "sa_bq_data_editor" {
    project = var.project_id
    role    = "roles/bigquery.dataEditor"
    member  = local.pipeline_sa
}

resource "google_project_iam_member" "sa_bq_job_user" {
    project = var.project_id
    role    = "roles/bigquery.jobUser"
    member  = local.pipeline_sa
}
resource "google_storage_bucket_iam_member" "sa_bucket_object_admin" {
    bucket = google_storage_bucket.raw.name
    role   = "roles/storage.objectAdmin"
    member = local.pipeline_sa
}