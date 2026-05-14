from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from patsy import dmatrix
from scipy import stats


ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "paper1" / "output" / "tables" / "C3"
FIGURE_DIR = ROOT / "paper1" / "output" / "figures"
DATA_DIR = ROOT / "paper1" / "output" / "data"


def ensure_output_dirs() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)


def read_region_panel() -> pd.DataFrame:
    df = pd.read_parquet(DATA_DIR / "panel_region_month.parquet")
    return prepare_panel(df, region_col="region")


def read_commune_panel() -> pd.DataFrame:
    df = pd.read_parquet(DATA_DIR / "panel_comuna_month.parquet")
    return prepare_panel(df, region_col="region", commune_col="comuna")


def prepare_panel(
    df: pd.DataFrame,
    region_col: str = "region",
    commune_col: str | None = None,
) -> pd.DataFrame:
    out = df.copy()
    out["date"] = pd.to_datetime(
        out["year"].astype(int).astype(str) + "-" + out["month"].astype(int).astype(str) + "-01"
    )
    out["month_of_year"] = out["month_of_year"].astype(int).astype("category")
    out[region_col] = out[region_col].astype(int).astype("category")
    if commune_col and commune_col in out.columns:
        out[commune_col] = out[commune_col].astype(int).astype("category")
    if "macrozona" in out.columns:
        macro_order = ["Austral", "Norte", "Centro", "RM", "Sur"]
        observed = [x for x in macro_order if x in set(out["macrozona"].dropna())]
        extra = sorted(set(out["macrozona"].dropna()) - set(observed))
        out["macrozona"] = pd.Categorical(out["macrozona"], categories=observed + extra)
    return out


def add_spline_basis(df: pd.DataFrame, n_knots: int = 3, prefix: str = "spline") -> tuple[pd.DataFrame, list[str], np.ndarray]:
    if n_knots < 1:
        raise ValueError("n_knots must be >= 1")
    out = df.copy()
    probs = np.linspace(0, 1, n_knots + 2)[1:-1]
    knots = np.quantile(out["trend_t"].astype(float), probs)
    basis = dmatrix(
        "cr(trend_t, knots=knots, constraints='center') - 1",
        {"trend_t": out["trend_t"].astype(float), "knots": knots},
        return_type="dataframe",
    )
    cols = [f"{prefix}_{i + 1}" for i in range(basis.shape[1])]
    basis.columns = cols
    out = pd.concat([out.reset_index(drop=True), basis.reset_index(drop=True)], axis=1)
    return out, cols, knots


def key_terms(spline_cols: Iterable[str]) -> list[str]:
    return ["d_estallido", "d_pandemia", *list(spline_cols)]


def normal_pvalue(estimate: float, se: float) -> float:
    if se <= 0 or not np.isfinite(se):
        return np.nan
    z = estimate / se
    return 2 * (1 - stats.norm.cdf(abs(z)))


def coefficient_table(
    result,
    terms: Iterable[str],
    label: str,
    exponentiate: bool = True,
    extra: dict | None = None,
) -> pd.DataFrame:
    rows = []
    params = result.params
    bse = result.bse
    pvalues = getattr(result, "pvalues", pd.Series(index=params.index, dtype=float))
    for term in terms:
        if term not in params.index:
            continue
        est = float(params[term])
        se = float(bse[term])
        row = {
            "specification": label,
            "term": term,
            "estimate": est,
            "std_error": se,
            "z_or_t": est / se if se > 0 else np.nan,
            "p_value": float(pvalues.get(term, normal_pvalue(est, se))),
            "ci_lower": est - 1.96 * se,
            "ci_upper": est + 1.96 * se,
        }
        if exponentiate:
            row["ratio"] = float(np.exp(est))
            row["ratio_ci_lower"] = float(np.exp(row["ci_lower"]))
            row["ratio_ci_upper"] = float(np.exp(row["ci_upper"]))
        if extra:
            row.update(extra)
        rows.append(row)
    return pd.DataFrame(rows)


def weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    values = pd.Series(values, dtype=float)
    weights = pd.Series(weights, dtype=float)
    mask = values.notna() & weights.notna() & (weights > 0)
    if not mask.any():
        return np.nan
    return float(np.average(values[mask], weights=weights[mask]))


def period_mask(df: pd.DataFrame, period: str) -> pd.Series:
    if period == "baseline_2016_sep2019":
        return (df["year"].between(2016, 2019)) & ~((df["year"] == 2019) & (df["month"] >= 10))
    if period == "post_2022_2025":
        return df["year"].between(2022, 2025)
    if period == "pandemic_2020_2021":
        return ((df["year"] == 2020) & (df["month"] >= 3)) | (df["year"] == 2021)
    raise ValueError(f"Unknown period: {period}")


def aggregate_share(df: pd.DataFrame, success_col: str, failure_col: str, mask: pd.Series) -> float:
    sub = df.loc[mask]
    success = sub[success_col].sum()
    total = success + sub[failure_col].sum()
    return float(success / total) if total > 0 else np.nan
