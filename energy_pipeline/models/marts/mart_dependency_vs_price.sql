SELECT
    geo,
    year,
    dependency_pct,
    avg_price_eur_kwh,
    CASE
        WHEN dependency_pct >= 75 THEN 'Alta dependencia'
        WHEN dependency_pct >= 40 THEN 'Dependencia media'
        ELSE 'Baja dependencia'
    END AS dependency_category
FROM {{ ref('stg_dependency_vs_price') }}
ORDER BY year, dependency_pct DESC
