"""C8 lower bound on the coupled life.

Spec row: C8 (needs C4).  x* by bisection of x - rho (1-x)^q on (0,1) (ends -rho and +1);
ratio tau_LB/tau_c = x*/(tau_c/t_c) on the C6 rho grid (121 points, 1e-3..1e3);
minimum ratio located on the grid and refined by golden section on ln(rho) (golden maximises
-ratio); end-of-grid minima are reported.  The real test: ratio <= 1 at every rho.
Independence: x* uses the bound's own equation; tau_c uses the C4 closed form; the two share
no algebra, so ratio <= 1 is a genuine test of the bound (not an identity).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_common import *

grid = log_grid(1e-3, 1e3, 20)
for q in (4.5585, 9.804, 19.608):
    # bracket ends check
    rho = 1.0
    ends = (0.0 - rho * 1.0, 1.0 - 0.0)
    ratios = np.array([c8_ratio(r, q) for r in grid])
    i = int(np.argmin(ratios))
    interior = 0 < i < len(grid) - 1
    print("q=%g: max ratio over grid = %.8f (<=1: %s); grid min ratio %.6f at rho=%.4g (interior=%s)" %
          (q, ratios.max(), "PASS" if ratios.max() <= 1.0 else "FAIL", ratios[i], grid[i], interior))
    if interior:
        lr, v = golden_max(lambda lr: -c8_ratio(math.exp(lr), q), math.log(grid[i-1]), math.log(grid[i+1]))
        print("    golden: min ratio = %.4f at rho = %.5g" % (-v, math.exp(lr)))
    else:
        ext = log_grid(grid[0] / 10 if i == 0 else grid[-1], grid[0] if i == 0 else grid[-1] * 10, 20)
        r2 = np.array([c8_ratio(r, q) for r in ext])
        print("    minimum at grid end (rho=%.3g); extended one decade: min over extension %.6f at rho=%.4g" % (grid[i], r2.min(), ext[int(np.argmin(r2))]))
    print("    ratio at rho = 1e-3, 1e-2, 0.1, 1, 10, 100, 1e3: " + ", ".join("%.4f" % c8_ratio(r, q) for r in (1e-3, 1e-2, .1, 1, 10, 100, 1e3)))
    # bisection verification: residual
    for r in (0.01, 1.0, 100.0):
        xs = x_star(r, q)
        print("    rho=%-5g x*=%.6f residual x-rho(1-x)^q = %.2e  tau_LB/t_c=%.6f tau_c/t_c=%.6f" % (r, xs, xs - r * (1 - xs) ** q, xs, float(tau_c_over_tc(r, q))))
print()
print("Planner checks (UNSURE hand values):")
x = x_star(1.0, 9.804); print("  q=9.804 rho=1: x*=%.4f (exp 0.167), ratio=%.4f (exp 0.73) -> %s" % (x, c8_ratio(1.0, 9.804), "PASS" if abs(x/0.167-1)<0.02 and abs(c8_ratio(1.0,9.804)/0.73-1)<0.02 else "CHECK"))
print("  q=9.804 rho=100: ratio=%.4f (exp about 0.80)" % c8_ratio(100.0, 9.804))
x = x_star(1.056, 19.608); print("  q=19.608 rho=1.056: x*=%.4f (exp 0.109)" % x)
print("  ratio -> 1 as rho -> 0: ratio(1e-3)=%.5f, ratio(1e-6)=%.7f (q=9.804)" % (c8_ratio(1e-3, 9.804), c8_ratio(1e-6, 9.804)))
