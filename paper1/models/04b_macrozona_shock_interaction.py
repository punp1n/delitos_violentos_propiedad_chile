from __future__ import annotations

import warnings

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

from model_helpers import (
    FIGURE_DIR,
    TABLE_DIR,
    add_spline_basis,
    ensure_output_dirs,
    normal_pvalue,
    read_region_panel,
)


def safe_exp(value: float) -> float:
    if not np.isfinite(value):
        return np.nan
    if value > 700:
        return np.inf
    if value < -700:
        return 0.0
    return float(np.exp(value))


def interaction_formula(outcome: str, spline_cols: list[str]) -> str:
    spline_terms = " + ".join(spline_cols)
    spline_interactions = " + ".join(f"{col}:C(macrozona)" for col in spline_cols)
    rhs = (
        "C(month_of_year) + d_estallido*C(macrozona) + d_pandemia*C(macrozona) + "
        f"{spline_terms} + {spline_interactions} + C(region)"
    )
    return f"{outcome} ~ {rhs}"


def fit_category(panel: pd.DataFrame, outcome: str):
    df, spline_cols, knots = add_spline_basis(panel, n_knots=3)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = smf.glm(
            interaction_formula(outcome, spline_cols),
            data=df,
            family=sm.families.Poisson(),
            offset=np.log(df["pop_monthly"]),
        )
        result = model.fit(maxiter=200, cov_type="cluster", cov_kwds={"groups": df["region"]})
        fallback = model.fit(maxiter=200, cov_type="HC1")
    return result, fallback, df, spline_cols, knots


def combined_effect(result, fallback, term: str, macrozona: str) -> dict:
    names = list(result.params.index)
    lvec = np.zeros(len(names))
    if term in names:
        lvec[names.index(term)] = 1.0
    interaction_names = [
        f"{term}:C(macrozona)[T.{macrozona}]",
        f"C(macrozona)[T.{macrozona}]:{term}",
    ]
    for inter in interaction_names:
        if inter in names:
            lvec[names.index(inter)] = 1.0
    est = float(np.dot(lvec, result.params))
    cov = result.cov_params()
    variance = float(np.dot(lvec, np.dot(cov, lvec)))
    se_source = "cluster_region"
    if variance <= 0 or not np.isfinite(variance):
        cov = fallback.cov_params()
        variance = float(np.dot(lvec, np.dot(cov, lvec)))
        se_source = "HC1_fallback_non_psd_cluster"
    se = float(np.sqrt(variance)) if variance > 0 else np.nan
    return {
        "estimate": est,
        "std_error": se,
        "p_value": normal_pvalue(est, se),
        "irr": safe_exp(est),
        "irr_ci_lower": safe_exp(est - 1.96 * se),
        "irr_ci_upper": safe_exp(est + 1.96 * se),
        "se_source": se_source,
    }


