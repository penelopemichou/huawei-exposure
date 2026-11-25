"""Session 2, Stage B: pull the Huawei sentences and the 10%-customer paragraphs
out of the saved 10-K documents (no internet; standard library HTML reading).

Rows written to results/huawei_sentences.csv (columns: firm, filing, section, sentence, label):
  1. every sentence that contains "Huawei" or "HiSilicon";
  2. every paragraph that contains "10%" / "10 %" / "ten percent" together with "customer";
  3. every table row that names an unnamed customer ("Customer A", "Customer B", ...);
  4. up to 12 table rows right after a 10%-customer paragraph that ends with ":" (the customer table).
A whole table row is one block, its cells separated by "|".
The label column is left empty here: labels are proposed by reading each row.
Identical text in the same document is kept once.

Run from the project folder:
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/extract_sentences.py B1
"""

import csv
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
PLAN = PROJECT / "notes" / "stage-b-plan.md"
RAW = PROJECT / "data" / "raw" / "stage_b"
def out_csv(stage):
    """B1 keeps its original file name (row numbers in the notes refer to it)."""
    name = "huawei_sentences.csv" if stage == "B1" else f"huawei_sentences_{stage}.csv"
    return PROJECT / "results" / name

BLOCK_TAGS = {"p", "div", "tr", "li", "br", "h1", "h2", "h3", "h4", "h5", "h6", "table", "section"}
CELL_TAGS = {"td", "th"}
HUAWEI = re.compile(r"huawei|hisilicon", re.I)
TEN_PCT = re.compile(r"\b10\s?%|\bten percent", re.I)
CUSTOMER = re.compile(r"customer", re.I)
UNNAMED = re.compile(r"\bcustomer\s+[A-H]\b")
ITEM = re.compile(r"^(item\s+\d+[a-z]?\b\.?.*)$", re.I)
NOTE = re.compile(r"^(note\s+\d+\b.*|\d{1,2}\.\s+[A-Z][A-Za-z ,&'\-]{3,80})$")
ABBREV = ["U.S.", "Inc.", "Co.", "Corp.", "Ltd.", "No.", "e.g.", "i.e.", "vs.", "approx.", "Mr.", "Ms.", "Dr.", "S.A.", "N.V.", "L.P."]


class Blocks(HTMLParser):
    """Text blocks of a document; hidden parts (display:none, ix:header) are skipped."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.buf, self.hidden = [], [], 0
        self.stack = []
        self.in_tr = 0          # inside a table row, the whole row is one block

    def flush(self):
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text.startswith("|") or " | " in text:                  # a table row: tidy the cell marks
            text = re.sub(r"(\|\s*)+", "| ", text).strip(" |")
            text = re.sub(r"\s+%", "%", text)
            text = "| " + text if text else ""
        if text and re.search(r"[A-Za-z0-9]", text):
            self.blocks.append(text)
        self.buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        hide = tag == "ix:header" or "display:none" in (a.get("style") or "").replace(" ", "").lower()
        self.stack.append((tag, hide))
        if hide:
            self.hidden += 1
        if tag == "tr":
            self.flush()
            self.in_tr += 1
        elif tag in BLOCK_TAGS:
            if self.in_tr:
                self.buf.append(" ")
            else:
                self.flush()
        elif tag in CELL_TAGS:
            self.buf.append(" | ")

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):        # pop to the matching tag
            if self.stack[i][0] == tag:
                for _, hide in self.stack[i:]:
                    if hide:
                        self.hidden -= 1
                del self.stack[i:]
                break
        if tag == "tr":
            self.flush()
            self.in_tr = max(0, self.in_tr - 1)
        elif tag in BLOCK_TAGS and not self.in_tr:
            self.flush()

    def handle_data(self, data):
        if not self.hidden:
            self.buf.append(data)


def sentences(block):
    t = block
    for k, a in enumerate(ABBREV):
        t = t.replace(a, f"\x00{k}\x00")
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z“\"(])", t)
    out = []
    for p in parts:
        for k, a in enumerate(ABBREV):
            p = p.replace(f"\x00{k}\x00", a)
        out.append(p.strip())
    return out


def plan_rows(stage):
    """(firm, filing label, path) for each document in the stage's table."""
    text = PLAN.read_text()
    m = re.search(rf"^#{{2,3}} {re.escape(stage)}:.*$", text, re.M)
    section = re.split(r"\n#{2,3} ", text[m.end():], maxsplit=1)[0]
    rows = []
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not cells[-1].startswith("https://"):
            continue
        firm, fy, form = cells[0], cells[1] if stage in ("B1", "B3") else cells[2], cells[2] if stage in ("B1", "B3") else cells[3]
        parts = cells[-1].split("/")
        rows.append((firm, f"{form} FY{fy} {parts[-2]} {parts[-1]}", RAW / parts[-3].zfill(10) / parts[-2] / parts[-1]))
    return rows


def main():
    stage = sys.argv[1]
    OUT = out_csv(stage)
    out_rows, per_doc = [], []
    for firm, filing, path in plan_rows(stage):
        p = Blocks()
        p.feed(path.read_text(encoding="utf-8", errors="replace"))
        p.flush()
        item, note, seen = "", "", set()
        n_h = n_p = n_u = 0
        table_after = 0          # table rows still to keep after a "... as follows:" 10% paragraph
        for b in p.blocks:
            if table_after and b.startswith("| "):
                table_after -= 1
                if b not in seen:
                    seen.add(b); n_u += 1
                    out_rows.append({"firm": firm, "filing": filing, "section": item + (f" / {note}" if note else ""),
                                     "sentence": b, "label": ""})
                continue
            table_after = 0
            if len(b) < 160 and ITEM.match(b):
                item, note = b[:80], ""
            elif len(b) < 120 and NOTE.match(b) and item.lower().startswith("item 8"):
                note = b[:80]
            section = item + (f" / {note}" if note else "")
            found = []
            for s in sentences(b):
                if HUAWEI.search(s):
                    found.append(s); n_h += 1
            if TEN_PCT.search(b) and CUSTOMER.search(b):
                found.append(b); n_p += 1
                if b.rstrip().endswith(":"):
                    table_after = 12
            elif UNNAMED.search(b):
                found.append(b); n_u += 1
            for s in found:
                if s not in seen:
                    seen.add(s)
                    out_rows.append({"firm": firm, "filing": filing, "section": section, "sentence": s, "label": ""})
        per_doc.append((firm, filing.split()[1], filing.split()[0], n_h, n_p, n_u))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["firm", "filing", "section", "sentence", "label"])
        w.writeheader()
        w.writerows(out_rows)
    print(f"{'firm':13s} {'FY':6s} {'form':6s} huawei_sent 10%_par unnamed_rows")
    for r in per_doc:
        print(f"{r[0]:13s} {r[1]:6s} {r[2]:6s} {r[3]:11d} {r[4]:7d} {r[5]:12d}")
    print(f"\nrows written (after removing repeats within a document): {len(out_rows)} -> {OUT.relative_to(PROJECT)}")


if __name__ == "__main__":
    main()
