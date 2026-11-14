"""Shared numerical helpers for Prompt 6 scripts (numpy only).

Implements the numerical rules of plan 3.2: composite Simpson with doubling,
bisection with end-value check and one decade extension, golden-section.
Claim level: derived (unverified).
"""
import numpy as np

YR = 3.15576e7          # s per year (convention)
UM_PER_YR = 3.16881e-14  # m/s per um/yr (convention)
R_GAS = 8.314462618      # M01
SEED = 20261115


def simpson_fixed(f, a, b, n):
    """Composite Simpson with n (even) intervals; f must accept numpy arrays."""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h / 3.0 * (y[0] + y[-1] + 4.0 * y[1:-1:2].sum() + 2.0 * y[2:-1:2].sum())


def simpson(f, a, b, tol=1e-8, n0=64, nmax=2 ** 24):
    """Simpson, n0 intervals, doubling until relative change < tol.
    Returns (value, n_final, last_relative_change, converged)."""
    n = n0
    prev = simpson_fixed(f, a, b, n)
    while n < nmax:
        n *= 2
        cur = simpson_fixed(f, a, b, n)
        rc = abs(cur - prev) / max(abs(cur), 1e-300)
        if rc < tol:
            return cur, n, rc, True
        prev = cur
    return cur, n, rc, False


def bisect(f, lo, hi, rtol=1e-12, extend_limit=None, max_it=400):
    """Bisection per plan 3.2.  Evaluates f at both ends first.  If no sign
    change, extends hi once by a factor 10 (or to extend_limit) and retries.
    Returns dict(root, bracketed, lo, hi, flo, fhi, extended, note)."""
    flo, fhi = f(lo), f(hi)
    info = dict(lo=lo, hi=hi, flo=flo, fhi=fhi, extended=False, bracketed=True)
    if flo * fhi > 0:
        hi2 = hi * 10 if extend_limit is None else min(hi * 10, extend_limit)
        fhi2 = f(hi2)
        info.update(extended=True, hi_ext=hi2, fhi_ext=fhi2)
        if flo * fhi2 > 0:
            info.update(bracketed=False, root=None)
            return info
        hi, fhi = hi2, fhi2
    if flo == 0:
        info['root'] = lo
        return info
    for _ in range(max_it):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm == 0:
            lo = hi = mid
            break
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
        if (hi - lo) <= rtol * max(abs(mid), 1e-300):
            break
    info['root'] = 0.5 * (lo + hi)
    return info


def golden_max(f, lo, hi, tol=1e-10, max_it=300):
    """Golden-section maximisation of f on [lo, hi] to absolute width tol."""
    g = (np.sqrt(5.0) - 1) / 2
    c = hi - g * (hi - lo)
    d = lo + g * (hi - lo)
    fc, fd = f(c), f(d)
    it = 0
    while (hi - lo) > tol and it < max_it:
        if fc > fd:
            hi, d, fd = d, c, fc
            c = hi - g * (hi - lo)
            fc = f(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + g * (hi - lo)
            fd = f(d)
        it += 1
    x = 0.5 * (lo + hi)
    return x, f(x)


def golden_min(f, lo, hi, tol=1e-10):
    x, v = golden_max(lambda z: -f(z), lo, hi, tol)
    return x, -v


def tag(ok):
    return 'PASS' if ok else 'FAIL'
