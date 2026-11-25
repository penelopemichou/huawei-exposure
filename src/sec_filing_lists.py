"""Session 2: SEC filing lists (submissions files) and two small Cree checks.

Each request is logged in data/raw/filing_lists/request_log.csv with its purpose.
Limits per purpose (approved by Penelope on 25 Nov 2026):
    cree      <= 2    companyconcept files for Cree's two likely revenue tags
    random10  <= 10   filing lists of 10 random entries missing from the frames files
    lists80   <= 100  filing lists of the 80 firms with >= $100M 2018 revenue, plus older-filing files
One request every 0.5 s (2 per second; Penelope's limit is 5). Stops after 2 errors in a row
or 3 errors in total. The User-Agent is read from .env and never printed.

Run from the project folder:
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_filing_lists.py cree
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_filing_lists.py random10
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_filing_lists.py lists80
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_filing_lists.py older FILE_NAME [FILE_NAME ...]
"""

import csv
import random
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

PROJECT = Path(__file__).resolve().parent.parent
STAGE_A = PROJECT / "data" / "raw" / "stage_a"
OUT = PROJECT / "data" / "raw" / "filing_lists"
LOG = OUT / "request_log.csv"
LIMITS = {"cree": 2, "random10": 10, "lists80": 100, "revenue7": 7}
# revenue7 (approved 25 Nov 2026): XBRL companyfacts of the 6 exposed firms and Intel
REVENUE7 = {"NeoPhotonics": "0001227025", "Inphi": "0001160958", "Lumentum": "0001633978", "Qorvo": "0001604778",
            "Micron": "0000723125", "Finisar": "0001094739", "Intel": "0000050863"}
PAUSE_SECONDS = 0.5
CREE = "0000895419"
errors = {"in_a_row": 0, "total": 0}


def user_agent():
    for line in (PROJECT / ".env").read_text().splitlines():
        if line.startswith("SEC_USER_AGENT="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("SEC_USER_AGENT is missing from .env")


def used(purpose):
    if not LOG.exists():
        return 0
    with LOG.open() as f:
        return sum(1 for r in csv.DictReader(f) if r["purpose"] == purpose)


def get(purpose, url, out_file):
    if out_file.exists():
        print(f"  kept (already here): {out_file.name}")
        return
    n = used(purpose)
    if n >= LIMITS[purpose]:
        raise SystemExit(f"STOP: {n} '{purpose}' requests logged, limit {LIMITS[purpose]}. Ask Penelope first.")
    time.sleep(PAUSE_SECONDS)
    r = requests.get(url, headers={"User-Agent": user_agent()}, timeout=60)
    new = not LOG.exists()
    with LOG.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["purpose", "n", "time", "status", "mb", "url"])
        w.writerow([purpose, n + 1, datetime.now().isoformat(timespec="seconds"), r.status_code,
                    f"{len(r.content) / 1e6:.2f}", url])
    if r.status_code == 200:
        errors["in_a_row"] = 0
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_bytes(r.content)
        print(f"  {purpose} {n + 1}/{LIMITS[purpose]}: {len(r.content) / 1e6:.2f} MB  {out_file.name}")
    else:
        errors["in_a_row"] += 1
        errors["total"] += 1
        print(f"  {purpose} {n + 1}/{LIMITS[purpose]}: HTTP {r.status_code}  {out_file.name}")
        if errors["in_a_row"] >= 2 or errors["total"] >= 3:
            raise SystemExit(f"STOP: repeated errors ({errors}). Ask Penelope first.")


def submissions(purpose, cik):
    cik = str(cik).zfill(10)
    get(purpose, f"https://data.sec.gov/submissions/CIK{cik}.json", OUT / "submissions" / f"CIK{cik}.json")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    job = sys.argv[1]
    if job == "cree":
        for tag in ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"]:
            get("cree", f"https://data.sec.gov/api/xbrl/companyconcept/CIK{CREE}/us-gaap/{tag}.json",
                OUT / "cree" / f"CIK{CREE}_{tag}.json")
    elif job == "random10":
        missing = list(csv.DictReader((STAGE_A / "frames_missing.csv").open()))
        pick = random.Random(42).sample(missing, 10)            # seed 42, fixed before the draw
        (OUT / "random10_ciks.txt").write_text("\n".join(p["cik"] for p in pick) + "\n")
        for p in pick:
            submissions("random10", p["cik"])
    elif job == "lists80":
        rows = list(csv.DictReader((STAGE_A / "sic_universe_revenue.csv").open()))
        have = {p.stem[3:] for p in (STAGE_A / "submissions").glob("CIK??????????.json")}
        todo = [r["cik"].zfill(10) for r in rows if r["rev2018_musd"] and float(r["rev2018_musd"]) >= 100
                and r["cik"].zfill(10) not in have]
        print(f"lists80: {len(todo)} firms")
        for cik in todo:
            submissions("lists80", cik)
    elif job == "revenue7":
        for firm, cik in REVENUE7.items():
            get("revenue7", f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json",
                OUT / "companyfacts" / f"CIK{cik}.json")
    elif job == "older":
        for name in sys.argv[2:]:
            get("lists80", f"https://data.sec.gov/submissions/{name}", OUT / "submissions" / name)
    else:
        raise SystemExit(f"unknown job {job}")


if __name__ == "__main__":
    main()
