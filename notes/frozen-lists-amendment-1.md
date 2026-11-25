# Amendment 1 to the frozen lists — APPROVED on 25 Nov 2026 (before any forecast)

**Reason: placement gap found before any forecast; no outcome seen.** No forecast has been run and no miss has been opened (freeze commit `adb3a8b`).

Firms from Stages B2a, B2b and B2c whose 10-K names Huawei as a customer, or as an indirect sales channel, with no 10 %+ share, had **no group** in the frozen file. They were only listed in `results/dropped_donors.csv` as "not a donor" or "moved out by a later filing" (SiTime, NXP, CEVA and Xperi were not even listed there). Only the B1 firms of that type (MACOM, Skyworks, Broadcom, Qualcomm) had a group, "low exposure, implied".

## Proposed rule

1. **Chip or optical-component makers** of that type that pass the **history and h = 1 checks** are added to the **LOW-EXPOSURE** group. They get their own rows and are in the three-group check (design-v2 (e)), **not in the primary test**.
2. **Contract manufacturers, equipment makers and others** with a named-customer or indirect label are **listed, not compared**.
3. Chip makers of that type that **fail** the history or h = 1 checks are **listed, not compared**, with the reason.
4. Unchanged: "unclear = out of donors" (Mellanox, Kulicke & Soffa) and the primary test (5 exposed vs 14 primary donors).

## Proposed names

Class basis: "10-K read" = the opening of Item 1 in the 10-K already on disk; "name" = SIC 3674 plus the company name, where Item 1 opens with history only. Checks: `results/donor_screen.csv` (first 10-K/10-Q filed by 2014, origin filed within 65 days, h = 1 quarter reported). **"pass?" = older filings exist but were not downloaded; the exact 20-quarter count needs the firm's revenue file (not downloaded).**

### Add to LOW EXPOSURE (12)

| Firm | Class | Basis | Huawei label | Huawei named in | History | Origin, h = 1 |
|---|---|---|---|---|---|---|
| ON Semiconductor | chip | name | customer without % | FY2019 10-K | pass (exact) | pass |
| MaxLinear | chip | 10-K read | customer without % | FY2018/19 10-K | pass (exact) | pass |
| Semtech | chip | 10-K read | customer without % | FY2018/19 10-K | pass (exact) | pass |
| Synaptics | chip | 10-K read | customer without % | FY2018/19 10-K | pass (exact) | pass |
| Cypress | chip | 10-K read | customer without % | FY2019 10-K | pass (exact) | pass |
| DSP Group | chip | 10-K read | customer without % | FY2018/19 10-K | pass (exact) | pass |
| Applied Optoelectronics | optical-component | 10-K read | customer without % | FY2019 10-K | pass (exact) | pass |
| Cree/Wolfspeed | chip | 10-K read | customer without % | FY2019 10-K | pass (exact) | pass |
| Marvell | chip | 10-K read | customer without % | **FY2020 10-K only** | pass (exact) | pass |
| Cirrus Logic | chip | 10-K read | customer without % | **FY2020 10-K only** | pass (exact) | pass |
| Alpha & Omega | chip | 10-K read | **indirect** (~2 % of FY2019 revenue) | **FY2020 10-K only** | pass (exact) | pass |
| Xilinx | chip | 10-K read | customer without % | **FY2020 10-K only** | pass (exact) | pass |

**Decided by Penelope (25 Nov 2026): all 12 join**, including Marvell, Cirrus Logic, Alpha & Omega and Xilinx, which name Huawei **only in a 10-K filed after the event** (FY2020). For these four the low-exposure definition is extended to later filings; they are flagged "FY2020 10-K only" wherever they are shown.

### Listed, not compared (7)

| Firm | Class | Basis | Huawei label | Reason |
|---|---|---|---|---|
| Flex | contract manufacturer | 10-K read | customer without % | class not chip/optical |
| TTM Technologies | other (printed circuit boards) | 10-K read | customer without % | class not chip/optical |
| Applied Materials | equipment | 10-K read | indirect (FY2020) | class not chip/optical |
| CEVA | other (licensing) | 10-K read | customer without % (licensee) | class not chip/optical |
| Xperi | other (licensing) | 10-K Huawei rows ("licensed to … Huawei") | customer without % | class not chip/optical |
| NXP | chip | 10-K read | customer without % | fails history and origin (20-F filer until 2019) |
| SiTime | chip | 10-K read | indirect | fails history (listed Nov 2019, from memory; not screened, revenue < $100M) |

## Exact eligibility of the 12 (25 Nov 2026, Penelope's "yes" for their revenue files)

- 12 revenue files, 40.1 MB (limits 10 MB per file, 60 MB in total).
- Checked with Project 2's own functions, imported read-only (`src/eligibility_exact.py amend`, `results/eligibility_exact_amendment1.csv`; counts and dates only).
- **All 12 pass:** 20 quarters (`first_origin`), origin filed by the cutoff (`known_at`), an h = 1 quarter, and at least 12 unbroken quarters for AutoETS.
- Notes: Cypress has no h = 4 quarter (bought by Infineon in 2020) and only 13 unbroken quarters. For Cree/Wolfspeed, `prepare()` dropped 9 full-year values that differ more than 25 % from the first 10-K figure (values not shown).

## Approved

**Approved on 25 Nov 2026** by Penelope ("Yes, all 12 join"), before any forecast was run; last commit before approval `adb3a8b`. No outcome was seen.

- Low exposure is now **16 firms**: the 4 of the frozen lists plus these 12.
- **Unchanged:** the primary test (5 exposed vs 14 primary donors, `notes/permutation-setup.md`), the donors, the sensitivity group and the exposed firms.
