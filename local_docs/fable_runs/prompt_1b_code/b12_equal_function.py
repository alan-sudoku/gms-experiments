"""Row B12: equal function.  Fan power each Al architecture needs to reach the Cu plate-fin
optimum's R_fa at 0.1 W, with the design re-optimised at every P_air.

Bisection on ln P_air in [ln 0.01, ln 30] (tolerance 1e-3 in ln P, i.e. 0.1 % in P).
dW_elec = (P_req - 0.1)/eta_fan; dS = dW_elec/T0; dE = dW_elec*tau_life.
Second estimate: P_req ~ 0.1*(R_Al/R_Cu)^(-1/n) with the architecture's own n (B10 fit) and its
R ratio at 0.1 W; agreement within a factor 1.5.  Winner and two runners-up at P_req printed.
Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B12  (level: derived, unverified)")
target = best(arch_designs("Cu plate"), 0.1)[0]
print_inputs(target_R_fa=target, eta_fan=ETA_FAN, tau_life=TAU_LIFE, T0=T0, P_bracket="0.01-30 W")
names = ["Al plate k=100", "Al plate k=150", "Al plate k=180", "Al plate k=200", "Al pin k=150 fav", "Gyroid ks=150 cf=0.3 chi=0.2"]
out = {}
for n in names:
    ds = arch_designs(n)
    Preq, note = required_power(ds, target)
    Rs = [min_R(ds, P) for P in P_SET]
    nn = lnfit_slope(P_SET, Rs)
    R01 = min_R(ds, 0.1)
    print("\n%s: R_fa(0.1 W)=%.4f (ratio to Cu %.4f), own n=%.4f" % (n, R01, R01 / target, nn))
    if Preq is None:
        print("  P_req: not reachable (%s)" % note)
        out[n] = None
        issue("B12 %s: not reachable at P<=30 W (%s)" % (n, note))
        continue
    dW = (Preq - 0.1) / ETA_FAN
    dS = dW / T0
    dE = dW * TAU_LIFE
    est2 = 0.1 * (R01 / target) ** (-1.0 / nn)
    fac = max(Preq / est2, est2 / Preq)
    print("  P_req = %.4f W (%s); dW_elec = %.4f W; dS = %.3e W/K; dE = %.2f MJ" % (Preq, note, dW, dS, dE / 1e6))
    print("  second estimate from n: %.4f W; factor between estimates %.3f" % (est2, fac))
    check("B12 %s: bisection and B10 estimate agree within factor 1.5" % n, fac <= 1.5, "factor %.3f" % fac)
    rk = ranked(ds, Preq)
    for i, (R, r, d) in enumerate(rk[:3]):
        print("   %s R_fa=%.4f V=%.4e dP=%.3f Re=%.1f eta=%.3f NTU=%.3f mass=%.4f %s %s" % (("WIN", "ru2", "ru3")[i], R, r["V"], r["dP"], r["Re"], r["eta"], r["NTU"], r["mass"], d.label(), r["flags"]))
    bn = boundary_notes(rk[0][2], rk[0][2].kind)
    print("   winner boundary: " + ("; ".join(bn) if bn else "interior"))
    if bn:
        issue("B12 %s at P_req=%.3f W: winner on boundary: %s (%s)" % (n, Preq, "; ".join(bn), rk[0][2].label()))
    out[n] = (Preq, dW, dE)
if out.get("Al plate k=150"):
    Preq, dW, dE = out["Al plate k=150"]
    rng("Al plate k=150 P_req", Preq, 0.15, 0.35)
    rng("Al plate k=150 dW_elec", dW, 0.2, 1.0)
    rng("Al plate k=150 dE [MJ]", dE / 1e6, 30, 160)
