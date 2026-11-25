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
