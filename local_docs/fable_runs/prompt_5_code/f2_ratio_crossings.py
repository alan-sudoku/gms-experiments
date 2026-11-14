#!/usr/bin/env python3
"""Row F2 (claims G3.2, G4.1): W/C mass-attenuation ratio against energy, interval where ratio < 2.

LOOKUP: NIST XCOM total attenuation with coherent scattering, Z = 6, 13, 26, 74 (data/xcom_z*.csv, XCOM web,
access 2026-11-14); water and ordinary concrete: NISTIR 5632 Table 4 (data/nist_comtab_*.csv, NIST composition, same date).
Method: log-log interpolation between tabulated points (never across an absorption edge: XCOM lists each edge as a
pre/post pair with the same energy, so the curve is discontinuous there and each side is interpolated separately);
crossings of ratio = 2 by brentq on the interpolated function inside each smooth piece (+ jump check at edges);
minimum by minimize_scalar (bounded) on a bracket around the lowest sampled value.
Range 0.03-20 MeV. Everything is level `derived`.
"""
import os, math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
FAILS = []; ISSUES = []

def load_csv(fn, ecol, vcol):
    E = []; V = []
    for ln in open(os.path.join(D, fn)):
        if ln.startswith("#") or ln.startswith("edge"): continue
        p = ln.strip().split(","); E.append(float(p[ecol])); V.append(float(p[vcol]))
    return np.array(E), np.array(V)
MAT = {}
for name, z in [("C", 6), ("Al", 13), ("Fe", 26), ("W", 74)]:
    MAT[name] = load_csv("xcom_z%03d.csv" % z, 1, 7)
MAT["water"] = load_csv("nist_comtab_water.csv", 1, 2)
MAT["concrete"] = load_csv("nist_comtab_concrete.csv", 1, 2)

def mu(name, E):
    """log-log interpolation; at an edge energy returns the post-edge value."""
    x, y = MAT[name]
    i = np.searchsorted(x, E, side="right") - 1
    i = min(max(i, 0), len(x) - 2)
    x0, x1, y0, y1 = x[i], x[i+1], y[i], y[i+1]
    if x1 == x0: return y1
    t = (math.log(E) - math.log(x0))/(math.log(x1) - math.log(x0))
    return math.exp(math.log(y0) + t*(math.log(y1) - math.log(y0)))
def edges_of(name):
    x, _ = MAT[name]; return sorted(set(x[:-1][np.diff(x) == 0]))
EMIN, EMAX = 0.03, 20.0

def analyse(num, den, target=2.0, verbose=True, EMAX=EMAX):
    f = lambda E: mu(num, E)/mu(den, E)
    brk = sorted(set([EMIN, EMAX] + [e for e in edges_of(num) + edges_of(den) if EMIN < e < EMAX]))
    # pieces between breakpoints; within a piece both materials are smooth
    cross = []; pieces = list(zip(brk[:-1], brk[1:]))
    for a, b in pieces:
        la, lb = a*(1+1e-9), b*(1-1e-9)
        g = lambda lnE: f(math.exp(lnE)) - target
        grid = np.linspace(math.log(la), math.log(lb), 400)
        vals = [g(u) for u in grid]
        for k in range(len(grid)-1):
            if vals[k] == 0 or vals[k]*vals[k+1] < 0:
                r = brentq(g, grid[k], grid[k+1], xtol=1e-14)
                cross.append(math.exp(r))
    # jumps at edges
    for e in [e for e in edges_of(num) + edges_of(den) if EMIN < e < EMAX]:
        before = f(e*(1-1e-9)); after = f(e)
        if (before-target)*(after-target) < 0: cross.append(e)
    cross = sorted(cross)
    # minimum: scan, then bound a bracket around lowest sample (sample grid only to pick the bracket)
    grid = np.exp(np.linspace(math.log(EMIN*1.0001), math.log(EMAX), 3000))
    vals = np.array([f(e) for e in grid]); k = int(np.argmin(vals))
    lo, hi = grid[max(k-3, 0)], grid[min(k+3, len(grid)-1)]
    res = minimize_scalar(lambda u: f(math.exp(u)), bounds=(math.log(lo), math.log(hi)), method="bounded",
                          options={"xatol": 1e-12})
    emin, rmin = math.exp(res.x), res.fun
    interior = (k > 3) and (k < len(grid)-4)
    return f, cross, (emin, rmin, interior, lo, hi)

