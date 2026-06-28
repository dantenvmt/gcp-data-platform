# GCP Modern Data Stack — Learning Project Design

**Date:** 2026-06-28
**Owner:** Thuan Nguyen
**Type:** Learning project + portfolio artifact (equally weighted)

## Purpose

Build an end-to-end batch data platform on Google Cloud to (1) genuinely learn cloud
stacks and big-data tooling hands-on, and (2) produce a public, recruiter-facing
portfolio piece linked from the personal portfolio site. Targets Data Analyst /
Data Scientist roles.

This is a **guided learning** project. Claude acts as tutor/mentor, not autopilot:
explain the concept, assign the task, the user writes the code, Claude reviews and
explains the why. Claude writes code only for scaffolding/reference or when the user
is truly stuck.

## Constraints & decisions

- **Cloud:** GCP + BigQuery (user already has Azure experience; adding GCP).
- **Data:** Public mega-dataset — NYC TLC taxi trips (1B+ rows) enriched with the
  public weather dataset (multi-source join).
- **Scope:** Full modern data stack, ~3-5 weeks.
- **Budget:** GCP $300 / 90-day free-trial credit; design to stay ~$0. Budget alerts
  set up in Milestone 0. Airflow runs locally in Docker (free) instead of Cloud
  Composer (~$300/mo).

## Architecture

```
                    Terraform (provisions all GCP resources)

  PUBLIC SOURCE        INGEST           BIG-DATA COMPUTE        WAREHOUSE
  NYC taxi + weather → GCS (raw      → Dataproc Serverless  → BigQuery (raw)
  (BQ public data)     Parquet)        PySpark: clean+agg        │
                                                                 ▼
                                              dbt (staging → intermediate → marts)
                                                   + tests + docs/lineage
                                                                 │
                    Airflow DAG orchestrates the full chain ─────┤
                                                                 ▼
                                              Looker Studio dashboard
                                              (linked from portfolio site)

  CI: GitHub Actions runs dbt build + tests on every PR
```

**Flow:** Terraform stands up infra → public data slice lands in GCS as Parquet →
Dataproc Serverless PySpark cleans/aggregates (big-data compute) → results land in
BigQuery `raw` → dbt transforms `raw → staging → marts` with tests + lineage →
Airflow orchestrates the chain on a schedule → Looker Studio reads the marts →
GitHub Actions tests on every PR.

## Repo structure

```
gcp-data-platform/
├── README.md              architecture diagram + project story
├── terraform/             IaC: GCS bucket, BQ datasets, Dataproc, IAM
├── ingestion/             land public data → GCS as Parquet
├── spark/                 PySpark job for Dataproc Serverless
├── dbt/                   staging → intermediate → marts, tests, docs
├── airflow/
│   ├── docker-compose.yaml
│   └── dags/              one DAG orchestrating the full pipeline
├── .github/workflows/     CI: dbt build + tests on every PR
└── docs/                  notes, decisions, screenshots, this spec
```

## Components (each has one job)

| Component | Role | Skills learned |
|-----------|------|----------------|
| Terraform | Declare all GCP resources as code | IaC, providers, state, plan/apply |
| GCS + ingestion | Land raw data as Parquet | object storage, Parquet, partitioning |
| Dataproc PySpark | Distributed clean/aggregate | Spark, serverless big-data compute |
| BigQuery | Warehouse (raw→marts) | partitioning, clustering, cost control |
| dbt | SQL transforms + tests + lineage | analytics engineering core |
| Airflow (local Docker) | Orchestrate the DAG | dependencies, scheduling, operators |
| GitHub Actions | Test on every PR | CI/CD for data |
| Looker Studio | Dashboard on marts | BI delivery |

## Working rhythm (per layer)

1. Claude teaches the concept (short, focused — why it exists, how it fits).
2. Claude assigns a concrete task with instructions + docs links.
3. User writes the code; asks questions mid-way.
4. Claude reviews, points out issues, explains the why behind fixes.
5. Checkpoint: confirm it runs, commit, move on.

## Build order & milestones (~1 milestone per 3-5 days)

- **M0 — Foundations (Day 1-2):** GCP account + free-trial billing + budget alerts,
  install toolbelt (gcloud, terraform, dbt, Docker, Python), create + push GitHub repo.
  *Done when:* gcloud authenticated, empty repo pushed.
- **M1 — Infra as code:** Terraform for GCS bucket + BQ datasets (raw/staging/marts) +
  IAM. *Done when:* `terraform apply` creates resources, `terraform destroy` cleans up.
- **M2 — Ingestion → GCS:** script lands a slice of NYC taxi + weather as partitioned
  Parquet. *Done when:* Parquet files exist in the bucket.
- **M3 — Big-data compute (Dataproc + PySpark):** PySpark job cleans/aggregates raw
  Parquet → BigQuery `raw`. *Done when:* Dataproc Serverless batch succeeds, `raw`
  tables populated. **Headline big-data milestone.**
- **M4 — Transformations (dbt):** models build staging→intermediate→marts with tests
  (not-null, unique, relationships) + docs/lineage. *Done when:* `dbt build` passes,
  `dbt docs` renders lineage.
- **M5 — Orchestration (Airflow):** local Docker DAG runs Dataproc → dbt end-to-end.
  *Done when:* one DAG run executes the full pipeline green.
- **M6 — CI + Dashboard + Writeup:** GitHub Actions runs dbt tests on PRs; Looker
  Studio dashboard on the marts; README with architecture diagram + story; link from
  portfolio site. *Done when:* CI green on a PR, dashboard live, repo linked.

## Success criteria

- Full pipeline runs end-to-end reproducibly (public data → dashboard).
- Everything is infra-as-code (clone + `terraform apply` + run).
- User can explain every component and its trade-offs in an interview (the real goal).
- Costs stayed within the free-trial credit.
- Public GitHub repo with recruiter-readable README, linked from portfolio site.

## Out of scope (YAGNI)

- Streaming/real-time (batch only).
- Cloud Composer / managed Airflow (cost).
- Custom ingestion of a live growing source (using a ready public dataset instead).
- Multi-cloud (GCP only; Azure already covered elsewhere).
