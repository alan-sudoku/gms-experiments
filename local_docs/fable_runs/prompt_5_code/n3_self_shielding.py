#!/usr/bin/env python3
"""Row N3 (claims G1.4, G3.8, G2.9): self-shielding of an absorber slab in an isotropic flux.

P(tau) = 1 - 2*E3(tau) (scipy.special.expn(3, tau)), f = P/(2 tau), tau = Sigma_a * t.
Sigma_a = rho*N_A*w*sigma_a/M for Cd metal, natural B4C, Gd metal, steel with 1 wt% B (boron only; Fe added as info).
LOOKUP: sigma_a from outputs/n1_values.csv (Sears 1992 natural-element values, ENDF/B-VII.1 column also run); molar masses from
data/nist_atomic_weights.csv (NIST/IUPAC standard atomic weights, access 2026-11-14). rho: Cd 8.65, B4C 2.52, Gd 7.90, steel 7.8 g/cm3 (MEMORY).
Independent route: Monte Carlo, cosine-law incidence (direction cosine = sqrt(u)), absorption 1-exp(-tau/cosine), 1e6 samples, seed 20261114.
Sweep tau in [1e-3, 1e2]. Level `derived`. Run n1_thermal_ri.py first.
"""
import os, csv, math
import numpy as np
from scipy.special import expn
from scipy.optimize import brentq
from scipy.integrate import quad
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
NA = 6.02214076e23; SEED = 20261114; N = 1_000_000; FAILS = []
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
P = lambda t: 1 - 2*expn(3, t)
f = lambda t: P(t)/(2*t)
AW = {r["symbol"]: float(r["A_r"]) for r in csv.DictReader(l for l in open(os.path.join(D, "nist_atomic_weights.csv")) if not l.startswith("#"))}
N1 = {r["entry"]: r for r in csv.DictReader(l for l in open(os.path.join(HERE, "outputs", "n1_values.csv")) if not l.startswith("#"))}
print("N3 LOOKUP: sigma_a <- outputs/n1_values.csv (Sears 1992 Table 1 via NIST NCNR; ENDF/B-VII.1 via NNDC Sigma); molar masses <- data/nist_atomic_weights.csv (NIST/IUPAC, midpoint of interval where given)")
print("  A_r: B %.4f  C %.4f  Fe %.3f  Cd %.3f  Gd %.2f" % (AW["B"], AW["C"], AW["Fe"], AW["Cd"], AW["Gd"]))
print("  MEMORY densities (g/cm3): Cd 8.65, B4C 2.52, Gd 7.90, steel 7.8")
# --- sweep
taus = np.logspace(-3, 2, 41)
fv = np.array([f(t) for t in taus]); Pv = np.array([P(t) for t in taus])
print("\n--- Sweep tau = 1e-3 .. 1e2 (E3 via scipy.special.expn) ---")
print("  tau        P          f=P/(2 tau)")
for t in (1e-3, 1e-2, 0.1, 0.3, 1, 3, 10, 100):
    print("  %-8g %.6f   %.6f" % (t, P(t), f(t)))
check("f monotonic decreasing over the sweep", bool(np.all(np.diff(fv) < 0)), "f(1e-3)=%.6f f(1e2)=%.6f" % (fv[0], fv[-1]))
check("limit P -> 2 tau at tau=1e-3 within 0.5% (Cauchy chord 4V/S = 2t)", abs(P(1e-3)/(2e-3)-1) < 0.005, "P/(2 tau) = %.6f" % (P(1e-3)/2e-3))
check("black limit P -> 1 at tau=100 (1e-9)", abs(P(100.0)-1) < 1e-9, "1-P = %.2e" % (1-P(100.0)))
e3 = quad(lambda u: math.exp(-2.5*u)/u*0 + math.exp(-2.5/u)*0 + u*math.exp(-2.5/u), 0, 1)[0]   # E3(x)=int_0^1 u exp(-x/u) du
check("scipy expn(3,2.5) vs direct quadrature of int_0^1 u exp(-x/u) du (1e-10)", abs(e3-expn(3, 2.5)) < 1e-10, "%.12f vs %.12f" % (e3, expn(3, 2.5)))
tb = brentq(lambda t: P(t)-0.9, 1e-3, 1e2); print("  tau at which a slab absorbs 90%% of an isotropic flux: %.4f (f=%.4f)" % (tb, f(tb)))
print("  black criterion check: P(tau=3) = %.4f" % P(3.0))
# --- MC
rng = np.random.default_rng(SEED)
c = np.sqrt(rng.random(N))      # cosine-law incidence, pdf 2c on (0,1]
bad = 0; zmax = 0
mt = np.logspace(-3, 2, 21)
print("\n--- Monte Carlo (cosine-law, %d samples, seed %d) vs 1-2E3 ---" % (N, SEED))
for t in mt:
    s = 1 - np.exp(-t/c); m = s.mean(); se = s.std(ddof=1)/math.sqrt(N); tol = max(3*se, 1e-9); z = abs(m-P(t))/max(se, 1e-9/3); zmax = max(zmax, z); bad += abs(m-P(t)) > tol   # tol floor 1e-9 when the sample variance vanishes (tau >> 1)
