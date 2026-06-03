SELECT
    geo,
    year,
    renewables_pct,
    RANK() OVER (PARTITION BY year ORDER BY renewables_pct DESC) AS rank_by_year
FROM {{ ref('stg_renewables_leaders') }}

