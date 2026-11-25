"""Session 7: is smoothing the reason ETS wins?

B4, the only new rule (fixed before any results; no variants):
    forecast for t+h = revenue[t] x geometric mean over k = 1, 2, 3 of
                       revenue[t+h-4k] / revenue[t-4k]
    i.e. the latest known quarter, moved by the AVERAGE of the same step over
    the last 3 years (B3 uses only last year's step).
If fewer than 3 years of steps are public, the ones that are public are used.
If last year's step isn't public yet (rare), the 3 years start one year earlier,
as in B3.

Run from the project folder (prints the Mattel worked example):
    .venv/bin/python src/smoothing.py
"""

import numpy as np

from baselines import HORIZONS, cutoff_date, first_origin, known_at, load
from companies import COMPANIES
from latest_start import b3_latest_times_last_years_step

ALL = list(COMPANIES)
YEARS = 3


def b4_steps(known, target):
    """The (up to 3) year-ago steps B4 averages: list of (from quarter, to quarter, ratio)."""
    t = known.index[-1]
    k = 1
    while target - 4 * k > t:                 # last year's step not public yet: start a year earlier
        k += 1
    steps = []
    for kk in range(k, k + YEARS):
        a, b = t - 4 * kk, target - 4 * kk
        if a in known.index and b in known.index:
            steps.append((a, b, float(known[b]) / float(known[a])))
    return steps


def b4_latest_times_average_step(known, target):
    """B4: latest known quarter x geometric mean of the same step over the last 3 years."""
    steps = b4_steps(known, target)
    if not steps:
        return np.nan
    t = known.index[-1]
    geo_mean = float(np.exp(np.mean([np.log(r) for _, _, r in steps])))
    return float(known[t]) * geo_mean


def worked_example(company="Mattel"):
    from ets import ets_at_origin
    df = load(companies=ALL)
    cdf = df[df["company"] == company]
    origin = first_origin(cdf)
    known = known_at(cdf, origin)
    t = known.index[-1]
    targets = [origin + h for h in HORIZONS]
    ets = ets_at_origin(known, targets)
    m = 1e6
    print(f"{company}, first origin {origin}: we pretend it is {cutoff_date(origin, cdf).date()}; "
          f"latest known quarter {t} = {known[t] / m:,.1f}\n")
    for h, target, e in zip(HORIZONS, targets, ets):
        steps = b4_steps(known, target)
        geo = np.exp(np.mean([np.log(r) for _, _, r in steps]))
        b4 = b4_latest_times_average_step(known, target)
        b3 = b3_latest_times_last_years_step(known, target)
        print(f"h = {h}, target {target}:")
        for a, b, r in steps:
            print(f"    {b} / {a} = {known[b] / m:,.1f} / {known[a] / m:,.1f} = {r:.4f}")
        print(f"    geometric mean = ({' x '.join(f'{r:.4f}' for _, _, r in steps)})^(1/{len(steps)}) = {geo:.4f}")
        print(f"    B4 = {known[t] / m:,.1f} x {geo:.4f} = {b4 / m:,.1f}    "
              f"(B3 = {b3 / m:,.1f} uses only {steps[0][2]:.4f};  ETS = {e['ets'] / m:,.1f})\n")


if __name__ == "__main__":
    worked_example()
