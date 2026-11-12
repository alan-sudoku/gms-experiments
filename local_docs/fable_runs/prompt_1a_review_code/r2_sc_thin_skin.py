"""Reviewer check R2: thin-skin edge factor kappa and logarithmic capacity of a rectangle
by an exact Schwarz-Christoffel map (independent of the writer's BEM in a2_hf_limit_bem.py).

Purpose
    The writer reports, for the 10 x 100 mm rectangle in the limit delta -> 0,
    kappa = 1.5613 (R' = kappa/(sigma*delta*P)) and capacity c = 29.7646 mm, hence the
    bound ratio (P/kappa)/(2*pi*c) = 0.7535 and 0.9474 for Al vs Cu.  This script
    recomputes these with a different method.

Method
    The exterior of the unit disk maps onto the exterior of a rectangle by
        f'(w) = C * w^-2 * prod_k (w - w_k)^(1/2),  w_k = e^{+-i th}, e^{i(pi +- th)}
    (each corner has exterior angle 3*pi/2, exponent +1/2; f(w) ~ C*w at infinity, so the
    logarithmic capacity is c = C).  On |w| = 1, |f'| = C * prod |e^{it} - w_k|^(1/2).
    Side lengths are integrals of |f'| over the arcs between prevertices; th is solved so
    that the side ratio is 10:1, then C is fixed by the 100 mm side.
    Thin-skin current: the flux function is A = const on the conductor and
    -(mu0 I/2pi) ln|Phi| outside (Phi = inverse map), so the surface current density is
    K = (I/2pi)|Phi'| = (I/2pi)/|f'(e^{it})| and
        kappa = P * closed-int K^2 dl / (closed-int K dl)^2 = P * int_0^{2pi} dt/|f'| / (2pi)^2.
    The 1/sqrt singularities at the prevertices are removed by the substitution
    t = t_k + s^2 near each prevertex (Gauss-Legendre on each arc piece).

Assumptions
    Surface-impedance (thin-skin) limit, z-invariant isolated conductor, mu = mu0.
    numpy only.  Run: python3 r2_sc_thin_skin.py  (about one second).
"""
import math

import numpy as np

XG, WG = np.polynomial.legendre.leggauss(200)


def absfp(t, th):
    """|f'(e^{it})| / C on the unit circle."""
    z = np.exp(1j * t)
    pv = [th, -th, math.pi - th, math.pi + th]
    return np.prod([np.abs(z - np.exp(1j * p)) ** 0.5 for p in pv], axis=0)


def arc_int(fun, t0, t1):
    """Integral over (t0, t1) of fun(t), where fun may have |t - t0|^(+-1/2) and
    |t - t1|^(+-1/2) behaviour at the ends: split at the midpoint, substitute t = t_end +- s^2."""
    tm = 0.5 * (t0 + t1)
    tot = 0.0
    for te, sgn in ((t0, 1), (t1, -1)):
        smax = math.sqrt(abs(tm - te))
        s = 0.5 * smax * (XG + 1)
        ws = 0.5 * smax * WG
        t = te + sgn * s * s
        tot += np.sum(ws * fun(t) * 2 * s)
    return tot


def geometry(th):
    """Side lengths (in units of C): arc (-th, th) maps to one side, (th, pi - th) to the other."""
    L1 = arc_int(lambda t: absfp(t, th), -th, th)
    L2 = arc_int(lambda t: absfp(t, th), th, math.pi - th)
    return L1, L2


def solve_th(ratio):
    """th such that L2/L1 = ratio (bisection; ratio > 1 means the long side is (th, pi - th))."""
    lo, hi = 1e-6, math.pi / 4
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        L1, L2 = geometry(mid)
        if L2 / L1 > ratio:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def rect(long_side, short_side):
    th = solve_th(long_side / short_side)
    L1, L2 = geometry(th)
    C = long_side / L2
    P = 2 * (long_side + short_side)
    inv = 2 * (arc_int(lambda t: 1 / absfp(t, th), -th, th) + arc_int(lambda t: 1 / absfp(t, th), th, math.pi - th))
    kappa = P * inv / C / (2 * math.pi) ** 2
    return C, kappa, th, (L1 * C, L2 * C)


if __name__ == "__main__":
    S_CU, S_AL = 5.96e7, 3.77e7
    C, k, th, sides = rect(10.0, 10.0)
    print(f"square 10 x 10 mm: capacity {C:.5f} mm (exact Gamma(1/4)^2/(4 pi^1.5)*10 = "
          f"{math.gamma(0.25)**2/(4*math.pi**1.5)*10:.5f}); kappa {k:.4f}  (writer BEM 1.2736)")
    C, k, th, sides = rect(100.0, 10.0)
    P = 220.0
    print(f"rectangle 100 x 10 mm: sides {sides[1]:.4f} x {sides[0]:.4f} mm, prevertex angle {th:.6f} rad")
    print(f"   capacity c = {C:.4f} mm   (writer BEM 29.7646)")
    print(f"   kappa      = {k:.4f}      (writer BEM 1.5613)")
    print(f"   bound / solid bar, same metal = (P/kappa)/(2 pi c) = {(P/k)/(2*math.pi*C):.4f}  (writer 0.7535)")
    print(f"   bound for any Al structure / solid Cu bar = {math.sqrt(S_CU/S_AL)*(P/k)/(2*math.pi*C):.4f}  (writer 0.9474)")
    C, k, th, sides = rect(100.0, 0.01)
    print(f"thin strip 100 x 0.01 mm: capacity {C:.4f} mm (expect -> 25), kappa {k:.3f}")
