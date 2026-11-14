#!/usr/bin/env python3
"""A3: break-even embodied ratio r = e_Al/e_Cu for Sigma*_Al = Sigma*_Cu (Kelvin optimum), and evaluation with LOOKUP values.
Spec row A3. Claim G2.3. Level: derived (unverified).
Method: sweep r in [0.2,10] (200 log points) at fixed e_Cu = 55 MJ/kg; root of Sigma*_Al/Sigma*_Cu - 1 by brentq on the NUMERICAL
minimiser of A2 (imported logic duplicated here to stay standalone). Independent root: (rho_Cu/sigma_Cu)/(rho_Al/sigma_Al).
LOOKUP: embodied energy (MJ/kg) from data/a3_embodied_energy.csv (ICE v2.0, Hammond and Jones 2011; Nuss and Eckelman 2014 SI Table S38).
Note: embodied ENERGY (cumulative energy demand) is used where the framework wants embodied exergy destroyed (UNSURE, see issues).
"""
import csv, os
import numpy as np
from scipy.optimize import minimize_scalar, brentq
here = os.path.dirname(os.path.abspath(__file__))
T0 = 298.15; I, L, tau = 1e3, 1.0, 6.31e8
MAT = {"Cu": (5.80e7, 8960.0), "Al": (3.54e7, 2700.0)}
def sig(A, m, e):
    s, r = MAT[m]; return (e*r*A*L + I*I*L*tau/(s*A))/T0
def sstar(m, e):
    s, r = MAT[m]; ref = 2*I*L*np.sqrt(r*e*tau/s)/T0
    res = minimize_scalar(lambda x: sig(np.exp(x), m, e)/ref, bounds=(np.log(1e-12), np.log(1e6)), method="bounded", options={"xatol": 1e-11})
    return sig(np.exp(res.x), m, e)
def ratio(eAl, eCu): return sstar("Al", eAl)/sstar("Cu", eCu)
fails = 0
def chk(name, val, exp, tol, absolute=False):
    global fails
    ok = abs(val-exp) <= tol if absolute else abs(val/exp-1) <= tol
    fails += (not ok)
    print(f"CHECK {name}: {val:.5f} vs {exp:.5f} tol={'+-'+str(tol) if absolute else '+-%g%%' % (tol*100)} -> {'PASS' if ok else 'FAIL'}")
ecu = 55e6
rs = np.logspace(np.log10(0.2), np.log10(10), 200)
g = np.array([ratio(r*ecu, ecu)-1 for r in rs])
brk = g.min() < 0 < g.max()
print(f"INPUTS: sigma/rho as A1/A2; e_Cu={ecu/1e6:.0f} MJ/kg fixed; I={I} A, L={L} m, tau={tau:g} s")
print(f"sweep r in [0.2,10], 200 log points: f(0.2)={g[0]:+.3f}, f(10)={g[-1]:+.3f}; sweep brackets the crossover: {brk}")
idx = np.where(np.diff(np.sign(g)) != 0)[0]
root = brentq(lambda r: ratio(r*ecu, ecu)-1, rs[idx[0]], rs[idx[0]+1], xtol=1e-13)
indep = (8960/5.8e7)/(2700/3.54e7)
print(f"brentq root r* = {root:.5f} ; independent (rho_Cu/sigma_Cu)/(rho_Al/sigma_Al) = {indep:.5f} ; spec expected 2.03")
chk("root vs independent formula", root, indep, 0.02, True)
chk("root vs spec 2.03", root, 2.03, 0.02, True)
chk("ratio at e_Al=200,e_Cu=55 (expected 1.34)", ratio(200e6, 55e6), 1.34, 0.02)
chk("ratio at equal e (expected 0.70)", ratio(55e6, 55e6), 0.70, 0.02)
print("\nLOOKUP evaluation (source: ICE v2.0 Jan 2011 summary tables; Nuss and Eckelman 2014 SI Table S38; access 2026-11-14)")
rows = []
with open(os.path.join(here, "data", "a3_embodied_energy.csv")) as f:
    for r in csv.reader(l for l in f if not l.startswith("#")):
        if r[0] == "source": continue
        rows.append(r)
def pick(src, metal, key):
    for r in rows:
        if r[0].startswith(src) and r[1] == metal and r[2].startswith(key): return float(r[3])
cases = []
for src, kal, kcu in (("ICE", "virgin (rolled", "virgin"), ("ICE", "general", "EU tube"), ("Nuss", "primary", "primary"), ("Nuss", "supply-weighted", "supply-weighted")):
    cases.append((src, "primary/primary" if "virgin" in kal or "primary" in kal else "general/general", pick(src, "Al", kal), pick(src, "Cu", kcu)))
cases.append(("ICE", "secondary Al / primary Cu", pick("ICE", "Al", "recycled"), pick("ICE", "Cu", "virgin")))
cases.append(("ICE", "secondary/secondary", pick("ICE", "Al", "recycled"), pick("ICE", "Cu", "recycled")))
cases.append(("Nuss", "secondary Al (old scrap) / primary Cu", pick("Nuss", "Al", "secondary from old"), pick("Nuss", "Cu", "primary")))
cases.append(("Nuss", "secondary/secondary (old scrap Al, refinery Cu)", pick("Nuss", "Al", "secondary from old"), pick("Nuss", "Cu", "secondary (refinery")))
print(f"break-even r* = {indep:.4f}; Al wins in Sigma iff e_Al/e_Cu < r*")
print("source  case                                       e_Al  e_Cu  r=eAl/eCu  Sigma*Al/Sigma*Cu  closed  Al wins?")
for src, name, ea, ec in cases:
    q = ratio(ea*1e6, ec*1e6); cl = np.sqrt((ea*2700/3.54e7)/(ec*8960/5.8e7))
    assert abs(q/cl-1) < 1e-6
    print(f"{src:5s} {name:48s} {ea:6.1f} {ec:5.1f} {ea/ec:7.3f} {q:10.4f} {cl:10.4f}   {'yes' if q < 1 else 'no'}")
print("\nPlanner UNSURE ranges: primary Al 150-220 (ICE 218, Nuss 194: inside), secondary Al 10-30 (ICE 29.0, Nuss old scrap 23.8: inside; new scrap 8.3: below),")
print("primary Cu 35-75 (ICE 57, Nuss 59.3: inside), secondary Cu 10-20 (ICE 16.5 inside; Nuss refinery secondary 28.1: ABOVE range; electronic scrap 1.8: below)")
print("Equal-e MEMORY central pair 200/55 -> r=3.64 > 2.03 -> Al loses (1.34). ICE primary/primary r=3.82 -> Al loses; Nuss primary/primary r=3.27 -> Al loses.")
print("IDENTITY CHECKS: the root vs independent formula compares brentq-on-numerical-minimiser with algebra (not identity). 'closed' column assert is minimiser-vs-algebra.")
print("OVERALL", "PASS" if fails == 0 and brk else "FAIL")
