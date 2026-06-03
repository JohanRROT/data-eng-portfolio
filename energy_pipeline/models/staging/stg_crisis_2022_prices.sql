SELECT
    geo,
    year,
    semester,
    period,
    price_eur_kwh
FROM {{ source('energy_portfolio', 'crisis_2022_prices') }}
