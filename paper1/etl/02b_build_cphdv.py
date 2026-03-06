"""
02b_build_cphdv.py — ETL: Homicidios confirmados CPHDV
Proyecto v4.0 (rev.2)

Lee la Base del Centro para la Prevención de Homicidios y Delitos Violentos
(CPHDV), que reúne homicidios confirmados interinstitucionalmente (2018-2025).
Agrega a nivel región × año × mes y guarda como parquet.

Uso: Comparar con homicidios CCH (CUM 702+703+705) para validar consistencia
     y proveer cifra negra ≈ 0 a nivel regional.
"""

import pandas as pd
from pathlib import Path


REGION_MAP = {
    "Arica y Parinacota": 15,
    "Tarapacá": 1,
    "Antofagasta": 2,
    "Atacama": 3,
    "Coquimbo": 4,
    "Valparaíso": 5,
    "Metropolitana de Santiago": 13,
    "Libertador General Bernardo O'Higgins": 6,
    "O'Higgins": 6,
    "Maule": 7,
    "Ñuble": 16,
    "Biobío": 8,
    "La Araucanía": 9,
    "Los Ríos": 14,
    "Los Lagos": 10,
    "Aysén del Gral. Carlos Ibáñez del Campo": 11,
    "Aysén del General Carlos Ibáñez del Campo": 11,
    "Magallanes y de la Antártica Chilena": 12,
}


def main():
    input_path = Path("data/CPHDV/Base-VHC_2018_PS2025.xlsx")
    output_path = Path("paper1/output/data/cphdv_homicidios.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Reading CPHDV data from {input_path}...")
    df = pd.read_excel(input_path)
    print(f"  Raw shape: {df.shape}")

    # Map region names to numeric codes
    df["region"] = df["NOM_REG"].map(REGION_MAP)
    unmapped = df[df["region"].isna()]["NOM_REG"].unique()
    if len(unmapped) > 0:
        print(f"  WARNING: Unmapped regions: {unmapped}")
        # Try fuzzy matching for encoding issues
        for nom in unmapped:
            for key, val in REGION_MAP.items():
                if key.lower()[:10] in nom.lower()[:10] or nom.lower()[:10] in key.lower()[:10]:
                    df.loc[df["NOM_REG"] == nom, "region"] = val
                    print(f"    Fuzzy matched '{nom}' -> region {val}")
                    break

    df = df[df["region"].notna()].copy()
    df["region"] = df["region"].astype(int)
    df["year"] = df["ID_ANO"].astype(int)
    df["month"] = df["MES2"].astype(int)

    # Filter to 2018-2024 (exclude 2025 partial)
    df = df[df["year"].between(2018, 2024)]
    print(f"  After filtering 2018-2024: {len(df)} homicides")

    # Aggregate to region × year × month
    agg = (
        df.groupby(["region", "year", "month"])
        .size()
        .reset_index(name="n_homicidios_cphdv")
    )

    # Also create a national aggregate
    agg_nacional = (
        df.groupby(["year", "month"])
        .size()
        .reset_index(name="n_homicidios_cphdv")
    )
    agg_nacional["region"] = 0  # 0 = national

    agg_full = pd.concat([agg, agg_nacional], ignore_index=True)

    print(f"\nAggregated shape: {agg_full.shape}")
    print(f"Regions: {sorted(agg_full['region'].unique())}")
    print(f"\nAnnual totals (national):")
    print(agg_full[agg_full["region"] == 0].groupby("year")["n_homicidios_cphdv"].sum())

    print(f"\nSaving to {output_path}...")
    agg_full.to_parquet(output_path, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
