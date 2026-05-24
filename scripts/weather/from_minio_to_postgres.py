from airflow.hooks.base import BaseHook
from models.database import engine_from_airflow


def from_minio_to_postgres(**context):
    conn = BaseHook.get_connection("postgres_dwh")
    engine = engine_from_airflow(conn)

    try:
        with engine.begin() as db:
            db.execute()
    finally:
        engine.dispose()
