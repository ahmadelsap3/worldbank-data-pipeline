{{
  config(
    materialized='view',
    schema='RAW_marts'
  )
}}

-- Fact table for transit trips
-- Contains all trip-level metrics for analysis

select
    "trip_id",
    "route_id",
    "route_short_name",
    "route_long_name",
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
    "on_time"
from {{ ref('stg_gtfs') }}
