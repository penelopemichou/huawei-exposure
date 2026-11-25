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

## Session 2 log (24 Nov 2026), not committed

- Session 1 committed (`41c03ce`, 6 files) after the private-word check (8 words, self-test first, 0 hits).
- **Stage A done** with Penelope's "yes": 42 of 60 requests, about 3.5 MB, no 10-Ks. New scripts `src/sec_stage_a.py` (downloads; reads `SEC_USER_AGENT` from `.env`; hard stop at 60) and `src/read_stage_a.py` (reads only). Results: `notes/stage-a-results.md`.
- **The search gives no sentences**, so no hit is labelled yet. Labels and the "Customer A" table need Stage B.
- Provisional: 12 of the 14 mention Huawei in a fiscal 2018/2019 10-K. **Intel and Xilinx are not named.** 22 other donor-code firms mention Huawei; 685 listed entries do not.

## Session 2 log, continued (25 Nov 2026), not committed after `865283b`

- Donor rule reworded to a label-based test (`notes/donor-rule.md`). Committed in `865283b` with the Stage A results and the Stage B plan, after the private-word and email check (clean).
- **Stage A2 done:** 5 frames files, 1.1 MB, requests 43–47 of 60.
  - 136 of the 714 industry-list entries have 2018 revenue; **91 have at least $100 million**.
  - **578 are missing from all 5 files**, mostly firms that stopped filing long ago, plus a few private individuals. The list is in `data/raw/stage_a/frames_missing.csv` (gitignored, because it holds private names).
  - Among our 14 and the 22: only **Cree** is missing (to check).
- **Stage B1 done:** 31 documents, 97.6 MB, largest 6.4 MB. 434 rows extracted and labelled. Results: `notes/stage-b-results.md`; every row: `notes/stage-b1-labels.md`; dropped donors: `results/dropped_donors.csv`.
- **Proposed:**
  - **exposed:** NeoPhotonics, Inphi, Lumentum, Qorvo, Micron, Finisar;
  - **low exposure (implied, to decide):** MACOM, Skyworks, Broadcom, Qualcomm;
  - **donor:** Intel;
  - **out of the donor group:** Xilinx (FY2020), Acacia (history), II-VI (industry code).
- New scripts: `src/sec_stage_b.py` (download with the 20 MB / 100 MB stops), `src/extract_sentences.py`, `src/label_sentences.py`.
- **Next step after A2 (counted, not started):** filing lists for 80 firms, about 80–100 requests.

## Session 2 log, continued (25 Nov 2026, second part), not committed

- **Decided by Penelope:**
  - MACOM, Skyworks, Broadcom and Qualcomm = **low exposure, implied**: not donors, not in the primary test, shown in their own rows and in the guidance-cut table.
  - Qualcomm's exposure is royalty income, not product sales.
  - Group and dose rules written in `donor-rule.md` and `screening-plan.md`.
  - Dose: NeoPhotonics 46 %, Inphi 14 %, Lumentum 11.0 %, Qorvo 13 %, Finisar 10 %, Micron 12 % (**fallback, flagged**).
- **Proposed B3 (not downloaded):** the Skyworks 10-Q for the quarter ended 29 Mar 2019, `q21910qmarch292019.htm` (`https://www.sec.gov/Archives/edgar/data/4127/000000412719000022/q21910qmarch292019.htm`). The whole filing is 4.8 MB; the document is estimated at 1.5–3 MB.
- **Cree (now Wolfspeed) missing from the frames:** its FY2019 revenue (Jun 2018–Jun 2019, $538.2M, refiled in a 2021 8-K) carries no frame label. It passes the size test by hand.
- **10 random entries of the 578 missing (seed 42):** 0 of 10 filed a 10-K for FY2018 or FY2019.
  - 6 stopped filing before 2018, 2 are 20-F filers, 1 started 10-Ks later, 1 files only Form D.
  - 0 of 10 still allows up to about 26 % of the 578 to have filed (95 % bound), and Cree shows the frames can miss an active firm.
  - Exact check proposed, not run: the SEC's quarterly 10-K index files for 2019.
