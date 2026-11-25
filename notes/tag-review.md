# Data check and revenue-tag review for the 64 firms (25 Nov 2026)

Project 2's checks (`src/check_data.py`, functions unchanged), run by `src/check_ours.py` on **quarters up to each firm's origin only** (2,363 quarters), so that nothing about revenue after the event is seen. Only counts and quarter labels were printed. Full table: `results/check_ours.csv`. No forecast was run.

## Summary

- Firms with gaps: 6 (Micron, Lattice, Silicon Labs, SMTC, SunPower, Cypress). AutoETS uses the latest unbroken stretch; all have ≥ 12 (`results/eligibility_exact.csv`).
- Firms where quarters do not add up to the year (> 0.5 %) at least once: 22.
- Firms with first-reported vs latest revisions > 0.5 %: 32.
- Firms with quarters first filed more than 65 days after the quarter end: 56. These are mostly early comparison quarters and derived Q4s. Every **origin** passed the 65-day check.
- Firms with tag switches: 63. Expected: most moved to the new revenue standard's tag (ASC 606) in 2018.
- **Firms with tag conflicts: 13.**
- **Firms with jumps in the last 12 quarters before the origin: 16.**

## Tag conflicts (two tags first reported with values > 0.5 % apart; labels only)

| Firm | Group | Conflict quarters | Inside the last 12 quarters before the origin? |
|---|---|---|---|
| AMD | primary donor | 2017 Q1–Q4 | **yes** |
| Analog Devices | primary donor | 2018 Q1–Q4 | **yes** |
| Qorvo | primary exposed | 2015 Q1–Q2 | no |
| Diodes | primary donor | 2013 Q2, 2014 Q2 | no |
| Lattice | primary donor | 2011 Q2 | no |
| Xilinx | low exposure | 2018 Q1–Q4 | **yes** |
| Cree / Wolfspeed | low exposure | 2018 Q3–2019 Q3 | **yes (up to its origin)** |
| Cypress | low exposure | 2017 Q2–Q3 | **yes** |
| Plexus | sensitivity | 2019 Q1–Q2 | **yes (at its origin)** |
| Amkor, SMTC, SunPower | sensitivity | 2017 Q1–Q3 | **yes** |
| Benchmark | sensitivity | 2016 Q1 – 2017 Q3 (11 quarters) | **yes** |

## Jumps in the last 12 quarters before the origin (flagged, not dropped, as in Project 2)

- Primary exposed: Inphi 2018 Q1.
- Secondary exposed: Lumentum 2018 Q2.
- Primary donors: Microchip 2017 Q1, NVIDIA 2019 Q4.
- Low exposure: ON Semiconductor 2016 Q4, Cypress 2016 Q2, Applied Optoelectronics 2018 Q3, **Cree / Wolfspeed 2019 Q3 (its origin quarter)**.
- Sensitivity: Advanced Energy (5), CMC Materials, First Solar (7), FormFactor (2), IEC Electronics, Rambus, SMTC (2), SunPower (2).

## Proposed fix (not applied; Penelope decides)

For every conflict quarter **inside the last 12 quarters before the origin**, use the tag that equals the firm's **total** revenue (Project 2's rule). It is found inside the script by checking which tag's quarters add up to the 10-K full-year total. Only the chosen tag (a label) is reported. Then rebuild the table and rerun `src/eligibility_exact.py` and `src/check_ours.py`. No value is printed.

## Fix applied (approved by Penelope, 25 Nov 2026): result, no change needed

`src/tag_fix.py` → `results/tag_fix.csv` (labels and counts only). For each conflict quarter in the last 12 quarters before the origin it checks whether the two tags differ **inside the earliest filing** of that quarter (the only case where the tag order changes the first-reported value).

- **AMD, Analog Devices, Xilinx, Cree/Wolfspeed, Cypress, Amkor, SMTC, SunPower:** later restatements only. The earliest filing held one tag; a later filing restated the quarter under another tag. The first-reported series is unaffected.
- **Plexus (2019 Q1–Q2) and Benchmark (2018 Q1–Q3, 2019 Q1):** same-filing conflicts. The current order already picks the contract-revenue tag (EX), which is the **larger (total)** value in every filing before the origin where both tags appear (4 of 4; 11 of 11).
- **So the total-revenue rule changes nothing:** the tag order in `src/build_quarterly.py` stands as confirmed; no rebuild was needed.
