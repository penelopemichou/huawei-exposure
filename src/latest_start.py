"""Session 6: start from the LATEST quarter instead of the same quarter last year.

B3, a new simple rule:
    forecast for t+h = revenue[t] x revenue[t+h-4] / revenue[t-4]
    i.e. the latest known quarter, moved by the same step as last year
    (last year, how did revenue change from quarter t-4 to quarter t+h-4?).
If last year's step isn't public yet (rare), the step from two years ago is
used, as B1 does for its base.

New LightGBM target: change from the latest known quarter, in logs:
    target = log(revenue[t+h]) - log(revenue[t])
Features (all known at the origin):
    step_ly          last year's same step: log(revenue[t+h-4]) - log(revenue[t-4])
    yoy_0 .. yoy_3, qoq, target_quarter, type   the Session 5 features
(At h = 4, step_ly equals yoy_0: last year's 4-quarter step IS this year's
year-on-year growth.)
public_date: as in Session 5, the day the last quarter used became public.

Run from the project folder (prints the table, one example row and B3's worked example):
    .venv/bin/python src/latest_start.py
"""

import numpy as np
import pandas as pd

from baselines import FORECASTERS, HORIZONS, cutoff_date, first_origin, known_at, load
from companies import COMPANIES, TYPES
from features import row_for as session5_row

ALL = list(COMPANIES)
FEATURES = ["step_ly", "yoy_0", "yoy_1", "yoy_2", "yoy_3", "qoq", "target_quarter", "type"]
CATEGORICAL = ["target_quarter", "type"]


# --- B3 ---------------------------------------------------------------------------

def b3_latest_times_last_years_step(known, target):
    """B3: latest known quarter x last year's same step.

    t = the latest known quarter. Usually the step is from t-4 to target-4; if
    target-4 is not public yet, go back one more year (t-8 to target-8)."""
    t = known.index[-1]
    k = 1
    while target - 4 * k > t:
        k += 1
    a, b = t - 4 * k, target - 4 * k
    if a not in known.index or b not in known.index:
        return np.nan
    # Divide first: revenue is stored as whole numbers, and multiplying two
    # ~$100 bn whole numbers overflows (it wraps around to nonsense).
    return float(known[t]) * (float(known[b]) / float(known[a]))


# --- Feature table ------------------------------------------------------------------

def row_for(logrev, filed, company, origin, h):
    """One row: the Session 5 row, with the new target and the step_ly feature."""
    row = session5_row(logrev, filed, company, origin, h)
    lv = lambda q: logrev.get(q, np.nan)
    row["step_ly"] = lv(origin + h - 4) - lv(origin - 4)
    row["start_log"] = lv(origin)
    row["target"] = lv(origin + h) - lv(origin)                 # change from the latest quarter
    return row


def build_table(df=None):
    if df is None:
        df = load(companies=ALL)
    rows = []
    for company, cdf in df.groupby("company", sort=False):
        s = cdf.set_index("quarter")
        logrev, filed = np.log(s["value"]), s["first_filed_date"]
        for origin in s.index:
            for h in HORIZONS:
                if origin + h in s.index:
                    rows.append(row_for(logrev, filed, company, origin, h))
    t = pd.DataFrame(rows).drop(columns=["base_q", "base_log"])
    t["type"] = pd.Categorical(t["type"], categories=TYPES)
    t["target_quarter"] = pd.Categorical(t["target_quarter"], categories=[1, 2, 3, 4])
    return t


# --- Worked examples -----------------------------------------------------------------

def describe_example(t, company="Mattel", origin="2013Q1", h=1):
    r = t[(t["company"] == company) & (t["origin"] == pd.Period(origin, freq="Q")) & (t["h"] == h)].iloc[0]
    pct = lambda x: f"{100 * (np.exp(x) - 1):+.1f} %"
    o = r["origin"]
    print(f"{company}, origin {o}, h = {h}: predict the change from {o} to {r['target_q']}")
    print(f"  target  = log(rev {r['target_q']}) - log(rev {o}) = {r['target']:+.4f}  ({pct(r['target'])})")
    print(f"  step_ly = log(rev {o + h - 4}) - log(rev {o - 4}) = {r['step_ly']:+.4f}  ({pct(r['step_ly'])})   <- last year's same step")
    for k in range(4):
        print(f"  yoy_{k}   = {o - k} vs {o - k - 4}: {r[f'yoy_{k}']:+.4f}  ({pct(r[f'yoy_{k}'])})")
    print(f"  qoq     = {o} vs {o - 1}: {r['qoq']:+.4f}  ({pct(r['qoq'])})")
    print(f"  target_quarter = {r['target_quarter']}   type = {r['type']}")
    print(f"  public_date = {r['public_date'].date()}")


def b3_worked_example(company="Mattel"):
    df = load(companies=ALL)
    cdf = df[df["company"] == company]
    origin = first_origin(cdf)
    known = known_at(cdf, origin)
    t = known.index[-1]
    m = 1e6
    print(f"{company}, first origin {origin}: we pretend it is {cutoff_date(origin, cdf).date()}; "
          f"latest known quarter {t} = {known[t] / m:,.1f}\n")
    print(f"  {'h':<2} {'target':<7} {'last year step':<22} {'B3 = latest x step':<30} {'B1':>8} {'B2':>8}")
    for h in HORIZONS:
        target = origin + h
        a, b = t - 4, target - 4
        step = known[b] / known[a]
        b3 = b3_latest_times_last_years_step(known, target)
        print(f"  {h:<2} {str(target):<7} {f'{b} / {a} = {step:.4f}':<22} "
              f"{f'{known[t] / m:,.1f} x {step:.4f} = {b3 / m:,.1f}':<30} "
              f"{FORECASTERS['B1'](known, target) / m:>8,.1f} {FORECASTERS['B2'](known, target) / m:>8,.1f}")
    print("\n  Last year's quarters ($m): " + ", ".join(f"{q} = {known[q] / m:,.1f}" for q in [t - 4, t - 3, t - 2, t - 1]))


if __name__ == "__main__":
    t = build_table()
    print(f"{len(t):,} rows; rows per h: {t.groupby('h').size().to_dict()}")
    print("missing values:", t[FEATURES + ["target"]].isna().sum().to_dict(), "\n")
    describe_example(t)
    print()
    b3_worked_example()
