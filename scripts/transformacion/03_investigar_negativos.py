# scripts/transformacion/03_investigar_negativos.py
# Objetivo: investigar los ~102 valores negativos en electricity_prices

import pandas as pd
from pathlib import Path

# ── 1. Rutas ──────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent
INPUT = ROOT / "data" / "processed" / "eurostat" / "electricity_prices.csv"

# ── 2. Carga ──────────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT)

# ── 3. Filtrar negativos ──────────────────────────────────────────────────────
negativos = df[df["value"] < 0].copy()

# ── 4. Resumen general ────────────────────────────────────────────────────────
print("=" * 60)
print(f"Total de valores negativos: {len(negativos)}")
print("=" * 60)

# ── 5. ¿En qué países aparecen? ───────────────────────────────────────────────
print("\n── Por país (geo) ──")
print(negativos["geo"].value_counts().to_string())

# ── 6. ¿En qué período de tiempo? ────────────────────────────────────────────
print("\n── Por año ──")
negativos["year"] = pd.to_datetime(negativos["time"]).dt.year
print(negativos["year"].value_counts().sort_index().to_string())

# ── 7. ¿En qué banda de consumo? ─────────────────────────────────────────────
print("\n── Por banda de consumo (nrg_cons) ──")
print(negativos["nrg_cons"].value_counts().to_string())

# ── 8. ¿Con o sin impuestos? ──────────────────────────────────────────────────
print("\n── Por régimen fiscal (tax) ──")
print(negativos["tax"].value_counts().to_string())

# ── 9. Muestra de filas negativas ────────────────────────────────────────────
print("\n── Muestra de 10 filas negativas ──")
print(negativos[["geo", "time", "nrg_cons", "tax", "value"]].head(10).to_string())

# ── 10. Rango de valores negativos ───────────────────────────────────────────
print("\n── Rango de los valores negativos ──")
print(f"  Mínimo : {negativos['value'].min()}")
print(f"  Máximo : {negativos['value'].max()}")
print(f"  Media  : {negativos['value'].mean():.6f}")