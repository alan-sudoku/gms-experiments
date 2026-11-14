"""C6 worst case of F_min over rho; C7 effect of an allowable section loss.

Spec rows: C6, C7 (no dependency on other rows beyond the C4 closed form).
Method: grid rho in [1e-3,1e3] at 20 points per decade (121 points); the maximum must be
strictly interior; golden-section on ln(rho) on each side of the kink (kink at rho=1 for C6,
rho=x_allow for C7), each side bracketed by the grid neighbours of the grid maximum.
Closed-form comparison for C6 at rho=1 is an IDENTITY check (the C4 formula evaluated at rho=1),
so an additional independent check uses the RK4 first-passage of C5 at rho=1.
C7: rho_1 compared with a bisection on tau_c(rho) - tau_rec (forward formula only; the closed
form rho_1 is the algebraic inverse, so the bisection is independent of the inversion algebra
but shares the C4 formula).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_common import *
from c5_rk4_verify import rk4_life

def fmin_c6(rho, q):
    return float(c4(rho, q)[2])

def fmin_c7(rho, q, xa):
    x = float(tau_c_over_tc(rho, q))
    rec = xa
    return min(rho, rec) / min(x, rec)

def maximise(F, grid, kink):
    """Grid maximum, interior test, golden section on ln rho each side of the kink."""
    v = np.array([F(r) for r in grid])
    i = int(np.argmax(v))
    info = {"i": i, "grid_rho": grid[i], "grid_val": v[i], "interior": 0 < i < len(grid) - 1}
    if not info["interior"]:
        return info, None
    lo, hi = grid[i - 1], grid[i + 1]
    cand = []
    for a, b in ((lo, min(kink, hi)), (max(kink, lo), hi)):
        if b > a * (1 + 1e-12):
            g = lambda lr: F(math.exp(lr))
            lr, val = golden_max(g, math.log(a), math.log(b))
            cand.append((math.exp(lr), val))
    best = max(cand, key=lambda c: c[1])
    return info, (best, cand)

grid = log_grid(1e-3, 1e3, 20)
print("grid: %d points rho in [%g, %g], 20/decade" % (len(grid), grid[0], grid[-1]))
print("\nC6")
exp6 = {3: 2.37, 5: 3.02, 9.804: 4.38, 15: 5.69, 19.608: 6.77, 29.412: 8.91}
for q, e in exp6.items():
    qq = 9.804 if q == 9.804 else q
    info, res = maximise(lambda r: fmin_c6(r, qq), grid, 1.0)
    (rb, vb), cand = res
    cf = 1.0 / (1.0 - qq ** (-1.0 / (qq - 1.0)))
    rk, _, _, _ = rk4_life(1.0, qq)
    f_rk = 1.0 / rk
    print("  q=%-7g grid max at rho=%.4f (F=%.4f, interior=%s); golden rho=%.8f F=%.6f; closed 1/(1-q^(-1/(q-1)))=%.6f; "
          "RK4-based F_min(rho=1)=%.6f; expected %.2f diff %+.2f%% %s" %
          (qq, info["grid_rho"], info["grid_val"], info["interior"], rb, vb, cf, f_rk, e, (vb/e-1)*100,
           "PASS" if abs(vb/e-1) <= 0.01 else "FAIL"))
    print("     both-sides golden: %s" % ", ".join("rho=%.6f F=%.6f" % c for c in cand))
    print("     IDENTITY: grid/golden value at rho=1 vs closed form compares C4's formula with itself at rho=1 (agreement %.1e); independent check = RK4 value above (diff %.1e)" %
          (abs(vb-cf), abs(f_rk-cf)))
print("\n  F_cur at rho=1e3 (C6 extra report):")
for q in (3, 5, 9.804, 15, 19.608, 29.412):
    x, fc, fm = c4(1e3, q)
    print("  q=%-7g tau_c/t_c=%.4f F_cur=%.2f F_cur/rho=%.4f F_min=%.4f" % (q, x, fc, fc/1e3, fm))
print("  planner: F_cur >= rho; about 1.55*rho for q=9.804 (tau_c/t_c ~ 0.64): ", end="")
x, fc, _ = c4(1e3, 9.804)
print("computed F_cur/rho = %.3f, tau_c/t_c = %.3f -> %s" % (fc/1e3, x, "PASS" if fc >= 1e3 and abs(fc/1e3/1.55-1) < 0.02 else "FAIL/CHECK"))

print("\nC7  (q=9.804 and 19.608)")
exp7 = {(9.804, 0.2): 1.84, (9.804, 0.5): 2.87, (9.804, 0.8): 3.79, (9.804, 1.0): 4.38}
for q in (9.804, 19.608):
    for xa in (0.2, 0.5, 0.8, 1.0):
        info, res = maximise(lambda r: fmin_c7(r, q, xa), grid, xa)
        (rb, vb), cand = res
        if xa < 1.0:
            rho1 = ((1 - xa) ** (-(q - 1)) - 1) / (q - 1)
        else:
            rho1 = float("inf")
        # bisection: tau_c(rho) - xa = 0 (rho > xa side)
        g = lambda r: float(tau_c_over_tc(r, q)) - xa
        if xa < 1.0:
            root, glo, ghi, it = bisect(g, 1e-3, 1e3)
            ext = ""
            if root is None:
                ext = "NO SIGN CHANGE on [1e-3,1e3] (ends %.3e, %.3e); extended once x10 to [1e-4,1e4]: " % (glo, ghi)
                root, glo, ghi, it = bisect(g, 1e-4, 1e4)
            if root is None:
                bres = ext + "still no sign change (ends %.3e, %.3e): rho_1 NOT BRACKETED (closed form says %.4g)" % (glo, ghi, rho1)
                rcheck = float('nan')
            else:
                bres = ext + "bisect rho_1=%.6f (g ends %.3f,%.3f, bracketed)" % (root, glo, ghi)
                rcheck = abs(root / rho1 - 1)
            fcheck = fmin_c7(rho1 * 1.5, q, xa)
        else:
            bres = "x_allow=1: tau_rec=t_c, no rho_1 (tau_c<t_c always); F_min>1 for all rho"
            rcheck = float('nan'); fcheck = float('nan')
        e = exp7.get((q, xa))
        es = ("expected %.2f diff %+.2f%% %s" % (e, (vb/e-1)*100, "PASS" if abs(vb/e-1) <= 0.02 else "FAIL")) if e else "no planner value"
        print("  q=%-6g x_allow=%.1f grid max rho=%.3f (interior=%s), golden max F_min=%.4f at rho=%.5f; %s" %
              (q, xa, info["grid_rho"], info["interior"], vb, rb, es))
        print("      rho_1 closed=%s; %s; rel.diff %.1e; F_min at 1.5*rho_1 = %.6f (expect 1)" % (rho1, bres, rcheck, fcheck))
print("\nC7 q=9.804 planner: rho_1 = 0.70 for x_allow=0.2 ->  computed %.4f" % (((1-0.2)**(-(9.804-1))-1)/(9.804-1)))
print("C7 maximum location: planner states max at rho = x_allow; compare golden rho above.")
