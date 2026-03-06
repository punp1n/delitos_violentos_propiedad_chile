import pandas as pd
import pyodbc, os
from dotenv import load_dotenv

load_dotenv("data/SyJ/.env")
conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('SQLSERVER_HOST')}\\{os.getenv('SQLSERVER_INSTANCE')};DATABASE={os.getenv('SQLSERVER_DATABASE')};UID={os.getenv('SQLSERVER_USER')};PWD={os.getenv('SQLSERVER_PASSWORD')};TrustServerCertificate=yes;"
try:
    conn = pyodbc.connect(conn_str)
    query = """
    SELECT cum, glosa_cum, glosa_ine
    FROM cum.cnp_periodo
    WHERE cum IN (202, 235, 236, 237, 248, 249)
    AND periodo_id = (SELECT MAX(periodo_id) FROM cum.cnp_periodo)
    """
    df = pd.read_sql(query, conn)
    print("Glosas de Secuestro encontradas:")
    print(df.to_string(index=False))
except Exception as e:
    print("Error:", e)
