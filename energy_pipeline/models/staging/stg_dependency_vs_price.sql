SELECT
    geo,
    year,
    dependency_pct,
    avg_price_eur_kwh
FROM {{ source('energy_portfolio', 'dependency_vs_price') }}

