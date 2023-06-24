-- Use the `ref` function to select from other models

select *
from "postgres"."myschema"."my_first_dbt_model"
where id = 1