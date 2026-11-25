"""Session 5: the feature table for LightGBM.

One row = one company, one origin quarter o, one horizon h (1-4).

Target (what the model learns to predict):
    growth vs the same quarter last year, h quarters ahead, on the log scale
    target = log(revenue[o+h]) - log(revenue[o+h-4])
    (0.10 means about +10.5 %; the forecast is then revenue[o+h-4] x exp(prediction))

Features, all known at the origin:
    yoy_0 .. yoy_3   the last 4 year-on-year growths: log(rev[o-k]) - log(rev[o-k-4]), k = 0..3
    qoq              the last quarter-on-quarter growth: log(rev[o]) - log(rev[o-1])
    target_quarter   which fiscal quarter the target is (1-4), a category
    type             company type (Seasonal, Growth tech, ...), a category
Not used: company name, and anything about 2020 (a forecast made in 2019
couldn't know about 2020). A missing quarter gives a missing feature
(LightGBM handles missing values).

public_date: the day the LAST piece of the row became public, the target or any
quarter used in its features. A model trained at some origin may only use rows
whose public_date is on or before that origin's cutoff date.

Revenue is first-reported revenue (what was known at the time).

Run from the project folder (prints the table's size and one example row):
    .venv/bin/python src/features.py
"""

import numpy as np
import pandas as pd

from baselines import HORIZONS, load
from companies import COMPANIES, TYPES, company_type

ALL = list(COMPANIES)
FEATURES = ["yoy_0", "yoy_1", "yoy_2", "yoy_3", "qoq", "target_quarter", "type"]
CATEGORICAL = ["target_quarter", "type"]


def row_for(logrev, filed, company, origin, h):
    """One row of the table from log revenue and filing dates (Series indexed by quarter).

    Quarters missing from `logrev` give missing (NaN) features. Works both on a
    company's full history (to build training rows) and on only the quarters
    known at an origin (to build the row we forecast from)."""
    def lv(q):
        return logrev.get(q, np.nan)

    target_q, base_q = origin + h, origin + h - 4
    row = {"company": company, "type": company_type(company), "origin": origin, "h": h,
           "target_q": target_q, "target_quarter": target_q.quarter,
           "base_q": base_q, "base_log": lv(base_q)}
    for k in range(4):
        row[f"yoy_{k}"] = lv(origin - k) - lv(origin - k - 4)
    row["qoq"] = lv(origin) - lv(origin - 1)
    row["target"] = lv(target_q) - lv(base_q)

    used = {origin - k for k in range(8)} | {target_q, base_q}
    dates = [filed[q] for q in used if q in filed.index]
    row["public_date"] = max(dates) if dates else pd.NaT
    return row


def build_table(df=None):
    """All rows with a known target, for every company and origin in the data."""
    if df is None:
        df = load(companies=ALL)                     # first-reported revenue
    rows = []
    for company, cdf in df.groupby("company", sort=False):
        s = cdf.set_index("quarter")
        logrev, filed = np.log(s["value"]), s["first_filed_date"]
        for origin in s.index:
            for h in HORIZONS:
                if origin + h in s.index:            # the target must exist
                    rows.append(row_for(logrev, filed, company, origin, h))
    t = pd.DataFrame(rows)
    t["type"] = pd.Categorical(t["type"], categories=TYPES)
    t["target_quarter"] = pd.Categorical(t["target_quarter"], categories=[1, 2, 3, 4])
    return t


def describe_example(t, company="Mattel", origin="2013Q1", h=1):
    r = t[(t["company"] == company) & (t["origin"] == pd.Period(origin, freq="Q")) & (t["h"] == h)].iloc[0]
    pct = lambda x: f"{100 * (np.exp(x) - 1):+.1f} %"
    o = r["origin"]
    print(f"{company}, origin {o}, h = {h}: predict growth of {r['target_q']} vs {r['base_q']}")
    print(f"  target  = log(rev {r['target_q']}) - log(rev {r['base_q']}) = {r['target']:+.4f}  ({pct(r['target'])})")
    for k in range(4):
        print(f"  yoy_{k}   = {o - k} vs {o - k - 4}: {r[f'yoy_{k}']:+.4f}  ({pct(r[f'yoy_{k}'])})")
    print(f"  qoq     = {o} vs {o - 1}: {r['qoq']:+.4f}  ({pct(r['qoq'])})")
    print(f"  target_quarter = {r['target_quarter']}   type = {r['type']}")
    print(f"  public_date = {r['public_date'].date()}  (the last quarter used became public then)")


if __name__ == "__main__":
    t = build_table()
    print(f"{len(t):,} rows, {t['company'].nunique()} companies; rows per h: "
          f"{t.groupby('h').size().to_dict()}")
    print(f"targets from {t['target_q'].min()} to {t['target_q'].max()}; "
          f"public dates {t['public_date'].min().date()} to {t['public_date'].max().date()}")
    print("missing values per column:", t[FEATURES + ["target"]].isna().sum().to_dict(), "\n")
    describe_example(t)
