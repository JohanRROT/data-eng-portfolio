# scripts/transformacion/04_analisis_renovables.py
# Pregunta: ¿Qué países lideran la transición renovable?

import pandas as pd
from pathlib import Path

# ── 1. Rutas ──────────────────────────────────────────────────────────────────
ROOT  = Path(__file__).resolve().parent.parent.parent
INPUT = ROOT / "data" / "processed" / "eurostat" / "renewables_share.csv"
OUTPUT_DIR = ROOT / "data" / "analytical"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT = OUTPUT_DIR / "renewables_leaders.csv"

# ── 2. Carga ──────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT, parse_dates=["time"])

# ── 3. Filtrar solo métrica principal ─────────────────────────────────────────
df = df[df["nrg_bal"] == "Renewable energy - overall"].copy()

# ── 4. Excluir agregados regionales ───────────────────────────────────────────
# ── 4. Excluir agregados regionales ───────────────────────────────────────────
excluir = [
    "European Union - 27 countries (from 2020)",
    "Euro area – 21 countries (from 2026)",
    "Euro area – 20 countries (2023-2025)",
]
df = df[~df["geo"].isin(excluir)].copy()

# ── 5. Extraer año ────────────────────────────────────────────────────────────
df["year"] = df["time"].dt.year

# ── 6. Tabla 1: evolución anual por país ──────────────────────────────────────
evolucion = (
    df[["geo", "year", "value"]]
    .rename(columns={"value": "renewables_pct"})
    .sort_values(["geo", "year"])
)

# ── 7. Tabla 2: ranking por valor más reciente (2024) ─────────────────────────
ultimo_anio = df["year"].max()
ranking = (
    df[df["year"] == ultimo_anio][["geo", "value"]]
    .rename(columns={"value": "renewables_pct_2024"})
    .sort_values("renewables_pct_2024", ascending=False)
    .reset_index(drop=True)
)
ranking.index += 1
ranking.index.name = "rank"

# ── 8. Tabla 3: crecimiento 2004 → 2024 ──────────────────────────────────────
anio_base = df["year"].min()

base = (
    df[df["year"] == anio_base][["geo", "value"]]
    .rename(columns={"value": "pct_2004"})
)
final = (
    df[df["year"] == ultimo_anio][["geo", "value"]]
    .rename(columns={"value": "pct_2024"})
)

crecimiento = pd.merge(base, final, on="geo")
crecimiento["crecimiento_pp"] = (
    crecimiento["pct_2024"] - crecimiento["pct_2004"]
).round(2)
crecimiento = crecimiento.sort_values("crecimiento_pp", ascending=False).reset_index(drop=True)

# ── 9. Resultados en consola ──────────────────────────────────────────────────
print("=" * 60)
print(f"Año base: {anio_base} | Año final: {ultimo_anio}")
print(f"Países analizados: {df['geo'].nunique()}")
print("=" * 60)

print("\n── Top 10 países por % renovables en 2024 ──")
print(ranking.head(10).to_string())

print("\n── Top 10 países por crecimiento 2004→2024 (puntos porcentuales) ──")
print(crecimiento.head(10).to_string())

# ── 10. Guardar output ────────────────────────────────────────────────────────
evolucion.to_csv(OUTPUT, index=False)
print(f"\n✅ Archivo guardado en: {OUTPUT}")