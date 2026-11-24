# Donor rule: who counts as a supplier with no Huawei exposure?

Written on 24 Nov 2026 (Session 1), before any SEC file was downloaded and before any forecast. Do not change it after seeing results. If something turns out to be impossible, write the change and the reason here, dated, before running anything.

## The rule in one sentence

A **donor** is a semiconductor or electronic-components company that files a 10-K with the SEC and whose 10-K **does not name Huawei as a 10 %+ customer** in fiscal 2018 or fiscal 2019.

## What each part means

- **Semiconductor or electronic-components company:** the industry code (SIC) the SEC gives the filer. **Proposed, to confirm before Session 2:** SIC 3674 (semiconductors and related devices) and SIC 3672, 3677, 3678, 3679 (printed circuit boards, coils and transformers, connectors, other electronic components). The code is read from the SEC's own company record, not chosen by hand.
- **Files a 10-K:** a US annual report. Foreign filers using 20-F or 40-F are left out, so all firms follow the same reporting rules.
- **Fiscal 2018 or fiscal 2019:** the firm's own fiscal years, as named in its 10-K. Both 10-Ks are read. Naming Huawei at 10 %+ in either year makes the firm "exposed", not a donor.
- **Names Huawei as a 10 %+ customer:** the 10-K gives Huawei (or HiSilicon, Huawei's chip unit) a share of revenue of 10 % or more, anywhere in the filing (customer section, risk factors, the segment or concentration note).
- **Same data rules as the exposed firms:** a donor goes through the same Project 2 code, the same 65-day rule, the same 20-quarter start, the same origin rule (its last fiscal quarter ending before 16 May 2019) and h = 1–4. A donor with fewer than 20 quarters before the origin, or whose origin quarter was filed after the 65-day cutoff, goes to the SECONDARY table exactly as an exposed firm would (see `screening-plan.md`, "Primary and secondary comparison"; wording updated 24 Nov 2026, before any download). A missing target quarter is recorded, not filled in.

## The plain limit: hidden exposure below 10 %

US accounting rules require a company to report a customer only when it reaches **10 % of revenue**. Below that line, a firm can sell a lot to Huawei and say nothing. **So "donor" means "did not disclose 10 %+ Huawei exposure", not "had no Huawei exposure".** Some donors probably did sell to Huawei. If they did, the gap between exposed firms and donors is **smaller** than the true gap, because part of the effect sits inside the comparison group too.

The same 10 % line causes three more blind spots:

1. **Named below 10 %.** A 10-K can mention Huawei with a smaller share (for example in the risk factors). Under this rule such a firm is still a donor. Each one found is listed, so its effect on the result can be seen.
2. **Unnamed big customers.** Some 10-Ks say "Customer A, 12 %" without a name. If Customer A was Huawei, the rule wrongly counts the firm as a donor. Each such firm is listed as "unnamed 10 %+ customer".
3. **Sales through others.** Chips sold to Huawei through a distributor or a contract manufacturer show up under that middleman's name, not Huawei's.

## Other limits (why this is descriptive only)

- **2019 was a chip downturn for everyone**: falling memory prices, customers cutting stock, US–China tariffs. Exposed firms and donors were both hit. The comparison only shows whether exposed firms missed by *more*, not why.
- **Exposed firms sell more to China in general.** A larger miss could come from China demand or tariffs, not from Huawei.
- **Few exposed firms** (about five to ten). One firm can move the whole result, so each firm is shown on its own as well as in the group.
- **The yardstick lines come from non-chip companies.** None of the 20 Project 2 companies makes chips or electronic components, and chip revenue swings more. So the 90th-percentile lines are a rough guide only. The main comparison is exposed firms against donors, both of them chip firms.

## Decisions for Penelope before Session 2 (not decided here)

- Confirm the SIC codes above, or change them.
- Whether firms that name Huawei **below** 10 % stay donors (the rule as written: yes) or are shown separately as well.
- Whether firms with an **unnamed** 10 %+ customer stay donors (the rule as written: yes) or are shown separately as well.
