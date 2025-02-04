from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
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

    # Task 2: Run transform dbt
    run_transform_dbt = BashOperator(task_id='run_transform_dbt', bash_command='cd /path/to/your/dbt/project && dbt run --models your_model_name')

    # Define task order
    run_extract_python >> run_transform_dbt