"""Download SEC EDGAR "companyfacts" JSON files for our companies.

A companyfacts file holds every number a company has tagged in its
filings (10-Q, 10-K, ...), for every period, together with the filing
it came from. We save each file unchanged in data/raw/.

Files that are already in data/raw/ are kept, so earlier results stay
reproducible. Add --refresh to download everything again.

Run from the project folder:
    .venv/bin/python src/download_edgar.py [--refresh]
"""

import json
import sys
import time
from pathlib import Path

import requests

from companies import COMPANIES as COMPANY_LIST

# --- 1. Settings --------------------------------------------------------

# The project folder is one level above this file (src/..).
PROJECT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT / "data" / "raw"

# CIK = the SEC's ID number for a company, always written with 10 digits.
COMPANIES = {cik: entity for _, entities, _ in COMPANY_LIST.values() for cik, entity in entities}

URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"

# The SEC allows at most 10 requests per second. Waiting 0.5 seconds
# between requests keeps us far below that (2 per second).
PAUSE_SECONDS = 0.5


# --- 2. Read the email from .env -----------------------------------------

def read_user_agent():
    """Return SEC_USER_AGENT (name and email) from the .env file (a simple NAME=value file)."""
    env_file = PROJECT / ".env"
    if not env_file.exists():
        raise SystemExit("No .env file. Copy .env.example to .env and add your email.")
    for line in env_file.read_text().splitlines():
        if line.startswith("SEC_USER_AGENT="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("SEC_USER_AGENT is missing from .env")


# --- 3. Download each company ----------------------------------------------

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # The SEC asks every program to say who it is: a name and an email.
    headers = {"User-Agent": read_user_agent()}

    refresh = "--refresh" in sys.argv
    for cik, name in COMPANIES.items():
        out_file = RAW_DIR / f"CIK{cik}.json"
        if out_file.exists() and not refresh:
            print(f"{name:<38} -> {out_file.name}  already downloaded, kept")
            continue
        response = requests.get(URL.format(cik=cik), headers=headers, timeout=60)
        response.raise_for_status()  # stop with an error if the SEC says no

        out_file.write_bytes(response.content)  # save exactly what we got

        # A quick look inside, so we know the file is what we expect.
        data = json.loads(response.content)
        n_tags = len(data["facts"].get("us-gaap", {}))
        size_mb = len(response.content) / 1_000_000
        print(f"{name:<38} -> {out_file.name}  {size_mb:5.1f} MB, "
              f"SEC name: {data['entityName']!r}, {n_tags} us-gaap tags")

        time.sleep(PAUSE_SECONDS)


if __name__ == "__main__":
    main()
