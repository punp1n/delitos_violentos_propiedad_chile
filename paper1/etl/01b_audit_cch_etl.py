"""
01b_audit_cch_etl.py -- QA report for CCH ETL.

Outputs:
  - paper1/output/tables/cch_etl_audit_report.csv
  - paper1/output/tables/cch_cum_totals.csv
  - paper1/output/tables/cch_validation_checks.csv
  - paper1/output/tables/cum_classification_table.csv
"""

from pathlib import Path

import pandas as pd

from cum_classification import ALL_PROPERTY_CUMS, add_classifications, classification_table


CCH_PATH = Path("paper1/output/data/cch_panel_comuna_month.parquet")
OUT_DIR = Path("paper1/output/tables")


EXPECTED_CHECKS = [
    {"cum": 804, "year": 2025, "region": None, "expected_n_denuncias": 35678, "label": "CUM 804 national 2025"},
    {"cum": 804, "year": 2025, "region": 5, "expected_n_denuncias": 2399, "label": "CUM 804 Valparaiso 2025"},
    {"cum": 808, "year": 2025, "region": None, "expected_n_denuncias": 55543, "label": "CUM 808 national 2025"},
    {"cum": 808, "year": 2025, "region": 13, "expected_n_denuncias": 28121, "label": "CUM 808 RM 2025"},
]


def validation_checks(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for chk in EXPECTED_CHECKS:
        q = df[(df["cum"] == chk["cum"]) & (df["year"] == chk["year"])]
        if chk["region"] is not None:
            q = q[q["region"] == chk["region"]]
        observed = int(q["n_denuncias"].sum())
        expected = int(chk["expected_n_denuncias"])
        rows.append(
            {
                **chk,
                "observed_n_denuncias": observed,
                "diff": observed - expected,
                "passed": observed == expected,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(CCH_PATH)
    df["cum"] = df["cum"].astype(int)
    if "c3_modelable" not in df.columns or "excluded_reason" not in df.columns:
        df = add_classifications(df.drop(columns=[c for c in ["C1_violento", "C2_violento", "C3_categoria"] if c in df.columns]))

    comuna_month_observed = df[["comuna", "year", "month"]].drop_duplicates().shape[0]
    comuna_n = df["comuna"].nunique()
    expected_comuna_month = comuna_n * 13 * 12
    region_month_observed = df[["region", "year", "month"]].drop_duplicates().shape[0]
    expected_region_month = df["region"].nunique() * 13 * 12

    report = pd.DataFrame(
        [
            {"metric": "rows_long_cum", "value": len(df), "expected": None, "passed": True},
            {"metric": "regions", "value": df["region"].nunique(), "expected": 16, "passed": df["region"].nunique() == 16},
            {"metric": "communes", "value": comuna_n, "expected": 345, "passed": comuna_n == 345},
            {"metric": "cums", "value": df["cum"].nunique(), "expected": len(ALL_PROPERTY_CUMS), "passed": df["cum"].nunique() == len(ALL_PROPERTY_CUMS)},
            {"metric": "region_month_observed", "value": region_month_observed, "expected": expected_region_month, "passed": region_month_observed == expected_region_month},
            {"metric": "commune_month_observed_with_events", "value": comuna_month_observed, "expected": expected_comuna_month, "passed": comuna_month_observed == expected_comuna_month},
            {"metric": "missing_c3_category", "value": int(df["C3_categoria"].isna().sum()), "expected": 0, "passed": int(df["C3_categoria"].isna().sum()) == 0},
            {"metric": "excluded_receptacion_rows", "value": int((df["excluded_reason"] == "receptacion").sum()), "expected": None, "passed": True},
            {"metric": "excluded_receptacion_denuncias", "value": int(df.loc[df["excluded_reason"] == "receptacion", "n_denuncias"].sum()), "expected": None, "passed": True},
        ]
    )

    cum_totals = (
        df.groupby(["cum", "glosa_ine", "C1_violento", "C2_violento", "C3_categoria", "c3_modelable", "excluded_reason"], dropna=False)
        .agg(n_denuncias=("n_denuncias", "sum"), n_detenciones=("n_detenciones", "sum"))
        .reset_index()
        .sort_values("cum")
    )
    checks = validation_checks(df)
    checks_ok = bool(checks["passed"].all())
    report = pd.concat(
        [
            report,
            pd.DataFrame([{"metric": "known_cum_count_checks", "value": int(checks["passed"].sum()), "expected": len(checks), "passed": checks_ok}]),
        ],
        ignore_index=True,
    )

    report.to_csv(OUT_DIR / "cch_etl_audit_report.csv", index=False)
    cum_totals.to_csv(OUT_DIR / "cch_cum_totals.csv", index=False)
    checks.to_csv(OUT_DIR / "cch_validation_checks.csv", index=False)
    classification_table().to_csv(OUT_DIR / "cum_classification_table.csv", index=False)

    print(report.to_string(index=False))
    print("\nValidation checks:")
    print(checks.to_string(index=False))
    if not checks_ok:
        raise SystemExit("Known CUM validation checks failed.")


if __name__ == "__main__":
    main()
