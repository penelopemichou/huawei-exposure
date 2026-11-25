# huawei-exposure

Did US chip and electronic-component suppliers with more disclosed Huawei exposure miss simple revenue forecasts by more after Huawei was added to the US Entity List (16 May 2019) than suppliers with none?

**Descriptive only.** This project can say how large the gap was. It cannot say why: 2019 was also a chip downturn, and US–China tariffs hit at the same time.

- **Data:** public SEC filings only (EDGAR filing lists, full-text search, XBRL revenue data, 10-K documents).
- **Forecast rules:** two simple rules reused unchanged from an earlier project (B4 and AutoETS), with a 65-day data-availability rule.
- **Design:** `PROGRESS.md` (v1) and `notes/design-v2.md` (changes made before any forecast).
- **Who counts as exposed or as a donor:** `notes/donor-rule.md`.

## Limits

- **Hidden exposure below 10 %.** Firms only have to name customers that reach 10 % of revenue. A "donor" is a firm that did not *say* its sales depend on Huawei, not one with no Huawei sales.
- **The later-filing check misses December year-end firms.** The Huawei full-text search covers 10-Ks filed up to 31 Dec 2020. Firms whose fiscal year ends in December filed their FY2020 10-K in 2021, so a Huawei mention there is not seen. For them, "later filings can move a firm out of the donor group" is not checked.
- **The search looks for the word "Huawei" only.** A 10-K naming only "HiSilicon" (Huawei's chip unit) is not found by the search, though HiSilicon sentences are extracted from the documents that are read.
- **The industry lists carry no dates**, and the 2018 revenue files (SEC frames) can miss active firms (Cree/Wolfspeed was missing). The donor pool may be incomplete.
- **Few exposed firms**, and fewer at longer horizons (Finisar stops reporting after July 2019). One firm can move the result.
- **The yardstick lines come from non-chip companies**, so they are a rough guide only.
