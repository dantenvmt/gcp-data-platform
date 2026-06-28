# GCP Modern Data Stack — Guided Learning Plan

> **Working mode:** GUIDED LEARNING, not autopilot. For each task: Claude teaches the
> concept → assigns the hands-on task → **Thuan writes the code** → Claude reviews and
> explains the why → checkpoint + commit. Claude writes code only for short reference
> snippets or when Thuan is truly stuck. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible, end-to-end batch data platform on GCP (public data →
dashboard) while learning each layer of the modern data stack hands-on.

**Architecture:** Terraform provisions GCP infra; a slice of NYC TLC taxi + weather data
lands in GCS as Parquet; a Dataproc Serverless PySpark job cleans/aggregates it into
BigQuery; dbt transforms raw→staging→marts with tests + lineage; Airflow (local Docker)
orchestrates the chain; GitHub Actions runs dbt tests on PRs; Looker Studio serves a
dashboard linked from the portfolio site.

**Tech Stack:** GCP (BigQuery, GCS, Dataproc Serverless, IAM), Terraform, Python, PySpark,
dbt Core, Apache Airflow (Docker), GitHub Actions, Looker Studio.

## Global Constraints

- Budget: stay within GCP $300 / 90-day free-trial credit; target ~$0. Budget alert set in M0.
- Airflow runs LOCALLY in Docker (never Cloud Composer — cost).
- Everything reproducible as infra-as-code: clone + `terraform apply` + run.
- Region: pin a single region (e.g. `us-central1`) everywhere to avoid egress + keep public-dataset joins cheap.
- BigQuery cost control: always partition + cluster large tables; never `SELECT *` on raw taxi data.
- Real learning goal: Thuan must be able to explain every component and its trade-offs.
- Commit after every working checkpoint; small, frequent commits.

---

## Milestone 0 — Foundations (Day 1-2)

**Deliverable:** Authenticated GCP + local toolbelt + pushed GitHub repo with a budget guardrail.

### Task 0.1: GCP account, project, billing + budget alert
**Concept Claude teaches:** GCP project/billing model, why free-trial ≠ auto-charge, budget alerts.
- [ ] Create a GCP account, start the $300 free trial.
- [ ] Create a project `gcp-data-platform` (note the project ID).
- [ ] Set a budget of $20 with email alerts at 50/90/100% (guardrail; we expect ~$0).
- [ ] Enable APIs: BigQuery, Cloud Storage, Dataproc, IAM.
- [ ] **Verify:** project visible in console, budget alert listed, APIs enabled.
- [ ] **Checkpoint with Claude** before moving on.

### Task 0.2: Local toolbelt
**Concept Claude teaches:** what each CLI is for; auth via `gcloud auth application-default login`.
- [ ] Install: `gcloud` CLI, `terraform`, `python`/`uv` or `conda`, Docker Desktop, `dbt-bigquery`.
- [ ] Run `gcloud auth login` and `gcloud auth application-default login`.
- [ ] Set default project: `gcloud config set project <PROJECT_ID>`.
- [ ] **Verify:** `gcloud config list`, `terraform -version`, `docker run hello-world`, `dbt --version` all succeed.

### Task 0.3: Create + push the repo
**Concept Claude teaches:** repo hygiene, `.gitignore` for secrets/state, README as the portfolio front door.
- [ ] `git init` the `gcp-data-platform/` folder; add a `.gitignore` (Terraform state, creds, `.env`, dbt target/).
- [ ] Write a starter `README.md` (one paragraph: what this project is + the architecture diagram).
- [ ] Create the GitHub repo and push.
- [ ] **Commit the spec + this plan** (already in `docs/`).
- [ ] **Verify:** repo is public on GitHub, no secrets committed.

---

## Milestone 1 — Infra as Code with Terraform

**Deliverable:** `terraform apply` creates a GCS bucket + 3 BigQuery datasets + a service account; `terraform destroy` removes them.

### Task 1.1: Terraform skeleton + provider
**Concept Claude teaches:** providers, `init/plan/apply/destroy`, remote vs local state (we use local for now).
- [ ] Create `terraform/main.tf`, `variables.tf`, `outputs.tf`.
- [ ] Configure the `google` provider with `project` + `region` variables.
- [ ] **Verify:** `terraform init` succeeds.

### Task 1.2: Define resources
**Concept Claude teaches:** resource blocks, naming, why datasets are layered (raw/staging/marts).
- [ ] GCS bucket (uniform access, the pinned region).
- [ ] BigQuery datasets: `raw`, `staging`, `marts`.
- [ ] A service account for pipeline jobs + minimal IAM roles.
- [ ] Wire useful `outputs` (bucket name, dataset ids).
- [ ] **Verify:** `terraform plan` shows the expected adds, then `terraform apply`.

### Task 1.3: Prove reproducibility
**Concept Claude teaches:** idempotency, why destroy/apply must be clean.
- [ ] `terraform destroy`, then `terraform apply` again.
- [ ] **Verify:** resources reappear identically; **commit** the Terraform.

---

## Milestone 2 — Ingestion → GCS

**Deliverable:** A slice of NYC taxi + weather lands in the bucket as partitioned Parquet.

