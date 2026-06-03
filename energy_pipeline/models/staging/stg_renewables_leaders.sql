SELECT
    geo,
    year,
    renewables_pct
FROM {{ source('energy_portfolio', 'renewables_leaders') }}
