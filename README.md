# GCP Modern Data Platform

An end-to-end batch data platform on Google Cloud, built to turn a public, billion-row
dataset (NYC TLC taxi trips) into an analytics-ready warehouse and dashboard. Every layer
is infrastructure-as-code and reproducible from a clean clone.

> **Status:** complete — built milestone by milestone as a hands-on study of the modern data stack.

## Architecture

```
  Terraform  (provisions all GCP resources)

  NYC taxi + weather  ->  GCS (raw Parquet)  ->  Dataproc Serverless (PySpark)
                                                        |
                                                        v
                                          BigQuery  (raw -> staging -> marts)
                                                        |
                                                        v
                                          dbt  (transforms + tests + lineage)
                                                        |
                                          Airflow orchestrates the pipeline
                                                        |
                                                        v
                                          Looker Studio dashboard

  CI: GitHub Actions runs dbt tests on every pull request
```

## Tech stack

| Layer | Tool |
|-------|------|
| Infrastructure as code | Terraform |
| Storage | Google Cloud Storage (Parquet) |
| Big-data compute | Dataproc Serverless + PySpark |
| Warehouse | BigQuery |
| Transformations | dbt Core |
| Orchestration | Apache Airflow (Docker) |
| CI/CD | GitHub Actions |
| BI | Looker Studio |

## Roadmap

- [x] **M1** — Infrastructure as code (Terraform): GCS bucket, BigQuery datasets, service account
- [x] **M2** — Ingestion: land a slice of the source data as Parquet in GCS
- [x] **M3** — Big-data compute: PySpark on Dataproc Serverless into BigQuery
- [x] **M4** — Transformations: dbt models, tests, and lineage
- [x] **M5** — Orchestration: an Airflow DAG running the full pipeline
- [x] **M6** — CI (keyless dbt tests via WIF), Looker Studio dashboard, and writeup

## Running the infrastructure

Requires the [gcloud CLI](https://cloud.google.com/sdk) (authenticated) and
[Terraform](https://developer.hashicorp.com/terraform).

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars   # then set your project_id
terraform init
terraform plan
terraform apply
```

`terraform destroy` tears everything back down to zero.
