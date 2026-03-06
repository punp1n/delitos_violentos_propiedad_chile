import os
import pandas as pd
import pyodbc
import warnings
warnings.filterwarnings('ignore')

out_dir = r"C:\Users\Asvaldebenitom\OneDrive - Instituto Nacional de Estadisticas\Artículos\Trayectoria_delictual_Chile\resultados\exploratorio\resultados"
os.makedirs(out_dir, exist_ok=True)

# 1. Cargar las 102 comunas
comunas_path = r"C:\Users\Asvaldebenitom\OneDrive - Instituto Nacional de Estadisticas\Artículos\Trayectoria_delictual_Chile\data\ENUSC\comunas_102_historicas.csv"
com102_df = pd.read_csv(comunas_path)
comunas_102 = com102_df['cod_comuna'].tolist()
comunas_str = ",".join([str(c) for c in comunas_102])

# 2. Conexión SQL CCH
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=10.94.2.32\\EXPLOT;"
    "DATABASE=SYJ_SCV_DEDS;"
    "UID=UsuarioSCV;"
    "PWD=F4TQD8pkNAUBI8TF;"
    "TrustServerCertificate=yes;"
)

codigos_violentos = ['802','803','804','827','828','829','861','862','867']
codigos_no_violentos = ['808','809','810','812','821','826','831','846','847','848',
                        '853','858','864','868','869','870','871','872','891','892',
                        '2009','12053','13028']
query_in = ", ".join([f"'{c}'" for c in codigos_violentos + codigos_no_violentos])

conn = pyodbc.connect(conn_str)
print("Extrayendo Denuncias (Temporal)...")
query_denuncias = f"""
    SELECT year, id_mes, id_dia, id_tramo_horario, codigo_delito_carabineros, COUNT(id_hecho) as n_casos
    FROM cch.denuncias
    WHERE codigo_delito_carabineros IN ({query_in}) AND year >= 2014 AND year <= 2024
    AND comuna_ocurrencia_codigo IN ({comunas_str})
    GROUP BY year, id_mes, id_dia, id_tramo_horario, codigo_delito_carabineros
"""
df_den = pd.read_sql(query_denuncias, conn)

print("Extrayendo Detenciones en Flagrancia (Temporal)...")
query_detenciones = f"""
    SELECT year, id_mes, id_dia, id_tramo_horario, codigo_delito_carabineros, COUNT(id_hecho) as n_casos
    FROM cch.detenciones
    WHERE codigo_delito_carabineros IN ({query_in}) AND year >= 2014 AND year <= 2024
    AND comuna_ocurrencia_codigo IN ({comunas_str})
    GROUP BY year, id_mes, id_dia, id_tramo_horario, codigo_delito_carabineros
"""
df_det = pd.read_sql(query_detenciones, conn)
conn.close()

# Categorizar violencia
df_den['tipo_hecho'] = 'Denuncia'
df_den['violencia'] = df_den['codigo_delito_carabineros'].apply(lambda x: 'Violento' if str(x) in codigos_violentos else 'No Violento')

df_det['tipo_hecho'] = 'Detencion Flagrancia'
df_det['violencia'] = df_det['codigo_delito_carabineros'].apply(lambda x: 'Violento' if str(x) in codigos_violentos else 'No Violento')

# Output Excel con Múltiples Pestañas para Denuncias y Detenciones Flagrancia separadas
excel_path = os.path.join(out_dir, 'tendencias_temporales_cch.xlsx')
with pd.ExcelWriter(excel_path) as writer:
    # 1. Denuncias por Mes
    df_den.groupby(['year', 'violencia', 'id_mes'])['n_casos'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Denuncias_Mes')
    # 2. Denuncias por Dia
    df_den.groupby(['year', 'violencia', 'id_dia'])['n_casos'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Denuncias_Dia')
    # 3. Denuncias por Tramo Horario
    df_den.groupby(['year', 'violencia', 'id_tramo_horario'])['n_casos'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Denuncias_Tramo')
    
    # 4. Detenciones Flagrancia por Mes
    df_det.groupby(['year', 'violencia', 'id_mes'])['n_casos'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Flagrancia_Mes')
    # 5. Detenciones Flagrancia por Dia
    df_det.groupby(['year', 'violencia', 'id_dia'])['n_casos'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Flagrancia_Dia')
    # 6. Detenciones Flagrancia por Tramo
    df_det.groupby(['year', 'violencia', 'id_tramo_horario'])['n_casos'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Flagrancia_Tramo')

print(f"Exportado exitosamente a {excel_path}")
