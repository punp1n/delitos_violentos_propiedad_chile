"""
03c_build_communal_population.py -- communal monthly population.

Reads INE 2017-base commune projections, aggregates sex-age rows to commune-year
totals, and linearly interpolates annual totals to commune-month.

The modelling universe is restricted to the 345 communes observed in CCH/SAE.
Antartica (12202) exists in INE projections but is absent from CCH and SAE and is
therefore excluded from the default output.
"""

from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data/Poblacion_base_2017/estimaciones-y-proyecciones-2002-2035-comunas.xlsx")
CCH_PATH = Path("paper1/output/data/cch_panel_comuna_month.parquet")
OUTPUT_PATH = Path("paper1/output/data/poblacion_comunal_mensual.csv")


def cch_commune_universe() -> set[int]:
    if not CCH_PATH.exists():
        return set()
    cch = pd.read_parquet(CCH_PATH, columns=["comuna"])
    return set(cch["comuna"].astype(int).unique())


def build_annual_population() -> pd.DataFrame:
    print("Reading INE commune projections...")
    pop = pd.read_excel(INPUT_PATH)
    pop_cols = [c for c in pop.columns if str(c).startswith("Poblacion ")]

    annual = (
        pop.groupby(["Region", "Nombre Region", "Comuna", "Nombre Comuna"], as_index=False)[pop_cols]
        .sum()
        .rename(
            columns={
                "Region": "region",
                "Nombre Region": "region_name",
                "Comuna": "comuna",
                "Nombre Comuna": "comuna_name",
            }
        )
    )

    long = annual.melt(
        id_vars=["region", "region_name", "comuna", "comuna_name"],
        var_name="year_col",
        value_name="pop_ine_comuna",
    )
    long["year"] = long["year_col"].str.extract(r"(\d{4})").astype(int)
    long = long[long["year"].between(2013, 2025)].copy()
    return long[["region", "region_name", "comuna", "comuna_name", "year", "pop_ine_comuna"]]


def interpolate_monthly(pop_annual: pd.DataFrame) -> pd.DataFrame:
    print("Interpolating commune-month population...")
    rows = []
    for comuna, g in pop_annual.groupby("comuna"):
        g = g.sort_values("year")
        meta = g.iloc[0][["region", "region_name", "comuna_name"]].to_dict()
        for _, row in g.iterrows():
            year = int(row["year"])
            pop_this = float(row["pop_ine_comuna"])
            next_row = g[g["year"] == year + 1]
            if len(next_row):
                pop_next = float(next_row["pop_ine_comuna"].iloc[0])
            else:
                prev_row = g[g["year"] == year - 1]
                pop_next = pop_this + (pop_this - float(prev_row["pop_ine_comuna"].iloc[0])) if len(prev_row) else pop_this
            for month in range(1, 13):
                pop_monthly = pop_this + (month - 6.5) / 12 * (pop_next - pop_this)
                rows.append(
                    {
                        "comuna": int(comuna),
                        "region": int(meta["region"]),
                        "region_name": meta["region_name"],
                        "comuna_name": meta["comuna_name"],
                        "year": year,
                        "month": month,
                        "pop_ine_comuna": pop_this,
                        "pop_monthly_comuna": max(pop_monthly, 1),
                    }
                )
    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    annual = build_annual_population()
    universe = cch_commune_universe()
    if universe:
        annual = annual[annual["comuna"].isin(universe)].copy()
    monthly = interpolate_monthly(annual)
    monthly = monthly[monthly["year"].between(2013, 2025)].copy()

    print(f"\nRows: {len(monthly)}")
    print(f"Communes: {monthly['comuna'].nunique()}")
    print(f"Regions: {monthly['region'].nunique()}")
    print(f"Missing population: {monthly['pop_monthly_comuna'].isna().sum()}")
    print(f"Saving to {OUTPUT_PATH}...")
    monthly.to_csv(OUTPUT_PATH, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
