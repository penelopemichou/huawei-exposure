# huawei-exposure

Did US chip and electronic-component suppliers with more disclosed Huawei exposure miss simple revenue forecasts by more after Huawei was added to the US Entity List (16 May 2019) than suppliers with none?

**Descriptive only.** This project can say how large the gap was. It cannot say why: 2019 was also a chip downturn, and US–China tariffs hit at the same time.

- **Data:** public SEC filings only (EDGAR filing lists, full-text search, XBRL revenue data, 10-K documents).
- **Forecast rules:** two simple rules reused unchanged from an earlier project (B4 and AutoETS), with a 65-day data-availability rule.
- **Design:** `PROGRESS.md` (v1) and `notes/design-v2.md` (changes made before any forecast).
- **Who counts as exposed or as a donor:** `notes/donor-rule.md`.

## Results

**Headline.** After Huawei was added to the US Entity List on 16 May 2019, the five suppliers that had reported Huawei as a 10 %+ customer saw their next-quarter revenue come in, on average, about 6 percentage points further below two simple forecasts than the 14 chip makers that did not mention Huawei. A gap this size turns up often by chance with so few firms (one-sided p = 0.22). It rests mostly on Micron, whose 2019 shortfall came at the same time as a fall in memory-chip prices. Without Micron, the other four exposed firms show almost no gap (post-hoc arithmetic from the printed ranks, not run in code: rank-sum 36 against an expected 38). Firms that named Huawei as a customer but never reported a 10 %+ share ("low exposure") fell furthest below their forecasts. Six firms cut their guidance in the middle of the quarter and named Huawei; four of them were low-exposure firms.

This is descriptive. It shows how large the gaps were, not why.

### The primary test (next quarter, h = 1)

5 exposed firms (NeoPhotonics, Inphi, Qorvo, Micron, Finisar) against 14 chip-maker donors. Each firm's miss is the average of the two forecasting rules (B4 and AutoETS); positive means revenue came in above the forecast. The test ranks all 19 firms and adds up the exposed firms' ranks: a low sum means the exposed firms missed by more. Every possible choice of 5 firms out of 19 (11,628) is counted.

| | Rank-sum (expected 50) | One-sided p | Two-sided p | Gap in means (exposed − donors) |
|---|---|---|---|---|
| **Average of the two rules (primary)** | **41** | **0.22** | 0.44 | −6.3 points |
| B4 alone | 42 | 0.25 | 0.50 | −6.0 points |
| AutoETS alone | 38 | 0.15 | 0.30 | −6.6 points |

- **Both rules point the same way**, so the result counts as "consistent". But none of the three p-values is small.
- **Ranks of the exposed firms** (1 = biggest shortfall of all 19): Micron 1, Finisar 4, NeoPhotonics 7, Inphi 12, Qorvo 17.
- **Later quarters (secondary):**
  - two quarters ahead, the gap in means is −4.5 points, but the medians point the other way;
  - three quarters ahead it is −1.4 points, and the two rules disagree on its sign;
  - four quarters ahead runs into COVID and is not interpreted.

### Three groups

The "low exposure" group: 16 chip and optical firms that named Huawei as a customer or sales channel but never at 10 %+.

| One quarter ahead (h = 1) | Exposed (5) | Low exposure (16) | Donors (14) |
|---|---|---|---|
| Mean miss | −4.7 % | **−8.0 %** | +1.7 % |
| Median miss | −2.0 % | **−9.3 %** | +2.3 % |

- **Low exposure is the lowest group at every horizon**, with or without the four firms whose Huawei link appears only in a filing made after the event.
- At h = 1 the order is low < exposed < donors, by means and by medians.
- At h = 2 and h = 3 the medians put the exposed firms above the donors (post-hoc check).
- Scaled by each firm's own usual miss, the exposed and low-exposure firms' h = 1 misses were about 1.5 times their usual miss on the low side; the donors' were slightly above their forecasts.

### Guidance cuts

Six firms cut their revenue guidance for the quarter in progress, in an 8-K filed after 16 May 2019, and named Huawei:

| Firm | Group | Guidance cut (midpoint) | Model miss, h = 1 (average of the two rules) |
|---|---|---|---|
| MACOM | low exposure | −11.5 % | −23.8 % |
| Skyworks | low exposure | −7.3 % | −8.5 % |
| Cree / Wolfspeed | low exposure | −6.9 % | −19.2 % |
| Qorvo | exposed | −6.3 % | **+9.6 %** |
| Inphi | exposed | −5.1 % | **+5.5 %** |
| MaxLinear | low exposure | −3.5 % | −12.3 % |

- **The two exposed firms that cut guidance still came in above both simple forecasts; the four low-exposure firms that cut came in well below them.** (Their guidance levels were not compared with the model forecasts.)
- **Cirrus Logic** said the ban had "no material impact" on its current-quarter guidance.
- **Nine firms filed no 8-K after 16 May within their quarter**, including NeoPhotonics, Lumentum and Micron. That is not the same as no revision: see Limits.

### Predictions against the outcome

Both sets of predictions were written by Claude: one by Claude Code in this repo, and one drafted by Claude in a chat at Penelope's request and adopted by her. Both were committed before any forecast was run (commit `604c437`). **Neither was blind**: both were written by someone who knew about the 2019 chip downturn and the Huawei ban, and Claude Code had read some full-year 2019 revenue sentences in the 10-Ks (see `notes/predictions-before-run.md`).

**Set 1: drafted by Claude in a chat, adopted by Penelope**

