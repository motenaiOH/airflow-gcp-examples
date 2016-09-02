
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

from airflow import DAG

from datetime import timedelta, datetime

seven_days_ago = datetime.combine(datetime.today() - timedelta(7),
                                  datetime.min.time())

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': seven_days_ago,
    'email': ['alex@vanboxel.be'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=30),
}

with DAG('gcp_smoke_bq', schedule_interval=timedelta(days=1),
         default_args=default_args) as dag:

    bq_exec_copy_year = BigQueryOperator(
        task_id='bq_exec_copy_year',
        bql='gcp_smoke/noaa_gsod_shift_10y.sql',
        destination_dataset_table='{{var.value.gcp_smoke_dataset}}.noaa_gsod_y{{ ds_nodash }}',
        write_disposition='WRITE_TRUNCATE',
        bigquery_conn_id='gcp_default'
    )
