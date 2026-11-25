"""Session 4, Step 2: data checks for every company (the Session 0 checks, plus two new ones).

  coverage()      quarters, first/last, gaps, Q4 reported or derived, 14-week quarters, first origin
  sums_to_year()  do the four quarters add up to the reported fiscal year (within 0.5 %)?
  revisions()     how often first-reported and latest revenue differ, and by how much
  lags()          days from the end of the quarter until its revenue was first filed
  jumps()         quarter-to-quarter changes more than 30 % away from the company's usual
                  seasonal change (likely an acquisition, a sale or a data problem): flagged, not dropped
  tag_conflicts() quarters where two revenue tags were first reported with different values

Run from the project folder:
    .venv/bin/python src/check_data.py
"""

import pandas as pd

from baselines import DAYS_AFTER_QUARTER_END, HISTORY_QUARTERS, load
from build_quarterly import load_facts, prepare
from companies import COMPANIES, company_type

JUMP_LIMIT = 0.30


def _label(p):
    return f"{p.year} Q{p.quarter}"


def coverage(q):
    rows = []
    for c, g in q.groupby("company", sort=False):
        have = set(g["quarter"])
        span = pd.period_range(g["quarter"].min(), g["quarter"].max(), freq="Q")
        missing = [p for p in span if p not in have]
        q4 = g[g["fiscal_quarter"] == 4]
        rows.append({"company": c, "type": company_type(c), "quarters": len(g),
                     "first": _label(g["quarter"].min()), "last": _label(g["quarter"].max()),
                     "gaps": ", ".join(_label(p) for p in missing) or "none",
                     "Q4 reported": int((~q4["q4_derived"]).sum()), "Q4 derived": int(q4["q4_derived"].sum()),
                     "14-week quarters": int((g["period_days"] >= 96).sum()),
                     "first origin": _label(g["quarter"].min() + HISTORY_QUARTERS - 1)})
    return pd.DataFrame(rows).set_index("company")


def sums_to_year(q, facts):
    years = facts[facts["kind"] == "year"].sort_values(["filed", "accn"])
    full = years.groupby(["company", "fiscal_year"])["val"].last().rename("year_latest")
    direct = (facts[(facts["kind"] == "quarter") & (facts["fiscal_quarter"] == 4)]
              .groupby(["company", "fiscal_year"]).size().rename("q4_direct") > 0)
    complete = q.groupby(["company", "fiscal_year"]).filter(lambda g: len(g) == 4)
    s = (complete.groupby(["company", "fiscal_year"])["revenue_latest"].sum().rename("quarters")
         .to_frame().join(full).join(direct))
    s["q4_direct"] = s["q4_direct"].eq(True)
    s["diff_%"] = 100 * (s["quarters"] / s["year_latest"] - 1)
    s["fail"] = s["diff_%"].abs() > 0.5
    summary = s.groupby("company").agg(
        years=("fail", "size"), real_tests=("q4_direct", "sum"),
        failures=("fail", "sum"), largest_diff_pct=("diff_%", lambda x: x.abs().max()))
    return summary.reindex(list(COMPANIES)), s[s["fail"]].reset_index()


def revisions(q):
    r = 100 * (q["revenue_latest"] / q["revenue_first_reported"] - 1)
    out = q.assign(rev=r).groupby("company", sort=False).agg(
        revised=("rev", lambda x: int((x != 0).sum())),
        over_half_pct=("rev", lambda x: int((x.abs() > 0.5).sum())),
        largest_abs_pct=("rev", lambda x: x.abs().max()))
    return out


def lags(q):
    d = (q["first_filed_date"] - q["period_end"]).dt.days
    x = q.assign(days=d)
    recent = x[x["period_end"] >= "2010-01-01"]
    out = recent.groupby("company", sort=False)["days"].agg(["median", "max"])
    out[f"over {DAYS_AFTER_QUARTER_END} days (since 2010)"] = recent.groupby(
        "company", sort=False)["days"].apply(lambda s: int((s > DAYS_AFTER_QUARTER_END).sum()))
    return out


def jumps(q, series="revenue_first_reported"):
    """Quarter-to-quarter change vs the company's usual change for that quarter.

    usual = median over all years of (this quarter / previous quarter) for the
    same fiscal quarter. A change more than 30 % above or below the usual one
    is flagged. (A descriptive check on the whole history, not used for forecasting.)
    """
    rows = []
    for c, g in q.groupby("company", sort=False):
        s = g.set_index("quarter")[series].sort_index()
        prev = s.shift(1)
        consecutive = [(a - b).n == 1 for a, b in zip(s.index[1:], s.index[:-1])]
        ratio = (s / prev)[1:][[bool(x) for x in consecutive]]
        usual = ratio.groupby(ratio.index.quarter).median()
        adj = ratio / usual.reindex(ratio.index.quarter).to_numpy()
        for p, a in adj.items():
            if abs(a - 1) > JUMP_LIMIT:
                rows.append({"company": c, "type": company_type(c), "quarter": _label(p),
                             "period_end": g.loc[g["quarter"] == p, "period_end"].iloc[0].date(),
                             "change vs usual, %": 100 * (a - 1),
                             "revenue $bn": s[p] / 1e9, "previous $bn": s[p - 1] / 1e9})
    return pd.DataFrame(rows)


def tag_conflicts(facts):
    """Quarters reported under two different tags whose first values differ by more than 0.5 %."""
    f = facts[facts["kind"] == "quarter"].sort_values(["filed", "accn"])
    first = f.groupby(["company", "fiscal_year", "fiscal_quarter", "tag"]).agg(
        val=("val", "first"), filed=("filed", "first")).reset_index()
    rows = []
    for (c, fy, fq), g in first.groupby(["company", "fiscal_year", "fiscal_quarter"]):
        if len(g) < 2:
            continue
        spread = g["val"].max() / g["val"].min() - 1
        if spread > 0.005:
            rows.append({"company": c, "quarter": f"{fy} Q{fq}", "spread_%": 100 * spread,
                         "values": "; ".join(f"{t}={v / 1e9:.3f}bn ({d.date()})"
                                             for t, v, d in zip(g["tag"], g["val"], g["filed"]))})
    return pd.DataFrame(rows)


def main():
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 30)
    pd.set_option("display.max_colwidth", 140)
    pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
    q = load(companies=list(COMPANIES))
    facts = prepare(load_facts())

    print("1. COVERAGE"); print(coverage(q).to_string(), "\n")
    summary, fails = sums_to_year(q, facts)
    print("2. QUARTERS ADD UP TO THE FISCAL YEAR (latest values; real test = years with a reported Q4)")
    print(summary.to_string())
    print("Failures:"); print(fails.to_string(index=False) if len(fails) else "none", "\n")
    print("3. FIRST REPORTED vs LATEST"); print(revisions(q).to_string(), "\n")
    print("4. DAYS UNTIL PUBLIC (quarters ending 2010 or later)"); print(lags(q).to_string(), "\n")
    print(f"5. JUMPS: quarter-to-quarter change more than {JUMP_LIMIT:.0%} away from the usual seasonal change")
    j = jumps(q)
    print(j.to_string(index=False) if len(j) else "none", "\n")
    print("6. TAG CONFLICTS: same quarter, different tags, first values differ > 0.5 %")
    t = tag_conflicts(facts)
    print(t.to_string(index=False) if len(t) else "none")


if __name__ == "__main__":
    main()
