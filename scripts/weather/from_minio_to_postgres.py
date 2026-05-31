from airflow.sdk.bases.hook import BaseHook
from models.database import Database


def from_minio_to_postgres(**context):
    conn = BaseHook.get_connection("postgres_dwh")
    engine = Database.engine_from_airflow(conn)

    try:
        with engine.begin() as db:
            db.execute()
    finally:
        engine.dispose()
