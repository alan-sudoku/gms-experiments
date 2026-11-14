#!/usr/bin/env python3
"""S5 review, task (2): independent resonance-integral integration from the ENDF/B-VII.1 pointwise files used by N1.
Differences from n1_thermal_ri.py: each reaction file is integrated on its own grid (no common grid), with three
quadratures (exact lin-lin, log-log power-law pieces, trapezoid in ln E of sigma), and natural abundances are taken
as the isotope weights that S2 printed (Sears 1992) only for the weighting step. Also tests point density: the
1.457 eV In-115 resonance region is fitted with a single-level Breit-Wigner (capture shape) and its analytic integral
compared with the lin-lin integral over the same window. Reference values (Mughabghab 2003, INDC(NDS)-440, capture,
as read by S3): In 3 167, Hf 1 992, nat Gd 390, Cd-113 390 b.
Usage: python3 r4_n1_ri_independent.py   Level: derived.
"""
import os, re, csv, math
import numpy as np
from scipy.optimize import curve_fit
HERE = os.path.dirname(os.path.abspath(__file__))
C5 = os.path.normpath(os.path.join(HERE, "..", "prompt_5_code"))
RAW = os.path.join(C5, "data", "raw", "endf_sigma")
def load(nuc, mt):
    f = os.path.join(RAW, "%s_mt%d.txt" % (nuc, mt))
    if not os.path.exists(f): return None
    E, S = [], []
    for ln in open(f):
        p = ln.strip().split(",")
        if len(p) != 2: continue
        try: e, s = float(p[0]), float(p[1])
        except ValueError: continue
        E.append(e); S.append(s)
    E, S = np.array(E), np.array(S)
    o = np.argsort(E, kind="stable"); return E[o], S[o]
def clip(E, S, lo, hi):
    si = np.interp([lo, hi], E, S, left=0, right=0)
    m = (E > lo) & (E < hi)
    return np.concatenate([[lo], E[m], [hi]]), np.concatenate([[si[0]], S[m], [si[1]]])
def ri_linlin(E, S):
    E1, E2, S1, S2 = E[:-1], E[1:], S[:-1], S[1:]
    ok = E2 > E1
    E1, E2, S1, S2 = E1[ok], E2[ok], S1[ok], S2[ok]
    b = (S2 - S1)/(E2 - E1); a = S1 - b*E1
    return float(np.sum(a*np.log(E2/E1) + b*(E2 - E1)))
def ri_loglog(E, S):
    E1, E2, S1, S2 = E[:-1], E[1:], S[:-1], S[1:]
    ok = (E2 > E1) & (S1 > 0) & (S2 > 0)
    tot = 0.0
    L = np.log(E2[ok]/E1[ok]); k = np.log(S2[ok]/S1[ok])/L    # sigma = S1 (E/E1)^k ; int sigma/E dE = S1/k ((E2/E1)^k - 1)
    small = np.abs(k*L) < 1e-8
    tot += float(np.sum(np.where(small, S1[ok]*L, S1[ok]/np.where(small, 1, k)*(np.exp(k*L) - 1))))
    nz = ~ok & (E2 > E1)
    tot += float(np.sum(0.5*(S1[nz] + S2[nz])*np.log(E2[nz]/E1[nz])))
    return tot
def ri_trap(E, S): return float(np.trapezoid(S, np.log(E)))
def ri_all(nuc, mts=(102, 103, 105, 107), lo=0.5, hi=2e7):
    out = np.zeros(3)
    for mt in mts:
        t = load(nuc, mt)
        if t is None: continue
        E, S = clip(*t, lo, hi)
        out += [ri_linlin(E, S), ri_loglog(E, S), ri_trap(E, S)]
    return out
# isotope weights: read Sears abundances from the S2 data CSV (same source as N1; weighting is not the thing under test)
AB = {}
for r in csv.DictReader(l for l in open(os.path.join(C5, "data", "sears_1992_table1.csv")) if not l.startswith("#")):
    try: AB[r["label"]] = float(r["conc"])/100
    except ValueError: pass
