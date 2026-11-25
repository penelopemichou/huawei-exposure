"""Guidance-cut table (separate step, after the main run). Ranges are copied verbatim, by hand, from
the saved 8-K filings (src/guidance_extract.py; results/guidance_sentences.csv). Midpoint change is
computed from the verbatim ranges. The h = 1 model miss (descriptive) comes from results/results_by_firm_long.csv.

Run (bash):  ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/guidance_table.py
"""

import re
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
NO8K = "no 8-K found after 16 May"
NOPRE = "no pre-event guidance for this quarter"
MID = "mid-quarter update"
NOGUIDE = "no guidance range in the filed 8-K"
NOREV = "no revision in the filed 8-Ks"

# firm, group, dose, quarter guided,
# before (verbatim, date, accession), after (verbatim, date, accession), flags, revision names Huawei?, notes
ROWS = [
    ("Neophotonics", "Exposed (primary)", "46%", "2019 Q2",
     ("$88 to $93 million", "2019-05-02", "0001227025-19-000035"), ("", "", ""), NO8K, "n/a", ""),
    ("Inphi", "Exposed (primary)", "14%", "2019 Q2",
     ("$86.8 million to $90.8 million", "2019-04-30", "0001437749-19-008324"),
     ("$82.3 million to $86.3 million", "2019-05-22", "0001437749-19-010660"), MID, "yes", ""),
    ("Qorvo", "Exposed (primary)", "13%", "FY2020 Q1",
     ("$780 million to $800 million", "2019-05-07", "0001604778-19-000025"),
     ("$730 million to $750 million", "2019-05-21", "0001604778-19-000035"), MID, "yes",
     "25 Jun 8-K (items 1.01/8.01): no guidance"),
    ("Micron Technology", "Exposed (primary)", "12% (fallback)", "FY2019 Q3 (ends 30 May)",
     ("", "2019-03-20", "0000723125-19-000012"), ("", "", ""), f"{NOGUIDE}; {NO8K}", "n/a",
     "release says guidance is given on the conference call"),
    ("Finisar", "Exposed (primary)", "10%", "FY2020 Q1",
     ("", "2019-02-28", "0001171843-19-001376"), ("", "2019-06-13", "0001171843-19-003983"), f"{NOPRE}; {NOGUIDE}", "n/a",
     "merger with II-VI pending; 'will not hold an earnings call'; no outlook in either release"),
    ("Lumentum", "Exposed (secondary)", "11.0%", "FY2019 Q4",
     ("$405 million to $425 million", "2019-05-07", "0001633978-19-000029"), ("", "", ""), NO8K, "n/a", ""),
    ("MACOM", "Low exposure", "n/a", "FY2019 Q3",
     ("$120 million to $124 million", "2019-05-07", "0001493594-19-000020"),
     ("$107 million and $109 million", "2019-06-18", "0001493594-19-000034"), MID, "yes",
     "also cites reduced shipments to distribution partners"),
    ("Skyworks Solutions", "Low exposure", "n/a", "FY2019 Q3",
     ("$815 and $835 million", "2019-05-02", "0000004127-19-000020"),
     ("$755 million and $775 million", "2019-06-04", "0000004127-19-000029"), MID, "yes",
     "8-K: 'sales to Huawei were approximately 12 percent' of H1 FY2019 revenue"),
    ("Broadcom", "Low exposure", "n/a", "FY2019 Q3",
     ("", "2019-03-14", "0001193125-19-074832"), ("", "2019-06-13", "0001193125-19-172516"), f"{NOPRE} (annual outlook only)", "no (not in the filed text)",
     "annual outlook: '$24.5 billion' (14 Mar) -> '$22.5 billion' (13 Jun); not a quarter guidance"),
    ("Qualcomm", "Low exposure", "n/a", "FY2019 Q3",
     ("", "2019-05-01", "0001728949-19-000034"), ("", "", ""), f"{NOGUIDE}; {NO8K}", "n/a",
     "release: Q3 guidance includes $4.5-4.7 billion Apple settlement and $150 million Huawei royalties; no overall range found"),
    ("ON Semiconductor", "Low exposure", "n/a", "2019 Q2",
     ("$1,360 to $1,410 million", "2019-04-29", "0001193125-19-123574"), ("", "", ""), NOREV, "n/a",
     "19 Jun 8-K (item 8.01): no guidance"),
    ("MaxLinear", "Low exposure", "n/a", "2019 Q2",
     ("$83 million to $88 million", "2019-05-01", "0001288469-19-000056"),
     ("$80 million to $85 million", "2019-06-04", "0001288469-19-000103"), MID, "yes", ""),
    ("Semtech", "Low exposure", "n/a", "FY2020 Q2",
     ("", "2019-03-13", "0001157523-19-000599"), ("$128.0 million to $142.0 million", "2019-05-29", "0001157523-19-001317"), NOPRE, "yes",
     "13 Mar release guided FY2020 Q1 ('$125.0 million to $135.0 million'), not this quarter"),
    ("Synaptics", "Low exposure", "n/a", "FY2019 Q4",
     ("$300 to $320 million", "2019-05-09", "0001193125-19-143042"), ("", "", ""), NO8K, "n/a", ""),
    ("Cypress", "Low exposure", "n/a", "2019 Q2",
     ("$515 million to $545 million", "2019-04-25", "0000791915-19-000009"), ("", "", ""), NOREV, "n/a",
     "five 8-Ks in June (merger with Infineon): no guidance"),
    ("DSP Group", "Low exposure", "n/a", "2019 Q2",
     ("", "2019-05-06", "0001437749-19-008757"), ("", "", ""), f"{NOGUIDE}; {NO8K}", "n/a",
     "release says the outlook is given on the conference call"),
    ("Applied Optoelectronics", "Low exposure", "n/a", "2019 Q2",
     ("$40 million to $45 million", "2019-05-08", "0001683168-19-001413"), ("", "", ""), NO8K, "n/a", ""),
    ("Cree / Wolfspeed", "Low exposure", "n/a", "FY2019 Q4",
     ("$263 million to $271 million", "2019-05-01", "0000895419-19-000014"),
     ("$245 million to $252 million", "2019-06-11", "0000895419-19-000035"), MID, "yes",
     "continuing operations; also cites softer LED demand"),
    ("Marvell", "Low exposure", "n/a", "FY2020 Q2",
     ("", "2019-05-06", "0001193125-19-137573"), ("$650 million +/- 3%", "2019-05-30", "0001058057-19-000013"), NOPRE, "no (not in the filed text)",
     "6 May 8-K: preliminary Q1 results only"),
    ("Cirrus Logic", "Low exposure", "n/a", "FY2020 Q1",
     ("$200 million and $240 million", "2019-05-01", "0001157523-19-001015"), ("(reaffirmed)", "2019-05-20", "0001157523-19-001266"),
     f"{MID}; {NOREV}", "yes",
     "20 May Q&A: 'there is no material impact to the guidance we've provided for the current quarter'"),
    ("Alpha & Omega", "Low exposure", "n/a", "FY2019 Q4",
     ("$110 million to $114 million", "2019-05-02", "0001157523-19-001055"), ("", "", ""), NO8K, "n/a", ""),
    ("Xilinx", "Low exposure", "n/a", "FY2020 Q1",
     ("$835M - $865M", "2019-04-24", "0000743988-19-000009"), ("", "", ""), NO8K, "n/a", ""),
]
SESSION0 = {"Qorvo": "about -6%", "Lumentum": "about -8%", "Skyworks Solutions": "about -7%"}


