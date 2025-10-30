{{
  config(
    materialized='view',
    schema='RAW'
  )
}}

-- Dimension table for service types (weekday, saturday, sunday)
-- Useful for analyzing service patterns by day type

select
    row_number() over (order by "service_id") as "service_pk",
    "service_id" as "service_type",
    case
        when "service_id" = 'weekday' then 'Monday-Friday'
        when "service_id" = 'saturday' then 'Saturday'
        when "service_id" = 'sunday' then 'Sunday/Holiday'
    end as "service_description"
from (
    select distinct "service_id"
    from {{ ref('stg_gtfs') }}
)
