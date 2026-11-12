"""2-D eddy-current solver for long straight conductors (shared module for Prompt 1a).

What it computes
    AC resistance per metre R' of z-invariant, non-magnetic conductors of arbitrary
    cross-section built from rectangular cells, all connected in parallel.
    Run directly (`python3 eddy2d.py`) it prints three validation cases (V1-V3).

Which answer items it supports
    Every numerical result in A2 and A3 (imported by the other scripts in this folder).

Method (volume integral equation / filament method, cf. Silvester 1967, Weeks et al. 1979)
    J(r)/sigma(r) + j*omega*A(r) = V'            (V' = common voltage drop per metre)
    A(r) = -(mu0/2pi) * Integral J(r') ln|r - r'| dA'      (open boundary is exact)
    Piecewise-constant J on rectangular cells, collocation at cell centres, the
    ln-kernel integrated EXACTLY over every source rectangle (closed form F below).
    Quarter symmetry (J even in x and y, or odd for go/return pairs) via image cells.

Assumptions
    Infinitely long straight conductor, sinusoidal steady state, mu = mu0, linear
    isotropic conductivity, no displacement current, conductivities at 20 C
    (Cu 5.96e7 S/m, Al 3.77e7 S/m as given in the prompt), return conductor at
    infinity unless a script says otherwise.

Dependencies: numpy only.  All lengths in metres.
"""
import math
import time

import numpy as np

MU0 = 4e-7 * math.pi
S_CU = 5.96e7
S_AL = 3.77e7
T0 = 298.15          # K, reference temperature used for Sigma_dot = P/T0
RHO_CU = 8960.0      # kg/m3
RHO_AL = 2700.0      # kg/m3


def delta(sigma, f):
    """Skin depth sqrt(1/(pi f mu0 sigma))."""
    return math.sqrt(1.0 / (math.pi * f * MU0 * sigma))


def F(x, y):
    """Indefinite double integral of ln(sqrt(x^2+y^2)) dx dy."""
    r2 = x * x + y * y
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = np.where(r2 > 0, 0.5 * x * y * np.log(np.where(r2 > 0, r2, 1.0)), 0.0)
        t2 = np.where(x != 0, 0.5 * x * x * np.arctan(y / np.where(x != 0, x, 1.0)), 0.0)
        t3 = np.where(y != 0, 0.5 * y * y * np.arctan(x / np.where(y != 0, y, 1.0)), 0.0)
    return t1 - 1.5 * x * y + t2 + t3


def rect_ln_integral(xi, yi, x0, x1, y0, y1):
    """Integral over rectangle [x0,x1]x[y0,y1] of ln|r_i - r'|; broadcasts."""
    u0 = x0 - xi
    u1 = x1 - xi
    v0 = y0 - yi
    v1 = y1 - yi
    return F(u1, v1) - F(u0, v1) - F(u1, v0) + F(u0, v0)


def build_M(cells, f, sym=(1, 1), chunk=400):
    """System matrix M with  M @ J = V' (per cell), plus cell areas and the image list.

    cells: dict with arrays x0,x1,y0,y1,sigma for the quadrant x>0,y>0.
    sym=(sx,sy): +1 -> J even under x->-x (resp. y->-y); -1 -> odd; 0 -> no image."""
    x0, x1, y0, y1, sg = (np.asarray(cells[k], float) for k in ("x0", "x1", "y0", "y1", "sigma"))
    n = x0.size
    xc = 0.5 * (x0 + x1)
    yc = 0.5 * (y0 + y1)
    area = (x1 - x0) * (y1 - y0)
    w = 2 * math.pi * f
    images = [(1.0, 1, 1)]
    sx, sy = sym
    if sx:
        images.append((float(sx), -1, 1))
    if sy:
        images.append((float(sy), 1, -1))
    if sx and sy:
        images.append((float(sx * sy), -1, -1))
    G = np.empty((n, n))
    for s in range(0, n, chunk):
        e = min(n, s + chunk)
        xi = xc[s:e, None]
        yi = yc[s:e, None]
        acc = np.zeros((e - s, n))
        for sgn, mx, my in images:
            ax0, ax1 = (x0, x1) if mx == 1 else (-x1, -x0)
            ay0, ay1 = (y0, y1) if my == 1 else (-y1, -y0)
            acc += sgn * rect_ln_integral(xi, yi, ax0[None, :], ax1[None, :], ay0[None, :], ay1[None, :])
        G[s:e] = acc
    M = (-1j * w * MU0 / (2 * math.pi)) * G
    del G
    M[np.arange(n), np.arange(n)] += 1.0 / sg
    return M, area, sg, images, xc, yc


