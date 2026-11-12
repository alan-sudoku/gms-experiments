"""Reviewer check R1: an independently written 2-D volume-integral eddy-current solver.

Purpose
    Re-derive the writer's key 2-D numbers (answer A3.3, A2.6) with code that shares no
    lines with eddy2d.py, and add one comparison the writer did not make: a copper tube
    of the SAME MASS as the aluminium lattice and the aluminium tube (equal mass AND equal
    envelope), plus a copper tube with a 1.6 delta_Cu wall.

Formulation (same physics as the writer's, different implementation)
    For z-invariant conductors in parallel:  J/sigma - j*omega*(mu0/2pi) * int J ln|r-r'| dA' = V'.
    Piecewise-constant J on rectangular cells, collocation at cell centres.  Differences from
    eddy2d.py: (i) the self term is computed by polar integration over the cell (1-D Gauss
    quadrature on the angle), not by the closed-form antiderivative; (ii) other cells are
    integrated numerically: near cells split along their long side into pieces of aspect
    <= 2 with 4 x 4 Gauss points each, far cells with 2 x 2 Gauss points, not in
    closed form; (iii) own mesh grading; (iv) own quarter-symmetry image handling;
    (v) R' from the dissipated power, P/|I|^2 (peak phasors, so time-average P = sum
    |J|^2 a/(2 sigma) and P = R'|I|^2/2), and separately Re(V'/I).
    Validation: isolated round wire against the exact Bessel solution.

Assumptions
    Isolated straight conductor (return at infinity), mu = mu0, 20 C conductivities as in
    the prompt (Cu 5.96e7, Al 3.77e7 S/m), densities Cu 8960 and Al 2700 kg/m^3.
    numpy only.  Run: python3 r1_vie_independent.py  (a few minutes).
"""
import math
import time

import numpy as np

MU0 = 4e-7 * math.pi
S_CU, S_AL = 5.96e7, 3.77e7
RHO_CU, RHO_AL = 8960.0, 2700.0
GX8, GW8 = np.polynomial.legendre.leggauss(8)
GX2, GW2 = np.polynomial.legendre.leggauss(2)
GX50, GW50 = np.polynomial.legendre.leggauss(50)


def delta(s, f):
    return math.sqrt(1 / (math.pi * f * MU0 * s))


def self_term(hx, hy):
    """int over a hx x hy rectangle of ln(r), r measured from its centre (polar integration)."""
    a, b = hx / 2, hy / 2
    tot = 0.0
    for (t0, t1, edge) in ((0.0, math.atan2(b, a), "x"), (math.atan2(b, a), math.pi / 2, "y")):
        th = 0.5 * (t1 - t0) * (GX50 + 1) + t0
        wt = 0.5 * (t1 - t0) * GW50
        R = a / np.cos(th) if edge == "x" else b / np.sin(th)
        tot += np.sum(wt * (0.5 * R * R * np.log(R) - 0.25 * R * R))
    return 4 * tot


def ln_int(xi, yi, cx, cy, hx, hy, gx, gw):
    """int over cells (centres cx, cy, sizes hx, hy) of ln|r_i - r'| by Gauss product rule."""
    acc = np.zeros(np.broadcast(xi, cx).shape)
    for p, wp in zip(gx, gw):
        for q, wq in zip(gx, gw):
            X = cx + 0.5 * hx * p
            Y = cy + 0.5 * hy * q
            acc += wp * wq * 0.5 * np.log((xi - X) ** 2 + (yi - Y) ** 2)
    return acc * 0.25 * hx * hy


GX4, GW4 = np.polynomial.legendre.leggauss(4)


def ln_int_near(xi, yi, cx, cy, hx, hy):
    """As ln_int, for near pairs: each source cell is split along its long side into
    ceil(2*aspect) pieces (at most 256), each integrated with 4 x 4 Gauss points, so that
    high-aspect boundary-layer cells are integrated accurately."""
    along_x = hx >= hy
    long_ = np.where(along_x, hx, hy)
    short = np.where(along_x, hy, hx)
    k = np.minimum(256, np.ceil(2 * long_ / short)).astype(int)
    acc = np.zeros(xi.shape)
    for s in range(int(k.max())):
        act = s < k
        if not act.any():
            break
        piece = long_ / k
        # centre of piece s along the long axis
        off = -0.5 * long_ + (s + 0.5) * piece
        pcx = np.where(along_x, cx + off, cx)
        pcy = np.where(along_x, cy, cy + off)
        phx = np.where(along_x, piece, hx)
        phy = np.where(along_x, hy, piece)
        val = ln_int(xi, yi, pcx, pcy, phx, phy, GX4, GW4)
        acc += np.where(act, val, 0.0)
    return acc


