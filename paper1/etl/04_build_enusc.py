"""
04_build_enusc.py — ETL: Procesamiento ENUSC interanual
Proyecto v4.0

Lee base interanual 2008-2024, filtra a 2016-2024 y 102 comunas históricas,
crea variables de victimización y selecciona factores de expansión.
"""

import pandas as pd
from pathlib import Path


def load_enusc():
    """Lee la base interanual ENUSC con parsing correcto."""
    print("  Reading ENUSC interanual CSV (this may take a minute)...")
    df = pd.read_csv(
        "data/ENUSC/Interanual_2008_2024/base-de-datos---interanual-2008---2024.csv",
        sep=";",
        decimal=",",
        low_memory=False,
    )
    print(f"  Raw shape: {df.shape}")
    print(f"  Columns sample: {df.columns[:20].tolist()}")

    # Normalizar nombres a minúscula
    df.columns = df.columns.str.strip().str.lower()
    return df


def process_enusc(df):
    """Filtra, construye variables de victimización y selecciona factor de expansión."""

    # Filtrar a 2016-2024
    if "año" in df.columns:
        year_col = "año"
    elif "ano" in df.columns:
        year_col = "ano"
    else:
        # Try to find year column
        candidates = [c for c in df.columns if "año" in c.lower() or "ano" in c.lower() or "year" in c.lower()]
        year_col = candidates[0] if candidates else None
        if year_col is None:
            raise ValueError(f"Cannot find year column. Available: {df.columns.tolist()}")

    print(f"  Year column: '{year_col}'")
    print(f"  Years available: {sorted(df[year_col].unique())}")

    df = df[df[year_col].between(2016, 2024)].copy()
    print(f"  After year filter: {df.shape}")

    # Filtrar a 102 comunas históricas
    if "com102" in df.columns:
        df = df[df["com102"] == 1].copy()
        print(f"  After com102 filter: {df.shape}")

    # Variables de victimización
    for var in ["rvi", "rps", "rfv", "hur"]:
        if var in df.columns:
            df[var] = pd.to_numeric(df[var], errors="coerce")
        else:
            print(f"  Warning: variable '{var}' not found")

    # Construir variables de victimización
    if "rvi" in df.columns:
        df["victim_hard"] = df["rvi"].clip(0, 1)
    if "rps" in df.columns and "rvi" in df.columns:
        df["victim_violent"] = df[["rvi", "rps"]].max(axis=1).clip(0, 1)
    if "rfv" in df.columns and "hur" in df.columns:
        df["victim_nonviolent"] = df[["rfv", "hur"]].max(axis=1).clip(0, 1)

    # Seleccionar factor de expansión según período
    # 2016-2018: fact_hog_2008_2019
    # 2019-2022: fact_hog_2019_2024
    # 2023-2024: fact_hog_2023_2024
    weight_candidates = {
        "fact_hog_2008_2019": None,
        "fact_hog_2019_2024": None,
        "fact_hog_2023_2024": None,
    }
    for wc in list(weight_candidates.keys()):
        matches = [c for c in df.columns if wc in c.lower()]
        if matches:
            weight_candidates[wc] = matches[0]

    print(f"  Weight columns found: {weight_candidates}")

    # Create unified weight column
    df["weight"] = None
    w1 = weight_candidates.get("fact_hog_2008_2019")
    w2 = weight_candidates.get("fact_hog_2019_2024")
    w3 = weight_candidates.get("fact_hog_2023_2024")

    if w1:
        df.loc[df[year_col].between(2016, 2018), "weight"] = df.loc[df[year_col].between(2016, 2018), w1]
    if w2:
        df.loc[df[year_col].between(2019, 2022), "weight"] = df.loc[df[year_col].between(2019, 2022), w2]
    if w3:
        df.loc[df[year_col].between(2023, 2024), "weight"] = df.loc[df[year_col].between(2023, 2024), w3]

    # If weight is still None for some rows, try any available factor
    if df["weight"].isna().any():
        fallback = w2 or w1 or w3
        if fallback:
            df["weight"] = df["weight"].fillna(df[fallback])

    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")

    # Variables de diseño muestral
    design_vars = ["varstrat", "conglomerado", "region16"]
    for dv in design_vars:
        if dv not in df.columns:
            matches = [c for c in df.columns if dv in c.lower()]
            if matches:
                df = df.rename(columns={matches[0]: dv})

    # Seleccionar columnas finales
    keep_cols = [
        year_col, "region16", "varstrat", "conglomerado", "weight",
        "victim_violent", "victim_hard", "victim_nonviolent",
    ]
    # Add RVI_DENUNCIA if exists (for reporting behavior analysis)
    denuncia_cols = [c for c in df.columns if "denuncia" in c.lower()]
    keep_cols.extend(denuncia_cols)

    existing = [c for c in keep_cols if c in df.columns]
    df_out = df[existing].copy()

    if year_col != "año":
        df_out = df_out.rename(columns={year_col: "año"})

    return df_out


def main():
    output_path = Path("paper1/output/data/enusc_microdata_filtered.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = load_enusc()
    df_out = process_enusc(df)

    print(f"\nFinal shape: {df_out.shape}")
    print(f"Years: {sorted(df_out['año'].unique())}")
    print(f"Regions: {sorted(df_out['region16'].unique()) if 'region16' in df_out.columns else 'N/A'}")
    print(f"\nVictimization summary:")
    for var in ["victim_violent", "victim_hard", "victim_nonviolent"]:
        if var in df_out.columns:
            print(f"  {var}: mean={df_out[var].mean():.4f}, n_valid={df_out[var].notna().sum()}")

    print(f"\nSaving to {output_path}...")
    df_out.to_parquet(output_path, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
