"""
extract_eurostat.py
-------------------
Ingesta de datos energéticos desde la API REST de Eurostat.
Datasets:
    - nrg_pc_204  : Precios electricidad hogares
    - nrg_ind_ren : Participación energías renovables
    - ten00124    : Consumo final de energía por sector
    - nrg_ind_id  : Dependencia energética por país
"""

import requests
import pandas as pd
import json
import time
from pathlib import Path

# ── Configuración ──────────────────────────────────────────────────────────────
BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
OUTPUT_DIR = Path("data/raw/eurostat")

DATASETS = {
    "electricity_prices":   "nrg_pc_204",
    "renewables_share":     "nrg_ind_ren",
    "energy_consumption":   "ten00124",
    "energy_dependency":    "nrg_ind_id",
}

# ── Funciones ──────────────────────────────────────────────────────────────────
def fetch_dataset(code: str) -> dict:
    """
    Llama a la API de Eurostat y devuelve el JSON crudo.
    
    Args:
        code: Código del dataset en Eurostat
    Returns:
        dict con el JSON de respuesta
    """
    url = f"{BASE_URL}/{code}?format=JSON&lang=EN"
    print(f"  Descargando {code}...")
    
    response = requests.get(url, timeout=60)
    response.raise_for_status()  # Lanza error si status != 200
    
    return response.json()


def parse_jsonstat(data: dict, name: str) -> pd.DataFrame:
    """
    Convierte el formato JSON-stat de Eurostat a un DataFrame de pandas.
    
    JSON-stat es un formato de cubo multidimensional donde:
    - 'dimension': contiene las categorías de cada eje
    - 'value': contiene los valores en orden secuencial
    
    Args:
        data: JSON crudo de la API
        name: Nombre del dataset para logs
    Returns:
        DataFrame con los datos en formato tabular
    """
    print(f"  Procesando {name}...")
    
    # Extraer dimensiones y sus categorías
    dimensions = data['dimension']
    dim_names  = list(dimensions.keys())
    dim_sizes  = data['size']
    
    # Construir índice MultiIndex con todas las combinaciones posibles
    categories = []
    for dim in dim_names:
        cats = list(dimensions[dim]['category']['label'].values())
        categories.append(cats)
    
    # Crear todas las combinaciones de dimensiones
    index = pd.MultiIndex.from_product(categories, names=dim_names)
    
    # Los valores vienen como dict {posición: valor} — rellenar huecos con NaN
    total = 1
    for s in dim_sizes:
        total *= s
    
    values = [data['value'].get(str(i), None) for i in range(total)]
    
    # Crear DataFrame
    df = pd.Series(values, index=index, name='value').reset_index()
    df['dataset'] = name
    
    return df


def save_raw(df: pd.DataFrame, name: str) -> Path:
    """
    Guarda el DataFrame como CSV en data/raw/eurostat/
    
    Args:
        df: DataFrame a guardar
        name: Nombre del archivo (sin extensión)
    Returns:
        Path del archivo guardado
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"  Guardado: {path} ({len(df):,} filas)")
    return path


# ── Pipeline principal ─────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("EXTRACCIÓN DE DATOS ENERGÉTICOS — EUROSTAT API")
    print("=" * 60)
    
    resultados = {}
    
    for name, code in DATASETS.items():
        print(f"\n[{name}]")
        try:
            # 1. Descargar
            raw_json = fetch_dataset(code)
            
            # 2. Parsear
            df = parse_jsonstat(raw_json, name)
            
            # 3. Guardar
            path = save_raw(df, name)
            
            resultados[name] = {
                "filas": len(df),
                "columnas": list(df.columns),
                "path": str(path)
            }
            
            # Pausa entre requests para no sobrecargar la API
            time.sleep(2)
            
        except Exception as e:
            print(f"  ❌ Error en {name}: {e}")
            resultados[name] = {"error": str(e)}
    
    # Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DE EXTRACCIÓN")
    print("=" * 60)
    for name, info in resultados.items():
        if "error" in info:
            print(f"  ❌ {name}: {info['error']}")
        else:
            print(f"  ✅ {name}: {info['filas']:,} filas → {info['path']}")


if __name__ == "__main__":
    main()