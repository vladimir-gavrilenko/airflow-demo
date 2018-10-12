# Airflow Demo

## Steps
0. Activate virtual environment:
    ```console
    source venv/bin/activate
    ```
1. Run [1-start-airflow-server.sh](1-start-airflow-server.sh)
2. In another terminal activate venv and run [2-start-airflow-scheduler.sh](2-start-airflow-scheduler.sh)
3. Open [Airflow UI](http://localhost:8080)
4. Turn on `preprocessor_dag`
