"""
RAW

- [v] Проверить коннект airflow к minio
- [v] Проверить получение данных из апи
- [v] Проверить мультитаск
- [ ] Положить в минио
"""

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from scripts.weather.api_download import api_download

# Если нужно за текущий день
# START_DATE = pendulum.today("UTC").subtract(days=30)

default_args = {
    "owner": "loader",
    # Внутренний backfill
    # "start_date": pendulum.datetime(2026, 5, 18, tz="UTC"),
    "retries": 2,
}

dag = DAG(
    dag_id="WEATHER_API",
    default_args=default_args,
    # "0 10 * * *"
    schedule=None,
    # Внутренний backfill
    # catchup=False,
    description="API WEATHER to MINIO(RAW) -> PostgreSQL(Operational) -> Clickhouse(Mart)",
    tags=["weather", "api", "minio", "postgresql", "clickhouse"],
)

dag.doc_md = __doc__

city_request_params = {
    "Moscow": {"latitude": 55.7558, "longitude": 37.6173},
    "Kazan": {"latitude": 55.7887, "longitude": 49.1221},
    "Ulyanovsk": {"latitude": 54.3142, "longitude": 48.4031},
}

city_request_params_mapped = [
    {"op_kwargs": {"city_name": city_name, **params}}
    for city_name, params in city_request_params.items()
]

download_weather_api_upload_to_minio = PythonOperator.partial(
    task_id="download_weather_api_upload_to_minio",
    python_callable=api_download,
    dag=dag,
).expand_kwargs(city_request_params_mapped)