def solve(cells, f, sym=(1, 1), chunk=400, rhs=None):
    """Solve for J with all cells in parallel.

    rhs: optional per-cell driving voltage per metre (default 1 V/m everywhere).
    Returns dict with R = Re(V'/I) [ohm/m], R_loss = P/|I|^2, X, I, J, n.
    For sym with a -1 entry (go/return pair) I and P refer to the 'go' conductor."""
    M, area, sg, images, xc, yc = build_M(cells, f, sym, chunk)
    n = area.size
    J = np.linalg.solve(M, np.ones(n, complex) if rhs is None else np.asarray(rhs, complex))
    npos = sum(1 for sgn, _, _ in images if sgn > 0)     # copies carrying 'go' current
    I = npos * np.sum(J * area)
    P = npos * np.sum(np.abs(J) ** 2 * area / sg)
    Z = 1.0 / I
    return dict(R=Z.real, X=Z.imag, R_loss=P / abs(I) ** 2, I=I, J=J, n=n,
                xc=xc, yc=yc, area=area)


# ---------------------------------------------------------------- meshes
def graded(L, h0, r, hmax, ends="hi"):
    """Cell edges on [0,L], geometrically graded (first size h0, ratio r, cap hmax)
    towards the 'hi' end, the 'lo' end, or 'both' ends."""
    if ends == "both":
        half = graded(L / 2, h0, r, hmax, "hi")
        return np.concatenate([(L / 2 - half)[::-1], (L / 2 + half)[1:]])
    sizes = []
    h = h0
    tot = 0.0
    while tot < L * (1 - 1e-12):
        hh = min(h, hmax)
        sizes.append(hh)
        tot += hh
        h *= r
    sizes = np.array(sizes) * (L / tot)
    dist = np.concatenate([[0.0], np.cumsum(sizes)])     # distance from the graded end
    if ends == "hi":
        return (L - dist)[::-1]
    return dist


def tensor_cells(xe, ye, sigma, mask=None):
    """Cells of a tensor grid; mask(xc, yc) -> bool selects which cells are metal."""
    X0, Y0 = np.meshgrid(xe[:-1], ye[:-1], indexing="ij")
    X1, Y1 = np.meshgrid(xe[1:], ye[1:], indexing="ij")
    c = dict(x0=X0.ravel(), x1=X1.ravel(), y0=Y0.ravel(), y1=Y1.ravel())
    if mask is not None:
        keep = mask(0.5 * (c["x0"] + c["x1"]), 0.5 * (c["y0"] + c["y1"]))
        c = {k: v[keep] for k, v in c.items()}
    c["sigma"] = np.full(c["x0"].size, float(sigma))
    return c


MESH_H0_DIV = (3, 6, 10)            # first cell = delta / this   (lvl 0, 1, 2)
MESH_RATIO = (1.35, 1.22, 1.15)
MESH_HMAX = (2e-3, 1e-3, 0.6e-3)