| Prediction | Outcome | Right? |
|---|---|---|
| Gap negative under both rules | −6.0 (B4), −6.6 (AutoETS) | yes |
| Main driver Micron | Micron ranks 1 of 19 | yes |
| Size about −5 points, range −15 to +1 | −6.3 | yes (within range) |
| One-sided p 0.05–0.20, best guess 0.10 | 0.22 (average); 0.25 (B4); 0.15 (AutoETS) | no for the primary (just above) |
| Exposed lowest of the three groups (65 %) | low exposure lowest | no |
| Low exposure and donors look similar | low −8.0 vs donors +1.7 | no |
| Biggest exposed miss Micron | Micron −26.7 | yes |
| Smallest, possibly positive: Inphi, then NeoPhotonics | Qorvo +9.6, Inphi +5.5, NeoPhotonics −2.0 | partly |
| Gap similar at h = 2, smaller at h = 3 | −4.5 at h = 2 (medians reverse), −1.4 at h = 3 | partly |
| Driven by one or two firms (Micron, Qorvo) | Micron yes; Qorvo was the exposed firm furthest above its forecast | partly |
| Scaled outcome reduces Micron's weight | scaled, Finisar (−3.1) is below Micron (−2.9) | yes |
| Sensitivity donors close to zero | mean +0.2 | yes |

**Set 2: written by Claude Code in this repo**

| Prediction | Outcome | Right? |
|---|---|---|
| Gap negative under both rules | yes | yes |
| Size about −6 points (range −2 to −15) | −6.3 | yes |
| One-sided p 0.05–0.20 (best guess 0.10); two-sided about double | 0.22; two-sided 0.44 | no for the band; yes for "double" |
| Both rules point the same way (70 %) | yes | yes |
| Order exposed < low < donors (50 %) | low < exposed < donors | no |
| Biggest exposed miss Micron; smallest Inphi | Micron yes; most positive was Qorvo | partly |
| Gap larger at h = 2, smaller at h = 3 | smaller at both | half |
| Sensitivity donors closer to zero than primary donors | +0.2 vs +1.7 | yes |
| Scaled: exposed 1.5–3 times their usual miss; donors 1–2 times | exposed about 1.6; donors about 0.7 | half |

### What this does not show

It does **not** show that the Huawei ban had no effect on these firms: six of them named Huawei in their own mid-quarter guidance cuts. It also does not show a cause. What it shows is narrower: **two simple forecasting rules and five exposed firms cannot see an effect** that stands out from the ordinary spread of misses among chip makers in 2019.

### Limits (in short; full list below)

- **Few firms.** 5 exposed firms, 4 after the first quarter; one firm (Micron) moves the result.
- **Memory and optical markets** cannot be separated from Huawei exposure.
- **The 10 % disclosure line is a weak proxy** for real exposure, and guidance cuts and model misses measure different things.
- **Descriptive only:** 2019 was also a chip downturn with US–China tariffs. Nothing here says what drove any gap.

## Limits

- **Hidden exposure below 10 %.** Firms only have to name customers that reach 10 % of revenue. A "donor" is a firm that did not *say* its sales depend on Huawei, not one with no Huawei sales.
- **The later-filing check misses December year-end firms.** The Huawei full-text search covers 10-Ks filed up to 31 Dec 2020. Firms whose fiscal year ends in December filed their FY2020 10-K in 2021, so a Huawei mention there is not seen. For them, "later filings can move a firm out of the donor group" is not checked.
- **The search looks for the word "Huawei" only.** A 10-K naming only "HiSilicon" (Huawei's chip unit) is not found by the search, though HiSilicon sentences are extracted from the documents that are read.
- **The industry lists carry no dates**, and the 2018 revenue files (SEC frames) can miss active firms (Cree/Wolfspeed was missing). The donor pool may be incomplete.
- **Few exposed firms**, and fewer at longer horizons. One firm can move the result.
- **Acquired firms disappear from the sample.** Oclaro (Huawei 11 % of FY2018 revenue) was bought by Lumentum in Dec 2018 and has no quarter after the event. Finisar was bought by II-VI and stops reporting after July 2019, so it has h = 1 only. Firms that survived may differ from those that did not.
- **No 8-K is not the same as no revision.** The guidance-cut table only sees guidance and revisions filed with the SEC on 8-K. A firm may update its outlook in an unfiled press release or on a conference call. Some firms give their outlook only on the call (Micron, DSP Group in 2019).
- **Unsourced figures are not used.** For example, a note of a Lumentum guidance cut of "about −8 %" was not found in any filing: Lumentum filed no 8-K after 16 May 2019 in that quarter. Unsourced, not used.
- **Grouping uses 10-Ks only; later 8-Ks can give other numbers.** Skyworks' "approximately 12 percent" of H1 FY2019 revenue from Huawei is in its 4 June 2019 8-K, which is post-event and not in either 10-K. Skyworks stays "low exposure". Qorvo's 21 May 2019 8-K puts Huawei at "approximately $469 million or 15%" of FY2019 revenue, while its FY2019 10-K says 13 %. The dose uses the 10-K.
- **The 10 % disclosure line is a weak proxy for real exposure.** Four of the six mid-quarter guidance cuts that named Huawei came from "low exposure" firms (MACOM, Skyworks, MaxLinear, Cree), which never reported Huawei at 10 % or more. Also, the two measures differ: a guidance cut is the company's own statement of a direct hit, while the model misses measure surprise against two simple forecasting rules.
- **The yardstick lines come from non-chip companies**, so they are a rough guide only.
- **The new revenue accounting standard (ASC 606), adopted by most firms in 2018–2019, can cause small level shifts in revenue history** where the old and new standards differ. It affects all groups.
- **Sub-sector cannot be separated from Huawei exposure.** Most exposed firms make optical and datacom parts; most donors do not. Even after limiting the primary donors to chip and optical-component makers, a gap between the groups may reflect the optical/datacom market rather than Huawei.
