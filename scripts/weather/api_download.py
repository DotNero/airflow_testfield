import pendulum
import logging
from datetime import datetime, date, timedelta
import requests
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

logger = logging.getLogger(__name__)


def api_download(
    city_name: str, longitude: float = None, latitude: float = None, **context
):

    # Временные параметры выборки
    data_interval_start = context.get("data_interval_start").to_date_string()
    data_interval_end = context.get("data_interval_end").to_date_string()

    logger.info(
        "start_time = %s, end_time = %s", data_interval_start, data_interval_end
    )

    # Запрос в погоду
    params = {
        "start_date": data_interval_start,
        "end_date": data_interval_end,
        "longitude": longitude,
        "latitude": latitude,
        "hourly": "temperature_2m",
    }

    url = "https://archive-api.open-meteo.com/v1/archive"

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        logger.info(
            "Weather response: city=%s, status code = %s, bytes=%s",
            city_name,
            response.status_code,
            len(response.text),
        )
    except requests.RequestException:
        logger.exception("Weather request failed city=%s", city_name)

    raw_json = response.text
    check = True if raw_json and len(raw_json) > 0 else False

    # Отправка в S3

    bucket_name = "weather"
    s3_key = (
        f"raw/open_meteo/"
        f"city={city_name}/"
        f"date={data_interval_start}/"
        f"date={data_interval_end}/"
        f"response.json"
    )

    s3_hook = S3Hook(aws_conn_id="minio_s3")

    s3_hook.load_string(
        string_data=raw_json,
        key=s3_key,
        bucket_name=bucket_name,
        replace=True,
        encoding="utf-8",
    )

    # Возврат метаданных в XCom

    return {
        "city_name": city_name,
        "start_date": data_interval_start,
        "end_date": data_interval_end,
        "check": check,
    }
