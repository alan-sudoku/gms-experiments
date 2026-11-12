"""Rows R32-R35: spectral (mode-by-mode) exergy integrals and per-mode Carnot bound.

Spec rows implemented: R32, R33, R34a, R34b, R35.
Assumptions:
- Trapezoid on u = logspace(-4, log10(150), 200001), as specified.
- sg(n) = (1+n) log1p(n) - n log(n), 0 at n = 0; n0 = 0 where u/x > 700.
- R32 tolerance for E vs pi^4/15 is not given in the spec; the row's +/-1e-5 is applied
  (to E, absolute), noted in the output.
- R33 "energy fraction above u_c" = E_c/E (both integrals of u^3 n_s).
- R34b: eps = 2.1627e-5, T0 = 298.15, Ts = 5772.
- R35: default_rng(0); 10000 draws of u ~ U(0.05,20) first, then f = 10**U(-8,0);
  cases kept where n > n0; violation tolerance 1e-12 relative slack.
- R33/R34 hand estimates are used as sanity targets with the stated tolerances.
"""
import math
import sys
import numpy as np

TREF = 298.15
RGAS = 8.314462618
SIG = 5.670374419e-8
TS = 5772.0

_ROW_OK = {}


def _rec(row, ok):
    _ROW_OK[row] = _ROW_OK.get(row, True) and bool(ok)


def num(row, label, value, unit, expected, tol, rel=False, note=""):
    """Compare value to expected within tol (absolute, or relative if rel)."""
    err = abs(value - expected)
    ok = err <= (tol * abs(expected) if rel else tol)
    toltxt = (f"{tol:g} relative" if rel else f"+/-{tol:g} {unit}")
    print(f"{row} | {label} = {value:.10g} {unit} | expected {expected:.10g} {unit}"
          f" | tol {toltxt} | |diff|={err:.3e} | {'PASS' if ok else 'FAIL'}"
          + (f" | {note}" if note else ""))
    _rec(row, ok)
    return ok


def cond(row, label, ok, detail="", value="", expect=""):
    """Boolean sanity check."""
    print(f"{row} | {label}: {value} | sanity: {expect} | tol exact | {detail} | {'PASS' if ok else 'FAIL'}")
    _rec(row, ok)
    return ok


def summary():
    print("\n=== ROW SUMMARY ===")
    for r, ok in _ROW_OK.items():
        print(f"{r}: {'PASS' if ok else 'FAIL'}")


x = 298.15 / 5772.0
u = np.logspace(-4, math.log10(150), 200001)
trap = np.trapezoid if hasattr(np, "trapezoid") else np.trapz


def sg(n):
    n = np.asarray(n, dtype=float)
    out = np.zeros_like(n)
    pos = n > 0
    nn = n[pos]
    out[pos] = (1 + nn) * np.log1p(nn) - nn * np.log(nn)
    return out


def occ0(u, x):
    z = u / x
    out = np.zeros_like(u)
    ok = z <= 700
    out[ok] = 1.0 / np.expm1(z[ok])
    return out


with np.errstate(all="ignore"):
    n_s = 1.0 / np.expm1(u)
n0 = occ0(u, x)


def Wint(n):
    integrand = u ** 2 * (u * (n - n0) - x * (sg(n) - sg(n0)))
    return trap(integrand, u)


E_full = trap(u ** 3 * n_s, u)

# R32
psi32 = Wint(n_s) / E_full
ref27 = 1 - (4 / 3) * x + (1 / 3) * x ** 4
num("R32", "psi (spectral)", psi32, "-", 0.931130, 1e-5)
num("R32", "psi vs Landsberg formula", psi32, "-", ref27, 1e-5)
num("R32", "E", E_full, "(dimensionless)", math.pi ** 4 / 15, 1e-5, note="pi^4/15 = 6.49394; tol assumed 1e-5")

# R33
uc = 2.266
n33 = np.where(u >= uc, n_s, n0)
Ec = trap(np.where(u >= uc, u ** 3 * n_s, 0.0), u)
psi33 = Wint(n33) / Ec
num("R33", "psi (high-pass)", psi33, "-", 0.9355, 0.001, note="hand estimate")
num("R33", "energy fraction above u_c", Ec / E_full, "-", 0.7655, 0.001, note="approx in spec; tol assumed 0.001")
cond("R33", "ordering R27 < psi < R28", ref27 < psi33 < 1 - x, value=(ref27, psi33, 1 - x), expect="0.931130 < psi < 0.948345")

# R34a
eps = 2.1627e-5
n34a = np.maximum(eps * n_s, n0)
psi34a = Wint(n34a) / (eps * E_full)
num("R34a", "psi (diluted, with sky background)", psi34a, "-", 0.734, 0.01, note="hand estimate")
cond("R34a", "psi < R27", psi34a < ref27, value=(psi34a, ref27), expect="< 0.931130")

# R34b
n34b = eps * n_s
psi34b = Wint(n34b) / (eps * E_full)
share = (1 / 3) * x ** 4 / eps
solar = eps * SIG * TS ** 4
cold = SIG * 298.15 ** 4 / 3
num("R34b", "psi (no thermal sky background)", psi34b, "-", 0.838, 0.01, note="hand estimate")
num("R34b", "share", share, "-", 0.10973, 1e-4)
num("R34b", "eps*sig*Ts^4", solar, "W/m2", 1361.2, 0.1, note="approx in spec; tol assumed 0.1")
num("R34b", "sig*T0^4/3", cold, "W/m2", 149.36, 0.01, note="approx in spec; tol assumed 0.01")
num("R34b", "share cross-check", cold / solar, "-", share, 1e-4)
dpsi = psi34b - psi34a
num("R34b", "psi(34b) - psi(34a) vs share", dpsi, "-", share, 0.02)

# R35
rng = np.random.default_rng(0)
N = 10000
uu = rng.uniform(0.05, 20, N)
f = 10 ** rng.uniform(-8, 0, N)
ns = 1.0 / np.expm1(uu)
n = f * ns
n0r = occ0(uu, x)
keep = n > n0r
uu, n, n0r = uu[keep], n[keep], n0r[keep]
lhs = uu * (n - n0r) - x * (sg(n) - sg(n0r))
rhs1 = uu * (n - n0r) * (1 - x * np.log((1 + n) / n) / uu)
rhs2 = uu * n * (1 - x)
slack = 1e-12
v1 = int(np.sum(lhs > rhs1 + slack * np.abs(rhs1)))
v2 = int(np.sum(rhs1 > rhs2 + slack * np.abs(rhs2)))
print(f"R35 | draws kept (n > n0) = {keep.sum()} of {N}")
cond("R35", "LHS <= first bound violations", v1 == 0, value=v1, expect="0")
cond("R35", "first bound <= u n (1-x) violations", v2 == 0, value=v2, expect="0")
summary()
