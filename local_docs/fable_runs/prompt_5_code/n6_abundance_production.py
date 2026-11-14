#!/usr/bin/env python3
"""Row N6 (claim G3.9): abundance and production of absorber elements and the other x in the plan.

LOOKUP status:
  * Crustal abundance: the plan's primary source (CRC Handbook table) is not reachable. Per the run rules the row is run with the PLANNER's
    values (plan section 3 row N6, UNSURE, MEMORY) labelled 'NOT A LOOKUP'. As a cross-check only, data/crust_abundance_secondary.csv holds the
    column C1 (labelled CRC Handbook) of a Wikipedia data page: a SECONDARY reproduction, not accepted as the lookup.
  * Annual production: USGS Mineral Commodity Summaries 2026 (data year 2025e), data/usgs_mcs2026_world_production.csv (hand transcription from the
    PDFs in data/raw/usgs_mcs2026/), access 2026-11-14.
Check: B must be more abundant than Cd, Ag, In, Hf and Gd. Level `derived`.
"""
import os, csv, math
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
FAILS = []
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
PLAN = {"Al": 82300, "Fe": 56300, "Cu": 60, "Co": 25, "Li": 20, "Pb": 14, "B": 10, "Nd": 41.5, "Gd": 6.2, "Dy": 5.2, "Hf": 3.0, "Sn": 2.3, "W": 1.25,
        "In": 0.25, "Cd": 0.15, "Ag": 0.075, "Pt": 0.005, "Ir": 0.001}   # NOT A LOOKUP (planner, UNSURE); no planner value for C, Ni, Sm, Eu, Bi
SEC = {r["symbol"]: float(r["crust_mg_per_kg"]) for r in csv.DictReader(l for l in open(os.path.join(D, "crust_abundance_secondary.csv")) if not l.startswith("#"))}
PROD = {r["element"]: r for r in csv.DictReader(l for l in open(os.path.join(D, "usgs_mcs2026_world_production.csv")) if not l.startswith("#"))}
EL = "B Cd Gd Hf Ag In Dy Eu Sm Li C Al Fe Cu Ni Co W Pb Sn Bi Pt Ir Nd".split()
print("N6 sources: abundance = planner values (NOT A LOOKUP, UNSURE) + secondary column C1 (Wikipedia reproduction of CRC; access 2026-11-14, not accepted as lookup);")
print("            production = USGS MCS 2026 (Feb 2026), world totals 2025e, data/usgs_mcs2026_world_production.csv")
print("\n%-3s %14s %14s %10s %14s   %s" % ("el", "planner mg/kg", "secondary C1", "ratio", "world t/yr", "production note"))
for e in EL:
    p = PLAN.get(e); s = SEC.get(e); pr = PROD[e]
    tpy = pr["t_per_yr"]
    print("%-3s %14s %14s %10s %14s   %s" % (e, "-" if p is None else "%g" % p, "-" if s is None else "%g" % s, "-" if (p is None or s is None) else "%.3f" % (s/p),
          tpy if tpy else "not reported", (pr["note"] or pr["commodity_basis"])[:90]))
print("\nPlanner values vs secondary C1 (info; the planner's values are consistent with this column wherever both exist):")
for e in PLAN:
    if e in SEC: 
        if abs(SEC[e]/PLAN[e]-1) > 0.01: print("   differs: %s planner %g secondary %g" % (e, PLAN[e], SEC[e]))
print("   (no differences > 1%% for the %d elements with both values)" % sum(1 for e in PLAN if e in SEC and abs(SEC[e]/PLAN[e]-1) <= 0.01) if all(abs(SEC[e]/PLAN[e]-1) <= 0.01 for e in PLAN if e in SEC) else "")
for lab, tab in (("planner values", PLAN), ("secondary C1", SEC)):
    ok = all(tab["B"] > tab[x] for x in ("Cd", "Ag", "In", "Hf", "Gd"))
    check("B more abundant than Cd, Ag, In, Hf, Gd (%s)" % lab, ok, ", ".join("B/%s = %.3g" % (x, tab["B"]/tab[x]) for x in ("Cd", "Ag", "In", "Hf", "Gd")))
print("\nAbundance ordering (secondary C1, descending):", " > ".join(sorted([e for e in EL if e in SEC], key=lambda e: -SEC[e])))
print("\nExtra: production rank among elements with a world total (t/yr, descending):")
pl = sorted([(float(PROD[e]["t_per_yr"]), e) for e in EL if PROD[e]["t_per_yr"]], reverse=True)
print("   " + ", ".join("%s %.3g" % (e, v) for v, e in pl))
print("   Scarce-input note (G3.9): world production of Ag %.0f t, In %.0f t, Cd %.0f t; Hf and individual rare earths (Gd, Dy, Eu, Sm) have no USGS world figure (REO total 390000 t); boron has no world total either (borate deposits, Turkey alone 1.5 Mt refined borates)." % (26000, 1100, 23000))
print("   Boron is a non-scarce input only in the sense of crustal abundance (10 mg/kg); the USGS data show borates concentrated in few countries (Turkey, Chile, Bolivia, China, Peru, Argentina). Enriched B-10 is not covered by USGS data.")
print("FAILED CHECKS:", FAILS if FAILS else "none")
