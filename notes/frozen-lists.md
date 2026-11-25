# Frozen lists — DRAFT (prepared 25 Nov 2026; NOT frozen)

**Status: DRAFT.** These lists become frozen only when Penelope writes "frozen" with a date below, **before** any forecast is run. After freezing, no firm is added, removed or moved between groups.

Rules: `notes/donor-rule.md` (label test, groups, dose), `notes/design-v2.md` (h = 1 primary, Lumentum SECONDARY, stitching rule). Evidence per firm: `results/dropped_donors.csv`, `results/donor_screen.csv`, `notes/decision-rows.md`. Sub-sector tags: `results/sub_sector_tags.csv`.

## Exposed (Huawei named at 10 %+ in the FY2018 or FY2019 10-K)

| Firm | Dose | Comparison | Horizons |
|---|---|---|---|
| NeoPhotonics | 46 % | PRIMARY | h = 1–4 |
| Inphi | 14 % | PRIMARY | h = 1–4 |
| Qorvo | 13 % | PRIMARY | h = 1–4 |
| Micron | 12 % (fallback, flagged) | PRIMARY | h = 1–4 |
| Finisar | 10 % | PRIMARY | **h = 1 only** |
| Lumentum | 11.0 % | **SECONDARY** (design-v2 (d)) | h = 1–4 |

Primary exposed: 5 at h = 1, 4 at h = 2–4. Oclaro (11 %) is exposed by the rule but has no quarter after 16 May 2019: listed, not compared.

## Low exposure, implied (own rows; not in the primary test)

MACOM, Skyworks, Broadcom (stitched; level jumps flagged), Qualcomm (royalty income, not product sales).

## Donors (42): split by class (design-v2 (f)); `results/firm_classes.csv`, **class table confirmed by Penelope on 25 Nov 2026**

- **PRIMARY (chip makers, 14):** Intel, Ambarella, Microchip, AMD, Analog Devices, Diodes, Lattice, MagnaChip, Maxim, Monolithic Power, NVIDIA, Power Integrations, Silicon Labs, Texas Instruments. No optical-component donor is confirmed yet.
- **Sensitivity (28; forecast, not in the primary test):**
  - contract manufacturers (10): Amkor, Benchmark, IEC, Jabil, Key Tronic, Kimball, Nortech, Plexus, Sanmina, SMTC;
  - equipment and materials (6): Advanced Energy, AXT, CMC Materials, FormFactor, Photronics, Ultra Clean;
  - solar (3): Enphase, First Solar, SunPower;
  - other (6): Amphenol, Bel Fuse, CTS, Methode, Vicor, Rambus (mainly patent licensing: royalties 56 % of 2018 revenue);
  - sensitivity from rules, system/instrument or unclear (3): IPG Photonics, Viavi (10-K read, Stage E), OSI Systems (no 10-K read).

## Not donors: unclear = out (standing rule)

Mellanox, Kulicke & Soffa.

## Still to do BEFORE these lists can be frozen

1. ~~**Criterion 3 for 13 donors is "pass?"**~~ **Done 25 Nov 2026:** all 13 pass (earliest revenue value filed 2009–2012). Was: (first 10-K/10-Q filed by 2014, not yet confirmed): AMD, Ambarella, Analog Devices, Diodes, IPG Photonics, Jabil, Microchip, OSI Systems, Plexus, Power Integrations, Texas Instruments, Viavi, Vicor.
2. ~~**Pre-flight for all 42 donors and the 4 low-exposure firms**~~ **Done 25 Nov 2026** (Stage C, `results/quarter_counts_all.csv`): all 42 donors pass the 20-quarter rule and have h = 1–4; MACOM, Skyworks and Qualcomm pass; **Broadcom fails (10 quarters from Jan 2017)**; **stitched** Avago → Broadcom Ltd → Broadcom Inc. (approved by Penelope 25 Nov 2026; 9/9 overlaps identical; 38 quarters, passes; level jumps Feb 2016 and Nov 2018 flagged). Was: Pre-flight (20 quarters, origin filed by the cutoff, h = 1 target reported), from their revenue files (one request each, about 46; needs a "yes"). Broadcom Inc. is a new SEC entity (2018); its predecessor may qualify for stitching under design-v2 (c), to check.
3. ~~Penelope's confirmation of the class table~~ (done 25 Nov 2026) (`results/firm_classes.csv`; 21 of 52 rows rest on memory after Stage E). Decided 25 Nov 2026: "other" and system/instrument or unclear classes go to sensitivity; Stage D not downloaded.
4. ~~**Sub-sector mismatch (to discuss before freezing):**~~ **Handled 25 Nov 2026:** design-v2 (f) (primary donors are chip makers only) and a README limit. Was: 4 of the 6 exposed firms are optical/datacom; 40 of the 42 donors are "analog/other" (15 of them contract manufacturers, solar or equipment makers). See `results/sub_sector_tags.csv`.

## Frozen

(empty: Penelope writes "frozen on <date>" here)
