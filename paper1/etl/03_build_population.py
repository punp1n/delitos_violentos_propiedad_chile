"""
03_build_population.py — ETL: Denominador poblacional
Proyecto v4.0

Lee proyecciones INE (comuna → región), aplica corrección SERMIG,
e interpola linealmente a nivel mensual.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def build_ine_population():
    """Lee proyecciones INE y agrega a nivel regional-anual."""
    print("  Reading INE projections...")
    pop = pd.read_excel(
        "data/Poblacion_base_2017/estimaciones-y-proyecciones-2002-2035-comunas.xlsx",
        header=0,
    )
    # Columnas de población: 'Poblacion 2002' ... 'Poblacion 2035'
    pop_cols = [c for c in pop.columns if c.startswith("Poblacion")]
    pop_region = pop.groupby("Region")[pop_cols].sum().reset_index()

    # Reshape a long
    pop_long = pop_region.melt(
        id_vars="Region", var_name="year_col", value_name="pop_ine"
    )
    pop_long["year"] = pop_long["year_col"].str.extract(r"(\d+)").astype(int)
    pop_long = (
        pop_long[pop_long["year"].between(2014, 2025)]
        [["Region", "year", "pop_ine"]]
        .rename(columns={"Region": "region"})
    )
    return pop_long


def build_sermig_correction():
    """Lee SERMIG (RD + RT otorgadas), acumula desde 2018."""
    print("  Reading SERMIG data...")

    region_map = {
        "Arica y Parinacota": 15, "Tarapacá": 1, "Antofagasta": 2,
        "Atacama": 3, "Coquimbo": 4, "Valparaíso": 5,
        "Metropolitana de Santiago": 13, "O'Higgins": 6,
        "Maule": 7, "Ñuble": 16, "Biobío": 8,
        "La Araucanía": 9, "Los Ríos": 14, "Los Lagos": 10,
        "Aysén del Gral. Carlos Ibáñez del Campo": 11,
        "Magallanes y de la Antártica Chilena": 12,
    }

    frames = []
    for archivo, tipo in [
        ("data/SERMIG/Residencias_definitivas/RD-Resueltas-2o-semestre-2025.xlsx", "RD"),
        ("data/SERMIG/Residencias_temporales/RT-Resueltas-2o-semestre-2025.xlsx", "RT"),
    ]:
        try:
            df = pd.read_excel(archivo)
            # Filtrar solo otorgadas
            df = df[df["TIPO_RESUELTO"].str.strip().str.lower() == "otorga"].copy()
            # Mapear regiones
            df["region"] = df["REGIÓN"].map(region_map)
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
        return pd.DataFrame(columns=["region", "year", "sermig_cumul"])

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

    return sermig_full[["region", "year", "sermig_cumul"]]


def interpolate_monthly(pop_annual):
    """Interpola linealmente la población a nivel mensual."""
    print("  Interpolating monthly population...")
    rows = []
    for region in pop_annual["region"].unique():
        reg_data = pop_annual[pop_annual["region"] == region].sort_values("year")
        for _, row in reg_data.iterrows():
            year = int(row["year"])
            pop_corr = row["pop_corrected"]
            # Buscar pop del año siguiente
            next_row = reg_data[reg_data["year"] == year + 1]
            if len(next_row) > 0:
                pop_next = next_row["pop_corrected"].values[0]
            else:
                # Extrapolar con pendiente del año anterior
                prev_row = reg_data[reg_data["year"] == year - 1]
                if len(prev_row) > 0:
                    pop_next = pop_corr + (pop_corr - prev_row["pop_corrected"].values[0])
                else:
                    pop_next = pop_corr

            for month in range(1, 13):
                pop_monthly = pop_corr + (month - 6.5) / 12 * (pop_next - pop_corr)
                rows.append({
                    "region": int(region),
                    "year": year,
                    "month": month,
                    "pop_ine": row["pop_ine"],
                    "sermig_cumul": row["sermig_cumul"],
                    "pop_corrected": pop_corr,
                    "pop_monthly": max(pop_monthly, 1),  # floor at 1
                })

    return pd.DataFrame(rows)


def main():
    output_path = Path("paper1/output/data/poblacion_regional_mensual.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pop_ine = build_ine_population()
    sermig = build_sermig_correction()

    # Merge
    pop = pop_ine.merge(sermig, on=["region", "year"], how="left")
    pop["sermig_cumul"] = pop["sermig_cumul"].fillna(0)
    pop["pop_corrected"] = pop["pop_ine"] + pop["sermig_cumul"]

    # Filtrar a 2014-2024
    pop = pop[pop["year"].between(2014, 2024)]

    # Interpolar mensualmente
    pop_monthly = interpolate_monthly(pop)
    pop_monthly = pop_monthly[pop_monthly["year"].between(2014, 2024)]

    print(f"\nDataframe shape: {pop_monthly.shape}")
    print(f"Regiones: {pop_monthly['region'].nunique()}")
    print(f"\nSample (region 13, 2024):")
    sample = pop_monthly[(pop_monthly["region"] == 13) & (pop_monthly["year"] == 2024)]
    print(sample.to_string(index=False))

    print(f"\nSaving to {output_path}...")
    pop_monthly.to_csv(output_path, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
