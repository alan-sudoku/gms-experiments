"""Rows R22-R31: dead-state temperature shift, Gibbs-Helmholtz check, divisor choice,
verdict flip, oxygen reference shift, Landsberg factor, Carnot gap, cold radiative sinks,
false-infeasible example, cold-source thermal term.

Spec rows implemented: R22, R23, R24, R25, R26, R27, R28, R29, R30, R31.
Assumptions: constants as in section 3 header. R29 scan: Te on a 2,000,001-point grid in
[0, Ta]; the non-negativity test of the ultimate bound uses a 100,001-point grid on
Tc in [0, Ta] (non-negative within -1e-12 W/m2 rounding). R30 uses unrounded R29 values.
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


# R22
b0, d0, T0 = 400.0, 420.0, 250.0
bT = (T0 / TREF) * b0 + (1 - T0 / TREF) * d0
num("R22", "b(T0)", bT, "kJ/mol", 403.230, 0.001)
cond("R22", "between b0 and d0", b0 < bT < d0, value=bT, expect="400 < b < 420")

# R23
dG, dH = -b0 * 1e3, -d0 * 1e3
dS = (dH - dG) / TREF
bT2 = -(dH - T0 * dS)
num("R23", "dS", dS, "J/(mol K)", -67.08, 0.01)
num("R23", "b(T0) Gibbs-Helmholtz", bT2 / 1e3, "kJ/mol", bT, 1e-9, rel=True, note="vs R22")

# R24
W = 600e3
a, c = W / TREF, W / 200.0
num("R24", "W/Tref", a, "J/K", 2012.41, 0.01)
num("R24", "W/T0 (T0=200 K)", c, "J/K", 3000.00, 0.01)
num("R24", "ratio", c / a, "-", 1.49075, 1e-5)

# R25
Wg, Ws, Sg, Ss, T0 = 900e3, 600e3, 1500.0, 2700.0, 200.0
cg, cs = Wg / TREF + Sg, Ws / TREF + Ss
fg, fs = Wg / T0 + Sg, Ws / T0 + Ss
num("R25", "correct g", cg, "J/K", 4518.61, 0.02)
num("R25", "correct s", cs, "J/K", 4712.41, 0.02)
num("R25", "correct margin g-s", cg - cs, "J/K", -193.80, 0.02)
num("R25", "framework g", fg, "J/K", 6000.0, 0.02)
num("R25", "framework s", fs, "J/K", 5700.0, 0.02)
num("R25", "framework margin g-s", fg - fs, "J/K", 300.0, 0.02)
cond("R25", "margins opposite signs", (cg - cs) < 0 < (fg - fs), value=(cg - cs, fg - fs), expect="-, +")

# R26
T0 = 298.15
p_old, p_new = 20.39e3, 1.0e-5
d_bO2 = RGAS * T0 * math.log(p_old / p_new)
d_bM = -0.5 * d_bO2
bO2_std = RGAS * T0 * math.log(101.325e3 / p_old)
num("R26", "d_bO2", d_bO2, "J/mol", 53138.0, 5.0)
num("R26", "d_bM", d_bM, "J/mol", -26569.0, 5.0)
num("R26", "bO2_std", bO2_std, "J/mol", 3974.0, 5.0, note="spec: tabulated ~3.97 kJ/mol UNSURE")


def eta(T0, Ts=TS):
    x = T0 / Ts
    return 1 - (4 / 3) * x + (1 / 3) * x ** 4


# R27
vals = []
for (t0, ts), e in zip([(300, 6000), (298.15, 5772), (200, 5772), (3, 5772)],
                       [0.933335, 0.931130, 0.953800, 0.999307]):
    v = eta(t0, ts)
    vals.append(v)
    num("R27", f"eta(T0={t0}, Ts={ts})", v, "-", e, 2e-6)
cond("R27", "increases as T0 falls (entries 2-4)", vals[1] < vals[2] < vals[3], value=vals[1:], expect="increasing")

# R28
x = 298.15 / 5772.0
carnot = 1 - x
gap = (x / 3) * (1 - x ** 3)
gap2 = carnot - eta(298.15, 5772.0)
num("R28", "Carnot factor", carnot, "-", 0.948345, 2e-6)
num("R28", "gap formula", gap, "-", 0.017216, 2e-6)
num("R28", "gap by subtraction", gap2, "-", 0.017216, 2e-6)
num("R28", "gap formula vs subtraction", gap, "-", gap2, 1e-9)

# R29
Ta = 300.0


def ultimate(Tc):
    return SIG * ((1 / 3) * Ta ** 4 - (4 / 3) * Ta * Tc ** 3 + Tc ** 4)


P_bb = SIG * Ta ** 4
P0 = ultimate(0.0)
P270 = ultimate(270.0)
num("R29", "sig*Ta^4", P_bb, "W/m2", 459.300, 0.005)
num("R29", "ultimate, Tc=0", P0, "W/m2", 153.100, 0.005)
num("R29", "ultimate, Tc=270 K", P270, "W/m2", 8.007, 0.005)
Te = np.linspace(0, Ta, 2000001)
em = SIG * (Ta * Te ** 3 - Te ** 4)
k = int(np.argmax(em))
num("R29", "single-emitter max (scan)", em[k], "W/m2", 48.442, 0.005)
num("R29", "scan argmax Te", Te[k], "K", 225.0, 0.01)
num("R29", "(27/256) sig Ta^4", (27 / 256) * P_bb, "W/m2", em[k], 0.005)
Tc = np.linspace(0, Ta, 100001)
ub = ultimate(Tc)
cond("R29", "bound zero at Tc=Ta", abs(ultimate(Ta)) < 1e-9, value=ultimate(Ta), expect="0")
cond("R29", "bound non-negative on [0,Ta]", ub.min() > -1e-9, value=f"min={ub.min():.3e}", expect=">= 0")

# R30
eta_, q, A, t, demand = 0.933, 200.0, 1.0, 86400.0, 20e6
U_fw = eta_ * q * A * t
U_deep = U_fw + P0 * A * t
U_sky = U_fw + P270 * A * t
num("R30", "U_fw", U_fw / 1e6, "MJ", 16.122, 0.002)
num("R30", "deep-space addition", P0 * A * t / 1e6, "MJ", 13.228, 0.002)
num("R30", "U with deep-space sink", U_deep / 1e6, "MJ", 29.350, 0.002)
num("R30", "270 K sky addition", P270 * A * t / 1e6, "MJ", 0.692, 0.002)
num("R30", "U with 270 K sky", U_sky / 1e6, "MJ", 16.814, 0.002)
cond("R30", "verdicts (demand > U): fw infeasible, deep not excluded, sky infeasible",
     (demand > U_fw) and not (demand > U_deep) and (demand > U_sky),
     value=(demand > U_fw, demand > U_deep, demand > U_sky), expect="(True, False, True)")

# R31
q, T0, Tsrc = 100.0, 300.0, 250.0
num("R31", "framework term", q * (1 - T0 / Tsrc), "W/m2", -20.0, 1e-9, rel=True)
num("R31", "corrected term", q * (T0 / Tsrc - 1), "W/m2", 20.0, 1e-9, rel=True)
summary()
