import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings('ignore')

load_dotenv()

conn_str = (
    f"DRIVER={{{os.getenv('SQLSERVER_DRIVER', 'ODBC Driver 18 for SQL Server')}}};"
    f"SERVER={os.getenv('SQLSERVER_HOST')}\\{os.getenv('SQLSERVER_INSTANCE')};"
    f"DATABASE={os.getenv('SQLSERVER_DATABASE')};"
    f"UID={os.getenv('SQLSERVER_USER')};"
    f"PWD={os.getenv('SQLSERVER_PASSWORD')};"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    
    print("Columns in cum.cnp_periodo:")
    df_cols = pd.read_sql("SELECT TOP 5 * FROM cum.cnp_periodo", conn)
    print(df_cols.to_string())

    print("\nColumns in cum.cnp_hist:")
    df_hist = pd.read_sql("SELECT TOP 5 * FROM cum.cnp_hist", conn)
    print(df_hist.to_string())

    conn.close()
except Exception as e:
    import traceback
    print("Failed with Driver 18. Trying Driver 17...")
    try:
        conn_str_17 = conn_str.replace("18", "17")
        conn = pyodbc.connect(conn_str_17)
        print("Columns in cum.cnp_periodo:")
        df_cols = pd.read_sql("SELECT TOP 5 * FROM cum.cnp_periodo", conn)
        print(df_cols.to_string())
        conn.close()
    except Exception as e2:
        print(f"Error: {e2}")
        traceback.print_exc()
