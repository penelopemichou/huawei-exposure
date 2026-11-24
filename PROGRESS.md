# PROGRESS — huawei-exposure (Project 6)

Last updated: 24 Nov 2026 (Session 1).

Session 1 done: setup and reading only. Nothing downloaded, nothing committed, no forecast run.

## Sessions

| Session | Date | What | Status |
|---|---|---|---|
| 1 | 24 Nov 2026 | Setup, read Projects 2 and 5, screening plan, donor rule | Done |
| 2 | | SEC screening files and 10-Ks; fill the exposure table | Next (waits for "yes") |
| 3 | | Copy the code, build revenue tables, run B4 and AutoETS | Later |

## The question (fixed on 24 Nov 2026, before any forecast)

Did US suppliers with more **disclosed** Huawei exposure miss their revenue forecasts by more after Huawei was put on the US Entity List (16 May 2019) than suppliers with none?

**Descriptive only.** This can say "exposed firms missed by X more than donors". It cannot say why. 2019 was also a chip downturn, and US–China tariffs hit at the same time. Never write that the Entity List *caused* a miss.

## Design (fixed on 24 Nov 2026; do not change it after seeing results)

- **Rules:** only the Project 2 rules **B4** and **AutoETS**, with the same **65-day rule** and the same code. No new models, no tuning, no variants.
  - B4 = latest known quarter × geometric mean of the same step over the last 3 years.
  - AutoETS = statsforecast `AutoETS(season_length=4)`, chosen by AICc at the origin, on the latest unbroken stretch of ≥ 12 known quarters.
  - 65-day rule: at an origin, use only quarters whose `first_filed_date` is on or before the end of the firm's own fiscal origin quarter + 65 days.
- **Origin:** each firm's **last fiscal quarter ending before 16 May 2019**.
- **Horizons:** h = 1, 2, 3, 4 quarters ahead.
- **Outcome:** quarterly revenue as first reported.
- **Signed miss, in %:** 100 × (actual − forecast) ÷ actual. Positive = revenue came in above the forecast; negative = below. "Missed by more" means a more negative signed miss.
- **Groups:** exposed = the 10-K names Huawei as a 10 %+ customer in fiscal 2018 or 2019; donors = `notes/donor-rule.md`.
- **Reused, read-only:** the forecast-gap code (`~/Documents/forecast-gap`, commit `e332753`) and its yardstick file `results/yardstick_thresholds.csv`. Copies are recorded with SHA-256 fingerprints, as in forecast-gap.
- **Data:** public SEC filings only.

## Working rules (every session)

- Public data only. Never any employer or private data.
- Before every run, Claude writes its own prediction of the result.
- Never download anything without Penelope's explicit "yes". Before asking, list each file: name, source URL and size (estimated if unknown).
- Never commit without "yes, commit". Never push without "yes".
- The SEC User-Agent (name and email, `SEC_USER_AGENT`) and the SEC email (`SEC_EMAIL`) live only in `.env` (gitignored; see `.env.example`). Never print them, never commit them, never write them in code.
- `~/Documents/forecast-gap` and `~/Documents/ai-fpa-forecast` are read-only: copy from them, never change them.
- Stay under 10 requests per second to the SEC.
- No new installs. Run with Project 2's venv (`~/Documents/ai-fpa-forecast/.venv/bin/python`). Ask before installing anything.

## Session 1 log (24 Nov 2026)

