# Stage A results (24 Nov 2026)

42 SEC requests (limit 60), about 3.5 MB, all in `data/raw/stage_a/` (gitignored; every request in `request_log.csv`). No 10-K was downloaded. Two requests returned HTTP 503 (server busy) and were retried once, successfully.

## Important: the hits cannot be labelled yet

EDGAR full-text search returns **which document** mentions "Huawei", but **not the sentence**. So no hit can be labelled "customer with %", "customer without %" or "competitor/other mention" yet. That needs the documents themselves (Stage B, separate "yes"). Every group below is therefore **provisional**:

- **mentions Huawei** in a fiscal 2018 or 2019 10-K → to read in Stage B: it becomes named at 10 %+, named below 10 %, or "other mention" (which counts as not named);
- **no mention** in a fiscal 2018 or 2019 10-K → **not named** (no download needed; the search result is the evidence).

Fiscal year = the calendar year in which the fiscal year ends, as in Project 2.

The "Customer A" table (unnamed 10 %+ customers) is **empty for now**: it can only be filled by reading the customer sections in Stage B.

## Search

"Huawei", form 10-K, filed 2018-01-01 to 2020-12-31: **266 documents, 260 filings, 129 firms**. Documents: 250 10-K, 9 10-K/A, 7 exhibits. Full list: `data/raw/stage_a/fts/huawei_hits.csv`.

## The 14 firms

| Firm | CIK | SIC | FY end | First 10-K/10-Q | Origin (period end, form, filed) | Huawei mentioned in 10-K for | Provisional group |
|---|---|---|---|---|---|---|---|
| Qorvo | 0001604778 | 3674 | ~31 Mar | 2014-09-12 | 2019-03-30, 10-K, filed 2019-05-17 | FY2018, FY2019, FY2020 | mentions: read |
| Skyworks | 0000004127 | 3674 | ~30 Sep | 1995-02-15 | 2019-03-29, 10-Q, filed 2019-05-03 | FY2018, FY2019 (+10-K/A), FY2020 | mentions: read |
| Lumentum | 0001633978 | 3669 | ~30 Jun | 2015-09-25 | 2019-03-30, 10-Q, filed 2019-05-07 | FY2017 (10-K/A), FY2018, FY2019, FY2020 | mentions: read |
| NeoPhotonics | 0001227025 | 3674 | 31 Dec | 2011-03-28 | 2019-03-31, 10-Q, filed 2019-05-07 | FY2017, FY2018, FY2019 (+10-K/A) | mentions: read |
| Inphi | 0001160958 | 3674 | 31 Dec | 2011-03-07 | 2019-03-31, 10-Q, filed 2019-05-06 | FY2017, FY2018, FY2019 | mentions: read |
| Acacia | 0001651235 | 3674 | 31 Dec | 2016-08-11 | 2019-03-31, 10-Q, filed 2019-05-02 | FY2017, FY2018, FY2019 | mentions: read |
| Finisar | 0001094739 | 3674 | ~30 Apr | 1999-12-27 | 2019-04-28, 10-K, filed 2019-06-14 | FY2018, FY2019 | mentions: read |
| II-VI (now Coherent Corp.) | 0000820318 | 3827 | 30 Jun | 1995-05-15 | 2019-03-31, 10-Q, filed 2019-05-09 | FY2019, FY2020 | mentions: read |
| MACOM | 0001493594 | 3674 | ~30 Sep | 2012-05-10 | 2019-03-29, 10-Q, filed 2019-05-08 | FY2018, FY2019, FY2020 | mentions: read |
| Micron | 0000723125 | 3674 | ~31 Aug | 1994-03-22 | 2019-02-28, 10-Q, filed 2019-03-21 | FY2019, FY2020 | mentions: read |
| Qualcomm | 0000804328 | 3663 | ~30 Sep | 1996-05-13 | 2019-03-31, 10-Q, filed 2019-05-01 | FY2018, FY2019, FY2020 | mentions: read |
| Broadcom Inc. | 0001730168 | 3674 | ~31 Oct | 2018-06-14 | 2019-05-05, 10-Q, filed 2019-06-14 | FY2019, FY2020 | mentions: read |
| Intel | 0000050863 | 3674 | ~31 Dec | 1994-03-25 | 2019-03-30, 10-Q, filed 2019-04-26 | only an exhibit (EX-99.1) to FY2017 | **not named** |
| Xilinx | 0000743988 | 3674 | ~31 Mar | 1996-06-27 | 2019-03-30, 10-K, filed 2019-05-10 | only FY2020 (Apr 2019–Mar 2020) | **not named** |

Origin = the last 10-K/10-Q period ending before 16 May 2019, from the SEC filing list. All 14 were filed 21–47 days after the period end, so within 65 days. The final check uses `first_filed_date` from the revenue data (pre-flight table, after Stage C).

**Points to decide or check (not decided here):**
- **Xilinx:** under the rule as written it is a donor, although its fiscal 2020 10-K (filed May 2020) mentions Huawei.
- **Qualcomm (3663), Lumentum (3669) and II-VI (3827)** are outside the proposed donor codes. That matters only if one of them is not named.
- **Possibly fewer than 20 quarters:** Acacia (first 10-Q Aug 2016), Lumentum (Sep 2015), Qorvo (Sep 2014, merger in 2015) and Broadcom Inc. (new SEC entity in 2018; its predecessor Broadcom Ltd may need joining, like Google/Alphabet in Project 2). Settled by the pre-flight table.

## Other firms with the donor codes (3674, 3672, 3677, 3678, 3679)

The industry lists hold **714 entries** (3674: 506, 3679: 113, 3672: 61, 3678: 29, 3677: 5; `sic_universe.csv`). They include firms that stopped filing long ago and some private individuals, and they carry no dates. **So the lists alone cannot say who filed a 10-K for fiscal 2018 or 2019.** That needs one more step (see the Stage B plan in PROGRESS.md).

- **685** listed entries have no Huawei mention in a fiscal 2018 or 2019 10-K: **not named** (if they filed one at all).
- **22 firms** with the donor codes mention Huawei in a fiscal 2018 or 2019 10-K. All need reading before they can be donors (`donor_code_mentions.csv`):

| Firm | SIC | Fiscal years with a mention |
|---|---|---|
| Ambarella | 3674 | 2019 |
| Applied Optoelectronics | 3674 | 2019 |
| CEVA | 3674 | 2018, 2019 |
| Cree | 3674 | 2019 |
| Cypress Semiconductor | 3674 | 2019 |
| DSP Group | 3674 | 2018, 2019 |
| Enphase Energy | 3674 | 2018, 2019 |
| Flex | 3672 | 2018 |
| MaxLinear | 3674 | 2018, 2019 |
| Mellanox | 3674 | 2019 |
| MoSys | 3674 | 2018, 2019 |
| NXP Semiconductors | 3674 | 2019 |
| Oclaro | 3674 | 2018 |
| ON Semiconductor | 3674 | 2019 |
| Pixelworks | 3674 | 2018, 2019 |
| Quantenna | 3674 | 2018 |
| Semtech | 3674 | 2018, 2019 |
| SiTime | 3674 | 2019 |
| SolarEdge | 3674 | 2018, 2019 |
| Synaptics | 3674 | 2018, 2019 |
| TTM Technologies | 3672 | 2018, 2019 |
| Xperi | 3674 | 2018, 2019 |

Two of the 22 (counted by CIK) are not in the downloaded industry lists, probably because their current SIC code differs from the one the search shows. Not yet checked.

Limit: the search matches the word "Huawei" only. A 10-K that names only "HiSilicon" (Huawei's chip unit) is not found.