print("F2: ratio of total mass attenuation (with coherent) mu/rho(W)/mu/rho(X), %g-%g MeV, target ratio 2" % (EMIN, EMAX))
print("LOOKUP sources: XCOM web (Method=Elem; Z=6,13,26,74), NISTIR 5632 Table 4 (water, ordinary concrete); access 2026-11-14;")
print("  files data/xcom_z006.csv, z013, z026, z074, data/nist_comtab_water.csv, data/nist_comtab_concrete.csv. W K-edge rows in file:", edges_of("W")[:1], "MeV (K edge)")
summary = {}
for den in ["C", "Fe", "Al", "water", "concrete"]:
    f, cross, (emin, rmin, interior, lo, hi) = analyse("W", den)
    print("\n== W/%s ==" % den)
    print("  ratio at 0.03 MeV = %.4g, at 20 MeV = %.4g, at 10 MeV = %.4g" % (f(EMIN*1.0000001), f(EMAX), f(10.0)))
    print("  crossings of ratio=2 (brentq on interpolated pieces): " + ", ".join("%.5g MeV" % c for c in cross))
    print("  minimum (minimize_scalar bounded on bracket [%.4g, %.4g] MeV): ratio %.5g at E = %.5g MeV; bracket interior: %s" % (lo, hi, rmin, emin, interior))
    below = f(emin) < 2
    brackets = (f(EMIN*1.0000001) > 2) and (f(EMAX) > 2) and below
    print("  sweep brackets both crossings and the minimum: %s" % ("YES" if brackets else "NO (ratio at an end of the range is not > 2, or no region < 2)"))
    if not brackets: ISSUES.append("W/%s: sweep %g-%g MeV does not bracket both crossings of 2" % (den, EMIN, EMAX))
    summary[den] = (cross, emin, rmin)

# W/C specific checks
f, cross, (emin, rmin, interior, lo, hi) = analyse("W", "C")
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
print("\nW/C checks against plan:")
c_lo = [c for c in cross if c < emin]; c_hi = [c for c in cross if c > emin]
print("  expected crossings ~0.4 and ~6 MeV (+-10% in energy); minimum 1.5-2 MeV; min value UNSURE 0.98-1.05; ratio at 10 MeV UNSURE 2.2-2.6")
print("  found: lower crossings %s, upper crossings %s, minimum %.4g MeV" % (c_lo, c_hi, emin))
# the relevant crossings are those bounding the < 2 interval around the minimum
lo_c = max(c_lo) if c_lo else None; hi_c = min(c_hi) if c_hi else None
check("lower crossing 0.4 MeV +-10%", lo_c is not None and abs(lo_c/0.4-1) <= 0.10, "%.4g MeV (%+.1f%%)" % (lo_c, 100*(lo_c/0.4-1)))
check("upper crossing 6 MeV +-10%", hi_c is not None and abs(hi_c/6.0-1) <= 0.10, "%.4g MeV (%+.1f%%)" % (hi_c, 100*(hi_c/6.0-1)))
check("minimum energy in 1.5-2 MeV", 1.5 <= emin <= 2.0, "%.4g MeV" % emin)
check("minimum value in 0.98-1.05", 0.98 <= rmin <= 1.05, "%.5g" % rmin)
check("ratio at 10 MeV in 2.2-2.6", 2.2 <= f(10.0) <= 2.6, "%.4g" % f(10.0))
# monotonicity on tabulated W and C points: ratio at the union of table energies
Eg = sorted(set(list(MAT["W"][0]) + list(MAT["C"][0])))
Eg = [e for e in Eg if 0.1 <= e <= EMAX]
rv = [f(e) for e in Eg]
imin = int(np.argmin(rv))
dec = all(rv[i+1] <= rv[i] + 1e-12 for i in range(imin))
inc = all(rv[i+1] >= rv[i] - 1e-12 for i in range(imin, len(rv)-1))
bad_dec = [(Eg[i], rv[i], Eg[i+1], rv[i+1]) for i in range(imin) if rv[i+1] > rv[i] + 1e-12]
bad_inc = [(Eg[i], rv[i], Eg[i+1], rv[i+1]) for i in range(imin, len(rv)-1) if rv[i+1] < rv[i] - 1e-12]
print("  monotonic check on %d tabulated energies 0.1-20 MeV: lowest tabulated ratio %.5g at %.4g MeV" % (len(Eg), rv[imin], Eg[imin]))
check("ratio falls monotonically 0.1 MeV to the minimum", dec, "violations: %s" % bad_dec[:3])
check("ratio rises monotonically above the minimum to 20 MeV", inc, "violations: %s" % bad_inc[:3])
print("  tabulated W/C ratio around the minimum:", ["%.4g MeV: %.5g" % (e, f(e)) for e in Eg if 1.0 <= e <= 2.5])
print("  NOTE: the interpolated minimum sits on a table vertex (1.5 MeV); between vertices the log-log curve is a ratio of two power laws, so the true minimum may lie between table points. The location is only as good as the grid.")
f2, c2, _ = analyse("W", "Fe", EMAX=100.0)
print("  extra (outside spec range): W/Fe extended to 100 MeV: crossings of 2 at", ["%.4g" % c for c in c2], "ratio at 100 MeV %.4g" % f2(100.0))
print("\nSummary W/X: crossings of 2 (MeV), min energy (MeV), min ratio")
for k, (c, e, r) in summary.items():
    print("  W/%-8s crossings %s  min at %.4g MeV, ratio %.4g" % (k, ["%.4g" % x for x in c], e, r))
print("\nSweep notes:", ISSUES if ISSUES else "all five sweeps bracket their crossings and minimum")
print("FAILED CHECKS:", FAILS if FAILS else "none")
