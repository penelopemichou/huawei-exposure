# Stage C: revenue files (XBRL companyfacts), 45 files — DONE 25 Nov 2026 (Penelope's "yes")

Result: 45 of 45 saved, 153.5 MB (largest 4.8 MB, First Solar), 0 errors. Quarter counts (no values): `results/quarter_counts_all.csv`.

Drafted 25 Nov 2026, after the class table was confirmed. Nothing downloaded.

- **Source:** `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` (one request per firm, 0.5 s apart, logged).
- **Saved as:** `data/raw/filing_lists/companyfacts/CIK##########.json` (gitignored), next to the 7 files already there (6 exposed firms + Intel).
- **Size:** unknown until downloaded. The 7 files so far were 1.8–4.4 MB, so expect about 2–5 MB each, **about 90–200 MB in all**.
- **Stops:** any single file over 10 MB is not saved (stop and tell); the run stops before passing 200 MB in total.
- **What is printed after the download:** only counts of quarters and first-quarter dates per firm (as in `results/quarter_counts.csv`); no revenue value, no forecast, no miss.
- **Broadcom:** its own file is in the list. If it has fewer than 20 quarters before the origin, its predecessor's file is proposed separately (design-v2 (c)), not downloaded now.

| # | group | comparison | firm | CIK | file |
|---|---|---|---|---|---|
| 1 | donor | PRIMARY | ADVANCED MICRO DEVICES INC | 0000002488 | CIK0000002488.json |
| 2 | donor | PRIMARY | AMBARELLA INC | 0001280263 | CIK0001280263.json |
| 3 | donor | PRIMARY | ANALOG DEVICES INC | 0000006281 | CIK0000006281.json |
| 4 | donor | PRIMARY | DIODES INC /DEL/ | 0000029002 | CIK0000029002.json |
| 5 | donor | PRIMARY | LATTICE SEMICONDUCTOR CORP | 0000855658 | CIK0000855658.json |
| 6 | donor | PRIMARY | MAGNACHIP SEMICONDUCTOR Corp | 0001325702 | CIK0001325702.json |
| 7 | donor | PRIMARY | MAXIM INTEGRATED PRODUCTS INC | 0000743316 | CIK0000743316.json |
| 8 | donor | PRIMARY | MICROCHIP TECHNOLOGY INC | 0000827054 | CIK0000827054.json |
| 9 | donor | PRIMARY | MONOLITHIC POWER SYSTEMS, INC. | 0001280452 | CIK0001280452.json |
| 10 | donor | PRIMARY | NVIDIA CORP | 0001045810 | CIK0001045810.json |
| 11 | donor | PRIMARY | POWER INTEGRATIONS INC | 0000833640 | CIK0000833640.json |
| 12 | donor | PRIMARY | SILICON LABORATORIES INC. | 0001038074 | CIK0001038074.json |
| 13 | donor | PRIMARY | TEXAS INSTRUMENTS INC | 0000097476 | CIK0000097476.json |
| 14 | donor | sensitivity | ADVANCED ENERGY INDUSTRIES INC | 0000927003 | CIK0000927003.json |
| 15 | donor | sensitivity | AMKOR TECHNOLOGY, INC. | 0001047127 | CIK0001047127.json |
| 16 | donor | sensitivity | AMPHENOL CORP /DE/ | 0000820313 | CIK0000820313.json |
| 17 | donor | sensitivity | AXT INC | 0001051627 | CIK0001051627.json |
| 18 | donor | sensitivity | BEL FUSE INC /NJ | 0000729580 | CIK0000729580.json |
| 19 | donor | sensitivity | BENCHMARK ELECTRONICS INC | 0000863436 | CIK0000863436.json |
| 20 | donor | sensitivity | CMC Materials, Inc. | 0001102934 | CIK0001102934.json |
| 21 | donor | sensitivity | CTS CORP | 0000026058 | CIK0000026058.json |
| 22 | donor | sensitivity | Enphase Energy, Inc. | 0001463101 | CIK0001463101.json |
| 23 | donor | sensitivity | FIRST SOLAR, INC. | 0001274494 | CIK0001274494.json |
| 24 | donor | sensitivity | FORMFACTOR INC | 0001039399 | CIK0001039399.json |
| 25 | donor | sensitivity | IEC ELECTRONICS CORP | 0000049728 | CIK0000049728.json |
| 26 | donor | sensitivity | IPG PHOTONICS CORP | 0001111928 | CIK0001111928.json |
| 27 | donor | sensitivity | JABIL INC | 0000898293 | CIK0000898293.json |
| 28 | donor | sensitivity | KEY TRONIC CORP | 0000719733 | CIK0000719733.json |
| 29 | donor | sensitivity | Kimball Electronics, Inc. | 0001606757 | CIK0001606757.json |
| 30 | donor | sensitivity | METHODE ELECTRONICS INC | 0000065270 | CIK0000065270.json |
| 31 | donor | sensitivity | NORTECH SYSTEMS INC | 0000722313 | CIK0000722313.json |
| 32 | donor | sensitivity | OSI SYSTEMS INC | 0001039065 | CIK0001039065.json |
| 33 | donor | sensitivity | PHOTRONICS INC | 0000810136 | CIK0000810136.json |
| 34 | donor | sensitivity | PLEXUS CORP | 0000785786 | CIK0000785786.json |
| 35 | donor | sensitivity | RAMBUS INC | 0000917273 | CIK0000917273.json |
| 36 | donor | sensitivity | SANMINA CORP | 0000897723 | CIK0000897723.json |
| 37 | donor | sensitivity | SMTC CORP | 0001108320 | CIK0001108320.json |
| 38 | donor | sensitivity | SUNPOWER CORP | 0000867773 | CIK0000867773.json |
| 39 | donor | sensitivity | Ultra Clean Holdings, Inc. | 0001275014 | CIK0001275014.json |
| 40 | donor | sensitivity | VIAVI SOLUTIONS INC. | 0000912093 | CIK0000912093.json |
| 41 | donor | sensitivity | VICOR CORP | 0000751978 | CIK0000751978.json |
| 42 | low exposure, implied | own rows | Broadcom Inc. | 0001730168 | CIK0001730168.json |
| 43 | low exposure, implied | own rows | MACOM Technology Solutions Holdings, Inc. | 0001493594 | CIK0001493594.json |
| 44 | low exposure, implied | own rows | QUALCOMM INC/DE | 0000804328 | CIK0000804328.json |
| 45 | low exposure, implied | own rows | SKYWORKS SOLUTIONS, INC. | 0000004127 | CIK0000004127.json |
