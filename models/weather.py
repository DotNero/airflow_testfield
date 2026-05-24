from sqlalchemy import (
    BigInteger,
    Date,
    DateTime,
    Integer,
    Numeric,
    Text,
    text,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class WeatherRawLog(Base):
    __tablename__ = "weather_raw_log"
    __table_args__ = (
        # Дописать индекс
        Index(),
        {"schema": "metadata"},
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    city_name: Mapped[str] = mapped_column(Text, nullable=False)
    minio_link: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[str] = mapped_column(Numeric(15, 8), nullable=False)
    longitude: Mapped[str] = mapped_column(Numeric(15, 8), nullable=False)
    start_date: Mapped[str] = mapped_column(Date, nullable=False)
    end_date: Mapped[str] = mapped_column(Date, nullable=False)
    s3_bucker: Mapped[str] = mapped_column(Text, nullable=False)
    response_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    http_status_code: Mapped[int] = mapped_column(Integer, nullable=True)
    dag_id: Mapped[int] = mapped_column(Integer, nullable=False)
    run_id: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=text("now()"),
    )


"""
create schema if not exists metadata;
create schema if not exists stg;

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




SELECT
    current_user,
    current_database(),
    inet_server_addr(),
    inet_server_port(),
    version();
"""
