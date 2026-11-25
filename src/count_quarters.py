"""Session 2: count the revenue quarters per firm from the XBRL companyfacts files.

Prints ONLY counts and dates (no revenue value, no forecast, no miss).
Simplified version of Project 2's table builder (the exact table comes from the copied
Project 2 code later): 3-month revenue values from 10-K/10-Q filings under Project 2's
revenue tags, plus a derived Q4 where a full-year value and the other three quarters exist.

Run from the project folder:
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/count_quarters.py
"""

import json
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
CF = PROJECT / "data" / "raw" / "filing_lists" / "companyfacts"
TAGS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
        "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet", "SalesRevenueGoodsNet"]
FIRMS = {"NeoPhotonics": ("0001227025", "2019-03-31"), "Inphi": ("0001160958", "2019-03-31"),
         "Lumentum": ("0001633978", "2019-03-30"), "Qorvo": ("0001604778", "2019-03-30"),
         "Micron": ("0000723125", "2019-02-28"), "Finisar": ("0001094739", "2019-04-28"),
         "Intel": ("0000050863", "2019-03-30")}


def facts(cik):
    d = json.loads((CF / f"CIK{cik}.json").read_text())["facts"].get("us-gaap", {})
    rows = []
    for t in TAGS:
        for f in d.get(t, {}).get("units", {}).get("USD", []):
            if f.get("form") in ("10-K", "10-Q", "10-K/A", "10-Q/A") and "start" in f:
                rows.append({"tag": t, "start": f["start"], "end": f["end"], "filed": f["filed"]})
    df = pd.DataFrame(rows)
    df["start"], df["end"], df["filed"] = (pd.to_datetime(df[c]) for c in ["start", "end", "filed"])
    df["days"] = (df.end - df.start).dt.days
    return df


def quarter_ends(df):
    """Distinct quarter end dates: 3-month values, plus Q4 derived from a year minus three quarters."""
    q = df[df.days.between(80, 100)].drop_duplicates(["start", "end"])
    ends = sorted(set(q.end))
    for _, y in df[df.days.between(350, 380)].drop_duplicates(["start", "end"]).iterrows():
        inside = q[(q.start >= y.start - pd.Timedelta(days=5)) & (q.end <= y.end + pd.Timedelta(days=5))]
        if len(set(inside.end)) == 3 and not any(abs((e - y.end).days) <= 10 for e in ends):
            ends.append(y.end)
    ends = sorted(ends)
    out = []
    for e in ends:                          # merge ends within 10 days (52/53-week calendars)
        if not out or (e - out[-1]).days > 10:
            out.append(e)
    return out, q


def main():
    rows = []
    for firm, (cik, origin) in FIRMS.items():
        df = facts(cik)
        ends, q = quarter_ends(df)
        o = pd.Timestamp(origin)
        upto = [e for e in ends if e <= o + pd.Timedelta(days=10)]
        span = round((o - upto[0]).days / 91.3) + 1
        rows.append({"firm": firm, "first_quarter_end": str(upto[0].date()), "quarters_present_to_origin": len(upto),
                     "quarters_span_to_origin": span, "gaps": span - len(upto),
                     "20q_rule": "pass" if span >= 20 else "FAIL", "last_quarter_end": str(ends[-1].date()),
                     "quarters_after_origin_h1_4": sum(1 for e in ends if o + pd.Timedelta(days=10) < e <= o + pd.Timedelta(days=380)),
                     "tags_used": ", ".join(sorted(set(df.tag)))})
    d = pd.DataFrame(rows)
    pd.set_option("display.width", 250, "display.max_colwidth", 90)
    print(d.drop(columns=["tags_used"]).to_string(index=False))
    print("\n(20-quarter rule as in Project 2's first_origin: span from the first quarter to the origin, inclusive.)")
    d.to_csv(PROJECT / "results" / "quarter_counts.csv", index=False)


if __name__ == "__main__":
    main()
