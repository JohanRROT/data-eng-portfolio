import pandas as pd
from ydata_profiling import ProfileReport
import os

datasets = {
    "electricity_prices": "data/raw/eurostat/electricity_prices.csv",
    "energy_dependency": "data/raw/eurostat/energy_dependency.csv",
    "renewables_share": "data/raw/eurostat/renewables_share.csv",
    "energy_consumption": "data/raw/eurostat/energy_consumption.csv",
}

os.makedirs("docs/profiling", exist_ok=True)

for nombre, ruta in datasets.items():
    print(f"Procesando: {nombre}...")
    df = pd.read_csv(ruta)
    perfil = ProfileReport(df, title=nombre, minimal=True)
    perfil.to_file(f"docs/profiling/{nombre}_report.html")
    print(f"  ✓ Reporte guardado: docs/profiling/{nombre}_report.html")

print("\nTodos los reportes generados.")