"""
06_assemble_panel.py — ETL: Ensamblaje del Panel Final
Proyecto v4.0

Une CCH, Población Regional, e indicadores temporales (estallido, pandemia, trend).
"""

import pandas as pd
import numpy as np
from pathlib import Path


def main():
    print("Reading CCH panel...")
    cch = pd.read_parquet("paper1/output/data/cch_panel_comuna_month.parquet")
    print(f"CCH initial shape: {cch.shape}")

    print("Reading Population...")
    pop = pd.read_csv("paper1/output/data/poblacion_regional_mensual.csv")
    print(f"Pop initial shape: {pop.shape}")

    print("Aggregating CCH to region-month by classification C3...")
    # Agregamos denuncias (que son la VD) por región, mes y categoría C3
    cch_agg = cch.groupby(["region", "year", "month", "C3_categoria"])["n_denuncias"].sum().reset_index()

    # Pivotamos para que cada categoría sea una columna
    cch_pivot = cch_agg.pivot_table(
        index=["region", "year", "month"],
        columns="C3_categoria",
        values="n_denuncias",
        fill_value=0
    ).reset_index()

    # Renombramos explícitamente a formato analítico
    renames = {
        "Violencia Dura": "n_violencia_dura",
        "Sorpresa": "n_sorpresa",
        "No Violento": "n_no_violento"
    }
    cch_pivot = cch_pivot.rename(columns=renames)

    print("Merging CCH with Population...")
    
    # Agregar C1 y C2 a la base final
    c1_agg = cch[cch["C1_violento"] == 1.0].groupby(["region", "year", "month"])["n_denuncias"].sum().reset_index(name="n_violento_c1")
    c2_agg = cch[cch["C2_violento"] == 1.0].groupby(["region", "year", "month"])["n_denuncias"].sum().reset_index(name="n_violento_c2")
    
    cch_pivot = cch_pivot.merge(c1_agg, on=["region", "year", "month"], how="left").fillna({"n_violento_c1": 0})
    cch_pivot = cch_pivot.merge(c2_agg, on=["region", "year", "month"], how="left").fillna({"n_violento_c2": 0})

    panel = cch_pivot.merge(pop, on=["region", "year", "month"], how="left")

    print("Creating time variables and dummies...")
    panel["yyyymm"] = panel["year"] * 100 + panel["month"]
    panel = panel.sort_values(["region", "yyyymm"]).reset_index(drop=True)

    # Trend continuo (1, 2, 3...)
    fechas_unicas = sorted(panel["yyyymm"].unique())
    mapa_trend = {d: i + 1 for i, d in enumerate(fechas_unicas)}
    panel["trend_t"] = panel["yyyymm"].map(mapa_trend)

    # Dummies de shocks exógenos
    # Estallido Social: Octubre 2019 - Marzo 2020
    panel["d_estallido"] = ((panel["yyyymm"] >= 201910) & (panel["yyyymm"] <= 202003)).astype(int)
    
    # Pandemia COVID-19: Abril 2020 - Diciembre 2021 (fijado por diseño v4.0)
    panel["d_pandemia"] = ((panel["yyyymm"] >= 202004) & (panel["yyyymm"] <= 202112)).astype(int)

    # Dummy para estacionalidad mensual
    panel["month_of_year"] = panel["month"]

    # Variable de macrozona — criterio geográfico (rev.2)
    # Norte: Arica, Tarapacá, Antofagasta, Atacama, Coquimbo
    # Centro: Valparaíso, O'Higgins, Maule
    # Sur: Ñuble, Biobío, La Araucanía, Los Ríos
    # Austral: Los Lagos, Aysén, Magallanes
    # RM: Región Metropolitana (sin macrozona)
    macrozona_map = {
        15: "Norte", 1: "Norte", 2: "Norte", 3: "Norte", 4: "Norte",
        5: "Centro", 6: "Centro", 7: "Centro",
        16: "Sur", 8: "Sur", 9: "Sur", 14: "Sur",
        10: "Austral", 11: "Austral", 12: "Austral",
        13: "RM",
    }
    panel["macrozona"] = panel["region"].map(macrozona_map)
    
    # Para Componente 1b, sería útil tener todo esto a nivel de comuna, 
    # pero el diseño base evalúa variancia a nivel regional. 
    # Dejamos este script para panel regional y lo usamos en 02_main_poisson_wcb.R

    output_path = Path("paper1/output/data/panel_region_month.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\nFinal Panel shape: {panel.shape}")
    print("\nSample (RM 2024):")
    sample = panel[(panel["region"] == 13) & (panel["year"] == 2024)].head(3)
    print(sample[["region", "yyyymm", "n_violencia_dura", "pop_monthly", "trend_t", "d_pandemia"]].to_string())

    print(f"\nSaving to {output_path}...")
    panel.to_parquet(output_path, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
