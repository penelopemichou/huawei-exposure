"""Session 2: proposed class for every exposed, low-exposure and donor firm (no internet).

SIC code and SIC description come from the firm's saved SEC filing list. The proposed class
(chip / optical-component / contract manufacturer / solar / equipment / other) and its evidence
are set below by hand: "SIC", "name", "10-K read" (the firm's 10-K was read in Stage B) or
"from memory" (nothing read; marked). Classes marked "unclear" need a 10-K (ask Penelope first).
Writes results/firm_classes.csv (DRAFT until Penelope approves it).

Run from the project folder:
    ~/Documents/ai-fpa-forecast/.venv/bin/python -I src/classify_firms.py
"""

import json
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
DIRS = [PROJECT / "data" / "raw" / "stage_a" / "submissions", PROJECT / "data" / "raw" / "filing_lists" / "submissions"]
K, MEM = "10-K read", "from memory"

# group -> [(name as in the filing list (start), proposed class, evidence, note)]
FIRMS = {
    "exposed": [("NEOPHOTONICS", "optical-component", K, "optical components for telecom/datacom"),
                ("INPHI", "chip", K, "high-speed analog chips for optical links"),
                ("Lumentum", "optical-component", K, "optical components and lasers (SECONDARY)"),
                ("Qorvo", "chip", K, "RF chips"),
                ("MICRON", "chip", K, "memory chips"),
                ("FINISAR", "optical-component", K, "optical transceivers")],
    "low exposure, implied": [("MACOM", "chip", K, "analog RF/microwave/optical chips"),
                              ("SKYWORKS", "chip", K, "RF chips"),
                              ("Broadcom", "chip", K, "networking, broadband, wireless chips"),
                              ("QUALCOMM", "chip", K, "phone chips and licensing")],
    "donor": [("INTEL", "chip", K, "processors"),
              ("Enphase", "solar", K, "solar microinverters (10-K: inverter competitors)"),
              ("AMBARELLA", "chip", K, "video-processing chips"),
              ("MICROCHIP", "chip", K, "microcontrollers, analog"),
              ("ADVANCED ENERGY", "equipment", MEM, "power subsystems for chip-making equipment"),
              ("ADVANCED MICRO DEVICES", "chip", "name", "processors"),
              ("AMKOR", "contract manufacturer", K, "10-K FY2018: 'outsourced semiconductor packaging and test services'"),
              ("AMPHENOL", "other", MEM, "connectors and cables"),
              ("ANALOG DEVICES", "chip", "name", "analog chips"),
              ("AXT", "equipment", K, "10-K FY2018: 'materials science company ... substrates ... We do not design or manufacture the chips'"),
              ("BEL FUSE", "other", MEM, "magnetics, connectors, power supplies"),
              ("BENCHMARK ELECTRONICS", "contract manufacturer", MEM, "contract electronics manufacturing"),
              ("CMC Materials", "equipment", "name", "chip-polishing materials"),
              ("CTS", "other", MEM, "sensors, actuators, components"),
              ("DIODES", "chip", "name", "discrete and analog chips"),
              ("FIRST SOLAR", "solar", "name", "solar panels"),
              ("FORMFACTOR", "equipment", MEM, "probe cards for chip testing"),
              ("IEC ELECTRONICS", "contract manufacturer", MEM, "contract electronics manufacturing"),
              ("IPG PHOTONICS", "sensitivity from rules", K, "10-K FY2018: lasers used primarily in materials processing, sold to OEMs, system integrators and end users"),
              ("JABIL", "contract manufacturer", MEM, "contract electronics manufacturing"),
              ("KEY TRONIC", "contract manufacturer", MEM, "contract electronics manufacturing"),
              ("Kimball Electronics", "contract manufacturer", MEM, "contract electronics manufacturing"),
              ("LATTICE SEMICONDUCTOR", "chip", "name", "FPGAs"),
              ("MAGNACHIP SEMICONDUCTOR", "chip", "name", "display-driver and power chips"),
              ("MAXIM INTEGRATED", "chip", MEM, "analog chips"),
              ("METHODE", "other", MEM, "connectors, sensors, automotive electronics"),
              ("MONOLITHIC POWER", "chip", K, "10-K FY2018: 'a leading semiconductor company ... high-performance power solutions'"),
              ("NORTECH", "contract manufacturer", MEM, "contract electronics manufacturing"),
              ("NVIDIA", "chip", MEM, "graphics and data-centre processors"),
              ("OSI SYSTEMS", "sensitivity from rules", MEM, "security scanners, healthcare, optoelectronics (system/instrument or unclear; no 10-K read)"),
              ("PHOTRONICS", "equipment", MEM, "photomasks"),
              ("PLEXUS", "contract manufacturer", MEM, "contract electronics manufacturing"),
              ("POWER INTEGRATIONS", "chip", K, "10-K FY2018: 'analog and mixed-signal integrated circuits (ICs)'"),
              ("RAMBUS", "other", K, "10-K FY2018: primary revenue is patent licenses; royalties 56% of 2018 revenue"),
              ("SANMINA", "contract manufacturer", MEM, "contract electronics manufacturing"),
              ("SILICON LABORATORIES", "chip", "name", "mixed-signal chips"),
              ("SMTC", "contract manufacturer", MEM, "contract electronics manufacturing"),
              ("SUNPOWER", "solar", "name", "solar panels and systems"),
              ("TEXAS INSTRUMENTS", "chip", MEM, "analog and embedded chips"),
              ("Ultra Clean", "equipment", MEM, "gas/fluid subsystems for chip-making equipment"),
              ("VIAVI", "sensitivity from rules", K, "10-K FY2018: 'global provider of network test, monitoring and assurance solutions'; optical coatings second"),
              ("VICOR", "other", K, "10-K FY2018: 'modular power components and power systems'")],
}


def find(name):
    for d in DIRS:
        for p in sorted(d.glob("CIK??????????.json")):
            s = json.loads(p.read_text())
            if s["name"].upper().startswith(name.upper()):
                return p.stem[3:], s
    raise SystemExit(f"not found on disk: {name}")


def main():
    rows = []
    for group, firms in FIRMS.items():
        for name, cls, ev, note in firms:
            cik, s = find(name)
            rows.append({"group": group, "firm": s["name"], "cik": cik, "sic": s.get("sic"), "sic_description": s.get("sicDescription"),
                         "proposed_class": cls, "evidence": ev, "note": note,
                         "comparison": ("PRIMARY" if cls in ("chip", "optical-component") else "sensitivity")
                                       if group == "donor" else ""})   # donor-rule.md class rule, 25 Nov 2026
    d = pd.DataFrame(rows)
    d.to_csv(PROJECT / "results" / "firm_classes.csv", index=False)
    pd.set_option("display.width", 260, "display.max_rows", 100, "display.max_colwidth", 60)
    print(d[["group", "firm", "sic", "sic_description", "proposed_class", "evidence", "comparison"]].to_string(index=False))
    dn = d[d.group == "donor"]
    print("\ndonors by class:", dn.proposed_class.value_counts().to_dict())
    print("donors by comparison:", dn.comparison.value_counts().to_dict())
    print("rows from memory:", (d.evidence == MEM).sum(), "of", len(d))


if __name__ == "__main__":
    main()
