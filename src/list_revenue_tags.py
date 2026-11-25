"""Step 3: which us-gaap tags hold each company's revenue, and for which years?

Companies changed tag names over time (new accounting rules, new
preferences), so one company's revenue can sit under several tags.
This script lists every revenue-like tag with:
  - how many values it has, and how many of those are 3-month or 12-month values
  - the first and last period it covers
Then it compares tags where they cover the same period, so we can see
which tags mean "total revenue" and which hold only a piece of it.

Run from the project folder:
    .venv/bin/python src/list_revenue_tags.py
"""

import json
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT / "data" / "raw"

FILES = {
    "Mattel": "CIK0000063276.json",
    "Caterpillar": "CIK0000018230.json",
    "Google Inc.": "CIK0001288776.json",
    "Alphabet": "CIK0001652044.json",
    "Meta": "CIK0001326801.json",        # forecast-gap, added 24 Nov 2026
    # huawei-exposure, added 25 Nov 2026
    "NEOPHOTONICS CORP": "CIK0001227025.json",
    "INPHI Corp": "CIK0001160958.json",
    "Lumentum Holdings Inc.": "CIK0001633978.json",
    "Qorvo, Inc.": "CIK0001604778.json",
    "MICRON TECHNOLOGY INC": "CIK0000723125.json",
    "FINISAR CORP": "CIK0001094739.json",
    "MACOM Technology Solutions Holdings, Inc.": "CIK0001493594.json",
    "SKYWORKS SOLUTIONS, INC.": "CIK0000004127.json",
    "Avago Technologies LTD": "CIK0001441634.json",
    "Broadcom Pte. Ltd.": "CIK0001649338.json",
    "Broadcom Inc.": "CIK0001730168.json",
    "QUALCOMM INC/DE": "CIK0000804328.json",
    "INTEL CORP": "CIK0000050863.json",
    "Enphase Energy, Inc.": "CIK0001463101.json",
    "AMBARELLA INC": "CIK0001280263.json",
    "MICROCHIP TECHNOLOGY INC": "CIK0000827054.json",
    "ADVANCED ENERGY INDUSTRIES INC": "CIK0000927003.json",
    "ADVANCED MICRO DEVICES INC": "CIK0000002488.json",
    "AMKOR TECHNOLOGY, INC.": "CIK0001047127.json",
    "AMPHENOL CORP /DE/": "CIK0000820313.json",
    "ANALOG DEVICES INC": "CIK0000006281.json",
    "AXT INC": "CIK0001051627.json",
    "BEL FUSE INC /NJ": "CIK0000729580.json",
    "BENCHMARK ELECTRONICS INC": "CIK0000863436.json",
    "CMC Materials, Inc.": "CIK0001102934.json",
    "CTS CORP": "CIK0000026058.json",
    "DIODES INC /DEL/": "CIK0000029002.json",
    "FIRST SOLAR, INC.": "CIK0001274494.json",
    "FORMFACTOR INC": "CIK0001039399.json",
    "IEC ELECTRONICS CORP": "CIK0000049728.json",
    "IPG PHOTONICS CORP": "CIK0001111928.json",
    "JABIL INC": "CIK0000898293.json",
    "KEY TRONIC CORP": "CIK0000719733.json",
    "Kimball Electronics, Inc.": "CIK0001606757.json",
    "LATTICE SEMICONDUCTOR CORP": "CIK0000855658.json",
    "MAGNACHIP SEMICONDUCTOR Corp": "CIK0001325702.json",
    "MAXIM INTEGRATED PRODUCTS INC": "CIK0000743316.json",
    "METHODE ELECTRONICS INC": "CIK0000065270.json",
    "MONOLITHIC POWER SYSTEMS, INC.": "CIK0001280452.json",
    "NORTECH SYSTEMS INC": "CIK0000722313.json",
    "NVIDIA CORP": "CIK0001045810.json",
    "OSI SYSTEMS INC": "CIK0001039065.json",
    "PHOTRONICS INC": "CIK0000810136.json",
    "PLEXUS CORP": "CIK0000785786.json",
    "POWER INTEGRATIONS INC": "CIK0000833640.json",
    "RAMBUS INC": "CIK0000917273.json",
    "SANMINA CORP": "CIK0000897723.json",
    "SILICON LABORATORIES INC.": "CIK0001038074.json",
    "SMTC CORP": "CIK0001108320.json",
    "SUNPOWER CORP": "CIK0000867773.json",
    "TEXAS INSTRUMENTS INC": "CIK0000097476.json",
    "Ultra Clean Holdings, Inc.": "CIK0001275014.json",
    "VIAVI SOLUTIONS INC.": "CIK0000912093.json",
    "VICOR CORP": "CIK0000751978.json",
    "ON SEMICONDUCTOR CORP": "CIK0001097864.json",
    "MAXLINEAR, INC": "CIK0001288469.json",
    "SEMTECH CORP": "CIK0000088941.json",
    "SYNAPTICS Inc": "CIK0000817720.json",
    "CYPRESS SEMICONDUCTOR CORP /DE/": "CIK0000791915.json",
    "DSP GROUP INC /DE/": "CIK0000915778.json",
    "APPLIED OPTOELECTRONICS, INC.": "CIK0001158114.json",
    "WOLFSPEED, INC.": "CIK0000895419.json",
    "MARVELL TECHNOLOGY GROUP LTD": "CIK0001058057.json",
    "CIRRUS LOGIC, INC.": "CIK0000772406.json",
    "ALPHA & OMEGA SEMICONDUCTOR Ltd": "CIK0001387467.json",
    "XILINX INC": "CIK0000743988.json",
}

