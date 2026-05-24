from sqlalchemy import BigInteger, Date, DateTime, Integer, Numeric, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class WeatherRawLog(Base):
    __tablename__ = "weather_raw_log"
    __table_args__ = {"schema": "metadata"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city_name: Mapped[str] = mapped_column(Text, nullable=False)

    created_at = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=text("now()"),
    )
