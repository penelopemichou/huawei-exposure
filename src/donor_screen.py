"""Session 2: donor filter criteria 1-4 for every firm with >= $100M of 2018 revenue,
and the state of criterion 5 (label test), from saved files only (no internet).

Inputs: data/raw/stage_a/sic_universe_revenue.csv, the submissions files in
data/raw/stage_a/submissions and data/raw/filing_lists/submissions, and
data/raw/stage_a/fts/huawei_hits.csv. Output: results/donor_screen.csv.

Criterion 3 here is a first screen: a 10-K/10-Q filed in 2014 or earlier is "pass";
older filing files that were not downloaded give "pass?" (to confirm from the revenue
file in Stage C); otherwise "fail".

Run from the project folder:
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/donor_screen.py
"""

import json
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
RAW = PROJECT / "data" / "raw"
EVENT = pd.Timestamp("2019-05-16")
CODES = {"3674", "3672", "3677", "3678", "3679"}
EXTRA = {"0000895419": 538.2}          # Cree: no frame label; FY2019 revenue $538.2M read from its own file


def filings(cik):
    for d in [RAW / "stage_a" / "submissions", RAW / "filing_lists" / "submissions"]:
        p = d / f"CIK{cik}.json"
        if p.exists():
            s = json.loads(p.read_text())
            fr = [pd.DataFrame(s["filings"]["recent"])]
            missing_older = 0
            for o in s["filings"].get("files", []):
                q = d / o["name"]
                if q.exists():
                    fr.append(pd.DataFrame(json.loads(q.read_text())))
                else:
                    missing_older += 1
            f = pd.concat(fr, ignore_index=True)
            f["fd"] = pd.to_datetime(f.filingDate)
            f["rd"] = pd.to_datetime(f.reportDate, errors="coerce")
            return s, f, missing_older
    return None, None, None


def main():
    u = pd.read_csv(RAW / "stage_a" / "sic_universe_revenue.csv", dtype={"cik": str, "sic": str})
    u["cik"] = u.cik.str.zfill(10)
    for cik, rev in EXTRA.items():
        u.loc[u.cik == cik, "rev2018_musd"] = rev
    c = u[u.rev2018_musd >= 100].copy()
    if not (c.cik == "0000895419").any():
        c = pd.concat([c, pd.DataFrame([{"cik": "0000895419", "name": "CREE, INC.", "sic": "3674", "rev2018_musd": 538.2}])])
    hits = pd.read_csv(RAW / "stage_a" / "fts" / "huawei_hits.csv", dtype=str)
    hits["fy"] = hits.period.str[:4]
    out = []
    for _, r in c.iterrows():
        s, f, missing_older = filings(r.cik)
        per = f[f.form.isin(["10-K", "10-Q"])]
        sic = s.get("sic") or r.sic
        k1819 = f[(f.form == "10-K") & f.rd.dt.year.isin([2018, 2019])]
        early = per.fd.min()
        c3 = "pass" if early <= pd.Timestamp("2014-12-31") else ("pass?" if missing_older else "fail")
        before = per[per.rd < EVENT].sort_values("rd")
        if len(before):
            o = before.iloc[-1]
            cutoff = o.rd + pd.Timedelta(days=65)
            c4 = "pass" if o.fd <= cutoff else "fail"
            origin = (o.form, str(o.rd.date()), str(o.fd.date()), (o.fd - o.rd).days)
        else:
            c4, origin = "fail", ("", "", "", "")
        # data check (not a filter criterion): the h = 1 target quarter must end after 16 May 2019 and be reported
        nxt = per[per.rd > (before.iloc[-1].rd if len(before) else EVENT)].sort_values("rd")
        h1 = "yes" if len(nxt) and nxt.iloc[0].rd > EVENT and (nxt.iloc[0].rd - (before.iloc[-1].rd if len(before) else EVENT)).days <= 120 else "NO"
        h = hits[hits.cik == r.cik]
        h1819 = h[h.fy.isin(["2018", "2019"])]
        hlater = h[h.fy >= "2020"]
        c5 = ("no hit: pass" if len(h1819) == 0 else "hit FY2018/19: read") + ("; later hit: read" if len(hlater) else "")
        fails = [n for n, ok in [("1 industry", sic in CODES), ("10-K filer", len(k1819) > 0),
                                 ("3 history", c3 != "fail"), ("4 origin", c4 == "pass"),
                                 ("no h=1 target", h1 == "yes")] if not ok]
        out.append({"cik": r.cik, "name": s["name"], "sic": sic, "rev2018_musd": round(r.rev2018_musd, 1),
                    "10k_fy2018_19": len(k1819), "first_10k10q_seen": str(early.date()) if pd.notna(early) else "",
                    "older_files_not_downloaded": missing_older, "c3_history": c3,
                    "origin_form": origin[0], "origin_period_end": origin[1], "origin_filed": origin[2],
                    "origin_days": origin[3], "c4_origin": c4, "c5_label": c5,
                    "fails_1_to_4": "; ".join(fails)})
    d = pd.DataFrame(out).sort_values(["fails_1_to_4", "c5_label", "name"])
    (PROJECT / "results").mkdir(exist_ok=True)
    d.to_csv(PROJECT / "results" / "donor_screen.csv", index=False)
    ok = d[d.fails_1_to_4 == ""]
    print(f"firms screened: {len(d)} | pass criteria 1-4: {len(ok)} (of which criterion 3 'pass?': {(ok.c3_history == 'pass?').sum()})")
    print("fail reasons:", d[d.fails_1_to_4 != ""].fails_1_to_4.value_counts().to_dict())
    print("among the passes, criterion 5:", ok.c5_label.value_counts().to_dict())
    pd.set_option("display.width", 220, "display.max_rows", 200)
    print("\n== fail criteria 1-4:")
    print(d[d.fails_1_to_4 != ""][["name", "sic", "rev2018_musd", "first_10k10q_seen", "origin_period_end", "origin_filed", "fails_1_to_4"]].to_string(index=False))
    print("\n== pass 1-4 but need reading (criterion 5):")
    print(ok[ok.c5_label != "no hit: pass"][["name", "sic", "rev2018_musd", "c3_history", "c5_label"]].to_string(index=False))


if __name__ == "__main__":
    main()
