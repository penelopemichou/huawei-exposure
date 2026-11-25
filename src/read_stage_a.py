"""Session 2, Stage A: read the saved screening files (no internet).

Run from the project folder:
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/read_stage_a.py submissions
"""

import json
import sys
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "data" / "raw" / "stage_a"
EVENT = pd.Timestamp("2019-05-16")


def filings_table(sub):
    """All filings in a submissions file (recent block + any older files already saved)."""
    frames = [pd.DataFrame(sub["filings"]["recent"])]
    for f in sub["filings"].get("files", []):
        p = OUT / "submissions" / f["name"]
        if p.exists():
            frames.append(pd.DataFrame(json.loads(p.read_text())))
    df = pd.concat(frames, ignore_index=True)
    for c in ["filingDate", "reportDate"]:
        df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


def submissions():
    rows, tenks, missing = [], [], []
    for p in sorted((OUT / "submissions").glob("CIK??????????.json")):
        sub = json.loads(p.read_text())
        f = filings_table(sub)
        periodic = f[f["form"].isin(["10-K", "10-Q"])]
        before = periodic[periodic["reportDate"] < EVENT].sort_values("reportDate")
        origin = before.iloc[-1] if len(before) else None
        older = sub["filings"].get("files", [])
        older_missing = [o for o in older if not (OUT / "submissions" / o["name"]).exists()]
        missing += [(sub["name"], o["name"], o["filingFrom"], o["filingTo"], o["filingCount"]) for o in older_missing]
        rows.append({
            "cik": p.stem[3:], "name": sub["name"],
            "former": "; ".join(n["name"] for n in sub.get("formerNames", [])),
            "sic": sub.get("sic"), "sic_desc": sub.get("sicDescription"),
            "fy_end": sub.get("fiscalYearEnd"),
            "first_10K_10Q_seen": periodic["filingDate"].min().date() if len(periodic) else None,
            "older_files_missing": len(older_missing),
            "origin_form": origin["form"] if origin is not None else None,
            "origin_period_end": origin["reportDate"].date() if origin is not None else None,
            "origin_filed": origin["filingDate"].date() if origin is not None else None,
        })
        k = f[(f["form"] == "10-K") & (f["reportDate"] >= "2017-12-01") & (f["reportDate"] <= "2020-12-31")]
        for _, r in k.iterrows():
            tenks.append({"name": sub["name"], "period_end": r["reportDate"].date(),
                          "filed": r["filingDate"].date(), "accession": r["accessionNumber"],
                          "document": r["primaryDocument"], "size_mb": round(r["size"] / 1e6, 1)})
    pd.set_option("display.width", 250, "display.max_columns", 20, "display.max_colwidth", 60)
    print(pd.DataFrame(rows).to_string(index=False))
    print("\nOlder-filing files not downloaded (name, file, from, to, count):")
    for m in missing:
        print("  ", *m)
    print("\n10-Ks for fiscal years ending Dec 2017 - Dec 2020:")
    print(pd.DataFrame(tenks).to_string(index=False))


if __name__ == "__main__":
    {"submissions": submissions}[sys.argv[1]]()
