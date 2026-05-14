from __future__ import annotations

import warnings

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller, kpss, pacf

from model_helpers import (
    FIGURE_DIR,
    TABLE_DIR,
    add_spline_basis,
    coefficient_table,
    ensure_output_dirs,
    key_terms,
    period_mask,
    read_region_panel,
)


def formula(outcome: str, spline_cols: list[str], include_lags: list[str] | None = None) -> str:
    rhs = ["C(month_of_year)", "d_estallido", "d_pandemia", *spline_cols, "C(region)"]
    if include_lags:
        rhs.extend(include_lags)
    return f"{outcome} ~ " + " + ".join(rhs)


def fit_binomial_residuals(df: pd.DataFrame, n_knots: int = 3):
    model_df = df.copy()
    model_df["total_comp"] = model_df["n_confrontational"] + model_df["n_non_confrontational"]
    model_df = model_df.loc[model_df["total_comp"] > 0].copy()
    model_df["share_comp"] = model_df["n_confrontational"] / model_df["total_comp"]
    model_df, spline_cols, knots = add_spline_basis(model_df, n_knots=n_knots)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = smf.glm(
            formula("share_comp", spline_cols),
            data=model_df,
            family=sm.families.Binomial(),
            freq_weights=model_df["total_comp"],
        ).fit(maxiter=200, cov_type="cluster", cov_kwds={"groups": model_df["region"]})
    model_df["resid_binomial_pearson"] = res.resid_pearson
    return res, model_df, spline_cols, knots


def fit_poisson_residuals(df: pd.DataFrame, y_col: str, n_knots: int = 3) -> pd.DataFrame:
    model_df, spline_cols, _ = add_spline_basis(df, n_knots=n_knots)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = smf.glm(
            formula(y_col, spline_cols),
            data=model_df,
            family=sm.families.Poisson(),
            offset=np.log(model_df["pop_monthly"]),
        ).fit(maxiter=200)
    model_df[f"resid_{y_col}"] = res.resid_pearson
    return model_df[["date", "region", f"resid_{y_col}"]]


def monthly_residual_series(panel: pd.DataFrame, binomial_df: pd.DataFrame) -> pd.DataFrame:
    pieces = [
        binomial_df.groupby("date", as_index=False)["resid_binomial_pearson"].mean().rename(
            columns={"resid_binomial_pearson": "binomial_composition"}
        )
    ]
    for label, col in [
        ("poisson_confrontational", "n_confrontational"),
        ("poisson_snatching", "n_snatching"),
        ("poisson_non_confrontational", "n_non_confrontational"),
    ]:
        resid = fit_poisson_residuals(panel, col)
        resid_col = f"resid_{col}"
        pieces.append(resid.groupby("date", as_index=False)[resid_col].mean().rename(columns={resid_col: label}))
    out = pieces[0]
    for piece in pieces[1:]:
        out = out.merge(piece, on="date", how="outer")
    return out.sort_values("date")


def national_series(panel: pd.DataFrame) -> pd.DataFrame:
    nat = (
        panel.groupby("date", as_index=False)
        .agg(
            n_confrontational=("n_confrontational", "sum"),
            n_snatching=("n_snatching", "sum"),
            n_non_confrontational=("n_non_confrontational", "sum"),
            pop=("pop_monthly", "sum"),
        )
        .sort_values("date")
    )
    for col in ["n_confrontational", "n_snatching", "n_non_confrontational"]:
        nat[f"log_rate_{col}"] = np.log((nat[col] + 0.5) / nat["pop"] * 100000)
    nat["logratio_v_nv"] = np.log((nat["n_confrontational"] + 0.5) / (nat["n_non_confrontational"] + 0.5))
    return nat


