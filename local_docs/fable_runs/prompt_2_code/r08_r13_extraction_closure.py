"""Rows R8-R13: scrap burden, framework extraction charge, closure gap, corrected charge,
double-count variant, random closure-identity check.

Spec rows implemented: R8, R9, R10, R11, R12, R13.
Assumptions: R13 draws, in this order from numpy.random.default_rng(0), arrays of
size 1000: n, b, k (CExC = b*(1+k)), R, m (integers 0..10 via integers(0,11)).
Claim C4 was read to resolve R13's "choice C equals choice B": the spec row does not
define the choice labels. Implemented as: choice C = make-up charged CExC-b plus
dispersion charged b, n[(CExC-b)(1+m(1-R)) + b(1-R)(m+1)]; choice B = corrected closed
form B = IN - R*n*b = n[CExC(1+m(1-R)) - R b]. See issues.md.
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


# R8
n, y = 20.0, 0.6
w_ext, w_conv, w_rm, R_scrap = 1820.0, 100.0, 50.0, 0.95
n_scrap = n * (1 / y - 1)
correct = n_scrap * ((1 - R_scrap) * w_ext + R_scrap * w_rm + w_conv)
double = n_scrap * (w_ext + w_conv)
omitted = 0.0
num("R8", "n_scrap", n_scrap, "mol", 13.3333, 1e-4)
num("R8", "correct burden", correct, "kJ", 3180.0, 0.1)
num("R8", "correct burden / Tref", correct * 1e3 / TREF, "J/K", 10665.8, 0.5)
num("R8", "double-counted burden", double, "kJ", 25600.0, 0.1)
num("R8", "double-counted burden / Tref", double * 1e3 / TREF, "J/K", 85862.8, 0.5)
cond("R8", "omitted = 0 and 0 < correct < double", omitted == 0 and 0 < correct < double,
     value=(omitted, correct, double), expect="0 < 3180 < 25600")

# R9-R12
n, CExC, b, R, m = 2.0, 1500.0, 400.0, 0.8, 3
F = n * (CExC - b) * (1 + m * (1 - R))
num("R9", "F", F, "kJ", 3520.0, 1e-9, rel=True)
num("R9", "F/Tref", F * 1e3 / TREF, "J/K", 11806.14, 0.01)

IN = n * CExC * (1 + m * (1 - R))
stock = n * b
gap = IN - stock - F
num("R10", "IN", IN, "kJ", 4800.0, 1e-9, rel=True)
num("R10", "stock", stock, "kJ", 800.0, 1e-9, rel=True)
num("R10", "gap", gap, "kJ", 480.0, 1e-9, rel=True)
num("R10", "gap vs m(1-R)nb", gap, "kJ", m * (1 - R) * n * b, 1e-9, rel=True)

B = F + (m + 1) * (1 - R) * n * b
num("R11", "B", B, "kJ", 4160.0, 1e-9, rel=True)
num("R11", "B vs IN - R n b", B, "kJ", IN - R * n * b, 1e-9, rel=True)
num("R11", "IN - 640", IN - R * n * b, "kJ", 4160.0, 1e-9, rel=True)
num("R11", "B/Tref", B * 1e3 / TREF, "J/K", 13952.71, 0.01)

Dd = n * (CExC - b) + m * (1 - R) * n * CExC + (m + 1) * (1 - R) * n * b
num("R12", "Dd", Dd, "kJ", 4640.0, 1e-9, rel=True)
num("R12", "excess", Dd - B, "kJ", 480.0, 1e-9, rel=True)
num("R12", "excess vs m(1-R)nb", Dd - B, "kJ", m * (1 - R) * n * b, 1e-9, rel=True)

# R13
rng = np.random.default_rng(0)
N = 1000
n = rng.uniform(0.1, 50, N)
b = rng.uniform(10, 1000, N)
CExC = b * (1 + rng.uniform(0.1, 50, N))
R = rng.uniform(0, 1, N)
m = rng.integers(0, 11, N)
lhs = n * ((CExC - b) * (1 + m * (1 - R)) + b * (1 - R) * (m + 1))   # choice C
rhs = n * (CExC * (1 + m * (1 - R)) - R * b)                          # closed form
B_ = n * (CExC - b) * (1 + m * (1 - R)) + (m + 1) * (1 - R) * n * b   # choice B = F + (m+1)(1-R)nb
mx1 = np.max(np.abs(lhs - rhs) / np.abs(rhs))
mx2 = np.max(np.abs(lhs - B_) / np.abs(B_))
print(f"R13 | max rel diff LHS vs RHS = {mx1:.3e}; max rel diff choice C vs choice B = {mx2:.3e}")
cond("R13", "closure identity", mx1 < 1e-12, value=f"{mx1:.3e}", expect="< 1e-12 relative")
cond("R13", "choice C equals choice B", mx2 < 1e-12, value=f"{mx2:.3e}", expect="< 1e-12 relative")
summary()
