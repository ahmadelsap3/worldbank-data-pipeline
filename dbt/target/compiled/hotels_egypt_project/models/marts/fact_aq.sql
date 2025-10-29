-- fact table for OpenAQ measurements
select
    "measurement_id",
    "location",
    "city",
    "country",
    "parameter",
    "value",
    "unit",
    "latitude",
    "longitude",
    "measured_at",
    "fetched_at"
from ANALYTICS_DB.RAW_staging.stg_openaq