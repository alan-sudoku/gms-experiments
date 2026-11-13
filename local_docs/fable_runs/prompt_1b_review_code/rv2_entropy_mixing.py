"""S5 review, check RV2: exhaust-mixing share of the thermal entropy term (claim B1.2, 36-43 %).

Level: derived (unverified).  numpy + standard library.
  (a) Closed form from the design's R_fa, C and base 1-D resistance (values taken from S2's B16 output
      header lines: R_fa, C, T_hot).  Share = C[(dT/T0) - ln(1 + dT/T0)] / [Q (1/T0 - 1/T_hot)].
      Leading-order approximation share ~ (1/C) / (2 (R_fa + R_base)) printed beside it.
  (b) Same share with the 2-D (height-unmixed) closure of RV1 for the Cu optimum: the exhaust is stratified,
      so mixing to T0 is summed over height strips (it includes the mixing between strips).
  (c) Sensitivity of the share to the operating point: Cu optimum at 0.01-1 W (S2 B05 numbers re-derived
      by RV1's independent code, set S, 1-D).
Run: python3 rv2_entropy_mixing.py > outputs/rv2_entropy_mixing.txt
"""
import math
import numpy as np
import rv1_plate_independent as rv

Q, T0 = 100.0, 298.15
print("RV2 exhaust-mixing share  (level: derived, unverified)")
print("\n=== (a) closed form from B16 header values ===")
cases = [("Cu plate", 0.26794, 4.5117, 325.300), ("Al plate k=150", 0.30437, 4.1653, 329.513),
         ("Al pin k=150", 0.40250, 2.9564, 339.326), ("Gyroid c_f 0.3 chi 0.2", 0.35167, 4.0329, 334.243)]
for nm, R, C, Th in cases:
    dT = Q / C
    Smix = C * (dT / T0 - math.log(1 + dT / T0))
    Sth = Q * (1 / T0 - 1 / Th)
    approx = (1 / C) / (2 * (Th - T0) / Q)
    print("%-24s dT_air=%.2f K  S_mix=%.4e  S_th=%.4e  share=%.4f  (leading order %.4f)" % (nm, dT, Smix, Sth, Smix / Sth, approx))

print("\n=== (b) Cu optimum (38 x 0.3 mm, 0.1 W) with the 2-D height-unmixed closure ===")
t, Nf, k = 0.3e-3, 38, 390.0
V, dP, Re = rv.solve_V(t, Nf, 0.1, "S")
s, Nch = rv.geom(t, Nf)
h = rv.h_S(s, V / (Nch * s * rv.H))
R2, Taout, _ = rv.R_2d(t, Nf, k, V, h)
C = rv.RHO * rv.CP * V
Troot = T0 + Q * R2
Tstrip = T0 + (Troot - T0) * Taout              # outlet temperature per height strip
w = np.full(len(Taout), C / len(Taout))
Smix_strat = float((w * ((Tstrip - T0) / T0 - np.log(Tstrip / T0))).sum())
Tmix = T0 + Q / C
Smix_mean = C * ((Tmix - T0) / T0 - math.log(Tmix / T0))
Thot = Troot + Q * 0.005 / (390 * 0.0036)
Sth = Q * (1 / T0 - 1 / Thot)
print("R_2D=%.5f T_root=%.3f  exhaust strips %.2f..%.2f K  mixing (stratified)=%.4e, (mixed-mean)=%.4e, S_th=%.4e" % (
    R2, Troot, Tstrip.min(), Tstrip.max(), Smix_strat, Smix_mean, Sth))
print("share stratified %.4f ; share if exhaust were pre-mixed %.4f" % (Smix_strat / Sth, Smix_mean / Sth))

print("\n=== (c) Cu optimum share across air power (RV1 set S, 1-D) ===")
for P in (0.01, 0.03, 0.1, 0.3, 1.0):
    b = rv.optimise(390.0, P, "S", "1D", rv.CU_T)
    R, V = b[0], b[4]
    C = rv.RHO * rv.CP * V
    Thot = T0 + Q * (R + 0.005 / (390 * 0.0036))
    sh = C * ((Q / C) / T0 - math.log(1 + Q / C / T0)) / (Q * (1 / T0 - 1 / Thot))
    print("P=%5.2f W: R=%.4f 1/C=%.4f share=%.3f" % (P, R, 1 / C, sh))
