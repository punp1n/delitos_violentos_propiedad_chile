"""
04_build_sermig.py — ETL: Corrección migratoria SERMIG
Proyecto v4.0

Lee archivos SERMIG (Residencias Definitivas + Temporales otorgadas),
acumula desde 2018, y guarda como CSV.

Output: sermig_correction.csv con columns [region, year, sermig_annual, sermig_cumul]
"""

import pandas as pd
import numpy as np
from pathlib import Path


REGION_MAP = {
    "Arica y Parinacota": 15, "Tarapacá": 1, "Antofagasta": 2,
    "Atacama": 3, "Coquimbo": 4, "Valparaíso": 5,
    "Metropolitana de Santiago": 13, "O'Higgins": 6,
    "Maule": 7, "Ñuble": 16, "Biobío": 8,
    "La Araucanía": 9, "Los Ríos": 14, "Los Lagos": 10,
    "Aysén del Gral. Carlos Ibáñez del Campo": 11,
    "Magallanes y de la Antártica Chilena": 12,
}

SERMIG_FILES = [
    ("data/SERMIG/Residencias_definitivas/RD-Resueltas-2o-semestre-2025.xlsx", "RD"),
    ("data/SERMIG/Residencias_temporales/RT-Resueltas-2o-semestre-2025.xlsx", "RT"),
]


def build_sermig_correction():
    """Lee SERMIG (RD + RT otorgadas), acumula desde 2018."""
    print("  Reading SERMIG data...")

    frames = []
    for archivo, tipo in SERMIG_FILES:
        try:
            df = pd.read_excel(archivo)
            # Filtrar solo otorgadas
            df = df[df["TIPO_RESUELTO"].str.strip().str.lower() == "otorga"].copy()
            # Mapear regiones
            df["region"] = df["REGIÓN"].map(REGION_MAP)
            df = df[df["region"].notna()].copy()
            df["region"] = df["region"].astype(int)
            df = df.rename(columns={"AÑO": "year"})
            # Agregar
            agg = df.groupby(["region", "year"]).agg(otorga=(df.columns[-2], "size")).reset_index()
            # Usar Total si existe
            if "Total" in df.columns:
                df["Total"] = pd.to_numeric(df["Total"], errors="coerce").fillna(0)
                agg = df.groupby(["region", "year"])["Total"].sum().reset_index()
                agg = agg.rename(columns={"Total": "otorga"})
            agg["tipo_residencia"] = tipo
            frames.append(agg)
        except Exception as e:
            print(f"  Warning reading {archivo}: {e}")

    if not frames:
        print("  No SERMIG data found. Returning empty correction.")
        return pd.DataFrame(columns=["region", "year", "sermig_annual", "sermig_cumul"])

    sermig = pd.concat(frames)
    sermig_agg = sermig.groupby(["region", "year"])["otorga"].sum().reset_index()
    sermig_agg = sermig_agg.rename(columns={"otorga": "sermig_annual"})

    # Acumular desde 2018
    all_regions = sermig_agg["region"].unique()
    all_years = range(2014, 2026)
    idx = pd.MultiIndex.from_product([all_regions, all_years], names=["region", "year"])
    sermig_full = sermig_agg.set_index(["region", "year"]).reindex(idx, fill_value=0).reset_index()
    sermig_full["sermig_annual"] = pd.to_numeric(sermig_full["sermig_annual"], errors="coerce").fillna(0)
    sermig_full.loc[sermig_full["year"] < 2018, "sermig_annual"] = 0
    sermig_full["sermig_cumul"] = (
        sermig_full.sort_values("year")
        .groupby("region")["sermig_annual"]
        .cumsum()
    )

    return sermig_full[["region", "year", "sermig_annual", "sermig_cumul"]]


def main():
    output_path = Path("paper1/output/data/sermig_correction.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sermig = build_sermig_correction()

    print(f"\nDataframe shape: {sermig.shape}")
    print(f"Regiones: {sermig['region'].nunique()}")
    print(f"\nSample (region 13):")
    sample = sermig[sermig["region"] == 13]
    print(sample.to_string(index=False))

    print(f"\nSaving to {output_path}...")
    sermig.to_csv(output_path, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
