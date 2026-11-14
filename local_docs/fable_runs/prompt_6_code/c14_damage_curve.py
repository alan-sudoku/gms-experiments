"""C14 nonlinear (damage-curve) accumulation under continuously rising stress.

Spec row: C14 (needs C4).  ODE (units of t_c; t_c = 1, tau0 = rho):
 du/dt = (1/rho)(1-t)^(-q) + 0.4 q u ln(u)/(1-t),  u(0)=0, u ln u := 0 at u = 0.
 RK4 fixed step min(rho,1)/1000, halved until the time to u=1 changes < 0.1 %; event by bisection inside
 the bracketing step; upper limit t_c(1-1e-12); u kept in [0,1] (stage values: u<=0 -> u ln u = 0;
 u>1 evaluated at u = 1, where the term vanishes).
Null case q=0 returns tau0 by construction (the second term is multiplied by q): flagged as an identity
check of the event/step logic only.  Comparison: tau_DCA/tau_c, tau_c from the C4 closed form (q = 9.804).
Ratio below 1 would contradict the sign argument of plan 2.6; reported if it occurs.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_common import *

def dca_life(rho, q, tol=1e-3, max_halve=12):
    def f(t, u):
        uu = min(max(u, 0.0), 1.0)
        ul = uu * math.log(uu) if uu > 0 else 0.0
        return (1.0 / rho) * (1.0 - t) ** (-q) + 0.4 * q * ul / (1.0 - t)
    h = min(rho, 1.0) / 1000.0
    t_end = 1.0 - 1e-12
    prev = None
    hist = []
    for k in range(max_halve):
        t = first_passage_rk4(f, 1.0, t_end, h, y0=0.0, clamp=lambda u: max(0.0, u))
        hist.append((h, t))
        if t is None:
            return None, hist
        if prev is not None and abs(t - prev) / prev < tol:
            return t, hist
        prev = t
        h /= 2.0
    return prev, hist

print("C14  null case q=0 (identity of event logic; second term vanishes by construction)")
for rho in (0.01, 0.1, 1.0, 10.0):
    t, hist = dca_life(rho, 0.0)
    if t is None:
        print("   rho=%-5g UNDECIDED: with q=0, tau = tau0 = rho*t_c >= t_c, beyond the integration limit t_c(1-1e-12); u reaches 1 only at t = %g t_c" % (rho, rho)); continue
    print("   rho=%-5g tau/tau0 = %.8f (expected 1 within 0.1%%) %s" % (rho, t / rho, "PASS" if abs(t / rho - 1) < 1e-3 else "FAIL"))
print("\nC14  q=9.804, damage-curve approach vs Miner closed form (C4)")
for rho in (0.01, 0.1, 1.0, 10.0):
    t, hist = dca_life(rho, 9.804)
    if t is None:
        print("   rho=%g: u never reached 1 before t_c(1-1e-12): UNDECIDED" % rho); continue
    cf = float(tau_c_over_tc(rho, 9.804))
    ratio = t / cf
    steps = "; ".join("h=%.2e -> %.8f" % (h, v) for h, v in hist)
    conv = abs(hist[-1][1] - hist[-2][1]) / hist[-2][1] if len(hist) > 1 else float("nan")
    print("   rho=%-5g tau_DCA/t_c=%.8f tau_c/t_c=%.8f ratio=%.5f %s (in [1,2.5]: %s); halvings=%d, final change %.1e <0.1%%: %s" %
          (rho, t, cf, ratio, "(RATIO BELOW 1: contradicts sign argument)" if ratio < 1 else "", 1.0 <= ratio <= 2.5, len(hist) - 1, conv, conv < 1e-3))
    print("      step history: " + steps)
# extra convergence evidence: finer than the criterion
print("\nConvergence stress: rho=1, q=9.804, steps h = 1e-3 / 2^k:")
def f_(rho, q):
    def f(t, u):
        uu = min(max(u, 0.0), 1.0); ul = uu * math.log(uu) if uu > 0 else 0.0
        return (1.0 / rho) * (1.0 - t) ** (-q) + 0.4 * q * ul / (1.0 - t)
    return f
for k in range(0, 8):
    h = 1e-3 / 2 ** k
    print("   h=%.3e tau=%.10f" % (h, first_passage_rk4(f_(1.0, 9.804), 1.0, 1 - 1e-12, h, 0.0, lambda u: max(0.0, u))))
