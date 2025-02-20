# Import Airflow libraries, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator
from datetime import datetime, timedelta

# Define arguments, such as retry frequency
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

# Define the actual DAG
# Runs once an hour
with DAG(
    dag_id='run_extract_fmi_aq',
    default_args=default_args,
    description='Run a Python script to extract FMI air quality data and save to Snowflake raw layer.',
    schedule_interval='0 */12 * * *', 
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:
    
    # Task 1: Run extract Python-script
    run_extract_python = BashOperator(
        task_id='run_extract_python',
        bash_command="python /Users/timosarkka/Projects/finnish-air-quality/extract/fmi_aq_ingest_daily.py",  
        cwd="/Users/timosarkka/Projects/finnish-air-quality/extract"  
    )

    # Task 2: Run a dbt job
    run_dbt_job = DbtCloudRunJobOperator(
        task_id='run_dbt_job',
        job_id=12345,
        account_id=67890,
        wait_for_completion=True
    )
    
    # Set task dependencies
    run_extract_python >> run_dbt_job
