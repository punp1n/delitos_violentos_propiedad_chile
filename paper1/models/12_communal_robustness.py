from __future__ import annotations

import warnings

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

from model_helpers import (
    FIGURE_DIR,
    TABLE_DIR,
    add_spline_basis,
    coefficient_table,
    ensure_output_dirs,
    key_terms,
    period_mask,
    read_commune_panel,
)


def fixed_effect_ols(df: pd.DataFrame, outcome: str, spline_cols: list[str]):
    month_dummies = pd.get_dummies(df["month_of_year"].astype(str), prefix="month", drop_first=True)
    x = pd.concat(
        [
            df[["d_estallido", "d_pandemia", *spline_cols]].reset_index(drop=True),
            month_dummies.reset_index(drop=True),
        ],
        axis=1,
    ).astype(float)
    y = df[outcome].astype(float).reset_index(drop=True)
    group = df["comuna"].reset_index(drop=True)

    x_dm = x - x.groupby(group, observed=True).transform("mean")
    y_dm = y - y.groupby(group, observed=True).transform("mean")
    keep = x_dm.notna().all(axis=1) & y_dm.notna()
    return sm.OLS(y_dm.loc[keep], x_dm.loc[keep]).fit(
        cov_type="cluster",
        cov_kwds={"groups": group.loc[keep]},
    )


def fit_count(df: pd.DataFrame, outcome: str, sample_label: str):
    model_df, spline_cols, knots = add_spline_basis(df, n_knots=3)
    model_df["log_rate"] = np.log((model_df[outcome] + 0.5) / model_df["pop_monthly_comuna"] * 100000)
    result = fixed_effect_ols(model_df, "log_rate", spline_cols)
    tab = coefficient_table(
        result,
        key_terms(spline_cols),
        f"{sample_label}_{outcome}",
        exponentiate=True,
        extra={
            "sample": sample_label,
            "outcome": outcome,
            "n_obs": int(result.nobs),
            "n_communes": int(model_df["comuna"].nunique()),
            "knots": ";".join(f"{k:.1f}" for k in knots),
            "method": "OLS on log rate with absorbed commune FE and clustered SE",
        },
    ).rename(columns={"ratio": "rate_multiplier", "ratio_ci_lower": "multiplier_ci_lower", "ratio_ci_upper": "multiplier_ci_upper"})
    return tab


def fit_composition(df: pd.DataFrame, sample_label: str):
    model_df = df.copy()
    model_df["total_comp"] = model_df["n_confrontational"] + model_df["n_non_confrontational"]
    model_df = model_df.loc[model_df["total_comp"] > 0].copy()
    model_df["logratio_comp"] = np.log((model_df["n_confrontational"] + 0.5) / (model_df["n_non_confrontational"] + 0.5))
    model_df, spline_cols, knots = add_spline_basis(model_df, n_knots=3)
    result = fixed_effect_ols(model_df, "logratio_comp", spline_cols)
    tab = coefficient_table(
        result,
        key_terms(spline_cols),
        f"{sample_label}_composition",
        exponentiate=True,
        extra={
            "sample": sample_label,
            "n_obs": int(result.nobs),
            "n_communes": int(model_df["comuna"].nunique()),
            "knots": ";".join(f"{k:.1f}" for k in knots),
            "method": "OLS on log ratio with absorbed commune FE and clustered SE",
        },
    ).rename(columns={"ratio": "ratio_multiplier", "ratio_ci_lower": "multiplier_ci_lower", "ratio_ci_upper": "multiplier_ci_upper"})
    return tab


