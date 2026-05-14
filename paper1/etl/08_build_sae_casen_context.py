"""
08_build_sae_casen_context.py -- SAE communal income-poverty context.

Decision for this revision: use poverty by income, not multidimensional poverty,
for communal socioeconomic heterogeneity. Income poverty is the more direct
proxy for economic strain and is available in comparable SAE files for 2017,
2022, and 2024 using current commune codes.

Outputs:
  - paper1/output/data/sae_pobreza_comunal.csv
  - paper1/output/tables/sae_pobreza_comunal_qa.csv
"""

from pathlib import Path
import unicodedata

import pandas as pd


SOURCES = [
    {
        "year": 2017,
        "path": Path("data/Estimaciones_pobreza_comunal/SAE_ingresos_multidimensional_2017.xlsx"),
        "sheet": "Ingresos 2017",
    },
    {
        "year": 2022,
        "path": Path("data/Estimaciones_pobreza_comunal/SAE_ingresos_2022.xlsx"),
        "sheet": "Estimaciones",
    },
    {
        "year": 2024,
        "path": Path("data/Estimaciones_pobreza_comunal/SAE_ingresos_2024.xlsx"),
        "sheet": "Sheet1",
    },
]

OUT_DATA = Path("paper1/output/data/sae_pobreza_comunal.csv")
OUT_QA = Path("paper1/output/tables/sae_pobreza_comunal_qa.csv")


def find_col(columns: list[str], starts: str | None = None, contains: str | None = None) -> str:
    for col in columns:
        norm = normalize_col(col)
        if starts and norm.startswith(normalize_col(starts)):
            return col
        if contains and normalize_col(contains) in norm:
            return col
    raise KeyError(f"Could not find column starts={starts!r} contains={contains!r}")


def normalize_col(value) -> str:
    text = " ".join(str(value).replace("\n", " ").split()).lower()
    text = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def read_source(src: dict) -> pd.DataFrame:
    df = pd.read_excel(src["path"], sheet_name=src["sheet"])
    cols = list(df.columns)
    code_col = find_col(cols, starts="codigo")
    region_col = find_col(cols, starts="region")
    comuna_col = find_col(cols, starts="nombre comuna")
    n_col = find_col(cols, starts="numero de personas en situacion de pobreza")
    rate_col = find_col(cols, starts="porcentaje de personas")
    low_col = find_col(cols, starts="limite inferior")
    high_col = find_col(cols, starts="limite superior")

    # The last metadata column changed names across releases.
    estimation_col = None
    sample_col = None
    for col in cols:
        norm = normalize_col(col)
        if "tipo de estimacion" in norm or "metodologia de estimacion" in norm:
            estimation_col = col
        if "presencia de la comuna" in norm:
            sample_col = col

    out = pd.DataFrame(
        {
            "year": src["year"],
            "comuna": pd.to_numeric(df[code_col], errors="coerce"),
            "region_name_sae": df[region_col],
            "comuna_name": df[comuna_col],
            "poverty_income_n": pd.to_numeric(df[n_col], errors="coerce"),
            "poverty_income_rate": pd.to_numeric(df[rate_col], errors="coerce"),
            "poverty_income_ci_low": pd.to_numeric(df[low_col], errors="coerce"),
            "poverty_income_ci_high": pd.to_numeric(df[high_col], errors="coerce"),
            "estimation_type": df[estimation_col] if estimation_col else pd.NA,
            "in_casen_sample": df[sample_col] if sample_col else pd.NA,
            "source_file": src["path"].name,
            "source_sheet": src["sheet"],
        }
    )
    out = out[out["comuna"].notna()].copy()
    out["comuna"] = out["comuna"].astype(int)
    out["region"] = out["comuna"] // 1000
    return out


def main() -> None:
    OUT_DATA.parent.mkdir(parents=True, exist_ok=True)
    OUT_QA.parent.mkdir(parents=True, exist_ok=True)

    frames = [read_source(src) for src in SOURCES]
    sae = pd.concat(frames, ignore_index=True)
    sae = sae.sort_values(["comuna", "year"]).reset_index(drop=True)

    qa = (
        sae.groupby("year")
        .agg(
            rows=("comuna", "size"),
            communes=("comuna", "nunique"),
            regions=("region", "nunique"),
            missing_rate=("poverty_income_rate", lambda s: int(s.isna().sum())),
            min_rate=("poverty_income_rate", "min"),
            max_rate=("poverty_income_rate", "max"),
        )
        .reset_index()
    )
    qa["expected_communes"] = 345
    qa["passed"] = (qa["communes"] == 345) & (qa["missing_rate"] == 0)

    print(qa.to_string(index=False))
    if not bool(qa["passed"].all()):
        raise SystemExit("SAE QA failed.")

    sae.to_csv(OUT_DATA, index=False)
    qa.to_csv(OUT_QA, index=False)
    print(f"\nSaved {OUT_DATA}")
    print(f"Saved {OUT_QA}")


if __name__ == "__main__":
    main()
