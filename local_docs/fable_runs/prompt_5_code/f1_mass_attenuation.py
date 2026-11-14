#!/usr/bin/env python3
"""Row F1 (claims G3.1, G3.3): mass attenuation coefficient of W and C at 0.1, 0.5, 1, 5 MeV.

LOOKUP: NIST XCOM (total attenuation with coherent scattering), cross-checked against
NISTIR 5632 Table 3 element pages (parsed from separate downloads). Z/A from NISTIR 5632 Table 1.
Independent route: N_A*(Z/A)*sigma_KN(E) from the closed Klein-Nishina formula vs carbon's tabulated value (2%).
Assumptions: values taken at the exact XCOM grid energies (no interpolation needed);
constants as in plan section 3 (CODATA). Everything here is level `derived` (unverified).
"""
import os, csv, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
NA = 6.02214076e23; re_cm = 2.8179403e-13; mec2 = 0.51099895  # r_e in cm
FAILS = []

def load_xcom(z):
    rows = []
    for ln in open(os.path.join(D, "xcom_z%03d.csv" % z)):
        if ln.startswith("#") or ln.startswith("edge"): continue
        p = ln.strip().split(","); rows.append([p[0]] + [float(x) for x in p[1:]])
    a = np.array([r[1:] for r in rows]); return a  # E, coh, inc, pe, pn, pe, tot_c, tot_nc
def load_el(z):
    a = []
    for ln in open(os.path.join(D, "nist_eltab_z%02d.csv" % z)):
        if ln.startswith("#") or ln.startswith("edge"): continue
        p = ln.strip().split(","); a.append([float(p[1]), float(p[2])])
    return np.array(a)
def za(z):
    for r in csv.DictReader(l for l in open(os.path.join(D, "nist_tab1_za.csv")) if not l.startswith("#")):
        if int(r["Z"]) == z: return float(r["Z_over_A"])
def at(a, E, col):
    i = np.where(np.isclose(a[:, 0], E, rtol=1e-9))[0]
    assert len(i) >= 1, "energy %g not on grid" % E
    return a[i[-1], col]            # post-edge row if duplicated (none at these energies)
def sigma_kn_barn(E):
    k = E / mec2
    f = (1+k)/k**2*(2*(1+k)/(1+2*k) - math.log(1+2*k)/k) + math.log(1+2*k)/(2*k) - (1+3*k)/(1+2*k)**2
    return 2*math.pi*re_cm**2*f/1e-24
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)

EN = [0.1, 0.5, 1.0, 5.0]
RNG = {6: [(0.148,0.155),(0.086,0.088),(0.063,0.064),(0.0265,0.0275)],
       74: [(4.3,4.6),(0.135,0.141),(0.065,0.067),(0.040,0.042)]}
RAT = [29, 1.6, 1.04, 1.5]
print("F1 inputs: E =", EN, "MeV. Constants: N_A=%.8e r_e=%.7e cm m_e c2=%.8f MeV" % (NA, re_cm, mec2))
print("LOOKUP source: data/xcom_z006.csv, data/xcom_z074.csv (NIST XCOM web, Method=Elem, access 2026-11-14, version not printed by page, UNSURE 3.1);")
print("  cross-check data/nist_eltab_z06.csv, z74 (NISTIR 5632 Table 3 HTML, same date); Z/A: data/nist_tab1_za.csv (Table 1).")
tab = {}
for z in (6, 74):
    X = load_xcom(z); T = load_el(z)
    tab[z] = []
    print("\nZ=%d  Z/A=%.5f" % (z, za(z)))
    for j, E in enumerate(EN):
        v = at(X, E, 6)   # total with coherent
        vt = T[np.isclose(T[:, 0], E, rtol=1e-9)][-1, 1]
        lo, hi = RNG[z][j]
        tab[z].append(v)
        print("  E=%5.2f MeV  XCOM total(w/coh)=%.4g  NISTIR5632 Table3=%.4g  UNSURE range [%g, %g]: %s" %
              (E, v, vt, lo, hi, "inside" if lo <= v <= hi else "OUTSIDE"))
        check("XCOM vs Table 3 transcription Z=%d E=%g (two downloads of the same NIST data, not independent physics)" % (z, E),
              abs(v - vt) <= 1.5e-3*vt + 1e-12, "%.4g vs %.4g" % (v, vt))
print("\nRatios W/C (mass basis):")
for j, E in enumerate(EN):
    r = tab[74][j]/tab[6][j]
    print("  E=%5.2f MeV  W/C=%.4g   planner approx %.3g" % (E, r, RAT[j]))
print("\nIndependent route: N_A*(Z/A)*sigma_KN vs carbon tabulated total (with coherent) [2% tolerance]")
print("  sigma_KN(k->0) = 8 pi r_e^2/3 = %.5f b (expected 0.6652)" % (8*math.pi*re_cm**2/3/1e-24))
check("sigma_KN(k->0)", abs(8*math.pi*re_cm**2/3/1e-24 - 0.6652) < 5e-5, "")
s1 = sigma_kn_barn(1.0); print("  sigma_KN(1 MeV) = %.5f b (expected ~0.2112)" % s1)
check("sigma_KN(1 MeV)", abs(s1-0.2112) < 5e-4, "%.5f" % s1)
X6 = load_xcom(6)
for E in EN:
    kn = NA*za(6)*sigma_kn_barn(E)*1e-24
    tabv = at(X6, E, 6); inc = at(X6, E, 2)
    print("  E=%4.1f MeV: N_A(Z/A)sigma_KN=%.5g  tabulated total=%.5g (dev %+.2f%%)  XCOM incoherent=%.5g (dev %+.2f%%)" %
          (E, kn, tabv, 100*(kn/tabv-1), inc, 100*(kn/inc-1)))
    if E in (0.5, 1.0):
        check("KN vs carbon total at %g MeV (2%%)" % E, abs(kn/tabv-1) <= 0.02, "%+.2f%%" % (100*(kn/tabv-1)))
print("\nFAILED CHECKS:", FAILS if FAILS else "none")
