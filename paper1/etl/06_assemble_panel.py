"""
06_assemble_panel.py -- audited regional panel assembly.

Builds the region-month panel from the long CCH file and regional monthly
population. Receptacion is kept in the long audit file but excluded from the C3
modelable categories. No residual Unknown column is exported.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from cum_classification import add_classifications


MONTHS = pd.MultiIndex.from_product(
    [range(1, 17), range(2013, 2026), range(1, 13)],
    names=["region", "year", "month"],
).to_frame(index=False)


def identify_periods(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["yyyymm"] = out["year"] * 100 + out["month"]
    out["d_estallido"] = ((out["yyyymm"] >= 201910) & (out["yyyymm"] <= 202002)).astype(int)
    out["d_pandemia"] = ((out["yyyymm"] >= 202003) & (out["yyyymm"] <= 202112)).astype(int)
    out["month_of_year"] = out["month"]
    out["trend_t"] = (out["year"] - 2013) * 12 + out["month"]

    conditions = [
        out["yyyymm"] < 201601,
        (out["yyyymm"] >= 201601) & (out["yyyymm"] <= 201909),
        (out["yyyymm"] >= 201910) & (out["yyyymm"] <= 202002),
        (out["yyyymm"] >= 202003) & (out["yyyymm"] <= 202112),
        out["yyyymm"] >= 202201,
    ]
    choices = ["Pre-base", "Linea base", "Estallido", "Pandemia", "Reciente"]
    out["period_cat"] = np.select(conditions, choices, default="Unknown")
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
        modelable.groupby(["region", "year", "month", "C3_categoria"], dropna=False)[value_col]
        .sum()
        .reset_index()
    )
    piv = (
        agg.pivot_table(
            index=["region", "year", "month"],
            columns="C3_categoria",
            values=value_col,
            fill_value=0,
        )
        .reset_index()
    )
    rename = {
        "confrontational": f"{prefix}_confrontational",
        "snatching": f"{prefix}_snatching",
        "non_confrontational": f"{prefix}_non_confrontational",
    }
    return piv.rename(columns=rename)


def build_panel(cch_path: str, pop_path: str) -> pd.DataFrame:
    print("Reading CCH and population...")
    cch = pd.read_parquet(cch_path)
    pop = pd.read_csv(pop_path)

    if "c3_modelable" not in cch.columns or "C3_categoria" not in cch.columns:
        cch = add_classifications(cch)

    cch["cum"] = cch["cum"].astype(int)
    cch = cch[cch["year"].between(2013, 2025)].copy()

    den = pivot_category(cch, "n_denuncias", "n")
    det = pivot_category(cch, "n_detenciones", "n_det")
    panel = MONTHS.merge(den, on=["region", "year", "month"], how="left")
    panel = panel.merge(det, on=["region", "year", "month"], how="left")

    count_cols = [c for c in panel.columns if c.startswith("n_")]
    panel[count_cols] = panel[count_cols].fillna(0)

    c1 = (
        cch[cch["C1_violento"] == 1.0]
        .groupby(["region", "year", "month"])["n_denuncias"]
        .sum()
        .reset_index(name="n_violento_c1")
    )
    c2 = (
        cch[cch["C2_violento"] == 1.0]
        .groupby(["region", "year", "month"])["n_denuncias"]
        .sum()
        .reset_index(name="n_violento_c2")
    )
    excluded = (
        cch[~cch["c3_modelable"]]
        .groupby(["region", "year", "month"])["n_denuncias"]
        .sum()
        .reset_index(name="n_excluded_receptacion")
    )

    panel = panel.merge(c1, on=["region", "year", "month"], how="left")
    panel = panel.merge(c2, on=["region", "year", "month"], how="left")
    panel = panel.merge(excluded, on=["region", "year", "month"], how="left")
    panel[["n_violento_c1", "n_violento_c2", "n_excluded_receptacion"]] = (
        panel[["n_violento_c1", "n_violento_c2", "n_excluded_receptacion"]].fillna(0)
    )

    # Legacy aliases kept for current models; new aliases support revised models.
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

    panel = panel.merge(pop, on=["region", "year", "month"], how="left")
    panel = identify_periods(panel)
    panel = add_macrozona(panel)
    panel = panel.sort_values(["region", "yyyymm"]).reset_index(drop=True)

    return panel


def main() -> None:
    output_path = Path("paper1/output/data/panel_region_month.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    panel = build_panel(
        "paper1/output/data/cch_panel_comuna_month.parquet",
        "paper1/output/data/poblacion_regional_mensual.csv",
    )

    print(f"\nFinal Panel shape: {panel.shape}")
    print(f"Regions: {panel['region'].nunique()}")
    print(f"Missing population rows: {panel['pop_monthly'].isna().sum()}")
    print("Columns:", list(panel.columns))
    print(f"\nSaving to {output_path}...")
    panel.to_parquet(output_path, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