- **Filing lists:** 80 firms + 7 older files + Cree = 88 of 100 requests (plus 2 Cree checks and 10 random lists); 0 errors.
  - Older files for the first-filing date were **not** downloaded (they would have made 109). Criterion 3 for 20 firms is "pass?", to confirm from the revenue files.
- **Donor screen** (`src/donor_screen.py`, `results/donor_screen.csv`):
  - 92 firms; 68 pass criteria 1–4; **40 pass with no Huawei hit**.
  - 14 have FY2018/19 hits not yet read; 6 have only later hits.
  - 24 fail: 10 not 10-K filers, 13 too young (incl. Broadcom Inc., new entity 2018), SigmaTron's origin filed 86 days late.
- **Pre-flight from filing lists** (`src/preflight_from_filings.py`, `results/preflight_from_filings.csv`). An estimate: the exact 20-quarter count needs the revenue files.
  - All 7 origins filed within 65 days.
  - **Lumentum** 16 reports up to the origin (likely fails the 20-quarter rule) and **Qorvo** 20 (borderline). The predecessor joins (JDSU, RFMD/TriQuint) are from memory, to verify.
  - **Finisar's last report is the 10-Q for Jul 2019: h = 1 only.**
  - **Warning:** at h = 2–4 the primary exposed group may be only NeoPhotonics, Inphi, Micron and Qorvo (4), or 3 if Qorvo fails. That is below Penelope's stop line.
- **B2 revised** (`notes/stage-b-plan.md`, not downloaded): 45 documents.
  - B2a: 21 documents, 14 firms that can become donors.
  - B2b: 11 later documents, read only if still a donor after B2a.
  - B2c: 13 documents, 8 firms, exposure only.
  - Limit: the search covers 10-Ks filed up to 31 Dec 2020, so later filings are checked for firms with mid-2020 year ends but not for December year ends.

## Session 2 log, continued (25 Nov 2026, third part)

- **`notes/design-v2.md` written first:** h = 1 primary (h = 2, 3 secondary; h = 4 flagged COVID), the primary test with a permutation p-value, dose-response descriptive only, and the stitching rule.
- **README.md created**, with the limits (including the later-filing gap for December year-end firms).
- **Guidance-cut table** added to the plan below (nothing downloaded).
- **16 well-known US chip firms:** all are in the 92 screened. The SEC index files are not needed.
- **Downloads:** B2a + B2c 34 documents (119.0 MB of 120), B3 1 document (1.0 MB), 7 revenue files (1.8–4.4 MB). No errors.
- **Results:** `notes/stage-b-results.md`, every B2 row in `notes/stage-b2-labels.md`, dropped donors in `results/dropped_donors.csv` (25 lines).
  - Donors so far 41 (+ up to 7 after B2b).
  - **Oclaro** is exposed (11 % FY2018) but has no data after the event.
  - No new exposed firm in B2c.
  - Skyworks' "about 12 % of H1 FY2019" is not in the March 2019 10-Q: **unsourced, not used**.
  - New data check: the h = 1 target must be reported after 16 May 2019.
- **Quarter counts** (`results/quarter_counts.csv`, no values printed): all 7 firms pass the 20-quarter rule by Project 2's count. Qorvo qualifies for stitching but needs none.
  - **Lumentum's 23 include 9 pre-spin-off carve-out quarters**, which rule (c) may exclude. Penelope decides.
- **B2b (11 documents) waits** for Penelope's reading of the B2a results.

## Session 2 log, continued (25 Nov 2026, fourth part), not committed after `1a3bff2`

- **Private-word scan changed** (the scan lives outside the repo):
  - Two of the words must now match as whole words. The others and the email still match anywhere.
  - The self-test plants a two-word name, the bare word, and a longer company name that contains it; only the first two are caught.
  - Clean, so all changes were committed in `1a3bff2`.
