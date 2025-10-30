{{
  config(
    materialized='table',
    schema='RAW'
  )
}}

-- Dimension table for countries
-- Deduplicates country information

SELECT
    ROW_NUMBER() OVER (ORDER BY COUNTRY_ID) as COUNTRY_PK,
    COUNTRY_ID,
    COUNTRY_NAME,
    REGION
FROM (
    SELECT DISTINCT
        COUNTRY_ID,
        COUNTRY_NAME,
        REGION
    FROM {{ ref('stg_worldbank') }}
)
ORDER BY COUNTRY_ID
