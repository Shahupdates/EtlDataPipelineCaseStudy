WITH filtered_data AS (
    SELECT *
    FROM myschema.postgres
    WHERE contract_type = 'Magic Eden'
        AND timestamp >= (CURRENT_TIMESTAMP - INTERVAL '2 years')
)
SELECT *
FROM filtered_data
