-- ============================================================
-- Proyecto: European Energy Transition Pipeline
-- Archivo:  01_create_tables.sql
-- Descripción: Tablas analíticas cargadas desde data/analytical/
-- ============================================================

-- Tabla 1: Líderes en renovables por país y año
CREATE TABLE IF NOT EXISTS renewables_leaders (
    geo             VARCHAR(100),
    year            INTEGER,
    renewables_pct  NUMERIC(6,2)
);

-- Tabla 2: Impacto de la crisis energética 2022
CREATE TABLE IF NOT EXISTS crisis_2022_prices (
    geo             VARCHAR(100),
    year            INTEGER,
    semester        VARCHAR(5),
    period          VARCHAR(10),
    price_eur_kwh   NUMERIC(10,4)
);

-- Tabla 3: Relación dependencia energética vs precio
CREATE TABLE IF NOT EXISTS dependency_vs_price (
    geo             VARCHAR(100),
    year            INTEGER,
    dependency_pct  NUMERIC(8,2),
    avg_price_eur_kwh NUMERIC(10,4)
);
