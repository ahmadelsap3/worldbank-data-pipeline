-- staging: expects a source/table `local.openaq_stream` with columns matching the NDJSON keys
with raw as (
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
        "date_utc" as "measured_at",
        "fetched_at"
    from {{ source('local', 'openaq_stream') }}
)

select * from raw
