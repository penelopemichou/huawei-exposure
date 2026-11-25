"""Tag fix (approved by Penelope, 25 Nov 2026): for conflict quarters in the last 12 quarters before
each firm's origin, find out whether the conflict is inside the EARLIEST filing of that quarter
(then the tag order decides the first-reported value) or only in a later filing (a restatement:
the first-reported value is unaffected). For same-filing conflicts, the total revenue is the
LARGER value in that filing (a part, such as goods only or a segment, is smaller); this is checked
in every filing before the origin where both tags appear.

Prints ONLY tag labels, quarter labels and counts: no value. Writes results/tag_fix.csv.

Run (bash):  ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/tag_fix.py
"""

import contextlib
import io
import re
import sys
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))
import build_quarterly as bq                      # noqa: E402  (copied Project 2 code)
from companies import COMPANIES, PROJECT2_COMPANIES   # noqa: E402

EVENT = pd.Timestamp("2019-05-16")
FIRMS = ["Advanced Micro Devices", "Analog Devices", "Xilinx", "Cree / Wolfspeed", "Cypress", "Plexus",
         "Amkor Technology", "SMTC", "Sunpower", "Benchmark Electronics"]
SHORT = {"RevenueFromContractWithCustomerExcludingAssessedTax": "EX", "Revenues": "R",
         "RevenueFromContractWithCustomerIncludingAssessedTax": "IN", "SalesRevenueNet": "SRN",
         "SalesRevenueGoodsNet": "SGN"}


def labelled_by_tag(raw):
    """prepare() run once on all tags, with each tag's filing ID made unique (accn|tag), so its
    one-tag-per-filing step keeps every tag; the fiscal calendar still comes from all tags."""
    r = raw.copy()
    r["accn"] = r["accn"] + "|" + r["tag"]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):         # prepare() can print values: never shown
        f = bq.prepare(r)
    f["accn"] = f["accn"].str.split("|").str[0]
    return f


def main():
    raw = bq.load_facts()
    raw = raw[raw.company.isin(FIRMS)]
    f = labelled_by_tag(raw)
    q = f[f.kind == "quarter"].copy()
    table = pd.read_csv(PROJECT / "data" / "processed" / "revenue_quarterly.csv", parse_dates=["period_end"])
    rows, decisions = [], {}
    for c in FIRMS:
        t = table[table.company == c].sort_values(["fiscal_year", "fiscal_quarter"])
        o = t[t.period_end < EVENT].iloc[-1]
        oi = o.fiscal_year * 4 + o.fiscal_quarter
        g = q[(q.company == c) & ((q.fiscal_year * 4 + q.fiscal_quarter) > oi - 12) & ((q.fiscal_year * 4 + q.fiscal_quarter) <= oi)]
        tags = list(COMPANIES[c][1][0][1:]) if False else None
        entity_tags = bq.TAGS[[n for _, n in COMPANIES[c][1]][-1]]
        same_filing, later, current_wrong = [], [], []
        larger_tags = []
        for (fy, fq), h in g.groupby(["fiscal_year", "fiscal_quarter"]):
            per_tag_first = h.sort_values(["filed", "accn"]).groupby("tag").first()
            if len(per_tag_first) < 2 or per_tag_first.val.max() / per_tag_first.val.min() - 1 <= 0.005:
                continue
            first_accn = h.sort_values(["filed", "accn"]).iloc[0].accn
            in_first = h[h.accn == first_accn].groupby("tag").val.first()
            lab = f"{fy} Q{fq}"
            if len(in_first) >= 2 and in_first.max() / in_first.min() - 1 > 0.005:
                same_filing.append(lab)
                big = in_first.idxmax()
                larger_tags.append(big)
                picked = min(in_first.index, key=lambda tg: entity_tags.index(tg))
                if picked != big:
                    current_wrong.append(lab)
            else:
                later.append(lab)
        chosen = max(set(larger_tags), key=larger_tags.count) if larger_tags else ""
        # consistency: in every filing before the origin where the chosen tag and another tag both appear,
        # is the chosen tag's value the larger (or equal) one?
        consistent = total = 0
        if chosen:
            pre = q[(q.company == c) & ((q.fiscal_year * 4 + q.fiscal_quarter) <= oi)]
            for (_, _, _), h in pre.groupby(["accn", "fiscal_year", "fiscal_quarter"]):
                v = h.groupby("tag").val.first()
                if chosen in v.index and len(v) >= 2:
                    total += 1
                    consistent += int(v[chosen] >= v.max() * 0.995)
        rows.append({"firm": c, "group": COMPANIES[c][0],
                     "conflicts_in_window": len(same_filing) + len(later),
                     "later_restatement_only": len(later), "same_filing": len(same_filing),
                     "same_filing_quarters": ", ".join(same_filing),
                     "current_order_picks_smaller": len(current_wrong),
                     "total_tag": SHORT.get(chosen, chosen),
                     "total_tag_largest_in_filings": f"{consistent} of {total}" if chosen else "",
                     "current_order": ", ".join(SHORT[x] for x in entity_tags),
                     "change_needed": "yes" if current_wrong else "no"})
        if current_wrong:
            decisions[c] = chosen
    d = pd.DataFrame(rows)
    d.to_csv(PROJECT / "results" / "tag_fix.csv", index=False)
    text = d.to_string(index=False)
    if re.search(r"\d{6,}", text):
        raise SystemExit("STOP: a 6+ digit number would be printed")
    pd.set_option("display.width", 250)
    print(text)
    print("\nchange needed for:", {k: SHORT[v] for k, v in decisions.items()} or "none")


if __name__ == "__main__":
    main()
