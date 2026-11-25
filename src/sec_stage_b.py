"""Session 2, Stage B: download the 10-K documents listed in notes/stage-b-plan.md.

Only the exact links in the stage's table are used. Each file's size is read from
the server's reply BEFORE the file is saved:
  - a single file over 20 MB  -> stop, nothing saved for it;
  - the run total over the limit (100 MB unless --max-total) -> stop, nothing saved for it.
Every request is logged in data/raw/stage_b/request_log.csv; hard stop at 60.
One request every 0.5 s. The User-Agent is read from .env and never printed.

Run from the project folder (one or more stages; the size limits apply to the whole run):
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_stage_b.py B1
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/sec_stage_b.py B2a B2c --max-total 120
Each run has its own log (B1: request_log.csv; others: request_log_<stages>.csv) and its own total.
"""

import csv
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

PROJECT = Path(__file__).resolve().parent.parent
PLAN = PROJECT / "notes" / "stage-b-plan.md"
OUT = PROJECT / "data" / "raw" / "stage_b"
LOG = OUT / "request_log.csv"
MAX_REQUESTS = 60
MAX_FILE_MB = 20
MAX_TOTAL_MB = 100
PAUSE_SECONDS = 0.5
CHUNK = 1 << 20


def user_agent():
    for line in (PROJECT / ".env").read_text().splitlines():
        if line.startswith("SEC_USER_AGENT="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("SEC_USER_AGENT is missing from .env")


def links(stage):
    """The exact links in the stage's table (the section that starts with '## B1:' etc.)."""
    text = PLAN.read_text()
    m = re.search(rf"^#{{2,3}} {re.escape(stage)}:.*$", text, re.M)
    section = re.split(r"\n#{2,3} ", text[m.end():], maxsplit=1)[0]
    return re.findall(r"\| (https://www\.sec\.gov/Archives/edgar/data/\S+) \|", section)


def log(row):
    new = not LOG.exists()
    with LOG.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["n", "time", "status", "mb", "result", "url"])
        w.writerow(row)


def n_logged():
    if not LOG.exists():
        return 0
    with LOG.open() as f:
        return sum(1 for _ in csv.DictReader(f))


def path_for(url):
    parts = url.split("/")
    return OUT / parts[-3].zfill(10) / parts[-2] / parts[-1]


def main():
    global LOG, MAX_TOTAL_MB
    args = sys.argv[1:]
    global MAX_FILE_MB
    for flag in ("--max-total", "--max-file"):
        if flag in args:
            i = args.index(flag)
            if flag == "--max-total":
                MAX_TOTAL_MB = float(args[i + 1])
            else:
                MAX_FILE_MB = float(args[i + 1])
            args = args[:i] + args[i + 2:]
    stages = args
    if stages != ["B1"]:
        LOG = OUT / f"request_log_{'_'.join(stages)}.csv"
    urls = [u for s in stages for u in links(s)]
    print(f"{' + '.join(stages)}: {len(urls)} links in the plan; limits {MAX_FILE_MB} MB per file, {MAX_TOTAL_MB:g} MB in total")
    OUT.mkdir(parents=True, exist_ok=True)
    total = sum(path_for(u).stat().st_size for u in urls if path_for(u).exists()) / 1e6   # this run's files only
    headers = {"User-Agent": user_agent()}
    for url in urls:
        parts = url.split("/")
        out_file = path_for(url)
        if out_file.exists():
            print(f"  kept (already here): {parts[-1]}")
            continue
        n = n_logged()
        if n >= MAX_REQUESTS:
            raise SystemExit(f"STOP: {n} requests logged, limit {MAX_REQUESTS}. Ask Penelope first.")
        time.sleep(PAUSE_SECONDS)
        stamp = datetime.now().isoformat(timespec="seconds")
        with requests.get(url, headers=headers, stream=True, timeout=120) as r:
            size = int(r.headers.get("Content-Length", 0)) / 1e6
            if r.status_code != 200:
                log([n + 1, stamp, r.status_code, "", "error", url])
                raise SystemExit(f"STOP: HTTP {r.status_code} for {parts[-1]}")
            if size > MAX_FILE_MB:
                log([n + 1, stamp, 200, f"{size:.1f}", f"not saved: file over {MAX_FILE_MB:g} MB", url])
                raise SystemExit(f"STOP: {parts[-1]} is {size:.1f} MB (> {MAX_FILE_MB} MB). Not saved.")
            if total + size > MAX_TOTAL_MB:
                log([n + 1, stamp, 200, f"{size:.1f}", f"not saved: total over {MAX_TOTAL_MB:g} MB", url])
                raise SystemExit(f"STOP: {parts[-1]} ({size:.1f} MB) would bring the total to "
                                 f"{total + size:.1f} MB (> {MAX_TOTAL_MB} MB). Not saved.")
            body = b""
            for chunk in r.iter_content(CHUNK):      # also guards a missing Content-Length
                body += chunk
                if len(body) / 1e6 > MAX_FILE_MB:
                    log([n + 1, stamp, 200, f">{MAX_FILE_MB}", f"not saved: file over {MAX_FILE_MB:g} MB", url])
                    raise SystemExit(f"STOP: {parts[-1]} passed {MAX_FILE_MB} MB while reading. Not saved.")
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_bytes(body)
        total += len(body) / 1e6
        log([n + 1, stamp, 200, f"{len(body) / 1e6:.1f}", "saved", url])
        print(f"  request {n + 1}: {len(body) / 1e6:5.1f} MB  total {total:6.1f} MB  {parts[-1]}")
    print(f"done: total {total:.1f} MB, {n_logged()} requests logged")


if __name__ == "__main__":
    main()
