"""C5 numerical verification of C4's closed form.

Spec row: C5 (needs C4).  Method: RK4 on dD/dt = (1/tau0)(1 - t/t_c)^(-q) in units of t_c
(t_c = 1, tau0 = rho), first passage of D = 1, step min(tau0,t_c)/400 halved until the
time changes < 0.1 %, event by bisection inside the bracketing step, upper limit t_c(1-1e-12).
Independence: the closed form comes from analytic integration of the integrand with a
power-law antiderivative; the RK4 route never uses that antiderivative, only the
integrand evaluated pointwise. They share the ODE (the model), so this verifies the
integration algebra of C4, NOT the physical model. Not an identity check.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_common import *

def rk4_life(rho, q, halve_tol=1e-3, max_halve=14):
    f = lambda t, D: (1.0 / rho) * (1.0 - t) ** (-q)
    t_end = 1.0 - 1e-12
    h = min(rho, 1.0) / 400.0
    prev = None
    for k in range(max_halve):
        t = first_passage_rk4(f, 1.0, t_end, h)
        if t is None:
            return None, h, k, None
        if prev is not None and abs(t - prev) / prev < halve_tol:
            return t, h, k, abs(t - prev) / prev
        prev = t
        h /= 2.0
    return prev, h, max_halve, None

if __name__ == "__main__":
    cases = [(0.01, 9.804), (0.1, 9.804), (1, 9.804), (10, 9.804), (1, 19.608), (1, 4.5585)]
    print("C5 RK4 first passage of D=1 vs C4 closed form (units of t_c)")
    allok = True
    for rho, q in cases:
        t, h, k, rel = rk4_life(rho, q)
        cf = float(tau_c_over_tc(rho, q))
        if t is None:
            print("  rho=%g q=%g: no passage before t_c(1-1e-12): UNDECIDED" % (rho, q)); allok = False; continue
        diff = abs(t / cf - 1)
        ok = diff < 1e-3
        allok &= ok
        print("  rho=%-5g q=%-7g RK4 tau/t_c=%.8f closed=%.8f rel.diff=%.2e  final step=%.3e after %d halvings (last change %.2e) %s" %
              (rho, q, t, cf, diff, h, k, rel if rel is not None else float('nan'), "PASS" if ok else "FAIL"))
    print("C5 overall:", "PASS" if allok else "FAIL")
