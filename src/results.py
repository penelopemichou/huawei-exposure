"""Results, exactly as fixed before opening (notes/permutation-setup.md, notes/design-v2.md,
notes/frozen-lists.md with amendment 1). Opened on Penelope's "open", 26 Nov 2026.

Primary test (h = 1): primary exposed (5) vs primary donors (14). Per-firm outcome = average of the
B4 and AutoETS signed miss (positive = revenue above the forecast). Rank all firms from the lowest
signed miss (rank 1); ties share the average rank. Statistic = rank-sum of the exposed firms.
Exact enumeration of every choice of n exposed firms out of N. One-sided p = share with rank-sum <=
observed; two-sided p = share at least as far from n(N+1)/2. Each rule is also tested on its own.
"Consistent" only if the B4 and AutoETS rank-sums are on the same side of n(N+1)/2.
Everything else is descriptive (no test). AVG = average of the two rules where both exist.

Run (bash):  ~/Documents/ai-fpa-forecast/.venv/bin/python -B -I src/results.py
"""

import sys
from itertools import combinations
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "src"))
from companies import COMPANIES   # noqa: E402

FY2020_ONLY = ["Marvell", "Cirrus Logic", "Alpha & Omega", "Xilinx"]
pd.set_option("display.width", 250, "display.max_rows", 200, "display.max_columns", 30)


def rank_test(outcome, exposed):
    """outcome: Series firm -> value; exposed: set of firms. Returns observed rank-sum, expected, p1, p2, N, n."""
    r = outcome.rank(method="average")
    N, n = len(outcome), len([f for f in outcome.index if f in exposed])
    obs = r[[f for f in outcome.index if f in exposed]].sum()
    mid = n * (N + 1) / 2
    sums = [sum(c) for c in combinations(r.to_numpy(), n)]
    p1 = sum(s <= obs + 1e-9 for s in sums) / len(sums)
    p2 = sum(abs(s - mid) >= abs(obs - mid) - 1e-9 for s in sums) / len(sums)
    return obs, mid, p1, p2, N, n, len(sums)


