# Stage B plan: the 10-K documents (drafted 25 Nov 2026, nothing downloaded)

Two stages, each needs its own "yes": **B1** (the 14 firms) and **B2** (the 22 other firms with the donor codes that mention Huawei).

## Rules for both stages

- **Only the document named in the table** is downloaded: the main 10-K (or 10-K/A) file, not the whole filing, not the exhibits, not the XBRL files.
- **Source:** `https://www.sec.gov/Archives/edgar/data/<CIK>/<accession without dashes>/<document>`.
- **Saved to:** `data/raw/stage_b/<CIK>/<accession>/<document>` (gitignored, a new empty folder).
- **Requests:** one per document, 0.5 s apart, logged, with the same hard stop as Stage A (60 per stage).
- **Fiscal year** = the calendar year in which the fiscal year ends (Project 2's rule, `fiscal_labels` in `build_quarterly.py`). Exception noted: TTM's year ending 1 Jan 2018 is "fiscal 2018" here, though TTM calls it fiscal 2017.
- **Sizes:** the SEC filing list gives only the size of the **whole filing** (document + exhibits + XBRL data), so the "filing total" column is an **upper bound**. The main document is usually 1–10 MB. For B2 there is no filing list yet, so sizes are estimates only.

## What is extracted (after the download, no internet)

One script (in `src/`, outside the data folder; Python `-I`; standard library HTML reading, no new installs) writes `results/huawei_sentences.csv` with exactly these columns:

| Column | Content |
|---|---|
| firm | firm name |
| filing | form, fiscal year, accession, document (e.g. `10-K FY2019 0001604778-19-000031 qorvo2019033010-k.htm`) |
| section | the nearest heading above the text (e.g. "Item 1A. Risk Factors", "Note 15") |
| sentence | the full sentence, unchanged |
| label | customer with % / customer without % / indirect / competitor/other / unclear (definitions: `donor-rule.md`, reworded 25 Nov 2026) |

Two kinds of rows:
1. **Every sentence containing "Huawei"** (also "HiSilicon", Huawei's chip unit, so it is not missed).
2. **The 10 %-customer paragraph:** every paragraph that contains "10%" (or "ten percent") together with "customer". One row per paragraph, whether or not it names Huawei. This is where unnamed "Customer A" cases show up; they go to a separate table in `notes/stage-b-results.md`.

**Labelling:** every row is read and given a proposed label by hand. A sentence that cannot be told is marked "unclear", never guessed. Penelope sees all rows. A label changed by hand is marked as such. Numbers are copied as written, never rounded.

## B1: the 14 firms (FY2018 and FY2019 10-Ks, Xilinx FY2020, and the 10-K/As the search found)

**31 documents, 31 requests.** Upper bound (sum of whole filings): 670 MB. Expected for the documents alone: about 31–248 MB.

| firm | FY | form | period end | filed | document | search found Huawei | filing total MB | url |
|---|---|---|---|---|---|---|---|---|
| Acacia | 2018 | 10-K | 2018-12-31 | 2019-02-21 | acia1231201810k.htm | yes | 11.3 | https://www.sec.gov/Archives/edgar/data/1651235/000165123519000042/acia1231201810k.htm |
| Acacia | 2019 | 10-K | 2019-12-31 | 2020-02-18 | aciaq4201910k.htm | yes | 12.6 | https://www.sec.gov/Archives/edgar/data/1651235/000165123520000022/aciaq4201910k.htm |
| Broadcom | 2018 | 10-K | 2018-11-04 | 2018-12-21 | avgo-11042018x10k.htm | no | 31.2 | https://www.sec.gov/Archives/edgar/data/1730168/000173016818000084/avgo-11042018x10k.htm |
| Broadcom | 2019 | 10-K | 2019-11-03 | 2019-12-20 | avgo-11032019x10k.htm | yes | 31.3 | https://www.sec.gov/Archives/edgar/data/1730168/000173016819000144/avgo-11032019x10k.htm |
| Finisar | 2018 | 10-K | 2018-04-29 | 2018-06-15 | fnsr10kfy18.htm | yes | 9.3 | https://www.sec.gov/Archives/edgar/data/1094739/000109473918000035/fnsr10kfy18.htm |
| Finisar | 2019 | 10-K | 2019-04-28 | 2019-06-14 | fnsr10kfy19.htm | yes | 9.9 | https://www.sec.gov/Archives/edgar/data/1094739/000109473919000038/fnsr10kfy19.htm |
| II-VI | 2018 | 10-K | 2018-06-30 | 2018-08-28 | iivi-10k_20180630.htm | no | 22.8 | https://www.sec.gov/Archives/edgar/data/820318/000156459018022409/iivi-10k_20180630.htm |
| II-VI | 2019 | 10-K | 2019-06-30 | 2019-08-16 | iivi-10k_20190630.htm | yes | 23.5 | https://www.sec.gov/Archives/edgar/data/820318/000156459019032471/iivi-10k_20190630.htm |
| Inphi | 2018 | 10-K | 2018-12-31 | 2019-02-28 | iphi20181231_10k.htm | yes | 11.3 | https://www.sec.gov/Archives/edgar/data/1160958/000143774919003645/iphi20181231_10k.htm |
| Inphi | 2019 | 10-K | 2019-12-31 | 2020-03-02 | iphi20191231_10k.htm | yes | 12.4 | https://www.sec.gov/Archives/edgar/data/1160958/000143774920004130/iphi20191231_10k.htm |
| Intel | 2018 | 10-K | 2018-12-29 | 2019-02-01 | a12292018q4-10kdocument.htm | no | 59.9 | https://www.sec.gov/Archives/edgar/data/50863/000005086319000007/a12292018q4-10kdocument.htm |
| Intel | 2019 | 10-K | 2019-12-28 | 2020-01-24 | a12282019q4-10kdocument.htm | no | 143.1 | https://www.sec.gov/Archives/edgar/data/50863/000005086320000011/a12282019q4-10kdocument.htm |
| Lumentum | 2018 | 10-K | 2018-06-30 | 2018-08-28 | lumentumfy1810k.htm | yes | 17.4 | https://www.sec.gov/Archives/edgar/data/1633978/000163397818000108/lumentumfy1810k.htm |
| Lumentum | 2019 | 10-K | 2019-06-29 | 2019-08-27 | lumentumfy19-10k.htm | yes | 21.0 | https://www.sec.gov/Archives/edgar/data/1633978/000163397819000069/lumentumfy19-10k.htm |
| MACOM | 2018 | 10-K | 2018-09-28 | 2018-11-16 | mtsi10-k2018.htm | yes | 15.2 | https://www.sec.gov/Archives/edgar/data/1493594/000149359418000034/mtsi10-k2018.htm |
| MACOM | 2019 | 10-K | 2019-09-27 | 2019-11-26 | mtsi10-k2019.htm | yes | 16.5 | https://www.sec.gov/Archives/edgar/data/1493594/000149359419000064/mtsi10-k2019.htm |
| Micron | 2018 | 10-K | 2018-08-30 | 2018-10-15 | a2018q4.htm | no | 19.0 | https://www.sec.gov/Archives/edgar/data/723125/000072312518000092/a2018q4.htm |
| Micron | 2019 | 10-K | 2019-08-29 | 2019-10-17 | a2019q4.htm | yes | 26.0 | https://www.sec.gov/Archives/edgar/data/723125/000072312519000094/a2019q4.htm |
| NeoPhotonics | 2018 | 10-K | 2018-12-31 | 2019-03-08 | nptn12311810k.htm | yes | 16.3 | https://www.sec.gov/Archives/edgar/data/1227025/000122702519000013/nptn12311810k.htm |
| NeoPhotonics | 2019 | 10-K | 2019-12-31 | 2020-02-28 | nptn12311910k.htm | yes | 16.0 | https://www.sec.gov/Archives/edgar/data/1227025/000122702520000020/nptn12311910k.htm |
| NeoPhotonics | 2019 | 10-K/A | 2019-12-31 | 2020-03-03 | nptn12311910ka.htm | yes | 16.1 | https://www.sec.gov/Archives/edgar/data/1227025/000122702520000025/nptn12311910ka.htm |
| Qorvo | 2018 | 10-K | 2018-03-31 | 2018-05-21 | qorvo2018033110-k.htm | yes | 16.5 | https://www.sec.gov/Archives/edgar/data/1604778/000160477818000023/qorvo2018033110-k.htm |
| Qorvo | 2019 | 10-K | 2019-03-30 | 2019-05-17 | qorvo2019033010-k.htm | yes | 15.6 | https://www.sec.gov/Archives/edgar/data/1604778/000160477819000031/qorvo2019033010-k.htm |
| Qualcomm | 2018 | 10-K | 2018-09-30 | 2018-11-07 | qcom10-k2018.htm | yes | 15.3 | https://www.sec.gov/Archives/edgar/data/804328/000172894918000095/qcom10-k2018.htm |
| Qualcomm | 2019 | 10-K | 2019-09-29 | 2019-11-06 | qcom10-k2019.htm | yes | 15.9 | https://www.sec.gov/Archives/edgar/data/804328/000172894919000072/qcom10-k2019.htm |
| Skyworks | 2018 | 10-K | 2018-09-28 | 2018-11-15 | fy1810k92818.htm | yes | 10.0 | https://www.sec.gov/Archives/edgar/data/4127/000000412718000046/fy1810k92818.htm |
| Skyworks | 2019 | 10-K | 2019-09-27 | 2019-11-14 | fy1910k92719.htm | yes | 9.9 | https://www.sec.gov/Archives/edgar/data/4127/000000412719000049/fy1910k92719.htm |
| Skyworks | 2019 | 10-K/A | 2019-09-27 | 2020-01-27 | fy1910-kajanuary242020.htm | yes | 1.0 | https://www.sec.gov/Archives/edgar/data/4127/000000412720000009/fy1910-kajanuary242020.htm |
| Xilinx | 2018 | 10-K | 2018-03-31 | 2018-05-15 | xlnx331201810k.htm | no | 14.2 | https://www.sec.gov/Archives/edgar/data/743988/000074398818000022/xlnx331201810k.htm |
| Xilinx | 2019 | 10-K | 2019-03-30 | 2019-05-10 | xlnx330201910k.htm | no | 14.2 | https://www.sec.gov/Archives/edgar/data/743988/000074398819000012/xlnx330201910k.htm |
| Xilinx | 2020 | 10-K | 2020-03-28 | 2020-05-08 | xlnx328202010k.htm | yes | 15.7 | https://www.sec.gov/Archives/edgar/data/743988/000074398820000020/xlnx328202010k.htm |

## B2: the 22 other firms with the donor codes that mention Huawei

**34 documents from 22 CIKs, 34 requests.** All are main 10-K documents (the one exhibit hit, Synaptics EX-2.2(C), is fiscal 2020 and left out). No filing list was downloaded for these firms, so sizes are estimates: about 1–8 MB each, about 34–272 MB in all.

| firm | SIC | FY | form | period end | filed | document | url |
|---|---|---|---|---|---|---|---|
| Ambarella Inc | 3674 | 2019 | 10-K | 2019-01-31 | 2019-03-29 | amba-10k_20190131.htm | https://www.sec.gov/Archives/edgar/data/1280263/000156459019010114/amba-10k_20190131.htm |
| Applied Optoelectronics, Inc. | 3674 | 2019 | 10-K | 2019-12-31 | 2020-02-28 | aaoi20191231_10k.htm | https://www.sec.gov/Archives/edgar/data/1158114/000143774920003909/aaoi20191231_10k.htm |
| Ceva Inc | 3674 | 2018 | 10-K | 2018-12-31 | 2019-03-04 | ceva20181231_10k.htm | https://www.sec.gov/Archives/edgar/data/1173489/000143774919003949/ceva20181231_10k.htm |
| Ceva Inc | 3674 | 2019 | 10-K | 2019-12-31 | 2020-02-28 | ceva20191231_10k.htm | https://www.sec.gov/Archives/edgar/data/1173489/000143774920003932/ceva20191231_10k.htm |
| Cree, Inc. | 3674 | 2019 | 10-K | 2019-06-30 | 2019-08-21 | a06302019-10k.htm | https://www.sec.gov/Archives/edgar/data/895419/000089541919000046/a06302019-10k.htm |
| Cypress Semiconductor Corp /De/ | 3674 | 2019 | 10-K | 2019-12-29 | 2020-02-21 | cy-12292019x10xk.htm | https://www.sec.gov/Archives/edgar/data/791915/000079191520000006/cy-12292019x10xk.htm |
| Dsp Group Inc /De/ | 3674 | 2018 | 10-K | 2018-12-31 | 2019-03-11 | dspg20181231_10k.htm | https://www.sec.gov/Archives/edgar/data/915778/000143774919004573/dspg20181231_10k.htm |
| Dsp Group Inc /De/ | 3674 | 2019 | 10-K | 2019-12-31 | 2020-03-11 | dspg20191231_10k.htm | https://www.sec.gov/Archives/edgar/data/915778/000143774920004811/dspg20191231_10k.htm |
| Enphase Energy, Inc. | 3674 | 2018 | 10-K | 2018-12-31 | 2019-03-15 | a2018form10-k.htm | https://www.sec.gov/Archives/edgar/data/1463101/000146310119000033/a2018form10-k.htm |
| Enphase Energy, Inc. | 3674 | 2019 | 10-K | 2019-12-31 | 2020-02-21 | a2019q410-kdoc.htm | https://www.sec.gov/Archives/edgar/data/1463101/000146310120000021/a2019q410-kdoc.htm |
| Flex Ltd. | 3672 | 2018 | 10-K | 2018-03-31 | 2018-06-14 | flex331201810-k.htm | https://www.sec.gov/Archives/edgar/data/866374/000086637418000007/flex331201810-k.htm |
| Maxlinear Inc | 3674 | 2018 | 10-K | 2018-12-31 | 2019-02-05 | a12311810-k.htm | https://www.sec.gov/Archives/edgar/data/1288469/000128846919000006/a12311810-k.htm |
| Maxlinear Inc | 3674 | 2019 | 10-K | 2019-12-31 | 2020-02-05 | a12311910-k.htm | https://www.sec.gov/Archives/edgar/data/1288469/000128846920000013/a12311910-k.htm |
| Mellanox Technologies, Ltd. | 3674 | 2019 | 10-K | 2019-12-31 | 2020-02-20 | a2019123110-k.htm | https://www.sec.gov/Archives/edgar/data/1356104/000135610420000008/a2019123110-k.htm |
| Mosys, Inc. | 3674 | 2018 | 10-K | 2018-12-31 | 2019-03-12 | mosy-10k_20181231.htm | https://www.sec.gov/Archives/edgar/data/890394/000156459019007379/mosy-10k_20181231.htm |
| Mosys, Inc. | 3674 | 2019 | 10-K | 2019-12-31 | 2020-03-17 | mosy-10k_20191231.htm | https://www.sec.gov/Archives/edgar/data/890394/000156459020011421/mosy-10k_20191231.htm |
| Nxp Semiconductors N.V. | 3674 | 2019 | 10-K | 2019-12-31 | 2020-02-27 | nxp10-k.htm | https://www.sec.gov/Archives/edgar/data/1413447/000141344720000009/nxp10-k.htm |
| Oclaro, Inc. | 3674 | 2018 | 10-K | 2018-06-30 | 2018-08-23 | oclaro10k2018-06x30.htm | https://www.sec.gov/Archives/edgar/data/1110647/000162828018011325/oclaro10k2018-06x30.htm |
| On Semiconductor Corp | 3674 | 2019 | 10-K | 2019-12-31 | 2020-02-19 | d864442d10k.htm | https://www.sec.gov/Archives/edgar/data/1097864/000119312520041751/d864442d10k.htm |
| Pixelworks, Inc | 3674 | 2018 | 10-K | 2018-12-31 | 2019-03-13 | pxlw12312018_10k.htm | https://www.sec.gov/Archives/edgar/data/1040161/000104016119000008/pxlw12312018_10k.htm |
| Pixelworks, Inc | 3674 | 2019 | 10-K | 2019-12-31 | 2020-03-11 | pxlw1231201910k.htm | https://www.sec.gov/Archives/edgar/data/1040161/000104016120000010/pxlw1231201910k.htm |
| Quantenna Communications Inc | 3674 | 2018 | 10-K | 2018-12-30 | 2019-03-01 | quantenna-12302018x10k.htm | https://www.sec.gov/Archives/edgar/data/1370702/000137070219000006/quantenna-12302018x10k.htm |
| Semtech Corp | 3674 | 2018 | 10-K | 2018-01-28 | 2018-03-22 | smtc-01282018x10k.htm | https://www.sec.gov/Archives/edgar/data/88941/000162828018003489/smtc-01282018x10k.htm |
| Semtech Corp | 3674 | 2019 | 10-K | 2019-01-27 | 2019-03-21 | smtc-01272019x10k.htm | https://www.sec.gov/Archives/edgar/data/88941/000162828019003241/smtc-01272019x10k.htm |
| Sitime Corp | 3674 | 2019 | 10-K | 2019-12-31 | 2020-03-02 | sitm-10k_20191231.htm | https://www.sec.gov/Archives/edgar/data/1451809/000156459020008145/sitm-10k_20191231.htm |
| Solaredge Technologies, Inc. | 3674 | 2019 | 10-K | 2019-12-31 | 2020-02-27 | sedg10k2019.htm | https://www.sec.gov/Archives/edgar/data/1419612/000117891320000672/sedg10k2019.htm |
| Synaptics Inc | 3674 | 2018 | 10-K | 2018-06-30 | 2018-08-24 | syna-10k_20180630.htm | https://www.sec.gov/Archives/edgar/data/817720/000156459018022311/syna-10k_20180630.htm |
| Synaptics Inc | 3674 | 2019 | 10-K | 2019-06-29 | 2019-08-23 | syna-10k_20190629.htm | https://www.sec.gov/Archives/edgar/data/817720/000156459019032908/syna-10k_20190629.htm |
| Solaredge Technologies Inc | 3674 | 2018 | 10-K | 2018-12-31 | 2019-02-28 | zk1922755.htm | https://www.sec.gov/Archives/edgar/data/1419612/000117891319000721/zk1922755.htm |
| Ttm Technologies Inc | 3672 | 2018 | 10-K | 2018-01-01 | 2018-02-23 | d490922d10k.htm | https://www.sec.gov/Archives/edgar/data/1116942/000119312518055988/d490922d10k.htm |
| Ttm Technologies Inc | 3672 | 2018 | 10-K | 2018-12-31 | 2019-02-26 | ttmi-10k_20181231.htm | https://www.sec.gov/Archives/edgar/data/1116942/000156459019004520/ttmi-10k_20181231.htm |
| Ttm Technologies Inc | 3672 | 2019 | 10-K | 2019-12-30 | 2020-02-26 | ttmi-10k_20191230.htm | https://www.sec.gov/Archives/edgar/data/1116942/000156459020006477/ttmi-10k_20191230.htm |
| Xperi Corp | 3674 | 2018 | 10-K | 2018-12-31 | 2019-02-20 | xper-10k_20181231.htm | https://www.sec.gov/Archives/edgar/data/1690666/000156459019003460/xper-10k_20181231.htm |
| Xperi Corp | 3674 | 2019 | 10-K | 2019-12-31 | 2020-02-18 | xper-10k_20191231.htm | https://www.sec.gov/Archives/edgar/data/1690666/000156459020005044/xper-10k_20191231.htm |

(Totals: B1 31, B2 34 documents.)
