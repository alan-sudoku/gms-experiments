"""D5, D7: critical scale thickness for spallation, and time for an oxide notch to
reach the crack threshold.

Spec rows: D5 (delta_c = Gc (1-nu)/(E eps^2), t_sp = delta_c^2/(2 kp')) and
D7 (a_tr = (1/pi) (dK_th/(Y dsigma))^2, t_i = a_tr^2/(2 kp')).
Claim level: derived (unverified).  All inputs are MEMORY (M15, M17, M18, M20, M31)
or planner-chosen parametric grids; none is looked up.

Assumptions: eps = d_alpha*dT + eps_mech with d_alpha = 7e-6 /K (M18), E_ox = 380 GPa,
nu_ox = 0.25 (M17); Y = 1.12 for D7 (spec, M15); dK_th = 5 MPa sqrt(m) (M31).
Pure arithmetic rows: the planner's hand values are the only comparison, so the
"checks" below compare the formula with hand arithmetic of the same formula
(flagged as such).  numpy only.
"""
import math
import numpy as np

E_OX, NU_OX, D_ALPHA = 380e9, 0.25, 7e-6
GC = [1.0, 5.0, 20.0, 100.0]               # J/m^2 (M20)
DTS = [200.0, 500.0, 1000.0]               # K
EMECH = [0.0, 1.5e-3]
KPS = [1e-18, 1e-17, 1e-16]                # m^2/s (parametric)


def delta_c(gc, dT, em):
    eps = D_ALPHA * dT + em
    return gc * (1 - NU_OX) / (E_OX * eps ** 2)


print("=" * 70)
print("D5: critical scale thickness delta_c [um] and time to reach it  (level: derived)")
print("=" * 70)
for em in EMECH:
    print(f"\neps_mech = {em:g}")
    print(f"{'Gc J/m2':>8} " + " ".join(f"dT={d:>5g}K" for d in DTS))
    for g in GC:
        print(f"{g:8g} " + " ".join(f"{delta_c(g, d, em)*1e6:10.4f}" for d in DTS))
print("\nt_sp = delta_c^2/(2 kp') [h], eps_mech = 0 (rows: Gc, dT; columns: kp')")
print(f"{'Gc':>6} {'dT':>6} " + " ".join(f"kp'={k:.0e}" for k in KPS))
for g in GC:
    for d in DTS:
        dc = delta_c(g, d, 0.0)
        print(f"{g:6g} {d:6g} " + " ".join(f"{dc**2/(2*k)/3600:11.4g}" for k in KPS))
hand = [(5, 1000, 0.0, 0.20), (5, 500, 0.0, 0.81), (100, 500, 0.0, 16.0)]
print("\nHand values (tolerance 2 %):")
for g, d, em, h in hand:
    v = delta_c(g, d, em) * 1e6
    print(f"  Gc = {g}, dT = {d}, eps_mech = {em}: {v:.4f} um vs hand {h} -> rel dev {abs(v/h-1):.2%} "
          f"{'PASS' if abs(v/h-1) <= 0.02 else 'FAIL'}")
print("  (hand values restate the same formula: IDENTITY-class check, arithmetic only)")
allv = np.array([delta_c(g, d, em) * 1e6 for g in GC for d in DTS for em in EMECH])
inside = np.sum((allv >= 1) & (allv <= 10))
print(f"\nPlausibility (1 to 10 um for alumina scales, UNSURE): {inside} of {allv.size} grid cases lie in "
      f"[1, 10] um; range of grid {allv.min():.3g} to {allv.max():.3g} um. Plausibility only, not a test.")

print()
print("=" * 70)
print("D7: oxide notch reaching the crack threshold  (level: derived)")
print("=" * 70)
DK, Y = 5e6, 1.12
DS = [200e6, 400e6, 800e6]
print(f"dK_th = 5 MPa sqrt(m), Y = {Y}")
print(f"{'dsigma MPa':>10} {'a_tr um':>10} " + " ".join(f"t_i(kp'={k:.0e}) [s]" for k in KPS))
for ds in DS:
    a = (DK / (Y * ds)) ** 2 / math.pi
    print(f"{ds/1e6:10g} {a*1e6:10.3f} " + " ".join(f"{a**2/(2*k):18.4e}" for k in KPS))
a = (DK / (Y * 400e6)) ** 2 / math.pi
ti = a ** 2 / (2 * 1e-16)
print(f"\nhand check dsigma = 400 MPa, kp' = 1e-16: a_tr = {a*1e6:.2f} um (hand 39.7), "
      f"t_i = {ti:.3e} s = {ti/86400:.1f} d (hand 7.9e6 s, 91 d): "
      f"{'PASS' if abs(a*1e6/39.7-1) <= 0.02 and abs(ti/7.9e6-1) <= 0.02 else 'FAIL'} (tolerance 2 %)")
tis = [((DK / (Y * ds)) ** 2 / math.pi) ** 2 / (2 * 1e-16) for ds in DS]
slope = np.polyfit(np.log(DS), np.log(tis), 1)[0]
print(f"log-log slope of t_i versus dsigma = {slope:.6f} (expect -4). IDENTITY check: follows from "
      "the formula by algebra (a_tr ~ dsigma^-2, t_i ~ a_tr^2), not an independent test.")
