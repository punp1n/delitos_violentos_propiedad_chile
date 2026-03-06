import os
import pandas as pd

db_dir = r"C:\Users\Asvaldebenitom\OneDrive - Instituto Nacional de Estadisticas\Artículos\Trayectoria_delictual_Chile\data\ENUSC\DB_anuales\DB"

files = [
    (2016, "base-de-datos---enusc-xiii-2016cad748e69c24f439dbbe2379f53e71a.csv"),
    (2017, "base-de-datos---xiv-enusc-2017fab4413dfd354e599b78bcbb5b9467cd.csv"),
    (2018, "base-de-datos-xv-enusc-2018c69503c552fa4299b4e03274a6a347a5.csv"),
    (2019, "base-de-datos---xvi-enusc-2019-(csv).csv"),
    (2020, "base-usuario-17-enusc-2020-csv.csv"),
    (2021, "base-usuario-18-enusc-2021-csv.csv"),
    (2022, "base-usuario-19-enusc-2022596d21326fc149bb95ee810b74ce6e6a.csv"),
    (2023, "base-usuario-20-enusc-2023-FE-Actualizado-136.csv"),
    (2024, "base-de-datos---enusc-2024-csv.csv")
]

results = []

for year, filename in files:
    path = os.path.join(db_dir, filename)
    try:
        try:
            df_head = pd.read_csv(path, nrows=5, encoding='utf-8', sep=None, engine='python')
            enc = 'utf-8'
        except UnicodeDecodeError:
            df_head = pd.read_csv(path, nrows=5, encoding='latin-1', sep=None, engine='python')
            enc = 'latin-1'

        delimiter = ',' if ',' in ''.join(df_head.columns) else ';'
        
        # Look for possible comuna columns
        comuna_col = next((col for col in df_head.columns if 'comuna' in col.lower()), None)
        
        # Find expansion factor columns
        fact_cols = [col for col in df_head.columns if 'fact' in col.lower() or 'fe' in col.lower()]
        
        if comuna_col:
            df = pd.read_csv(path, usecols=[comuna_col], encoding=enc, sep=delimiter, engine='python')
            n_comunas = df[comuna_col].nunique()
            results.append(f"Year: {year} | N Comunas: {n_comunas} | Column used: {comuna_col} | Factor cols: {', '.join(fact_cols)}")
        else:
            results.append(f"Year: {year} | N Comunas: Not Found! | Columns: {list(df_head.columns[:10])} | Factor cols: {', '.join(fact_cols)}")
            
    except Exception as e:
        results.append(f"Year: {year} | Error reading file: {e}")

for res in results:
    print(res)
