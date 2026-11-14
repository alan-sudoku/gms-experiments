"""Shared baseline inputs, numerical helpers and the C1/C3/C4/C8 functions.

Purpose: importable module for rows C1-C17 and for later rows E1-E5, D6.
Spec rows: C1, C3, C4, C8 (functions); numerical rules of plan 3.2 (helpers).
Assumptions: all inputs are the planner's MEMORY inputs (M02..M08, M14..M16,
M24, M25); everything here is a claim at level `derived` (unverified).
Units: lives in years unless stated; stresses in MPa; lengths in m unless named.

Run directly (`.venv/bin/python c_common.py`) to print C1's sigma_a0.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# ---- conventions ----
YR = 3.15576e7            # s
UM_PER_YR = 3.16881e-14   # m/s
KSI = 6.894757            # MPa

# ---- MEMORY inputs ----
SIGMA_F = 900.0           # M02 MPa
B_EXP = -0.102            # M03
M_EXP = -1.0 / B_EXP      # 9.804
N0 = 5e8                  # M04
RHO_M = 2780.0            # M06 kg/m3
ISO_LIMITS = [("C2", 0.6), ("C3", 2.0), ("C4", 5.0), ("C5", 10.0)]  # M08, g/(m2 yr)
Y_GEOM = 2 * 1.12 / math.pi   # M15
DA_DN_TH = 1e-10          # M16 m/cycle
PF_GRID = [1, 3, 10, 30]  # M24

# ---- C1 ----
def sigma_a0(sigma_f=SIGMA_F, b=B_EXP, n0=N0):
    """C1: sigma_a0 = sigma_f' * (2*N0)^b  (MPa)."""
    return sigma_f * (2.0 * n0) ** b


def tau0_years(nu_hz, n0=N0):
    """C1: air life tau0 = N0/nu in years."""
    return n0 / nu_hz / YR


# ---- C3 ----
def t_c_years(kind, size_m, r_um_yr, n_s=1):
    """C3: recession-through time in years. kind 'wall': h0/(n_s r); 'strut': d0/(2 r)."""
    r = r_um_yr * 1e-6  # m/yr
    if kind == "wall":
        return size_m / (n_s * r)
    if kind == "strut":
        return size_m / (2.0 * r)
    raise ValueError(kind)


def mass_loss_g_m2_yr(r_um_yr):
    """C3: mass-loss rate r*rho_m in g/(m2 yr)."""
    return r_um_yr * 1e-6 * RHO_M * 1e3


def iso_class(rate):
    """C3 class placement under M08."""
    for name, lim in ISO_LIMITS:
        if rate <= lim:
            return name
    return "CX"


# ---- C4 (closed form) ----
def tau_c_over_tc(rho, q):
    """C4: tau_c/t_c = 1 - [1+(q-1) rho]^(-1/(q-1)); q=1 limit 1-exp(-rho)."""
    rho = np.asarray(rho, dtype=float)
    if abs(q - 1.0) < 1e-12:
        return -np.expm1(-rho)
    return -np.expm1(-np.log1p((q - 1.0) * rho) / (q - 1.0))


def c4(rho, q):
    """C4: returns (tau_c/t_c, F_cur, F_min) for rho = tau0/t_c."""
    x = tau_c_over_tc(rho, q)
    rho = np.asarray(rho, dtype=float)
    f_cur = rho / x
    f_min = np.minimum(rho, 1.0) / x
    return x, f_cur, f_min


# ---- C8 (bisection root) ----
def bisect(f, lo, hi, rtol=1e-12, maxit=400):
    """Bisection per plan 3.2: evaluate both ends first; return
    (root or None, f_lo, f_hi at the ORIGINAL bracket ends, iterations). Stops at relative bracket width rtol."""
    flo, fhi = f(lo), f(hi)
    if flo == 0.0:
        return lo, flo, fhi, 0
    if fhi == 0.0:
        return hi, flo, fhi, 0
    if flo * fhi > 0:
        return None, flo, fhi, 0
    flo0, fhi0 = flo, fhi   # original end values are what gets reported
    it = 0
    while it < maxit and abs(hi - lo) > rtol * max(abs(lo), abs(hi), 1e-300):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm == 0.0:
            return mid, flo0, fhi0, it
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
        it += 1
    return 0.5 * (lo + hi), flo0, fhi0, it


def x_star(rho, q):
    """C8: root x* of x - rho*(1-x)^q on (0,1). Ends: -rho and +1."""
    r, _, _, _ = bisect(lambda x: x - rho * (1.0 - x) ** q, 0.0, 1.0)
    return r


def c8_ratio(rho, q):
    """C8: tau_LB/tau_c = x* / (tau_c/t_c)."""
    return x_star(rho, q) / float(tau_c_over_tc(rho, q))


# ---- numerical helpers ----
def golden_max(f, a, b, tol=1e-10):
    """Golden-section maximum of f on [a,b] (relative width tol)."""
    g = (math.sqrt(5.0) - 1.0) / 2.0
    c = b - g * (b - a)
    d = a + g * (b - a)
    fc, fd = f(c), f(d)
    while abs(b - a) > tol * max(abs(a), abs(b), 1e-300):
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = f(d)
    x = 0.5 * (a + b)
    return x, f(x)


def simpson(f, a, b, n):
    """Composite Simpson with n (even) intervals; f must accept numpy arrays."""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3.0 * (y[0] + y[-1] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-1:2].sum())


def simpson_adaptive(f, a, b, tol=1e-8, n0=64, nmax=2 ** 24):
    """Plan 3.2: start at 64 intervals, double until relative change < tol.
    Returns (value, n, rel_change)."""
    n = n0
    prev = simpson(f, a, b, n)
    while n < nmax:
        n *= 2
        cur = simpson(f, a, b, n)
        rel = abs(cur - prev) / max(abs(cur), 1e-300)
        if rel < tol:
            return cur, n, rel
        prev = cur
    return cur, n, rel


def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h / 2, y + h / 2 * k1)
    k3 = f(t + h / 2, y + h / 2 * k2)
    k4 = f(t + h, y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def first_passage_rk4(f, y_target, t_end, h, y0=0.0, clamp=None):
    """RK4, fixed step h, first time y reaches y_target, event located by
    bisection inside the bracketing step (re-integrating a fractional RK4 step).
    t_end is the upper limit (the event must occur before it).
    Returns time or None if not reached by t_end."""
    t, y = 0.0, y0
    while t < t_end:
        hh = min(h, t_end - t)
        yn = rk4_step(f, t, y, hh)
        if clamp:
            yn = clamp(yn)
        if yn >= y_target:
            lo, hi = 0.0, hh   # fractional step sizes
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                ym = rk4_step(f, t, y, mid)
                if clamp:
                    ym = clamp(ym)
                if ym >= y_target:
                    hi = mid
                else:
                    lo = mid
                if hi - lo < 1e-14 * max(hh, 1e-300):
                    break
            return t + 0.5 * (lo + hi)
        t += hh
        y = yn
    return None


def log_grid(lo, hi, per_decade):
    n = int(round(math.log10(hi / lo) * per_decade))
    return np.logspace(math.log10(lo), math.log10(hi), n + 1)


if __name__ == "__main__":
    s = sigma_a0()
    print("C1 baseline: sigma_a0 = %.4f MPa (planner expects about 108.7; accept 105 to 112)" % s)
    print("m = %.4f" % M_EXP)
    for nu in (0.01, 0.1, 1, 10):
        print("nu=%g Hz  tau0 = %.4f yr" % (nu, tau0_years(nu)))