def shock_table(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label, outcome in [
        ("confrontational", "n_confrontational"),
        ("snatching", "n_snatching"),
        ("non_confrontational", "n_non_confrontational"),
    ]:
        result, fallback, _, spline_cols, knots = fit_category(panel, outcome)
        macrozones = list(panel["macrozona"].cat.categories)
        for shock in ["d_estallido", "d_pandemia"]:
            for macro in macrozones:
                eff = combined_effect(result, fallback, shock, macro)
                rows.append(
                    {
                        "category": label,
                        "shock": shock,
                        "macrozona": macro,
                        "knots": ";".join(f"{k:.1f}" for k in knots),
                        **eff,
                    }
                )
        for spline in spline_cols:
            for macro in macrozones:
                eff = combined_effect(result, fallback, spline, macro)
                rows.append(
                    {
                        "category": label,
                        "shock": spline,
                        "macrozona": macro,
                        "knots": ";".join(f"{k:.1f}" for k in knots),
                        **eff,
                    }
                )
    return pd.DataFrame(rows)


def plot_shocks(table: pd.DataFrame) -> None:
    shock_df = table.loc[table["shock"].isin(["d_estallido", "d_pandemia"])].copy()
    category_order = ["confrontational", "snatching", "non_confrontational"]
    macro_order = list(shock_df["macrozona"].drop_duplicates())
    fig, axes = plt.subplots(1, 3, figsize=(12, 4.8), sharey=True)
    colors = {"d_estallido": "#2166ac", "d_pandemia": "#b2182b"}
    offsets = {"d_estallido": -0.12, "d_pandemia": 0.12}
    for ax, category in zip(axes, category_order):
        sub = shock_df.loc[shock_df["category"].eq(category)]
        ybase = np.arange(len(macro_order))
        for shock, shock_label in [("d_estallido", "Social uprising"), ("d_pandemia", "Pandemic")]:
            ss = sub.loc[sub["shock"].eq(shock)].set_index("macrozona").loc[macro_order].reset_index()
            ypos = ybase + offsets[shock]
            stable = (
                ss["se_source"].eq("cluster_region")
                & np.isfinite(ss["irr_ci_lower"])
                & np.isfinite(ss["irr_ci_upper"])
                & ((ss["irr_ci_upper"] - ss["irr_ci_lower"]) < 2.0)
            )
            if stable.any():
                stable_ss = ss.loc[stable]
                ax.errorbar(
                    stable_ss["irr"],
                    ypos[stable.to_numpy()],
                    xerr=[
                        stable_ss["irr"] - stable_ss["irr_ci_lower"],
                        stable_ss["irr_ci_upper"] - stable_ss["irr"],
                    ],
                    fmt="o",
                    color=colors[shock],
                    capsize=2,
                    label=shock_label if category == category_order[0] else None,
                )
            if (~stable).any():
                unstable_ss = ss.loc[~stable]
                ax.scatter(
                    unstable_ss["irr"],
                    ypos[(~stable).to_numpy()],
                    facecolors="none",
                    edgecolors=colors[shock],
                    s=32,
                    linewidths=1.3,
                )
        ax.axvline(1, color="#737373", lw=0.9, ls="--")
        ax.set_title(category.replace("_", " ").title(), fontsize=10)
        ax.set_xlabel("IRR")
        ax.set_xlim(0.35, 1.45)
        ax.set_yticks(ybase)
        ax.set_yticklabels(macro_order)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].legend(frameon=False, loc="upper left", bbox_to_anchor=(0.0, -0.12), ncols=2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(FIGURE_DIR / "fig9_macrozona_shock_effects.png", dpi=300)
    fig.savefig(FIGURE_DIR / "fig9_macrozona_shock_effects.pdf")
    plt.close(fig)


def plot_macrozona_trends(panel: pd.DataFrame) -> None:
    trend = (
        panel.groupby(["macrozona", "date"], observed=True, as_index=False)
        .agg(
            n_confrontational=("n_confrontational", "sum"),
            n_non_confrontational=("n_non_confrontational", "sum"),
            pop=("pop_monthly", "sum"),
        )
        .sort_values(["macrozona", "date"])
    )
    trend["share"] = trend["n_confrontational"] / (trend["n_confrontational"] + trend["n_non_confrontational"])
    trend["rate"] = trend["n_confrontational"] / trend["pop"] * 100000

    macrozones = list(panel["macrozona"].cat.categories)
    fig, axes = plt.subplots(len(macrozones), 1, figsize=(10, 9), sharex=True)
    for ax, macro in zip(axes, macrozones):
        sub = trend.loc[trend["macrozona"].eq(macro)]
        ax.axvspan(pd.Timestamp("2019-10-01"), pd.Timestamp("2020-02-29"), color="#d9d9d9", alpha=0.45, lw=0)
        ax.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2021-12-31"), color="#efefef", alpha=0.75, lw=0)
        ax.plot(sub["date"], sub["share"], color="#b2182b", lw=1.2)
        ax.set_ylabel(macro)
        ax.yaxis.set_major_formatter(lambda x, pos: f"{x:.0%}")
        ax.spines[["top", "right"]].set_visible(False)
    axes[-1].set_xlabel("")
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "fig9b_macrozona_composition_trends.png", dpi=300)
    fig.savefig(FIGURE_DIR / "fig9b_macrozona_composition_trends.pdf")
    plt.close(fig)


def main() -> None:
    ensure_output_dirs()
    panel = read_region_panel()
    table = shock_table(panel)
    table.to_csv(TABLE_DIR / "tabla_4b_macrozona_shock_interactions.csv", index=False)
    plot_shocks(table)
    plot_macrozona_trends(panel)

    print("Macrozone shock interactions complete.")
    print(
        table.loc[table["shock"].isin(["d_estallido", "d_pandemia"]), ["category", "shock", "macrozona", "irr", "p_value"]]
        .head(30)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
