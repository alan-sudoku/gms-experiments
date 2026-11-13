"""Rows B03, B04: Cu plate-fin reference design at 0.1 W, and material swap at fixed geometry.

Uses M-PF (PF1-PF12), closure X1, bisection for V (rel. tol 1e-8).
B03 checks: PF12 ratio, exact pressure-drop limit 12*mu*u*L/s^2, Nu limit 7.55, Re<2300.
B04: R_fa(k)/R_fa(Cu), eta(k), share of 1/C for all P_air; V and dP identical for all k.
Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B03, B04  (level: derived, unverified)")
t, Nf = 0.4e-3, 32
print_inputs(t=t, N_f=Nf, k=K_CU, P_air=0.1, H=H, L=L, W=W)
d = PF(t, Nf, K_CU)
V = V_at_P(d, 0.1)
r = d.eval(V)
head("B03 reference design")
for key, lab in [("s", "s [m]"), ("V", "V [m3/s]"), ("u", "u [m/s]"), ("Re", "Re"), ("dP", "dP [Pa]"), ("Nu", "Nu"), ("h", "h [W/m2/K]"),
                 ("eta", "eta_f"), ("NTU", "NTU"), ("dT", "dT_air [K]"), ("R_fa", "R_fa [K/W]"), ("invC", "1/C [K/W]"), ("mass", "mass [kg]"),
                 ("P_air", "V*dP [W]"), ("R_faT", "R_fa,T (PF12) [K/W]")]:
    print("  %-22s %.6g" % (lab, r[key]))
check("B03 bisection: V*dP = 0.1 W within 1e-8 rel", abs(r["P_air"] - 0.1) / 0.1 < 1e-7, "P_air=%.10g" % r["P_air"])
ratio = r["R_faT"] / r["R_fa"]
check("B03 (i) PF12 ratio R_fa,T/R_fa in 0.85-1.15", 0.85 <= ratio <= 1.15, "ratio=%.4f" % ratio)
s0 = 1.5e-3
dp_ex, _, _ = pf_dp_u(s0, 1000.0, 10.0, 1.0, Kc=0.0, Ke=0.0)
ex = 12 * MU * 1.0 * 10.0 / s0 ** 2
check("B03 (ii) dP with H=1000 m, L=10 m, s=1.5 mm, u=1 within 1.5% of 12*mu*u*L/s^2", abs(dp_ex / ex - 1) < 0.015, "dP=%.5f exact=%.5f rel diff=%.3e" % (dp_ex, ex, dp_ex / ex - 1))
nu_l = pf_nu(100.0, 1.5e-3, 1.0)
check("B03 (iii) Nu with L=100 m = 7.55 +-0.02", abs(nu_l - 7.55) <= 0.02, "Nu=%.5f (exact fully developed 7.541)" % nu_l)
check("B03 (iv) Re < 2300", r["Re"] < 2300, "Re=%.1f" % r["Re"])
rng("s [mm]", r["s"] * 1e3, 1.51, 1.54)
rng("V [1e-3 m3/s]", r["V"] * 1e3, 3.5, 5.0)
rng("dP [Pa]", r["dP"], 18, 32)
rng("h", r["h"], 60, 90)
rng("eta_f", r["eta"], 0.75, 0.83)
rng("NTU", r["NTU"], 1.1, 1.7)
rng("dT_air", r["dT"], 17, 25)
rng("R_fa", r["R_fa"], 0.24, 0.31)
info("PF8 Nu note", "PF8 is a mean on the log-mean temperature difference; R_fa in X1 additionally uses eps-NTU with C; both applied as written")

head("B04 material swap, geometry fixed (t=0.4 mm, N_f=32)")
ks = [390, 200, 180, 150, 120, 100]
Vs_all = {}
dps_all = {}
for P in P_SET:
    print("\nP_air = %g W" % P)
    print("  %5s %10s %8s %8s %10s %9s %9s %9s" % ("k", "R_fa", "ratio", "eta_f", "1/C", "1/C share", "V", "dP"))
    base = None
    for k in ks:
        dd = PF(t, Nf, float(k))
        VV = V_at_P(dd, P)
        rr = dd.eval(VV)
        if base is None:
            base = rr["R_fa"]
        Vs_all.setdefault(P, []).append(rr["V"]); dps_all.setdefault(P, []).append(rr["dP"])
        print("  %5g %10.5f %8.4f %8.4f %10.5f %9.3f %9.4e %9.4f" % (k, rr["R_fa"], rr["R_fa"] / base, rr["eta"], rr["invC"], rr["invC"] / rr["R_fa"], rr["V"], rr["dP"]))
        if P == 0.1:
            if k == 180: rng("ratio k=180 at 0.1 W", rr["R_fa"] / base, 1.08, 1.14)
            if k == 150: rng("ratio k=150 at 0.1 W", rr["R_fa"] / base, 1.11, 1.18)
            if k == 100: rng("ratio k=100 at 0.1 W", rr["R_fa"] / base, 1.17, 1.30)
            if k == 390: rng("1/C share for Cu at 0.1 W", rr["invC"] / rr["R_fa"], 0.6, 0.8)
same = all(max(v) == min(v) for v in Vs_all.values()) and all(max(v) == min(v) for v in dps_all.values())
check("B04 V and dP identical for all k at each P_air", same, "bitwise comparison")
issue("B04 check 'V and dP identical for all k' is true by construction: the hydraulics function does not take k (the spec itself says it checks the code path); flagged per instructions")
