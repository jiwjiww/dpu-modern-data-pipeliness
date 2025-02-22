import os

from airflow.utils import timezone

from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping


profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="weather_postgres_conn",
        profile_args={"schema": "dbt_kan"},
    ),
)

dbt_dag = DbtDag(
    dag_id="dbt_dag",
    project_config=ProjectConfig(
        "/opt/airflow/dbt/weather",
    ),
    profile_config=profile_config,
    schedule_interval="@daily",
    start_date=timezone.datetime(2025, 2, 22),
    catchup=False,
    default_args={"retries": 2},
    tags=["dpu"],
)