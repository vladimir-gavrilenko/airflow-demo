import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import BranchPythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 11, 6, 11, 5),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG('pipeline_dag', default_args=default_args, schedule_interval='*/5 * * * *')

date_time = '{{ execution_date.strftime("%Y-%m-%d-%H-%M") }}'
project_dir = os.environ['PROJECT_DIR']

# commands
preprocessor_command = '{project_dir}/tasks/preprocessor.sh -i {project_dir}/tasks/working-dir/raw' \
                       ' -o {project_dir}/tasks/working-dir/preprocessed -t {date_time} -s 1 ' \
    .format(project_dir=project_dir, date_time=date_time)

ten_min_aggregator_command = 'python3 {project_dir}/tasks/n-min-aggregator.py ' \
                             '-i {project_dir}/tasks/working-dir/preprocessed' \
                             ' -o {project_dir}/tasks/working-dir/10-min-aggregates -t {date_time} ' \
                             '-d 5 -n 2 ' \
    .format(project_dir=project_dir, date_time=date_time)

hour_aggregator_command = 'python3 {project_dir}/tasks/n-min-aggregator.py ' \
                          '-i {project_dir}/tasks/working-dir/10-min-aggregates' \
                          ' -o {project_dir}/tasks/working-dir/hour-aggregates -t {date_time} ' \
                          '-d 10 -n 6 ' \
    .format(project_dir=project_dir, date_time=date_time)


def get_branch_if_minutes_end_with_suffix(*args, **kwargs):
    execution_date = kwargs['execution_date']
    if execution_date.strftime('%M').endswith(kwargs['params']['minutes_suffix']):
        return kwargs['params']['branch']


# tasks
preprocessor = BashOperator(
    task_id='preprocessor',
    bash_command=preprocessor_command,
    depends_on_past=True,
    dag=dag)

if_ten_min = BranchPythonOperator(
    task_id='if_ten_min',
    python_callable=get_branch_if_minutes_end_with_suffix,
    provide_context=True,
    params={'branch': 'ten_min_aggregator', 'minutes_suffix': '0'},
    dag=dag
)

ten_min_aggregator = BashOperator(
    task_id='ten_min_aggregator',
    bash_command=ten_min_aggregator_command,
    dag=dag
)

if_hour = BranchPythonOperator(
    task_id='if_hour',
    python_callable=get_branch_if_minutes_end_with_suffix,
    provide_context=True,
    params={'branch': 'hour_aggregator', 'minutes_suffix': '00'},
    dag=dag
)

hour_aggregator = BashOperator(
    task_id='hour_aggregator',
    bash_command=hour_aggregator_command,
    dag=dag
)

# dag
preprocessor >> if_ten_min >> ten_min_aggregator >> if_hour >> hour_aggregator
