"""
06b_assemble_communal_panel.py -- balanced commune-month CCH panel.

Builds the 345 x 156 balanced panel used for communal robustness models.
Population is INE 2017-base commune population, interpolated monthly. SERMIG is
not applied at commune level.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from cum_classification import add_classifications


CCH_PATH = Path("paper1/output/data/cch_panel_comuna_month.parquet")
POP_PATH = Path("paper1/output/data/poblacion_comunal_mensual.csv")
OUTPUT_PATH = Path("paper1/output/data/panel_comuna_month.parquet")


def identify_periods(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["yyyymm"] = out["year"] * 100 + out["month"]
    out["d_estallido"] = ((out["yyyymm"] >= 201910) & (out["yyyymm"] <= 202002)).astype(int)
    out["d_pandemia"] = ((out["yyyymm"] >= 202003) & (out["yyyymm"] <= 202112)).astype(int)
    out["month_of_year"] = out["month"]
    out["trend_t"] = (out["year"] - 2013) * 12 + out["month"]
    return out


def add_macrozona(df: pd.DataFrame) -> pd.DataFrame:
    macrozona_map = {
        15: "Norte", 1: "Norte", 2: "Norte", 3: "Norte", 4: "Norte",
        5: "Centro", 6: "Centro", 7: "Centro",
        16: "Sur", 8: "Sur", 9: "Sur", 14: "Sur", 10: "Sur",
        11: "Austral", 12: "Austral",
        13: "RM",
    }
    out = df.copy()
    out["macrozona"] = out["region"].map(macrozona_map)
    return out


def pivot_category(df: pd.DataFrame, value_col: str, prefix: str) -> pd.DataFrame:
    modelable = df[df["c3_modelable"]].copy()
    agg = (
        modelable.groupby(["comuna", "year", "month", "C3_categoria"], dropna=False)[value_col]
        .sum()
        .reset_index()
    )
    piv = (
        agg.pivot_table(
            index=["comuna", "year", "month"],
            columns="C3_categoria",
            values=value_col,
            fill_value=0,
        )
        .reset_index()
    )
    return piv.rename(
        columns={
            "confrontational": f"{prefix}_confrontational",
            "snatching": f"{prefix}_snatching",
            "non_confrontational": f"{prefix}_non_confrontational",
        }
    )


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    print("Reading CCH and commune population...")
    cch = pd.read_parquet(CCH_PATH)
    pop = pd.read_csv(POP_PATH)
    if "c3_modelable" not in cch.columns:
        cch = add_classifications(cch)

    communes = sorted(cch["comuna"].astype(int).unique())
    grid = pd.MultiIndex.from_product(
        [communes, range(2013, 2026), range(1, 13)],
        names=["comuna", "year", "month"],
    ).to_frame(index=False)

    den = pivot_category(cch, "n_denuncias", "n")
    det = pivot_category(cch, "n_detenciones", "n_det")
    panel = grid.merge(den, on=["comuna", "year", "month"], how="left")
    panel = panel.merge(det, on=["comuna", "year", "month"], how="left")
    count_cols = [c for c in panel.columns if c.startswith("n_")]
    panel[count_cols] = panel[count_cols].fillna(0)

    c1 = (
        cch[cch["C1_violento"] == 1.0]
        .groupby(["comuna", "year", "month"])["n_denuncias"]
        .sum()
        .reset_index(name="n_violento_c1")
    )
    c2 = (
        cch[cch["C2_violento"] == 1.0]
        .groupby(["comuna", "year", "month"])["n_denuncias"]
        .sum()
        .reset_index(name="n_violento_c2")
    )
    excluded = (
        cch[~cch["c3_modelable"]]
        .groupby(["comuna", "year", "month"])["n_denuncias"]
        .sum()
        .reset_index(name="n_excluded_receptacion")
    )
    panel = panel.merge(c1, on=["comuna", "year", "month"], how="left")
    panel = panel.merge(c2, on=["comuna", "year", "month"], how="left")
    panel = panel.merge(excluded, on=["comuna", "year", "month"], how="left")
    panel[["n_violento_c1", "n_violento_c2", "n_excluded_receptacion"]] = (
        panel[["n_violento_c1", "n_violento_c2", "n_excluded_receptacion"]].fillna(0)
    )

    panel = panel.merge(pop, on=["comuna", "year", "month"], how="left")
    panel = identify_periods(panel)
    panel = add_macrozona(panel)

    panel["n_robos_violentos"] = panel["n_confrontational"]
    panel["n_robos_sorpresa"] = panel["n_snatching"]
    panel["n_robos_no_violentos"] = panel["n_non_confrontational"]
    panel["n_det_violentos"] = panel["n_det_confrontational"]
    panel["n_det_sorpresa"] = panel["n_det_snatching"]
    panel["n_det_no_violentos"] = panel["n_det_non_confrontational"]
    panel["n_total_composition"] = panel["n_confrontational"] + panel["n_non_confrontational"]
    panel["share_confrontational"] = np.where(
        panel["n_total_composition"] > 0,
        panel["n_confrontational"] / panel["n_total_composition"],
        np.nan,
    )
    panel["dense_commune"] = (
        panel.groupby("comuna")["n_confrontational"].transform("mean") >= 1
    )

    panel = panel.sort_values(["comuna", "yyyymm"]).reset_index(drop=True)
    print(f"\nRows: {len(panel)}")
    print(f"Communes: {panel['comuna'].nunique()}")
    print(f"Regions: {panel['region'].nunique()}")
    print(f"Missing population rows: {panel['pop_monthly_comuna'].isna().sum()}")
    print(f"Dense communes: {panel[['comuna', 'dense_commune']].drop_duplicates()['dense_commune'].sum()}")
    print(f"Saving to {OUTPUT_PATH}...")
    panel.to_parquet(OUTPUT_PATH, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
