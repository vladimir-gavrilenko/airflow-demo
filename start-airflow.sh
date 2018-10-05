#!/usr/bin/env bash
export AIRFLOW_HOME=airflow-home
export AIRFLOW_GPL_UNIDECODE=yes

pip install apache-airflow

airflow initdb
airflow webserver -p 8080
airflow scheduler
