-- dimension: distinct stations / locations
select
    row_number() over (order by "location") as "station_id",
    "location" as "station_name",
    "city",
    "country",
    "latitude",
    "longitude"
from (
    select distinct "location", "city", "country", "latitude", "longitude"
    from {{ ref('stg_openaq') }}
)
