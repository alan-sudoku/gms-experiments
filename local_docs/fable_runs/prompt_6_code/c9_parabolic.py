"""C9 coupled life with parabolic (oxidation) section loss.

Spec row: C9.  x = sqrt(t/t_c).  D(tau) = (2 t_c/tau0){[W^(1-q)-1]/(q-1) - [W^(2-q)-1]/(q-2)}, W = 1 - sqrt(tau/t_c).
Route 1: bisection on tau/t_c in (0,1) of D - 1 with this closed form (ends: -1 and +huge).
Route 2 (independent): Simpson (64 intervals, doubling to rel. change 1e-8, plan 3.2 default) of
D(S) = (1/rho) * int_0^S 2 s (1-s)^(-q) ds, S = sqrt(tau/t_c); the integrand comes directly from
dD/dt = (1/tau0)(1-sqrt(t/t_c))^(-q) with t = t_c s^2, never using the antiderivative.
Route 2 bisection on tau/t_c uses the Simpson D.  F_min = min(tau0,t_c)/tau.
Assumptions: q = 9.804 and 19.608; dimensional illustration uses k_p = 1e-16 m2/s (parametric).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_common import *

def D_closed(u, rho, q):
    """u = tau/t_c."""
    S = math.sqrt(u)
    lw = math.log1p(-S)
    a = math.expm1((1 - q) * lw) / (q - 1)
    b = math.expm1((2 - q) * lw) / (q - 2)
    return 2.0 / rho * (a - b)

def D_simpson(u, rho, q):
    S = math.sqrt(u)
    val, n, rel = simpson_adaptive(lambda s: 2 * s * (1 - s) ** (-q), 0.0, S, 1e-8)
    return val / rho

print("Dimensional illustration: h0=0.3 mm, n_s=2, k_p=1e-16 m2/s: t_c = h0^2/(2 k_p n_s^2) = %.4e s = %.4f yr (expected 1.125e8 s = 3.56 yr)" %
      ((0.3e-3) ** 2 / (2 * 1e-16 * 4), (0.3e-3) ** 2 / (2 * 1e-16 * 4) / YR))
print()
for q in (9.804, 19.608):
    for rho in (0.01, 0.1, 1.0, 10.0):
        # small-tau check
        u_small = 1e-8 * rho
        r1, f_lo, f_hi, it = bisect(lambda u: D_closed(u, rho, q) - 1.0, 1e-300 if False else 0.0, 1.0 - 1e-12)
        r2, g_lo, g_hi, it2 = bisect(lambda u: D_simpson(u, rho, q) - 1.0, 0.0, 1.0 - 1e-12)
        _, nq, relq = simpson_adaptive(lambda s: 2 * s * (1 - s) ** (-q), 0.0, math.sqrt(r1), 1e-8)
        Dq = D_simpson(r1, rho, q)
        fmin = min(rho, 1.0) / r1
        print("q=%-7g rho=%-5g closed: tau/t_c=%.8f (bracket ends %.3f, %.3e; %d it)  Simpson-route: %.8f (n=%d, rel chg %.1e)  rel.diff %.2e [%s]  D_simpson at closed root = %.8f  F_min=%.4f" %
              (q, rho, r1, f_lo, f_hi, it, r2, nq, relq, abs(r1 / r2 - 1), "PASS" if abs(r1 / r2 - 1) < 1e-6 else "FAIL", Dq, fmin))
    print("  small-tau check D -> tau/tau0: D_closed(u=1e-6 rho)/(u/rho)... ", end="")
    rho = 1.0; u = 1e-6
    print("ratio %.6f (expect ~1)" % (D_closed(u, rho, q) / (u / rho)))
print()
r1, *_ = bisect(lambda u: D_closed(u, 1.0, 9.804) - 1.0, 0.0, 1.0 - 1e-12)
fm = 1.0 / r1
print("Hand value check q=9.804 rho=1: tau/t_c = %.5f (planner ~0.086, +-5%% -> %s), F_min = %.3f (accept 10.5..13 -> %s)" %
      (r1, "PASS" if abs(r1/0.086-1) <= 0.05 else "FAIL", fm, "PASS" if 10.5 <= fm <= 13 else "FAIL"))
