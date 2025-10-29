-- dimension: measurement parameter (pm25, no2, etc.)
select
    row_number() over (order by "parameter") as "parameter_id",
    "parameter" as "parameter_name",
    min("unit") as "unit"
from (
    select distinct "parameter", "unit"
    from ANALYTICS_DB.RAW_staging.stg_openaq
)
group by "parameter"