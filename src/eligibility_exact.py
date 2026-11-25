"""Exact eligibility table with Project 2's own functions (imported read-only from forecast-gap).

Rows are built exactly as forecast-gap's build_quarterly.load_facts() builds them, but from this
project's revenue files; then Project 2's prepare(), build_table(), and baselines.first_origin(),
cutoff_date(), known_at() and ets.training_series() are called unchanged.
Prints ONLY counts, quarter labels and dates: no revenue value, no forecast, no miss.

Tag order (provisional; Project 2 chose tags per company by hand, to be confirmed before forecasting):
RevenueFromContractWithCustomerExcludingAssessedTax, Revenues, ...IncludingAssessedTax, SalesRevenueNet, SalesRevenueGoodsNet.

Run from the project folder (-B: no cache files are written into forecast-gap):
    ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/eligibility_exact.py          (frozen-list firms)
    ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/eligibility_exact.py amend    (amendment-1 candidates)
"""

import csv
import json
import sys
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
FG_SRC = Path.home() / "Documents" / "forecast-gap" / "src"
sys.path.insert(0, str(FG_SRC))
import build_quarterly as bq            # noqa: E402  (Project 2 code, read-only)
import baselines as bl                  # noqa: E402
from ets import training_series, MIN_QUARTERS   # noqa: E402

CF = PROJECT / "data" / "raw" / "filing_lists" / "companyfacts"
EX, R, IN = ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
             "RevenueFromContractWithCustomerIncludingAssessedTax")
TAGS = [EX, R, IN, "SalesRevenueNet", "SalesRevenueGoodsNet"]
EVENT = pd.Timestamp("2019-05-16")
STITCH = {"Broadcom Inc.": ["0001441634", "0001649338", "0001730168"]}     # results/stitching.csv


def raw_rows(company, cik):
    """The same rows as forecast-gap's load_facts(), for one entity."""
    facts = json.loads((CF / f"CIK{cik}.json").read_text())["facts"]["us-gaap"]
    rows = []
    for priority, tag in enumerate(TAGS):
        for v in facts.get(tag, {}).get("units", {}).get("USD", []):
            if "start" not in v:
                continue
            rows.append({"company": company, "entity": cik, "tag": tag, "priority": priority, "start": v["start"],
                         "end": v["end"], "val": v["val"], "accn": v["accn"], "form": v["form"], "filed": v["filed"]})
    return rows


def table_for(company, ciks):
    df = pd.DataFrame([r for cik in ciks for r in raw_rows(company, cik)])
    for col in ["start", "end", "filed"]:
        df[col] = pd.to_datetime(df[col])
    import contextlib, io
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):          # prepare() prints dropped values WITH revenue figures: never shown
        prepared = bq.prepare(df)
    dropped = sum(int(w) for w in __import__("re").findall(r"Dropped (\d+) full-year", buf.getvalue()))
    if dropped:
        print(f"  {company}: Project 2's prepare() dropped {dropped} full-year value(s) (>25 % from the first 10-K figure); values not shown")
    t = bq.build_table(prepared, company)
    t["period_end"] = pd.to_datetime(t["period_end"])
    t["first_filed_date"] = pd.to_datetime(t["first_filed_date"])
    t["quarter"] = pd.PeriodIndex.from_fields(year=t["fiscal_year"], quarter=t["fiscal_quarter"], freq="Q")
    t["value"] = t["revenue_first_reported"]              # used by known_at only; never printed
    return t.sort_values("quarter").reset_index(drop=True)


def main():
    amend = sys.argv[1:] == ["amend"]
    if amend:   # amendment-1 candidates (proposed low exposure), results/amendment1_candidates.csv
        firms = [{"firm": r["firm"], "cik": r["cik"], "group": "proposed low exposure (amendment 1)", "comparison": ""}
                 for r in csv.DictReader((PROJECT / "results" / "amendment1_candidates.csv").open())]
    else:
        firms = [r for r in csv.DictReader((PROJECT / "results" / "firm_classes.csv").open())
                 if r["group"] in ("exposed", "low exposure, implied") or r["comparison"] == "PRIMARY"]
    out = []
    for r in firms:
        t = table_for(r["firm"], STITCH.get(r["firm"], [r["cik"]]))
        before = t[t.period_end < EVENT]
        o = before.iloc[-1]
        origin = o.quarter
        fo = bl.first_origin(t)
        cutoff = bl.cutoff_date(origin, t)
        known = bl.known_at(t, origin)
        try:
            ets_n = len(training_series(known))
        except ValueError:
            ets_n = 0
        idx = set(t.quarter)
        comp = ("SECONDARY (design-v2 (d))" if r["firm"].startswith("Lumentum") else
                "PRIMARY" if r["group"] == "exposed" or r["comparison"] == "PRIMARY" else "own rows")
        out.append({"group": r["group"], "comparison": comp, "firm": r["firm"],
                    "first_quarter": f"{t.quarter.min()} ({t.period_end.min().date()})",
                    "quarters_to_origin": int((t.quarter <= origin).sum()),
                    "origin": f"{origin} ({o.period_end.date()})", "first_origin": str(fo),
                    "20q_rule": "pass" if origin >= fo else "FAIL",
                    "origin_filed": str(o.first_filed_date.date()), "cutoff": str(cutoff.date()),
                    "origin_known_at_cutoff": "yes" if origin in known.index else "NO",
                    "ets_unbroken_known": ets_n, "ets_ok": "yes" if ets_n >= MIN_QUARTERS else "NO",
                    **{f"h{h}": ("yes" if origin + h in idx else "no") for h in (1, 2, 3, 4)}})
    d = pd.DataFrame(out)
    d.to_csv(PROJECT / "results" / ("eligibility_exact_amendment1.csv" if amend else "eligibility_exact.csv"), index=False)
    pd.set_option("display.width", 260, "display.max_rows", 100, "display.max_colwidth", 40)
    print(d.drop(columns=["group"]).to_string(index=False))
    bad = d[(d["20q_rule"] != "pass") | (d.origin_known_at_cutoff != "yes") | (d.ets_ok != "yes") | (d.h1 != "yes")]
    print("\nfirms failing a check:", "none" if bad.empty else bad[["firm", "20q_rule", "origin_known_at_cutoff", "ets_ok", "h1"]].to_string(index=False))


if __name__ == "__main__":
    main()
