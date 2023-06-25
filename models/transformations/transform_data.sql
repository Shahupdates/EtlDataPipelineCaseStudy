SELECT
  address,
  amount,
  timestamp,
  amount_sol
FROM
  public.transactions
WHERE
  timestamp > CURRENT_TIMESTAMP - INTERVAL '2 years'
