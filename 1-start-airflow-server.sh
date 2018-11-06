#!/usr/bin/env bash
PROJECT_DIR="$(cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

source ${PROJECT_DIR}/venv/bin/activate
source ${PROJECT_DIR}/env.sh

airflow initdb
airflow webserver -p 8080