def edges(L, h0, ratio, hmax):
    """Edges on [0, L], finest (h0) at L, geometric growth inwards, capped at hmax."""
    s = []
    h = h0
    while sum(s) < L:
        s.append(min(h, hmax))
        h *= ratio
    s = np.array(s) * L / sum(s)
    return np.concatenate([[0.0], np.cumsum(s[::-1])])


def edges_both(L, h0, ratio, hmax):
    """Edges on [0, L], finest (h0) at BOTH ends."""
    left = L / 2 - edges(L / 2, h0, ratio, hmax)[::-1]       # finest at 0
    return np.concatenate([left, L - left[::-1][1:]])


def cells_from(xe, ye, keep=None):
    X0, Y0 = np.meshgrid(xe[:-1], ye[:-1], indexing="ij")
    X1, Y1 = np.meshgrid(xe[1:], ye[1:], indexing="ij")
    cx, cy = (0.5 * (X0 + X1)).ravel(), (0.5 * (Y0 + Y1)).ravel()
    hx, hy = (X1 - X0).ravel(), (Y1 - Y0).ravel()
    if keep is not None:
        k = keep(cx, cy)
        cx, cy, hx, hy = cx[k], cy[k], hx[k], hy[k]
    return cx, cy, hx, hy


def solve_quarter(cells, sigma, f):
    """cells in x>0, y>0; current density even in x and y.  Returns (R_loss, R_V) [ohm/m]."""
    cx, cy, hx, hy = cells
    n = cx.size
    w = 2 * math.pi * f
    G = np.zeros((n, n))
    size = np.maximum(hx, hy)
    for sx in (1, -1):
        for sy in (1, -1):
            icx, icy = sx * cx, sy * cy
            for s0 in range(0, n, 500):
                s1 = min(n, s0 + 500)
                xi, yi = cx[s0:s1, None], cy[s0:s1, None]
                dist = np.hypot(xi - icx[None, :], yi - icy[None, :])
                near = dist < 3.0 * np.maximum(size[s0:s1, None], size[None, :])
                blk = ln_int(xi, yi, icx[None, :], icy[None, :], hx[None, :], hy[None, :], GX2, GW2)
                ii, jj = np.nonzero(near)
                if ii.size:
                    blk[ii, jj] = ln_int_near(xi[ii, 0], yi[ii, 0], icx[jj], icy[jj], hx[jj], hy[jj])
                if sx == 1 and sy == 1:
                    d = np.arange(s0, s1)
                    blk[d - s0, d] = [self_term(hx[k], hy[k]) for k in d]
                G[s0:s1] += blk
    M = (-1j * w * MU0 / (2 * math.pi)) * G
    M[np.arange(n), np.arange(n)] += 1 / sigma
    J = np.linalg.solve(M, np.ones(n, complex))
    a = hx * hy
    I = 4 * np.sum(J * a)
    P = 4 * np.sum(np.abs(J) ** 2 * a) / (2 * sigma)
    return P / (0.5 * abs(I) ** 2), (1 / I).real


def bar(a, b, sigma, f, lvl):
    d = delta(sigma, f)
    h0, hmax = d / (4, 8)[lvl], (1.0e-3, 0.6e-3)[lvl]
    return cells_from(edges(a, h0, 1.25, hmax), edges(b, h0, 1.25, hmax))


def tube(a, b, wall, sigma, f, lvl):
    d = delta(sigma, f)
    h0, hmax = min(d, wall) / (4, 8)[lvl], (1.0e-3, 0.6e-3)[lvl]
    xe = np.concatenate([edges(a - wall, h0, 1.25, hmax), (a - wall) + edges_both(wall, h0, 1.25, hmax)[1:]])
    ye = np.concatenate([edges(b - wall, h0, 1.25, hmax), (b - wall) + edges_both(wall, h0, 1.25, hmax)[1:]])
    return cells_from(xe, ye, keep=lambda x, y: (x > a - wall) | (y > b - wall))


