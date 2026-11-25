"""Step 3c: the event rows. For every firm in the frozen lists (64), at its origin (the last fiscal
quarter ending before 16 May 2019): B4 and AutoETS forecasts for h = 1-4, with the copied Project 2
code (known_at = 65-day rule; smoothing.b4_latest_times_average_step; ets.ets_at_origin), as in
forecast-gap's event step. Actual = first-reported revenue.

Signed miss = 100 x (actual - forecast) / actual: positive = revenue came in ABOVE the forecast.

Writes the rows to the file given (default results/event_rows.csv) and prints ONLY the number of rows.
Nothing from the file is printed here.

Run (bash):  ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/event_rows.py [OUT_FILE]
"""

import contextlib
import io
import sys
import warnings
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))
from baselines import HORIZONS, cutoff_date, known_at, load       # noqa: E402  (copied Project 2 code)
from companies import COMPANIES, PROJECT2_COMPANIES                 # noqa: E402
from ets import ets_at_origin                                       # noqa: E402
from smoothing import b4_latest_times_average_step                  # noqa: E402

EVENT = pd.Timestamp("2019-05-16")


def signed_miss(actual, forecast):
    """Signed miss in %: positive = revenue came in above the forecast."""
    return 100 * (actual - forecast) / actual


def main():
    warnings.filterwarnings("ignore")
    out_file = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT / "results" / "event_rows.csv"
    ours = [c for c in COMPANIES if c not in PROJECT2_COMPANIES]
    df = load(companies=ours)
    rows = []
    sink = io.StringIO()
    for c in ours:
        cdf = df[df.company == c]
        actual = cdf.set_index("quarter")["value"]
        origin = cdf.loc[cdf.period_end < EVENT, "quarter"].max()
        known = known_at(cdf, origin)
        cutoff = cutoff_date(origin, cdf)
        targets = [origin + h for h in HORIZONS if origin + h in actual.index]
        base = {"company": c, "group": COMPANIES[c][0], "origin": str(origin),
                "last_known": str(known.index[-1]), "cutoff": str(cutoff.date())}
        for t in targets:
            fc = b4_latest_times_average_step(known, t)
            rows.append({**base, "rule": "B4", "h": (t - origin).n, "target": str(t),
                         "forecast": fc, "actual": actual[t], "signed_miss": signed_miss(actual[t], fc)})
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            ets = ets_at_origin(known, targets)
        for r in ets:
            t = r["target"]
            rows.append({**base, "rule": "ETS", "h": (t - origin).n, "target": str(t),
                         "forecast": r["ets"], "actual": actual[t], "signed_miss": signed_miss(actual[t], r["ets"])})
    d = pd.DataFrame(rows)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    d.to_csv(out_file, index=False)
    print(f"rows written: {len(d)}")


if __name__ == "__main__":
    main()
