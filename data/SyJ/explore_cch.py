import pandas as pd
import pyodbc
import warnings
warnings.filterwarnings('ignore')

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=10.94.2.32\\EXPLOT;"
    "DATABASE=SYJ_SCV_DEDS;"
    "UID=UsuarioSCV;"
    "PWD=F4TQD8pkNAUBI8TF;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    tables = ['cch.denuncias', 'cch.detenciones', 'cch.detenidos', 'cch.victimas']
    
    for table in tables:
        print(f"========================================\n--- Table: {table} ---")
        query = f"SELECT TOP 5 * FROM {table}"
        df = pd.read_sql(query, conn)
        
        print(f"Columns: {list(df.columns)}")
        print("Sample Data:")
        for idx, row in df.head(2).iterrows():
            print(row.to_dict())
            
    conn.close()
except Exception as e:
    import traceback
    print(f"Connection/Execution Error: {e}")
    traceback.print_exc()
