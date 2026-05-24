from airflow.providers.postgres.hooks.postgres import PostgresHook
import logging

logger = logging.getLogger(__name__)


def write_log_to_postgres(xcom, **context):
    data_interval_start = context.get("data_interval_start").to_date_string()
    data_interval_end = context.get("data_interval_end").to_date_string()
    dag_id = context.get("dag_id")
    run_id = context.get("run_id")
    logger.info()

    params = {
        "start_date": data_interval_start,
        "end_date": data_interval_end,
        "longitude": longitude,
        "latitude": latitude,
        "response_bytes": xcom.response_bytes,
        "http_status_code": xcom.http_status_code,
        "s3_bucker": "weather",
        "dag_id": dag_id,
        "run_id": run_id,
        "minio_link": xcom.minio_link,
    }
