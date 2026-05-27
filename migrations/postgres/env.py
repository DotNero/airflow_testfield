from alembic import context

from config.settings import settings
from models.base import Base
from models.database import Database
import models.weather

target_metadata = Base.metadata

include_schemas = True


def run_migrations_online():
    engine = Database.engine_from_settings()

    with engine.connect() as conn:
        context.configure(
            connection=conn,
            target_metadata=target_metadata,
            include_schemas=include_schemas,
        )

        with context.begin_transaction():
            context.run_migrations()
