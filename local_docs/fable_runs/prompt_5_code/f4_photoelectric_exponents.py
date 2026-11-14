#!/usr/bin/env python3
"""Row F4 (claim G3.3): photoelectric Z and E exponents, and carbon's Compton fraction at 100 keV.

LOOKUP: NIST XCOM partial cross sections (photoelectric absorption, incoherent, coherent, totals), cm2/g,
Z = 6, 13, 26, 29, 50, 74, 82 (data/xcom_z*.csv, XCOM web, access 2026-11-14). Z/A from NISTIR 5632 Table 1.
Method: least-squares slope of ln(tau/rho) vs ln Z at 100 keV (per mass); per atom: ln(tau/rho * A) with A = Z/(Z/A).
Energy exponent: slope of ln tau vs ln E for W from 100 to 500 keV (tabulated points, also two-point). All level `derived`.
Caveat recorded: at 100 keV Sn (K edge 29.2 keV), W (69.5 keV) and Pb (88.0 keV) are all above their K edges; only
Pb is within 12% of its edge, so the K-shell step is part of the fitted trend.
"""
import os, csv, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
FAILS = []
def load(z):
    a=[]
    for ln in open(os.path.join(D,"xcom_z%03d.csv"%z)):
        if ln.startswith("#") or ln.startswith("edge"): continue
        p=ln.strip().split(","); a.append([float(x) for x in p[1:]])
    return np.array(a)   # E coh inc pe pn pe tot_c tot_nc
def za(z):
    for r in csv.DictReader(l for l in open(os.path.join(D,"nist_tab1_za.csv")) if not l.startswith("#")):
        if int(r["Z"])==z: return float(r["Z_over_A"])
def row(a,E): return a[np.where(np.isclose(a[:,0],E,rtol=1e-9))[0][-1]]
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
Zs=[6,13,26,29,50,74,82]
print("F4 LOOKUP: XCOM partial tables data/xcom_z006.csv ... z082.csv (photoelectric column), E = 0.1 MeV (grid point), access 2026-11-14")
tau=[]; A=[]
print("  Z   Z/A      A=Z/(Z/A)  tau/rho (cm2/g) at 100 keV")
for z in Zs:
    r=row(load(z),0.1); tau.append(r[3]); A.append(z/za(z))
    print("  %2d  %.5f  %8.3f   %.5g" % (z, za(z), A[-1], r[3]))
x=np.log(Zs); y=np.log(tau)
def fit(x,y):
    p=np.polyfit(x,y,1); res=y-np.polyval(p,x); return p[0], p[1], np.sqrt(np.sum(res**2)/(len(x)-2)) if len(x)>2 else float('nan')
sm, ic, rms=fit(x,y)
sa, _, _=fit(x, np.log(np.array(tau)*np.array(A)))
print("\nFit all 7 elements: Z exponent per mass = %.3f (rms residual in ln %.3f), per atom = %.3f" % (sm, rms, sa))
print("  UNSURE expected: 2.8-3.6 per mass, 3.8-4.6 per atom. A per-mass exponent >= 3.9 would falsify G3.3.")
check("Z exponent per mass in 2.8-3.6", 2.8<=sm<=3.6, "%.3f" % sm)
check("Z exponent per atom in 3.8-4.6", 3.8<=sa<=4.6, "%.3f" % sa)
check("per-mass exponent < 3.9 (G3.3 stands)", sm<3.9, "%.3f" % sm)
print("  Sensitivity (extra, not a spec check): leave-one-out per-mass exponents")
for i,z in enumerate(Zs):
    m=[j for j in range(len(Zs)) if j!=i]; s,_,_=fit(x[m],y[m]); print("    without Z=%2d: %.3f" % (z, s))
s2,_,_=fit(x[[0,5]],y[[0,5]]); print("  two-point C to W slope (extra): %.3f -> ratio tau_W/tau_C = %.4g" % (s2, tau[5]/tau[0]))
print("  [note] the fitted line is a least-squares summary over a range where the local slope varies; the K-edge position relative to 100 keV changes the apparent exponent.")
# energy exponent W
W=load(74); sel=[E for E in W[:,0] if 0.1-1e-12<=E<=0.5+1e-12]
pts=[]
for E in sorted(set(sel)):
    pts.append((E,row(W,E)[3]))
ee=np.array([p[0] for p in pts]); tt=np.array([p[1] for p in pts])
s_lsq=np.polyfit(np.log(ee),np.log(tt),1)[0]; s_2=math.log(tt[-1]/tt[0])/math.log(ee[-1]/ee[0])
print("\nW photoelectric energy exponent, 100-500 keV on %d tabulated points %s MeV:" % (len(ee), list(ee)))
print("  least-squares slope = %.3f; two-point 100->500 keV = %.3f (UNSURE expected -2.6 to -3.1)" % (s_lsq, s_2))
check("energy exponent in -3.1..-2.6 (lsq)", -3.1<=s_lsq<=-2.6, "%.3f" % s_lsq)
check("energy exponent in -3.1..-2.6 (two-point)", -3.1<=s_2<=-2.6, "%.3f" % s_2)
print("  no W K-edge inside 100-500 keV (69.5 keV is below); local slopes between points:", ["%.2f" % (math.log(tt[i+1]/tt[i])/math.log(ee[i+1]/ee[i])) for i in range(len(ee)-1)])
# carbon compton fraction
C=row(load(6),0.1)
print("\nCarbon at 100 keV (cm2/g): coherent=%.4g incoherent=%.4g photoelectric=%.4g total(w/coh)=%.4g total(w/o coh)=%.4g" % (C[1],C[2],C[3],C[6],C[7]))
f1=C[2]/C[6]; f2=C[2]/C[7]
print("  Compton (incoherent) fraction of total with coherent = %.4f; of total without coherent = %.4f (UNSURE expected >= 0.85)" % (f1,f2))
check("carbon incoherent fraction >= 0.85 (with coherent total)", f1>=0.85, "%.4f" % f1)
check("carbon incoherent fraction >= 0.85 (without coherent)", f2>=0.85, "%.4f" % f2)
print("  ratio of photoelectric parts W/C at 100 keV = %.4g; if the Z^4/E^3 law were the whole story with Z^3 per mass, (74/6)^3 = %.4g" % (tau[5]/tau[0], (74/6)**3))
print("FAILED CHECKS:", FAILS if FAILS else "none")
