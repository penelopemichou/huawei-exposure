# Permutation test setup — FIXED on 25 Nov 2026 (choices by Penelope; not run)

The choices below were made by Penelope on 25 Nov 2026, before any forecast. **Fixed on 25 Nov 2026** (see the end of this note). It must be committed before any forecast is run (design-v2 (b)). Nothing below may change after a forecast has been run.

## Firms

- **PRIMARY exposed firms** (5 at h = 1: NeoPhotonics, Inphi, Qorvo, Micron, Finisar) and **PRIMARY donors**. Primary donors are chip and optical-component makers only (design-v2 (f)); the exact list is in `notes/frozen-lists.md` once frozen.
- N = all firms in the test, n = number of exposed firms (5).
- A firm without an h = 1 forecast from **both** rules drops out of the test and is listed with the reason. The test is then redone on the firms left.

## Outcome per firm

- Signed miss at **h = 1**, in %: 100 × (actual − forecast) ÷ actual. Negative = revenue came in below the forecast.
- **Per-firm outcome = the average of the B4 and the AutoETS signed miss** at h = 1.
- Each rule is also tested **separately**, in the same way: three results in all (average, B4, AutoETS).

## Statistic: rank-sum

1. Rank all N firms by their outcome, from the **lowest** signed miss (rank 1, biggest shortfall) to the highest (rank N). Ties share the average of their ranks.
2. **Statistic = the sum of the exposed firms' ranks.** A small rank-sum means the exposed firms tend to have the lowest signed misses.
3. If exposure made no difference, the expected rank-sum is n × (N + 1) ÷ 2.

## p-values

- **Exact enumeration** of every way to choose n "exposed" firms out of N, for example C(20, 5) = 15,504 if N = 20. No random shuffling, no seed.
- **Primary, one-sided:** share of all choices with rank-sum **≤** the real rank-sum ("exposed firms' signed miss lower").
- **Two-sided, reported next to it:** share of all choices whose rank-sum is at least as far from n × (N + 1) ÷ 2 as the real one, in either direction.
- The real labelling is counted among the choices, so p is never 0.

## When is a result "consistent"?

**Only if both rules point the same way:** the B4 rank-sum and the AutoETS rank-sum are both below n × (N + 1) ÷ 2, or both above it. Otherwise the result is reported as "rules disagree", whatever the p-value of the average.

## Also reported, without a test

- Every firm's own signed miss (average, B4, AutoETS) at h = 1–4. h = 2 and 3 are secondary; h = 4 is flagged COVID.
- The secondary outcome (design-v2 (g)): signed miss ÷ the firm's own median absolute pre-event miss, with the number of pre-event forecasts per firm.
- The three-group order (design-v2 (e)) and the sensitivity group (design-v2 (f)).
- The firms that dropped out, with the reason.

Descriptive only: no causal claim.

## Fixed

**Fixed on 25 Nov 2026** by Penelope, before any forecast. Last commit before fixing: `86a8e28`.

- Firms in the primary test at h = 1, from `notes/frozen-lists.md` (frozen on 25 Nov 2026): N = 19 (n = 5 exposed + 14 primary donors).
- Exact enumeration: C(19, 5) = 11,628 ways to choose the five "exposed" firms.
- Expected rank-sum if exposure made no difference: n × (N + 1) ÷ 2 = 5 × 20 ÷ 2 = 50.
- If a firm drops out (no h = 1 forecast from both rules), N, the enumeration and the expected rank-sum are recomputed, and the firm is listed.
