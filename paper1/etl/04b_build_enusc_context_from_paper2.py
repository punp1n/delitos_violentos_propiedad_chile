"""
04b_build_enusc_context_from_paper2.py
======================================

Builds a compact ENUSC context series for paper1 using the harmonized paper2
ENUSC panel. This is intentionally descriptive: it tracks public perception and
personal victimization, but it does not validate CUM-level C3 classifications.

Inputs:
  - paper2/output/data/enusc_panel_kish.parquet
  - paper2/output/tables/percepcion_por_anio.csv (optional QA comparison)

Outputs:
  - paper1/output/tables/enusc_context_series.csv
  - paper1/output/tables/enusc_context_qa.csv
  - paper1/output/figures/fig_enusc_perception_context.png
  - paper1/output/figures/fig_enusc_perception_context.pdf
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


REQUIRED_COLUMNS = {
    "anio",
    "enc_region",
    "com102",
    "weight",
    "varstrat",
    "conglomerado",
    "percep_pais",
    "percep_com",
    "percep_barrio",
    "vict_rvi",
    "vict_rps",
    "vict_delitos_especificos",
}

EXPECTED_WEIGHTED_N = 238_262


def find_project_root(start: Path | None = None) -> Path:
    """Find repository root containing paper1, paper2, and data."""
    current = (start or Path.cwd()).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "paper1").is_dir() and (candidate / "paper2").is_dir() and (candidate / "data").is_dir():
            return candidate
    raise FileNotFoundError("Could not find project root containing paper1, paper2, and data.")


def pct_wtd(group: pd.DataFrame, var: str) -> float:
    """
    Weighted percent using the same denominator convention as paper2.

    Denominator: all Kish observations with valid 102-commune weight.
    Numerator: weighted observations where var == 1. Missing/NS/NR remain in
    the denominator, matching the INE-style descriptive series in paper2.
    """
    weight = group["weight"]
    total_weight = weight.sum()
    if total_weight <= 0:
        return float("nan")
    numerator = weight[group[var].eq(1)].sum()
    return numerator / total_weight * 100


def build_series(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year, group in panel.groupby("anio", sort=True):
        valid = group[group["weight"].notna() & group["weight"].gt(0)].copy()
        rows.append(
            {
                "anio": int(year),
                "N_kish_total": int(len(group)),
                "N_con_peso": int(len(valid)),
                "N_excluded_weight": int(len(group) - len(valid)),
                "n_regions_total": int(group["enc_region"].nunique(dropna=True)),
                "n_regions_weighted": int(valid["enc_region"].nunique(dropna=True)),
                "pct_pais": round(pct_wtd(valid, "percep_pais"), 2),
                "pct_com": round(pct_wtd(valid, "percep_com"), 2),
                "pct_barrio": round(pct_wtd(valid, "percep_barrio"), 2),
                "pct_vict": round(pct_wtd(valid, "vict_delitos_especificos"), 2),
                "pct_vict_rvi": round(pct_wtd(valid, "vict_rvi"), 2),
                "pct_vict_rps": round(pct_wtd(valid, "vict_rps"), 2),
            }
        )
    return pd.DataFrame(rows)


def build_qa(panel: pd.DataFrame, series: pd.DataFrame, paper2_table: Path) -> pd.DataFrame:
    qa_rows = []
    total_valid_weight = int(panel["weight"].notna().sum())
    qa_rows.append(
        {
            "check": "weighted_n_102_communes",
            "value": total_valid_weight,
            "expected": EXPECTED_WEIGHTED_N,
            "status": "OK" if total_valid_weight == EXPECTED_WEIGHTED_N else "WARN",
            "note": "Kish observations with valid 102-commune weight.",
        }
    )

    for year, group in panel.groupby("anio", sort=True):
        valid = group[group["weight"].notna() & group["weight"].gt(0)]
        invalid = group[~(group["weight"].notna() & group["weight"].gt(0))]
        invalid_are_new_communes = bool(invalid.empty or invalid["com102"].fillna(0).eq(0).all())
        expected_regions = 15 if int(year) <= 2018 else 16
        n_regions = int(valid["enc_region"].nunique(dropna=True))
        qa_rows.append(
            {
                "check": f"regional_coverage_{int(year)}",
                "value": n_regions,
                "expected": expected_regions,
                "status": "OK" if n_regions == expected_regions else "WARN",
                "note": "2016-2018 do not separate Nuble as region 16; avoid regional longitudinal claims unless collapsing Nuble-Biobio.",
            }
        )
        if int(year) in (2023, 2024):
            qa_rows.append(
                {
                    "check": f"new_communes_excluded_{int(year)}",
                    "value": int(len(invalid)),
                    "expected": "invalid weights correspond to com102=0",
                    "status": "OK" if invalid_are_new_communes else "WARN",
                    "note": "Valid 102-commune weights exclude observations from the expanded 136-commune frame.",
                }
            )

    if paper2_table.exists():
        reference = pd.read_csv(paper2_table)
        compare_cols = ["pct_pais", "pct_com", "pct_barrio", "pct_vict"]
        merged = series[["anio", *compare_cols]].merge(
            reference[["anio", *compare_cols]],
            on="anio",
            suffixes=("_paper1", "_paper2"),
        )
        max_diff = max(
            (merged[f"{col}_paper1"] - merged[f"{col}_paper2"]).abs().max()
            for col in compare_cols
        )
        qa_rows.append(
            {
                "check": "replicate_paper2_percepcion_por_anio",
                "value": round(float(max_diff), 8),
                "expected": 0,
                "status": "OK" if max_diff < 1e-8 else "WARN",
                "note": "Maximum absolute difference in percentage points versus paper2/output/tables/percepcion_por_anio.csv.",
            }
        )
    else:
        qa_rows.append(
            {
                "check": "replicate_paper2_percepcion_por_anio",
                "value": "missing reference",
                "expected": "reference table exists",
                "status": "WARN",
                "note": str(paper2_table),
            }
        )

    return pd.DataFrame(qa_rows)


def make_figure(series: pd.DataFrame, out_base: Path) -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
        }
    )

    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(7.2, 5.2),
        sharex=True,
        gridspec_kw={"height_ratios": [1.2, 1.0]},
    )

    perception_colors = {
        "pct_pais": "#1f4e79",
        "pct_com": "#4f8f6f",
        "pct_barrio": "#c46a2b",
    }
    perception_labels = {
        "pct_pais": "Country",
        "pct_com": "Municipality",
        "pct_barrio": "Neighborhood",
    }
    for col, color in perception_colors.items():
        axes[0].plot(
            series["anio"],
            series[col],
            marker="o",
            linewidth=2,
            color=color,
            label=perception_labels[col],
        )
    axes[0].set_ylabel("Perceives crime increased (%)")
    axes[0].set_ylim(35, 95)
    axes[0].legend(ncol=3, frameon=False, loc="upper left")

    victim_colors = {
        "pct_vict": "#6f4e7c",
        "pct_vict_rvi": "#9b2f2f",
        "pct_vict_rps": "#4d6f9f",
    }
    victim_labels = {
        "pct_vict": "Personal victimization basket",
        "pct_vict_rvi": "Robbery with violence/intimidation",
        "pct_vict_rps": "Snatching",
    }
    for col, color in victim_colors.items():
        axes[1].plot(
            series["anio"],
            series[col],
            marker="o",
            linewidth=2,
            color=color,
            label=victim_labels[col],
        )
    axes[1].set_ylabel("Personal victimization (%)")
    axes[1].set_xlabel("ENUSC survey year")
    axes[1].set_ylim(0, max(series[["pct_vict", "pct_vict_rvi", "pct_vict_rps"]].max()) + 1.5)
    axes[1].legend(ncol=1, frameon=False, loc="upper left")

    for ax in axes:
        ax.set_xticks(series["anio"])

    fig.suptitle("ENUSC perception and personal victimization, 2016-2024", y=0.99, fontsize=12)
    fig.tight_layout()
    fig.savefig(out_base.with_suffix(".png"), dpi=300)
    fig.savefig(out_base.with_suffix(".pdf"))
    plt.close(fig)


def main() -> None:
    root = find_project_root()
    input_path = root / "paper2" / "output" / "data" / "enusc_panel_kish.parquet"
    paper2_reference = root / "paper2" / "output" / "tables" / "percepcion_por_anio.csv"
    table_dir = root / "paper1" / "output" / "tables"
    figure_dir = root / "paper1" / "output" / "figures"
    table_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    panel = pd.read_parquet(input_path)
    missing = sorted(REQUIRED_COLUMNS - set(panel.columns))
    if missing:
        raise ValueError(f"Missing required columns in {input_path}: {missing}")

    series = build_series(panel)
    qa = build_qa(panel, series, paper2_reference)

    series_path = table_dir / "enusc_context_series.csv"
    qa_path = table_dir / "enusc_context_qa.csv"
    figure_base = figure_dir / "fig_enusc_perception_context"

    series.to_csv(series_path, index=False)
    qa.to_csv(qa_path, index=False)
    make_figure(series, figure_base)

    print(f"Input: {input_path}")
    print(f"Series: {series_path}")
    print(f"QA: {qa_path}")
    print(f"Figure PNG: {figure_base.with_suffix('.png')}")
    print(f"Figure PDF: {figure_base.with_suffix('.pdf')}")
    print("\nENUSC context series:")
    print(series.to_string(index=False))
    print("\nQA checks:")
    print(qa.to_string(index=False))


if __name__ == "__main__":
    main()
