"""
Canonical CUM classifications for paper1 ETL.

The revised manuscript uses functional English labels:
  - confrontational: force, intimidation, victim retention, severe outcomes
  - snatching: sudden seizure without prior coercive confrontation
  - non_confrontational: burglary, theft, vehicle theft without violence, etc.

Receptacion/receiving stolen property remains in the broad C1 institutional
universe but is excluded from the C2/C3 modelable property-offense universe.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


CONFRONTATIONAL_CUMS = {802, 803, 827, 828, 829, 861, 862, 867}
SNATCHING_CUMS = {804}
RECEPTACION_CUMS = {812, 864, 869, 2009, 12053}
NON_CONFRONTATIONAL_CUMS = {
    808, 809, 810,
    821, 826, 846, 847, 848, 853, 13028,
    831, 868,
    858,
    870, 871, 872,
    891, 892,
}

# Institutional binary: includes snatching in the violent block and includes
# receptacion in the non-violent administrative block.
C1_VIOLENT_CUMS = CONFRONTATIONAL_CUMS | SNATCHING_CUMS
C1_NON_VIOLENT_CUMS = NON_CONFRONTATIONAL_CUMS | RECEPTACION_CUMS

# ICCS-adjusted binary used in sensitivity checks: snatching is not counted as
# confrontational and receptacion is excluded.
C2_CONFRONTATIONAL_CUMS = CONFRONTATIONAL_CUMS
C2_NON_CONFRONTATIONAL_CUMS = NON_CONFRONTATIONAL_CUMS | SNATCHING_CUMS

ALL_PROPERTY_CUMS = C1_VIOLENT_CUMS | C1_NON_VIOLENT_CUMS
MODELABLE_C3_CUMS = CONFRONTATIONAL_CUMS | SNATCHING_CUMS | NON_CONFRONTATIONAL_CUMS


@dataclass(frozen=True)
class CumClassification:
    cum: int
    c1_violent: float | None
    c2_confrontational: float | None
    c3_category: str | None
    c3_modelable: bool
    excluded_reason: str | None


def classify_cum(cum: int) -> CumClassification:
    cum = int(cum)

    if cum in C1_VIOLENT_CUMS:
        c1 = 1.0
    elif cum in C1_NON_VIOLENT_CUMS:
        c1 = 0.0
    else:
        c1 = None

    if cum in C2_CONFRONTATIONAL_CUMS:
        c2 = 1.0
    elif cum in C2_NON_CONFRONTATIONAL_CUMS:
        c2 = 0.0
    else:
        c2 = None

    if cum in CONFRONTATIONAL_CUMS:
        c3 = "confrontational"
        modelable = True
        reason = None
    elif cum in SNATCHING_CUMS:
        c3 = "snatching"
        modelable = True
        reason = None
    elif cum in NON_CONFRONTATIONAL_CUMS:
        c3 = "non_confrontational"
        modelable = True
        reason = None
    elif cum in RECEPTACION_CUMS:
        c3 = "excluded_receptacion"
        modelable = False
        reason = "receptacion"
    else:
        c3 = None
        modelable = False
        reason = "outside_property_scope"

    return CumClassification(cum, c1, c2, c3, modelable, reason)


def classification_table(cums: Iterable[int] | None = None) -> pd.DataFrame:
    if cums is None:
        cums = sorted(ALL_PROPERTY_CUMS)
    rows = []
    for cum in sorted({int(c) for c in cums}):
        cls = classify_cum(cum)
        rows.append(
            {
                "cum": cls.cum,
                "C1_violento": cls.c1_violent,
                "C2_violento": cls.c2_confrontational,
                "C3_categoria": cls.c3_category,
                "c3_modelable": cls.c3_modelable,
                "excluded_reason": cls.excluded_reason,
            }
        )
    return pd.DataFrame(rows)


def add_classifications(df: pd.DataFrame, cum_col: str = "cum") -> pd.DataFrame:
    out = df.copy()
    out[cum_col] = pd.to_numeric(out[cum_col], errors="coerce").astype("Int64")
    table = classification_table(out[cum_col].dropna().astype(int).unique())
    out = out.merge(table, left_on=cum_col, right_on="cum", how="left", suffixes=("", "_class"))
    if cum_col != "cum":
        out = out.drop(columns=["cum"]).rename(columns={cum_col: "cum"})
    return out


C3_TO_LEGACY_COUNT_COL = {
    "confrontational": "n_robos_violentos",
    "snatching": "n_robos_sorpresa",
    "non_confrontational": "n_robos_no_violentos",
}

C3_TO_NEW_COUNT_COL = {
    "confrontational": "n_confrontational",
    "snatching": "n_snatching",
    "non_confrontational": "n_non_confrontational",
}
