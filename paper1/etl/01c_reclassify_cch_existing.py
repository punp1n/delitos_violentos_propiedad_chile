"""
01c_reclassify_cch_existing.py -- apply canonical CUM classification to current
CCH long parquet when SQL extraction is not available in the local environment.

This does not replace 01_extract_cch.py. It is a deterministic reclassification
step over the already extracted raw CCH commune-month-CUM panel.
"""

from pathlib import Path

import pandas as pd

from cum_classification import add_classifications


PATH = Path("paper1/output/data/cch_panel_comuna_month.parquet")


def main() -> None:
    df = pd.read_parquet(PATH)
    drop_cols = [c for c in ["C1_violento", "C2_violento", "C3_categoria", "c3_modelable", "excluded_reason"] if c in df.columns]
    df = df.drop(columns=drop_cols)
    df = add_classifications(df)
    df.to_parquet(PATH, index=False)
    print(f"Reclassified {len(df):,} rows in {PATH}")
    print(df.groupby(["C3_categoria", "c3_modelable"], dropna=False)["n_denuncias"].sum().to_string())


if __name__ == "__main__":
    main()
