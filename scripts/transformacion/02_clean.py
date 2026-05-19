import pandas as pd
import os

os.makedirs("data/processed/eurostat", exist_ok=True)

# ── 1. FUNCIONES AUXILIARES ──────────────────────────────────────────

def limpiar_base(df):
    if "dataset" in df.columns:
        df = df.drop(columns=["dataset"])
    df = df.dropna(subset=["value"])
    return df

def convertir_tiempo_anual(df):
    df["time"] = pd.to_datetime(df["time"], format="%Y")
    return df

def convertir_tiempo_semestral(df):
    df["year"] = df["time"].str[:4].astype(int)
    df["semester"] = df["time"].str[-1].astype(int)
    df["time"] = pd.to_datetime(df["year"].astype(str) + "-" +
                                df["semester"].map({1: "01", 2: "07"}))
    df = df.drop(columns=["year", "semester"])
    return df

# ── 2. LIMPIEZA POR DATASET ──────────────────────────────────────────

# renewables_share
df = pd.read_csv("data/raw/eurostat/renewables_share.csv")
df = limpiar_base(df)
df = convertir_tiempo_anual(df)
df.to_csv("data/processed/eurostat/renewables_share.csv", index=False)
print(f"renewables_share:   {len(df)} filas → data/processed/eurostat/")

# energy_consumption
df = pd.read_csv("data/raw/eurostat/energy_consumption.csv")
df = limpiar_base(df)
df = convertir_tiempo_anual(df)
df.to_csv("data/processed/eurostat/energy_consumption.csv", index=False)
print(f"energy_consumption: {len(df)} filas → data/processed/eurostat/")

# energy_dependency
df = pd.read_csv("data/raw/eurostat/energy_dependency.csv")
df = limpiar_base(df)
df = convertir_tiempo_anual(df)
df.to_csv("data/processed/eurostat/energy_dependency.csv", index=False)
print(f"energy_dependency:  {len(df)} filas → data/processed/eurostat/")

# electricity_prices
df = pd.read_csv("data/raw/eurostat/electricity_prices.csv")
df = limpiar_base(df)
df = convertir_tiempo_semestral(df)
print(f"  Valores negativos en prices: {(df['value'] < 0).sum()}")
df.to_csv("data/processed/eurostat/electricity_prices.csv", index=False)
print(f"electricity_prices: {len(df)} filas → data/processed/eurostat/")

print("\n✓ Limpieza completada.")