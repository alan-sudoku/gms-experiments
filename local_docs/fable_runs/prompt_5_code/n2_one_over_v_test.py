#!/usr/bin/env python3
"""Row N2 (claim G3.6): 1/v test, ratio RI_table / RI_1/v for each N1 entry.

RI_1/v = 2*sigma0*sqrt(0.0253/0.5) = 0.450*sigma0 (exact integral of sigma0*sqrt(E0/E) dE/E from 0.5 eV to infinity).
Inputs: outputs/n1_values.csv (written by n1_thermal_ri.py: Sears 1992 thermal sigma0 [LOOKUP], ENDF/B-VII.1 RI [LOOKUP]).
RI used: integral from 0.5 eV to 20 MeV of sigma_abs dE/E (column ri_abs_20MeV_b). The 1/v integral to infinity differs from that to 20 MeV by
sqrt(0.0253/2e7) ~ 1e-6 relative, negligible. For C, Al and Fe, threshold reactions at MeV energies add to the 20 MeV integral; the
100 keV column is printed too. Level `derived`. Run n1_thermal_ri.py first.
"""
import os, csv, math
HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
rows = list(csv.DictReader(l for l in open(os.path.join(HERE, "outputs", "n1_values.csv")) if not l.startswith("#")))
E0, EC = 0.0253, 0.5
fac = 2*math.sqrt(E0/EC)
# independent numerical check of the factor
from scipy.integrate import quad
num = quad(lambda lnE: math.sqrt(E0/math.exp(lnE)), math.log(EC), math.log(1e12))[0]
print("N2: 1/v factor 2*sqrt(0.0253/0.5) = %.6f; numerical integral of sqrt(E0/E) dE/E from 0.5 eV to 1e12 eV = %.6f" % (fac, num))
check("factor 0.450", abs(fac-0.450) < 5e-4 and abs(num-fac) < 1e-6, "%.6f / %.6f" % (fac, num))
print("LOOKUP inputs: outputs/n1_values.csv <- Sears 1992 (sigma0), ENDF/B-VII.1 NNDC Sigma (RI), access 2026-11-14")
print("\n%-8s %11s %11s %12s %8s %14s %8s   %s" % ("entry", "sigma0 (b)", "0.45*sigma0", "RI abs 20MeV", "ratio", "RI abs 100keV", "ratio", "class"))
PLAN = {"B-10": (1720, 1730), "nat Cd": (50, 100), "nat Gd": (380, 410), "nat Hf": (1900, 2000), "nat In": (3100, 3300), "nat Ag": (740, 770)}
res = {}
for r in rows:
    s0 = float(r["sigma_sears_b"]); ri = float(r["ri_abs_20MeV_b"]); ri1 = float(r["ri_abs_100keV_b"])
    ref = fac*s0; q = ri/ref; q1 = ri1/ref
    cls = "1/v-like" if 0.95 <= q <= 1.05 else ("RI >> 1/v" if q > 1.5 else ("RI << 1/v" if q < 0.67 else "intermediate"))
    res[r["entry"]] = (s0, ri, q)
    print("%-8s %11.5g %11.5g %12.5g %8.3f %14.5g %8.3f   %s" % (r["entry"], s0, ref, ri, q, ri1, q1, cls))
print("\nChecks (plan):")
q = res["B-10"][2]; check("B-10 ratio within 0.95-1.05 (outside would falsify G3.6)", 0.95 <= q <= 1.05, "%.4f" % q)
check("B-10 RI in UNSURE range 1720-1730 b", 1720 <= res["B-10"][1] <= 1730, "%.5g b" % res["B-10"][1])
check("Li-6 ratio about 1.0 (0.95-1.05)", 0.95 <= res["Li-6"][2] <= 1.05, "%.4f" % res["Li-6"][2])
for k in ("nat Cd", "nat Gd"):
    check("%s ratio << 1 (< 0.3)" % k, res[k][2] < 0.3, "%.4f" % res[k][2])
for k in ("nat Hf", "nat In", "nat Ag"):
    check("%s ratio >> 1 (> 3)" % k, res[k][2] > 3, "%.4f" % res[k][2])
print("\nRI values against the planner's UNSURE ranges (b):")
for k, (lo, hi) in PLAN.items():
    v = res[k][1]; print("  %-7s RI = %.5g  range [%g, %g]: %s" % (k, v, lo, hi, "inside" if lo <= v <= hi else "OUTSIDE (above)" if v > hi else "OUTSIDE (below)"))
print("\nNotes: (1) Cd-113 RI/(0.45 s0) = %.3f and Gd-155/157 = %.3f, %.3f: single-isotope ratios are even further below 1/v for Gd-157 (thermal resonance below the cut)." % (res["Cd-113"][2], res["Gd-155"][2], res["Gd-157"][2]))
print("(2) The ratio for B-10 compares RI from ENDF/B-VII.1 with sigma0 from Sears 1992: two sources, so it is a genuine consistency test, not an identity.")
print("FAILED CHECKS:", FAILS if FAILS else "none")
