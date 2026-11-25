# Stage B1 results (25 Nov 2026): proposed groups, waiting for Penelope

31 documents, 97.6 MB, 31 requests (`data/raw/stage_b/request_log.csv`). No file over 20 MB (largest 6.4 MB), total under 100 MB. 434 rows extracted (`results/huawei_sentences.csv`); every row with its proposed label in `notes/stage-b1-labels.md`. 41 labels were changed by hand after reading; 6 rows are **unclear** (listed below, not guessed).

## Proposed groups for the 14 firms

| Firm | What the 10-K says (FY2018 / FY2019) | Proposed group |
|---|---|---|
| NeoPhotonics | Huawei incl. HiSilicon 46 % / 41 % | **exposed** |
| Inphi | about 14 % / about 11 % ("directly and indirectly, through subcontractors") | **exposed** |
| Lumentum | 11.0 % / 15.2 % | **exposed** |
| Qorvo | 8 % / 13 % | **exposed** (via FY2019) |
| Micron | no Huawei mention / 12 % | **exposed** (via FY2019) |
| Finisar | below 10 % (only Cisco and Google named) / 10 % | **exposed** (via FY2019) |
| MACOM | named as a customer; "no direct customer ≥ 10 %" in both years (Huawei 10 % in FY2017) | low exposure, implied: decide |
| Skyworks | named as a key customer; only Apple ≥ 10 % in both years (Huawei 10 % in FY2017) | low exposure, implied: decide |
| Broadcom | FY2018 HiSilicon only as competitor / FY2019 "Huawei …, one of our customers" | low exposure, implied: decide |
| Qualcomm | Huawei a royalty licensee: $600 million (FY2018), $450 million (FY2019); no % | low exposure, implied: decide |
| Intel | no Huawei mention in either year | **not named → donor** (criteria 1–5 pass; final check in the pre-flight table) |
| II-VI | one general Entity List mention | not named; not a donor (SIC 3827) |
| Acacia | competitor and general mentions only; unnamed customers A, B, C, E | not named; not a donor (first 10-Q in 2016) |
| Xilinx | FY2018/FY2019 nothing / FY2020: "unable to sell certain products to Huawei" | **moved out of the donor group by a later filing** |

"Low exposure, implied": the 10-K names Huawei as a customer, and the < 10 % comes only from the statement that no *other* customer reached 10 %. The rule's "low exposure" says "a share below 10 %". So these four are either **low exposure** or just **out of the donor group**. Penelope's call.

**Pre-filled numbers checked against the 10-Ks:**
- Qorvo FY2019 = **13 %**, not "about 15 %".
- NeoPhotonics 46 % / 41 %: confirmed.
- Lumentum FY2018 11 %: confirmed.
- Inphi 2018 14 %: confirmed in the 10-K (no longer "news only").
- Skyworks "about 12 % of H1 FY2019": not in either 10-K nor in the March 2019 10-Q: **unsourced, not used**.

## Count of primary exposed firms: warning

6 exposed firms. Two may go to the SECONDARY table in the pre-flight check: **Lumentum** (first 10-Q in 2015) and **Qorvo** (first filing in 2014, merger in 2015). If both do, the primary exposed group is **exactly 4** (Finisar, Inphi, Micron, NeoPhotonics). That is at the stop line, not under it. Finisar was bought in late 2019, so it may have only h = 1.

## Unclear rows (Penelope decides; none of them changes a group)

| Row | Firm | Sentence |
|---|---|---|
| 211 | Micron FY2019 | "We are unable to predict the duration of the export restrictions imposed with respect to Huawei, whether any licenses will be issued, or the long-term effects on our business." |
| 276 (and 332, 10-K/A) | NeoPhotonics FY2019 | "This trend may accelerate as a result of the current Huawei listing on the Entity List and U.S.-China trade tensions." |
| 366 | Qorvo FY2019 | "… unable to predict the scope and duration of the export restrictions imposed on Huawei and the corresponding future effects on our business." |
| 379 | Qorvo FY2019 | "… unable to predict the scope or duration of the new EAR restrictions on Huawei or the impact to the Company's business …" |
| 398 | Qualcomm FY2019 | "… partially offset by a decline in unit demand and a shift in OEM share towards Huawei" |

All five firms are already placed by other, clear rows.

## Unnamed 10 %+ customers ("Customer A" table)

| Firm | What the 10-K says | Identity given elsewhere in the 10-K? |
|---|---|---|
| Acacia | Customers A, B, C, E with 13–30 % of revenue (2016–2019). A was under US restrictions 15 Apr–13 Jul 2018. | **No** |
| Inphi | "Customer A is a subcontractor of a direct customer that would be a 'Customer F'" (notes) | Partly: Microsoft, Huawei and Cisco are named as end customers |
| Lumentum | Customers A–D in the notes | Yes: the same percentages in the named table in Item 1 (B = Huawei) |

## Dropped-donor list

`results/dropped_donors.csv`: one line per firm with the criterion and the row.

## B2a, B2c and B3 (25 Nov 2026)

