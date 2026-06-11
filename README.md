# European Energy Transition Pipeline
 
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-1.11-FF694B?style=flat&logo=dbt&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-24.04_WSL2-E95420?style=flat&logo=ubuntu&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
 
End-to-end data engineering pipeline built on real Eurostat data (2005–2024). Ingests four official EU datasets via REST API, cleans and loads them into PostgreSQL, and transforms raw tables into analytical models using dbt — with 25 automated data quality tests.
 
The pipeline answers three concrete questions about Europe's energy transition:
 
- Which countries lead the shift toward renewables?
- How did the 2022 energy crisis affect electricity prices across Europe?
- Does energy dependency actually drive electricity prices — or is something else at play?
---
 
## Pipeline Architecture
 
```
Eurostat REST API (JSON-stat)
        │
        ▼
scripts/ingesta/extract_eurostat.py
        │  pandas · requests
        ▼
data/raw/eurostat/                    ← 4 datasets · ~115,000 rows
        │
        ▼
scripts/transformacion/
  ├── 01_profiling.py                 ← ydata-profiling · null detection · anomalies
  └── 02_clean.py                     ← type casting · date normalisation · null removal
        │
        ▼
data/processed/eurostat/              ← clean data ready for load
        │
        ▼
PostgreSQL 16  (WSL2 · energy_portfolio DB)
  ├── renewables_leaders              (749 rows)
  ├── crisis_2022_prices              (272 rows)
  └── dependency_vs_price            (148 rows)
        │
        ▼
dbt  (energy_pipeline/)
  ├── staging/                        ← views on source tables
  └── marts/                          ← analytical models · RANK() · CASE
        │
        ▼
25 data tests  (not_null · accepted_values)
```
 
---
 
## Tech Stack
 
| Layer | Technology |
|---|---|
| Language | Python 3.12, SQL |
| Ingestion | `requests`, `pandas` |
| Profiling | `ydata-profiling` |
| Database | PostgreSQL 16 |
| Transformation | dbt-core 1.11, dbt-postgres 1.10 |
| Data Quality | dbt tests (`not_null`, `accepted_values`) |
| Documentation | dbt docs |
| Environment | WSL2, Ubuntu 24.04 |
| Version Control | Git, GitHub |
 
---
 
## Key Findings
 
### 1. Renewable Transition Leaders
 
Iceland, Norway and Sweden have held the top three positions without interruption from 2004 to 2024. The threshold to enter the top 5 rose from 29% in 2004 to 46% in 2024 — evidence of broad progress across the continent, not just isolated leaders.
 
| Country | 2004 | 2010 | 2015 | 2020 | 2024 |
|---|---|---|---|---|---|
| Iceland | 58.9% | 70.9% | 72.0% | 83.7% | 79.3% |
| Norway | 58.4% | 61.9% | 68.6% | 77.4% | 77.9% |
| Sweden | 38.4% | 46.1% | 52.2% | 60.1% | 62.9% |
| Denmark | — | — | — | — | 46.5% |
 
Denmark enters the top 5 for the first time in 2024, driven by wind energy expansion.
 
### 2. The 2022 Energy Crisis — Not a Single Shock
 
The crisis did not hit all countries at the same time. Each absorbed the impact differently depending on energy mix and subsidy policy:
 
- **Italy** recorded the sharpest jump: from €0.26/kWh in H2 2021 to €0.41 in H1 2023 — a 57% increase in four semesters.
- **Germany** absorbed the shock with delay: prices only exceeded the historical average in H1 2023.
- **France** showed a slow but irreversible rise — every semester since 2022 set a new maximum.
- **Netherlands** is the most volatile case: €0.012/kWh in H1 2022 (likely a large state subsidy), followed by €0.349 in H1 2023.
### 3. Energy Dependency vs. Electricity Price
 
Energy dependency alone does not explain electricity prices. The 2023 data reveals patterns that break the expected intuition:
 
| Country | Energy Dependency | Price (€/kWh) | Explanation |
|---|---|---|---|
| Malta | 97.6% | 0.147 | State subsidies |
| Turkey | 70.0% | 0.056 | Government-controlled tariffs |
| Germany | 66.8% | 0.420 | Heavy energy taxation |
 
**Conclusion:** prices are driven primarily by the country's fiscal structure and subsidy policies, not by external energy dependency.
 
> **Methodological note:** Norway records −655% energy dependency — a correct value reflecting its status as a net energy exporter (gas and electricity) at continental scale.
 
---
 
## Repository Structure
 
```
european-energy-pipeline/
├── data/
│   ├── raw/eurostat/               ← original Eurostat datasets
│   └── processed/eurostat/         ← clean data post-transformation
├── scripts/
│   ├── ingesta/
│   │   └── extract_eurostat.py
│   └── transformacion/
│       ├── 01_profiling.py
│       └── 02_clean.py
├── energy_pipeline/                ← dbt project
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
└── docs/profiling/                 ← ydata-profiling HTML reports
```
 
---
 
## Quickstart
 
```bash
# 1. Clone the repository
git clone https://github.com/JohanRROT/european-energy-pipeline.git
cd european-energy-pipeline
 
# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
 
# 3. Install dependencies
pip install -r requirements.txt
 
# 4. Extract raw data from Eurostat API
python scripts/ingesta/extract_eurostat.py
 
# 5. Run profiling and cleaning
python scripts/transformacion/01_profiling.py
python scripts/transformacion/02_clean.py
 
# 6. Load clean data into PostgreSQL, then run dbt
cd energy_pipeline
dbt run
dbt test
```
 
> Requires PostgreSQL 16 running locally (or via WSL2). Update `profiles.yml` with your connection details before running dbt.
 
---
 
## Data Source
 
**Eurostat** — Statistical Office of the European Union.
Datasets used: renewable energy share, household electricity prices, energy dependency, final consumption by sector.
Access via REST API in JSON-stat format — [api.ec.europa.eu/eurostat](https://ec.europa.eu/eurostat)
 
---
 
## Related Repository
 
The orchestration layer for the Movie History project — a companion pipeline using Azure Data Factory + Databricks + Delta Lake:
 
[JohanRROT/adf-movie-history](https://github.com/JohanRROT/adf-movie-history) · [JohanRROT/Databricks_movie_history](https://github.com/JohanRROT/Databricks_movie_history)
 
---
 
## Author
 
**Johan Rodriguez** · Data Engineer
[LinkedIn](https://www.linkedin.com/in/johan-rodriguez-rojas-2736b4259) · [GitHub](https://github.com/JohanRROT)
 
