"""
01_extract_cch.py — ETL: Extracción CCH (Carabineros de Chile)
Proyecto v4.0: Cambio Estructural en Delitos Violentos contra la Propiedad

Extrae denuncias y detenciones de la BD SQL, clasifica según tres esquemas
(C1 institucional, C2 ajustada, C3 tricotómica), agrega a nivel
comuna × región × mes × CUM, y guarda como parquet.
"""

import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
import argparse
from pathlib import Path
from cum_classification import ALL_PROPERTY_CUMS, add_classifications


def get_connection():
    """Establece conexión SQL Server usando credenciales .env."""
    load_dotenv("data/SyJ/.env")
    conn_str = (
        f"DRIVER={{{os.getenv('SQLSERVER_DRIVER', 'ODBC Driver 17 for SQL Server')}}};"
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


def extract_police_data(conn):
    """Extrae denuncias y detenciones agrupadas por comuna×mes×CUM."""
    query = """
        SELECT
            comuna_ocurrencia_codigo,
            year,
            id_mes             AS month,
            codigo_materia     AS cum,
            '{tipo}'           AS tipo_caso,
            COUNT(*)           AS cant
        FROM cch.{tabla}
        WHERE year >= 2013 AND year <= 2025
        GROUP BY comuna_ocurrencia_codigo, year, id_mes, codigo_materia
    """
    print("  Extracting denuncias...")
    df_den = pd.read_sql(query.format(tipo="denuncia", tabla="denuncias"), conn)
    print("  Extracting detenciones...")
    df_det = pd.read_sql(query.format(tipo="detencion", tabla="detenciones"), conn)
    return pd.concat([df_den, df_det], ignore_index=True)


def extract_cum_catalog(conn):
    """Extrae catálogo CUM (período más reciente)."""
    print("  Extracting CUM catalog...")
    return pd.read_sql("""
        SELECT cum, glosa_cum, glosa_ine
        FROM cum.cnp_periodo
        WHERE periodo_id = (SELECT MAX(periodo_id) FROM cum.cnp_periodo)
    """, conn)


def process_data(df_combined, df_cum):
    """Pivota, agrega, y clasifica el panel CCH."""
    print("Processing data...")

    # Añadir comuna y región
    df_combined["comuna"] = df_combined["comuna_ocurrencia_codigo"].astype(int)
    df_combined["region"] = df_combined["comuna"] // 1000

    # Pivotar tipo_caso → n_denuncias / n_detenciones
    df_pivot = (
        df_combined
        .pivot_table(
            index=["comuna", "region", "year", "month", "cum"],
            columns="tipo_caso",
            values="cant",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )
    for col in ("denuncia", "detencion"):
        if col not in df_pivot.columns:
            df_pivot[col] = 0
    df_pivot = df_pivot.rename(columns={"denuncia": "n_denuncias", "detencion": "n_detenciones"})

    # Merge con catálogo CUM
    df_pivot["cum"] = df_pivot["cum"].astype(int)
    df_cum["cum"] = df_cum["cum"].fillna(0).astype(int)
    df_final = df_pivot.merge(df_cum, on="cum", how="left")

    # Aplicar clasificaciones canonicas
    df_final = add_classifications(df_final)

    # Filtrar al universo de delitos contra la propiedad
    df_final = df_final[df_final["cum"].isin(ALL_PROPERTY_CUMS)].copy()

    # Reordenar columnas
    cols = [
        "comuna", "region", "year", "month", "cum", "glosa_cum", "glosa_ine",
        "C1_violento", "C2_violento", "C3_categoria", "c3_modelable", "excluded_reason",
        "n_denuncias", "n_detenciones",
    ]
    df_final = df_final[[c for c in cols if c in df_final.columns]]

    return df_final


def main():
    parser = argparse.ArgumentParser(description="Extract CCH panel data (v4.0)")
    parser.add_argument(
        "--output",
        default="paper1/output/data/cch_panel_comuna_month.parquet",
        help="Output Parquet path",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    try:
        df_police = extract_police_data(conn)
        df_cum = extract_cum_catalog(conn)
        df_panel = process_data(df_police, df_cum)

        # Resumen
        print(f"\nDataframe shape: {df_panel.shape}")
        print(f"Comunas:  {df_panel['comuna'].nunique()}")
        print(f"Regiones: {df_panel['region'].nunique()}")
        print(f"Período:  {df_panel['year'].min()}-{df_panel['year'].max()}")
        print(f"\nClasificaciones (sample):")
        sample = (
            df_panel[["cum", "glosa_cum", "C1_violento", "C2_violento", "C3_categoria"]]
            .drop_duplicates()
            .sort_values("cum")
        )
        print(sample.to_string(index=False))
        print(f"\nDenuncias por C3:")
        print(df_panel.groupby("C3_categoria")["n_denuncias"].sum())
        print(f"\nSaving to {output_path}...")
        df_panel.to_parquet(output_path, index=False)
        print("Done.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
