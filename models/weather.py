from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    Integer,
    Float,
    Text,
    text,
    UniqueConstraint,
    Index,
    Time,
    ForeignKey,
)

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from models.base import Base


class WeatherRawLog(Base):
    __tablename__ = "weather_raw_log"
    __table_args__ = (
        Index(None, "dag_id", postgresql_using="hash"),
        Index(None, "run_id"),
        {"schema": "metadata"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city_name: Mapped[str] = mapped_column(Text, nullable=False)
    minio_link: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(Float(precision=53), nullable=False)
    longitude: Mapped[float] = mapped_column(Float(precision=53), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    s3_bucket: Mapped[str] = mapped_column(Text, nullable=False)
    response_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    http_status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    dag_id: Mapped[str] = mapped_column(Text, nullable=False)
    run_id: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=text("now()"),
    )

    hourly_rows: Mapped[list["WeatherHourly"]] = relationship(back_populates="load")


class WeatherHourly(Base):
    __tablename__ = "weather_hourly"
    __table_args__ = (
        Index(None, "city_name", "observation_time"),
        UniqueConstraint("city_name", "observation_time"),
        {"schema": "stg"},
    )
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city_name: Mapped[str] = mapped_column(Text, nullable=False)
    observation_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False
    )
    temperature_2m: Mapped[float | None] = mapped_column(
        Float(precision=53), nullable=True
    )
    temperature_measure: Mapped[str] = mapped_column(Text, nullable=False)
    source_s3_bucket: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_s3_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), nullable=False, server_default=text("now()")
    )
    load_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("metadata.weather_raw_log.id"), nullable=False
    )

    load: Mapped["WeatherRawLog"] = relationship(
        back_populates="hourly_rows",
    )


"""


create schema if not exists metadata;
create schema if not exists stg;

create table stg.weather_hourly (
	id bigserial primary key,
	city_name text not null,
	observation_time timestamp not null,
	temperature_2m double precision,
	temperature_measure text,
	source_s3_bucket text,
	source_s3_key text,
	created_at timestamp not null set default current_timestamp,
	load_id bigint not null references metadata.weather_raw_log(id),
	unique (city_name, observation_time)
);

create index  
	idx_observation_time
on 
	stg.weather_hourly
using 
	btree
(city_name, observation_time);


create table metadata.weather_raw_log (
	id BIGSERIAL primary key , 
	minio_link text not null,
	created_at timestamp not null default current_timestamp,
	city_name text not null,
	latitude decimal not null,
	longitude decimal not null,
	start_date date not null,
	end_date date not null,
	s3_bucket text not null,
	response_bytes int,
	http_status_code int,
	dag_id text not null,
	run_id text not null
);

create index 
	idx_dag_id 
on 
	metadata.weather_raw_log 
using 
	hash 
(dag_id);

create index
	idx_weather_raw_log_run_id
on 
	metadata.weather_raw_log (run_id);

create index 
	idx_weather_raw_log_city_period
on 
	metadata.weather_raw_log (
	city_name, 
	start_date, 
	end_date
);

"""
