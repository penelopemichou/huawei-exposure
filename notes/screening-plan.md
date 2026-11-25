# Screening plan: which US suppliers disclosed Huawei exposure?

Written on 24 Nov 2026 (Session 1), before any SEC file was downloaded and before any forecast.

## What goes in the table

- **Huawei % of revenue by year:** copied exactly as written in the 10-K (for example "approximately 15%"), with the fiscal year it refers to. No rounding, no guessing.
- **Filing and section:** form, fiscal year, filing date and the section where the number is (for example "10-K FY2019, filed 2019-05-xx, Note 15 Segment and geographic information" or "Item 1, Customers").
- **Origin quarter:** the firm's **last fiscal quarter ending before 16 May 2019**. The exact end date comes from the SEC data in Session 2. The dates below are from memory until then.
- **Source:** where the pre-filled number came from *before* checking: "Penelope's notes", "news" or "from memory".
- **Verified?:** "to verify" until the number has been read in the 10-K itself, then "yes (date)". A number found only in a 10-Q or the news stays "not in 10-K".

## Verified from the 10-Ks (Stage B1, 25 Nov 2026)

Group and dose rules: `donor-rule.md` ("Exposure group and dose"). Dose = Huawei's share in the latest fiscal year that ended before 16 May 2019; "fallback, flagged" if that year gives no %. Rows in `results/huawei_sentences.csv`.

| Firm | Latest FY ended before 16 May 2019 | Huawei % as written (FY2018 / FY2019 10-K) | Filing and section of the dose | Group | Dose | Verified? |
|---|---|---|---|---|---|---|
| NeoPhotonics | FY2018 (Dec 2018) | 46 % / 41 % (incl. HiSilicon) | 10-K FY2018, Item 1A (row 228) | exposed | **46 %** | yes (25 Nov 2026) |
| Inphi | FY2018 (Dec 2018) | "approximately … 14%" / "approximately … 11%" | 10-K FY2018 (row 68; section heading not found by the extractor) | exposed | **14 %** | yes (25 Nov 2026) |
| Lumentum | FY2018 (Jun 2018) | 11.0 % / 15.2 % | 10-K FY2018, Item 1 table (row 117) | exposed | **11.0 %** | yes (25 Nov 2026) |
| Qorvo | FY2019 (Mar 2019) | 8 % / 13 % | 10-K FY2019, Item 1 (row 364) | exposed | **13 %** | yes (25 Nov 2026) |
| Finisar | FY2019 (Apr 2019) | not given (below 10 %) / 10 % | 10-K FY2019, Item 8 (row 60) | exposed | **10 %** | yes (25 Nov 2026) |
| Micron | FY2018 (Aug 2018) | not given / 12 % (FY2019) | 10-K FY2019, Item 8 (row 214) | exposed | **12 %, fallback, flagged** | yes (25 Nov 2026) |
| MACOM | FY2018 (Sep 2018) | named, no % | n/a | low exposure, implied | n/a | yes (25 Nov 2026) |
| Skyworks | FY2018 (Sep 2018) | named, no % ("about 12 % of H1 FY2019": not in the 10-K; maybe a 10-Q, Stage B3) | n/a | low exposure, implied | n/a | yes (25 Nov 2026) |
| Broadcom | FY2018 (Nov 2018) | not named as customer / named, no % | n/a | low exposure, implied | n/a | yes (25 Nov 2026) |
| Qualcomm | FY2018 (Sep 2018) | licensee, $600 million / $450 million royalties (royalty income, not product sales) | n/a | low exposure, implied | n/a | yes (25 Nov 2026) |

The pre-filled tables below are kept as they were written. Where they differ from this table, this table holds (for example Qorvo: 13 %, not "about 15 %").

## Table 1: firms with a known Huawei number (to verify)

| Company | Fiscal year end | Huawei % of revenue by year (as written in the 10-K) | Filing and section | Origin quarter | Source | Verified? |
|---|---|---|---|---|---|---|
| Qorvo | Saturday nearest 31 Mar (from memory) | FY2019: about 15 % | | Q4 FY2019, ended about 30 Mar 2019 (from memory) | Penelope's notes | to verify |
| NeoPhotonics | 31 Dec (from memory) | 2018: 46 %; 2019: 41 % | | Q1 2019, ended 31 Mar 2019 (from memory) | Penelope's notes | to verify |
| Lumentum | Saturday nearest 30 Jun (from memory) | FY2018: 11 % | | Q3 FY2019, ended about 30 Mar 2019 (from memory) | Penelope's notes | to verify |
| Skyworks | Friday nearest 30 Sep (from memory) | H1 FY2019: about 12 % (a half year, so probably a 10-Q or a news figure; check the FY2019 10-K for the full year) | | Q2 FY2019, ended about 29 Mar 2019 (from memory) | Penelope's notes | to verify |
| Inphi | 31 Dec (from memory) | 2018: 14 % | | Q1 2019, ended 31 Mar 2019 (from memory) | news only | to verify |

