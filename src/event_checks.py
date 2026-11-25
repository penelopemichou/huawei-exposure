"""Step 3d: checks on the event rows before they are opened. Prints ONLY pass/fail, counts and file
fingerprints: no forecast, no actual, no miss.

  (a) a rerun of src/event_rows.py gives an identical file (SHA-256)
  (b) no firm's origin is shifted: the origin used is the firm's own origin (eligibility tables), and
      the last quarter known at the 65-day cutoff is that origin
  (c) sign convention: signed_miss() on made-up numbers; every row's miss recomputed (count of mismatches)
  (d) firms per group, rule and horizon with a miss, against the frozen lists / eligibility tables

Run (bash):  ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/event_checks.py RERUN_FILE
"""

import hashlib
import re
import sys
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))
from event_rows import signed_miss        # noqa: E402
from companies import COMPANIES           # noqa: E402

EVENT_FILE = PROJECT / "results" / "event_rows.csv"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    out = []
    rerun = Path(sys.argv[1])
    # (a)
    a, b = sha(EVENT_FILE), sha(rerun)
    out.append(f"(a) rerun identical: {'PASS' if a == b else 'FAIL'} (fingerprints {a[:16]} / {b[:16]})")

    e = pd.read_csv(EVENT_FILE)
    # (b) origin from the eligibility tables (exact Project 2 functions); sensitivity firms from the table itself
    elig = pd.concat([pd.read_csv(PROJECT / "results" / "eligibility_exact.csv"),
                      pd.read_csv(PROJECT / "results" / "eligibility_exact_amendment1.csv")])
    elig_origin = {}
    sec_names = {n.upper(): c for c, (_, ents, _) in COMPANIES.items() for _, n in ents}
    firm_to_company = {}
    for c, (_, ents, _) in COMPANIES.items():
        firm_to_company[c.upper()] = c
    for _, r in elig.iterrows():
        key = r.firm.upper()
        comp = sec_names.get(key) or firm_to_company.get(key) or firm_to_company.get(r.firm.replace("/", " / ").upper())
        if comp:
            elig_origin[comp] = r.origin.split(" ")[0]
    per_firm = e.groupby("company").agg(origin=("origin", "first"), last_known=("last_known", "first"))
    matched = [c for c in per_firm.index if c in elig_origin]
    shifted_vs_elig = sum(per_firm.loc[c, "origin"] != elig_origin[c] for c in matched)
    not_known = int((per_firm.origin != per_firm.last_known).sum())
    out.append(f"(b) origin not shifted: {'PASS' if shifted_vs_elig == 0 and not_known == 0 else 'FAIL'} "
               f"(firms: {len(per_firm)}; origin = eligibility-table origin for {len(matched) - shifted_vs_elig} of {len(matched)} "
               f"checked; last quarter known at the cutoff = origin for {len(per_firm) - not_known} of {len(per_firm)})")

    # (c) sign convention
    made_up = signed_miss(110, 100) > 0 and signed_miss(90, 100) < 0 and signed_miss(100, 100) == 0
    recomputed = signed_miss(e.actual, e.forecast)
    mism = int(((recomputed - e.signed_miss).abs() > 1e-9).sum())
    missing = int(e.signed_miss.isna().sum())
    out.append(f"(c) sign convention (positive = revenue above forecast): made-up test {'PASS' if made_up else 'FAIL'}; "
               f"rows recomputed: {len(e) - missing}, mismatches: {mism}; rows with no forecast (missing): {missing}")

    # (d) counts per group, rule, horizon (firms with a non-missing miss) vs expected
    got = (e[e.signed_miss.notna()].groupby(["group", "rule", "h"]).company.nunique()
           .unstack("h", fill_value=0))
    exp = {}
    for comp, (grp, _, _) in COMPANIES.items():
        if grp not in ("Exposed (primary)", "Exposed (secondary)", "Low exposure", "Donor (primary)", "Donor (sensitivity)"):
            continue
        hs = None
        er = elig[[(sec_names.get(f.upper()) or firm_to_company.get(f.upper()) or firm_to_company.get(f.replace("/", " / ").upper())) == comp
                   for f in elig.firm]]
        if len(er):
            hs = [h for h in (1, 2, 3, 4) if er.iloc[0][f"h{h}"] == "yes"]
        else:
            qc = pd.read_csv(PROJECT / "results" / "quarter_counts_all.csv")
            qr = qc[[firm_to_company.get(f.upper()) == comp or sec_names.get(f.upper()) == comp for f in qc.firm]]
            hs = list(range(1, int(qr.iloc[0].quarters_after_origin_h1_4) + 1)) if len(qr) else []
        for h in hs:
            exp[(grp, h)] = exp.get((grp, h), 0) + 1
    lines = ["(d) firms with a miss, per group, rule and horizon (got / expected):"]
    allok = True
    for grp in ["Exposed (primary)", "Exposed (secondary)", "Low exposure", "Donor (primary)", "Donor (sensitivity)"]:
        for rule in ["B4", "ETS"]:
            cells = []
            for h in (1, 2, 3, 4):
                g = int(got.loc[(grp, rule), h]) if (grp, rule) in got.index and h in got.columns else 0
                x = exp.get((grp, h), 0)
                allok &= g == x
                cells.append(f"h{h} {g}/{x}{'' if g == x else ' <-'}")
            lines.append(f"    {grp:20s} {rule:3s}  " + "  ".join(cells))
    pe = [int(got.loc[("Exposed (primary)", r), h]) for r in ("B4", "ETS") for h in (1, 2, 3, 4)]
    target_ok = pe == [5, 4, 4, 4, 5, 4, 4, 4]
    lines.append(f"    primary exposed 5 at h = 1 and 4 at h = 2-4, both rules: {'PASS' if target_ok else 'FAIL'}")
    out.append(f"(d) counts match: {'PASS' if allok else 'FAIL (see <-)'}")
    out += lines
    text = "\n".join(out)
    if re.search(r"(?<![0-9a-f])\d{6,}(?![0-9a-f])", text):
        raise SystemExit("STOP: a 6+ digit number would be printed")
    print(text)


if __name__ == "__main__":
    main()
