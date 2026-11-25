"""Session 1: three simple FP&A baselines, forecast with a rolling origin.

  B0  last quarter              (sanity check only)
  B1  same quarter last year
  B2  same quarter last year x (1 + growth), where growth = the last 4
      known quarters vs the 4 quarters before them

Rolling origin: for each origin quarter (2013 Q1, 2013 Q2, ...) we pretend
today is 65 days after that quarter ended, and use only the quarters whose
first_filed_date is on or before that day. From there we forecast the next
1, 2, 3 and 4 quarters (h = 1, 2, 3, 4).

Run from the project folder (prints one worked example):
    .venv/bin/python src/baselines.py
"""

from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
DATA = PROJECT / "data" / "processed" / "revenue_quarterly.csv"

FIRST_ORIGIN = pd.Period("2013Q1", freq="Q")   # Sessions 1-3 (and the worked examples)
HISTORY_QUARTERS = 20         # Session 4 rule: first origin after 5 years of a company's own history
HORIZONS = [1, 2, 3, 4]
DAYS_AFTER_QUARTER_END = 65   # large companies must file the 10-K within 60 days
BASELINES = ["B0", "B1", "B2"]
ORIGINAL_COMPANIES = ["Mattel", "Caterpillar", "Alphabet"]   # Sessions 0-3


# --- 1. Data ---------------------------------------------------------------

def load(value_col="revenue_first_reported", companies=None):
    """The quarterly table, with a 'quarter' column and a 'value' column holding
    the revenue series we forecast. `companies` picks (and orders) companies.

    'quarter' is the FISCAL quarter written as a period label, e.g. 2026Q1 for
    the first quarter of fiscal 2026 (for Microsoft that is Jul-Sep 2025).
    For December year ends it equals the calendar quarter. The real end date
    of each quarter is in 'period_end'.
    """
    from companies import SERIES_START
    df = pd.read_csv(DATA, parse_dates=["period_end", "first_filed_date"])
    if companies is not None:
        df = pd.concat([df[df["company"] == c] for c in companies], ignore_index=True)
    df["quarter"] = pd.PeriodIndex.from_fields(
        year=df["fiscal_year"], quarter=df["fiscal_quarter"], freq="Q")
    for company, start in SERIES_START.items():          # e.g. Best Buy after its fiscal-year change
        df = df[(df["company"] != company) | (df["quarter"] >= pd.Period(start, freq="Q"))]
    df = df.reset_index(drop=True)
    df["value"] = df[value_col]
    return df


def quarter_end_date(company_df, quarter):
    """The real end date of a company's fiscal quarter (estimated from the
    nearest earlier quarter, 91 days per quarter, if that quarter is missing)."""
    rows = company_df[company_df["quarter"] <= quarter]
    if rows.empty:
        return pd.Timestamp(quarter.end_time.date())
    last = rows.loc[rows["quarter"].idxmax()]
    return pd.Timestamp(last["period_end"]) + timedelta(days=91 * (quarter - last["quarter"]).n)


def cutoff_date(origin, company_df=None):
    """The day we pretend it is: 65 days after the origin quarter ended.
    With company_df, the end of that company's own fiscal quarter is used."""
    if company_df is None:
        quarter_end = pd.Timestamp(origin.end_time.date())
    else:
        quarter_end = quarter_end_date(company_df, origin)
    return quarter_end + timedelta(days=DAYS_AFTER_QUARTER_END)


def first_origin(company_df):
    """The first forecast origin: after 5 years (20 quarters) of the company's history."""
    return company_df["quarter"].min() + (HISTORY_QUARTERS - 1)


def known_at(company_df, origin):
    """Revenue of the quarters that were public on the cutoff date,
    as a Series: quarter -> revenue, oldest first."""
    public = company_df["first_filed_date"] <= cutoff_date(origin, company_df)
    known = company_df[public & (company_df["quarter"] <= origin)]
    return known.set_index("quarter")["value"].sort_index()


# --- 2. The three baselines -------------------------------------------------
# Each one gets the known quarters and the target quarter, and returns a forecast.

def b0_last_quarter(known, target):
    """B0: next quarter(s) = the latest known quarter."""
    return known.iloc[-1]


def b1_same_quarter_last_year(known, target):
    """B1: the latest known value of the same quarter (Q1 for a Q1 target, ...).
    That is normally last year's; if last year's is not public yet, the year before."""
    same_quarter = known[known.index.quarter == target.quarter]
    return same_quarter.iloc[-1] if len(same_quarter) else np.nan


