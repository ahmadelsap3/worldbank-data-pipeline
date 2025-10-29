
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select measured_at
from ANALYTICS_DB.RAW_staging.stg_openaq
where measured_at is null



  
  
      
    ) dbt_internal_test