Downloads: B2a + B2c 34 documents, **119.0 MB** (limit 120 MB; largest 8.3 MB, Xperi FY2019). B3 1 document, 1.0 MB. Rows: `results/huawei_sentences_B2a.csv` (160), `results/huawei_sentences_B2c.csv` (156), `results/huawei_sentences_B3.csv` (0). Hand corrections are in `src/label_sentences.py` (`STAGE_OVERRIDES`).

**B2a (can decide donors):**

| Firm | Huawei in FY2018/19 10-K | Result |
|---|---|---|
| Enphase | only as an inverter competitor | **donor** (no later hit) |
| Mellanox | only in a list of processor vendors | **donor** (no later hit) |
| Ambarella | only HiSilicon, as a competitor | passes FY2018/19; **waits for B2b** (later hit) |
| Oclaro | **Huawei 11 % of FY2018 revenue** (15 % FY2017, 21 % FY2016) | **exposed by the rule, but no quarter after 16 May 2019** (bought by Lumentum, Dec 2018): no comparison possible |
| Applied Optoelectronics, Cree/Wolfspeed, Cypress, DSP Group, Flex, MaxLinear, ON Semiconductor, Semtech, Synaptics, TTM | named as a customer, no % | out of the donor group (`results/dropped_donors.csv`) |

**B2c (exposure only; these firms fail the donor filter anyway):** no firm gives Huawei a %, so **no new exposed firm**.
- Customer without %: CEVA (licensee), NXP (top-10 OEM end customer), Xperi (licensee, "a current customer").
- Indirect: **SiTime** ("no direct sales with Huawei … a small amount of revenue attributable to Huawei" via distributors).
- Competitor/other only: MoSys, Pixelworks, Quantenna, SolarEdge (patent lawsuits with Huawei).

**B3 (Skyworks 10-Q, quarter ended 29 Mar 2019):** 0 mentions of Huawei or HiSilicon, and no 10 %-customer paragraph. **"About 12 % of H1 FY2019" is not in this 10-Q either.** **Unsourced, not used.**

**Data check added to the donor screen:** the h = 1 target quarter must end after 16 May 2019 and be reported. Oclaro and Sparton fail it, so **39** firms pass criteria 1–4 with no Huawei hit (was 40).

**Donors so far: 41** (39 with no hit + Enphase + Mellanox). Up to 7 more after B2b: Ambarella, Alpha & Omega, Applied Materials, Cirrus Logic, Kulicke & Soffa, Marvell, Microchip. Criterion 3 is "pass?" for some; it is confirmed from the revenue files.

## Revenue files: quarter counts (25 Nov 2026; counts and dates only, no values)

`src/count_quarters.py` → `results/quarter_counts.csv`. Simplified count (Project 2's tags; 3-month values plus derived Q4). The exact table comes from the copied Project 2 code later.

| Firm | First quarter | Quarters to the origin (span) | Last quarter | Quarters h = 1–4 |
|---|---|---|---|---|
| NeoPhotonics | 2010-06-30 | 36 (1 gap) | 2022-06-30 | 4 |
| Inphi | 2010-06-30 | 36 (1 gap) | 2020-12-31 | 4 |
| Lumentum | 2013-09-28 | 23 | 2026-09-26 | 4 |
| Qorvo | 2013-06-29 | 24 | 2026-03-28 | 4 |
| Micron | 2008-12-04 | 42 (3 gaps) | 2026-09-03 | 4 |
| Finisar | 2010-08-01 | 36 | **2019-07-28** | **1** |
| Intel | 2008-06-28 | 44 (1 gap) | 2026-09-26 | 4 |

**Qorvo (stitching check, design v2 (c)):**
- Its own file already holds 9 pre-merger quarters (first filed from Sep 2014), with full years ending in **March** 2013, 2014 and 2015. That is RF Micro Devices' fiscal calendar; TriQuint's year ended in December. So these are RF Micro Devices' history (accounting acquirer, from memory; the 10-K text is not downloaded).
- **Qorvo would qualify for stitching under (c), but does not need it:** 24 quarters without it. Joining RF Micro Devices' own SEC file would add roughly 2009–2013 (about 40 quarters in all; estimate, file not downloaded).

**Lumentum (decision for Penelope):**
- 9 of its 23 quarters are **before the Aug 2015 spin-off** (full years to June 2013, 2014, 2015). They were first filed by Lumentum itself in Sep/Nov 2015, as carve-out figures.
- This is not joining another company's file, but it is carve-out history, which rule (c) excludes.
- Counted: 23 → PRIMARY. Not counted: about 14–15 → SECONDARY.
- **Flag:** Lumentum bought Oclaro in Dec 2018, so its revenue level jumps just before the origin.

**Primary exposed group:** at h = 1, 6 firms (5 without Lumentum); at h = 2–4, 5 (4 without Lumentum). It does not fall below 4.

## Still to do (not started)

- B2 (34 documents, 22 firms): needs its own "yes".
- **New under the label test:** donor-code firms whose only "Huawei" hit is in a **later** 10-K (filed up to 31 Dec 2020) must be read too. They are not in the B2 list yet.
- Next step after A2: filing lists for the 80 firms with ≥ $100 million of 2018 revenue (about 80–100 requests).