print("  %d tau values (1e-3..1e2): max |z| = %.2f, %d outside 3 sigma (chance ~%.2f)" % (len(mt), zmax, bad, 0.0027*len(mt)))
for t in (1e-3, 1.0, 10.0):
    s = 1 - np.exp(-t/c); print("   tau=%-6g MC %.6f +- %.1e  analytic %.6f" % (t, s.mean(), s.std(ddof=1)/math.sqrt(N), P(t)))
check("MC vs 1-2E3 within 3 sigma at all tau (<=1 chance excursion)", bad <= 1, "%d/%d" % (bad, len(mt)))
# --- materials
def Sigma(rho, w, sig_b, M): return rho*NA*w*sig_b*1e-24/M
wB4C = 4*AW["B"]/(4*AW["B"]+AW["C"])
def mats(col):
    s = lambda e: float(N1[e][col])
    return {
     "Cd metal": (Sigma(8.65, 1.0, s("nat Cd"), AW["Cd"]), 117.0, "nat Cd"),
     "natural B4C (B only)": (Sigma(2.52, wB4C, s("nat B"), AW["B"]), 84.0, "nat B"),
     "Gd metal": (Sigma(7.90, 1.0, s("nat Gd"), AW["Gd"]), 1480.0, "nat Gd"),
     "steel 1 wt% B (B only)": (Sigma(7.8, 0.01, s("nat B"), AW["B"]), 3.3, "nat B"),
    }
for col, label in (("sigma_sears_b", "Sears 1992 (primary)"), ("sigma_endf_b", "ENDF/B-VII.1 at 0.0253 eV (comparison)")):
    print("\n=== sigma_a source: %s ===" % label)
    print("  B4C boron mass fraction w_B = %.5f" % wB4C)
    M = mats(col)
    print("  %-24s %10s %10s  %s" % ("material", "Sigma_a", "planner", "vs UNSURE (+-5% band shown)"))
    for k, (S, exp, el) in M.items():
        print("  %-24s %9.4g /cm %8g   %+.1f%%  [sigma_a = %.5g b]" % (k, S, exp, 100*(S/exp-1), float(N1[el][col])))
    if col == "sigma_sears_b":
        MS = M
    print("  thickness at f = 0.9 and f = 0.5 (brentq on f(tau)-f0, bracket [1e-3,1e2] contains both: f(1e-3)=%.4f > f0 > f(1e2)=%.4f):" % (f(1e-3), f(1e2)))
    for k, (S, exp, el) in M.items():
        t9 = brentq(lambda t: f(t)-0.9, 1e-3, 1e2, xtol=1e-14); t5 = brentq(lambda t: f(t)-0.5, 1e-3, 1e2, xtol=1e-14)
        print("   %-24s tau(f=0.9)=%.4f -> t = %.4g mm; tau(f=0.5)=%.4f -> t = %.4g mm" % (k, t9, 10*t9/S, t5, 10*t5/S))
    S = M["Cd metal"][0]; t = S*0.1
    print("   f for 1 mm Cd: tau = %.3f, P = %.5f, f = %.5f" % (t, P(t), f(t)))
t9 = brentq(lambda t: f(t)-0.9, 1e-3, 1e2); t5 = brentq(lambda t: f(t)-0.5, 1e-3, 1e2)
print("\nUniversal values: tau(f=0.9) = %.5f, tau(f=0.5) = %.5f (independent of material)" % (t9, t5))
check("planner Sigma_a: Cd ~117, B4C ~84, borated steel ~3.3 (each within 5% of the UNSURE value, Sears sigma)", all(abs(MS[k][0]/MS[k][1]-1) < 0.05 for k in ("Cd metal", "natural B4C (B only)", "steel 1 wt% B (B only)")), "see table above")
print("  Gd metal Sigma_a: planner ~1480; Sears-based value %.1f is %+.1f%% from it" % (MS["Gd metal"][0], 100*(MS["Gd metal"][0]/1480-1)))
print("\nBlack absorbers (tau >= 3 : P >= %.3f): 1 mm Cd tau = %.1f, 1 mm B4C tau = %.1f, 1 mm Gd tau = %.1f, 1 mm borated steel tau = %.2f" % (
      P(3.0), MS["Cd metal"][0]*0.1, MS["natural B4C (B only)"][0]*0.1, MS["Gd metal"][0]*0.1, MS["steel 1 wt% B (B only)"][0]*0.1))
print("FAILED CHECKS:", FAILS if FAILS else "none")
