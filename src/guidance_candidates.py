"""Guidance-cut step (separate, after the main run): candidate 8-K filings, from the saved SEC filing
lists only (no internet). For each firm (primary exposed, Lumentum, low exposure):

  before: the last 8-K with item 2.02 (results) filed before 16 May 2019 (guidance for the quarter in
          progress, if the firm gives it)
  after:  every 8-K with item 2.02, 7.01 or 8.01 filed from 16 May 2019 to the end of the quarter in
          progress on 16 May 2019 (the firm's h = 1 quarter; its end date from the revenue table)

Proposed download: the SEC "complete submission" text file of each filing (one request; size from
the filing list). Writes results/guidance_candidates.csv and prints the list. Nothing is downloaded.

Run (bash):  ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/guidance_candidates.py
"""

import json
import sys
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))
from baselines import load                    # noqa: E402
from companies import COMPANIES               # noqa: E402

EVENT = pd.Timestamp("2019-05-16")
DIRS = [PROJECT / "data" / "raw" / "stage_a" / "submissions", PROJECT / "data" / "raw" / "filing_lists" / "submissions"]


def filings(cik):
    for d in DIRS:
        p = d / f"CIK{cik}.json"
        if p.exists():
            s = json.loads(p.read_text())
            fr = [pd.DataFrame(s["filings"]["recent"])] + [pd.DataFrame(json.loads((d / o["name"]).read_text()))
                                                            for o in s["filings"].get("files", []) if (d / o["name"]).exists()]
            f = pd.concat(fr, ignore_index=True)
            f["fd"] = pd.to_datetime(f.filingDate)
            return f
    raise SystemExit(f"no filing list on disk for {cik}")


def main():
    firms = [c for c, v in COMPANIES.items() if v[0] in ("Exposed (primary)", "Exposed (secondary)", "Low exposure")]
    q = load(companies=firms)
    rows = []
    for c in firms:
        g = q[q.company == c].sort_values("quarter")
        origin = g.loc[g.period_end < EVENT, "quarter"].max()
        nxt = g[g.quarter == origin + 1]
        q_end = nxt.period_end.iloc[0] if len(nxt) else pd.NaT       # end of the quarter in progress
        cik = COMPANIES[c][1][-1][0]
        f = filings(cik)
        k8 = f[f.form.isin(["8-K", "8-K/A"])].copy()
        k8["items"] = k8["items"].fillna("")
        before = k8[(k8.fd < EVENT) & k8["items"].str.contains("2.02")].sort_values("fd").tail(1)
        after = k8[(k8.fd >= EVENT) & (k8.fd <= q_end) & k8["items"].str.contains(r"2\.02|7\.01|8\.01", regex=True)]
        for role, part in [("before", before), ("after", after.sort_values("fd"))]:
            for _, r in part.iterrows():
                acc = r.accessionNumber
                rows.append({"firm": c, "group": COMPANIES[c][0], "quarter in progress": str(origin + 1),
                             "quarter ends": str(q_end.date()) if pd.notna(q_end) else "", "role": role,
                             "form": r.form, "filed": r.filingDate, "items": r["items"], "accession": acc,
                             "size_mb": round(r["size"] / 1e6, 2),
                             "url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{acc}.txt"})
        if after.empty:
            rows.append({"firm": c, "group": COMPANIES[c][0], "quarter in progress": str(origin + 1),
                         "quarter ends": str(q_end.date()) if pd.notna(q_end) else "", "role": "after",
                         "form": "(none)", "filed": "", "items": "", "accession": "", "size_mb": 0.0, "url": ""})
    d = pd.DataFrame(rows)
    d.to_csv(PROJECT / "results" / "guidance_candidates.csv", index=False)
    pd.set_option("display.width", 250, "display.max_rows", 200, "display.max_colwidth", 30)
    print(d.drop(columns=["url", "accession"]).to_string(index=False))
    real = d[d.form != "(none)"]
    print(f"\nfilings: {len(real)} ({(real.role == 'before').sum()} before, {(real.role == 'after').sum()} after) from {d.firm.nunique()} firms; "
          f"firms with no 8-K in the after-window: {(d.form == '(none)').sum()}")
    print(f"total size (complete submission files): {real.size_mb.sum():.1f} MB; largest {real.size_mb.max():.2f} MB")


if __name__ == "__main__":
    main()