ISO = {"nat Ag": ["107", "109"], "nat Cd": "106 108 110 111 112 113 114 116".split(), "nat In": ["113", "115"],
       "nat Gd": "152 154 155 156 157 158 160".split(), "nat Hf": "174 176 177 178 179 180".split()}
SYM = {"nat Ag": "Ag", "nat Cd": "Cd", "nat In": "In", "nat Gd": "Gd", "nat Hf": "Hf"}
n1 = {}
for r in csv.DictReader(l for l in open(os.path.join(C5, "outputs", "n1_values.csv")) if not l.startswith("#")):
    n1[r["entry"]] = r
print("%-8s %12s %12s %12s %12s %10s %10s" % ("entry", "lin-lin", "log-log", "trap ln E", "N1 (S2)", "own/S2-1", "ref (S3)"))
REF = {"nat In": 3167, "nat Hf": 1992, "nat Gd": 390, "Cd-113": 390}
rows = [("Li-6", ["Li-6"], [1.0]), ("B-10", ["B-10"], [1.0]), ("Cd-113", ["Cd-113"], [1.0])]
for k, isos in ISO.items():
    rows.append((k, ["%s-%s" % (SYM[k], m) for m in isos], [AB["%s%s" % (m, SYM[k])] for m in isos]))
for name, nucs, w in rows:
    v = sum(wi*ri_all(n) for n, wi in zip(nucs, w))
    s2 = float(n1[name]["ri_abs_20MeV_b"])
    print("%-8s %12.5g %12.5g %12.5g %12.5g %+9.2e %10s" % (name, v[0], v[1], v[2], s2, v[0]/s2 - 1, REF.get(name, "")))
s0 = 3835.0
v = ri_all("B-10")
print("\nB-10: own RI (lin-lin) / (0.4499*sigma0 Sears 3835 b) = %.4f; with log-log quadrature %.4f" % (v[0]/(2*s0*math.sqrt(0.0253/0.5)), v[1]/(2*s0*math.sqrt(0.0253/0.5))))
v2 = ri_all("B-10", lo=0.5, hi=1e4)
print("B-10 RI 0.5 eV - 10 keV only: %.1f b, ratio %.4f (1/v region)" % (v2[0], v2[0]/(2*s0*(math.sqrt(0.0253/0.5) - math.sqrt(0.0253/1e4)))))
# point-density test: In-115 1.457 eV resonance, SLBW capture shape fitted to the pointwise data in a window
E, S = load("In-115", 102)
w = (E > 1.2) & (E < 1.75)
def slbw(e, s0, e0, g, bg):  # capture: s0 * (g/2)^2/((e-e0)^2+(g/2)^2) * sqrt(e0/e) + bg/sqrt(e)
    return s0*(g/2)**2/((e - e0)**2 + (g/2)**2)*np.sqrt(e0/e) + bg/np.sqrt(e)
p, _ = curve_fit(slbw, E[w], S[w], p0=[3e4, 1.457, 0.08, 10.0])
fine = np.geomspace(1.2, 1.75, 200001)
ri_fit = np.trapezoid(slbw(fine, *p), np.log(fine))
Ew, Sw = clip(E, S, 1.2, 1.75)
print("\nIn-115 1.457 eV window 1.2-1.75 eV: %d pointwise points; SLBW fit s0 = %.0f b, E0 = %.4f eV, Gamma = %.4f eV; rms rel. residual %.2e" % (
    w.sum(), p[0], p[1], p[2], np.sqrt(np.mean((slbw(E[w], *p)/S[w] - 1)**2))))
print("  RI over window: lin-lin on the file's points %.1f b; fitted SLBW, fine grid %.1f b; difference %+.2f%%" % (ri_linlin(Ew, Sw), ri_fit, 100*(ri_linlin(Ew, Sw)/ri_fit - 1)))
print("  (the fit is to the same points, so it measures under-resolution of the file's grid against a smooth shape, not ENDF accuracy)")
