
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select measurement_id
from ANALYTICS_DB.RAW_staging.stg_openaq
where measurement_id is null



  
  
      
    ) dbt_internal_test