def dense_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for sample_label, sub in [("full", df), ("dense", df.loc[df["dense_commune"].astype(bool)].copy())]:
        base = period_mask(sub, "baseline_2016_sep2019")
        post = period_mask(sub, "post_2022_2025")
        for period_label, mask in [("baseline_2016_sep2019", base), ("post_2022_2025", post)]:
            ss = sub.loc[mask]
            success = ss["n_confrontational"].sum()
            failure = ss["n_non_confrontational"].sum()
            rows.append(
                {
                    "sample": sample_label,
                    "period": period_label,
                    "n_communes": int(sub["comuna"].nunique()),
                    "n_confrontational": float(success),
                    "n_non_confrontational": float(failure),
                    "observed_share": float(success / (success + failure)),
                    "mean_monthly_confrontational": float(ss["n_confrontational"].mean()),
                }
            )
        base_share = rows[-2]["observed_share"]
        post_share = rows[-1]["observed_share"]
        rows.append(
            {
                "sample": sample_label,
                "period": "post_minus_baseline",
                "n_communes": int(sub["comuna"].nunique()),
                "n_confrontational": np.nan,
                "n_non_confrontational": np.nan,
                "observed_share": post_share - base_share,
                "mean_monthly_confrontational": np.nan,
            }
        )
    return pd.DataFrame(rows)


def plot_communal_distribution(df: pd.DataFrame) -> None:
    rows = []
    for comuna, sub in df.groupby("comuna", observed=True):
        base = period_mask(sub, "baseline_2016_sep2019")
        post = period_mask(sub, "post_2022_2025")
        if base.sum() == 0 or post.sum() == 0:
            continue
        base_success = sub.loc[base, "n_confrontational"].sum()
        base_total = base_success + sub.loc[base, "n_non_confrontational"].sum()
        post_success = sub.loc[post, "n_confrontational"].sum()
        post_total = post_success + sub.loc[post, "n_non_confrontational"].sum()
        if base_total <= 0 or post_total <= 0:
            continue
        rows.append(
            {
                "comuna": int(comuna),
                "comuna_name": sub["comuna_name"].iloc[0],
                "region": int(sub["region"].iloc[0]),
                "macrozona": sub["macrozona"].iloc[0],
                "dense_commune": bool(sub["dense_commune"].iloc[0]),
                "delta_share_pp": 100 * (post_success / post_total - base_success / base_total),
                "baseline_share": base_success / base_total,
                "post_share": post_success / post_total,
            }
        )
    dist = pd.DataFrame(rows)
    dist.to_csv(TABLE_DIR / "tabla_11d_communal_share_distribution.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    groups = [dist.loc[~dist["dense_commune"], "delta_share_pp"], dist.loc[dist["dense_commune"], "delta_share_pp"]]
    ax.boxplot(groups, tick_labels=["Sparse communes", "Dense communes"], vert=True, patch_artist=True)
    ax.axhline(0, color="#737373", lw=0.9, ls="--")
    ax.set_ylabel("Change in confrontational share (pp), 2022-2025 vs 2016-Sep.2019")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig8_communal_distribution.png", dpi=300)
    fig.savefig(FIGURE_DIR / "fig8_communal_distribution.pdf")
    plt.close(fig)


def main() -> None:
    ensure_output_dirs()
    panel = read_commune_panel()
    full = panel.copy()
    dense = panel.loc[panel["dense_commune"].astype(bool)].copy()

    count_rows = []
    for sample_label, sub in [("full", full), ("dense", dense)]:
        for outcome in ["n_confrontational", "n_snatching", "n_non_confrontational"]:
            count_rows.append(fit_count(sub, outcome, sample_label))
    count_table = pd.concat(count_rows, ignore_index=True)
    count_table.to_csv(TABLE_DIR / "tabla_11_communal_robustness.csv", index=False)

    comp_table = pd.concat([fit_composition(full, "full"), fit_composition(dense, "dense")], ignore_index=True)
    comp_table.to_csv(TABLE_DIR / "tabla_11b_communal_composition.csv", index=False)

    dense_summary(panel).to_csv(TABLE_DIR / "tabla_11c_communal_dense_sensitivity.csv", index=False)
    plot_communal_distribution(panel)

    print("Communal robustness complete.")
    print(comp_table.loc[comp_table["term"].isin(["d_estallido", "d_pandemia"]), ["sample", "term", "ratio_multiplier", "p_value"]].to_string(index=False))
    print(count_table.loc[count_table["term"].eq("d_pandemia"), ["sample", "outcome", "rate_multiplier", "p_value"]].to_string(index=False))


if __name__ == "__main__":
    main()