def solid_bar(a, b, sigma, f, lvl=1):
    """Quarter of a solid 2a x 2b bar. lvl 0/1/2 = coarse/medium/fine mesh."""
    d = delta(sigma, f)
    h0, r, hmax = d / MESH_H0_DIV[lvl], MESH_RATIO[lvl], MESH_HMAX[lvl]
    return tensor_cells(graded(a, h0, r, hmax, "hi"), graded(b, h0, r, hmax, "hi"), sigma)


def tube(a, b, wall, sigma, f, lvl=1):
    """Quarter of a hollow rectangular tube, outer 2a x 2b, uniform wall."""
    d = delta(sigma, f)
    h0, r, hmax = min(d, wall) / MESH_H0_DIV[lvl], MESH_RATIO[lvl], MESH_HMAX[lvl]
    xin = graded(a - wall, h0, r, hmax, "hi")
    yin = graded(b - wall, h0, r, hmax, "hi")
    ww = graded(wall, h0, r, hmax, "both")
    xe = np.concatenate([xin, (a - wall) + ww[1:]])
    ye = np.concatenate([yin, (b - wall) + ww[1:]])
    return tensor_cells(xe, ye, sigma, mask=lambda x, y: (x > a - wall) | (y > b - wall))


def strand_array(a, b, nx, ny, fill, sigma, nsub=1):
    """Quarter of a bundle of (2nx) x (2ny) square strands on a square pitch filling the
    2a x 2b envelope; metal area fraction = fill; each strand split into nsub x nsub cells.
    Returns (cells, strand side t, pitch)."""
    px, py = a / nx, b / ny
    assert abs(px - py) < 1e-12
    t = math.sqrt(fill) * px
    cx = (np.arange(nx) + 0.5) * px
    cy = (np.arange(ny) + 0.5) * py
    sub = (np.arange(nsub + 1) / nsub - 0.5) * t
    xe0 = (cx[:, None] + sub[None, :-1]).ravel()
    xe1 = (cx[:, None] + sub[None, 1:]).ravel()
    ye0 = (cy[:, None] + sub[None, :-1]).ravel()
    ye1 = (cy[:, None] + sub[None, 1:]).ravel()
    X0, Y0 = np.meshgrid(xe0, ye0, indexing="ij")
    X1, Y1 = np.meshgrid(xe1, ye1, indexing="ij")
    c = dict(x0=X0.ravel(), x1=X1.ravel(), y0=Y0.ravel(), y1=Y1.ravel())
    c["sigma"] = np.full(c["x0"].size, float(sigma))
    return c, t, px


# ---------------------------------------------------------------- analytic helpers
def dowell_skin(xi):
    """Claim A's factor xi*(sinh2xi+sin2xi)/(cosh2xi-cos2xi):
    R_ac/R_dc of a foil of thickness xi*delta with tangential H on ONE face only."""
    return xi * (math.sinh(2 * xi) + math.sin(2 * xi)) / (math.cosh(2 * xi) - math.cos(2 * xi))


def bessel_j01(z):
    """J0(z), J1(z) by power series (complex z, |z| < ~15)."""
    q = -(z * z) / 4
    term = 1.0 + 0j
    j0 = term
    j1 = term
    for k in range(1, 200):
        term *= q / (k * k)
        j0 += term
        j1 += term / (k + 1)
        if abs(term) < 1e-18 * abs(j0):
            break
    return j0, j1 * z / 2


def round_wire_ratio(a, sigma, f):
    """Exact R_ac/R_dc of an isolated round wire of radius a."""
    k = (1 - 1j) / delta(sigma, f)
    j0, j1 = bessel_j01(k * a)
    return (k * a / 2 * j0 / j1).real


def _Fx(x, y):
    """d/dx of F(x, y) = integral of ln(sqrt(x^2+y^2)) dy."""
    r2 = x * x + y * y
    with np.errstate(divide="ignore", invalid="ignore"):
        t1 = np.where(r2 > 0, 0.5 * y * np.log(np.where(r2 > 0, r2, 1.0)), 0.0)
        t2 = np.where(x != 0, x * np.arctan(y / np.where(x != 0, x, 1.0)), 0.0)
    return t1 - y + t2


