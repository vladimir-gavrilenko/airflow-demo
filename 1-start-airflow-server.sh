#!/usr/bin/env bash
export AIRFLOW_HOME=airflow-home
airflow initdb
airflow webserver -p 8080
