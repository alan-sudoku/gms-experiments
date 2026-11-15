"""Prompt 6 review (S5), script 3: spot-check of the rows S4 marked "not recomputed" for b = -0.124.

Level `derived` (unverified). Closed forms restated from prompt_6_answer.md (M2.5, M2.9, M2.10);
the parabolic case uses quadrature + brentq. Compares the change from b = -0.102 to -0.124 with the
direction and rough size S4 states in "Changed since plan".

Run: <gms-local>/.venv/bin/python rv03_not_recomputed_rows.py > outputs/rv03_not_recomputed_rows.txt
"""
import math
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

SIGF, N0, YR = 900.0, 5e8, 3.15576e7
TAU0 = N0 / YR


def xc_lin(rho, q):
    return 1 - (1 + (q - 1) * rho) ** (-1 / (q - 1))


def c7_max(q, xa):
    f = lambda lr: -(min(10 ** lr, xa) / min(xc_lin(10 ** lr, q), xa))
    r = minimize_scalar(f, bounds=(-3, 3), method="bounded", options={"xatol": 1e-9})
    return -r.fun


def par_life(rho, q):
    g = lambda x: 2 * quad(lambda u: u * (1 - u) ** (-q), 0, x, epsabs=1e-13)[0] - rho
    x = brentq(g, 1e-12, 1 - 1e-9)
    return x * x  # tau / t_c


out = {}
for b in (-0.102, -0.124):
    m = -1 / b
    sig = SIGF * (2 * N0) ** b
    o = {}
    o["C7 xa=0.2,0.5,0.8 (q=m)"] = [c7_max(m, xa) for xa in (0.2, 0.5, 0.8)]
    o["C7 xa=0.2,0.5,0.8 (q=2m)"] = [c7_max(2 * m, xa) for xa in (0.2, 0.5, 0.8)]
    o["C9 parabolic F_min rho=0.01,0.1,1,10 (q=m)"] = [min(r, 1) / par_life(r, m) for r in (0.01, 0.1, 1, 10)]
    o["C9 parabolic F_min rho=1 (q=2m)"] = [1 / par_life(1, 2 * m)]
    # C13 linear pit growth grid, 0.3 mm wall, n_s = 2
    Y = 2 * 1.12 / math.pi
    a0 = (1 / math.pi) * (3.0 / (Y * 2 * sig)) ** 2 * 1e6
    e = m / 2 + 1
    lives = []
    for PF in (1, 3, 10, 30):
        for r in (1, 10):
            ta = a0 / (PF * r)
            tau = ta * ((1 + e * TAU0 / ta) ** (1 / e) - 1)
            lives.append(tau)
    o["C13 linear pit-fatigue lives PF 1,3,10,30 x r 1,10 (yr)"] = lives
    # C15 displacement control lives tau/tau0
    o["C15 tau/tau0 rho=0.01,0.05"] = [(1 - (1 - (m + 1) * r) ** (1 / (m + 1))) / r for r in (0.01, 0.05)]
    # B1 equal-life point s* = phi^(-1/m)
    o["B1 s* phi=10,100,1000"] = [phi ** (-1 / m) for phi in (10, 100, 1000)]
    out[b] = o

print("rv03: rows S4 marked 'not recomputed'; values for b = -0.102 and b = -0.124, ratio. Level derived.")
for k in out[-0.102]:
    a, c = out[-0.102][k], out[-0.124][k]
    print("%-58s" % k)
    print("    b=-0.102: " + ", ".join("%.4g" % v for v in a))
    print("    b=-0.124: " + ", ".join("%.4g" % v for v in c))
    print("    ratio   : " + ", ".join("%.3f" % (y / x) for x, y in zip(a, c)))
# Missed regime (review #15): hysteresis multiplier for a round strut, p = 2n - 2, at the g end-of-life loss x_e = 0.15017
def m_lin(xe, p):
    return -math.log(1 - xe) / xe if abs(p - 1) < 1e-12 else ((1 - xe) ** (1 - p) - 1) / ((p - 1) * xe)
for n in (2, 3, 5, 8):
    p = 2 * n - 2
    print("Lazan n = %d: p = %d, M_lin(x_e = 0.15017) = %.4f ; Rule R gate 0.095/p = %.4f" % (n, p, m_lin(0.15017, p), 0.095 / p))
print("All values level `derived`.")
