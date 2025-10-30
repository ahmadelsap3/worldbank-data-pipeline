{{
  config(
    materialized='view',
    schema='RAW_STAGING'
  )
}}

-- Staging model for World Bank indicators data
-- Standardizes column names and data types from the raw WORLDBANK_INDICATORS table

SELECT
    RECORD_ID,
    INDICATOR_ID,
    INDICATOR_NAME,
    COUNTRY_ID,
    COUNTRY_NAME,
    YEAR,
    VALUE,
    UNIT,
    OBS_STATUS,
    DECADE,
    REGION,
    CATEGORY,
    FETCHED_AT
FROM {{ source('worldbank_raw', 'worldbank_indicators') }}
WHERE VALUE IS NOT NULL
