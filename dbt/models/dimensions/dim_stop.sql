{{
  config(
    materialized='view',
    schema='RAW'
  )
}}

-- Dimension table for Metro stops/stations
-- Combines origin and destination stops, deduplicates

with all_stops as (
    select
        "origin_stop_id" as "stop_id",
        "origin_stop_name" as "stop_name",
        "origin_lat" as "stop_lat",
        "origin_lon" as "stop_lon"
    from {{ ref('stg_gtfs') }}
    
    union
    
    select
        "destination_stop_id" as "stop_id",
        "destination_stop_name" as "stop_name",
        "destination_lat" as "stop_lat",
        "destination_lon" as "stop_lon"
    from {{ ref('stg_gtfs') }}
)

select
    row_number() over (order by "stop_id") as "stop_pk",
    "stop_id",
    "stop_name",
    "stop_lat",
    "stop_lon"
from (
    select distinct
        "stop_id",
        "stop_name",
        "stop_lat",
        "stop_lon"
    from all_stops
)
