"""A2/A3: thin-skin limit of a rectangular bar by an independent boundary-element method.

What it computes
    In the limit delta -> 0 the current is a surface sheet K(l) that makes the vector
    potential constant on the conductor surface (the same problem as the charge on a
    conducting cylinder of that cross-section).  Then

        R' = kappa / (sigma * delta * P),
        kappa = P * closed-integral(K^2 dl) / (closed-integral(K dl))^2  >= 1.

    1. kappa (the 'edge factor') for the 10 x 100 mm rectangle and for a square.
    2. The logarithmic capacity c of the cross-section (from the same solve), checked
       against the exact values for a thin strip (w/4) and a square (0.59017 * side).
    3. The lower bound  R'_HF >= R_s / (2 pi c),  R_s = 1/(sigma delta), which holds for
       ANY set of parallel-connected conductors of one material inside the envelope
       (derivation in the answer, item A2.5), and its ratio to the solid bar.
    4. How fast the finite-delta volume solver (eddy2d.py) approaches kappa.

Which answer items it supports
    A3 (independent check of the edge factor 1.52-1.56), A2.5 (bound on what any
    non-transposed structure can gain).

Assumptions
    Surface-impedance limit (every conductor dimension >> delta), z-invariant,
    conductors in parallel, mu = mu0.  1-D collocation BEM, piecewise-constant K on
    panels graded geometrically towards the corner, ln-kernel integrated exactly.

Run time: about 1 minute (part 4 dominates).
"""
import math

import numpy as np

from eddy2d import S_AL, S_CU, delta, graded, solve, tensor_cells


def seg_ln(u0, u1, v):
    """Integral of ln(sqrt(u^2+v^2)) du from u0 to u1 (broadcasts)."""
    def G(u):
        r2 = u * u + v * v
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(r2 > 0, 0.5 * u * np.log(np.where(r2 > 0, r2, 1.0)), 0.0)
            at = np.where(v != 0, v * np.arctan(u / np.where(v != 0, v, 1.0)), 0.0)
        return t - u + at
    return G(u1) - G(u0)


def corner_graded(L, hmin, r):
    sizes = []
    h = hmin
    tot = 0.0
    while tot < L:
        sizes.append(h)
        tot += h
        h *= r
    sizes = np.array(sizes) * (L / tot)
    d = np.concatenate([[0.0], np.cumsum(sizes)])
    return (L - d)[::-1]            # fine at the far (corner) end


def bem(a, b, hmin, r):
    """Rectangle 2a x 2b.  Returns (kappa, logarithmic capacity [m], panel count)."""
    xe = corner_graded(a, hmin, r)   # top face y=b, 0<x<a
    ye = corner_graded(b, hmin, r)   # side face x=a, 0<y<b
    nt, ns = xe.size - 1, ye.size - 1
    px = np.concatenate([0.5 * (xe[:-1] + xe[1:]), np.full(ns, a)])
    py = np.concatenate([np.full(nt, b), 0.5 * (ye[:-1] + ye[1:])])
    n = nt + ns
    G = np.zeros((n, n))
    for sx in (1, -1):
        for sy in (1, -1):
            x0, x1 = (xe[:-1], xe[1:]) if sx == 1 else (-xe[1:], -xe[:-1])
            G[:, :nt] += seg_ln(x0[None, :] - px[:, None], x1[None, :] - px[:, None], sy * b - py[:, None])
            y0, y1 = (ye[:-1], ye[1:]) if sy == 1 else (-ye[1:], -ye[:-1])
            G[:, nt:] += seg_ln(y0[None, :] - py[:, None], y1[None, :] - py[:, None], sx * a - px[:, None])
    K = np.linalg.solve(G, np.ones(n))          # potential 1 on the surface
    ln = np.concatenate([np.diff(xe), np.diff(ye)])
    Q = 4 * np.sum(K * ln)                      # total 'charge' = total current
    kappa = 4 * (a + b) * 4 * np.sum(K * K * ln) / Q ** 2
    return kappa, math.exp(1 / Q), n


if __name__ == "__main__":
    print("== 1. edge factor kappa in the limit delta -> 0 (panel refinement study)")
    for a, b, name in ((50e-3, 5e-3, "10 x 100 mm"), (5e-3, 5e-3, "10 x 10 mm (square)")):
        print(name)
        for hmin, r in ((1e-6, 1.5), (1e-8, 1.4), (1e-10, 1.3), (1e-12, 1.25), (1e-14, 1.2)):
            k, c, n = bem(a, b, hmin * b, r)
            print(f"   hmin/b={hmin:7.0e} ratio={r:4.2f} panels={n:4d}  kappa={k:.4f}  capacity={c*1e3:.4f} mm")

    print("\n== 2. capacity checks")
    print("   thin strip 100 mm x 1 um, expect c -> w/4 = 25 mm:        ", bem(50e-3, 0.5e-6, 1e-12, 1.3)[1] * 1e3)
    print("   square side 10 mm, expect c = 0.59017*side = 5.9017 mm:   ", bem(5e-3, 5e-3, 1e-13, 1.25)[1] * 1e3)

    print("\n== 3. lower bound for any parallel-connected conductor set inside the 10 x 100 mm envelope")
    kap, c, _ = bem(50e-3, 5e-3, 1e-13, 1.25)
    P = 0.22
    print(f"   c = {c*1e3:.4f} mm, 2*pi*c = {2*math.pi*c*1e3:.3f} mm, kappa = {kap:.4f}, P/kappa = {P/kap*1e3:.3f} mm")
    print(f"   bound / solid-bar thin-skin resistance (same material) = {(P/kap)/(2*math.pi*c):.4f}")
    print(f"   best conceivable Al structure / solid Cu bar            >= {math.sqrt(S_CU/S_AL)*(P/kap)/(2*math.pi*c):.4f}")

    print("\n== 4. finite-delta volume solver vs the delta -> 0 limit (solid Cu)")
    for a, b, name, kap in ((5e-3, 5e-3, "square 10x10", bem(5e-3, 5e-3, 1e-13, 1.25)[0]),
                            (50e-3, 5e-3, "bar 10x100", bem(50e-3, 5e-3, 1e-13, 1.25)[0])):
        P = 4 * (a + b)
        for f in (1e4, 1e5, 1e6, 1e7):
            d = delta(S_CU, f)
            xe = graded(a, d / 6, 1.22, 1e-3, "hi")
            ye = graded(b, d / 6, 1.22, 1e-3, "hi")
            s = solve(tensor_cells(xe, ye, S_CU), f)
            print(f"   {name} f={f:.0e} b/delta={b/d:7.1f} N={s['n']:5d} edge factor={s['R']*S_CU*d*P:.4f}"
                  f"  (BEM limit {kap:.4f}, deficit {kap - s['R']*S_CU*d*P:+.4f})", flush=True)
