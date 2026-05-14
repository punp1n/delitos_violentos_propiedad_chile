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
print("Extrayendo Perfiles de Detenidos...")
query_detenidos = f"""
    SELECT year, codigo_delito_carabineros, id_sexo, id_nacionalidad, id_estado_civil, id_nivel_educacional, id_tramo_etario, profesion_u_oficio, COUNT(id_hecho) as n_personas
    FROM cch.detenidos
    WHERE codigo_delito_carabineros IN ({query_in}) AND year >= 2014 AND year <= 2024
    AND comuna_ocurrencia_codigo IN ({comunas_str})
    GROUP BY year, codigo_delito_carabineros, id_sexo, id_nacionalidad, id_estado_civil, id_nivel_educacional, id_tramo_etario, profesion_u_oficio
"""
df_det = pd.read_sql(query_detenidos, conn)
conn.close()

# Categorizar violencia
df_det['violencia'] = df_det['codigo_delito_carabineros'].apply(lambda x: 'Violento' if str(x) in codigos_violentos else 'No Violento')

# Convertir código numérico de sexo a nominal tentativo (1=Hombre, 0/2=Mujer - a chequear diccionario ofcial después, por ahora mantenemos el ID)
# Agrupar por dimensiones
excel_path = os.path.join(out_dir, 'perfil_detenidos_cch.xlsx')
with pd.ExcelWriter(excel_path) as writer:
    # Por Género
    df_det.groupby(['year', 'violencia', 'id_sexo'])['n_personas'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Por_Sexo')
    # Por Tramo Etario
    df_det.groupby(['year', 'violencia', 'id_tramo_etario'])['n_personas'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Por_Edad')
    # Por Nacionalidad
    df_det.groupby(['year', 'violencia', 'id_nacionalidad'])['n_personas'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Por_Nacionalidad')
    # Por Estado Civil
    df_det.groupby(['year', 'violencia', 'id_estado_civil'])['n_personas'].sum().unstack(fill_value=0).to_excel(writer, sheet_name='Por_Estado_Civil')

print(f"Exportado exitosamente a {excel_path}")
