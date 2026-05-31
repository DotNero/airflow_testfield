from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class PostgresDWHSettings(BaseSettings):
    POSTGRES_DWH_HOST: str
    POSTGRES_DWH_USER: str
    POSTGRES_DWH_PASSWORD: str
    POSTGRES_DWH_DB: str
    POSTGRES_DWH_PORT: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def postgres_dwh_url_sync(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.POSTGRES_DWH_USER,
            password=self.POSTGRES_DWH_PASSWORD,
            host=self.POSTGRES_DWH_HOST,
            port=self.POSTGRES_DWH_PORT,
            database=self.POSTGRES_DWH_DB,
        )  # .render_as_string(hide_password=False)


settings = PostgresDWHSettings()