# A tag is "revenue-like" if its name contains "Revenue" but none of
# these words. They mark tags that are about revenue without being
# revenue earned in a period (for example deferred revenue is a balance,
# cost of revenue is a cost).
NOT_REVENUE = ["Cost", "Deferred", "Remaining", "Liability", "ProForma",
               "EquityMethod", "Disposal", "Percentage", "Sublease", "Receivable"]


def is_revenue_like(tag):
    return "Revenue" in tag and not any(word in tag for word in NOT_REVENUE)


# --- 1. Put every revenue-like value into one table ----------------------

rows = []
for company, file_name in FILES.items():
    facts = json.loads((RAW_DIR / file_name).read_text())["facts"]["us-gaap"]
    for tag, info in facts.items():
        if not is_revenue_like(tag):
            continue
        for value in info["units"].get("USD", []):
            rows.append({"company": company, "tag": tag, **value})

df = pd.DataFrame(rows)
df["start"] = pd.to_datetime(df["start"])
df["end"] = pd.to_datetime(df["end"])
df["days"] = (df["end"] - df["start"]).dt.days

# Kind of period, by its length in days.
df["kind"] = "other"
df.loc[df["days"].between(85, 95), "kind"] = "3-month"
df.loc[df["days"].between(350, 380), "kind"] = "12-month"


# --- 2. One summary row per company and tag ------------------------------

def summarise(group):
    q = group[group["kind"] == "3-month"]
    return pd.Series({
        "values": len(group),
        "periods": group[["start", "end"]].drop_duplicates().shape[0],
        "3-month": q[["start", "end"]].drop_duplicates().shape[0],
        "12-month": group.loc[group["kind"] == "12-month", ["start", "end"]]
                         .drop_duplicates().shape[0],
        "first_end": group["end"].min().date(),
        "last_end": group["end"].max().date(),
        "filings": group["accn"].nunique(),
    })

summary = (df.groupby(["company", "tag"]).apply(summarise, include_groups=False)
             .reset_index()
             .sort_values("first_end"))

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
print("REVENUE-LIKE TAGS (USD values; periods = distinct start/end pairs)\n")
for company in FILES:
    print(f"== {company}")
    print(summary[summary["company"] == company].drop(columns="company")
                 .to_string(index=False))
    print()


# --- 3. Compare tags on the same 3-month periods -------------------------
# For each period we take the value from the latest filing (just for this
# comparison), then divide each tag by the company's main candidate tags.

latest = (df[df["kind"] == "3-month"]
          .sort_values("filed")
          .groupby(["company", "tag", "start", "end"])["val"].last()
          .reset_index())
wide = latest.pivot_table(index=["company", "start", "end"], columns="tag", values="val")

MAIN_TAGS = ["Revenues", "SalesRevenueNet",
             "RevenueFromContractWithCustomerExcludingAssessedTax"]

print("TAG ÷ MAIN TAG, on 3-month periods both tags cover")
print("(1.000 = same number; median, and how many periods match within 0.1%)\n")
for company in FILES:
    w = wide.loc[company].dropna(axis=1, how="all")
    lines = []
    for main in [t for t in MAIN_TAGS if t in w]:
        for other in w.columns:
            if other == main:
                continue
            both = w[[main, other]].dropna()
            if both.empty:
                continue
            ratio = both[other] / both[main]
            same = (ratio - 1).abs().le(0.001).sum()
            lines.append(f"  {other:<52} ÷ {main:<52} n={len(both):>3}  "
                         f"median {ratio.median():.3f}  same {same}/{len(both)}")
    print(f"== {company}")
    print("\n".join(lines) if lines else "  (no overlapping 3-month periods)")
    print()
