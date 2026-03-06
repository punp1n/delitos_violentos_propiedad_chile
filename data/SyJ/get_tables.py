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
    query = "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
    df = pd.read_sql(query, conn)
    print("Tables:")
    print(df.to_string())

    print("\nColumns in cch.denuncias:")
    df_cols = pd.read_sql("SELECT TOP 1 * FROM cch.denuncias", conn)
    print(df_cols.columns.tolist())

    conn.close()
except Exception as e:
    import traceback
    print("Failed with Driver 17. Trying Driver 18...")
    try:
        conn_str_18 = conn_str.replace("17", "18")
        conn = pyodbc.connect(conn_str_18)
        query = "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
        df = pd.read_sql(query, conn)
        print("Tables:")
        print(df.to_string())

        print("\nColumns in cch.denuncias:")
        df_cols = pd.read_sql("SELECT TOP 1 * FROM cch.denuncias", conn)
        print(df_cols.columns.tolist())
        conn.close()
    except Exception as e2:
        print(f"Failed with Driver 18: {e2}")
        traceback.print_exc()
