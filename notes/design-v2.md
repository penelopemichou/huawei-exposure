# Design v2 (25 Nov 2026)

Design v1 is the "Design" section of PROGRESS.md (fixed on 24 Nov 2026). This note lists the only changes from v1.

**Reason for every change: made before any forecast; driven by data availability, not results.** No forecast has been run and no miss has been opened. What was known when this was written: filing lists, Huawei shares from the 10-Ks, and the fact that Finisar stops reporting after the quarter ended July 2019 (so only h = 1 exists for it). At h = 2–4 the primary exposed group may fall to 3 or 4 firms.

## (a) Horizons

- **Primary horizon: h = 1.**
- h = 1, 2, 3 and 4 are **all computed**.
- **h = 2 and h = 3** are reported per horizon, as **secondary** results.
- **h = 4 is flagged "COVID"**: for most origins (early 2019) the h = 4 target falls in late 2019 or early 2020, close to the start of the pandemic.
- Unchanged from v1: B4 and AutoETS, the 65-day rule, the origin rule (each firm's last fiscal quarter ending before 16 May 2019), and the signed miss in %.

## (b) The primary test

- **Primary test: exposed firms vs donors at h = 1**, with a **permutation p-value**: shuffle the exposed/donor labels across the firms in the primary comparison many times, and see how often the shuffled gap is at least as large as the real one.
- **Dose-response among the exposed firms is descriptive only**: show each firm's miss next to its Huawei dose, with no test.
- Unchanged from v1: descriptive, no causal claim; "low exposure, implied" firms are not in the primary test (shown in their own rows).
- Details of the permutation (statistic, number of shuffles, one- or two-sided) are fixed in a dated note **before** any forecast is run.

## (c) Stitching rule (joining a predecessor's history)

- **Join a predecessor's history only when the same business continues under a new SEC ID**: the predecessor is the **accounting acquirer**, as with Google Inc. → Alphabet Inc. in Project 2.
- **Never after a spin-off or carve-out.** For example, a business carved out of a larger company is not joined to that company's history.
- Not yet applied to any firm. Each case is checked and shown before it is used.
- **Qorvo** (checked 25 Nov 2026): its own file already holds the accounting acquirer's (RF Micro Devices') quarters, 24 in all, so no stitching is needed.
- **Broadcom** (checked 25 Nov 2026, Stage C2; **stitching approved by Penelope on 25 Nov 2026**; spec in `results/stitching.csv`):
  - Proposed chain: Avago Technologies (CIK 0001441634, quarters 2010-01 to 2015-11) → Broadcom Ltd (CIK 0001649338, now "Broadcom Pte. Ltd.", 2015-02 to 2018-02) → Broadcom Inc. (CIK 0001730168, from 2017-01).
  - Evidence: the same fiscal calendar (years ending about 1 November), and all 9 overlapping quarters (4 + 5) have **identical first-reported values**. Broadcom Corp (CIK 0001054374), the company bought in 2016, is never joined.
  - Stitched (newest file wins where they overlap): 38 quarters from 2010-01-31 to the origin, no gaps. Unstitched: 10, which fails the 20-quarter rule.
  - Caveats, **shown as flags next to Broadcom's results**: a level jump in Feb 2016 (Broadcom Corp added) and, from memory, another in Nov 2018 (CA Technologies added) just before the origin, like Lumentum–Oclaro. Broadcom stays in the low-exposure rows; it is not in the primary test.

## (d) Lumentum goes to SECONDARY (decided by Penelope, 25 Nov 2026)

Two reasons, both about the data, not the results:

1. **Only about 14–15 quarters after the spin-off** (Aug 2015) before the origin. The other 9 quarters in its file are carve-out figures from the time it was part of JDS Uniphase. Under rule (c), history from before a spin-off or carve-out is not used, so Lumentum fails the 20-quarter rule.
2. **A level jump just before the origin:** Lumentum bought Oclaro in Dec 2018, so its revenue base changes in the last quarters before the origin.

Lumentum is still forecast and shown, labelled SECONDARY. **Primary exposed group: 5 firms at h = 1** (NeoPhotonics, Inphi, Qorvo, Micron, Finisar) **and 4 at h = 2–4** (Finisar stops reporting after July 2019).

## (e) Secondary descriptive check: three groups (added 25 Nov 2026)

- Three groups: **exposed** (Huawei 10 %+), **low exposure** (Huawei named as a customer, no share given), **donors**.
- **What "exposure matters" would look like:** the low-exposure firms' misses sit **between** the exposed firms' and the donors' (exposed most negative, then low exposure, then donors).
- Descriptive only: no test, shown per horizon and per rule, with every firm's own miss visible.
- It does not change the primary test in (b).
- **After amendment 1 (25 Nov 2026), the low-exposure group has 16 firms**: the 4 from B1 plus 12 chip/optical makers from B2. Four of them name Huawei only in a FY2020 10-K and are shown flagged.

## (f) Primary donors = chip and optical-component makers only (decided by Penelope, 25 Nov 2026)

Reason: most donors were "analog/other" while most exposed firms are optical/datacom (`results/sub_sector_tags.csv`); found before any forecast.

- **Primary donors:** donors classed **chip** or **optical-component** maker.
- **Sensitivity group:** donors classed **contract manufacturer**, **solar** or **equipment** maker. They are still forecast and shown, but are **not in the primary test**.
- The class of every firm is set in a table (`results/firm_classes.csv`), approved by Penelope before the lists are frozen.
- **Limit:** even with this rule, the optical/datacom vs other mismatch cannot be separated from Huawei exposure (README).

## (g) Secondary outcome: the miss scaled by the firm's own usual miss (added 25 Nov 2026)

- **Scaled miss = signed miss ÷ the firm's own median absolute pre-event miss**, same rule and same horizon.
- **Pre-event misses:** the firm's own rolling-origin forecasts whose target quarter is **on or before its origin quarter**. Same code, same 65-day rule, same 20-quarter start (as forecast-gap's "own pre-event misses").
- Shown per firm and per rule (B4, AutoETS, and their average), **with the number of pre-event forecasts per firm**. A firm with few pre-event forecasts has a less reliable scale; this is shown, not hidden.
- Descriptive, secondary; it does not replace the primary test in (b).
