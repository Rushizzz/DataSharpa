"""
Sample Airflow DAG for DataSherpa
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline_daily',
    default_args=default_args,
    description='Daily data processing pipeline',
    schedule_interval='0 2 * * *',
    catchup=False,
    tags=['production', 'data-pipeline'],
)

def validate_input_data(**context):
    """Validate input data before processing"""
    # Add validation logic
    print("Validating input data...")
    return True

def send_completion_notification(**context):
    """Send notification on pipeline completion"""
    print("Pipeline completed successfully")

# Task 1: Validate input
validate_task = PythonOperator(
    task_id='validate_input',
    python_callable=validate_input_data,
    dag=dag,
)

# Task 2: Run Spark job
spark_task = SparkSubmitOperator(
    task_id='run_spark_pipeline',
    application='/path/to/sample_pipeline.py',
    conf={
        'spark.executor.memory': '8g',
        'spark.executor.cores': '4',
        'spark.sql.shuffle.partitions': '200',
    },
    dag=dag,
)

# Task 3: Send notification
notify_task = PythonOperator(
    task_id='send_notification',
    python_callable=send_completion_notification,
    dag=dag,
)

# Define task dependencies
validate_task >> spark_task >> notify_task
