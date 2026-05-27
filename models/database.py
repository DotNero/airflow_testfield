from config import settings
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text, Engine, pool


class Database:

    @staticmethod
    def engine_from_settings() -> Engine:
        engine_from_settings = create_engine(
            url=settings.postgres_dwh_url_sync,
            # Дублировать в консоль запросы
            echo=True,
            pool_size=5,
            max_overflow=10,
        )
        return engine_from_settings

    @staticmethod
    def engine_from_airflow(conn) -> Engine:
        db_url = URL.create(
            drivername="postgresql+psycopg2",
            username=conn.login,
            password=conn.password,
            host=conn.host,
            port=conn.port,
            database=conn.schema,
        )
        engine = create_engine(url=db_url, echo=True)
        return engine


database = Database()
