"""C15 displacement-controlled counter-case (bending under imposed curvature).

Spec row: C15 (no dependency beyond M03).  dD/dt = (1/tau0)(1 - t/t_c)^m, so in units of t_c:
 D(s) = (1/rho) int_0^s (1-x)^m dx, D(1) = 1/((m+1) rho).  Failure only if rho < 1/(m+1).
 tau = t_c{1 - [1-(m+1)rho]^(1/(m+1))}.
Verification: Simpson (64 doubling to 1e-8) of D plus bisection on s in (0,1] for D = 1 (independent of the
closed form), for every rho; rho* located by bisection on rho of Simpson D(1) - 1 over [0.09,0.095]
(independent of D(1) = 1/((m+1)rho)).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_common import *
m = M_EXP

def D_s(s, rho):
    val, n, rel = simpson_adaptive(lambda x: (1 - x) ** m, 0.0, s, 1e-10)
    return val / rho

rs = 1.0 / (m + 1)
print("m = %.5f, rho* = 1/(m+1) = %.6f (planner 0.0926)" % (m, rs))
for rho in (0.01, 0.05, 0.09, 0.095, 0.1, 1.0):
    d1_closed = 1.0 / ((m + 1) * rho)
    d1_num = D_s(1.0, rho)
    if rho < rs:
        cf = 1 - (1 - (m + 1) * rho) ** (1 / (m + 1))
        r, flo, fhi, it = bisect(lambda s: D_s(s, rho) - 1.0, 1e-12, 1.0)
        print("  rho=%-5g D(t_c) closed=%.5f Simpson=%.5f (>1) ; tau/t_c closed=%.8f, Simpson+bisection=%.8f (rel diff %.1e); tau/tau0=%.4f" %
              (rho, d1_closed, d1_num, cf, r, abs(cf / r - 1), cf / rho))
    else:
        r, flo, fhi, it = bisect(lambda s: D_s(s, rho) - 1.0, 1e-12, 1.0)
        print("  rho=%-5g D(t_c) closed=%.5f Simpson=%.5f (<1): no fatigue failure; bisection %s (ends %.3f, %.3f)" %
              (rho, d1_closed, d1_num, "found a root?!" if r is not None else "no sign change, as expected", flo, fhi))
print()
for e_rho, e in ((0.01, 1.053), (0.05, 1.39)):
    cf = (1 - (1 - (m + 1) * e_rho) ** (1 / (m + 1))) / e_rho
    print("  tau/tau0 at rho=%g: %.4f expected %.3f diff %+.2f%% %s" % (e_rho, cf, e, (cf / e - 1) * 100, "PASS" if abs(cf / e - 1) <= 0.01 else "FAIL"))
g = lambda rho: D_s(1.0, rho) - 1.0
print("  sweep bracketing: D(t_c)-1 at rho=0.09: %+.5f, at 0.095: %+.5f -> bracketed: %s" % (g(0.09), g(0.095), g(0.09) > 0 > g(0.095)))
r, flo, fhi, it = bisect(g, 0.09, 0.095)
print("  rho* by bisection on Simpson D(1)-1 over [0.09,0.095] = %.8f (closed 1/(m+1)=%.8f, rel diff %.1e) -> %s" % (r, rs, abs(r / rs - 1), "PASS" if abs(r / rs - 1) <= 0.01 else "FAIL"))
