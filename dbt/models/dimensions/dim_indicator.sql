{{
  config(
    materialized='table',
    schema='RAW'
  )
}}

-- Dimension table for World Bank indicators
-- Deduplicates indicator information

SELECT
    ROW_NUMBER() OVER (ORDER BY INDICATOR_ID) as INDICATOR_PK,
    INDICATOR_ID,
    INDICATOR_NAME,
    CATEGORY,
    UNIT
FROM (
    SELECT DISTINCT
        INDICATOR_ID,
        INDICATOR_NAME,
        CATEGORY,
        UNIT
    FROM {{ ref('stg_worldbank') }}
)
ORDER BY INDICATOR_ID
