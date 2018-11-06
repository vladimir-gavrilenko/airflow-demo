#!/usr/bin/env bash
export PROJECT_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

export AIRFLOW_HOME=${PROJECT_DIR}/airflow-home

export AIRFLOW__CORE__AIRFLOW_HOME=${AIRFLOW_HOME}
export AIRFLOW__CORE__DAGS_FOLDER=${PROJECT_DIR}/dags
export AIRFLOW__CORE__BASE_LOG_DIR=${AIRFLOW_HOME}/logs
