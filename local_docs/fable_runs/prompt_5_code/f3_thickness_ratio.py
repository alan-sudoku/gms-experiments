#!/usr/bin/env python3
"""Row F3 (claims G3.2, G4.1): thickness-basis ratio (mu/rho*rho)_W / (mu/rho*rho)_C over the F2 grid.

LOOKUP: NIST XCOM total attenuation with coherent scattering for Z=6 and Z=74 (data/xcom_z006.csv, z074;
XCOM web, access 2026-11-14). Densities are MEMORY inputs: rho_W = 19.3 g/cm3; graphite 1.70 and 2.26 g/cm3.
Carbon lattice: rho_eff = rel * rho_ref with rel in {0.1, 0.3, 0.5}; the plan does not say which solid density
rel refers to, so both 1.70 and 2.26 are used (recorded as an ambiguity in outputs/issues_b.md).
Method: log-log interpolation per smooth piece (as in F2); minimum by minimize_scalar on a bracket.
Note: thickness ratio = mass ratio * rho_W/rho_C, a constant multiple, so the energy of the minimum equals the F2
minimum by construction (labelled 'identity' below); only the minimum VALUE is new.
"""
import os, math
import numpy as np
from scipy.optimize import minimize_scalar
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
FAILS = []
def load(fn):
    E=[];V=[]
    for ln in open(os.path.join(D, fn)):
        if ln.startswith("#") or ln.startswith("edge"): continue
        p=ln.strip().split(","); E.append(float(p[1])); V.append(float(p[7]))
    return np.array(E), np.array(V)
M = {"C": load("xcom_z006.csv"), "W": load("xcom_z074.csv")}
def mu(n, E):
    x, y = M[n]; i = np.searchsorted(x, E, side="right")-1; i = min(max(i,0), len(x)-2)
    if x[i+1]==x[i]: return y[i+1]
    t=(math.log(E)-math.log(x[i]))/(math.log(x[i+1])-math.log(x[i])); return math.exp(math.log(y[i])+t*(math.log(y[i+1])-math.log(y[i])))
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
RW = 19.3
print("F3 inputs: rho_W=%.1f g/cm3 (MEMORY); graphite 1.70 and 2.26 g/cm3 (MEMORY); lattice rel density 0.1, 0.3, 0.5; energy range 0.03-20 MeV" % RW)
print("LOOKUP: data/xcom_z006.csv and data/xcom_z074.csv (NIST XCOM, total with coherent, access 2026-11-14)")
EMIN, EMAX = 0.03, 20.0
grid = np.exp(np.linspace(math.log(EMIN*1.0001), math.log(EMAX), 3000))
mass = np.array([mu("W", e)/mu("C", e) for e in grid])
k = int(np.argmin(mass)); lo, hi = grid[max(k-3,0)], grid[min(k+3,len(grid)-1)]
res = minimize_scalar(lambda u: mu("W", math.exp(u))/mu("C", math.exp(u)), bounds=(math.log(lo), math.log(hi)), method="bounded", options={"xatol":1e-12})
e0, m0 = math.exp(res.x), res.fun
print("mass ratio minimum (F2 repeat): %.5g at %.5g MeV, bracket [%.4g, %.4g] interior=%s" % (m0, e0, lo, hi, 3 < k < len(grid)-4))
print("\nThickness-ratio minimum over 0.03-20 MeV (minimize_scalar on bracket), and value at 0.1 and 1 MeV:")
rows = []
for ref in (1.70, 2.26):
    for rel in (1.0, 0.1, 0.3, 0.5):
        rho = ref*rel
        kappa = RW/rho
        mn = m0*kappa
        # numerical minimum of the thickness ratio itself (independent evaluation, same bracket)
        r2 = minimize_scalar(lambda u: kappa*mu("W", math.exp(u))/mu("C", math.exp(u)), bounds=(math.log(lo), math.log(hi)), method="bounded", options={"xatol":1e-12})
        label = "solid" if rel == 1.0 else "lattice rel=%.1f of %.2f" % (rel, ref)
        print("  rho_C=%.3f g/cm3 (%s): min thickness ratio %.4g at %.4g MeV; at 0.1 MeV %.4g; at 1 MeV %.4g" %
              (rho, label, math.exp(r2.fun*0)*r2.fun, math.exp(r2.x), kappa*mu("W",0.1)/mu("C",0.1), kappa*mu("W",1.0)/mu("C",1.0)))
        rows.append((ref, rel, r2.fun, math.exp(r2.x)))
        if rel == 1.0:
            exp = {1.70: 11.0, 2.26: 8.5}[ref]
            check("minimum thickness ratio ~%.1f for rho_C=%.2f (+-5%% of the plan's expected value)" % (exp, ref), abs(r2.fun/exp-1) <= 0.05, "%.4g (%+.1f%%)" % (r2.fun, 100*(r2.fun/exp-1)))
            check("never below 7 (rho_C=%.2f)" % ref, r2.fun >= 7, "%.4g" % r2.fun)
            check("[identity] energy of minimum equals F2 mass-ratio minimum energy (constant factor, true by construction)", abs(math.exp(r2.x)/e0-1) < 1e-6, "%.5g vs %.5g MeV" % (math.exp(r2.x), e0))
            check("minimum >= 3 (thickness-basis part of G3.2 not falsified)", r2.fun >= 3, "%.4g" % r2.fun)
print("\nLattice entries: minimum thickness ratio rises as 1/rel (denser tungsten, lighter carbon): all values >= the solid case:",
      all(r[2] >= [x for x in rows if x[0]==r[0] and x[1]==1.0][0][2]-1e-12 for r in rows))
print("Note: with the 2.26 reference the minimum is %.4g; with the 1.70 reference it is %.4g (plan: ~8.5 and ~11)" %
      (rows[0+4][2], rows[0][2]))
print("FAILED CHECKS:", FAILS if FAILS else "none")
