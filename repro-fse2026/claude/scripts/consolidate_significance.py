#!/usr/bin/env python3
"""Consolidate flip-significance CSVs into the family x tier table.

Tiers (on p_reproduce): flips-on-average (p>0.5), significant (p>=0.95).
Reported per aggregation (mean = primary expected-behavior, median = shadow),
split symmetric (target=cost) vs asymmetric (target!=cost) where applicable.
Missing families (no CSV yet) are listed as pending.
"""
import csv, os
from collections import defaultdict

ART = "artifacts"
# family -> (csv, total_decisions_from_paper_audit, sym_classifier)
def energy_sym(r):  return r.get("cost") == r.get("target")
def icpe_sym(r):    return r.get("combo") in ("size/size", "time/time")
def all_sym(r):     return True   # ICSE19: performance/performance

FAMILIES = [
    ("REPLICATION-ICSE19", "significance_flips_replication_icse19.csv", 49,  all_sym),
    ("REPLICATION-ICPE20", "significance_flips_replication_icpe20.csv", 476, icpe_sym),
    ("ENERGY",             "significance_flips_energy.csv",             196, energy_sym),
    ("WORKLOAD",           "significance_flips_workload.csv",           651, None),
    ("LCBENCH",            "significance_flips_lcbench.csv",            245, None),
    ("LINUX",              "significance_flips_linux.csv",              49,  None),
]


def load(path):
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        return list(csv.DictReader(fh))


def tier(rows):
    n = len(rows)
    onavg = sum(float(r["p_reproduce"]) > 0.5 for r in rows)
    sig = sum(float(r["p_reproduce"]) >= 0.95 for r in rows)
    return n, onavg, sig


def main():
    for agg in ("mean", "median"):
        print(f"\n{'='*92}\nAGGREGATION = {agg.upper()}   (mean = primary expected-behavior; median = conservative shadow)")
        print(f"{'='*92}")
        print(f"{'family':<22}{'decisions':>10}{'flips':>7}{'on-avg p>.5':>13}{'sig p>=.95':>12}   {'(asym flips: on-avg/sig)':<26}")
        print("-"*92)
        for fam, fname, dec, symfn in FAMILIES:
            rows = load(os.path.join(ART, fname))
            if rows is None:
                print(f"{fam:<22}{dec:>10}{'  — pending (adapter/data not yet run) —':>0}")
                continue
            rows = [r for r in rows if r.get("agg", "median") == agg]
            n, onavg, sig = tier(rows)
            extra = ""
            if symfn is not None and any("cost" in r or "combo" in r for r in rows[:1]):
                asym = [r for r in rows if not symfn(r)]
                if asym:
                    an, ao, asg = tier(asym)
                    extra = f"asym {an}: {ao}/{asg}"
            print(f"{fam:<22}{dec:>10}{n:>7}{onavg:>13}{sig:>12}   {extra:<26}")
    # also dump the asym vs sym contrast explicitly for the families that have it
    print(f"\n{'='*60}\nSYMMETRIC vs ASYMMETRIC (median p) — the target<->cost story")
    print(f"{'='*60}")
    for fam, fname, dec, symfn in FAMILIES:
        rows = load(os.path.join(ART, fname))
        if rows is None or symfn is None:
            continue
        rows = [r for r in rows if r.get("agg", "median") == "median"]
        if not rows or not ("cost" in rows[0] or "combo" in rows[0]):
            continue
        import statistics as st
        sym = [float(r["p_reproduce"]) for r in rows if symfn(r)]
        asym = [float(r["p_reproduce"]) for r in rows if not symfn(r)]
        sm = f"{st.median(sym):.2f}" if sym else "—"
        am = f"{st.median(asym):.2f}" if asym else "—"
        print(f"  {fam:<22} symmetric median p={sm} (n={len(sym)})   asymmetric median p={am} (n={len(asym)})")


if __name__ == "__main__":
    main()
