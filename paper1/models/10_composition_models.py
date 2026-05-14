from __future__ import annotations

import warnings

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.linear_model import LogisticRegression

from model_helpers import (
    DATA_DIR,
    FIGURE_DIR,
    TABLE_DIR,
    add_spline_basis,
    aggregate_share,
    coefficient_table,
    ensure_output_dirs,
    key_terms,
    period_mask,
    read_region_panel,
)


RNG_SEED = 2026
N_BOOT = 999


def build_formula(outcome: str, spline_cols: list[str], unit_fe: str = "region") -> str:
    rhs = ["C(month_of_year)", "d_estallido", "d_pandemia", *spline_cols, f"C({unit_fe})"]
    return f"{outcome} ~ " + " + ".join(rhs)


def fit_grouped_binomial(
    df: pd.DataFrame,
    success_col: str,
    failure_col: str,
    label: str,
    n_knots: int = 3,
) -> tuple[object, pd.DataFrame, list[str], str, np.ndarray]:
    model_df = df.copy()
    total_col = f"total_{label}"
    share_col = f"share_{label}"
    model_df[total_col] = model_df[success_col] + model_df[failure_col]
    model_df = model_df.loc[model_df[total_col] > 0].copy()
    model_df[share_col] = model_df[success_col] / model_df[total_col]
    model_df, spline_cols, knots = add_spline_basis(model_df, n_knots=n_knots)
    formula = build_formula(share_col, spline_cols)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = smf.glm(
            formula=formula,
            data=model_df,
            family=sm.families.Binomial(),
            freq_weights=model_df[total_col],
        ).fit(
            maxiter=200,
            cov_type="cluster",
            cov_kwds={"groups": model_df["region"]},
        )
    return result, model_df, spline_cols, share_col, knots


def fit_logratio(df: pd.DataFrame, success_col: str, failure_col: str, n_knots: int = 3) -> tuple[object, pd.DataFrame, list[str], np.ndarray]:
    model_df = df.copy()
    model_df["logratio_v_nv"] = np.log((model_df[success_col] + 0.5) / (model_df[failure_col] + 0.5))
    model_df, spline_cols, knots = add_spline_basis(model_df, n_knots=n_knots)
    formula = build_formula("logratio_v_nv", spline_cols)
    result = smf.ols(formula=formula, data=model_df).fit(
        cov_type="cluster",
        cov_kwds={"groups": model_df["region"]},
    )
    return result, model_df, spline_cols, knots


def cluster_bootstrap_share_diff(df: pd.DataFrame, success_col: str, failure_col: str, n_boot: int = N_BOOT) -> tuple[float, float, float]:
    rng = np.random.default_rng(RNG_SEED)
    region_values = pd.to_numeric(df["region"], errors="coerce").dropna().astype(int)
    regions = np.array(sorted(region_values.unique()))
    diffs = []
    for _ in range(n_boot):
        sampled = rng.choice(regions, size=len(regions), replace=True)
        boot = pd.concat([df.loc[pd.to_numeric(df["region"], errors="coerce").astype(int).eq(r)] for r in sampled], ignore_index=True)
        base = aggregate_share(boot, success_col, failure_col, period_mask(boot, "baseline_2016_sep2019"))
        post = aggregate_share(boot, success_col, failure_col, period_mask(boot, "post_2022_2025"))
        diffs.append(post - base)
    diffs = np.array(diffs)
    p_value = 2 * min(np.mean(diffs <= 0), np.mean(diffs >= 0))
    return float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5)), float(p_value)


