import datetime 
from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
from airflow.operators.bash import BashOperator

with DAG(
    dag_id = "taxi_pipeline",
    start_date = datetime.datetime(2024,1,1),
    schedule = None,
    catchup = False,
) as dag:
    spark_transform = DataprocCreateBatchOperator(
        task_id="spark_transform",
        project_id="project-60776627-9a3f-49ac-9b1",
        region='us-central1',
        batch_id = "taxi-transform-{{ ts_nodash | lower}}",
        batch = {
            "pyspark_batch" : { "main_python_file_uri": "gs://project-60776627-9a3f-49ac-9b1-raw/code/transform.py"},
            "runtime_config": {"version": "2.2"},
            "environment_config" : {"execution_config" : {"service_account" : "pipeline-runner@project-60776627-9a3f-49ac-9b1.iam.gserviceaccount.com"}}
        }
    )
    dbt_build = BashOperator(
        task_id = 'dbt_build',
        bash_command = '/opt/airflow/dbt-venv/bin/dbt --no-partial-parse build --project-dir /opt/airflow/dbt  --profiles-dir /opt/airflow/dbt '
    )
    spark_transform >> dbt_build