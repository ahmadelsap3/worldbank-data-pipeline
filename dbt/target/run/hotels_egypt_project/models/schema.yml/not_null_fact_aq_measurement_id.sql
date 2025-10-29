
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select measurement_id
from ANALYTICS_DB.RAW_marts.fact_aq
where measurement_id is null



  
  
      
    ) dbt_internal_test