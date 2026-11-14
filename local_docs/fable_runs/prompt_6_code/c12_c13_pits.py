"""C12 pit as a crack-like defect (El Haddad); C13 life with a growing pit and perforation time.

Spec rows: C12 (needs C1), C13 (needs C1, C12).  Inputs M15 (Y = 2*1.12/pi = 0.713), M24, M25;
LOOKUP L02 (DeltaK_th 2/3/5 MPa sqrt(m)) NOT read from a source (planner UNSURE grid used);
L06 pre-pitted life data used for comparison only (not read; planner range only).
C12: a0 = (1/pi)(DKth/(Y DSe))^2, DSe = 2 sigma_a0; K(a) = sqrt(a0/(a0+a)); life factor K^-m.
C13 (a) linear growth a = PF r t: closed form; independent check = Simpson integral of
 D(tau) = (1/tau0) int (1+a/a0)^(m/2) dt (in v = t) with bisection on tau, which does NOT use the closed form.
 (b) cube-root growth a = A t^(1/3), a(1 yr) = PF r (1 yr); D by Simpson in v = t^(1/3), bisection on (0,tau0].
 (c) t_perf = h0/(n_s PF r); life = min(tau_pit, t_perf).  nu = 1 Hz, h0 = 0.3 mm, n_s = 2.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_common import *

S0 = sigma_a0()
m = M_EXP
def a0_of(dkth):
    return (1 / math.pi) * (dkth / (Y_GEOM * 2 * S0)) ** 2   # m (MPa sqrt(m) / MPa)

print("C12  Y = %.4f, sigma_a0 = %.3f MPa, Delta sigma_e = %.3f MPa" % (Y_GEOM, S0, 2 * S0))
exp_a0 = {2: 53, 3: 119, 5: 331}
for dk in (2, 3, 5):
    a0 = a0_of(dk) * 1e6
    print("  DKth=%d: a0 = %.2f um (expected %d) diff %+.2f%% -> %s" % (dk, a0, exp_a0[dk], (a0 / exp_a0[dk] - 1) * 100, "PASS" if abs(a0 / exp_a0[dk] - 1) <= 0.03 else "FAIL"))
expK = {10: (0.960, 1.49), 30: (0.894, 3.0), 100: (0.737, 19.9), 300: (0.533, 478)}
a0b = a0_of(3) * 1e6
print("  baseline DKth=3, a0=%.2f um:" % a0b)
for a in (10, 30, 100, 300):
    K = math.sqrt(a0b / (a0b + a)); lf = K ** (-m)
    eK, eL = expK[a]
    print("    a=%3d um K=%.4f (exp %.3f) life factor %.3f (exp %g) diffs %+.2f%% / %+.2f%% -> %s" % (a, K, eK, lf, eL, (K / eK - 1) * 100, (lf / eL - 1) * 100,
          "PASS" if abs(K / eK - 1) <= 0.03 and abs(lf / eL - 1) <= 0.03 else "FAIL"))
print("  all DKth, life factors K^-m:")
for dk in (2, 3, 5):
    a0 = a0_of(dk) * 1e6
    print("    DKth=%d: " % dk + ", ".join("a=%d um: %.3g" % (a, (a0 / (a0 + a)) ** (-m / 2)) for a in (10, 30, 100, 300)))
print("  L06 comparison (plausibility only; L06 NOT read; planner range 'life factor 2 to 10 or more at ~100 um'): baseline factor at 100 um = %.1f, ABOVE the planner's 2-10 range but the planner states 'or more'; flagged for the reader." % ((a0b / (a0b + 100)) ** (-m / 2)))
print("  Note: the dD/dt = (1/tau0)(1+a/a0)^(m/2) assumption (K^-m with K=sqrt(a0/(a0+a))) is a model assumption of medium-low confidence per the plan; not tested here.")

print("\nC13  a0 baseline = %.2f um (C12), tau0 (1 Hz) = %.4f yr, h0=0.3 mm, n_s=2" % (a0b, tau0_years(1.0)))
tau0 = tau0_years(1.0)
a0 = a0_of(3)          # m
yr_um = 1e-6           # m per um

def tau_lin_closed(pf, r):
    ta = a0 / (pf * r * yr_um)     # yr
    e = m / 2 + 1
    return ta * ((1 + e * tau0 / ta) ** (1 / e) - 1)

def D_lin_simpson(tau, pf, r):
    g = pf * r * yr_um
    val, n, rel = simpson_adaptive(lambda t: (1 + g * t / a0) ** (m / 2), 0.0, tau, 1e-10)
    return val / tau0

def D_cbrt_simpson(tau, pf, r):
    g = pf * r * yr_um   # a(t) = g * t^(1/3) with t in yr
    # t = v^3, dt = 3 v^2 dv
    val, n, rel = simpson_adaptive(lambda v: (1 + g * v / a0) ** (m / 2) * 3 * v ** 2, 0.0, tau ** (1 / 3), 1e-8)
    return val / tau0

exp_a = {(10, 10): (1.31, 12.1), (1, 10): (5.3, 3.0), (1, 1): (12.3, 1.29)}
print("(a) linear: tau closed / tau by Simpson+bisection / F = tau0/tau / t_perf / life=min")
for pf in PF_GRID:
    for r in (1, 10):
        tc_ = tau_lin_closed(pf, r)
        rb, flo, fhi, it = bisect(lambda t: D_lin_simpson(t, pf, r) - 1.0, 1e-9, tau0)
        tp = 0.3e-3 / (2 * pf * r * yr_um)
        e = exp_a.get((pf, r))
        es = ""
        if e:
            es = " expected tau=%.2f F=%.2f diffs %+.2f%% %+.2f%% %s" % (e[0], e[1], (tc_ / e[0] - 1) * 100, (tau0 / tc_ / e[1] - 1) * 100,
                  "PASS" if abs(tc_ / e[0] - 1) <= 0.03 and abs(tau0 / tc_ / e[1] - 1) <= 0.03 else "FAIL")
        print("   PF=%-2d r=%-2g tau_closed=%.5f tau_Simpson=%.5f (rel diff %.1e, bracket ends %.3f,%.3f) F=%.3f t_perf=%.4f life=min=%.4f (%s)%s" %
              (pf, r, tc_, rb, abs(tc_ / rb - 1), flo, fhi, tau0 / tc_, tp, min(tc_, tp), "perforation first" if tp < tc_ else "fatigue first", es))
print("   planner: t_perf = 1.5 yr for PF=10, r=10 -> computed %.4f" % (0.3e-3 / (2 * 10 * 10 * yr_um)))
print("(b) cube-root growth a = A t^(1/3), a(1 yr) = PF r um; Simpson in v = t^(1/3) + bisection")
for pf in PF_GRID:
    for r in (1, 10):
        D_end = D_cbrt_simpson(tau0, pf, r)
        rb, flo, fhi, it = bisect(lambda t: D_cbrt_simpson(t, pf, r) - 1.0, 1e-9, tau0)
        tl = tau_lin_closed(pf, r)
        tp = 0.3e-3 / (2 * pf * r * yr_um)
        print("   PF=%-2d r=%-2g tau_b=%.5f yr (D(tau0)=%.3f>=1: %s) vs (a) tau=%.5f -> (b) %s (a)%s; F_b=%.3f t_perf=%.4f (perforation time uses linear PF r; spec c) life_b=min=%.4f" %
              (pf, r, rb, D_end, D_end >= 1, tl, "LONGER than" if rb > tl else "shorter than/equal to", "; expectation 'longer for tau>1 yr': " + ("consistent" if (tl > 1) == (rb > tl) else "NOT consistent"), tau0 / rb, tp, min(rb, tp)))
# convergence of Simpson for one case
for tol in (1e-6, 1e-8, 1e-10):
    g = 10 * 10 * yr_um
    val, n, rel = simpson_adaptive(lambda v: (1 + g * v / a0) ** (m / 2) * 3 * v ** 2, 0.0, 1.5 ** (1 / 3), tol)
    print("   Simpson convergence (PF=10, r=10, tau=1.5 yr) tol=%g: value %.10g with n=%d, last rel change %.1e" % (tol, val, n, rel))