## Table 2: candidates to screen (names from memory)

Every row here is **from memory**: the name, the fiscal year end and the notes. Nothing is known about Huawei's share until the 10-K is read. A candidate whose 10-K does not name Huawei as a 10 %+ customer in 2018 or 2019 becomes a possible donor (see `donor-rule.md`).

| Company | Fiscal year end | Huawei % of revenue by year (as written in the 10-K) | Filing and section | Origin quarter | Source | Verified? |
|---|---|---|---|---|---|---|
| Acacia Communications | 31 Dec (from memory) | | | Q1 2019 (from memory) | from memory | to verify |
| Finisar | Sunday nearest 30 Apr (from memory) | | | Q4 FY2019, ended about 28 Apr 2019 (from memory) | from memory | to verify |
| II-VI | 30 Jun (from memory) | | | Q3 FY2019, ended about 31 Mar 2019 (from memory) | from memory | to verify |
| MACOM | Friday nearest 30 Sep (from memory) | | | Q2 FY2019, ended about 29 Mar 2019 (from memory) | from memory | to verify |
| Xilinx | Saturday nearest 31 Mar (from memory) | | | Q4 FY2019, ended about 30 Mar 2019 (from memory) | from memory | to verify |
| Micron | Thursday nearest 31 Aug (from memory) | | | Q2 FY2019, ended about 28 Feb 2019 (from memory) | from memory | to verify |
| Intel | last Saturday of Dec (from memory) | | | Q1 2019, ended about 30 Mar 2019 (from memory) | from memory | to verify |
| Qualcomm | last Sunday of Sep (from memory) | | | Q2 FY2019, ended about 31 Mar 2019 (from memory) | from memory | to verify |
| Broadcom | Sunday nearest 31 Oct (from memory) | | | Q2 FY2019, ended about 5 May 2019 (from memory) | from memory | to verify |

## Primary and secondary comparison (decided 24 Nov 2026, before any download or forecast)

The copied code does **not** check these two conditions at a single origin: `first_origin` only starts the rolling loops, and `known_at` silently leaves out a quarter filed too late. So the pre-flight eligibility table (see PROGRESS.md, Session 2 plan) checks them for every firm, exposed or donor, before any forecast.

A firm goes into the **PRIMARY** comparison only if both hold:

1. **At least 20 quarters before the origin:** its revenue table starts at or before origin − 19 quarters (for an origin of fiscal 2019 Q1: 2014 Q2 or earlier). This is Project 2's 20-quarter rule (`first_origin` in `src/baselines.py`).
2. **Origin quarter known at the cutoff:** the origin quarter's `first_filed_date` is on or before the end of that quarter + 65 days. This is Project 2's 65-day rule (`cutoff_date` and `known_at` in `src/baselines.py`).

A firm that fails either condition is **excluded from the PRIMARY comparison** and listed in a separate **SECONDARY** table, with the reason. Secondary firms are forecast later with the same code and are always labelled "secondary". They never enter the primary result.

**Stop rule:** if the PRIMARY exposed group would have **fewer than 4 firms**, Penelope is told before Session 3, before any forecast.

## Things to check for each firm (from memory, to verify in Session 2)

- **History before the origin.** Two firms may be too young for condition 1 (from memory): Acacia listed in 2016, and Lumentum was spun off in 2015. If so, they go to the SECONDARY table. AutoETS also needs at least 12 unbroken known quarters.
- **Origin quarter filed late.** Smaller filers have up to 45 days for a 10-Q and 75–90 days for a 10-K. If the origin quarter was first filed after the 65-day cutoff, the firm goes to the SECONDARY table (condition 2).
- **Enough data after the origin.** h = 1–4 needs four reported quarters after the origin. Finisar was bought by II-VI in late 2019, so it may have only h = 1. Acacia, Inphi, NeoPhotonics and Xilinx were bought later (2021–2022), which should be late enough. Record any missing horizon; don't fill it in.
- **Origin quarter published after 16 May 2019.** Broadcom (quarter ending about 5 May) and Finisar (about 28 Apr) reported that quarter in June 2019. If it was filed within the 65-day cutoff, the rule allows it, and the revenue in that quarter is still from before 16 May. Note it next to the result.
- **Which revenue tag.** Each new firm needs its total-revenue XBRL tag chosen by the same rule as in Project 2 (one line per firm in `build_quarterly.py`).

## Not used

- Analyst reports, paid databases, anything that is not a public SEC filing. News is used only to know *where to look*. A number counts only once it is read in the 10-K.
