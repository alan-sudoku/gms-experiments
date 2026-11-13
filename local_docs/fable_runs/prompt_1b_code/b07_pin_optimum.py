"""Row B07: optimised Al (and Cu reference) pin fins for each k and P_air.

M-PIN exhaustive search over d in {1,1.5,2,3} mm, p in {1.5,1.75,2,2.5,3}, minimising R_fa.
Favourable combination = Nu version K with, at each flow rate, the friction version giving the
lower dP (equivalent to the higher V at fixed P_air).  The four pure combinations
(Nu K/Z x friction K/J) are also optimised.  Designs flagged (Re_d outside 40-1000 or N_L<10)
are kept in the search and marked; the best unflagged design is printed as well.
Comparison with the B05 plate-fin optima at the same k and P_air.  Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B07  (level: derived, unverified)")
ks = [390, 200, 180, 150, 120, 100]
print_inputs(k=ks, P_air=P_SET, d_mm=[x * 1e3 for x in PIN_D], p=PIN_P)
combos = [("fav(NuK,min fric)", "min", "K"), ("NuK,fK", "K", "K"), ("NuK,fJ", "J", "K"), ("NuZ,fK", "K", "Z"), ("NuZ,fJ", "J", "Z")]
fav = {}
for P in P_SET:
    head("P_air = %g W" % P)
    cu_plate = best(plate_designs(390.0), P)[0]
    for k in ks:
        al_plate = best(plate_designs(float(k)), P)[0]
        res = {}
        for name, fr, nu in combos:
            res[name] = best(pin_designs(float(k), fr, nu), P)
        w = print_top3("k=%g favourable" % k, pin_designs(float(k), "min", "K"), P, "PIN")
        fav[(k, P)] = w
        R, r, d = w
        bn = boundary_notes(d, "PIN")
        if bn:
            issue("B07 boundary optimum (favourable) k=%g P=%g W: %s (%s)" % (k, P, "; ".join(bn), d.label()))
        if r["flags"]:
            issue("B07 favourable winner flagged k=%g P=%g W: %s (%s)" % (k, P, r["flags"], d.label()))
            ru = [x for x in ranked(pin_designs(float(k), "min", "K"), P) if not x[1]["flags"]]
            if ru:
                print("   best unflagged: R_fa=%.4f %s" % (ru[0][0], ru[0][2].label()))
        print("   ratio to Cu plate-fin optimum = %.3f ; to Al plate-fin optimum (same k) = %.3f" % (R / cu_plate, R / al_plate))
        print("   other combinations (winner each):")
        Rs = []
        for name, fr, nu in combos:
            b = res[name]
            Rs.append(b[0])
            print("     %-18s R_fa=%.4f Re_d=%.0f dP=%.2f V=%.3e %s %s" % (name, b[0], b[1]["Re"], b[1]["dP"], b[1]["V"], b[2].label().split(" k=")[0], b[1]["flags"]))
        spread = max(Rs[1:]) / min(Rs[1:])
        print("   spread over the four pure combinations (max/min R_fa) = %.3f" % spread)
        if spread > 1.5:
            issue("B07 correlation combinations disagree by factor %.2f (>1.5) at k=%g P=%g W" % (spread, k, P))
head("Summary of favourable R_fa (rows k, columns P_air)")
print("%5s " % "k" + "".join("%12g" % P for P in P_SET))
for k in ks:
    print("%5g " % k + "".join("%12.4f" % fav[(k, P)][0] for P in P_SET))
w = fav[(150, 0.1)]
rng("R_fa k=150 favourable 0.1 W", w[0], 0.33, 0.50)
rng("ratio to Cu plate-fin, k=150, 0.1 W", w[0] / best(plate_designs(390.0), 0.1)[0], 1.2, 1.8)
