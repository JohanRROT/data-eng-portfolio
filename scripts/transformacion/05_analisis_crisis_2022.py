# scripts/transformacion/05_analisis_crisis_2022.py
# Pregunta: ¿Cómo impactó la crisis energética de 2022 en los precios de electricidad?

import pandas as pd
from pathlib import Path

# ── 1. Rutas ──────────────────────────────────────────────────────────────────
ROOT      = Path(__file__).resolve().parent.parent.parent
INPUT     = ROOT / "data" / "processed" / "eurostat" / "electricity_prices.csv"
OUTPUT_DIR = ROOT / "data" / "analytical"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT    = OUTPUT_DIR / "crisis_2022_prices.csv"

# ── 2. Carga ──────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT, parse_dates=["time"])

# ── 3. Filtros: banda de consumo, régimen fiscal y moneda ─────────────────────
df = df[
    (df["nrg_cons"]  == "Consumption of kWh - all bands") &
    (df["tax"]       == "All taxes and levies included") &
    (df["currency"]  == "Euro")
].copy()
# ── 4. Excluir agregados regionales ───────────────────────────────────────────
excluir = [
    "European Union - 27 countries (from 2020)",
    "Euro area (EA11-1999, EA12-2001, EA13-2007, EA15-2008, EA16-2009, EA17-2011, EA18-2014, EA19-2015, EA20-2023, EA21-2026)",
]
df = df[~df["geo"].isin(excluir)].copy()

# ── 5. Extraer año y semestre ─────────────────────────────────────────────────
df["year"]     = df["time"].dt.year
df["semester"] = df["time"].dt.month.map({1: "S1", 7: "S2"})
df["period"]   = df["year"].astype(str) + "-" + df["semester"]

# ── 6. Filtrar período relevante (2019–2024) ──────────────────────────────────
df = df[df["year"].between(2019, 2024)].copy()

# ── 7. Tabla 1: evolución semestral promedio EU ───────────────────────────────
eu_evolucion = (
    df.groupby("period")["value"]
    .mean()
    .reset_index()
    .rename(columns={"value": "avg_price_eur_kwh"})
    .sort_values("period")
)

# ── 8. Tabla 2: precio por país en el pico (2022-S2) ─────────────────────────
pico = df[df["period"] == "2022-S2"][["geo", "value"]].copy()
pico = pico.rename(columns={"value": "price_2022_S2"})
pico = pico.sort_values("price_2022_S2", ascending=False).reset_index(drop=True)
pico.index += 1
pico.index.name = "rank"

# ── 9. Tabla 3: variación de precio 2021-S2 → 2022-S2 por país ───────────────
pre_crisis = (
    df[df["period"] == "2021-S2"][["geo", "value"]]
    .rename(columns={"value": "price_2021_S2"})
)
crisis = (
    df[df["period"] == "2022-S2"][["geo", "value"]]
    .rename(columns={"value": "price_2022_S2"})
)

variacion = pd.merge(pre_crisis, crisis, on="geo")
variacion["variacion_pct"] = (
    (variacion["price_2022_S2"] - variacion["price_2021_S2"])
    / variacion["price_2021_S2"] * 100
).round(2)
variacion = variacion.sort_values("variacion_pct", ascending=False).reset_index(drop=True)

# ── 10. Resultados en consola ─────────────────────────────────────────────────
print("=" * 60)
print("Análisis de impacto — Crisis energética 2022")
print("=" * 60)

print("\n── Evolución semestral promedio EU (2019–2024) ──")
print(eu_evolucion.to_string(index=False))

print("\n── Top 10 precios más altos en el pico (2022-S2) ──")
print(pico.head(10).to_string())

print("\n── Top 10 mayores subidas de precio 2021-S1 → 2022-S2 ──")
print(variacion.head(10).to_string(index=False))

# ── 11. Guardar output ────────────────────────────────────────────────────────
output_df = df[["geo", "year", "semester", "period", "value"]].rename(
    columns={"value": "price_eur_kwh"}
)
output_df.to_csv(OUTPUT, index=False)
print(f"\n✅ Archivo guardado en: {OUTPUT}")