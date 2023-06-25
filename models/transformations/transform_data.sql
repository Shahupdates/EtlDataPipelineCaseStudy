SELECT
  address,
  amount,
  timestamp
FROM
  public.transactions
WHERE
  timestamp > CURRENT_TIMESTAMP - INTERVAL '2 years'