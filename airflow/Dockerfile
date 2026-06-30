# Custom Airflow image.
# - Adds the Google provider so the DAG can submit Dataproc batches.
# - Installs dbt in a SEPARATE virtualenv so dbt's dependencies can't clash with Airflow's.
FROM apache/airflow:2.10.4-python3.11

# Google provider, pinned via Airflow's official constraints (prevents version conflicts).
RUN pip install --no-cache-dir "apache-airflow-providers-google" \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.4/constraints-3.11.txt"

# dbt lives in its own isolated environment, separate from Airflow's Python.
RUN python -m venv /opt/airflow/dbt-venv \
    && /opt/airflow/dbt-venv/bin/pip install --no-cache-dir dbt-bigquery
