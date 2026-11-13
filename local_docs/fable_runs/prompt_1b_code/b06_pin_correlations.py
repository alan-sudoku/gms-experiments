"""Row B06: pin-fin correlations at reference points (f_K, f_J, Nu_K, Nu_Z).

Evaluates PN3, PN4, PN6, PN7 directly with S_L = S_T for p in {1.5,2,2.5,3},
Re_d in {100,300,500,1000}; cross-method ratios; reports where f_K rises with p
(also on a finer p grid 1.25-4.0, extra scan beyond the spec).
Assumption: d only enters through the class constructor; correlations depend on p and Re_d.
Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B06  (level: derived, unverified)")
ps = [1.5, 2.0, 2.5, 3.0]
Res = [100, 300, 500, 1000]
print_inputs(p=ps, Re_d=Res, Pr=PR, S_L="S_T")
d0 = 2e-3


def vals(p, Re):
    pin = PIN(d0, p, 150.0)
    return pin.f_K(Re), pin.f_J(Re), pin.Nu_K(Re), pin.Nu_Z(Re)


print("%5s %7s %9s %9s %9s %9s %9s %9s" % ("p", "Re_d", "f_K", "f_J", "Nu_K", "Nu_Z", "fK/fJ", "NuZ/NuK"))
for p in ps:
    for Re in Res:
        fK, fJ, nK, nZ = vals(p, Re)
        print("%5.2f %7g %9.4f %9.4f %9.3f %9.3f %9.3f %9.3f" % (p, Re, fK, fJ, nK, nZ, fK / fJ, nZ / nK))
        if not (0.65 <= fK / fJ <= 1.6):
            issue("B06 f_K/f_J=%.3f outside 0.65-1.6 at p=%g Re_d=%g" % (fK / fJ, p, Re))
        if not (0.55 <= nZ / nK <= 1.05):
            issue("B06 Nu_Z/Nu_K=%.3f outside 0.55-1.05 at p=%g Re_d=%g" % (nZ / nK, p, Re))
head("Outside range: loss coefficient per row 0.3-1.2 for p = 1.5-2.5, Re_d 300-1000")
for p in [1.5, 2.0, 2.5]:
    for Re in [300, 500, 1000]:
        fK, fJ, _, _ = vals(p, Re)
        for nm, f in (("f_K", fK), ("f_J", fJ)):
            ok = 0.3 <= f <= 1.2
            print(("RANGE-OK    " if ok else "RANGE-MISS  ") + "%s p=%g Re_d=%g: %.4f" % (nm, p, Re, f))
            if not ok:
                issue("B06 %s=%.4f outside 0.3-1.2 at p=%g Re_d=%g" % (nm, f, p, Re))
head("Hand values at p = 2, Re_d = 500")
fK, fJ, nK, nZ = vals(2.0, 500)
for nm, v, h, tol in (("f_K", fK, 0.70, 0.1), ("f_J", fJ, 0.54, 0.1), ("Nu_K", nK, 17.4, 0.1), ("Nu_Z", nZ, 14.0, 0.1)):
    ok = abs(v / h - 1) <= tol
    print(("RANGE-OK    " if ok else "RANGE-MISS  ") + "%s = %.4f hand ~%.2f (+-%d%% reading of '~')" % (nm, v, h, tol * 100))
    if not ok:
        issue("B06 hand value %s=%.4f vs ~%.2f at p=2, Re_d=500 (tolerance of '~' taken as 10%%, my reading)" % (nm, v, h))
head("Does f_K rise with p?  (spec grid, then fine scan)")
for Re in Res:
    seq = [vals(p, Re)[0] for p in ps]
    rises = [(ps[i], ps[i + 1]) for i in range(len(ps) - 1) if seq[i + 1] > seq[i]]
    print("Re_d=%5g f_K(p)=" % Re + ", ".join("%.4f" % x for x in seq) + ("   RISES between p pairs %s" % rises if rises else "   monotone falling"))
    if rises:
        issue("B06 f_K rises with p at Re_d=%g between %s (values %s); physically f should fall as pitch opens" % (Re, rises, ["%.3f" % x for x in seq]))
fine = [1.25 + 0.25 * i for i in range(12)]
print("fine scan p:", fine)
for Re in Res:
    seq = [vals(p, Re)[0] for p in fine]
    rises = [(fine[i], fine[i + 1]) for i in range(len(fine) - 1) if seq[i + 1] > seq[i]]
    print("Re_d=%5g f_K=" % Re + ", ".join("%.3f" % x for x in seq))
    print("      f_J=" + ", ".join("%.3f" % vals(p, Re)[1] for p in fine))
    if rises:
        issue("B06 fine scan: f_K rises with p at Re_d=%g for pairs %s" % (Re, rises))
