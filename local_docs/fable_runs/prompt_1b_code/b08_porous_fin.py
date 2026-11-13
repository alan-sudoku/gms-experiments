"""Row B08: porous-fin (homogenised) code path reproduces the plate-fin result.

Feeds GY6 and X1 with plate inputs from B03: a_sf = 2 N_ch/W, phi = N_ch s/W,
k_eff = k N_f t/W, h and V from B03 (GY3-GY5 bypassed).  Compares eta_f (2 %) and R_fa (3 %).
Assumption: A_wet = a_sf*W*L*H, base term phi*W*L, as in GY6.  Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B08  (level: derived, unverified)")
d = PF(0.4e-3, 32, K_CU)
V = V_at_P(d, 0.1)
r = d.eval(V)
print_inputs(t=0.4e-3, N_f=32, k=K_CU, V=V, h=r["h"])
asf = 2 * d.Nch / W
phi = d.Nch * d.s / W
keff = K_CU * d.Nf * d.t / W
m = math.sqrt(r["h"] * asf / keff)
eta = math.tanh(m * H) / (m * H)
Awet = asf * W * L * H
G = r["h"] * (eta * Awet + phi * W * L)
c = close_thermal(G, V, K_CU)
print("a_sf=%.3f 1/m, phi=%.5f, k_eff=%.3f W/m/K, m=%.4f (plate m=%.4f), eta=%.5f (plate %.5f)" % (asf, phi, keff, m, r["m"], eta, r["eta"]))
print("R_fa porous=%.6f  R_fa plate=%.6f  NTU %.5f vs %.5f" % (c["R_fa"], r["R_fa"], c["NTU"], r["NTU"]))
check("B08 eta within 2 %", abs(eta / r["eta"] - 1) < 0.02, "rel diff %.4e" % (eta / r["eta"] - 1))
check("B08 R_fa within 3 %", abs(c["R_fa"] / r["R_fa"] - 1) < 0.03, "rel diff %.4e" % (c["R_fa"] / r["R_fa"] - 1))
info("m ratio", "m_porous/m_plate = %.6f, sqrt(31/32) = %.6f" % (m / r["m"], math.sqrt(31 / 32)))
issue("B08 is a low-power check: the porous inputs are algebraic rearrangements of the plate inputs, so m differs only by sqrt(N_ch/N_f); the area terms are identical. It tests the GY6/X1 wiring, not the gyroid physics (spec states this). Also, the check re-implements GY6/X1 inline from the spec rather than calling GY.eval (which cannot take bypassed inputs), so the GY.eval class used in B09-B13 is not itself exercised by B08.")
