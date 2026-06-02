# scripts/transformacion/06_analisis_dependencia_precio.py
# Pregunta: ¿Qué relación existe entre dependencia energética y precio?

import pandas as pd
from pathlib import Path

# ── 1. Rutas ──────────────────────────────────────────────────────────────────
ROOT       = Path(__file__).resolve().parent.parent.parent
INPUT_DEP  = ROOT / "data" / "processed" / "eurostat" / "energy_dependency.csv"
INPUT_PREC = ROOT / "data" / "processed" / "eurostat" / "electricity_prices.csv"
OUTPUT_DIR = ROOT / "data" / "analytical"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT     = OUTPUT_DIR / "dependency_vs_price.csv"

# ── 2. Carga dependencia energética ───────────────────────────────────────────
dep = pd.read_csv(INPUT_DEP, parse_dates=["time"])
dep = dep[dep["siec"] == "Total"].copy()
dep["year"] = dep["time"].dt.year

excluir_dep = [
    "European Union - 27 countries (from 2020)",
    "Euro area – 21 countries (from 2026)",
    "Euro area – 20 countries (2023-2025)",
    "Euro area - 19 countries (2015-2022)",
]
dep = dep[~dep["geo"].isin(excluir_dep)].copy()
dep = dep[["geo", "year", "value"]].rename(columns={"value": "dependency_pct"})

# ── 3. Carga precios de electricidad ──────────────────────────────────────────
prec = pd.read_csv(INPUT_PREC, parse_dates=["time"])
prec = prec[
    (prec["nrg_cons"] == "Consumption of kWh - all bands") &
    (prec["tax"]      == "All taxes and levies included") &
    (prec["currency"] == "Euro")
].copy()

excluir_prec = [
    "European Union - 27 countries (from 2020)",
    "Euro area (EA11-1999, EA12-2001, EA13-2007, EA15-2008, EA16-2009, EA17-2011, EA18-2014, EA19-2015, EA20-2023, EA21-2026)",
]
prec = prec[~prec["geo"].isin(excluir_prec)].copy()
prec["year"] = prec["time"].dt.year

# ── 4. Promedio anual de precios por país ─────────────────────────────────────
prec_anual = (
    prec.groupby(["geo", "year"])["value"]
    .mean()
    .reset_index()
    .rename(columns={"value": "avg_price_eur_kwh"})
)

# ── 5. Join dependencia + precios ─────────────────────────────────────────────
df = pd.merge(dep, prec_anual, on=["geo", "year"])
df = df[df["year"].between(2021, 2024)].copy()

# ── 6. Tabla 1: correlación general ───────────────────────────────────────────
correlacion = df[["dependency_pct", "avg_price_eur_kwh"]].corr()

# ── 7. Tabla 2: promedio 2021-2024 por país ───────────────────────────────────
resumen = (
    df.groupby("geo")
    .agg(
        avg_dependency=("dependency_pct", "mean"),
        avg_price=("avg_price_eur_kwh", "mean"),
        n_years=("year", "count")
    )
    .reset_index()
    .round(4)
)
resumen = resumen[resumen["n_years"] >= 2].sort_values("avg_dependency", ascending=False)
resumen = resumen[resumen["avg_dependency"] > -200].copy()

# ── 8. Tabla 3: países extremos ───────────────────────────────────────────────
alta_dep  = resumen.nlargest(5, "avg_dependency")[["geo", "avg_dependency", "avg_price"]]
baja_dep  = resumen.nsmallest(5, "avg_dependency")[["geo", "avg_dependency", "avg_price"]]

# ── 9. Resultados en consola ────────────────────────────────────────
print("=" * 60)
print("Análisis: Dependencia energética vs Precio de electricidad")
print("Período: 2021–2024")
print("=" * 60)

print("\n── Correlación general ──")
print(correlacion.to_string())

print("\n── Países con MAYOR dependencia energética ──")
print(alta_dep.to_string(index=False))

print("\n── Países con MENOR dependencia energética ──")
print(baja_dep.to_string(index=False))

print("\n── Tabla completa (ordenada por dependencia) ──")
print(resumen[["geo", "avg_dependency", "avg_price"]].to_string(index=False))

# ── 10. Guardar output ────────────────────────────────────────────────────────
df.to_csv(OUTPUT, index=False)
print(f"\n✅ Archivo guardado en: {OUTPUT}")