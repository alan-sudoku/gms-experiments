"""A7, A8: electro-thermal temperature rise with section loss, and the time to lose
fraction x_a of the section with self-heating relative to isothermal at T_env.

Spec rows A7, A8 (plan 3.3; formulas of 2.5).
A7: closed form dT = dT0/(1 - x - alpha dT0); x_run = 1 - alpha dT0; independent
    fixed-point iteration dT <- dT0 (1 + alpha dT)/(1 - x) from dT0 until change
    < 1e-10 K (divergence reported when loop gain G = alpha dT0/(1-x) >= 1).
    Note: the iteration solves the same linear equation as the closed form, so it
    is an independent numerical route to the same fixed point, not an independent
    model (recorded in issues).
A8: (a) Simpson of exp[-(Q/R)(1/Te - 1/(Te + dT(x)))] on [0,x_a] / x_a, dT(x) from A7
    closed form; (b) RK4 of dx/dt = (1/t_c) exp[...] with t_c = 1, step t_c/200, halved
    until the time to x_a changes < 0.1 %, event located by bisection inside the
    bracketing step.  T_env = 300 K, Q = 50 kJ/mol, x_a = 0.5, R = M01.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from p6_common import simpson, bisect, tag, R_GAS as R

def dT_closed(dT0, alpha, x):
    den = 1 - x - alpha * dT0
    return dT0 / den if den > 0 else np.inf

def dT_iter(dT0, alpha, x, tol=1e-10, maxit=200000, cap=1e9):
    d = dT0
    for i in range(maxit):
        n = dT0 * (1 + alpha * d) / (1 - x)
        if n > cap:
            return np.inf, i, 'diverged'
        if abs(n - d) < tol:
            return n, i, 'converged'
        d = n
    return d, maxit, 'maxit'

print("=== A7 ===")
maxrd = 0; nchk = 0
diverge_ok = True
for dT0 in [1, 5, 20, 50, 100]:
    for a in [0.0, 0.0039, 0.0040]:
        print(f"dT0={dT0} alpha={a}: x_run=1-alpha*dT0={1-a*dT0:.4f}")
        for x in [0, 0.2, 0.5, 0.8]:
            G = a * dT0 / (1 - x)
            c = dT_closed(dT0, a, x)
            it, n, st = dT_iter(dT0, a, x)
            if G < 0.9:
                rd = abs(it - c) / c
                maxrd = max(maxrd, rd); nchk += 1
                tg = tag(rd < 1e-8)
            elif G < 1:
                rd = abs(it - c) / c
                tg = f"(0.9<=G<1, not in tolerance scope) rel={rd:.1e}"
            else:
                tg = f"G>=1: iteration {st}; closed form {'infinite/negative' if not np.isfinite(c) else c}"
                diverge_ok &= (st != 'converged')
            print(f"   x={x}: G={G:.4f} closed={c:.5f} iter={it:.5f} (n={n}) {tg}")
print(f"A7 max rel diff closed vs iteration over G<0.9 ({nchk} cases) = {maxrd:.2e} {tag(maxrd<1e-8)}")
print(f"A7 G>=1 cases never converge: {tag(diverge_ok)}")
for dT0, a, h in [(50, 0.004, 0.80), (100, 0.004, 0.60)]:
    print(f"A7 hand x_run dT0={dT0} alpha={a}: hand {h} calc {1-a*dT0:.3f} {tag(abs(1-a*dT0-h)<5e-3)}")
v = dT_closed(5, 0.004, 0.5)
print(f"A7 hand dT0=5 x=0.5 alpha=0.004: hand 10.42 calc {v:.4f} {tag(abs(v-10.42)<0.01)}")

print("\n=== A8 ===")
Te, Q, xa = 300.0, 50e3, 0.5
def rate(x, dT0, a):
    dT = dT_closed(dT0, a, x)
    return np.exp((Q / R) * (1 / Te - 1 / (Te + dT)))   # dx/dt in units of 1/t_c

def time_rk4(dT0, a, h, tol_bis=1e-13):
    """time to reach x_a, t_c=1; fixed step h (RK4), bisection in the bracketing step."""
    f = lambda x: rate(x, dT0, a)
    def step(x, hh):
        k1 = f(x); k2 = f(x + 0.5 * hh * k1); k3 = f(x + 0.5 * hh * k2); k4 = f(x + hh * k3)
        return x + hh / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    x, t = 0.0, 0.0
    while True:
        xn = step(x, h)
        if xn >= xa:
            g = lambda s: step(x, s * h) - xa
            r = bisect(g, 0.0, 1.0, rtol=1e-13)
            return t + r['root'] * h
        x, t = xn, t + h

res = {}
for a in [0.0, 0.004]:
    for dT0 in [0, 1, 5, 20]:
        fq = lambda x: np.exp(-(Q / R) * (1 / Te - 1 / (Te + np.array([dT_closed(dT0, a, xi) for xi in x]))))
        Ia, n, rc, ok = simpson(fq, 0.0, xa)
        ratio_a = Ia / xa
        h = 1 / 200; tprev = None; hist = []
        while True:
            tt = time_rk4(dT0, a, h)
            hist.append((h, tt))
            if tprev is not None and abs(tt - tprev) / tt < 1e-3:
                break
            tprev = tt; h /= 2
            if h < 1e-6: break
        t_b = hist[-1][1]
        ratio_b = t_b / xa
        iso = np.exp(-(Q / R) * (1 / Te - 1 / (Te + dT0)))
        rd = abs(ratio_a - ratio_b) / ratio_a
        res[(a, dT0)] = ratio_a
        xrun = 1 - a * dT0
        print(f"alpha={a} dT0={dT0:2d}: (a) Simpson ratio={ratio_a:.5f} (n={n}) | (b) RK4 ratio={ratio_b:.5f} "
              f"steps tried (h,t)={[(round(1/hh),round(tt,6)) for hh,tt in hist]} | rel diff a/b={rd:.2e} {tag(rd<2e-3)} | "
              f"isothermal-at-dT0={iso:.4f} | x_run={xrun:.3f} {'>' if xrun>xa else '<='} x_a")
for dT0, h in [(0, 1.000), (1, 0.91), (5, 0.64), (20, 0.19)]:
    v = res[(0.0, dT0)]
    print(f"A8 hand alpha=0 dT0={dT0}: hand {h} calc {v:.4f} rel={abs(v-h)/h:.3f} {tag(abs(v-h)/h<0.05)}")
iso5 = np.exp(-(Q / R) * (1 / Te - 1 / (Te + 5)))
print(f"A8 hand isothermal at dT0=5 K: hand 0.72 calc {iso5:.4f} {tag(abs(iso5-0.72)/0.72<0.05)}")
print(f"A8 x_run check alpha=0.004 dT0=20: x_run={1-0.004*20:.3f} (hand 0.92) > x_a=0.5: {tag(1-0.004*20>xa)}")
print("A8 note: null case alpha=0, dT0=0 gives exactly 1.000 in both (a),(b); (b) integrates the same separable ODE as (a) "
      "(a) is a quadrature of 1/f, (b) an RK4 of f: independent numerics, same model.")
