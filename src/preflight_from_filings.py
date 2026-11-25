"""Session 2: pre-flight eligibility from the SEC filing lists only (no internet, no revenue
data, no forecasts, no misses). For the exposed firms and the donors found so far.

For each firm: the origin (last 10-K/10-Q period ending before 16 May 2019), its filing date and
the 65-day check; the first 10-K/10-Q; the number of periodic reports up to the origin (an
ESTIMATE of the 20-quarter rule: the exact count needs the revenue file, Stage C); the predecessor
(from memory, to verify); the last periodic report; and which horizons h = 1-4 have a report.

Run from the project folder:
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/preflight_from_filings.py
"""

import json
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
SUB = PROJECT / "data" / "raw" / "stage_a" / "submissions"
EVENT = pd.Timestamp("2019-05-16")
FIRMS = {  # firm -> (CIK, group, predecessor: from memory, to verify)
    "NeoPhotonics": ("0001227025", "exposed", "none known"),
    "Inphi": ("0001160958", "exposed", "none known"),
    "Lumentum": ("0001633978", "exposed", "JDS Uniphase (now Viavi, CIK 0000912093): spun off Aug 2015 (from memory)"),
    "Qorvo": ("0001604778", "exposed", "RF Micro Devices and TriQuint: merged Jan 2015 (from memory)"),
    "Micron": ("0000723125", "exposed", "none known"),
    "Finisar": ("0001094739", "exposed", "none; acquired by II-VI in Sep 2019 (from memory)"),
    "Intel": ("0000050863", "donor", "none known"),
}


def table(cik):
    s = json.loads((SUB / f"CIK{cik}.json").read_text())
    fr = [pd.DataFrame(s["filings"]["recent"])] + [pd.DataFrame(json.loads((SUB / o["name"]).read_text()))
                                                    for o in s["filings"].get("files", []) if (SUB / o["name"]).exists()]
    f = pd.concat(fr, ignore_index=True)
    f = f[f.form.isin(["10-K", "10-Q"])].copy()
    f["rd"] = pd.to_datetime(f.reportDate, errors="coerce")
    f["fd"] = pd.to_datetime(f.filingDate)
    return f.sort_values("fd").drop_duplicates("rd", keep="first").sort_values("rd")   # first filing per period


def main():
    out = []
    for firm, (cik, group, pred) in FIRMS.items():
        f = table(cik)
        o = f[f.rd < EVENT].iloc[-1]
        cutoff = o.rd + pd.Timedelta(days=65)
        after = f[f.rd > o.rd].head(4)
        steps = [round((r - o.rd).days / 91) for r in after.rd]            # 1, 2, 3, 4 if every quarter is there
        hz = {h: ("yes" if h in steps else "no") for h in [1, 2, 3, 4]}
        last = f.iloc[-1]
        n_up_to = int((f.rd <= o.rd).sum())
        out.append({"firm": firm, "group": group,
                    "origin": f"{o.form} {o.rd.date()}", "origin_filed": str(o.fd.date()),
                    "days_after_end": (o.fd - o.rd).days, "known_at_cutoff": "yes" if o.fd <= cutoff else "NO",
                    "first_10k10q": str(f.fd.min().date()), "reports_up_to_origin": n_up_to,
                    "20q_estimate": "likely pass" if n_up_to >= 24 else ("borderline" if n_up_to >= 18 else "likely FAIL"),
                    "predecessor": pred,
                    "last_report": f"{last.form} {last.rd.date()} (filed {last.fd.date()})",
                    "h1": hz[1], "h2": hz[2], "h3": hz[3], "h4": hz[4]})
    d = pd.DataFrame(out)
    d.to_csv(PROJECT / "results" / "preflight_from_filings.csv", index=False)
    pd.set_option("display.width", 250, "display.max_colwidth", 70)
    print(d.drop(columns=["predecessor"]).to_string(index=False))
    print("\npredecessors (from memory, to verify):")
    for _, r in d.iterrows():
        print(f"  {r.firm}: {r.predecessor}")


if __name__ == "__main__":
    main()
