from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from tasks.load_data import scrape_data
from tasks.clean_scopus import clean_data


default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 5, 8),
    "retries": 1,
}

dag = DAG(
    "airflow_dag",
    default_args=default_args,
    description="A simple DAG to collect data from IEEE",
    schedule_interval=timedelta(days=1),
)

load_data = PythonOperator(
    task_id="load_data",
    python_callable=scrape_data,
    dag=dag,
)

clean_scopus = PythonOperator(
    task_id="clean_scopus",
    python_callable=clean_data,
    dag=dag,
)


load_data >> clean_scopus
