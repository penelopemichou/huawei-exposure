"""Step 3b: each firm's "own usual miss" (design-v2 (g)), from PRE-EVENT rolling forecasts only.

For every firm in the frozen lists (64): rolling origins from the firm's first_origin (20-quarter rule)
up to the quarter before its origin, h = 1-4, B4 and AutoETS, with the copied Project 2 code
(known_at = 65-day rule; smoothing.b4_latest_times_average_step; ets.ets_at_origin).
**Only forecasts whose target quarter is on or before the firm's origin quarter are kept**
(Penelope's rule, 26 Nov 2026): the origin = the last fiscal quarter ending before 16 May 2019.

Signed miss = 100 x (actual - forecast) / actual (positive = revenue above the forecast), actual =
first-reported revenue. Scale = median |signed miss| per firm x rule x horizon, for B4, ETS and AVG
(the average of the two rules' signed misses on the same origin and target).

Saves results/usual_miss_rows.csv and results/usual_miss_scales.csv (NOT printed).
Prints ONLY counts per firm and the number of targets after the origin (must be 0).

Run (bash):  ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/usual_miss.py
"""

import contextlib
import io
import re
import sys
import warnings
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))
from baselines import HORIZONS, first_origin, known_at, load      # noqa: E402  (copied Project 2 code)
from companies import COMPANIES, PROJECT2_COMPANIES                 # noqa: E402
from ets import ets_at_origin                                       # noqa: E402
from smoothing import b4_latest_times_average_step                  # noqa: E402

EVENT = pd.Timestamp("2019-05-16")


def main():
    warnings.filterwarnings("ignore")
    ours = [c for c in COMPANIES if c not in PROJECT2_COMPANIES]
    df = load(companies=ours)
    rows, counts = [], []
    sink = io.StringIO()
    for c in ours:
        cdf = df[df.company == c]
        actual = cdf.set_index("quarter")["value"]
        origin = cdf.loc[cdf.period_end < EVENT, "quarter"].max()
        fo = first_origin(cdf)
        o = fo
        ets_skipped = 0
        while o < origin:
            known = known_at(cdf, o)
            targets = [o + h for h in HORIZONS if o + h <= origin and o + h in actual.index]
            for t in targets:
                rows.append({"company": c, "rule": "B4", "fc_origin": str(o), "h": (t - o).n, "target": str(t),
                             "target_le_origin": t <= origin,
                             "signed": 100 * (actual[t] - b4_latest_times_average_step(known, t)) / actual[t]})
            try:
                with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
                    ets = ets_at_origin(known, targets)
                for r in ets:
                    t = r["target"]
                    rows.append({"company": c, "rule": "ETS", "fc_origin": str(o), "h": (t - o).n, "target": str(t),
                                 "target_le_origin": t <= origin,
                                 "signed": 100 * (actual[t] - r["ets"]) / actual[t]})
            except ValueError:
                ets_skipped += 1
            o += 1
        counts.append({"firm": c, "group": COMPANIES[c][0], "origin": str(origin), "first_origin": str(fo),
                       "rolling_origins": max((origin - fo).n, 0), "ets_origins_skipped": ets_skipped})
    r = pd.DataFrame(rows)
    r = r[r.signed.notna()]
    piv = r.pivot_table(index=["company", "fc_origin", "h", "target"], columns="rule", values="signed").dropna()
    avg = piv.mean(axis=1).rename("signed").reset_index().assign(rule="AVG", target_le_origin=True)
    allr = pd.concat([r, avg], ignore_index=True)
    allr.to_csv(PROJECT / "results" / "usual_miss_rows.csv", index=False)
    scales = (allr.assign(abs_miss=allr.signed.abs()).groupby(["company", "rule", "h"])
              .agg(n_forecasts=("abs_miss", "size"), usual_miss=("abs_miss", "median")).reset_index())
    scales.to_csv(PROJECT / "results" / "usual_miss_scales.csv", index=False)

    c = pd.DataFrame(counts).set_index("firm")
    n = allr.groupby(["company", "rule"]).size().unstack(fill_value=0)
    nh = allr[allr.rule == "AVG"].groupby(["company", "h"]).size().unstack(fill_value=0)
    out = c.join(n).join(nh.add_prefix("AVG_h"))
    after = int((~allr.target_le_origin.astype(bool)).sum())
    max_gap = max(0, max((pd.Period(t, "Q") - pd.Period(o, "Q")).n
                         for t, o in zip(allr.target, allr.company.map(c.origin))))
    pd.set_option("display.width", 250, "display.max_rows", 100)
    text = out.reset_index().to_string(index=False)
    text += (f"\n\nfirms: {len(out)} | forecasts kept: B4 {int(n['B4'].sum())}, ETS {int(n['ETS'].sum())}, "
             f"AVG {int(n['AVG'].sum())}\ntargets after the firm's origin: {after} | "
             f"latest target relative to the origin: {max_gap:+d} quarters (0 = the origin quarter itself)")
    if re.search(r"\d{6,}", text):
        raise SystemExit("STOP: a 6+ digit number would be printed")
    print(text)


if __name__ == "__main__":
    main()