def marginal_share_table(
    model_df: pd.DataFrame,
    result,
    success_col: str,
    failure_col: str,
    label: str,
) -> pd.DataFrame:
    df = model_df.copy()
    total = df[success_col] + df[failure_col]
    df["predicted_share"] = result.predict(df)
    rows = []
    for period, period_label in [
        ("baseline_2016_sep2019", "Baseline 2016-Sep.2019"),
        ("post_2022_2025", "Post-pandemic 2022-2025"),
    ]:
        mask = period_mask(df, period)
        rows.append(
            {
                "specification": label,
                "period": period_label,
                "observed_share": aggregate_share(df, success_col, failure_col, mask),
                "predicted_share": float(np.average(df.loc[mask, "predicted_share"], weights=total.loc[mask])),
                "n_success": float(df.loc[mask, success_col].sum()),
                "n_failure": float(df.loc[mask, failure_col].sum()),
                "n_total": float(total.loc[mask].sum()),
            }
        )

    base = rows[0]
    post = rows[1]
    ci_l, ci_u, p_value = cluster_bootstrap_share_diff(df, success_col, failure_col)
    rows.append(
        {
            "specification": label,
            "period": "Difference post - baseline",
            "observed_share": post["observed_share"] - base["observed_share"],
            "predicted_share": post["predicted_share"] - base["predicted_share"],
            "n_success": np.nan,
            "n_failure": np.nan,
            "n_total": np.nan,
            "bootstrap_ci_lower": ci_l,
            "bootstrap_ci_upper": ci_u,
            "bootstrap_p_value": p_value,
        }
    )
    return pd.DataFrame(rows)


def plot_predicted_share(model_df: pd.DataFrame, result, success_col: str, failure_col: str) -> None:
    df = model_df.copy()
    total = df[success_col] + df[failure_col]
    pred = result.get_prediction(df).summary_frame(alpha=0.05)
    df["pred"] = pred["mean"].to_numpy()
    df["pred_low"] = pred["mean_ci_lower"].to_numpy()
    df["pred_high"] = pred["mean_ci_upper"].to_numpy()

    monthly = (
        df.assign(total=total)
        .groupby("date", as_index=False)
        .apply(
            lambda g: pd.Series(
                {
                    "observed_share": g[success_col].sum() / g["total"].sum(),
                    "predicted_share": np.average(g["pred"], weights=g["total"]),
                    "pred_low": np.average(g["pred_low"], weights=g["total"]),
                    "pred_high": np.average(g["pred_high"], weights=g["total"]),
                }
            ),
            include_groups=False,
        )
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axvspan(pd.Timestamp("2019-10-01"), pd.Timestamp("2020-02-29"), color="#d9d9d9", alpha=0.45, lw=0)
    ax.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2021-12-31"), color="#efefef", alpha=0.75, lw=0)
    ax.plot(monthly["date"], monthly["observed_share"], color="#8c8c8c", lw=1.0, label="Observed")
    ax.plot(monthly["date"], monthly["predicted_share"], color="#b2182b", lw=1.8, label="Grouped-binomial fit")
    ax.fill_between(
        monthly["date"],
        monthly["pred_low"],
        monthly["pred_high"],
        color="#ef8a62",
        alpha=0.25,
        linewidth=0,
        label="95% CI",
    )
    ax.set_ylabel("Confrontational share")
    ax.set_xlabel("")
    ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", frameon=False, ncols=3)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig6_predicted_composition.png", dpi=300)
    fig.savefig(FIGURE_DIR / "fig6_predicted_composition.pdf")
    plt.close(fig)