def stationarity_rows(series: pd.Series, label: str) -> list[dict]:
    x = pd.Series(series).dropna().astype(float)
    rows = []
    if len(x) < 20 or x.nunique() < 3:
        return rows
    try:
        adf_stat, adf_p, _, _, _, _ = adfuller(x, autolag="AIC")
        rows.append({"series": label, "test": "ADF", "lag": np.nan, "statistic": adf_stat, "p_value": adf_p, "null_hypothesis": "unit root"})
    except Exception as exc:
        rows.append({"series": label, "test": "ADF", "lag": np.nan, "statistic": np.nan, "p_value": np.nan, "note": str(exc)})
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            kpss_stat, kpss_p, _, _ = kpss(x, regression="c", nlags="auto")
        rows.append({"series": label, "test": "KPSS", "lag": np.nan, "statistic": kpss_stat, "p_value": kpss_p, "null_hypothesis": "level stationarity"})
    except Exception as exc:
        rows.append({"series": label, "test": "KPSS", "lag": np.nan, "statistic": np.nan, "p_value": np.nan, "note": str(exc)})
    return rows


def ljung_rows(series: pd.Series, label: str) -> list[dict]:
    x = pd.Series(series).dropna().astype(float)
    rows = []
    if len(x) < 30:
        return rows
    lb = acorr_ljungbox(x, lags=[6, 12, 24], return_df=True)
    for lag, row in lb.iterrows():
        rows.append(
            {
                "series": label,
                "test": "Ljung-Box",
                "lag": int(lag),
                "statistic": float(row["lb_stat"]),
                "p_value": float(row["lb_pvalue"]),
                "null_hypothesis": "no autocorrelation through lag",
            }
        )
    return rows


