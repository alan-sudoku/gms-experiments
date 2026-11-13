"""Row B16: entropy generation by mechanism for four designs (case U, P_air = 0.1 W).

M-ENT (EN1-EN11): midpoint-rule quadrature on 400x400 (fin) and 400 (base) points.
Checks: (i) Q_num = Q within 0.2 %; (ii) S_film + S_fin = C ln(Tout/Tin) - Q/T_root within 0.5 %;
(iii) S_mix within 10 % of Q dT/(2 T0^2) for dT < 30 K.  (iv) algebraic closures printed, not counted.
Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B16  (level: derived, unverified)")
print_inputs(P_air=0.1, eta_fan=ETA_FAN, T0=T0, grid="400x400 fin, 400 base", case="U (uniform source)")
names = ["Cu plate", "Al plate k=150", "Al pin k=150 fav", "Gyroid ks=150 cf=0.3 chi=0.2"]
ent = {}
for n in names:
    R, r, d = best(arch_designs(n), 0.1)
    e = entropy(r, 0.1, ETA_FAN)
    ent[n] = (r, e)
    head(n + "  [" + d.label() + "]")
    print("  R_fa=%.5f T_root=%.3f T_out=%.3f T_hot=%.3f NTU=%.4f C=%.4f m=%.3f h=%.2f" % (R, r["T_root"], r["T_out"], e["Thot"], r["NTU"], r["C"], r["m"], r["h"]))
    items = [("S_base", e["Sbase"]), ("S_fin", e["Sfin"]), ("S_film", e["Sfilm"]), ("S_mix", e["Smix"]), ("S_pump", e["Spump"]), ("S_fanloss", e["Sfanloss"])]
    tot = sum(v for _, v in items)
    for nm, v in items:
        print("  %-10s %.5e W/K  share of S_th %.4f  share of total %.4f" % (nm, v, v / e["Sth"], v / tot))
    print("  S_th=%.5e  S_dev=%.5e  (S_th+S_dev = %.6e vs Q/T0 = %.6e : identity)" % (e["Sth"], e["Sdev"], e["Sth"] + e["Sdev"], Q / T0))
    print("  sum(base+fin+film+mix) = %.6e vs S_th = %.6e (algebraic consequence of (ii); printed, not counted)" % (e["Sbase"] + e["Sfin"] + e["Sfilm"] + e["Smix"], e["Sth"]))
    print("  Prompt expression E(Tc)=Q(1/Tc-1/T_hot)+P_air/T0:  Tc=T0: %.5e   Tc=mean: %.5e   Tc=T_lm: %.5e   (T_lm=%.3f K)" % (e["E"]["T0"], e["E"]["Tmean"], e["E"]["Tlm"], e["Tlm"]))
    print("  E(T0)-E(T_lm) = %.5e vs S_mix = %.5e (identity: both equal Q(1/T0-1/T_lm); not counted)" % (e["E"]["T0"] - e["E"]["Tlm"], e["Smix"]))
    print("  E(T_lm) vs S_th + S_pump: %.5e vs %.5e; mean-temperature reading differs from T_lm reading by %.2f %%" % (e["E"]["Tlm"], e["Sth"] - e["Smix"] + e["Spump"], (e["E"]["Tmean"] / e["E"]["Tlm"] - 1) * 100))
    check(n + " (i) Q_num = Q within 0.2 %", abs(e["Qnum"] / Q - 1) < 0.002, "Q_num=%.5f, rel diff %.3e" % (e["Qnum"], e["Qnum"] / Q - 1))
    lhs = e["Sfilm"] + e["Sfin"]
    check(n + " (ii) S_film+S_fin = C ln(Tout/Tin) - Q/T_root within 0.5 %", abs(lhs / e["stream"] - 1) < 0.005, "quadrature %.6e, stream %.6e, rel diff %.3e" % (lhs, e["stream"], lhs / e["stream"] - 1))
    ser = Q * r["dT"] / (2 * T0 ** 2)
    if r["dT"] < 30:
        check(n + " (iii) S_mix within 10 %% of Q dT/(2 T0^2) (dT=%.2f K)" % r["dT"], abs(e["Smix"] / ser - 1) < 0.10, "S_mix=%.5e, series %.5e, rel diff %.3e" % (e["Smix"], ser, e["Smix"] / ser - 1))
    else:
        info(n + " (iii) skipped, dT>=30 K")
r, e = ent["Cu plate"]
head("Hand ranges, Cu design")
rng("S_th", e["Sth"], 0.026, 0.031)
rng("S_mix share of S_th", e["Smix"] / e["Sth"], 0.25, 0.45)
rng("S_pump x1e4", e["Spump"] * 1e4, 3.3, 3.5)
rng("S_pump share of S_th", e["Spump"] / e["Sth"], 0.005, 0.015)
rng("S_pump+S_fanloss x1e3", (e["Spump"] + e["Sfanloss"]) * 1e3, 1.25, 1.35)
rng("(S_pump+S_fanloss)/S_th", (e["Spump"] + e["Sfanloss"]) / e["Sth"], 0.03, 0.07)
ok = e["E"]["Tlm"] < e["E"]["T0"]
print(("PASS  " if ok else "FAIL  ") + "E(T_lm) below E(T0) by the mixing share: %.5e vs %.5e (diff %.5e = S_mix %.5e)" % (e["E"]["Tlm"], e["E"]["T0"], e["E"]["T0"] - e["E"]["Tlm"], e["Smix"]))
issue("B16 'E(T_lm) below E(T0) by the mixing share' is an identity (difference = Q(1/T0-1/T_lm) = S_mix by algebra); the PASS line is not independent evidence")
issue("B16 note: all four designs use the uniform case U with T_hot = T_root + Q R_base,1D, whereas B17 uses case S; the two cases are not mixed in any one number")
