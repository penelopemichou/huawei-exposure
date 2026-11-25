"""Session 2, Stage B: proposed labels for results/huawei_sentences.csv (no internet).

Huawei/HiSilicon rows get one of the five labels in notes/donor-rule.md:
    customer with % / customer without % / indirect / competitor/other / unclear
First simple text rules propose a label; then OVERRIDES (row number -> label) holds
every change made after reading the row by hand. A row in OVERRIDES is marked "(read)".
Rows without Huawei get a descriptive label instead:
    10% paragraph / table row / unnamed customer

Run from the project folder (prints every Huawei row with its label):
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/label_sentences.py [B1|B2a|B2c|B3]
"""

import csv
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
import sys
STAGE = sys.argv[1] if len(sys.argv) > 1 else "B1"
CSV = PROJECT / "results" / ("huawei_sentences.csv" if STAGE == "B1" else f"huawei_sentences_{STAGE}.csv")

HUAWEI = re.compile(r"huawei|hisilicon", re.I)
PCT = re.compile(r"\d+(\.\d+)?\s?%|ten percent", re.I)
REVENUE = re.compile(r"revenue|net sales", re.I)
CUSTOMER_CUES = re.compile(
    r"our customers?\b|customers? include|key customers|sales? (of [\w ]+ )?to huawei|sell(ing)? .{0,60}to huawei"
    r"|sold to huawei|shipments? (of [\w ]+ )?to huawei|huawei revenue|revenue from huawei|demand for our products"
    r"|royalt|licens(e|ee)s?\b|business with huawei|largest customers?|dependent on huawei|one of our customers"
    r"|purchases from us|supplier to huawei|orders from huawei|eligible accounts|concentration limits|our sales"
    r"|other foreign customers|huawei demand|lawfully sold|ceased|suspend|resumed|vmi\b|work with huawei"
    r"|from that customer|growth between huawei and us|our revenue|future revenue|reduced shipments|net revenue"
    r"|inventory-related charge|we sell our products", re.I)

# Changes after reading each row by hand (row number in the CSV -> label), 25 Nov 2026.
# Row numbers refer to results/huawei_sentences.csv as written by extract_sentences.py B1.
W, P, O, U = "customer with %", "customer without %", "competitor/other", "unclear"
OVERRIDES_B1 = {
    15: O,                       # Acacia: general description of the Entity List licence rules
    36: O,                       # Broadcom: competitor list ("our customer relationships" misled the rule)
    52: P, 59: P,                # Finisar: % of its Huawei revenue / % of receivables, not share of total revenue
    88: O, 90: O, 93: O,         # Inphi: general Entity List / Temporary General License descriptions
    113: P, 143: P,              # Lumentum: customer list next to a "10%" table heading, no Huawei share
    117: W, 147: W,              # Lumentum: table rows "HUAWEI 11.0% / 15.2%"
    159: P, 161: P,              # Lumentum: Huawei buying from competitors / customised products for Huawei
    211: U,                      # Micron: "unable to predict ... long-term effects on our business"
    221: P, 240: P,              # NeoPhotonics FY2018: strategic customers incl. Huawei / table footnote
    237: W, 243: W,              # NeoPhotonics FY2018: table rows "Huawei 46% / 40% / 50%"
    246: P, 260: P, 283: P,      # NeoPhotonics FY2019: customers incl. Huawei / Huawei demand / shipment suspension
    268: O, 276: U,              # NeoPhotonics FY2019: general Entity List effect / "this trend may accelerate"
    287: W, 298: W,              # NeoPhotonics FY2019: table rows "Huawei 41% / 46% / 40%"
    302: P, 316: P, 339: P,      # NeoPhotonics FY2019 10-K/A: the same rows as 246, 260, 283
    324: O, 332: U,              # 10-K/A: the same rows as 268, 276
    343: W, 354: W,              # 10-K/A: the same rows as 287, 298
    366: U, 379: U,              # Qorvo: "unable to predict ... effects on our business"
    371: O,                      # Qorvo: general sentence on restrictions, refers to a note
    389: P, 391: P, 399: P, 401: P,   # Qualcomm: Huawei royalty payments / licence dispute
    398: U,                      # Qualcomm: "shift in OEM share towards Huawei"
    416: P,                      # Skyworks: revenue decrease driven by the Huawei listing
}


# Hand corrections for later stages (filled in after reading), keyed by stage.
STAGE_OVERRIDES = {
    # B2a, read 25 Nov 2026
    "B2a": {14: P,                                   # Cree: inventory of product intended for Huawei
            19: P, 30: P,                            # DSP Group: customer base includes Huawei
            58: P,                                   # MaxLinear: "Huawei and ZTE are each our current customers"
            100: W, 101: W, 102: W, 103: W,          # Oclaro: Huawei 11% (FY2018), 15% (FY2017), 21% (FY2016)
            105: P,                                  # ON Semiconductor: "Huawei ... and certain other customers"
            106: P, 107: P, 121: P, 122: P,          # Semtech: table "Representative Customers by End-Markets"
            126: P,                                  # Semtech: "other customers, such as Huawei"
            133: P, 143: P,                          # Synaptics: table "Our leading OEM customers ... included"
            154: P, 156: P, 158: P},                 # TTM: five largest OEM customers include Huawei
    # B2c (exposure only), read 25 Nov 2026
    "B2c": {1: O, 12: O,                             # CEVA: competes with Huawei's internal engineering teams
            43: P,                                   # NXP: 10 largest OEM end customers include Huawei
            100: O,                                  # SiTime: Temporary General License description
            101: "indirect",                         # SiTime: revenue attributable to Huawei via distributors
            131: P},                                 # Xperi: imaging technology licensed to Huawei
}


def rule_label(r):
    s = r["sentence"]
    if not HUAWEI.search(s):
        if re.search(r"\b[Cc]ustomer\s+[A-H]\b|^\| [A-H]\s?(\(\d\))? \|", s):
            return "unnamed customer"
        return "table row" if s.startswith("| ") else "10% paragraph"
    if PCT.search(s) and (REVENUE.search(s) or s.startswith("| ")) and not re.search(r"accounts receivable", s, re.I):
        return "customer with %"
    if CUSTOMER_CUES.search(s):
        return "customer without %"
    return "competitor/other"


def main():
    OVERRIDES = {"B1": OVERRIDES_B1}.get(STAGE, STAGE_OVERRIDES.get(STAGE, {}))
    rows = list(csv.DictReader(CSV.open()))
    for i, r in enumerate(rows):
        r["label"] = OVERRIDES.get(i, rule_label(r)) + (" (read)" if i in OVERRIDES else "")
    with CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["firm", "filing", "section", "sentence", "label"])
        w.writeheader()
        w.writerows(rows)
    for i, r in enumerate(rows):
        if HUAWEI.search(r["sentence"]):
            print(f"[{i}] {r['firm'][:7]} {r['filing'].split()[1][4:]} {r['label'][:20]:20s} | {r['sentence'][:105]}")


if __name__ == "__main__":
    main()
