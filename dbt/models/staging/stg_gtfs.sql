{{
  config(
    materialized='view',
    schema='RAW_staging'
  )
}}

-- Staging model for GTFS transit trip data
-- Standardizes column names and data types from the raw GTFS_TRIPS table

select
    "trip_id",
    "route_id",
    "route_short_name",
    "route_long_name",
    "route_type",
    "route_color",
    "direction_id",
    "direction_name",
    "service_id",
    "trip_date",
    "departure_time",
    "arrival_time",
    "origin_stop_id",
    "origin_stop_name",
    "origin_lat",
    "origin_lon",
    "destination_stop_id",
    "destination_stop_name",
    "destination_lat",
    "destination_lon",
    "num_stops",
    "ridership",
    "delay_minutes",
    "on_time",
    "generated_at"
from {{ source('gtfs_raw', 'gtfs_trips') }}