def growth_window(known):
    """The 8 most recent consecutive known quarters (oldest first), or None.
    Normally these are simply the last 8 quarters. If a quarter in between
    is not public yet, we step back to the latest complete set of 8."""
    for end in reversed(known.index):
        window = pd.period_range(end - 7, end, freq="Q")
        if all(q in known.index for q in window):
            return window
    return None


def growth(known):
    """Growth of the last 4 known quarters vs the 4 before them."""
    window = growth_window(known)
    if window is None:
        return np.nan
    return known[window[4:]].sum() / known[window[:4]].sum() - 1


def b2_same_quarter_times_growth(known, target):
    """B2: B1 x (1 + growth)."""
    return b1_same_quarter_last_year(known, target) * (1 + growth(known))


FORECASTERS = {"B0": b0_last_quarter,
               "B1": b1_same_quarter_last_year,
               "B2": b2_same_quarter_times_growth}


def seasonal_naive_scale(known):
    """MASE scale: the average in-sample error of 'same quarter last year',
    i.e. mean |y[q] - y[q - 4]| over the known quarters. Only data known
    at the origin is used."""
    errors = [abs(v - known[q - 4]) for q, v in known.items() if q - 4 in known.index]
    return np.mean(errors)


# --- 3. Rolling origin -----------------------------------------------------

def rolling_forecasts(df):
    """One row per company x origin x horizon, with every baseline's
    forecast and the actual revenue of the target quarter."""
    rows = []
    for company, cdf in df.groupby("company", sort=False):
        actual = cdf.set_index("quarter")["value"]
        last_quarter = actual.index.max()
        origin = first_origin(cdf)                   # after 5 years of history
        while origin + 1 <= last_quarter:            # last origin: h = 1 still has an actual
            known = known_at(cdf, origin)
            scale = seasonal_naive_scale(known)
            for h in HORIZONS:
                target = origin + h
                if target > last_quarter:
                    break
                if target not in actual.index:       # a missing quarter: nothing to compare with
                    continue
                row = {"company": company, "origin": origin, "h": h, "target": target,
                       "last_known": known.index[-1], "actual": actual[target],
                       "mase_scale": scale}
                for name, forecast in FORECASTERS.items():
                    row[name] = forecast(known, target)
                rows.append(row)
            origin += 1
    return pd.DataFrame(rows)


# --- 4. A worked example you can check by hand --------------------------------

def worked_example(df, company, origin):
    cdf = df[df["company"] == company]
    known = known_at(cdf, origin)
    m = 1e6                                            # show $ millions

    print(f"{company}, origin {origin}: we pretend it is {cutoff_date(origin, cdf).date()}")
    print(f"Latest public quarter: {known.index[-1]}\n")

    window = growth_window(known)
    last4, prev4 = known[window[4:]], known[window[:4]]
    print("Growth = last 4 known quarters vs the 4 before them ($m):")
    for (q_prev, v_prev), (q_last, v_last) in zip(prev4.items(), last4.items()):
        print(f"  {q_prev}  {v_prev / m:>8,.1f}      {q_last}  {v_last / m:>8,.1f}")
    g = last4.sum() / prev4.sum() - 1
    print(f"  sum     {prev4.sum() / m:>8,.1f}      sum     {last4.sum() / m:>8,.1f}"
          f"   -> growth = {last4.sum() / m:,.1f} / {prev4.sum() / m:,.1f} - 1 = {g:+.2%}\n")

    print("Forecasts ($m):")
    print(f"  {'h':<2} {'target':<7} {'B0 = last quarter':<20} {'B1 = same quarter':<24} B2 = B1 x (1 + growth)")
    for h in HORIZONS:
        target = origin + h
        base_q = known[known.index.quarter == target.quarter].index[-1]
        b0, b1, b2 = (FORECASTERS[n](known, target) / m for n in BASELINES)
        print(f"  {h:<2} {str(target):<7} {known.index[-1]} = {b0:>8,.1f}   "
              f"{base_q} = {b1:>8,.1f}      {b1:,.1f} x {1 + g:.4f} = {b2:>8,.1f}")


if __name__ == "__main__":
    worked_example(load(), "Mattel", FIRST_ORIGIN)
