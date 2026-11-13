"""S4 follow-up for rows B06, B07, B09, B11 (claims B2.5, B2.6, B2.7).  Level: derived (unverified).

Purpose (stage S4, finaliser; S2 scripts are not edited):
 (a) pins: which friction branch is active at the 'favourable' B07 winners (f_K is non-monotone in the
     pitch ratio, B06), and an extended pin sweep with the monotone friction f_J only.
 (b) gyroid: the B09 sweep did not bracket the optimum (139 of 180 winners on an edge).  Extended sweep
     in cell size and relative density; chi_min for the Cu plate optimum and the Al plate optimum,
     once for all cell sizes and once restricted to H/a >= 3 (at least three cells in the fin height).
 (c) equal volume flow with re-optimised designs (B11 used the fixed 0.1 W designs): smallest air power
     at V = V_Cu,opt for which each architecture reaches the Cu plate optimum's R_fa; and the best R_fa
     at that flow under pressure caps.
 (d) context numbers: wetted area per volume of the plate optimum, of gyroid cells and of a coarse pin
     benchmark; analogy factor implied by 'friction n_f x tube, Nu n_h x tube'.
Inputs: gms_core constants and models (plan sections 3.0, 3.1).  The gyroid model stays parametric
(c_f, chi); nothing here validates it.  Run: python3 s4_b_pin_gyroid.py > outputs/s4_b_pin_gyroid.txt
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *  # noqa: F401,F403

print("S4 pin and gyroid follow-up  (level: derived, unverified)")

CU = {P: best(plate_designs(390.0), P) for P in P_SET}
ALP = {(k, P): best(plate_designs(float(k)), P) for k in (100, 150, 180) for P in P_SET}

# ---------------------------------------------------------------- (a)
head("(a1) Active friction branch at the favourable B07 winners")
nK = 0
tot = 0
for P in P_SET:
    for k in [390, 200, 180, 150, 120, 100]:
        R, r, d = best(pin_designs(float(k), "min", "K"), P)
        act = "f_K" if r["fK"] < r["fJ"] else "f_J"
        nK += act == "f_K"
        tot += 1
        print("  P=%4.2f k=%3d  d=%.1f mm p=%.2f Re_d=%6.1f  f_K=%.4f f_J=%.4f  active: %s" % (P, k, d.d * 1e3, d.p, r["Re"], r["fK"], r["fJ"], act))
print("winners with f_K active: %d of %d" % (nK, tot))
nK2 = 0
tot2 = 0
for P in P_SET:
    for d in pin_designs(150.0, "min", "K"):
        V = V_at_P(d, P)
        r = d.eval(V)
        tot2 += 1
        nK2 += r["fK"] < r["fJ"]
print("all sweep designs (k=150, five P_air): f_K lower than f_J in %d of %d operating points" % (nK2, tot2))

head("(a2) Extended pin sweep, Nu_K with f_J only (monotone in pitch ratio)")
D_EXT = [0.5e-3, 0.75e-3, 1.0e-3, 1.5e-3, 2.0e-3, 3.0e-3, 4.0e-3]
P_EXT = [1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 3.5, 4.0]
print("d [mm] = %s ; p = %s ; d < 1 mm is below the plan's assumed LPBF limit (H/d > 30)" % ([x * 1e3 for x in D_EXT], P_EXT))
worst = None
for k in [390, 150]:
    for P in P_SET:
        ds = [PIN(d, p, float(k), "J", "K") for d in D_EXT for p in P_EXT]
        rk = ranked(ds, P)
        R, r, d = rk[0]
        ds1 = [x for x in ds if x.d >= 1.0e-3 - 1e-12]
        R1, r1, d1 = ranked(ds1, P)[0]
        edge = []
        if d.d in (D_EXT[0], D_EXT[-1]):
            edge.append("d edge")
        if d.p in (P_EXT[0], P_EXT[-1]):
            edge.append("p edge")
        ref_al = ALP[(150, P)][0] if k == 150 else CU[P][0]
        print("  k=%3d P=%4.2f  best: R_fa=%.4f d=%.2f mm p=%.2f N=%d Re_d=%.0f eta=%.3f NTU=%.2f %s [%s] ratio to Cu plate %.3f, to plate of same k %.3f" % (
            k, P, R, d.d * 1e3, d.p, d.N, r["Re"], r["eta"], r["NTU"], r["flags"], "; ".join(edge) if edge else "interior",
            R / CU[P][0], R / ref_al))
        print("                 with d >= 1 mm: R_fa=%.4f d=%.2f mm p=%.2f Re_d=%.0f  ratio to Cu plate %.3f, to plate of same k %.3f   [B07 favourable: %.4f]" % (
            R1, d1.d * 1e3, d1.p, r1["Re"], R1 / CU[P][0], R1 / ref_al, best(pin_designs(float(k), "min", "K"), P)[0]))
        if worst is None or R / CU[P][0] < worst[0]:
            worst = (R / CU[P][0], k, P)
print("smallest pin / Cu-plate ratio in the extended sweep (any d): %.3f at k=%d, P=%g W" % worst)

# ---------------------------------------------------------------- (b)
head("(b) Gyroid: extended sweep and chi_min")
A_EXT = [1.5e-3, 2e-3, 2.5e-3, 3e-3, 4e-3, 5e-3, 6e-3, 8e-3, 10e-3, 12e-3, 15e-3, 20e-3, 30e-3]
R_EXT = [0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50]
print("a [mm] = %s ; rho_bar = %s ; t_s >= 0.3 mm kept" % ([x * 1e3 for x in A_EXT], R_EXT))


def gdes(k, cf, restricted):
    out = []
    for a in A_EXT:
        if restricted and H / a < 3 - 1e-9:
            continue
        for rb in R_EXT:
            g = GY(a, rb, float(k), cf, 0.2)
            if g.valid:
                out.append(g)
    return out


def gbest(ds, chi, P):
    bestv = None
    for g in ds:
        g.chi = chi
        V = V_at_P(g, P)
        if V is None:
            continue
        r = g.eval(V)
        if bestv is None or r["R_fa"] < bestv[0]:
            bestv = (r["R_fa"], r, g)
    return bestv


def chi_min(ds, P, target):
    if gbest(ds, 1.0, P)[0] > target:
        return None
    lo, hi = 0.01, 1.0
    if gbest(ds, lo, P)[0] <= target:
        return lo
    while hi - lo > 1e-4:
        mid = 0.5 * (lo + hi)
        if gbest(ds, mid, P)[0] > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def edge_note(g, restricted):
    alist = [a for a in A_EXT if (not restricted) or H / a >= 3 - 1e-9]
    n = []
    if g.a == alist[0]:
        n.append("a min")
    if g.a == alist[-1]:
        n.append("a max" + (" (H/a = 3 limit)" if restricted else ""))
    if g.rb == R_EXT[0]:
        n.append("rho min")
    if g.rb == R_EXT[-1]:
        n.append("rho max")
    return "; ".join(n) if n else "interior"


for restricted in (False, True):
    print("\n--- %s ---" % ("restricted to H/a >= 3 (a <= 10 mm)" if restricted else "all cell sizes (H/a down to 1)"))
    nedge = 0
    ncase = 0
    for k in (100, 150, 180):
        for cf in (1.0, 0.3, 0.1):
            ds = gdes(k, cf, restricted)
            for P in P_SET:
                tCu, tAl = CU[P][0], ALP[(k, P)][0]
                c1, c2 = chi_min(ds, P, tCu), chi_min(ds, P, tAl)
                Rb, rb_, gb = gbest(ds, 0.35, P)
                en = edge_note(gb, restricted)
                ncase += 1
                nedge += en != "interior"
                f = lambda c: "no match (chi<=1)" if c is None else "%.3f" % c
                extra = ""
                if c1 is None:
                    extra = "  [R_fa(chi=1)=%.4f, min 1/C=%.4f]" % (gbest(ds, 1.0, P)[0], min(g.eval(V_at_P(g, P))["invC"] for g in ds))
                print("  k_s=%3d c_f=%.1f P=%4.2f  chi_min(Cu plate %.4f)=%s  chi_min(Al plate %.4f)=%s  | winner at chi=0.35: R_fa=%.4f a=%.1f mm rho=%.2f t_s=%.2f mm Re_h=%.0f eta=%.2f [%s]%s" % (
                    k, cf, P, tCu, f(c1), tAl, f(c2), Rb, gb.a * 1e3, gb.rb, gb.ts * 1e3, rb_["Re"], rb_["eta"], en, extra))
    print("  winners (chi = 0.35) on an edge of this sweep: %d of %d" % (nedge, ncase))

head("(b2) Sensitivity at the nominal case (k_s = 150, P = 0.1 W): S2 sweep against extended sweeps")
for cf in (1.0, 0.3, 0.1):
    ds_s2 = gy_designs(150.0, cf, 0.2)
    for name, ds in (("S2 sweep", ds_s2), ("extended, all a", gdes(150, cf, False)), ("extended, H/a>=3", gdes(150, cf, True))):
        c1 = chi_min(ds, 0.1, CU[0.1][0])
        c2 = chi_min(ds, 0.1, ALP[(150, 0.1)][0])
        print("  c_f=%.1f %-18s chi_min(Cu)=%s chi_min(Al plate)=%s ; best R_fa at chi=0.2: %.4f, at chi=0.35: %.4f" % (
            cf, name, "none" if c1 is None else "%.3f" % c1, "none" if c2 is None else "%.3f" % c2,
            gbest(ds, 0.2, 0.1)[0], gbest(ds, 0.35, 0.1)[0]))

# ---------------------------------------------------------------- (c)
head("(c) Equal volume flow V = V_Cu,opt(0.1 W), designs re-optimised at that flow")
Vc = CU[0.1][1]["V"]
target = CU[0.1][0]
print("V_Cu,opt = %.5e m3/s ; Cu plate optimum R_fa = %.4f K/W at dP = %.2f Pa, P_air = 0.1 W ; 1/C = %.4f K/W" % (Vc, target, CU[0.1][1]["dP"], CU[0.1][1]["invC"]))
tfree = [round(0.05e-3 * i, 7) for i in range(4, 41)]   # 0.2 ... 2.0 mm


def plates(k, tmin):
    out = []
    for t in tfree:
        if t < tmin - 1e-12:
            continue
        Nf = 6
        while (W - Nf * t) / (Nf - 1) >= S_MIN - 1e-12:
            out.append(PF(t, Nf, float(k)))
            Nf += 1
    return out


def gset(k, cf, chi):
    out = gdes(k, cf, True)
    for g in out:
        g.chi = chi
    return out


archs = [
    ("Cu plate (t >= 0.3 mm)", plates(390, 0.3e-3)),
    ("Al plate k=150 (t >= 0.4 mm)", plates(150, 0.4e-3)),
    ("Al plate k=100 (t >= 0.4 mm)", plates(100, 0.4e-3)),
    ("Al pin k=150 (Nu_K, f_J, d >= 1 mm)", [PIN(d, p, 150.0, "J", "K") for d in D_EXT if d >= 1e-3 - 1e-12 for p in P_EXT]),
    ("Gyroid k_s=150 c_f=0.3 chi=0.2 (H/a>=3)", gset(150, 0.3, 0.2)),
    ("Gyroid k_s=150 c_f=1.0 chi=0.1 (H/a>=3)", gset(150, 1.0, 0.1)),
    ("Gyroid k_s=150 c_f=0.3 chi=0.1 (H/a>=3)", gset(150, 0.3, 0.1)),
]
for name, ds in archs:
    ev = []
    for d in ds:
        r = d.eval(Vc)
        if r["excluded"]:
            continue
        ev.append((r, d))
    ok = [(r["P_air"], r, d) for r, d in ev if r["R_fa"] <= target * (1 + 1e-9)]
    print("  %s" % name)
    if ok:
        ok.sort(key=lambda x: x[0])
        Pm, r, d = ok[0]
        print("     smallest air power reaching R_fa <= %.4f: P_air = %.4f W (x%.2f of 0.1 W), dP = %.1f Pa, R_fa = %.4f, eta = %.3f, NTU = %.2f  %s" % (
            target, Pm, Pm / 0.1, r["dP"], r["R_fa"], r["eta"], r["NTU"], d.label()))
    else:
        print("     no design in the sweep reaches R_fa <= %.4f at this flow" % target)
    for cap in (30.0, 60.0, 120.0, 1e9):
        c = [(r["R_fa"], r, d) for r, d in ev if r["dP"] <= cap]
        if not c:
            print("     dP cap %6.0f Pa: no design" % cap)
            continue
        c.sort(key=lambda x: x[0])
        R, r, d = c[0]
        print("     dP cap %s: best R_fa = %.4f (x%.3f of Cu target), dP = %.1f Pa, P_air = %.3f W, NTU = %.2f  %s" % (
            "none   " if cap > 1e8 else "%4.0f Pa" % cap, R, R / target, r["dP"], r["P_air"], r["NTU"], d.label()))

# ---------------------------------------------------------------- (d)
head("(d) Context numbers")
dcu = CU[0.1][2]
r = CU[0.1][1]
vol = W * L * H
print("wetted area per envelope volume: Cu plate optimum (0.1 W) = %.0f m2/m3 ; Al plate optimum k=150 = %.0f m2/m3" % (
    (r["A_f"] + r["A_b"]) / vol, (ALP[(150, 0.1)][1]["A_f"] + ALP[(150, 0.1)][1]["A_b"]) / vol))
for a in (2.5e-3, 5e-3, 10e-3):
    print("   sheet gyroid a = %.1f mm: a_sf = 2 s_G/a = %.0f m2/m3" % (a * 1e3, 2 * S_G / a))
pitch, vf = 10e-3, 0.20
dpin = math.sqrt(4 * vf / math.pi) * pitch
print("   pin benchmark read as square array, pitch 10 mm, volume fraction 0.20 (reading of the thesis summary, UNSURE): d = %.2f mm, a_sf = pi d/pitch^2 = %.0f m2/m3" % (
    dpin * 1e3, math.pi * dpin / pitch ** 2))
for a in (2.5e-3, 5e-3, 10e-3):
    print("      area ratio gyroid(a = %.1f mm)/pin benchmark = %.1f" % (a * 1e3, (2 * S_G / a) / (math.pi * dpin / pitch ** 2)))
print("analogy factor chi = j/f_F for laminar fully developed tube flow: Nu/(16 Pr^(1/3)) = %.3f (Nu = 3.66), %.3f (Nu = 4.36)" % (
    3.66 / (16 * PR ** (1 / 3)), 4.36 / (16 * PR ** (1 / 3))))
print("   parallel plates: Nu/(24 Pr^(1/3)) = %.3f (Nu = 7.54), %.3f (Nu = 8.235)" % (7.54 / (24 * PR ** (1 / 3)), 8.235 / (24 * PR ** (1 / 3))))
for nf, nh in ((10, 2), (10, 3), (10, 5), (10, 10), (5, 3), (3, 2)):
    print("   friction x%d and Nu x%d relative to a tube (T wall): chi = %.3f" % (nf, nh, 3.66 / (16 * PR ** (1 / 3)) * nh / nf))
for Re in (200, 500, 1000, 2000):
    ft = 64.0 / Re
    print("   Re_h = %4d: tube f_D = %.4f ; model f_D at c_f = 1.0, 0.3, 0.1 = %.3f, %.3f, %.3f (x%.1f, x%.1f, x%.1f of tube) ; c_f equivalent to 10 x tube = %.3f" % (
        Re, ft, 133.33 / Re + 2.333, 0.3 * (133.33 / Re + 2.333), 0.1 * (133.33 / Re + 2.333),
        (133.33 / Re + 2.333) / ft, 0.3 * (133.33 / Re + 2.333) / ft, 0.1 * (133.33 / Re + 2.333) / ft, 10 * ft / (133.33 / Re + 2.333)))
