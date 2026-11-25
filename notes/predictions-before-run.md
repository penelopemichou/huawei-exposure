# Predictions, written BEFORE the forecasts are run

Fill this in after the lists are frozen and the permutation setup is fixed, and **before** any forecast is run. Then commit it with "yes, commit". The run happens only after that commit, and the commit hash is noted in the results.

Each prediction is short, concrete and checkable. Nothing here may be changed after the run; corrections go in a new dated section.

## Penelope's predictions (date: 26 Nov 2026)

I saw Claude's predictions before writing mine.

PENELOPE'S PREDICTIONS (26 Nov 2026)
Written by Claude in the chat at Penelope's request; Penelope adopts them as her own.
Not blind: general knowledge of the 2019 chip downturn and the Huawei ban, and Claude Code's predictions seen earlier. No forecast, quarterly value or miss seen.

1. Sign of the gap (exposed minus primary donors, h = 1, signed miss): negative under both B4 and AutoETS. Confidence about 65%. The main driver is Micron.

2. Size: about -5 percentage points, plausible range -15 to +1. Micron alone could pull the average of 5 exposed firms down by 4 to 6 points. The other exposed firms offset part of it, because some Huawei suppliers shipped extra in May and June 2019 before the ban took hold.

3. One-sided p-value (rank-sum, exact): band 0.05 to 0.20, best guess about 0.10. Chance of p below 0.05 is about 25%; it needs the exposed firms to sit in the bottom third of all 19 firms.

4. Order of the three groups: exposed lowest is likely (about 65%). The full order exposed < low exposure < donors is about 35%. I expect low exposure and donors to look similar, because the 16 low-exposure firms were also hit by the 2019 downturn (smartphones, inventory correction).

5. Biggest exposed miss: Micron (about 75%), mostly because DRAM prices fell sharply in 2019, which is not Huawei. Smallest, possibly positive: Inphi (datacentre demand), with NeoPhotonics second.

6. h = 2 and h = 3: the gap is similar at h = 2 (first full quarter after the ban) and smaller at h = 3, as the sector recovered in late 2019 and the temporary licence kept some shipments going. h = 4 is not interpretable (COVID).

7. Other: I expect the result to be driven by one or two firms (Micron, Qorvo), so it will be fragile. I expect the scaled outcome to reduce Micron's weight, since its usual miss is large. The sensitivity donors (contract manufacturers, solar, equipment) should sit close to zero. More likely than not, the result cannot be separated from sub-sector (memory and optical) effects, and the README should say that.

Answers are in the text above.

## Claude's predictions (date: 25 Nov 2026; written after the freeze `adb3a8b`, before any forecast)

**Not blind; read this first.** While labelling the 10-Ks (Stage B), Claude read some FY2019 sentences about revenue **after** the event: NeoPhotonics' 2019 revenue was above 2018, Inphi's 2019 revenue was above 2018, and Skyworks' fiscal 2019 revenue fell by $491.2 million. These are full-year figures, not the quarterly misses measured here, but they can lean the predictions below. Claude has also seen no forecast, no quarterly revenue value and no miss.

1. **Sign of the h = 1 gap** (exposed minus primary donors): B4 **negative**; AutoETS **negative**. Exposed firms miss by more.
2. **Size of the gap** (average of the two rules): about **−6 percentage points**, likely range −2 to −15.
3. **p-values** (average outcome): one-sided between **0.05 and 0.20** (best guess about 0.10). The two-sided value is about double. With only 5 exposed firms, a gap this size need not reach 0.05.
4. **Consistent?** Yes: both rules point the same way (about 70 % confident).
5. **Three-group order at h = 1:** exposed lowest, then low exposure, then primary donors (about 50 % confident). Most likely alternative: low exposure close to the donors.
6. **Biggest exposed miss: Micron**, largely because of the 2019 memory-price fall, not only Huawei. This is a confound to state with the result. **Smallest: Inphi** (data-centre growth).
7. **h = 2 and h = 3 vs h = 1:** the gap is **larger at h = 2** (the first full quarter after the ban) and somewhat smaller at h = 3.
8. **Sensitivity donors:** misses closer to zero than the primary donors on average (contract manufacturers and connector makers swing less than chip makers).
9. **Scaled miss (secondary outcome):** exposed firms' h = 1 misses about **1.5–3 times** their own usual pre-event miss; primary donors' about 1–2 times.

**Note added 25 Nov 2026, after these predictions were written (predictions unchanged):** while building the exact eligibility table, Project 2's `prepare()` printed some full-year revenue values it dropped: Inphi 2014, Lattice 2022, MagnaChip 2018–2019, Silicon Labs 2019–2022. Claude saw them; some are after the origin. No quarterly value, forecast or miss was seen.

## Inputs fixed at the time of writing

- Frozen lists: `notes/frozen-lists.md` (frozen on ____ )
- Permutation setup: `notes/permutation-setup.md` (fixed on ____ )
- Commit before the run: ____
