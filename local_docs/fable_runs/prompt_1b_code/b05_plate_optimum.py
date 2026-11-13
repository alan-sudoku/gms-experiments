"""Row B05: optimised plate fin for each material and each P_air.

Exhaustive search over the M-PF sweep sets (Cu: t 0.3-1.0 mm; Al: t 0.4-2.0 mm;
N_f from 6 while s >= 0.8 mm), minimising R_fa; designs with Re >= 2300 excluded.
Checks: (i) s/s_BS with s_BS = 2.7 L Be^(-1/4), Be = dP L^2/(mu alpha) at the optimum's dP;
(ii) sweep-boundary report; (iii) PF12 ratio at each optimum; hand ranges at 0.1 W.
Winner and two runners-up printed per search.  Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B05  (level: derived, unverified)")
ks = [390, 200, 180, 150, 120, 100]
print_inputs(k=ks, P_air=P_SET, Cu_t=[x * 1e3 for x in CU_T], Al_t=[x * 1e3 for x in AL_T], s_min_mm=0.8, Re_limit=2300)
opt = {}
for P in P_SET:
    head("P_air = %g W" % P)
    for k in ks:
        w = print_top3("k=%g" % k, plate_designs(float(k)), P, "PF")
        opt[(k, P)] = w
        R, r, d = w
        Be = r["dP"] * L ** 2 / (MU * ALPHA_A)
        sbs = 2.7 * L * Be ** -0.25
        ratio = r["s"] / sbs
        ok1 = 0.6 <= ratio <= 1.6
        ok3 = 0.85 <= r["R_faT"] / R <= 1.15
        print("   s=%.3f mm, s_BS=%.3f mm, s/s_BS=%.3f (%s);  PF12 R_fa,T/R_fa=%.3f (%s)" % (
            r["s"] * 1e3, sbs * 1e3, ratio, "in 0.6-1.6" if ok1 else "OUT of 0.6-1.6", r["R_faT"] / R, "in 0.85-1.15" if ok3 else "OUT"))
        if not ok1:
            issue("B05 (i) s/s_BS=%.3f outside 0.6-1.6 at k=%g, P=%g W" % (ratio, k, P))
        if not ok3:
            issue("B05 (iii) PF12 ratio %.3f outside 0.85-1.15 at k=%g, P=%g W" % (r["R_faT"] / R, k, P))
        bn = boundary_notes(d, "PF")
        if bn:
            issue("B05 (ii) boundary optimum k=%g P=%g W: %s (%s)" % (k, P, "; ".join(bn), d.label()))
head("Summary: ratio to Cu optimum")
print("%5s " % "k" + "".join("%12g" % P for P in P_SET))
for k in ks:
    print("%5g " % k + "".join("%12.4f" % (opt[(k, P)][0] / opt[(390, P)][0]) for P in P_SET))
print("Cu R_fa  " + "".join("%12.4f" % opt[(390, P)][0] for P in P_SET))
rng("Cu R_fa at 0.1 W", opt[(390, 0.1)][0], 0.24, 0.30)
rng("Al k=150 / Cu at 0.1 W", opt[(150, 0.1)][0] / opt[(390, 0.1)][0], 1.05, 1.25)
rng("Al k=200 / Cu at 0.1 W", opt[(200, 0.1)][0] / opt[(390, 0.1)][0], 1.03, 1.15)
# any Re-excluded winners?
for (k, P), (R, r, d) in opt.items():
    if r["Re"] > 1800:
        info("high Re winner", "k=%g P=%g Re=%.0f" % (k, P, r["Re"]))