def uniform_current_h2_factor(W, T, n=400):
    """Mean of |H|^2 over a W x T rectangle carrying uniform current density, divided by
    the 1-D value I^2/(12 W^2) (field parallel to the wide face only, H = J*y).
    Returns (parallel-component part, normal-component part); their sum is the factor
    by which the 1-D estimate of strand proximity loss in a transposed bundle is low."""
    a, b = W / 2, T / 2
    m = max(8, int(n * T / W))
    xs = (np.arange(n) + 0.5) * W / n - a
    ys = (np.arange(m) + 0.5) * T / m - b
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    u0, u1, v0, v1 = -a - X, a - X, -b - Y, b - Y
    dPdx = -(_Fx(u1, v1) - _Fx(u0, v1) - _Fx(u1, v0) + _Fx(u0, v0))
    dPdy = -(_Fx(v1, u1) - _Fx(v0, u1) - _Fx(v1, u0) + _Fx(v0, u0))
    J = 1.0 / (W * T)
    Hx = -(J / (2 * math.pi)) * dPdy
    Hy = (J / (2 * math.pi)) * dPdx
    one_d = 1.0 / (12 * W * W)
    return float(np.mean(Hx ** 2) / one_d), float(np.mean(Hy ** 2) / one_d)


def run(label, cells, f, **kw):
    """solve() with a one-line printed report."""
    t = time.time()
    s = solve(cells, f, **kw)
    print(f"{label:60s} N={s['n']:5d}  R'={s['R']*1e6:9.2f} uOhm/m  "
          f"(loss-based {s['R_loss']*1e6:9.2f})  [{time.time()-t:5.1f}s]", flush=True)
    return s


if __name__ == "__main__":
    a, b = 50e-3, 5e-3
    print("== V1: closed-form kernel vs brute-force midpoint quadrature")
    rng = np.random.default_rng(1)
    for _ in range(3):
        x0, y0 = rng.uniform(-1, 1, 2)
        dx, dy = rng.uniform(0.05, 0.7, 2)
        xi, yi = rng.uniform(-1.5, 1.5, 2)
        m = 1500
        xs = x0 + (np.arange(m) + 0.5) * dx / m
        ys = y0 + (np.arange(m) + 0.5) * dy / m
        num = np.sum(0.5 * np.log((xs[:, None] - xi) ** 2 + (ys[None, :] - yi) ** 2)) * dx * dy / m / m
        print(f"   exact {float(rect_ln_integral(xi, yi, x0, x0+dx, y0, y0+dy)):+.8f}   midpoint {num:+.8f}")
    print("== V2: DC limit, solid Cu 10x100 mm at 1 Hz:  expect", 1 / (S_CU * 4 * a * b) * 1e6, "uOhm/m")
    run("   solid Cu 1 Hz", solid_bar(a, b, S_CU, 1e3, 0), 1.0)
    print("== V3: round Cu wire radius 2 mm (staircase mesh) vs exact Bessel solution")
    rw = 2e-3
    for f in (1e4, 5e4):
        for nn in (20, 40, 64):
            e = np.linspace(0, rw, nn + 1)
            c = tensor_cells(e, e, S_CU, mask=lambda x, y: x * x + y * y < rw * rw)
            area = 4 * np.sum((c["x1"] - c["x0"]) * (c["y1"] - c["y0"]))
            s = solve(c, f)
            print(f"   f={f:8.0f} a/delta={rw/delta(S_CU,f):5.2f} n={nn:3d} N={s['n']:5d} "
                  f"Rac/Rdc numeric={s['R']*S_CU*area:7.4f} (loss {s['R_loss']*S_CU*area:7.4f}) "
                  f"exact={round_wire_ratio(rw, S_CU, f):7.4f}")
