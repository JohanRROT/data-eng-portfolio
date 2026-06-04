# European Energy Transition Pipeline

Pipeline de ingeniería de datos end-to-end construido sobre datos reales de Eurostat (2005–2024).
Demuestra ingestión, limpieza, modelado con dbt, tests de calidad y análisis sobre PostgreSQL.

---

## Preguntas analíticas

1. ¿Qué países lideran la transición hacia energías renovables?
2. ¿Cómo impactó la crisis energética de 2022 en los precios de electricidad?
3. ¿Qué relación existe entre dependencia energética y precio de electricidad?

---

## Arquitectura del pipeline
Eurostat API (JSON-stat)
│
▼
scripts/ingesta/extract_eurostat.py
│  pandas, requests
▼
data/raw/eurostat/          ← 4 datasets, ~115,000 filas
│
▼
scripts/transformacion/
01_profiling.py           ← ydata-profiling, detección de nulos y anomalías
02_clean.py               ← limpieza, conversión de fechas, eliminación de nulos
│
▼
data/processed/eurostat/    ← datos limpios listos para carga
│
▼
PostgreSQL 16 (WSL2)
energy_portfolio DB
├── renewables_leaders    (749 filas)
├── crisis_2022_prices    (272 filas)
└── dependency_vs_price   (148 filas)
│
▼
dbt (energy_pipeline/)
├── staging/              ← vistas sobre tablas fuente
└── marts/                ← modelos analíticos con RANK() y CASE
│
▼
25 data tests (not_null, accepted_values)

---

## Stack técnico

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.12, SQL |
| Ingestión | requests, pandas |
| Base de datos | PostgreSQL 16 |
| Transformación | dbt-core 1.11, dbt-postgres 1.10 |
| Calidad de datos | dbt tests (not_null, accepted_values) |
| Documentación | dbt docs |
| Entorno | WSL2, Ubuntu 24.04 |
| Control de versiones | Git, GitHub |

---

## Hallazgos principales

### 1. Líderes de la transición renovable

Islandia, Noruega y Suecia ocupan los tres primeros puestos de forma ininterrumpida
desde 2004 hasta 2024. El umbral para entrar al top 5 subió de 29% en 2004 a 46%
en 2024, lo que indica avance generalizado en todo el continente.

| País | 2004 | 2010 | 2015 | 2020 | 2024 |
|---|---|---|---|---|---|
| Iceland | 58.9% | 70.9% | 72.0% | 83.7% | 79.3% |
| Norway | 58.4% | 61.9% | 68.6% | 77.4% | 77.9% |
| Sweden | 38.4% | 46.1% | 52.2% | 60.1% | 62.9% |
| Denmark | — | — | — | — | 46.5% |

Dinamarca entra al top 5 por primera vez en 2024, impulsada por energía eólica.

### 2. Impacto de la crisis energética de 2022

El impacto no fue simultáneo en todos los países — cada uno lo absorbió en momentos
distintos según su mix energético y políticas de subsidio:

- **Italia** registró el salto más brusco: de 0.26 EUR/kWh en 2021 S2 a 0.41 en 2023 S1 (+57% en cuatro semestres).
- **Alemania** absorbió el shock con retraso: sus precios superaron el promedio histórico recién en 2023 S1.
- **Francia** mostró una subida lenta pero sin retorno — cada semestre desde 2022 marca un nuevo máximo.
- **Países Bajos** presenta el caso más volátil: precio de 0.012 EUR/kWh en 2022 S1 (posible subsidio estatal masivo) seguido de 0.349 en 2023 S1.

### 3. Dependencia energética y precio

La dependencia energética por sí sola no explica el precio de electricidad.
El análisis de 2023 muestra patrones que rompen la intuición esperada:

- **Malta** (97.6% dependencia) tiene precio bajo (0.147 EUR/kWh) — subsidios estatales.
- **Turquía** (70.0% dependencia) tiene el precio más bajo del grupo (0.056 EUR/kWh) — control gubernamental de tarifas.
- **Alemania** (66.8% dependencia) tiene el precio más alto (0.420 EUR/kWh) — estructura fiscal sobre la energía.

**Conclusión:** el precio está determinado principalmente por la estructura fiscal del país
y las políticas de subsidio, no por el nivel de dependencia energética del exterior.

**Nota metodológica:** Noruega registra dependencia de -655%, valor correcto que refleja
su condición de exportador neto de energía (gas y electricidad) a escala continental.

---

## Estructura del repositorio
data-eng-portfolio/
├── data/
│   ├── raw/eurostat/           ← datasets originales de Eurostat
│   └── processed/eurostat/     ← datos limpios post-transformación
├── scripts/
│   ├── ingesta/
│   │   └── extract_eurostat.py
│   └── transformacion/
│       ├── 01_profiling.py
│       └── 02_clean.py
├── energy_pipeline/            ← proyecto dbt
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
└── docs/profiling/             ← reportes HTML de ydata-profiling

---

## Fuente de datos

[Eurostat](https://ec.europa.eu/eurostat) — Oficina Estadística de la Unión Europea.
Datasets: participación renovables, precios electricidad hogares, dependencia energética,
consumo final por sector. Acceso vía API REST en formato JSON-stat.
