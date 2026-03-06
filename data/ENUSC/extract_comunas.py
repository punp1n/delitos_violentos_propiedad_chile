import pandas as pd

try:
    path = r"C:\Users\Asvaldebenitom\OneDrive - Instituto Nacional de Estadisticas\Artículos\Trayectoria_delictual_Chile\data\ENUSC\DB_anuales\DB\base-usuario-20-enusc-2023-FE-Actualizado-136.csv"
    df = pd.read_csv(path, sep=';', encoding='latin-1', usecols=['enc_rpc', 'com102'])
    
    comunas_102 = df[df['com102'] == 1]['enc_rpc'].unique()
    comunas_102.sort()
    
    out_path = r"C:\Users\Asvaldebenitom\OneDrive - Instituto Nacional de Estadisticas\Artículos\Trayectoria_delictual_Chile\data\ENUSC\comunas_102_historicas.csv"
    pd.Series(comunas_102, name='cod_comuna').to_csv(out_path, index=False)
    print(f"Extraction successful: {len(comunas_102)} comunas saved to {out_path}")
except Exception as e:
    print("Error:", e)
