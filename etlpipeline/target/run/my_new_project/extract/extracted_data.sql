
  create view "postgres"."myschema"."extracted_data__dbt_tmp" as (
    -- models/extract/extracted_data.sql
SELECT *
FROM myschema.transformed_addresses
  );