- **Repo created** at `~/Documents/huawei-exposure` (branch `main`). Git name and email set for this repo only, copied from Project 2's settings. `.env` copied from forecast-gap without being opened. `.env.example`, `.gitignore`, `CLAUDE.md`, this file and two notes added. Not committed.
- **Which of the 20 Project 2 companies make chips or electronic components? None.** The 20 are toy makers and retailers, software/ads/streaming, machinery and household goods. The closest are Best Buy (sells electronics, doesn't make them) and Parker-Hannifin (mechanical motion-control parts). Two consequences:
  1. Every firm in this project is new and needs its own SEC file.
  2. The yardstick lines (90th percentile of usual misses) come from non-chip companies, whose revenue swings less. They are a rough guide only. The main comparison is exposed firms against donors.
- **What can be copied from forecast-gap:**

  | File | Copy how | Why |
  |---|---|---|
  | `src/baselines.py`, `src/ets.py`, `src/smoothing.py`, `src/latest_start.py`, `src/features.py` | unchanged | the B4 / AutoETS / 65-day code; identical to Project 2 at `457d1ff` |
  | `src/check_data.py` | unchanged | data checks; identical to Project 2 |
  | `src/download_edgar.py` | copy, then **one edit** (below) | reads the User-Agent from `.env` instead of writing a name in the code |
  | `results/yardstick_thresholds.csv` | unchanged | the 8 yardstick lines (B4 and ETS × h = 1–4) |
  | `data/project2/session4_forecasts.csv`, `data/project2/session7_b4_forecasts.csv`, `data/project2/revenue_quarterly.csv` | unchanged | the yardstick pools behind the lines (about 2.9 MB) |
  | `src/companies.py` | copy, then replace the company list | needs the new firms; shown as a diff |
  | `src/build_quarterly.py`, `src/list_revenue_tags.py` | copy, then add lines only | one revenue-tag line per new firm, as forecast-gap did for Meta |
  | `src/event_misses.py`, `src/yardstick.py`, `src/chart.py` | template only | Meta and Netflix are written into them |

- **Planned edit to a copied file: `src/download_edgar.py`** (decided 24 Nov 2026; the only change to this file). The copy is made in a later session, so the diff is applied then and shown again:

  ```diff
  -def read_email():
  -    """Return SEC_EMAIL from the .env file (a simple NAME=value file)."""
  +def read_user_agent():
  +    """Return SEC_USER_AGENT (name and email) from the .env file (a simple NAME=value file)."""
  ...
  -        if line.startswith("SEC_EMAIL="):
  +        if line.startswith("SEC_USER_AGENT="):
  ...
  -    raise SystemExit("SEC_EMAIL is missing from .env")
  +    raise SystemExit("SEC_USER_AGENT is missing from .env")
  ...
  -    headers = {"User-Agent": f"<your name, written in the code> {read_email()}"}
  +    headers = {"User-Agent": read_user_agent()}
  ```

  (The removed line is shown with a placeholder, so that no name is written in this repo.)

  `SEC_USER_AGENT` was added to `.env` (value not shown) and to `.env.example`.
- **Primary and secondary comparison** (decided 24 Nov 2026): firms with fewer than 20 quarters before the origin, or whose origin quarter was filed after the 65-day cutoff, are excluded from the PRIMARY comparison and listed in a SECONDARY table. Fewer than 4 primary exposed firms → tell Penelope before Session 3. Details: `notes/screening-plan.md`.
- **Written:** `notes/screening-plan.md` (the empty exposure table, the five known numbers marked "to verify", the nine candidates marked "from memory") and `notes/donor-rule.md` (the donor rule and its limits).

## Session 2 plan (proposed 24 Nov 2026, waits for "yes")

Three stages, each small. Stage B and C file names are only known after Stage A, so each later stage is shown again, file by file, and needs its own "yes".

**Stage A: screening files (one "yes"; about 2–8 MB, about 25–40 requests)**

| # | File | Source | Size (estimate) | Why |
|---|---|---|---|---|
| A1 | `CIK##########.json` for the 14 firms (CIKs from memory, below) | `https://data.sec.gov/submissions/CIK##########.json` | 0.05–1 MB each; ≤ 6 MB in all. Very active filers (Intel, Qualcomm) may need one extra older-filings file each (`CIK##########-submissions-001.json`, ≤ 1 MB) | confirms the CIK, SIC code, fiscal year end and the exact 10-K file names for fiscal 2018 and 2019 |
| A2 | full-text search results: "Huawei" in 10-Ks filed 2018-01-01 to 2020-12-31 | EDGAR full-text search, `https://efts.sec.gov/LATEST/search-index` (exact query shown before the first request) | 0.1–0.3 MB per page of 100 hits; about 2–6 pages | finds exposed firms not on the list, and shows which possible donors mention Huawei at all |
| A3 | lists of 10-K filers for SIC 3674, 3672, 3677, 3678, 3679 | `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=####&type=10-K` | 50–100 KB per page; about 10–15 pages | the donor pool |

CIKs from memory, to confirm in A1: Qorvo 0001604778, Skyworks 0000004127, Lumentum 0001633978, NeoPhotonics 0001227025, Inphi 0001160958, Acacia 0001651235, Finisar 0001094739, II-VI 0000820318, MACOM 0001493594, Xilinx 0000743988, Micron 0000723125, Intel 0000050863, Qualcomm 0000804328, Broadcom Inc. 0001730168. Broadcom Inc. replaced Broadcom Ltd in 2018, so like Google/Alphabet in Project 2 it may need the old entity too.

**Stage B: the 10-Ks (separate "yes", after Stage A)**

- The main 10-K document for fiscal 2018 and fiscal 2019 for each of the 14 firms: up to 28 files, `https://www.sec.gov/Archives/edgar/data/<CIK>/<accession>/<main document>.htm`, about 1–4 MB each, **about 30–100 MB in all**. Exact names come from A1.
- Donors: only the 10-Ks that A2 shows mention "Huawei" are downloaded and read. A 10-K with no Huawei mention needs no download; the search result is the evidence.
- Only the customer, risk-factor and segment/concentration sections are read. Each number goes into the table with its filing and section.

**Stage C: revenue data (separate "yes", after the exposure table is verified and the donor list is fixed)**

- `CIK##########.json` for each exposed firm and each donor, from `https://data.sec.gov/api/xbrl/companyfacts/`, about 1–10 MB each, saved to `data/raw/` (gitignored).

**Pre-flight eligibility table (built after Stage C, before any forecast)**

The copied code does not check the 20-quarter rule or the origin's filing date at a single origin (`forecasts_at` runs anyway, and `known_at` silently drops a late quarter). So this table checks every firm, exposed and donor, and decides PRIMARY or SECONDARY before anything is forecast. It is saved as `results/preflight_eligibility.csv` and shown in full.

| Column | Meaning |
|---|---|
| firm, group, CIK | group = named at 10 %+, named below 10 %, not named |
| origin quarter | fiscal label and real end date (the last fiscal quarter ending before 16 May 2019) |
| first quarter in table | the earliest quarter in the firm's revenue table |
| quarters up to the origin | (origin − first quarter) + 1, as `first_origin` counts them; also the number actually present, so gaps show |
| ≥ 20 quarters? | yes / no |
| origin filing date | the origin quarter's `first_filed_date` |
| cutoff | origin quarter end + 65 days |
| origin known at the cutoff? | yes / no |
| comparison | PRIMARY, or SECONDARY with the reason |

Then count the PRIMARY exposed firms. Fewer than 4 → stop and tell Penelope before Session 3.

**Copied locally, no internet (Session 2 or 3):** the forecast-gap files in the table above, with SHA-256 fingerprints in `notes/copied_from_forecast_gap.md`.

## Words used here

- **Entity List:** a US government list of foreign firms that US companies may not sell to without a licence. Huawei was added on 16 May 2019.
- **10-K:** a US company's annual report to the SEC. **10-Q:** the quarterly report.
- **10 % customer:** a customer bringing in 10 % or more of a firm's revenue. US accounting rules make firms report these; smaller customers can stay hidden.
- **Donor:** a comparison firm (here, a chip or component maker that did not disclose 10 %+ Huawei sales).
- **SIC code:** the SEC's four-digit industry code for each filer (3674 = semiconductors).
- **CIK:** the SEC's ID number for each filer.
- **Origin:** the last quarter of data a forecast may use. **h:** how many quarters ahead the forecast looks.
