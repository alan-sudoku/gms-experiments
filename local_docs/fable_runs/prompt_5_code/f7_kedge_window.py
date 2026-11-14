#!/usr/bin/env python3
"""Row F7 (claim G3.5): K-edge window, ranking of Sn, W, Pb (and Bi, Gd, Ba) by mu/rho at 40, 60, 80, 100 keV.

LOOKUP: NIST XCOM total attenuation with coherent scattering (data/xcom_z050.csv Sn, z074 W, z082 Pb, z083 Bi,
z064 Gd, z056 Ba; XCOM web, access 2026-11-14), cross-checked for Sn, W, Pb against NISTIR 5632 Table 3
(data/nist_eltab_z50.csv, z74, z82). The four energies are XCOM grid points. K-edges (MEMORY): Sn 29.2, W 69.5, Pb 88.0 keV;
the K-edge energies found in the XCOM files are printed for comparison. Level `derived`.
"""
import os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
FAILS=[]
def load(fn, ecol, vcol):
    a=[]; e=[]
    for ln in open(os.path.join(D,fn)):
        if ln.startswith("#") or ln.startswith("edge"): continue
        p=ln.strip().split(","); a.append((p[0], float(p[ecol]), float(p[vcol])))
    return a
def val(a,E): return [v for (_,e,v) in a if abs(e/E-1)<1e-9][-1]
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
EL={"Sn":50,"W":74,"Pb":82,"Bi":83,"Gd":64,"Ba":56}
X={k:load("xcom_z%03d.csv"%z,1,7) for k,z in EL.items()}
T={k:load("nist_eltab_z%02d.csv"%EL[k],1,2) for k in ("Sn","W","Pb")}
EN=[0.04,0.06,0.08,0.10]
RNG={0.06:{"Sn":(6,7),"Pb":(4.8,5.2),"W":(3.6,3.8)},0.08:{"W":(7.6,8.0),"Sn":(2.9,3.2),"Pb":(2.3,2.5)},0.10:{"Pb":(5.4,5.7),"W":(4.3,4.6),"Sn":(1.6,1.8)}}
print("F7 LOOKUP: data/xcom_z050.csv (Sn), z074 (W), z082 (Pb), z083 (Bi), z064 (Gd), z056 (Ba); XCOM web, access 2026-11-14; mu/rho total with coherent, cm2/g")
print("K-edge energies in the XCOM files (keV):", {k:[round(e*1000,3) for (ed,e,_) in X[k] if ed=="K"] for k in EL}, "; MEMORY: Sn 29.2, W 69.5, Pb 88.0")
rank={}
for E in EN:
    vals={k:val(X[k],E) for k in EL}
    order=sorted(vals,key=lambda k:-vals[k]); rank[E]=order
    print("\nE = %3.0f keV: "%(E*1000)+"  ".join("%s=%.4g"%(k,vals[k]) for k in EL))
    print("  ranking (high to low): "+" > ".join(order))
    sub=sorted(("Sn","W","Pb"),key=lambda k:-vals[k]); print("  Sn/W/Pb ranking: "+" > ".join(sub))
    if E in RNG:
        for k,(lo,hi) in RNG[E].items():
            print("  vs UNSURE range %s: %.4g in [%g, %g] -> %s"%(k,vals[k],lo,hi,"inside" if lo<=vals[k]<=hi else "OUTSIDE"))
    for k in ("Sn","W","Pb"):
        t=val(T[k],E)
        check("XCOM vs Table 3 transcription %s %g keV (same NIST data, not independent)"%(k,E*1000), abs(vals[k]-t)<=2e-3*t, "%.4g vs %.4g"%(vals[k],t))
sn=lambda E:[k for k in rank[E] if k in("Sn","W","Pb")]
print("\nG3.5 statement: Sn > Pb > W near 60 keV, W > Sn > Pb near 80 keV, Pb > W > Sn at 100 keV")
check("60 keV Sn > Pb > W", sn(0.06)==["Sn","Pb","W"], " > ".join(sn(0.06)))
check("80 keV W > Sn > Pb", sn(0.08)==["W","Sn","Pb"], " > ".join(sn(0.08)))
check("100 keV Pb > W > Sn", sn(0.10)==["Pb","W","Sn"], " > ".join(sn(0.10)))
leaders={E:rank[E][0] for E in EN}
print("leader (of all six) at each energy:",{int(E*1000):v for E,v in leaders.items()})
check("no single element leads (Sn,W,Pb) at all four energies (else G3.5 false)", len({sn(E)[0] for E in EN})>1, str({int(E*1000):sn(E)[0] for E in EN}))
print("FAILED CHECKS:", FAILS if FAILS else "none")
