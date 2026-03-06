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


# ──────────────────────────────────────────────
# Clasificaciones de delitos contra la propiedad
# ──────────────────────────────────────────────

# CUM que conforman "Violento" en la clasificación institucional (SPD/CAPJ)
VIOLENTO_C1 = {802, 803, 804, 827, 828, 829, 861, 862, 867}

# CUM que conforman "No Violento" en C1 (incluye receptación)
NO_VIOLENTO_C1 = {
    808, 809, 810,                          # Robos en lugar
    812, 864, 869, 2009, 12053,             # Receptación
    821, 826, 846, 847, 848, 853, 13028,    # Hurtos
    831, 868,                               # Robo de vehículo s/v
    858,                                    # Cajeros automáticos
    870, 871,                               # Robos/hurtos en calamidad
    872,                                    # Saqueo
    891, 892,                               # Sustracción de madera
}

# CUM de receptación (excluidos en C2 y C3)
RECEPTACION = {812, 864, 869, 2009, 12053}

# CUM de "Violencia Dura" en C3 (subconjunto de VIOLENTO_C1)
VIOLENCIA_DURA_C3 = {802, 803, 827, 828, 829, 861, 862, 867}

# CUM de "Sorpresa" en C3
SORPRESA_C3 = {804}

# Universo completo de CUM del estudio
ALL_TARGET_CUMS = VIOLENTO_C1 | NO_VIOLENTO_C1


def get_connection():
    """Establece conexión SQL Server usando credenciales .env."""
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


def extract_police_data(conn):
    """Extrae denuncias y detenciones agrupadas por comuna×mes×CUM."""
    query = """
        SELECT
            comuna_ocurrencia_codigo,
            year,
            id_mes             AS month,
            codigo_delito_carabineros AS cum,
            '{tipo}'           AS tipo_caso,
            COUNT(*)           AS cant
        FROM cch.{tabla}
        WHERE year >= 2014 AND year <= 2024
        GROUP BY comuna_ocurrencia_codigo, year, id_mes, codigo_delito_carabineros
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


def calculate_classifications(df):
    """
    Añade tres clasificaciones como columnas:
      C1_violento  — dummy binaria institucional SPD/CAPJ (incluye receptación)
      C2_violento  — dummy binaria ajustada (excluye receptación)
      C3_categoria — tricotómica: 'Violencia Dura' / 'Sorpresa' / 'No Violento'
    """
    # C1: Institucional SPD/CAPJ
    df["C1_violento"] = df["cum"].map(
        lambda c: 1 if c in VIOLENTO_C1
        else (0 if c in NO_VIOLENTO_C1 else None)
    )

    # C2: Ajustada (excluye receptación → NaN)
    df["C2_violento"] = df["cum"].map(
        lambda c: None if c in RECEPTACION
        else (1 if c in VIOLENTO_C1
              else (0 if c in NO_VIOLENTO_C1 else None))
    )

    # C3: Tricotómica (excluye receptación → NaN)
    def _map_c3(cum):
        if cum in VIOLENCIA_DURA_C3:
            return "Violencia Dura"
        if cum in SORPRESA_C3:
            return "Sorpresa"
        if cum in (NO_VIOLENTO_C1 - RECEPTACION):
            return "No Violento"
        return None

    df["C3_categoria"] = df["cum"].apply(_map_c3)
    return df


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

    # Aplicar clasificaciones
    df_final = calculate_classifications(df_final)

    # Filtrar al universo de delitos contra la propiedad
    df_final = df_final[df_final["cum"].isin(ALL_TARGET_CUMS)].copy()

    # Reordenar columnas
    cols = [
        "comuna", "region", "year", "month", "cum", "glosa_cum", "glosa_ine",
        "C1_violento", "C2_violento", "C3_categoria",
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
