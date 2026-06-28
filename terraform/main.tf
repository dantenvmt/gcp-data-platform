terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"   # the official GCP provider plugin
      version = "~> 6.0"             # use any 6.x version
    }
  }
}

provider "google" {
  project = var.project_id   # which project to build in (from a variable)
  region  = var.region       # default region for resources
}

resource "google_storage_bucket" "raw" {
    name = "${var.project_id}-raw"
    location = var.region
    uniform_bucket_level_access = true
    force_destroy = true
}


resource "google_bigquery_dataset" "raw" {
    dataset_id = "raw"
    location = var.region
}

resource "google_bigquery_dataset" "staging" {
    dataset_id = "staging"
    location = var.region
}

resource "google_bigquery_dataset" "marts" {
    dataset_id = "marts"
    location = var.region
}
resource "google_service_account" "pipeline-runner" {
    account_id = "pipeline-runner"
    display_name = "Pipeline runner SA"
}