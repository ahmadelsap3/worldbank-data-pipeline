{{
  config(
    materialized='table',
    schema='RAW_MARTS'
  )
}}

-- Fact table for World Bank indicator measurements
-- Contains all measurements with references to dimensions

SELECT
    RECORD_ID,
    INDICATOR_ID,
    INDICATOR_NAME,
    COUNTRY_ID,
    COUNTRY_NAME,
    YEAR,
    DECADE,
    VALUE,
    UNIT,
    REGION,
    CATEGORY,
    OBS_STATUS,
    FETCHED_AT
FROM {{ ref('stg_worldbank') }}
ORDER BY COUNTRY_ID, INDICATOR_ID, YEAR