- **Lumentum → SECONDARY**, with both reasons in `design-v2.md` (d). Primary exposed: 5 at h = 1, 4 at h = 2–4.
- Three-group descriptive check added (`design-v2.md` (e)).
- Skyworks "about 12 % of H1 FY2019" is marked **unsourced, not used** everywhere.
- README limits: acquired firms drop out of the sample.
- **B2b:** 11 documents, 42.8 MB (limit 60).
  - Alpha & Omega (indirect), Applied Materials (indirect), Cirrus Logic and Marvell are **moved out** by later filings.
  - Ambarella and Microchip **stay donors**.
  - Kulicke & Soffa is **unclear**.
  - Mellanox re-read in context ("we work with leading vendors … including … Huawei"): **unclear**.
  - **Donors: 42**, plus 2 unclear.
- Every row a donor decision depends on: `notes/decision-rows.md` (15 donor rows, 81 hand-relabelled rows, plus the Mellanox change).
- **Sub-sector tags** in `results/sub_sector_tags.csv`. The donors' tags are from memory (their 10-Ks were not read).
  - Exposed: 4 optical/datacom, 1 handset RF, 1 memory.
  - Donors: 40 analog/other, 1 memory, 1 optical/datacom.
- **Prepared, not run:** `notes/frozen-lists.md` (DRAFT), `notes/permutation-setup.md` (DRAFT; exact enumeration, C(47, 5) = 1,533,939), `notes/predictions-before-run.md` (template).

## Session 2 log, continued (25 Nov 2026, fifth part), not committed

- **Standing rule: unclear = out of donors** (`donor-rule.md`). Mellanox and Kulicke & Soffa are out.
- **Permutation setup** (`permutation-setup.md`, DRAFT):
  - one-sided primary, two-sided shown;
  - rank-sum of the exposed firms, exact enumeration;
  - per-firm outcome = average of the B4 and AutoETS h = 1 signed miss, each rule also separately;
  - "consistent" only if both rules point the same way.
- **design-v2 (f):** primary donors = chip and optical-component makers; contract manufacturers, solar and equipment makers go to a sensitivity group.
- **design-v2 (g):** secondary outcome = signed miss ÷ the firm's own median absolute pre-event miss, with the number of pre-event forecasts.
- **README:** the optical/datacom vs other mismatch cannot be separated from Huawei exposure.
- **Class table** (`src/classify_firms.py`, `results/firm_classes.csv`, DRAFT; from files on disk only):
  - SIC descriptions cannot split 3674 firms, so 29 of 52 rows rest on memory (marked).
  - Donors: 15 chip (PRIMARY), 19 sensitivity, 5 "other" (to decide), 3 unclear (IPG Photonics, OSI Systems, Viavi; their latest pre-event 10-Ks are proposed as Stage D, not downloaded).
- Frozen lists still **DRAFT**.

## Session 2 log, continued (25 Nov 2026, sixth part), not committed

- **Class rule added to `donor-rule.md`:** a finished system or instrument, or an unclear class, goes to sensitivity, and so do the "other" firms. Stage D is **not** downloaded.
- **Donors: 15 PRIMARY (all chip makers; no optical-component donor) and 27 sensitivity** (`results/firm_classes.csv`).
- Waiting for Penelope's confirmation of the table. The revenue-file list comes after that.

## Session 2 log, continued (25 Nov 2026, seventh part), not committed