def midpoint(text):
    t = text.replace(",", "")
    if "+/-" in t:
        return float(re.search(r"\$(\d+(?:\.\d+)?)", t).group(1))
    nums = [float(x) for x in re.findall(r"\$?(\d+(?:\.\d+)?)\s*(?:million|M|billion)?", t) if x]
    nums = [n for n in nums if n > 0][:2]
    return sum(nums) / 2 if len(nums) == 2 else None


def main():
    miss = pd.read_csv(PROJECT / "results" / "results_by_firm_long.csv")
    m1 = miss[miss.h == 1].set_index("company")
    out = []
    for firm, group, dose, quarter, before, after, flags, huawei, note in ROWS:
        mb, ma = midpoint(before[0]) if before[0] else None, midpoint(after[0]) if after[0] and after[0] != "(reaffirmed)" else None
        change = round(100 * (ma - mb) / mb, 2) if mb and ma else None
        s0 = SESSION0.get(firm, "")
        if s0:
            s0 = f"{s0}: " + (f"filing gives {change:+.1f}%" if change is not None else "unsourced, not used (not in any filing)")
        out.append({"firm": firm, "group": group, "Huawei dose": dose, "quarter guided": quarter,
                    "range before (verbatim)": before[0] or "-", "before date": before[1], "before accession": before[2],
                    "range after (verbatim)": after[0] or "-", "after date": after[1], "after accession": after[2],
                    "midpoint change %": change if change is not None else "", "flags": flags,
                    "revision names Huawei?": huawei, "Session 0 note vs filing": s0,
                    "h = 1 model miss, AVG % (descriptive)": round(m1.loc[firm, "AVG"], 1) if firm in m1.index else "",
                    "notes": note})
    d = pd.DataFrame(out)
    d.to_csv(PROJECT / "results" / "guidance_cut_table.csv", index=False)
    pd.set_option("display.width", 320, "display.max_rows", 100, "display.max_colwidth", 44)
    print(d[["firm", "group", "Huawei dose", "quarter guided", "range before (verbatim)", "before date", "range after (verbatim)",
             "after date", "midpoint change %", "revision names Huawei?", "h = 1 model miss, AVG % (descriptive)", "flags"]].to_string(index=False))
    print("\nSession 0 note vs filings:")
    for _, r in d[d["Session 0 note vs filing"] != ""].iterrows():
        print(f"  {r.firm}: {r['Session 0 note vs filing']}")
    print("\nAccession numbers and notes: results/guidance_cut_table.csv")


if __name__ == "__main__":
    main()
