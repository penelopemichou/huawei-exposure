"""Step 4: build one quarterly revenue table -> data/processed/revenue_quarterly.csv

What it does, in order:
  1. Read the revenue values from the raw SEC files, using the tags chosen
     per company (in order of preference; see TAGS below).
  2. Keep only 3-month values (one quarter, 80-100 days: 13 or 14 weeks) and
     12-month values (full year). 6-month year-to-date values are dropped.
     Each value gets a FISCAL year and quarter (see fiscal_labels): fiscal
     years are named after the calendar year in which they end.
  3. Each quarter is usually reported in several filings. We keep:
       revenue_first_reported = value in the earliest filing (what an analyst knew then)
       revenue_latest         = value in the latest filing (after any restatements)
  4. Q4 is often not reported on its own, or only reported much later.
     Then Q4 = full year - Q1 - Q2 - Q3, or full year - the first-9-months
     total (the same sum; the only use of a year-to-date value). The first-reported
     Q4 is whichever way was public first; q4_derived = True when that was a
     derived value. See build_q4 for the details.
  5. Google Inc. and Alphabet are joined into one company, "Alphabet",
     after checking that the quarters both of them report agree.

Run from the project folder:
    .venv/bin/python src/build_quarterly.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

from companies import COMPANIES as COMPANY_LIST

PROJECT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT / "data" / "raw"
OUT_FILE = PROJECT / "data" / "processed" / "revenue_quarterly.csv"

# Revenue tags, in order of preference, per entity. Each list holds the
# company's TOTAL revenue under the names it used over time (the 2018
# revenue standard moved most companies to RevenueFromContract...).
# Sessions 0-3: chosen by Penelope in Session 0, Step 3.
# Session 4: chosen by the same rule; tags that were a segment or included
# other income in the same filing were put last or left out (see PROGRESS.md).
R, SRN, SGN = "Revenues", "SalesRevenueNet", "SalesRevenueGoodsNet"
EX = "RevenueFromContractWithCustomerExcludingAssessedTax"
IN = "RevenueFromContractWithCustomerIncludingAssessedTax"
TAGS = {
    "Mattel": [SRN, EX],
    "Caterpillar": [R],
    "Google Inc.": [R, SRN],
    # In 2019-2024 Alphabet tagged many quarters only with the second tag.
    # Where both exist they are the same number (14 of 14 in Step 3).
    "Alphabet Inc.": [R, EX],
    "Hasbro": [EX, SGN, SRN, R],          # Revenues was a segment in 2013-2015
    "Williams-Sonoma": [EX, SRN],
    "Best Buy": [IN, R, SRN],
    "Macy's": [EX, SRN],                  # Revenues includes credit-card income (+4 %)
    "Microsoft": [EX, SRN, R],
    # SalesRevenueServicesNet is total revenue in the 2015-2017 10-Qs but only
    # professional services elsewhere, so it comes last (used only if nothing else is there).
    "Salesforce": [EX, R, "SalesRevenueServicesNet"],
    "Netflix": [R],
    "Adobe": [R],
    "Deere": [R],                         # total incl. financial services, like Caterpillar
    "Cummins": [EX, R, SRN],
    "PACCAR": [R, SRN],                   # total incl. financial services
    "Parker-Hannifin": [EX, SRN, R],
    "Procter & Gamble": [SRN, R],         # Revenues was a part of sales in 2012-2013 filings
    "Colgate-Palmolive": [EX, SRN, R],
    "Clorox": [EX, R, SRN, SGN],
    "Church & Dwight": [EX, SGN],
    "General Mills": [EX, SGN],
    # forecast-gap, added 24 Nov 2026: Revenues covers 2010-2018 Q3, EX 2016 Q4 on;
    # the same number on all 6 quarters both cover. Advertising/other revenue are parts.
    "Meta Platforms": [EX, R],
    # huawei-exposure, added 25 Nov 2026: provisional tag order for every new entity (confirm per firm with
    # list_revenue_tags.py and check_data.py before forecasting; same order as src/eligibility_exact.py).
    "NEOPHOTONICS CORP": [EX, R, IN, SRN, SGN],
    "INPHI Corp": [EX, R, IN, SRN, SGN],
    "Lumentum Holdings Inc.": [EX, R, IN, SRN, SGN],
    "Qorvo, Inc.": [EX, R, IN, SRN, SGN],
    "MICRON TECHNOLOGY INC": [EX, R, IN, SRN, SGN],
    "FINISAR CORP": [EX, R, IN, SRN, SGN],
    "MACOM Technology Solutions Holdings, Inc.": [EX, R, IN, SRN, SGN],
    "SKYWORKS SOLUTIONS, INC.": [EX, R, IN, SRN, SGN],
    "Avago Technologies LTD": [EX, R, IN, SRN, SGN],
    "Broadcom Pte. Ltd.": [EX, R, IN, SRN, SGN],
    "Broadcom Inc.": [EX, R, IN, SRN, SGN],
    "QUALCOMM INC/DE": [EX, R, IN, SRN, SGN],
    "INTEL CORP": [EX, R, IN, SRN, SGN],
    "Enphase Energy, Inc.": [EX, R, IN, SRN, SGN],
    "AMBARELLA INC": [EX, R, IN, SRN, SGN],
    "MICROCHIP TECHNOLOGY INC": [EX, R, IN, SRN, SGN],
    "ADVANCED ENERGY INDUSTRIES INC": [EX, R, IN, SRN, SGN],
    "ADVANCED MICRO DEVICES INC": [EX, R, IN, SRN, SGN],
    "AMKOR TECHNOLOGY, INC.": [EX, R, IN, SRN, SGN],
    "AMPHENOL CORP /DE/": [EX, R, IN, SRN, SGN],
    "ANALOG DEVICES INC": [EX, R, IN, SRN, SGN],
    "AXT INC": [EX, R, IN, SRN, SGN],
    "BEL FUSE INC /NJ": [EX, R, IN, SRN, SGN],
    "BENCHMARK ELECTRONICS INC": [EX, R, IN, SRN, SGN],
    "CMC Materials, Inc.": [EX, R, IN, SRN, SGN],
    "CTS CORP": [EX, R, IN, SRN, SGN],
    "DIODES INC /DEL/": [EX, R, IN, SRN, SGN],
    "FIRST SOLAR, INC.": [EX, R, IN, SRN, SGN],
    "FORMFACTOR INC": [EX, R, IN, SRN, SGN],
    "IEC ELECTRONICS CORP": [EX, R, IN, SRN, SGN],
    "IPG PHOTONICS CORP": [EX, R, IN, SRN, SGN],
    "JABIL INC": [EX, R, IN, SRN, SGN],
    "KEY TRONIC CORP": [EX, R, IN, SRN, SGN],
    "Kimball Electronics, Inc.": [EX, R, IN, SRN, SGN],
    "LATTICE SEMICONDUCTOR CORP": [EX, R, IN, SRN, SGN],
    "MAGNACHIP SEMICONDUCTOR Corp": [EX, R, IN, SRN, SGN],
    "MAXIM INTEGRATED PRODUCTS INC": [EX, R, IN, SRN, SGN],
    "METHODE ELECTRONICS INC": [EX, R, IN, SRN, SGN],
    "MONOLITHIC POWER SYSTEMS, INC.": [EX, R, IN, SRN, SGN],
    "NORTECH SYSTEMS INC": [EX, R, IN, SRN, SGN],
    "NVIDIA CORP": [EX, R, IN, SRN, SGN],
    "OSI SYSTEMS INC": [EX, R, IN, SRN, SGN],
    "PHOTRONICS INC": [EX, R, IN, SRN, SGN],
    "PLEXUS CORP": [EX, R, IN, SRN, SGN],
    "POWER INTEGRATIONS INC": [EX, R, IN, SRN, SGN],
    "RAMBUS INC": [EX, R, IN, SRN, SGN],
    "SANMINA CORP": [EX, R, IN, SRN, SGN],
    "SILICON LABORATORIES INC.": [EX, R, IN, SRN, SGN],
    "SMTC CORP": [EX, R, IN, SRN, SGN],
    "SUNPOWER CORP": [EX, R, IN, SRN, SGN],
    "TEXAS INSTRUMENTS INC": [EX, R, IN, SRN, SGN],
    "Ultra Clean Holdings, Inc.": [EX, R, IN, SRN, SGN],
    "VIAVI SOLUTIONS INC.": [EX, R, IN, SRN, SGN],
    "VICOR CORP": [EX, R, IN, SRN, SGN],
    "ON SEMICONDUCTOR CORP": [EX, R, IN, SRN, SGN],
    "MAXLINEAR, INC": [EX, R, IN, SRN, SGN],
    "SEMTECH CORP": [EX, R, IN, SRN, SGN],
    "SYNAPTICS Inc": [EX, R, IN, SRN, SGN],
    "CYPRESS SEMICONDUCTOR CORP /DE/": [EX, R, IN, SRN, SGN],
    "DSP GROUP INC /DE/": [EX, R, IN, SRN, SGN],
    "APPLIED OPTOELECTRONICS, INC.": [EX, R, IN, SRN, SGN],
    "WOLFSPEED, INC.": [EX, R, IN, SRN, SGN],
    "MARVELL TECHNOLOGY GROUP LTD": [EX, R, IN, SRN, SGN],
    "CIRRUS LOGIC, INC.": [EX, R, IN, SRN, SGN],
    "ALPHA & OMEGA SEMICONDUCTOR Ltd": [EX, R, IN, SRN, SGN],
    "XILINX INC": [EX, R, IN, SRN, SGN],
}

# Company -> list of (raw file, entity name, tags in order of preference).
# Alphabet has two entries: Google Inc. (until 2015) and Alphabet Inc.
COMPANIES = {company: [(f"CIK{cik}.json", entity, TAGS[entity]) for cik, entity in entities]
             for company, (_, entities, _) in COMPANY_LIST.items()}

# A quarter: 13 weeks (90-92 days) or 14 weeks (97-98). 98 days is the longest
# real quarter; it also keeps out one mis-tagged Google value (Q3 2012 tagged
# from 22 June, 100 days).
QUARTER_DAYS = (80, 98)
NINE_MONTH_DAYS = (265, 285)  # first 9 months of the fiscal year; only used to derive Q4
YEAR_DAYS = (350, 380)        # a fiscal year: 52 weeks (364 days) to 53 weeks (371)
DAYS_PER_QUARTER = 91.3


# --- 1. Read the raw values ---------------------------------------------

def load_facts():
    """One row per (tag, period, filing) for the tags we chose."""
    rows = []
    for company, sources in COMPANIES.items():
        for file_name, entity, tags in sources:
            facts = json.loads((RAW_DIR / file_name).read_text())["facts"]["us-gaap"]
            for priority, tag in enumerate(tags):
                for v in facts.get(tag, {}).get("units", {}).get("USD", []):
                    if "start" not in v:      # skip values without a period
                        continue
                    rows.append({"company": company, "entity": entity, "tag": tag,
                                 "priority": priority, "start": v["start"], "end": v["end"],
                                 "val": v["val"], "accn": v["accn"], "form": v["form"],
                                 "filed": v["filed"]})
    df = pd.DataFrame(rows)
    for col in ["start", "end", "filed"]:
        df[col] = pd.to_datetime(df[col])
    return df


def fiscal_year_ends(entity_df):
    """The entity's fiscal-year end dates (anchors), from its 12-month periods,
    extended by one year at a time so that every period has an anchor after it."""
    ends = sorted(entity_df.loc[entity_df["kind"] == "year", "end"].unique())
    anchors = []
    for e in ends:                                   # merge near-duplicates (within 10 days)
        if not anchors or (e - anchors[-1]).days > 10:
            anchors.append(pd.Timestamp(e))
    year, slack = pd.Timedelta(days=365), pd.Timedelta(days=10)
    while anchors[0] - year >= entity_df["end"].min() - slack:
        anchors.insert(0, anchors[0] - year)
    while anchors[-1] < entity_df["end"].max():
        anchors.append(anchors[-1] + year)
    return anchors


def fiscal_labels(end, anchors):
    """(fiscal year, fiscal quarter, days off) for a period ending on `end`.

    The fiscal year is the first one ending on or after `end` (10 days of slack),
    named after the calendar year in which it ends. The quarter number counts
    back from that year end in steps of about 13 weeks: ending at the year end
    is Q4, about 13 weeks before it is Q3, and so on.
    """
    year_end = next(a for a in anchors if a >= end - pd.Timedelta(days=10))
    steps_back = (year_end - end).days / DAYS_PER_QUARTER
    quarter = 4 - int(round(steps_back))
    days_off = abs((year_end - end).days - round(steps_back) * DAYS_PER_QUARTER)
    return year_end.year, quarter, days_off


def prepare(df):
    """Keep quarters and full years, one value per period per filing."""
    days = (df["end"] - df["start"]).dt.days
    df["kind"] = None
    df.loc[days.between(*QUARTER_DAYS), "kind"] = "quarter"
    df.loc[days.between(*NINE_MONTH_DAYS), "kind"] = "nine-month"
    df.loc[days.between(*YEAR_DAYS), "kind"] = "year"
    df = df[df["kind"].notna()].copy()     # drops 6-month year-to-date values
    df["period_days"] = days + 1

    # Fiscal year and quarter from each entity's own fiscal-year ends
    # (not from calendar months: Microsoft's year ends in June, Best Buy's
    # around 31 January, and some companies use 52/53-week years).
    labels = []
    for entity, edf in df.groupby("entity", sort=False):
        anchors = fiscal_year_ends(edf)
        for i, end in edf["end"].items():
            labels.append((i, *fiscal_labels(end, anchors)))
    lab = pd.DataFrame(labels, columns=["i", "fiscal_year", "fiscal_quarter", "days_off"]).set_index("i")
    df = df.join(lab)

    # A quarter must sit within ~3 weeks of a quarter end, a full year must end
    # at a fiscal-year end, and a 9-month total at the end of Q3. Anything else
    # is reported and dropped.
    good = ((df["days_off"] <= 21) & df["fiscal_quarter"].between(1, 4) &
            (((df["kind"] == "quarter")) |
             ((df["kind"] == "year") & (df["fiscal_quarter"] == 4)) |
             ((df["kind"] == "nine-month") & (df["fiscal_quarter"] == 3))))
    odd = df[~good]
    if len(odd):
        print(f"Dropped {len(odd)} values with an unexpected end date:")
        print(odd[["entity", "tag", "start", "end", "kind"]].to_string(index=False))
    df = df[good].drop(columns="days_off").copy()

    # Full-year values only from annual reports (10-K, 10-K/A) and 8-K recasts:
    # a few 10-Qs reuse the revenue tag for other 12-month disclosures
    # (Church & Dwight's 2023 10-Qs: "2022" = $0.18 bn vs $5.38 bn in the 10-K).
    annual = df["form"].str.startswith("10-K") | df["form"].str.startswith("8-K")
    df = df[(df["kind"] != "year") | annual].copy()

    # A full-year value more than 25 % away from the first 10-K figure for the
    # same year is a mis-dated tag, not a restatement (the largest real
    # restatements here are about 13 %): Salesforce's 2018 10-K labels FY2016
    # revenue ($6.67 bn) with FY2013 dates. Such values are dropped.
    years = df[df["kind"] == "year"].sort_values(["filed", "accn"])
    first_10k = years.groupby(["entity", "fiscal_year"])["val"].transform("first")
    bad = years.index[(years["val"] / first_10k - 1).abs() > 0.25]
    if len(bad):
        print(f"Dropped {len(bad)} full-year values more than 25 % from the first 10-K figure:")
        print(df.loc[bad, ["entity", "tag", "start", "end", "val", "form", "filed"]].to_string(index=False))
    df = df.drop(index=bad)

    # If one filing has the same period under two of our tags, keep the
    # preferred tag (lowest priority number).
    df = (df.sort_values("priority")
            .drop_duplicates(["entity", "kind", "fiscal_year", "fiscal_quarter", "accn"])
            .sort_values(["filed", "accn"]))
    return df


# --- 2. One row per quarter ------------------------------------------------

def as_of(filings, date):
    """The latest value among filings made on or before `date`."""
    return filings[filings["filed"] <= date].iloc[-1]


def build_q4(quarters, years, nine_month, fy):
    """One Q4 row. There are up to three ways to get Q4:
         direct:  a 3-month Q4 value in a filing
         derived: full year - Q1 - Q2 - Q3
         derived: full year - first-9-months total (same sum; used for 2008-2009,
                  where Q1 is missing or became public late)
    """
    direct = quarters[(quarters["fiscal_year"] == fy) & (quarters["fiscal_quarter"] == 4)]
    year = years[years["fiscal_year"] == fy]

    # The pieces that add up to the first 9 months, in two versions.
    options = []
    q123 = [quarters[(quarters["fiscal_year"] == fy) & (quarters["fiscal_quarter"] == q)]
            for q in (1, 2, 3)]
    if all(len(p) for p in q123):
        options.append(q123)
    if len(nine_month[nine_month["fiscal_year"] == fy]):
        options.append([nine_month[nine_month["fiscal_year"] == fy]])
    if year.empty:
        options = []

    # Each way gives a value and the day it became known.
    candidates = []   # (date known, value, derived?, tag)
    if len(direct):
        candidates.append((direct["filed"].iloc[0], direct["val"].iloc[0], False,
                           direct["tag"].iloc[0]))
    for parts in options:
        date = max([year["filed"].min()] + [p["filed"].min() for p in parts])
        year_then = as_of(year, date)
        value = year_then["val"] - sum(as_of(p, date)["val"] for p in parts)
        candidates.append((date, value, True, year_then["tag"]))
    if not candidates:
        return None
    candidates.sort(key=lambda c: c[0])

    # First reported = the earliest way. But if the ways disagree, an early
    # one mixed old and restated pieces (Google 2012: Motorola Home was
    # removed from the full year before the 9-month total was restated). Then take
    # the earliest way that agrees (within 0.5 %) with the newest one.
    newest = candidates[-1][1]
    date, first, derived, tag = next(c for c in candidates if abs(c[1] / newest - 1) <= 0.005)

    # Latest = the latest direct Q4 value; otherwise full year - latest pieces.
    # The full year must be on the same basis as the pieces, so we take it
    # from the first filing on or after the pieces were last restated.
    # (Google 2013: quarters restated in 2014 10-Qs, full year in the 2015
    # 10-K. Google 2012: full year restated in 2015, but the 2012 quarters
    # never were, so the 2015 full year is not used.)
    if len(direct):
        latest, period_end = direct["val"].iloc[-1], direct["end"].iloc[-1]
        days = direct["period_days"].iloc[-1]
    else:
        parts = options[0]
        pieces_last_filed = max(p["filed"].max() for p in parts)
        later = year[year["filed"] >= pieces_last_filed]
        year_same_basis = later.iloc[0] if len(later) else year.iloc[-1]
        latest = year_same_basis["val"] - sum(p["val"].iloc[-1] for p in parts)
        period_end = year["end"].iloc[-1]
        days = (period_end - parts[-1]["end"].iloc[-1]).days    # from the end of Q3

    return {"period_end": period_end.date(), "revenue_first_reported": first,
            "revenue_latest": latest, "first_filed_date": date.date(),
            "source_tag": tag, "q4_derived": derived, "period_days": days}


def build_table(df, name):
    """Quarterly table for one company (or one entity) from its filings."""
    quarters = df[df["kind"] == "quarter"]
    years = df[df["kind"] == "year"]
    nine_month = df[df["kind"] == "nine-month"]
    rows = []
    for fy in sorted(set(quarters["fiscal_year"]) | set(years["fiscal_year"])):
        for fq in (1, 2, 3, 4):
            filings = quarters[(quarters["fiscal_year"] == fy) &
                               (quarters["fiscal_quarter"] == fq)]
            if fq == 4:                           # direct or derived
                row = build_q4(quarters, years, nine_month, fy)
            elif len(filings):                    # reported as a 3-month value
                first, last = filings.iloc[0], filings.iloc[-1]
                row = {"period_end": last["end"].date(),
                       "revenue_first_reported": first["val"],
                       "revenue_latest": last["val"],
                       "first_filed_date": first["filed"].date(),
                       "source_tag": first["tag"], "q4_derived": False,
                       "period_days": last["period_days"]}
            else:
                row = None
            if row:
                rows.append({"company": name, "fiscal_year": fy, "fiscal_quarter": fq, **row})
    return pd.DataFrame(rows)


# --- 3. Check Google Inc. against Alphabet Inc. --------------------------

def check_google_alphabet(df):
    """Compare the quarters that both Google Inc. and Alphabet Inc. report."""
    a = df[df["company"] == "Alphabet"]
    google = build_table(a[a["entity"] == "Google Inc."], "Google Inc.")
    alphabet = build_table(a[a["entity"] == "Alphabet Inc."], "Alphabet Inc.")
    both = google.merge(alphabet, on=["fiscal_year", "fiscal_quarter"],
                        suffixes=("_google", "_alphabet"))
    print("\nQuarters reported by both Google Inc. and Alphabet Inc.:")
    if both.empty:
        print("  none")
        return
    both["diff_latest_%"] = 100 * (both["revenue_latest_alphabet"] /
                                   both["revenue_latest_google"] - 1)
    cols = ["fiscal_year", "fiscal_quarter", "revenue_latest_google",
            "revenue_latest_alphabet", "diff_latest_%",
            "first_filed_date_google", "first_filed_date_alphabet"]
    print(both[cols].to_string(index=False))


# --- 4. Run everything -----------------------------------------------------

def main():
    df = prepare(load_facts())
    check_google_alphabet(df)

    # Joined table: Google Inc. and Alphabet Inc. filings are pooled, so
    # "first reported" is the earliest filing of either one.
    table = pd.concat([build_table(df[df["company"] == c], c) for c in COMPANIES],
                      ignore_index=True)
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(OUT_FILE, index=False)

    print(f"\nSaved {len(table)} rows to {OUT_FILE.relative_to(PROJECT)}\n")
    for company, t in table.groupby("company", sort=False):
        print(f"{company:<12} {len(t):>3} quarters, "
              f"{t.iloc[0]['fiscal_year']} Q{t.iloc[0]['fiscal_quarter']} to "
              f"{t.iloc[-1]['fiscal_year']} Q{t.iloc[-1]['fiscal_quarter']}, "
              f"Q4 derived {t['q4_derived'].sum()} times")


if __name__ == "__main__":
    main()