def diagnostics_table(panel: pd.DataFrame, residuals: pd.DataFrame, nat: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col in ["binomial_composition", "poisson_confrontational", "poisson_snatching", "poisson_non_confrontational"]:
        rows.extend(ljung_rows(residuals[col], col))
        rows.extend(stationarity_rows(residuals[col], f"{col}_residual"))
    for col in ["log_rate_n_confrontational", "log_rate_n_snatching", "log_rate_n_non_confrontational", "logratio_v_nv"]:
        rows.extend(stationarity_rows(nat[col], col))
        rows.extend(stationarity_rows(nat[col].diff(), f"d_{col}"))
    return pd.DataFrame(rows)


def autoregressive_sensitivity(panel: pd.DataFrame) -> pd.DataFrame:
    df = panel.sort_values(["region", "date"]).copy()
    df["logratio_v_nv"] = np.log((df["n_confrontational"] + 0.5) / (df["n_non_confrontational"] + 0.5))
    df["lag1_logratio"] = df.groupby("region", observed=True)["logratio_v_nv"].shift(1)
    df["lag2_logratio"] = df.groupby("region", observed=True)["logratio_v_nv"].shift(2)
    rows = []
    for label, lags in [("AR0", []), ("AR1", ["lag1_logratio"]), ("AR2", ["lag1_logratio", "lag2_logratio"])]:
        model_df = df.dropna(subset=lags).copy() if lags else df.copy()
        model_df, spline_cols, _ = add_spline_basis(model_df, n_knots=3)
        res = smf.ols(formula("logratio_v_nv", spline_cols, include_lags=lags), data=model_df).fit(
            cov_type="cluster",
            cov_kwds={"groups": model_df["region"]},
        )
        tab = coefficient_table(
            res,
            [*key_terms(spline_cols), *lags],
            f"logratio_{label}",
            exponentiate=True,
            extra={"n_obs": int(res.nobs)},
        )
        rows.append(tab.rename(columns={"ratio": "ratio_multiplier", "ratio_ci_lower": "multiplier_ci_lower", "ratio_ci_upper": "multiplier_ci_upper"}))
    return pd.concat(rows, ignore_index=True)


def spline_knot_sensitivity(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    plot_rows = []
    for n_knots in [3, 5, 7]:
        df = panel.copy()
        df["total_comp"] = df["n_confrontational"] + df["n_non_confrontational"]
        df["share_comp"] = df["n_confrontational"] / df["total_comp"]
        df, spline_cols, knots = add_spline_basis(df, n_knots=n_knots)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = smf.glm(
                formula("share_comp", spline_cols),
                data=df,
                family=sm.families.Binomial(),
                freq_weights=df["total_comp"],
            ).fit(maxiter=200, cov_type="cluster", cov_kwds={"groups": df["region"]})
        tab = coefficient_table(
            res,
            ["d_estallido", "d_pandemia"],
            f"{n_knots}_interior_knots",
            exponentiate=True,
            extra={"knots": ";".join(f"{k:.1f}" for k in knots), "dispersion_pearson": float(res.pearson_chi2 / res.df_resid)},
        ).rename(columns={"ratio": "odds_ratio", "ratio_ci_lower": "or_ci_lower", "ratio_ci_upper": "or_ci_upper"})
        df["pred"] = res.predict(df)
        base = period_mask(df, "baseline_2016_sep2019")
        post = period_mask(df, "post_2022_2025")
        pred_base = np.average(df.loc[base, "pred"], weights=df.loc[base, "total_comp"])
        pred_post = np.average(df.loc[post, "pred"], weights=df.loc[post, "total_comp"])
        tab["predicted_diff_pp"] = 100 * (pred_post - pred_base)
        rows.append(tab)

        monthly = (
            df.groupby("date", as_index=False)
            .apply(lambda g: pd.Series({"pred": np.average(g["pred"], weights=g["total_comp"])}), include_groups=False)
            .assign(specification=f"{n_knots} knots")
        )
        plot_rows.append(monthly)
    plot_df = pd.concat(plot_rows, ignore_index=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for spec, sub in plot_df.groupby("specification"):
        ax.plot(sub["date"], sub["pred"], lw=1.4, label=spec)
    ax.axvline(pd.Timestamp("2019-10-01"), color="#8c8c8c", lw=0.8, ls="--")
    ax.axvline(pd.Timestamp("2020-03-01"), color="#8c8c8c", lw=0.8, ls="--")
    ax.set_ylabel("Predicted confrontational share")
    ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig7b_spline_trend_fit.png", dpi=300)
    fig.savefig(FIGURE_DIR / "fig7b_spline_trend_fit.pdf")
    plt.close(fig)
    return pd.concat(rows, ignore_index=True)


def plot_pacf(residuals: pd.DataFrame) -> None:
    cols = ["binomial_composition", "poisson_confrontational", "poisson_snatching", "poisson_non_confrontational"]
    labels = ["Composition binomial", "Confrontational count", "Snatching count", "Non-confrontational count"]
    fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharex=True, sharey=True)
    for ax, col, label in zip(axes.ravel(), cols, labels):
        x = residuals[col].dropna().astype(float)
        vals = pacf(x, nlags=24, method="ywm")[1:]
        ax.axhline(0, color="#525252", lw=0.8)
        ax.axhline(1.96 / np.sqrt(len(x)), color="#bdbdbd", lw=0.8, ls="--")
        ax.axhline(-1.96 / np.sqrt(len(x)), color="#bdbdbd", lw=0.8, ls="--")
        ax.bar(np.arange(1, 25), vals, color="#4d4d4d", width=0.8)
        ax.set_title(label, fontsize=10)
        ax.set_ylim(-0.45, 0.45)
    for ax in axes[-1, :]:
        ax.set_xlabel("Lag")
    for ax in axes[:, 0]:
        ax.set_ylabel("PACF")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig7_pacf_residuals.png", dpi=300)
    fig.savefig(FIGURE_DIR / "fig7_pacf_residuals.pdf")
    plt.close(fig)


def main() -> None:
    ensure_output_dirs()
    panel = read_region_panel()
    _, binomial_df, _, _ = fit_binomial_residuals(panel)
    residuals = monthly_residual_series(panel, binomial_df)
    nat = national_series(panel)

    diagnostics = diagnostics_table(panel, residuals, nat)
    diagnostics.to_csv(TABLE_DIR / "tabla_10_its_diagnostics.csv", index=False)

    ar = autoregressive_sensitivity(panel)
    ar.to_csv(TABLE_DIR / "tabla_10b_autoregressive_sensitivity.csv", index=False)

    knots = spline_knot_sensitivity(panel)
    knots.to_csv(TABLE_DIR / "tabla_10c_spline_knot_sensitivity.csv", index=False)

    plot_pacf(residuals)

    print("ITS diagnostics complete.")
    print(diagnostics.loc[diagnostics["test"].eq("Ljung-Box"), ["series", "lag", "p_value"]].head(12).to_string(index=False))
    print(ar.loc[ar["term"].isin(["d_estallido", "d_pandemia"]), ["specification", "term", "ratio_multiplier", "p_value"]].to_string(index=False))


if __name__ == "__main__":
    main()