- **Stage E** (Penelope's "yes"): 8 10-K documents, 22.5 MB (limits 10 MB per file, 60 MB in total; largest 4.5 MB). Read only the opening of Item 1 to set the class.
- **Confirmed:**
  - chip: Power Integrations, Monolithic Power;
  - equipment and materials: AXT;
  - contract manufacturer: Amkor;
  - other: Vicor;
  - sensitivity by the rule: IPG Photonics (lasers mainly for industrial machines), Viavi (test instruments).
- **Changed: Rambus moves from PRIMARY to sensitivity** (other: patent royalties 56 % of 2018 revenue).
- **Donors: 14 PRIMARY (all chip makers), 28 sensitivity.** 21 of 52 class rows still rest on memory.

## Session 2 log, continued (25 Nov 2026, eighth part), not committed

- **Class table confirmed by Penelope.**
- **Stage C (Penelope's "yes"):** 45 revenue files, 153.5 MB (limits 10 MB per file, 200 MB in total; largest 4.8 MB), 0 errors. New size-capped job `stagec` in `src/sec_filing_lists.py`.
- **Quarter counts for all 52 firms** (`src/count_quarters.py all`, `results/quarter_counts_all.csv`; counts and dates only, no values):
  - all 14 primary and 28 sensitivity donors pass the 20-quarter rule and have h = 1–4;
  - all 6 exposed firms pass (Lumentum is SECONDARY by decision; Finisar has h = 1 only);
  - low exposure: MACOM, Skyworks and Qualcomm pass; **Broadcom fails (10 quarters)**.
- **Criterion 3 confirmed** for the 13 "pass?" donors: earliest revenue value filed 2009–2012.
- **Open: Broadcom.** From memory it is the same business as Broadcom Ltd (re-registered in 2018) and, before that, Avago (the accounting acquirer of Broadcom Corp in 2016), so it would qualify for stitching under design-v2 (c). Not checked; Penelope decides.

## Session 2 log, continued (25 Nov 2026, ninth part), not committed

- **Stage C2** (Penelope's "yes"): filing lists and revenue files for Broadcom Ltd (0001649338) and Avago (0001441634), 4 files, 2.1 MB.
- **Result:** the same fiscal calendar and 9 of 9 overlapping quarters identical, so the stitch qualifies under design-v2 (c). Stitched: 38 quarters, no gaps; unstitched: 10.
- **Stitching approved by Penelope (25 Nov 2026):** Avago → Broadcom Ltd → Broadcom Inc. (`results/stitching.csv`; newest file wins where they overlap). Broadcom now has 38 quarters and passes the 20-quarter rule. The level jumps (Feb 2016, and from memory Nov 2018) are flagged next to its results. **All 52 firms now pass the pre-flight checks** (Finisar h = 1 only; Lumentum SECONDARY by decision).

## Plan: guidance-cut table (added 25 Nov 2026; nothing downloaded)

**One row per firm that revised its current-quarter revenue guidance after 16 May 2019.** Firms looked at: the exposed firms, the "low exposure, implied" firms and the donors.

| Column | Content |
|---|---|
| firm | |
| quarter guided | the fiscal quarter the guidance is for (the quarter in progress on 16 May 2019) |
| range before | the guided revenue range, with date and accession of the 8-K it came from |
| range after | the revised range, with date and accession |
| midpoint change % | 100 × (midpoint after − midpoint before) ÷ midpoint before |
| revision names Huawei? | yes / no, from the text of the revision |
| Huawei dose | from `screening-plan.md` ("n/a" for low exposure and donors) |

- **No revision = "no revision", never 0.**
- **Sources: 8-K earnings releases** (usually exhibit 99.1) in the SEC filing lists already saved. Candidate 8-Ks are picked from those lists (filed between the last guidance before 16 May 2019 and the end of the guided quarter). The file list with links and sizes is shown before any "yes".
- **A firm that gives no quarterly guidance** is marked "no guidance given", not "no revision".

## Session 2 plan (proposed 24 Nov 2026, waits for "yes")

Three stages, each small. Stage B and C file names are only known after Stage A, so each later stage is shown again, file by file, and needs its own "yes".

**Stage A: screening files (one "yes"; about 2–8 MB, about 25–40 requests)**

| # | File | Source | Size (estimate) | Why |
|---|---|---|---|---|
| A1 | `CIK##########.json` for the 14 firms (CIKs from memory, below) | `https://data.sec.gov/submissions/CIK##########.json` | 0.05–1 MB each; ≤ 6 MB in all. Very active filers (Intel, Qualcomm) may need one extra older-filings file each (`CIK##########-submissions-001.json`, ≤ 1 MB) | confirms the CIK, SIC code, fiscal year end and the exact 10-K file names for fiscal 2018 and 2019 |
| A2 | full-text search results: "Huawei" in 10-Ks filed 2018-01-01 to 2020-12-31 | EDGAR full-text search, `https://efts.sec.gov/LATEST/search-index` (exact query shown before the first request) | 0.1–0.3 MB per page of 100 hits; about 2–6 pages | finds exposed firms not on the list, and shows which possible donors mention Huawei at all |
| A3 | lists of 10-K filers for SIC 3674, 3672, 3677, 3678, 3679 | `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&SIC=####&type=10-K` | 50–100 KB per page; about 10–15 pages | the donor pool |

CIKs from memory, to confirm in A1: Qorvo 0001604778, Skyworks 0000004127, Lumentum 0001633978, NeoPhotonics 0001227025, Inphi 0001160958, Acacia 0001651235, Finisar 0001094739, II-VI 0000820318, MACOM 0001493594, Xilinx 0000743988, Micron 0000723125, Intel 0000050863, Qualcomm 0000804328, Broadcom Inc. 0001730168. Broadcom Inc. replaced Broadcom Ltd in 2018, so like Google/Alphabet in Project 2 it may need the old entity too.

**Stage A2: 2018 revenue for all filers (drafted 25 Nov 2026; separate "yes"; 5 requests, about 1.5–3 MB)**

The SEC "frames" files list one value per filer for one XBRL tag and one period, for **all** filers at once. Joining them to the 714 industry-list entries by CIK gives each firm's 2018 revenue without 700 requests. One file per revenue tag Project 2 uses:

| # | File (saved as) | Source | Size (estimate) |
|---|---|---|---|
| 1 | `frames/Revenues_CY2018.json` | `https://data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2018.json` | 0.5–1.5 MB |
| 2 | `frames/RevenueFromContractWithCustomerExcludingAssessedTax_CY2018.json` | `https://data.sec.gov/api/xbrl/frames/us-gaap/RevenueFromContractWithCustomerExcludingAssessedTax/USD/CY2018.json` | 0.5–1.5 MB |
| 3 | `frames/RevenueFromContractWithCustomerIncludingAssessedTax_CY2018.json` | `https://data.sec.gov/api/xbrl/frames/us-gaap/RevenueFromContractWithCustomerIncludingAssessedTax/USD/CY2018.json` | 0.02–0.2 MB |
| 4 | `frames/SalesRevenueNet_CY2018.json` | `https://data.sec.gov/api/xbrl/frames/us-gaap/SalesRevenueNet/USD/CY2018.json` | 0.02–0.3 MB |
| 5 | `frames/SalesRevenueGoodsNet_CY2018.json` | `https://data.sec.gov/api/xbrl/frames/us-gaap/SalesRevenueGoodsNet/USD/CY2018.json` | 0.02–0.2 MB |

Saved under `data/raw/stage_a/frames/` (gitignored). Limits of these files:

- **"CY2018" is calendar 2018.** The SEC puts in each filer's annual value that best fits calendar 2018, so for a firm with another fiscal year end it is the nearest fiscal year. That is good enough for a size filter, not for forecasting.
- **Values are the latest filed** (after restatements), not first reported. Again fine for a size filter.
- **A firm can be missing from all five files.** That happens if it used another tag, reported under IFRS or filed no XBRL. Such firms are counted and listed as "no 2018 revenue found", not dropped silently.
- **Next step:** checking first filing and origin filing for the firms that pass needs one revenue file per firm (Stage C, `companyfacts`). The number of firms is known only after A2. If it is more than 60, Penelope is asked first.

**Stage B: the 10-Ks (separate "yes", after Stage A)**

**Drafted 25 Nov 2026 in `notes/stage-b-plan.md`:** B1 = 31 documents (14 firms, FY2018 and FY2019, Xilinx FY2020, 2 10-K/As), B2 = 34 documents (22 firms). Each stage needs its own "yes". The older text below is the first outline.

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
