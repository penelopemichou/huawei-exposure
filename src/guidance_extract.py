"""Guidance-cut step: pull candidate guidance sentences and Huawei sentences from the 48 saved 8-K
filings (complete-submission text files), offline. Writes results/guidance_sentences.csv and prints
them grouped by firm and filing, for reading by hand.

Run (bash):  ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/guidance_extract.py
"""

import csv
import re
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))
from extract_sentences import Blocks, sentences     # noqa: E402

G = PROJECT / "data" / "raw" / "filing_lists" / "guidance"
REV = re.compile(r"\b(revenue|revenues|net sales|sales)\b", re.I)
FWD = re.compile(r"\b(expect|expects|expected|anticipate|anticipates|outlook|guidance|guide|range|between|forecast|estimate)\w*", re.I)
MONEY = re.compile(r"\$\s?\d")
HUAWEI = re.compile(r"huawei|hisilicon", re.I)


def documents(raw):
    for d in re.findall(r"<DOCUMENT>(.*?)</DOCUMENT>", raw, re.S):
        typ = re.search(r"<TYPE>([^\n<]+)", d)
        body = re.search(r"<TEXT>(.*?)</TEXT>", d, re.S)
        yield (typ.group(1).strip() if typ else "?"), (body.group(1) if body else "")


def text_of(html):
    if "<" not in html[:2000]:
        return [b.strip() for b in html.split("\n\n") if b.strip()]
    p = Blocks()
    p.feed(html)
    p.flush()
    return p.blocks


def main():
    cands = [r for r in csv.DictReader((PROJECT / "results" / "guidance_candidates.csv").open()) if r["url"]]
    out_rows = []
    for r in cands:
        raw = (G / f"{r['accession']}.txt").read_text(encoding="utf-8", errors="replace")
        print(f"\n### {r['firm']} | {r['role']} | filed {r['filed']} | items {r['items']} | {r['accession']}")
        n = 0
        for typ, body in documents(raw):
            if not (typ.startswith("8-K") or typ.startswith("EX-99")):
                continue
            seen = set()
            for b in text_of(body):
                for s in sentences(b):
                    s = re.sub(r"\s+", " ", s).strip()
                    if s in seen or len(s) > 900:
                        continue
                    guide = REV.search(s) and FWD.search(s) and MONEY.search(s)
                    hw = HUAWEI.search(s)
                    if guide or hw:
                        seen.add(s)
                        kind = "+".join(k for k, v in [("guidance?", guide), ("huawei", hw)] if v)
                        out_rows.append({**{k: r[k] for k in ["firm", "role", "filed", "items", "accession"]},
                                         "document": typ, "kind": kind, "sentence": s})
                        if n < 8:
                            print(f"  [{typ}] ({kind}) {s[:600]}")
                        n += 1
        if n == 0:
            print("  (no revenue-guidance or Huawei sentence found)")
        elif n > 8:
            print(f"  … {n - 8} more in results/guidance_sentences.csv")
    with (PROJECT / "results" / "guidance_sentences.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["firm", "role", "filed", "items", "accession", "document", "kind", "sentence"])
        w.writeheader()
        w.writerows(out_rows)
    print(f"\nsentences saved: {len(out_rows)}")


if __name__ == "__main__":
    main()
