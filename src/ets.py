"""Session 2: exponential smoothing (AutoETS) with the same rolling origin as the baselines.

At every origin:
  1. take the quarters known at that origin (65-day rule, src/baselines.py),
  2. let AutoETS choose the best ETS model for them by AICc,
  3. forecast the next 1-4 quarters, with an 80 % prediction interval.
The model is chosen again at every origin, using only data known then.

Run from the project folder (prints one worked example):
    .venv/bin/python src/ets.py
"""

import numpy as np
import pandas as pd
from statsforecast.models import AutoETS

from baselines import FIRST_ORIGIN, FORECASTERS, HORIZONS, cutoff_date, first_origin, known_at, load

SEASON_LENGTH = 4          # 4 quarters in a year
LEVEL = 80                 # 80 % prediction interval
MIN_QUARTERS = 12          # train on at least 3 years
SCALE = 1e9                # fit in $ billions (smaller numbers are easier to optimise)


def training_series(known):
    """The latest unbroken stretch of known quarters, at least MIN_QUARTERS long.

    Usually that is simply every known quarter. But ETS needs quarters with no
    holes, and a few origins have one (for example Google's 2012 Q3-Q4 became
    public only in Oct 2013). Then we use the latest unbroken stretch.
    """
    breaks = np.flatnonzero(np.diff(known.index.asi8) != 1) + 1   # where a hole starts
    stretches = np.split(np.arange(len(known)), breaks)
    for stretch in reversed(stretches):
        if len(stretch) >= MIN_QUARTERS:
            return known.iloc[stretch]
    raise ValueError("no stretch of known quarters is long enough")


def model_name(fitted):
    """'ETS(M,Ad,M)' -> 'MAdM'."""
    return fitted.model_["method"].replace("ETS(", "").replace(")", "").replace(",", "")


def ets_at_origin(known, targets):
    """Fit AutoETS on the known quarters and forecast each target quarter."""
    if not targets:
        return []
    train = training_series(known)
    steps = [(t - train.index[-1]).n for t in targets]          # quarters ahead of the last training quarter
    model = AutoETS(season_length=SEASON_LENGTH).fit(train.to_numpy() / SCALE)
    pred = model.predict(h=max(steps), level=[LEVEL])
    out = []
    for target, s in zip(targets, steps):
        out.append({"target": target, "ets": pred["mean"][s - 1] * SCALE,
                    "lo80": pred[f"lo-{LEVEL}"][s - 1] * SCALE,
                    "hi80": pred[f"hi-{LEVEL}"][s - 1] * SCALE,
                    "model": model_name(model), "aicc": model.model_["aicc"],
                    "train_start": train.index[0], "train_end": train.index[-1],
                    "n_train": len(train)})
    return out


def rolling_ets(df):
    """One row per company x origin x horizon (same grid as the baselines)."""
    rows = []
    for company, cdf in df.groupby("company", sort=False):
        actual = cdf.set_index("quarter")["value"]
        last_quarter = actual.index.max()
        origin = first_origin(cdf)                   # after 5 years of history
        while origin + 1 <= last_quarter:
            known = known_at(cdf, origin)
            targets = [origin + h for h in HORIZONS if origin + h in actual.index]
            for row in ets_at_origin(known, targets):
                rows.append({"company": company, "origin": origin,
                             "h": (row["target"] - origin).n,
                             "actual": actual[row["target"]], **row})
            origin += 1
    return pd.DataFrame(rows)


def worked_example(df, company, origin):
    cdf = df[df["company"] == company]
    known = known_at(cdf, origin)
    targets = [origin + h for h in HORIZONS]
    rows = ets_at_origin(known, targets)
    m = 1e6

    print(f"{company}, origin {origin}: we pretend it is {cutoff_date(origin, cdf).date()}")
    print(f"Training quarters: {rows[0]['train_start']} to {rows[0]['train_end']} "
          f"({rows[0]['n_train']} quarters)")
    print(f"Model chosen by AICc: {rows[0]['model']}  (AICc {rows[0]['aicc']:.1f})\n")
    print("Forecasts ($m):")
    print(f"  {'h':<2} {'target':<7} {'ETS':>8}  {'80 % interval':<19} {'B0':>8} {'B1':>8} {'B2':>8}")
    for h, (target, r) in enumerate(zip(targets, rows), start=1):
        b = {n: f(known, target) / m for n, f in FORECASTERS.items()}
        print(f"  {h:<2} {str(target):<7} {r['ets'] / m:>8,.1f}  "
              f"{r['lo80'] / m:>7,.1f} – {r['hi80'] / m:>7,.1f}   "
              f"{b['B0']:>8,.1f} {b['B1']:>8,.1f} {b['B2']:>8,.1f}")


if __name__ == "__main__":
    worked_example(load(), "Mattel", FIRST_ORIGIN)
