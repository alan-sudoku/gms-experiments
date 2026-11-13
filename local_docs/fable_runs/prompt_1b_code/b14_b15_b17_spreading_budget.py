"""Rows B14, B15, B17.

B14: base spreading resistance (M-SP, Lee et al. 1995 closed form, constants UNSURE) for the
     concentrated source (A_s=4e-4 m2, A_p=3.6e-3 m2), t_b in {5, 10} mm, k set, R0 = the material's
     own plate-fin optimum R_fa at 0.1 W (B05).  Exact-limit checks (i) A_s=A_p, (ii) eps=1e-4, tau=5.
B15: resistance budget for four designs (case U and case S) with R_TIM beside them.
B17: T_hot candidates for the concentrated source (Cu and Al k=150).
Assumptions as in plan 3.2.  Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B14, B15, B17  (level: derived, unverified)")
Ap = W * L
ks = [390, 200, 180, 150, 120, 100]
print_inputs(A_s=A_S, A_p=Ap, t_b=[0.005, 0.010], k=ks, R0="own plate-fin optimum at 0.1 W")
R0 = {k: best(plate_designs(float(k)), 0.1)[0] for k in ks}
head("B14 table")
tab = {}
for tb in (0.005, 0.010):
    print("t_b = %g m" % tb)
    print("  %5s %9s %10s %10s %12s %12s" % ("k", "R0=R_fa", "R_sp,max", "R_sp,avg", "dmax(Al-Cu)", "davg(Al-Cu)"))
    for k in ks:
        rm, ra = sp_area(A_S, Ap, tb, float(k), R0[k])
        tab[(k, tb)] = (rm, ra)
        print("  %5g %9.4f %10.5f %10.5f %12.5f %12.5f" % (k, R0[k], rm, ra, rm - tab[(390, tb)][0], ra - tab[(390, tb)][1]))
rng("Cu R_sp,max (t_b=5 mm)", tab[(390, 0.005)][0], 0.06, 0.10)
rng("Al k=150 R_sp,max (t_b=5 mm)", tab[(150, 0.005)][0], 0.16, 0.24)
rng("penalty Al(150)-Cu R_sp,max (t_b=5 mm)", tab[(150, 0.005)][0] - tab[(390, 0.005)][0], 0.08, 0.16)
rng("Cu R_sp,avg (t_b=5 mm)", tab[(390, 0.005)][1], 0.06, 0.10)
# limits
head("B14 exact limits")
rm, ra = sp_area(Ap, Ap, 0.005, 150.0, 0.3)
ex = 0.005 / (150.0 * Ap)
check("B14 (i) A_s = A_p gives t_b/(k A_p) within 1e-9 (R_sp,max)", abs(rm / ex - 1) < 1e-9, "model %.10e exact %.10e" % (rm, ex))
check("B14 (i) A_s = A_p gives t_b/(k A_p) within 1e-9 (R_sp,avg)", abs(ra / ex - 1) < 1e-9, "model %.10e exact %.10e" % (ra, ex))
issue("B14 (i) is true by construction: at eps=1 the (1-eps) factor removes the Phi term, so the model reduces algebraically to tau/(pi k b_p)")
bp = math.sqrt(Ap / math.pi); a_s = 1e-4 * bp; tb = 5 * bp
for R0t in (0.05, 0.3, 5.0):
    rm, ra = sp_ab(a_s, bp, tb, 150.0, R0t)
    v1 = rm * math.pi * 150.0 * a_s
    v2 = ra * 150.0 * a_s
    check("B14 (ii) eps=1e-4, tau=5, R0=%g: R_sp,max*pi*k*a_s = 1 within 0.5 %%" % R0t, abs(v1 - 1) < 0.005, "value %.6f" % v1)
    check("B14 (ii) R_sp,avg*k*a_s = 0.2702 within 6 %% (R0=%g)" % R0t, abs(v2 / 0.2702 - 1) < 0.06, "value %.6f (%.2f %% from 8/(3 pi^2)=%.6f)" % (v2, (v2 / (8 / (3 * math.pi ** 2)) - 1) * 100, 8 / (3 * math.pi ** 2)))

head("B15 resistance budget at 0.1 W")
designs = [("Cu plate", "Cu plate"), ("Al plate k=150", "Al plate k=150"), ("Al pin k=150 fav", "Al pin k=150 fav"), ("Gyroid ks=150 cf=0.3 chi=0.2", "Gyroid ks=150 cf=0.3 chi=0.2")]
Rtim_U = 50e-6 / (3.0 * Ap)
Rtim_S = 50e-6 / (3.0 * A_S)
print("R_TIM case U = %.5f K/W, case S = %.5f K/W" % (Rtim_U, Rtim_S))
rng("R_TIM U", Rtim_U, 0.0045, 0.0055)
rng("R_TIM S", Rtim_S, 0.040, 0.044)
budget = {}
for nm, key in designs:
    b = best(arch_designs(key), 0.1)
    R, r, d = b
    k = d.k
    Rb1 = TB / (k * W * L)
    rmx, rav = sp_area(A_S, Ap, TB, k, R)
    totU = Rb1 + R
    totS = rmx + R
    budget[nm] = dict(R=R, Rb1=Rb1, rmx=rmx, rav=rav, k=k, r=r, d=d)
    print("%-30s [%s]" % (nm, d.label()))
    print("   case U: base(1D)=%.5f fin side(R_fa)=%.5f total=%.5f (+TIM %.5f = %.5f)  T_max-T_in=%.2f K (with TIM %.2f K)" % (Rb1, R, totU, Rtim_U, totU + Rtim_U, Q * totU, Q * (totU + Rtim_U)))
    print("   case S: base(R_sp,max)=%.5f fin side(R_fa)=%.5f total=%.5f (+TIM %.5f = %.5f)  T_max-T_in=%.2f K (with TIM %.2f K)" % (rmx, R, totS, Rtim_S, totS + Rtim_S, Q * totS, Q * (totS + Rtim_S)))
    for case, tot, rt in (("U", totU, Rtim_U), ("S", totS, Rtim_S)):
        check("B15 %s case %s: T_max - T_in < 100 K (with TIM)" % (nm, case), Q * (tot + rt) < 100, "%.2f K" % (Q * (tot + rt)))

head("B17 T_hot candidates (case S, B14 outputs, t_b = 5 mm)")
for nm in ("Cu plate", "Al plate k=150"):
    bd = budget[nm]
    Tavg = T0 + Q * (bd["R"] + bd["rav"])
    Tmax = T0 + Q * (bd["R"] + bd["rmx"])
    gap = (Tmax - Tavg) ** 2 / Tavg
    err = Q * (1 / Tavg - 1 / Tmax)
    base = Q * (1 / T0 - 1 / Tavg)
    print("%-16s T_avg=%.3f K T_max=%.3f K (T_max-T_avg=%.3f K) gap bound=%.4f K; entropy-term error Q(1/Tavg-1/Tmax)=%.4e W/K, ratio to Q(1/T0-1/Tavg)=%.4f" % (nm, Tavg, Tmax, Tmax - Tavg, gap, err, err / base))
    rng(nm + " T_max-T_avg", Tmax - Tavg, 1, 7)
    rng(nm + " gap bound", gap, 0.0, 0.15)
    rng(nm + " relative error", err / base, 0.03, 0.12)
