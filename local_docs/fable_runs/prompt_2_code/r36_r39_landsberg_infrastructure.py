"""Rows R36-R39: fixed versus computed Landsberg factor, infrastructure shares, net bias,
allocation per unit versus per mole.

Spec rows implemented: R36, R37, R38, R39.
Assumptions: R38 uses the unrounded lambda from R37 (avg share / Tref).
R39 per-mole shares are B/(N1 n1 + N2 n2) * n_k in J per unit of product k.
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


# R36
q, T0, Ts = 1361.0, 200.0, 5772.0
x = T0 / Ts
eta_c = 1 - (4 / 3) * x + (1 / 3) * x ** 4
num("R36", "0.933*q", 0.933 * q, "W/m2", 1269.81, 0.02)
num("R36", "eta(T0,Ts)*q", eta_c * q, "W/m2", 1298.12, 0.02)
cond("R36", "fixed < computed", 0.933 * q < eta_c * q, value=(0.933 * q, eta_c * q), expect="fixed < computed")

# R37
F, v, N = 4.0e13, 2.0e4, 1.0e9
avg = F / N + v
marg = v
num("R37", "avg", avg, "J/unit", 6.0e4, 1e-9, rel=True)
num("R37", "avg / Tref", avg / TREF, "J/K", 201.241, 0.001)
num("R37", "marg", marg, "J/unit", 2.0e4, 1e-9, rel=True)
num("R37", "marg / Tref", marg / TREF, "J/K", 67.080, 0.001)
cond("R37", "avg > marg", avg > marg, value=(avg, marg), expect="avg > marg")

# R38
lam = avg / TREF
d_omit = 150.0
net = lam - d_omit
num("R38", "net bias", net, "J/K", 51.241, 0.001)
cond("R38", "positive (candidate's favour)", net > 0, value=net, expect="> 0")

# R39
B = 6.0e13
N1, n1, N2, n2 = 9.0e8, 0.1, 1.0e8, 5.0
per_unit = B / (N1 + N2)
num("R39", "per unit share, product 1", per_unit / TREF, "J/K", 201.241, 0.001)
num("R39", "per unit share, product 2", per_unit / TREF, "J/K", 201.241, 0.001)
per_mol = B / (N1 * n1 + N2 * n2)
s1, s2 = per_mol * n1, per_mol * n2
num("R39", "per mole share, product 1", s1 / TREF, "J/K", 34.109, 0.001)
num("R39", "per mole share, product 2", s2 / TREF, "J/K", 1705.432, 0.001)
num("R39", "closure per mole N1 s1 + N2 s2", N1 * s1 + N2 * s2, "J", B, 1e-9, rel=True)
num("R39", "closure per unit", per_unit * (N1 + N2), "J", B, 1e-9, rel=True)
summary()
