import pandas as pd
import pyodbc, os
from dotenv import load_dotenv

load_dotenv("data/SyJ/.env")
conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('SQLSERVER_HOST')}\\{os.getenv('SQLSERVER_INSTANCE')};DATABASE={os.getenv('SQLSERVER_DATABASE')};UID={os.getenv('SQLSERVER_USER')};PWD={os.getenv('SQLSERVER_PASSWORD')};TrustServerCertificate=yes;"
try:
    conn = pyodbc.connect(conn_str)
    print("TOP 5 PLACEBOS:")
    print(pd.read_sql("SELECT TOP 5 codigo_delito_carabineros FROM cch.denuncias WHERE codigo_delito_carabineros IN (702, 703, 705, 14020, 12077)", conn))
    print("TOTAL DISTINCT CUMS:")
    print(pd.read_sql("SELECT COUNT(DISTINCT codigo_delito_carabineros) as n FROM cch.denuncias", conn))
except Exception as e:
    print("Error:", e)