def bessel_ratio(r, sigma, f):
    """Exact R_ac/R_dc of a round wire: Re[(k r/2) J0(k r)/J1(k r)], k = (1-j)/delta (series)."""
    z = (1 - 1j) / delta(sigma, f) * r
    q = -(z * z) / 4
    term, j0, j1s = 1 + 0j, 1 + 0j, 1 + 0j
    for k in range(1, 300):
        term *= q / (k * k)
        j0 += term
        j1s += term / (k + 1)
    return (z / 2 * j0 / (j1s * z / 2)).real


def wall_for_area(Wd, Td, area):
    """Uniform wall w with W*T - (W-2w)(T-2w) = area."""
    return ((Wd + Td) - math.sqrt((Wd + Td) ** 2 - 4 * area)) / 4


if __name__ == "__main__":
    print("== V. round Cu wire r = 2 mm, uniform staircase mesh, vs exact Bessel")
    r0 = 2e-3
    for f in (1e4, 5e4):
        for nn in (32, 48):
            e = np.linspace(0, r0, nn + 1)
            c = cells_from(e, e, keep=lambda x, y: x * x + y * y < r0 * r0)
            area = 4 * np.sum(c[2] * c[3])
            Rl, Rv = solve_quarter(c, S_CU, f)
            print(f"   f={f:.0f} n={nn} N={c[0].size}: Rac/Rdc={Rl*S_CU*area:.4f} (V-based {Rv*S_CU*area:.4f})"
                  f"  exact={bessel_ratio(r0, S_CU, f):.4f}", flush=True)

    a, b = 50e-3, 5e-3
    A = 4 * a * b
    w_lat = wall_for_area(2 * a, 2 * b, 0.3 * A)                    # Al tube, equal mass to lattice
    area_cu_eq = 0.3 * A * RHO_AL / RHO_CU                         # Cu area with the lattice's mass
    w_cu_eq = wall_for_area(2 * a, 2 * b, area_cu_eq)
    print(f"\n   Al tube wall (area 300 mm2) = {w_lat*1e3:.4f} mm;  Cu tube of equal mass: area "
          f"{area_cu_eq*1e6:.1f} mm2, wall {w_cu_eq*1e3:.4f} mm; mass {0.3*A*RHO_AL:.3f} kg/m")
    writer = {("solid Cu", 1e4): 178.44, ("solid Cu", 1e5): 564.67, ("lattice 0.3 sAl (homog.)", 1e4): 414.46,
              ("lattice 0.3 sAl (homog.)", 1e5): 1294.26, ("Al tube equal mass", 1e4): 212.12,
              ("Al tube equal mass", 1e5): 709.40}
    for f in (1e4, 1e5):
        print(f"\n== f = {f:.0f} Hz  (10 x 100 mm envelope, isolated)")
        cases = [("solid Cu", lambda l: bar(a, b, S_CU, f, l), S_CU, RHO_CU * A),
                 ("lattice 0.3 sAl (homog.)", lambda l: bar(a, b, 0.3 * S_AL, f, l), 0.3 * S_AL, 0.3 * A * RHO_AL),
                 ("Al tube equal mass", lambda l: tube(a, b, w_lat, S_AL, f, l), S_AL, 0.3 * A * RHO_AL),
                 ("Cu tube equal mass", lambda l: tube(a, b, w_cu_eq, S_CU, f, l), S_CU, area_cu_eq * RHO_CU),
                 ("Cu tube wall 1.6 delta_Cu", lambda l: tube(a, b, 1.6 * delta(S_CU, f), S_CU, f, l), S_CU,
                  (A - (2 * a - 3.2 * delta(S_CU, f)) * (2 * b - 3.2 * delta(S_CU, f))) * RHO_CU)]
        for name, mk, sg, mass in cases:
            out = []
            for lvl in (0, 1):
                t0 = time.time()
                c = mk(lvl)
                Rl, Rv = solve_quarter(c, sg, f)
                out.append((c[0].size, Rl, Rv, time.time() - t0))
            (n0, R0, V0, _), (n1, R1, V1, t1) = out
            wv = writer.get((name, f))
            ws = f"   writer {wv:.2f} ({(R1*1e6/wv-1)*100:+.2f} %)" if wv else ""
            print(f"   {name:26s} mass {mass:5.2f} kg/m  N={n0}/{n1}: R'={R0*1e6:8.2f} / {R1*1e6:8.2f} uOhm/m "
                  f"(V-based fine {V1*1e6:8.2f}){ws}  [{t1:.0f}s]", flush=True)
