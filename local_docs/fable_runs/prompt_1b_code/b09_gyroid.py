"""Row B09: gyroid sweep and minimum analogy factor chi_min.

M-GYR exhaustive search over a, rho_bar (t_s >= 0.3 mm enforced) for each (c_f, chi, k_s, P_air);
winner and two runners-up printed.  chi_min(c_f, k_s, P_air): smallest chi in [0.01, 1.0] for which
the best gyroid R_fa equals (1) the Cu plate-fin optimum of B05, (2) the Al plate-fin optimum at the
same k (bisection, tolerance 1e-4 in chi).  If R_fa(chi=1) > target: 'caloric-limited, no match'
with min(1/C).  Also chi_pin from the pin bank (p=2, Re_d=300).  Gyroid Re_h has no stated limit in
the spec; it is reported, not used for exclusion.  Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B09  (level: derived, unverified)")
CFS = [1.0, 0.3, 0.1]
CHIS = [0.05, 0.10, 0.20, 0.35]
KS = [100, 150, 180]
print_inputs(a_mm=[x * 1e3 for x in GY_A], rho_bar=GY_RHO, c_f=CFS, chi=CHIS, k_s=KS, P_air=P_SET, ts_min_mm=0.3)


def gbest(k, cf, chi, P):
    return best(gy_designs(float(k), cf, chi), P)


head("Winners (full table; winner + two runners-up for each search)")
tab = {}
for P in P_SET:
    for k in KS:
        for cf in CFS:
            for chi in CHIS:
                rk = ranked(gy_designs(float(k), cf, chi), P)
                tab[(cf, chi, k, P)] = rk[0]
                print("P=%g k_s=%g c_f=%g chi=%g:" % (P, k, cf, chi))
                for i, (R, r, d) in enumerate(rk[:3]):
                    print("    %s R_fa=%.4f 1/C=%.4f V=%.3e dP=%.3f Re_h=%.1f h=%.1f eta=%.3f NTU=%.3f t_s=%.3f mm mass=%.4f %s %s" % (
                        ("WIN", "ru2", "ru3")[i], R, r["invC"], r["V"], r["dP"], r["Re"], r["h"], r["eta"], r["NTU"], d.ts * 1e3, r["mass"],
                        "a=%.0fmm rho=%.2f" % (d.a * 1e3, d.rb), r["flags"]))
                bn = boundary_notes(rk[0][2], "GY")
                print("    winner boundary: " + ("; ".join(bn) if bn else "interior") + ("   [WINNER FLAG: %s]" % rk[0][1]["flags"] if rk[0][1]["flags"] else ""))
                if rk[0][1]["flags"]:
                    ru = [x for x in rk if not x[1]["flags"]]
                    if ru:
                        print("    best unflagged: R_fa=%.4f a=%.0fmm rho=%.2f" % (ru[0][0], ru[0][2].a * 1e3, ru[0][2].rb))

nb = sum(1 for v in tab.values() if boundary_notes(v[2], "GY"))
nf = sum(1 for v in tab.values() if v[1]["flags"])
print("\nSummary: %d of %d winners sit on a sweep boundary (a or rho_bar edge); %d of %d winners are flagged 'homogenisation doubtful'" % (nb, len(tab), nf, len(tab)))
issue("B09 %d of %d gyroid winners lie on a sweep boundary (a or rho_bar edge) and %d of %d winners have H/a<3 (homogenisation doubtful); the sweep does not bracket the optimum" % (nb, len(tab), nf, len(tab)))
# monotonicity of R_fa in chi (spec asserts it)
head("Monotonicity of best R_fa in chi (fine grid, spec assumes monotone falling)")
bad = 0
for P in P_SET:
    for k in KS:
        for cf in CFS:
            prev = None
            for i in range(0, 100):
                chi = 0.01 + i * 0.01
                R = gbest(k, cf, chi, P)[0]
                if prev is not None and R > prev + 1e-12:
                    bad += 1
                    issue("B09 non-monotone R_fa in chi at P=%g k=%g c_f=%g chi=%.2f (R %.5f > prev %.5f)" % (P, k, cf, chi, R, prev))
                prev = R
print("non-monotone steps found: %d" % bad)

head("chi_min")
chimin = {}
for P in P_SET:
    cu_t = best(plate_designs(390.0), P)[0]
    for k in KS:
        al_t = best(plate_designs(float(k)), P)[0]
        for cf in CFS:
            for nm, tgt in (("Cu-plate-opt", cu_t), ("Al-plate-opt(k)", al_t)):
                f = lambda chi: gbest(k, cf, chi, P)[0]
                R1 = f(1.0)
                if R1 > tgt:
                    mi = min(gbest(k, cf, 1.0, P)[1]["invC"] for _ in [0])
                    out = "caloric-limited, no match (R_fa(chi=1)=%.4f > target %.4f; min 1/C at chi=1: %.4f)" % (R1, tgt, mi)
                    chimin[(cf, k, P, nm)] = None
                elif f(0.01) <= tgt:
                    out = "chi_min <= 0.01 (R_fa(0.01)=%.4f <= target %.4f)" % (f(0.01), tgt)
                    chimin[(cf, k, P, nm)] = 0.01
                else:
                    lo, hi = 0.01, 1.0
                    while hi - lo > 1e-4:
                        mid = 0.5 * (lo + hi)
                        if f(mid) > tgt:
                            lo = mid
                        else:
                            hi = mid
                    out = "chi_min = %.4f (target %.4f, R_fa at chi_min = %.4f)" % (hi, tgt, f(hi))
                    chimin[(cf, k, P, nm)] = hi
                print("P=%g k_s=%g c_f=%g target %s: %s" % (P, k, cf, nm, out))

head("Hand expectation comparison")
for P in P_SET:
    vals = chimin[(1.0, 150, P, "Cu-plate-opt")]
    if P <= 0.3:
        ok = vals is None
        print(("RANGE-OK    " if ok else "RANGE-MISS  ") + "c_f=1.0, k_s=150, P=%g: no match at any chi expected; got %s" % (P, vals))
        if not ok:
            issue("B09 hand expectation 'c_f=1.0 gives no match for P<=0.3 W' fails at P=%g (Cu target): chi_min=%s" % (P, vals))
for cf in (0.3, 0.1):
    v = chimin[(cf, 150, 0.1, "Cu-plate-opt")]
    ok = v is not None and 0.2 <= v <= 0.6
    print(("RANGE-OK    " if ok else "RANGE-MISS  ") + "c_f=%g, k_s=150, P=0.1 W, Cu target: chi_min=%s, hand 0.2-0.6" % (cf, v))
    if not ok:
        issue("B09 hand range chi_min 0.2-0.6 missed: c_f=%g k_s=150 P=0.1 W Cu target: %s" % (cf, v))

head("chi_pin (pin bank equivalent analogy factor), p = 2, Re_d = 300")
pin = PIN(2e-3, 2.0, 150.0)
Re = 300.0
chi_pin = (pin.Nu_K(Re) / (Re * PR ** (1 / 3))) / (pin.f_K(Re) * (pin.ST - pin.d) / (math.pi * pin.d))
print("chi_pin = %.4f (Nu_K=%.3f, f_K=%.4f)" % (chi_pin, pin.Nu_K(Re), pin.f_K(Re)))
rng("chi_pin", chi_pin, 0.1, 0.3)
