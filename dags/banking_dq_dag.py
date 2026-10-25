from datetime import datetime
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT = '"/Users/macbookairm2/Projects/Python Project/banking-dq-etl"'

with DAG(
    dag_id="banking_dq_pipeline",
    start_date=datetime(2026,9,1),
    schedule=None,
    catchup=False,
    tags=["banking", "dq"]
) as dag:
    run_tests = BashOperator(
        task_id="run_tests",
        bash_command=f"cd {PROJECT} && .venv/bin/pytest",
    )
    run_pipeline= BashOperator(
        task_id = "run_pipeline",
        bash_command=f"cd {PROJECT} && set -a && source .env && set +a && .venv/bin/python -m banking_dq.pipeline --business_date {{{{ ds_nodash }}}}",
    )
    dbt_build= BashOperator(
        task_id= "dbt_build",
        bash_command=f"cd {PROJECT} && set -a && source .env && set +a && cd banking_dbt && ../.venv/bin/dbt build"
    )

    run_tests >> run_pipeline >> dbt_build
