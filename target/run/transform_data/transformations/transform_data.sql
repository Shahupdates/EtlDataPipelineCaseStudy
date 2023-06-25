
  create view "main_database"."public"."transform_data__dbt_tmp" as (
    SELECT
  address,
  amount,
  timestamp
FROM
  public.transactions
WHERE
  timestamp > CURRENT_TIMESTAMP - INTERVAL '2 years'
  );
