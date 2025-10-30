{{
  config(
    materialized='view',
    schema='RAW'
  )
}}

-- Dimension table for Metro routes
-- Deduplicates and assigns route_id as primary key

select
    row_number() over (order by "route_id") as "route_pk",
    "route_id",
    "route_short_name",
    "route_long_name",
    "route_type",
    "route_color"
from (
    select distinct
        "route_id",
        "route_short_name",
        "route_long_name",
        "route_type",
        "route_color"
    from {{ ref('stg_gtfs') }}
)
