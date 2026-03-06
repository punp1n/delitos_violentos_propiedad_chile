"""
02_extract_placebos.py — ETL: Extracción de series placebo
Proyecto v4.0 (rev.2)

Extrae denuncias de delitos placebo:
  P1: Cuasidelito vehicular (CUM 14020) — proxy de movilidad
  P2: Homicidios dolosos (CUM 702, 703, 705) — cifra negra ≈ 0
  P4: Daños simples (CUM 840) — propensión a denunciar estable
  P5: Lesiones leves (CUM 13001) — control no-propiedad, no-violento grave
  Complemento: No dar cuenta de accidente (CUM 12077)
  Complemento: Secuestros (CUM 202, 235, 236, 237, 248, 249)
"""

import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
from pathlib import Path


# CUM codes for placebos
PLACEBOS = {
    "cuasidelito_vehicular": [14020],
    "homicidio_doloso":      [702, 703, 705],
    "no_dar_cuenta_accid":   [12077],
    "secuestro":             [202, 235, 236, 237, 248, 249],
    "danos_simples":         [840],
    "lesiones_leves":        [13001],
}

ALL_PLACEBO_CUMS = [c for cums in PLACEBOS.values() for c in cums]


def get_connection():
    load_dotenv("data/SyJ/.env")
    conn_str = (
        f"DRIVER={{{os.getenv('SQLSERVER_DRIVER', 'ODBC Driver 18 for SQL Server')}}};"
        f"SERVER={os.getenv('SQLSERVER_HOST')}\\{os.getenv('SQLSERVER_INSTANCE')};"
        f"DATABASE={os.getenv('SQLSERVER_DATABASE')};"
        f"UID={os.getenv('SQLSERVER_USER')};"
        f"PWD={os.getenv('SQLSERVER_PASSWORD')};"
        "TrustServerCertificate=yes;"
    )
    try:
        return pyodbc.connect(conn_str)
    except pyodbc.Error:
        print("Trying ODBC Driver 17...")
        return pyodbc.connect(conn_str.replace("18", "17"))


def extract_placebos(conn):
    """Extrae denuncias de delitos placebo agrupadas por región×mes."""
    cums_str = ",".join(str(c) for c in ALL_PLACEBO_CUMS)
    query = f"""
        SELECT
            comuna_ocurrencia_codigo,
            year,
            id_mes AS month,
            codigo_delito_carabineros AS cum,
            COUNT(*) AS n_denuncias
        FROM cch.denuncias
        WHERE year >= 2014 AND year <= 2024
          AND codigo_delito_carabineros IN ({cums_str})
        GROUP BY comuna_ocurrencia_codigo, year, id_mes, codigo_delito_carabineros
    """
    print("  Extracting placebo denuncias...")
    df = pd.read_sql(query, conn)

    # Compute region from comuna
    df["region"] = df["comuna_ocurrencia_codigo"].astype(int) // 1000
    df["cum"] = df["cum"].astype(int)

    # Map CUM to placebo category
    cum_to_tipo = {}
    for tipo, cums in PLACEBOS.items():
        for c in cums:
            cum_to_tipo[c] = tipo
    df["tipo_placebo"] = df["cum"].map(cum_to_tipo)

    # Aggregate by region×month×tipo_placebo
    df_agg = (
        df.groupby(["region", "year", "month", "tipo_placebo"])
        .agg(n_denuncias=("n_denuncias", "sum"))
        .reset_index()
    )
    return df_agg


def main():
    output_path = Path("paper1/output/data/placebo_panel.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    try:
        df = extract_placebos(conn)
        print(f"\nDataframe shape: {df.shape}")
        print(f"Tipos placebo: {df['tipo_placebo'].unique()}")
        print(f"\nResumen anual:")
        print(df.groupby(["year", "tipo_placebo"])["n_denuncias"].sum().unstack(fill_value=0))
        print(f"\nSaving to {output_path}...")
        df.to_parquet(output_path, index=False)
        print("Done.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
