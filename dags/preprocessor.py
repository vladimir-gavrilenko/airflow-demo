from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 10, 8, 15, 45),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}

dag = DAG('preprocessor_dag', default_args=default_args, schedule_interval='*/5 * * * *')

execution_date = '{{ execution_date.strftime("%Y-%m-%d-%H-%M") }}'

input_dir = '/home/vladimir/Repos/github/airflow-demo/tasks/working-dir/raw'
output_dir = '/home/vladimir/Repos/github/airflow-demo/tasks/preprocessed'
sleep_seconds = 5

bash_command = '/home/vladimir/Repos/github/airflow-demo/tasks/preprocessor.sh\
    -i {input_dir} -o {output_dir} -t {date_time} -s {sleep_seconds}'.format(
    input_dir=input_dir, output_dir=output_dir, date_time=execution_date, sleep_seconds=sleep_seconds
)

task = BashOperator(
    task_id='preprocessor_task_1',
    bash_command=bash_command,
    dag=dag)
