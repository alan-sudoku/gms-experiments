"""Rows R1-R7: toy-chain CExC, losses, entropy, by-product mismatch, operational margin.

Spec rows implemented: R1, R2, R3, R4, R5, R6, R7 (section 3 of prompt_2_plan.md).
Assumptions: all inputs exactly as in the table. R7 uses r_el = 3.0 as stated in
its own row (R3 uses r_el = 1/eta_el = 2.5); the two are not reconciled here.
"Cumulative loss" in R3 is taken as loss_gen + loss_smelt (R1 sum, 1030 kJ/mol).
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


# R1
b_ore, b_fuel, W_el, eta_el, b = 30.0, 900.0, 200.0, 0.4, 400.0  # kJ/mol
CExC = b_ore + b_fuel + W_el / eta_el
loss_gen = W_el / eta_el - W_el
loss_smelt = b_ore + b_fuel + W_el - b
num("R1", "CExC", CExC, "kJ/mol", 1430.0, 1e-9, rel=True)
num("R1", "loss_gen", loss_gen, "kJ/mol", 300.0, 1e-9, rel=True)
num("R1", "loss_smelt", loss_smelt, "kJ/mol", 730.0, 1e-9, rel=True)
num("R1", "loss_gen+loss_smelt", loss_gen + loss_smelt, "kJ/mol", 1030.0, 1e-9, rel=True)
num("R1", "closure CExC-b", CExC - b, "kJ/mol", loss_gen + loss_smelt, 1e-9, rel=True)
cond("R1", "all losses positive", loss_gen > 0 and loss_smelt > 0, value=(loss_gen, loss_smelt), expect="> 0")

# R2
S = (CExC - b) * 1e3 / TREF
num("R2", "entropy generated", S, "J/(K mol)", 3454.64, 0.01)

# R3
r_el = 1.0 / eta_el
num("R3", "delivered-basis loss_smelt", loss_smelt, "kJ/mol", 730.0, 1e-9, rel=True)
num("R3", "r_el", r_el, "-", 2.5, 1e-9, rel=True)
cond("R3", "delivered loss < cumulative loss", loss_smelt < loss_gen + loss_smelt,
     value=(loss_smelt, loss_gen + loss_smelt), expect="730 < 1030")

# R4
b_bp, credit = 100.0, 250.0
CExC_net = CExC - credit
apparent = CExC_net - b
actual = CExC - b - b_bp
mismatch = actual - apparent
num("R4", "CExC_net", CExC_net, "kJ/mol", 1180.0, 1e-9, rel=True)
num("R4", "apparent", apparent, "kJ/mol", 780.0, 1e-9, rel=True)
num("R4", "actual", actual, "kJ/mol", 930.0, 1e-9, rel=True)
num("R4", "mismatch", mismatch, "kJ/mol", 150.0, 1e-9, rel=True)
cond("R4", "mismatch non-zero", mismatch != 0, value=mismatch, expect="!= 0")

# R5
P_g, P_s = 10.0, 12.0
tau = 10 * 365.25 * 86400
T0 = 298.15
R5 = (P_s - P_g) * tau / T0
num("R5", "tau", tau, "s", 315576000.0, 1e-9, rel=True)
num("R5", "operational advantage", R5, "J/K", 2116894.2, 0.5)
cond("R5", "positive", R5 > 0, value=R5, expect="> 0")

# R6
D = 4.0e6
m6 = D - R5
num("R6", "margin local", m6, "J/K", 1883105.8, 0.5)
cond("R6", "sign positive (candidate loses)", m6 > 0, value=m6, expect="> 0")

# R7
m7 = D - 3.0 * R5
num("R7", "margin cumulative (r_el=3.0)", m7, "J/K", -2350682.6, 1.5)
cond("R7", "sign negative (candidate wins), opposite to R6", m7 < 0 and (m7 * m6 < 0),
     value=(m6, m7), expect="R7<0, R6>0")
summary()