### Task 2.1: Pull a bounded slice
**Concept Claude teaches:** why bound the slice (cost/scale), Parquet vs CSV, partitioning by date.
- [ ] Write `ingestion/load_to_gcs.py`: query a bounded slice (e.g. a few months of taxi trips) + matching weather, write Parquet to GCS partitioned by date.
- [ ] **Verify:** Parquet objects exist under the expected `gs://.../year=/month=/` paths.
- [ ] **Review with Claude:** schema choices, partition layout, file sizes; **commit**.

---

## Milestone 3 — Big-Data Compute (Dataproc Serverless + PySpark) [HEADLINE]

**Deliverable:** A PySpark batch cleans/aggregates the raw Parquet and writes curated tables to BigQuery `raw`.

### Task 3.1: Write the PySpark job
**Concept Claude teaches:** Spark DataFrame API, lazy eval, partitions/shuffle, narrow vs wide transforms.
- [ ] `spark/transform.py`: read Parquet from GCS, clean (nulls, bad coords, negative fares), join weather, aggregate (e.g. trips + avg fare + tip% by zone/hour/day), write to BigQuery.
- [ ] **Verify locally first** on a tiny sample (Spark local mode) before cloud.

### Task 3.2: Run on Dataproc Serverless
**Concept Claude teaches:** serverless Spark, batch submission, the BigQuery connector, reading the Spark UI/logs.
- [ ] Submit the job as a Dataproc Serverless batch (via `gcloud` or Terraform).
- [ ] **Verify:** batch succeeds; `raw` tables populated; sanity-check row counts in BigQuery.
- [ ] **Review with Claude:** partitioning/clustering of the output tables, cost of the run; **commit**.

---

## Milestone 4 — Transformations (dbt)

**Deliverable:** `dbt build` passes all tests; `dbt docs` renders the lineage graph.

### Task 4.1: dbt project + sources
**Concept Claude teaches:** dbt mental model (refs, sources, materializations), staging conventions.
- [ ] `dbt init` against BigQuery; declare `raw` tables as sources.
- [ ] **Verify:** `dbt debug` connects.

### Task 4.2: Layered models + tests
**Concept Claude teaches:** staging→intermediate→marts, generic tests, why tests are the real value.
- [ ] Build `stg_` models (clean/rename), `int_` models (joins/logic), `mart_` models (analytics-ready facts).
- [ ] Add tests: `not_null`, `unique`, `relationships`, `accepted_values`.
- [ ] **Verify:** `dbt build` green; generate + open `dbt docs` lineage; **commit**.

---

## Milestone 5 — Orchestration (Airflow, local Docker)

**Deliverable:** One Airflow DAG runs the full chain (Dataproc job → dbt) end-to-end, green.

### Task 5.1: Airflow up in Docker
**Concept Claude teaches:** Airflow architecture (scheduler/webserver/executor), DAGs vs tasks, why local.
- [ ] Add `airflow/docker-compose.yaml`; bring Airflow up; mount `dags/`.
- [ ] **Verify:** Airflow UI reachable at localhost.

### Task 5.2: The pipeline DAG
**Concept Claude teaches:** operators, dependencies, idempotent tasks, connections/secrets to GCP.
- [ ] `airflow/dags/pipeline.py`: task to submit the Dataproc batch → task to run dbt → set dependencies.
- [ ] **Verify:** trigger a run; all tasks succeed; **commit**.

---

## Milestone 6 — CI + Dashboard + Writeup

**Deliverable:** Green CI on a PR, a live Looker Studio dashboard, a recruiter-ready README linked from the portfolio.

### Task 6.1: GitHub Actions CI
**Concept Claude teaches:** CI for data, running dbt tests in CI, keyless auth (Workload Identity Federation) vs key.
- [ ] `.github/workflows/dbt-ci.yml`: on PR, run `dbt build`/`dbt test` against a CI target.
- [ ] **Verify:** open a PR; CI runs green.

### Task 6.2: Looker Studio dashboard
**Concept Claude teaches:** BI delivery, connecting to BigQuery marts, designing for a non-technical reader.
- [ ] Build a dashboard on the `mart_` tables (demand by hour/zone, tipping, weather effect).
- [ ] **Verify:** dashboard loads; share link works.

### Task 6.3: Writeup + portfolio link
**Concept Claude teaches:** how to tell the project story for recruiters; what to screenshot.
- [ ] Finish `README.md`: architecture diagram, what/why, how to run, what you learned.
- [ ] Link the repo + dashboard from the portfolio site (`index.html`).
- [ ] Follow portfolio copy rules: no em dashes, no puffery, don't start sentences with "I".
- [ ] **Verify:** a stranger could clone and understand it; **commit + push**.

---

## Self-Review (against the spec)

- **Spec coverage:** Terraform (M1), GCS/Parquet ingestion (M2), Dataproc/PySpark (M3),
  BigQuery warehouse (M1+M3+M4), dbt tests/lineage (M4), Airflow (M5), GitHub Actions (M6.1),
  Looker Studio (M6.2), README + portfolio link (M6.3), budget guardrail (M0). All spec
  components mapped. ✓
- **Success criteria:** end-to-end reproducible (M1-M6), IaC (M1), explainability (teaching
  in every task), free-trial budget (M0 + per-run cost reviews), public repo + link (M6.3). ✓
- **Out of scope respected:** no streaming, no Cloud Composer, no custom live source, GCP-only. ✓
