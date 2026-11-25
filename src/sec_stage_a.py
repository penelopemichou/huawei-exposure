"""Session 2, Stage A: download the screening files from the SEC (no 10-Ks).

Every request is logged in data/raw/stage_a/request_log.csv. The script refuses
to send a request once 60 have been logged (Penelope's limit for Stage A).
One request every 0.5 s (the SEC limit is 10 per second).
The User-Agent is read from .env (SEC_USER_AGENT) and never printed.

Run from the project folder, one job at a time:
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_stage_a.py submissions CIK [CIK ...]
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_stage_a.py overflow FILE_NAME [FILE_NAME ...]
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_stage_a.py fts QUERY_NAME PAGE
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_stage_a.py sic CODE PAGE
"""

import csv
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode

import requests

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "data" / "raw" / "stage_a"
LOG = OUT / "request_log.csv"
MAX_REQUESTS = 60
PAUSE_SECONDS = 0.5

# Full-text searches (fixed before the first request).
FTS_QUERIES = {
    "huawei": {"q": '"Huawei"', "forms": "10-K", "dateRange": "custom",
               "startdt": "2018-01-01", "enddt": "2020-12-31"},
}


def user_agent():
    for line in (PROJECT / ".env").read_text().splitlines():
        if line.startswith("SEC_USER_AGENT="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("SEC_USER_AGENT is missing from .env")


def requests_so_far():
    if not LOG.exists():
        return 0
    with LOG.open() as f:
        return sum(1 for _ in csv.DictReader(f))


def get(url, out_file):
    """One logged request. Keeps files that already exist (no second request)."""
    if out_file.exists():
        print(f"  kept (already here): {out_file.relative_to(OUT)}")
        return
    n = requests_so_far()
    if n >= MAX_REQUESTS:
        raise SystemExit(f"STOP: {n} requests logged, limit is {MAX_REQUESTS}. Ask Penelope first.")
    time.sleep(PAUSE_SECONDS)
    r = requests.get(url, headers={"User-Agent": user_agent()}, timeout=60)
    new_log = not LOG.exists()
    with LOG.open("a", newline="") as f:
        w = csv.writer(f)
        if new_log:
            w.writerow(["n", "time", "status", "bytes", "url", "file"])
        w.writerow([n + 1, datetime.now().isoformat(timespec="seconds"), r.status_code,
                    len(r.content), url, out_file.relative_to(OUT)])
    print(f"  request {n + 1}/{MAX_REQUESTS}: HTTP {r.status_code}, {len(r.content) / 1e6:.2f} MB -> "
          f"{out_file.relative_to(OUT)}")
    if r.status_code == 200:
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_bytes(r.content)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    job, args = sys.argv[1], sys.argv[2:]
    if job == "submissions":
        for cik in args:
            cik = cik.zfill(10)
            get(f"https://data.sec.gov/submissions/CIK{cik}.json", OUT / "submissions" / f"CIK{cik}.json")
    elif job == "overflow":
        for name in args:
            get(f"https://data.sec.gov/submissions/{name}", OUT / "submissions" / name)
    elif job == "fts":
        name, page = args[0], int(args[1])
        params = dict(FTS_QUERIES[name])
        if page > 1:
            params["from"] = (page - 1) * 100
        get("https://efts.sec.gov/LATEST/search-index?" + urlencode(params),
            OUT / "fts" / f"{name}_p{page}.json")
    elif job == "frames":   # Stage A2: calendar-2018 revenue, all filers, one file per tag
        for tag in args:
            get(f"https://data.sec.gov/api/xbrl/frames/us-gaap/{tag}/USD/CY2018.json",
                OUT / "frames" / f"{tag}_CY2018.json")
    elif job == "sic":
        code, page = args[0], int(args[1])
        params = {"action": "getcompany", "SIC": code, "type": "10-K", "dateb": "",
                  "owner": "include", "count": 100, "start": (page - 1) * 100}
        get("https://www.sec.gov/cgi-bin/browse-edgar?" + urlencode(params),
            OUT / "sic" / f"sic{code}_p{page}.html")
    else:
        raise SystemExit(f"unknown job {job}")
    print(f"  total requests logged: {requests_so_far()}/{MAX_REQUESTS}")


if __name__ == "__main__":
    main()
