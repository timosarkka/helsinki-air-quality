from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='run_extract_and_transform',
    default_args=default_args,
    description='Run a Python script to extract FMI air quality data. Run a dbt to transform data from raw to analytics schema.',
    schedule_interval='0 */6 * * *', 
    start_date=datetime(2025, 2, 4),
    catchup=False
) as dag:
    
    # Task 1: Run extract Python-script
    run_extract_python = BashOperator(task_id='run_extract_python', bash_command='python ../extract/fmi_aq_ingest_daily.py')

    # Task 2: Run transform in dbt Cloud
    run_dbt_cloud_job = DbtCloudRunJobOperator(
        task_id='run_dbt_cloud',
        job_id='',  # Replace with your actual dbt Cloud Job ID
        check_interval=10,
        timeout=300
    )

    # Define task order
    run_extract_python >> run_dbt_cloud_job