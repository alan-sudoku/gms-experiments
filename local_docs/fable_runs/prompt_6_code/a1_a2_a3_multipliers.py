"""A1, A2, A3: life-averaged rate multipliers for linear and parabolic recession,
and the section-loss fraction at which the multiplier error equals eps.

Spec rows: A1, A2, A3 (plan 3.3; formulas of 2.2).
A1: M_lin closed form vs composite Simpson of (1-x)^-p on [0,x_e] / x_e.
A2: M_par p=1 closed form; all p by Simpson of 2 s (1-a s)^-p on [0,1].
    EXTRA (not in spec): general-p closed form of the parabolic integral used as a
    third cross-check (derived by substitution u = 1 - a s).
A3: bisection on x_e in [1e-6, 0.99] of M-1-eps for M_lin (closed form) and
    M_par (p=1 closed form, p=2,4 Simpson).
Assumptions: Simpson tol 1e-8, start 64 intervals, cap 2^24; bracket end values
printed; ends not bracketed are reported.  Run: .venv/bin/python <this file>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from p6_common import simpson, bisect, tag

XE = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
PS = [-1, 1, 2, 4, 5]


def mlin_closed(x, p):
    if p == 1:
        return -np.log1p(-x) / x
    return ((1 - x) ** (1 - p) - 1) / ((p - 1) * x)


def mlin_quad(x, p):
    v, n, rc, ok = simpson(lambda s: (1 - s) ** (-float(p)), 0.0, x)
    return v / x, n, rc, ok


def mpar_p1(a):
    return -2.0 * (a + np.log1p(-a)) / a ** 2


def mpar_quad(a, p):
    return simpson(lambda s: 2 * s * (1 - a * s) ** (-float(p)), 0.0, 1.0)


def mpar_closed_general(a, p):
    # 2/a^2 [ int_{1-a}^1 u^-p du - int_{1-a}^1 u^(1-p) du ]
    def I(e):  # int u^e du over [1-a,1]
        return -np.log1p(-a) if e == -1 else (1 - (1 - a) ** (e + 1)) / (e + 1)
    return 2 / a ** 2 * (I(-p) - I(1 - p))


fails = 0
print("=== A1: M_lin closed form vs Simpson (p x x_e) ===")
maxrd = 0
nonconv = []
for p in PS:
    for x in XE:
        c = mlin_closed(x, p)
        q, n, rc, ok = mlin_quad(x, p)
        rd = abs(c - q) / c
        maxrd = max(maxrd, rd)
        if not ok:
            nonconv.append((p, x, n, rc))
        print(f"p={p:2d} x_e={x:5.2f} closed={c:.8f} simpson={q:.8f} n={n} rel_diff={rd:.2e} {tag(rd < 1e-6)}")
        fails += rd >= 1e-6
print(f"A1 max rel diff closed vs quadrature = {maxrd:.2e}  {tag(maxrd < 1e-6)}; non-converged Simpson cases: {nonconv}")
hand = {(1, 0.1): 1.0536, (1, 0.5): 1.3863, (1, 0.9): 2.5584}
for (p, x), h in hand.items():
    c = mlin_closed(x, p)
    print(f"A1 hand p={p} x_e={x}: hand={h} calc={c:.5f} rel={abs(c-h)/h:.2e} {tag(abs(c-h)/h < 1e-3)}")
    fails += abs(c - h) / h >= 1e-3
for x in XE:
    d2 = abs(mlin_closed(x, 2) - 1 / (1 - x))
    dm = abs(mlin_closed(x, -1) - (1 - x / 2))
    print(f"A1 hand p=2 x_e={x}: |M-1/(1-x)|={d2:.1e}  p=-1: |M-(1-x/2)|={dm:.1e} {tag(max(d2,dm)<1e-9)}")
print("A1 note: p=2 and p=-1 'hand' values are the algebraic simplification of the same closed form; "
      "they check the algebra, the quadrature comparison is the independent check.")

print("\n=== A2: M_par (p x a) ===")
maxrd = 0
maxrd3 = 0
for p in [1, 2, 4]:
    for a in XE:
        q, n, rc, ok = mpar_quad(a, p)
        g = mpar_closed_general(a, p)
        s = f"p={p} a={a:5.2f} simpson={q:.8f} n={n} conv={ok}"
        if p == 1:
            c = mpar_p1(a)
            rd = abs(c - q) / c
            maxrd = max(maxrd, rd)
            s += f" closed_p1={c:.8f} rel_diff={rd:.2e} {tag(rd<1e-6)}"
            fails += rd >= 1e-6
        rd3 = abs(g - q) / g
        maxrd3 = max(maxrd3, rd3)
        s += f" extra_closed={g:.8f} rd={rd3:.1e}"
        print(s)
print(f"A2 max rel diff p=1 closed vs quadrature = {maxrd:.2e}; extra general closed vs quadrature = {maxrd3:.2e} {tag(maxrd3<1e-6)}")
for a, h in [(0.1, 1.0721), (0.5, 1.5452), (0.9, 3.463)]:
    c = mpar_p1(a)
    print(f"A2 hand p=1 a={a}: hand={h} calc={c:.5f} rel={abs(c-h)/h:.2e} {tag(abs(c-h)/h<1e-3)}")
    fails += abs(c - h) / h >= 1e-3

print("\n=== A3: x_e at which M-1 = eps ===")
for kind in ['lin', 'par']:
    for p in [1, 2, 4]:
        for eps in [0.02, 0.05, 0.10]:
            if kind == 'lin':
                f = lambda x: mlin_closed(x, p) - 1 - eps
            elif p == 1:
                f = lambda x: mpar_p1(x) - 1 - eps
            else:
                f = lambda x: mpar_quad(x, p)[0] - 1 - eps
            r = bisect(f, 1e-6, 0.99, extend_limit=0.999999)
            if not r['bracketed']:
                print(f"{kind} p={p} eps={eps}: NO BRACKET flo={r['flo']:.3e} fhi={r['fhi']:.3e} ext fhi={r.get('fhi_ext')}")
                continue
            xr = r['root']
            fo = 2 * eps / p if kind == 'lin' else 1.5 * eps / p
            line = (f"{kind} p={p} eps={eps}: bracket [1e-6,0.99] f=({r['flo']:.3e},{r['fhi']:.3e}) "
                    f"x_e={xr:.6f} first-order={fo:.5f} ratio root/first-order={xr/fo:.4f}")
            if kind == 'lin' and p == 2:
                ex = eps / (1 + eps)
                line += f" exact eps/(1+eps)={ex:.6f} rel={abs(xr-ex)/ex:.1e} {tag(abs(xr-ex)/ex<1e-9)}"
            print(line)
hand3 = {('lin', 1): (0.039, 0.094, 0.176), ('par', 1): (0.029, 0.071, 0.135)}
for (kind, p), hv in hand3.items():
    for eps, h in zip([0.02, 0.05, 0.10], hv):
        f = (lambda x: mlin_closed(x, p) - 1 - eps) if kind == 'lin' else (lambda x: mpar_p1(x) - 1 - eps)
        xr = bisect(f, 1e-6, 0.99)['root']
        print(f"A3 hand {kind} p=1 eps={eps}: hand={h} calc={xr:.5f} rel={abs(xr-h)/h:.3f} {tag(abs(xr-h)/h<0.03)}")
        fails += abs(xr - h) / h >= 0.03
print(f"\nTOTAL FAIL COUNT (A1-A3 checks): {fails}")
