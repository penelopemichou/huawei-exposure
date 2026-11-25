# Donor rule: who counts as a supplier with no Huawei exposure?

Written on 24 Nov 2026 (Session 1). **Reworded on 25 Nov 2026 to a label-based test**, before any 10-K was read and before any forecast. Do not change it after seeing results. If something turns out to be impossible, write the change and the reason here, dated, before running anything.

## The rule in one sentence

A **donor** is a semiconductor or electronic-components 10-K filer whose FY2018 and FY2019 10-Ks contain **no sentence saying that its own sales depend on Huawei**, directly or indirectly.

## Labels (one per sentence, from `results/huawei_sentences.csv`)

Every sentence that mentions Huawei or HiSilicon (Huawei's chip unit) gets one label:

| Label | Meaning | Example (made up) |
|---|---|---|
| customer with % | names Huawei as the firm's customer and gives its share of revenue | "Huawei accounted for 15% of our revenue" |
| customer without % | names Huawei as the firm's customer (or licensee) with no share | "our customers include Huawei" |
| indirect | says the firm's sales depend on Huawei through others | "our customers sell to Huawei"; "contract manufacturers that build for Huawei" |
| competitor/other | mentions Huawei but says nothing about the firm's own sales | "we compete with Huawei"; a general description of the Entity List |
| unclear | cannot be told from the sentence | (no guessing; Penelope decides) |

"Sales" includes licence revenue. A sentence saying that restrictions on selling to Huawei hurt **the firm's** business is about its own sales, so it gets a customer or indirect label, not "other".

## Groups

| Group | Who |
|---|---|
| **Exposed** | a sentence labelled *customer with %* gives Huawei a share of **10 % or more** in FY2018 or FY2019 |
| **Low exposure** | Huawei is named as a customer with a share **below 10 %** (and never 10 %+) |
| **Out of the donor group** | any sentence labelled *customer without %* or *indirect* (and not exposed or low exposure). Listed with the reason |
| **Donor** | passes the donor filter below: no mention at all, or only *competitor/other* mentions |

A sentence labelled *unclear* keeps the firm **out of the donor group until Penelope decides**. It is listed with the sentence.

### Exposure group and dose (decided 25 Nov 2026, before any forecast)

- **Group:** a firm is **exposed** if its FY2018 or FY2019 10-K names Huawei at **10 % or more** of total revenue.
- **Dose** (how exposed): Huawei's share in the firm's **latest fiscal year that ended before 16 May 2019**, as written in the 10-K. If that year's 10-K gives no percentage for Huawei, the other year's figure is used and marked **"fallback, flagged"**.

### Low exposure, implied (decided 25 Nov 2026)

The firm's FY2018/FY2019 10-K names Huawei as a customer (or licensee) but gives no share, and says no other customer reached 10 %. So the share is below 10 % only by implication.

- These firms are **not donors** and are **not in the primary exposed-vs-donor comparison**.
- They are shown in **their own rows** and in the **guidance-cut table**. (That table is not defined in this repo yet; Penelope's term, to be specified.)
- Firms (from B1): MACOM, Skyworks, Broadcom, Qualcomm.
  - **Qualcomm: royalty income, not product sales.** Huawei pays licence royalties ($600 million in FY2018, $450 million in FY2019), so its "exposure" is of a different kind.
  - **Skyworks:** Penelope's note "about 12 % of H1 FY2019" may come from a 10-Q; it is not in either 10-K. The 10-Q is proposed as Stage B3.

## Donor filter (all five must hold; drafted 25 Nov 2026, not applied yet)

1. **Industry:** SEC industry code 3674, 3672, 3677, 3678 or 3679.
2. **Size:** 2018 revenue of at least $100 million, from the SEC frames files for calendar 2018 (Stage A2). If a firm has more than one revenue tag, the largest value is used.
3. **History:** first 10-K or 10-Q filed in 2014 or earlier.
4. **Origin on time:** the origin quarter (last fiscal quarter ending before 16 May 2019) was filed by the cutoff (quarter end + 65 days).
5. **Label test:** in its FY2018 and FY2019 10-Ks (and 10-K/As), no sentence labelled customer with %, customer without %, indirect or unclear.
   - A firm with **no search hit** passes without reading. The full-text search is the evidence.
   - A firm **with a hit** passes only after its documents are read and labelled. It never passes by default.

**Every firm that passes is included.** No firm is added or removed by hand.

**Later filings can only move a firm OUT of the donor group, never in.** A later 10-K (filed up to 31 Dec 2020, the end of the full-text search; for example Xilinx FY2020) with a sentence labelled customer with %, customer without %, indirect or unclear moves the firm out, using the same label test. A firm moved out this way is not counted as exposed. Nothing filed later can make a firm a donor or change an exposed firm's group.

**Dropped-donor list:** every firm that fails any criterion is listed in `results/dropped_donors.csv` with the criterion it failed and, for criterion 5 or a later filing, the document and sentence.

**Donors and exposed firms are treated differently on history and timing.** A donor failing criterion 3 or 4 is simply not a donor. An exposed firm failing the 20-quarter or 65-day check goes to the SECONDARY table. The pre-flight table (PROGRESS.md) still applies to every firm that passes the filter. Criterion 3 is a first screen; the pre-flight table checks the 20 quarters exactly.

**What this means for the reading:** every firm with the donor codes that has a "Huawei" hit in FY2018–FY2019 (B2), **or only in a later 10-K up to 2020**, must be read before it can be a donor. The later-only firms are not in the B2 list yet.

## The plain limit: hidden exposure below 10 %

US accounting rules require a company to report a customer only when it reaches **10 % of revenue**. Below that line, a firm can sell a lot to Huawei and say nothing. **So "donor" means "did not say its sales depend on Huawei", not "had no Huawei exposure".** Some donors probably did sell to Huawei. If they did, the gap between exposed firms and donors is **smaller** than the true gap.

The same reporting rules cause more blind spots:

1. **Unnamed big customers.** Some 10-Ks say "Customer A, 12 %" without a name. If Customer A was Huawei, the test cannot see it. Each such firm is listed as "unnamed 10 %+ customer" (from the 10 %-customer paragraphs).
2. **Sales through others that are never described.** If a 10-K never says that its customers sell to Huawei, the indirect label cannot catch it.
3. **Words the search does not find.** The full-text search looks for "Huawei" only. A firm that writes only "HiSilicon" and has no "Huawei" hit is not read. (In the documents that *are* read, HiSilicon sentences are extracted too.)
4. **Filings after 2020** are not searched.

## Other limits (why this is descriptive only)

- **2019 was a chip downturn for everyone**: falling memory prices, customers cutting stock, US–China tariffs. Exposed firms and donors were both hit. The comparison only shows whether exposed firms missed by *more*, not why.
- **Exposed firms sell more to China in general.** A larger miss could come from China demand or tariffs, not from Huawei.
- **Few exposed firms** (about five to ten). One firm can move the whole result, so each firm is shown on its own as well as in the group.
- **The yardstick lines come from non-chip companies.** None of the 20 Project 2 companies makes chips or electronic components, and chip revenue swings more. So the 90th-percentile lines are a rough guide only. The main comparison is exposed firms against donors, both of them chip firms.

## Settled (25 Nov 2026)

- Industry codes: the five above.
- Firms naming Huawei as a customer below 10 % are **not** donors; they form the "low exposure" group.
- Firms with only competitor/other mentions **are** donors.


## Still open (Penelope's decision)

- Firms with an unnamed 10 %+ customer ("Customer A"). As written, they stay donors, because the test cannot see who the customer is. They are listed separately either way.
