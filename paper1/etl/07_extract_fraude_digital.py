"""
07_extract_fraude_digital.py — ETL: Estafas y Fraude con Medios de Pago
Proyecto v4.0 (extensión exploratoria)

Extrae cuatro CUMs de fraude/estafa para evaluar si se integran al análisis:
  816   — Estafas y otras defraudaciones contra particulares (Art. 468, 467, 469, 470, 473)
  12151 — Uso fraudulento de tarjetas o medios de pago (código padre, pre-desagregación)
  12201 — Uso malicioso de tarjeta, clave o dispositivo financiero (Art. 7a, Ley 20.009)
  12202 — Obtención maliciosa o restitución de fondos de operaciones reclamadas

Nota: 12201 y 12202 son la desagregación post-2020 de 12151.
      El script los captura por separado y construye un total armonizado.

Salida:
  - Tabla resumen anual por CUM (stdout)
  - Tabla resumen anual total armonizado (stdout)
  - paper1/output/data/fraude_digital_panel_comuna_month.parquet
"""

import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
from pathlib import Path

# ─── CUMs objetivo ────────────────────────────────────────────────────────────
FRAUDE_CUMS = {816, 12151, 12201, 12202}

GLOSA_FRAUDE = {
    816:   "Estafas y otras defraudaciones contra particulares",
    12151: "Uso fraudulento de tarjetas o medios de pago (código padre)",
    12201: "Uso malicioso de tarjeta, clave o dispositivo financiero",
    12202: "Obtención maliciosa o restitución de fondos de operaciones reclamadas",
}

# Grupo armonizado para el análisis
# 12151 es el código padre; 12201+12202 son su desagregación posterior.
# Para series de tiempo coherentes, se suma todo bajo "Fraude_Tarjetas".
GRUPO_FRAUDE = {
    816:   "Estafas",
    12151: "Fraude_Tarjetas",
    12201: "Fraude_Tarjetas",
    12202: "Fraude_Tarjetas",
}


def get_connection():
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
        conn_str2 = conn_str.replace("ODBC Driver 18", "ODBC Driver 17")
        return pyodbc.connect(conn_str2)


def extract_fraude(conn):
    """Extrae denuncias para los CUMs de fraude a nivel comuna×mes×CUM."""
    cums_str = ",".join(str(c) for c in FRAUDE_CUMS)
    query = f"""
        SELECT
            comuna_ocurrencia_codigo AS comuna,
            year,
            id_mes                   AS month,
            codigo_materia           AS cum,
            COUNT(*)                 AS n_denuncias
        FROM cch.denuncias
        WHERE year >= 2013
          AND year <= 2025
          AND codigo_materia IN ({cums_str})
        GROUP BY comuna_ocurrencia_codigo, year, id_mes, codigo_materia
    """
    print("  Extrayendo denuncias de fraude digital...")
    return pd.read_sql(query, conn)


def build_annual_summary(df):
    """Construye tabla de frecuencias anuales por CUM y por grupo armonizado."""
    df["glosa"] = df["cum"].map(GLOSA_FRAUDE)
    df["grupo"] = df["cum"].map(GRUPO_FRAUDE)
    df["region"] = df["comuna"].astype(int) // 1000

    # ── Tabla 1: por CUM individual ──────────────────────────────────────────
    anual_cum = (
        df.groupby(["year", "cum", "glosa"])["n_denuncias"]
        .sum()
        .reset_index()
        .pivot(index=["cum", "glosa"], columns="year", values="n_denuncias")
        .fillna(0)
        .astype(int)
    )

    # ── Tabla 2: grupo armonizado (Estafas / Fraude_Tarjetas) ────────────────
    anual_grupo = (
        df.groupby(["year", "grupo"])["n_denuncias"]
        .sum()
        .reset_index()
        .pivot(index="grupo", columns="year", values="n_denuncias")
        .fillna(0)
        .astype(int)
    )

    # ── Tabla 3: total fraude digital (suma de ambos grupos) ─────────────────
    anual_total = (
        df.groupby("year")["n_denuncias"]
        .sum()
        .reset_index()
        .rename(columns={"n_denuncias": "total_fraude"})
    )

    # ── Tabla 4: comparación con no-violentos del C3 (si existe el panel) ───
    panel_path = Path("paper1/output/data/panel_region_month.parquet")
    anual_noviol = None
    if panel_path.exists():
        panel = pd.read_parquet(panel_path)
        anual_noviol = (
            panel.groupby("year")["n_robos_no_violentos"]
            .sum()
            .reset_index()
            .rename(columns={"n_robos_no_violentos": "no_violentos_c3"})
        )

    return anual_cum, anual_grupo, anual_total, anual_noviol


def print_results(anual_cum, anual_grupo, anual_total, anual_noviol):
    sep = "=" * 90

    print(f"\n{sep}")
    print("TABLA 1 — FRECUENCIAS ANUALES POR CUM (denuncias nacionales)")
    print(sep)
    print(anual_cum.to_string())

    print(f"\n{sep}")
    print("TABLA 2 — GRUPOS ARMONIZADOS: Estafas vs. Fraude_Tarjetas")
    print("(12151 + 12201 + 12202 consolidados como 'Fraude_Tarjetas')")
    print(sep)
    print(anual_grupo.to_string())

    print(f"\n{sep}")
    print("TABLA 3 — TOTAL FRAUDE DIGITAL (todos los CUMs)")
    print(sep)
    print(anual_total.to_string(index=False))

    if anual_noviol is not None:
        merged = anual_total.merge(anual_noviol, on="year", how="inner")
        merged["ratio_fraude_vs_noviol_%"] = (
            merged["total_fraude"] / merged["no_violentos_c3"] * 100
        ).round(1)
        print(f"\n{sep}")
        print("TABLA 4 — FRAUDE vs. ROBOS NO VIOLENTOS C3 (magnitud relativa)")
        print(sep)
        print(merged.to_string(index=False))


def main():
    output_path = Path("paper1/output/data/fraude_digital_panel_comuna_month.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Conectando a SQL Server...")
    conn = get_connection()
    try:
        df = extract_fraude(conn)
        print(f"  Registros extraídos: {len(df):,}")
    finally:
        conn.close()

    # Añadir variables de clasificación
    df["glosa"] = df["cum"].map(GLOSA_FRAUDE)
    df["grupo"] = df["cum"].map(GRUPO_FRAUDE)
    df["region"] = df["comuna"].astype(int) // 1000

    # Guardar parquet para uso posterior
    df.to_parquet(output_path, index=False)
    print(f"  Parquet guardado en: {output_path}")

    # Imprimir tablas de diagnóstico
    anual_cum, anual_grupo, anual_total, anual_noviol = build_annual_summary(df)
    print_results(anual_cum, anual_grupo, anual_total, anual_noviol)

    print("\nExtraccion completada.")


if __name__ == "__main__":
    main()
