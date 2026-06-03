SELECT
    geo,
    year,
    semester,
    period,
    price_eur_kwh,
    AVG(price_eur_kwh) OVER (PARTITION BY geo) AS avg_price_by_country,
    price_eur_kwh - AVG(price_eur_kwh) OVER (PARTITION BY geo) AS deviation_from_avg
FROM {{ ref('stg_crisis_2022_prices') }}
ORDER BY geo, year, semester
