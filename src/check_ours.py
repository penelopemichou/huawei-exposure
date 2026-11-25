"""Project 2's data checks (src/check_data.py, functions unchanged) for this project's 64 firms,
on quarters UP TO EACH FIRM'S ORIGIN only (the last fiscal quarter ending before 16 May 2019),
so that nothing about revenue after the event is seen. Plus a revenue-tag review.

Prints ONLY counts and quarter labels: no revenue value, no percentage change, no forecast, no miss.
A final guard stops if any printed line holds a number with 6 or more digits.

Run from the project folder (bash):
    ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/check_ours.py
"""

import contextlib
import io
import re
import sys
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))
import check_data as cd                                   # noqa: E402  (copied Project 2 code, unchanged)
from baselines import DAYS_AFTER_QUARTER_END, load        # noqa: E402
from build_quarterly import load_facts, prepare           # noqa: E402
from companies import COMPANIES, PROJECT2_COMPANIES       # noqa: E402

EVENT = pd.Timestamp("2019-05-16")
SHORT = {"RevenueFromContractWithCustomerExcludingAssessedTax": "EX", "Revenues": "R",
         "RevenueFromContractWithCustomerIncludingAssessedTax": "IN", "SalesRevenueNet": "SRN",
         "SalesRevenueGoodsNet": "SGN"}


def main():
    ours = [c for c in COMPANIES if c not in PROJECT2_COMPANIES]
    q = load(companies=ours)
    origin = {c: g.loc[g.period_end < EVENT, "quarter"].max() for c, g in q.groupby("company")}
    origin_end = {c: g.loc[g.quarter == origin[c], "period_end"].iloc[0] for c, g in q.groupby("company")}
    pre = q[[r.quarter <= origin[r.company] for r in q.itertuples()]].copy()

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):                 # prepare() can print values: never shown
        facts = prepare(load_facts())
    facts = facts[facts.company.isin(ours)]
    facts = facts[[e <= origin_end[c] + pd.Timedelta(days=10) for c, e in zip(facts.company, facts.end)]]

    cov = cd.coverage(pre)
    summary, fails = cd.sums_to_year(pre, facts)
    rev = cd.revisions(pre)
    lag = cd.lags(pre)
    jmp = cd.jumps(pre)
    tag = cd.tag_conflicts(facts)

    rows = []
    for c in ours:
        g = pre[pre.company == c]
        tags = g.source_tag.map(SHORT).fillna("other").value_counts()
        switches = int((g.sort_values("quarter").source_tag != g.sort_values("quarter").source_tag.shift()).sum() - 1)
        jq = jmp[jmp.company == c]["quarter"].tolist() if len(jmp) else []
        tq = tag[tag.company == c]["quarter"].tolist() if len(tag) else []
        rows.append({
            "firm": c, "group": COMPANIES[c][0], "origin": cd._label(origin[c]),
            "q_to_origin": int(cov.loc[c, "quarters"]),
            "gaps": 0 if cov.loc[c, "gaps"] == "none" else len(cov.loc[c, "gaps"].split(", ")),
            "Q4_derived": int(cov.loc[c, "Q4 derived"]),
            "yr_tests": int(summary.loc[c, "years"]) if c in summary.index and pd.notna(summary.loc[c, "years"]) else 0,
            "yr_fail": int(summary.loc[c, "failures"]) if c in summary.index and pd.notna(summary.loc[c, "failures"]) else 0,
            "revised": int(rev.loc[c, "revised"]), "revised>0.5%": int(rev.loc[c, "over_half_pct"]),
            f"late>{DAYS_AFTER_QUARTER_END}d": int(lag.loc[c, f"over {DAYS_AFTER_QUARTER_END} days (since 2010)"]) if c in lag.index else 0,
            "jumps": len(jq), "jump_quarters": ", ".join(jq),
            "tag_conflicts": len(tq), "conflict_quarters": ", ".join(tq[:6]) + (" …" if len(tq) > 6 else ""),
            "tags_used": ", ".join(f"{k}:{v}" for k, v in tags.items()), "tag_switches": max(switches, 0)})
    d = pd.DataFrame(rows)
    d.to_csv(PROJECT / "results" / "check_ours.csv", index=False)

    lines = []
    pd.set_option("display.width", 300, "display.max_rows", 100, "display.max_colwidth", 48)
    lines += d.drop(columns=["conflict_quarters"]).to_string(index=False).splitlines()
    lines.append("")
    lines.append(f"firms checked: {len(d)} | quarters checked (up to each origin): {len(pre)}")
    for col in ["gaps", "yr_fail", "revised>0.5%", f"late>{DAYS_AFTER_QUARTER_END}d", "jumps", "tag_conflicts", "tag_switches"]:
        lines.append(f"  firms with {col} > 0: {int((d[col] > 0).sum())}")
    for line in lines:                                    # guard: no revenue-size number may be printed
        if re.search(r"\d{6,}", line):
            raise SystemExit("STOP: a printed line held a 6+ digit number; nothing more is printed.")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