def main():
    e = pd.read_csv(PROJECT / "results" / "event_rows.csv")
    wide = e.pivot_table(index=["company", "group", "h"], columns="rule", values="signed_miss").reset_index()
    wide["AVG"] = wide[["B4", "ETS"]].mean(axis=1, skipna=False)
    wide.columns.name = None
    wide.to_csv(PROJECT / "results" / "results_by_firm_long.csv", index=False)

    out = []
    # 1. Primary test, h = 1
    h1 = wide[(wide.h == 1) & wide.group.isin(["Exposed (primary)", "Donor (primary)"])].set_index("company")
    exposed = set(h1[h1.group == "Exposed (primary)"].index)
    out.append("=" * 100)
    out.append("1. PRIMARY TEST, h = 1: primary exposed vs primary donors (rank-sum, exact enumeration)")
    rows = []
    sides = {}
    for rule in ["AVG", "B4", "ETS"]:
        s = h1[rule].dropna()
        obs, mid, p1, p2, N, n, k = rank_test(s, exposed)
        sides[rule] = "below" if obs < mid else ("above" if obs > mid else "at")
        rows.append({"outcome": {"AVG": "average of B4 and AutoETS (primary)", "B4": "B4 alone", "ETS": "AutoETS alone"}[rule],
                     "N": N, "n exposed": n, "choices": k, "expected rank-sum": mid, "observed rank-sum": obs,
                     "one-sided p (primary)": round(p1, 4), "two-sided p": round(p2, 4),
                     "mean exposed": round(s[s.index.isin(exposed)].mean(), 2),
                     "mean donors": round(s[~s.index.isin(exposed)].mean(), 2),
                     "gap (exposed - donors)": round(s[s.index.isin(exposed)].mean() - s[~s.index.isin(exposed)].mean(), 2)})
    t1 = pd.DataFrame(rows)
    out.append(t1.to_string(index=False))
    consistent = sides["B4"] == sides["ETS"] and sides["B4"] != "at"
    out.append(f"   Both rules point the same way (rank-sums both {sides['B4']} {mid:g})? "
               f"{'yes: consistent' if consistent else 'no: rules disagree'} (B4 {sides['B4']}, AutoETS {sides['ETS']})")
    out.append("   Ranks at h = 1 (AVG outcome; rank 1 = lowest signed miss):")
    rk = h1["AVG"].rank(method="average")
    out.append("   " + "; ".join(f"{f} {rk[f]:g}" for f in sorted(exposed, key=lambda x: rk[x])))
    t1.to_csv(PROJECT / "results" / "results_primary_test.csv", index=False)

    # 2-3. h = 2, 3 and 4 (descriptive)
    def describe(h):
        w = wide[(wide.h == h) & wide.group.isin(["Exposed (primary)", "Donor (primary)"])]
        rows = []
        for g in ["Exposed (primary)", "Donor (primary)"]:
            x = w[w.group == g]
            rows.append({"group": g, "firms": len(x),
                         **{f"mean {r}": round(x[r].mean(), 2) for r in ["AVG", "B4", "ETS"]},
                         **{f"median {r}": round(x[r].median(), 2) for r in ["AVG", "B4", "ETS"]}})
        d = pd.DataFrame(rows)
        gap = {r: round(d.loc[0, f"mean {r}"] - d.loc[1, f"mean {r}"], 2) for r in ["AVG", "B4", "ETS"]}
        return d, gap
    for h, title in [(2, "2. h = 2 (secondary, descriptive)"), (3, "   h = 3 (secondary, descriptive)"),
                     (4, "3. h = 4: FLAGGED COVID (targets in late 2019 / early 2020; descriptive)")]:
        d, gap = describe(h)
        out.append("=" * 100 if h != 3 else "-" * 100)
        out.append(title)
        out.append(d.to_string(index=False))
        out.append(f"   gap in means (exposed - donors): AVG {gap['AVG']:+.2f}, B4 {gap['B4']:+.2f}, AutoETS {gap['ETS']:+.2f}")

    # 4. Three-group check
    out.append("=" * 100)
    out.append("4. THREE-GROUP CHECK (descriptive): exposed (primary) / low exposure / donors (primary), AVG outcome")
    rows = []
    for label, drop in [("with all 16 low-exposure firms", []), ("without the four FY2020-only firms (12)", FY2020_ONLY)]:
        for h in (1, 2, 3, 4):
            w = wide[wide.h == h]
            ex = w[w.group == "Exposed (primary)"].AVG
            lo = w[(w.group == "Low exposure") & ~w.company.isin(drop)].AVG
            dn = w[w.group == "Donor (primary)"].AVG
            order = " < ".join(n for n, v in sorted([("exposed", ex.mean()), ("low", lo.mean()), ("donors", dn.mean())], key=lambda z: z[1]))
            rows.append({"version": label, "h": h, "exposed mean": round(ex.mean(), 2), "low mean": round(lo.mean(), 2),
                         "donors mean": round(dn.mean(), 2), "exposed median": round(ex.median(), 2),
                         "low median": round(lo.median(), 2), "donors median": round(dn.median(), 2),
                         "n exp/low/don": f"{ex.notna().sum()}/{lo.notna().sum()}/{dn.notna().sum()}",
                         "order of means (lowest first)": order})
    t4 = pd.DataFrame(rows)
    out.append(t4.to_string(index=False))
    t4.to_csv(PROJECT / "results" / "results_three_groups.csv", index=False)

    # 5. Sensitivity donors
    out.append("=" * 100)
    out.append("5. SENSITIVITY DONORS (descriptive; not in the primary test), AVG outcome")
    rows = []
    for h in (1, 2, 3, 4):
        w = wide[wide.h == h]
        for g in ["Exposed (primary)", "Donor (primary)", "Donor (sensitivity)"]:
            x = w[w.group == g].AVG
            rows.append({"h": h, "group": g, "firms": int(x.notna().sum()), "mean": round(x.mean(), 2), "median": round(x.median(), 2)})
    t5 = pd.DataFrame(rows)
    out.append(t5.pivot_table(index="group", columns="h", values=["firms", "mean", "median"]).to_string())
    t5.to_csv(PROJECT / "results" / "results_sensitivity.csv", index=False)

    # 6. Scaled outcome (h = 1)
    out.append("=" * 100)
    out.append("6. SCALED OUTCOME, h = 1 (secondary, descriptive): signed miss / own usual pre-event miss; needs >= 8 pre-event h = 1 forecasts")
    sc = pd.read_csv(PROJECT / "results" / "usual_miss_scales.csv")
    sc1 = sc[sc.h == 1].pivot_table(index="company", columns="rule", values=["usual_miss", "n_forecasts"])
    rows = []
    for _, r in wide[wide.h == 1].iterrows():
        c = r.company
        n_h1 = int(sc1.loc[c, ("n_forecasts", "AVG")]) if c in sc1.index else 0
        row = {"firm": c, "group": r.group, "pre-event h1 forecasts": n_h1}
        for rule in ["AVG", "B4", "ETS"]:
            nr = int(sc1.loc[c, ("n_forecasts", rule)]) if c in sc1.index else 0
            row[f"scaled {rule}"] = ("scale too thin" if nr < 8 else round(r[rule] / sc1.loc[c, ("usual_miss", rule)], 2))
        rows.append(row)
    t6 = pd.DataFrame(rows)
    order = {"Exposed (primary)": 0, "Exposed (secondary)": 1, "Low exposure": 2, "Donor (primary)": 3, "Donor (sensitivity)": 4}
    t6 = t6.sort_values(["group", "firm"], key=lambda s: s.map(order) if s.name == "group" else s)
    out.append(t6.to_string(index=False))
    num = t6[t6["scaled AVG"] != "scale too thin"].copy()
    num["scaled AVG"] = num["scaled AVG"].astype(float)
    out.append("   group medians of scaled AVG (firms with >= 8): " + "; ".join(
        f"{g} {num[num.group == g]['scaled AVG'].median():.2f} (n={int((num.group == g).sum())})" for g in order))
    out.append("   scale too thin: " + ", ".join(t6[t6["scaled AVG"] == "scale too thin"].firm))
    t6.to_csv(PROJECT / "results" / "results_scaled.csv", index=False)

    # 7. Every firm's signed miss
    out.append("=" * 100)
    out.append("7. EVERY FIRM'S SIGNED MISS (%, positive = revenue above the forecast), h = 1-4, B4 and AutoETS")
    t7 = wide.pivot_table(index=["group", "company"], columns="h", values=["B4", "ETS"])
    t7.columns = [f"{r} h{h}" for r, h in t7.columns]
    t7 = t7.reset_index()
    t7 = t7.sort_values(["group", "company"], key=lambda s: s.map(order) if s.name == "group" else s)
    t7 = t7[["group", "company"] + [f"{r} h{h}" for r in ["B4", "ETS"] for h in (1, 2, 3, 4)]]
    out.append(t7.round(1).to_string(index=False))
    t7.to_csv(PROJECT / "results" / "results_every_firm.csv", index=False)
    print("\n".join(out))


if __name__ == "__main__":
    main()