def build_excluding_cum_867(panel: pd.DataFrame) -> pd.DataFrame:
    long = pd.read_parquet(DATA_DIR / "cch_panel_comuna_month.parquet")
    long = long.loc[long["c3_modelable"] & long["C3_categoria"].notna()].copy()
    long = long.loc[long["cum"].astype(int) != 867].copy()
    collapsed = (
        long.groupby(["region", "year", "month", "C3_categoria"], as_index=False)["n_denuncias"]
        .sum()
        .pivot_table(
            index=["region", "year", "month"],
            columns="C3_categoria",
            values="n_denuncias",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )
    collapsed = collapsed.rename(
        columns={
            "confrontational": "n_confrontational_no867",
            "non_confrontational": "n_non_confrontational_no867",
            "snatching": "n_snatching_no867",
        }
    )
    keys = [
        "region",
        "year",
        "month",
        "date",
        "d_estallido",
        "d_pandemia",
        "month_of_year",
        "trend_t",
        "macrozona",
    ]
    out = panel[keys].merge(collapsed, on=["region", "year", "month"], how="left")
    for col in ["n_confrontational_no867", "n_non_confrontational_no867", "n_snatching_no867"]:
        out[col] = out[col].fillna(0)
    return out


def sensitivity_table(panel: pd.DataFrame) -> pd.DataFrame:
    work = panel.copy()
    work["n_confrontational_plus_snatching"] = work["n_confrontational"] + work["n_snatching"]
    work["n_non_confrontational_plus_snatching"] = work["n_non_confrontational"] + work["n_snatching"]
    specs = [
        ("main", work, "n_confrontational", "n_non_confrontational"),
        ("snatching_pooled_with_confrontational", work, "n_confrontational_plus_snatching", "n_non_confrontational"),
        ("snatching_pooled_with_non_confrontational", work, "n_confrontational", "n_non_confrontational_plus_snatching"),
    ]
    no867 = build_excluding_cum_867(panel)
    specs.append(("cum867_excluded", no867, "n_confrontational_no867", "n_non_confrontational_no867"))

    rows = []
    for label, data, success_col, failure_col in specs:
        result, model_df, spline_cols, _, _ = fit_grouped_binomial(data, success_col, failure_col, label)
        tab = coefficient_table(result, ["d_estallido", "d_pandemia"], label, exponentiate=True)
        tab["success_definition"] = success_col
        tab["failure_definition"] = failure_col
        tab["dispersion_pearson"] = float(result.pearson_chi2 / result.df_resid)
        rows.append(tab)

        marg = marginal_share_table(model_df, result, success_col, failure_col, label)
        diff = marg.loc[marg["period"].eq("Difference post - baseline")].iloc[0]
        rows[-1]["observed_diff_pp"] = 100 * diff["observed_share"]
        rows[-1]["predicted_diff_pp"] = 100 * diff["predicted_share"]
    return pd.concat(rows, ignore_index=True)


def counts_rates_table(panel: pd.DataFrame) -> pd.DataFrame:
    categories = [
        ("confrontational", "n_confrontational"),
        ("snatching", "n_snatching"),
        ("non_confrontational", "n_non_confrontational"),
    ]
    periods = [
        ("Baseline 2016-Sep.2019", period_mask(panel, "baseline_2016_sep2019")),
        ("Post-pandemic 2022-2025", period_mask(panel, "post_2022_2025")),
    ]
    rows = []
    for cat, col in categories:
        vals = []
        for period_label, mask in periods:
            sub = panel.loc[mask].copy()
            count = float(sub[col].sum())
            pop_exposure = float((sub["pop_monthly"] / 12).sum())
            rate = count / pop_exposure * 100000
            vals.append((count, rate))
            rows.append({"category": cat, "period": period_label, "count": count, "annualized_rate_per_100k": rate})
        rows.append(
            {
                "category": cat,
                "period": "Post vs baseline % change",
                "count": (vals[1][0] / vals[0][0] - 1) * 100,
                "annualized_rate_per_100k": (vals[1][1] / vals[0][1] - 1) * 100,
            }
        )
    return pd.DataFrame(rows)


def multinomial_sensitivity(panel: pd.DataFrame, spline_cols: list[str]) -> pd.DataFrame:
    x_cols = ["d_estallido", "d_pandemia", *spline_cols]
    base = panel.copy()
    design = pd.get_dummies(base[["month_of_year", "region"]].astype(str), prefix=["month", "region"], drop_first=True)
    x = pd.concat([base[x_cols].reset_index(drop=True), design.reset_index(drop=True)], axis=1).astype(float)
    y_rows = []
    weights = []
    x_rows = []
    for category, col in [
        ("confrontational", "n_confrontational"),
        ("snatching", "n_snatching"),
        ("non_confrontational", "n_non_confrontational"),
    ]:
        y_rows.extend([category] * len(base))
        weights.extend(base[col].to_numpy())
        x_rows.append(x)
    x_long = pd.concat(x_rows, ignore_index=True)
    y = np.array(y_rows)
    weights = np.array(weights, dtype=float)
    keep = weights > 0

    clf = LogisticRegression(max_iter=2000, solver="lbfgs")
    clf.fit(x_long.loc[keep], y[keep], sample_weight=weights[keep])

    classes = list(clf.classes_)
    baseline_idx = classes.index("non_confrontational")
    rows = []
    for cls in ["confrontational", "snatching"]:
        cls_idx = classes.index(cls)
        beta_diff = clf.coef_[cls_idx] - clf.coef_[baseline_idx]
        for term in ["d_estallido", "d_pandemia", *spline_cols]:
            pos = list(x_long.columns).index(term)
            rows.append(
                {
                    "comparison": f"{cls} vs non_confrontational",
                    "term": term,
                    "estimate": float(beta_diff[pos]),
                    "relative_risk_ratio": float(np.exp(beta_diff[pos])),
                    "note": "Weighted multinomial logit via scikit-learn; no standard errors.",
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    ensure_output_dirs()
    panel = read_region_panel()

    main_result, main_df, spline_cols, _, knots = fit_grouped_binomial(
        panel,
        "n_confrontational",
        "n_non_confrontational",
        "main",
    )
    table_9 = coefficient_table(
        main_result,
        key_terms(spline_cols),
        "Grouped binomial: confrontational vs non-confrontational",
        exponentiate=True,
        extra={"dispersion_pearson": float(main_result.pearson_chi2 / main_result.df_resid)},
    )
    table_9 = table_9.rename(columns={"ratio": "odds_ratio", "ratio_ci_lower": "or_ci_lower", "ratio_ci_upper": "or_ci_upper"})
    table_9.to_csv(TABLE_DIR / "tabla_9_composition_logit.csv", index=False)

    logratio_result, logratio_df, logratio_splines, _ = fit_logratio(
        panel,
        "n_confrontational",
        "n_non_confrontational",
    )
    table_9b = coefficient_table(
        logratio_result,
        key_terms(logratio_splines),
        "Log-ratio OLS: log((confrontational+0.5)/(non-confrontational+0.5))",
        exponentiate=True,
    )
    table_9b = table_9b.rename(
        columns={"ratio": "ratio_multiplier", "ratio_ci_lower": "multiplier_ci_lower", "ratio_ci_upper": "multiplier_ci_upper"}
    )
    table_9b.to_csv(TABLE_DIR / "tabla_9b_logratio_model.csv", index=False)

    table_9c = marginal_share_table(
        main_df,
        main_result,
        "n_confrontational",
        "n_non_confrontational",
        "main",
    )
    table_9c.to_csv(TABLE_DIR / "tabla_9c_marginal_shares.csv", index=False)

    table_9d = sensitivity_table(panel)
    table_9d.to_csv(TABLE_DIR / "tabla_9d_composition_sensitivity.csv", index=False)

    table_9e = counts_rates_table(panel)
    table_9e.to_csv(TABLE_DIR / "tabla_9e_counts_rates_period_change.csv", index=False)

    panel_spline, multinom_spline_cols, _ = add_spline_basis(panel, n_knots=3)
    table_9f = multinomial_sensitivity(panel_spline, multinom_spline_cols)
    table_9f.to_csv(TABLE_DIR / "tabla_9f_multinomial_sensitivity.csv", index=False)

    plot_predicted_share(main_df, main_result, "n_confrontational", "n_non_confrontational")

    print("Composition models complete.")
    print(f"Knots: {', '.join(f'{k:.1f}' for k in knots)}")
    print(table_9.loc[table_9["term"].isin(["d_estallido", "d_pandemia"]), ["term", "odds_ratio", "p_value"]].to_string(index=False))
    print(table_9c.to_string(index=False))


if __name__ == "__main__":
    main()
