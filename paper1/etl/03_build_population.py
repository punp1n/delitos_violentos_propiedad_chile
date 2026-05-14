"""
03_build_population.py — ETL: Denominador poblacional
Proyecto v4.0

Lee proyecciones INE (comuna → región), aplica corrección SERMIG
(importada de 04_build_sermig.py), e interpola linealmente a nivel mensual.
"""

import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Agregar directorio actual al path para permitir importar 04_build_sermig
sys.path.insert(0, str(Path(__file__).parent))
from importlib import import_module
_sermig_mod = import_module("04_build_sermig")
build_sermig_correction = _sermig_mod.build_sermig_correction


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
        pop_long[pop_long["year"].between(2013, 2025)]
        [["Region", "year", "pop_ine"]]
        .rename(columns={"Region": "region"})
    )
    return pop_long


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

    # Filtrar a 2013-2025
    pop = pop[pop["year"].between(2013, 2025)]

    # Interpolar mensualmente
    pop_monthly = interpolate_monthly(pop)
    pop_monthly = pop_monthly[pop_monthly["year"].between(2013, 2025)]

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
