"""Rows R14-R21: full closed-form check, omitted dispersion, single-life conventions,
four-unit chain, mapping identity, incumbent charge, verdict flip, omission-bias count.

Spec rows implemented: R14, R15, R16, R17, R18, R19, R20, R21.
Assumptions:
- R14: the spec says "build literally from the prompt's formulas"; those formulas live
  in a file I was not told to read. I read claim C5 only and built the left side
  stage by stage from the structure C5/C6 describe (unit 0 virgin; each of m
  replacement units extracts (1-R_i) virgin; every one of m+1 units pays conversion,
  remelt R_i*w_rm, transport and effective manufacturing; tooling+components once, spread
  over N_units). This reconstruction is NOT the literal prompt text. See issues.md.
  Units: w in kJ/mol (x1e3 to J), b_transport MJ/kg (x1e6). 1000 draws, default_rng(0),
  draws made in the order of the table, per-element arrays of shape (1000,3).
- R18/R21 draw order: as listed in the table, default_rng(0).
- R19: "x" in the units is per mole of x.
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


# R14
rng = np.random.default_rng(0)
N = 1000
T0 = TREF
n_i = rng.uniform(0.1, 50, (N, 3))
w_ext = rng.uniform(100, 5000, (N, 3))
w_conv = rng.uniform(0, 500, (N, 3))
w_rm = rng.uniform(10, 200, (N, 3))
R_i = rng.uniform(0, 1, (N, 3))
M_G = rng.uniform(0.1, 10, N)
b_tr = rng.uniform(0.1, 5, N)
mfg = rng.uniform(0, 1e4, N)
tool = rng.uniform(0, 1e4, N)
comp = rng.uniform(0, 1e4, N)
N_units = rng.integers(1, 1001, N)
m = rng.integers(0, 11, N)


def stagewise(n_i, w_ext, w_conv, w_rm, R_i, M_G, b_tr, mfg, tool, comp, N_units, m):
    tot = np.zeros(len(M_G))
    # unit 0: virgin extraction; units 1..m: fraction (1-R) virgin
    for u in range(0, 11):
        active = u <= m
        ext_frac = 1.0 if u == 0 else None
        per_el = np.zeros(len(M_G))
        for i in range(3):
            frac = np.ones(len(M_G)) if u == 0 else (1 - R_i[:, i])
            per_el += n_i[:, i] * (w_ext[:, i] * frac * 1e3 + w_conv[:, i] * 1e3
                                   + R_i[:, i] * w_rm[:, i] * 1e3) / T0
        per_unit = per_el + M_G * b_tr * 1e6 / T0 + mfg
        tot += np.where(active, per_unit, 0.0)
    return tot + (tool + comp) / N_units


def closed(n_i, w_ext, w_conv, w_rm, R_i, M_G, b_tr, mfg, tool, comp, N_units, m):
    mm = m[:, None]
    bracket = (w_ext * (1 + mm * (1 - R_i)) + (mm + 1) * w_conv + (mm + 1) * R_i * w_rm) * 1e3
    return ((n_i * bracket).sum(axis=1) / T0
            + (m + 1) * (M_G * b_tr * 1e6 / T0 + mfg) + (tool + comp) / N_units)


args = (n_i, w_ext, w_conv, w_rm, R_i, M_G, b_tr, mfg, tool, comp, N_units, m)
a = stagewise(*args)
c = closed(*args)
mx = np.max(np.abs(a - c) / np.abs(c))
print(f"R14 | max rel diff stagewise vs closed form = {mx:.3e}")
cond("R14", "closed form", mx < 1e-12, value=f"{mx:.3e}", expect="< 1e-12 relative")
# multiplier of w_ext,i: set w_ext of element 0 to 1 kJ/mol, all else zero, in the stagewise sum
z = np.zeros((N, 3))
w1 = z.copy(); w1[:, 0] = 1.0
args_mult = (n_i, w1, z, z, R_i, np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), np.zeros(N), N_units, m)
mult = stagewise(*args_mult) * T0 / (n_i[:, 0] * 1e3)
mx2 = np.max(np.abs(mult - (1 + m * (1 - R_i[:, 0]))) / (1 + m * (1 - R_i[:, 0])))
print(f"R14 | max rel diff multiplier of w_ext,0 vs 1+m(1-R) = {mx2:.3e}")
cond("R14", "w_ext multiplier", mx2 < 1e-12, value=f"{mx2:.3e}", expect="< 1e-12 relative")

# R15
n_x, R_x, b_x = 0.5, 0.5, 300.0
n, R, b, mm = 20.0, 0.9, 380.0, 3
inc = n_x * (1 - R_x) * b_x
cand = (mm + 1) * n * (1 - R) * b
net = cand - inc
num("R15", "incumbent omitted", inc, "kJ", 75.0, 1e-9, rel=True)
num("R15", "incumbent / Tref", inc * 1e3 / TREF, "J/K", 251.55, 0.01)
num("R15", "candidate omitted", cand, "kJ", 3040.0, 1e-9, rel=True)
num("R15", "candidate / Tref", cand * 1e3 / TREF, "J/K", 10196.21, 0.01)
num("R15", "net", net, "kJ", 2965.0, 1e-9, rel=True)
num("R15", "net / Tref", net * 1e3 / TREF, "J/K", 9944.66, 0.01)
cond("R15", "net positive (against candidate)", net > 0, value=net, expect="> 0")

# R16
E_V, E_rec, R, A = 1100.0, 50.0, 0.8, 0.2
fw = E_V + R * E_rec
cut = E_V
avd = (1 - R) * E_V + R * E_rec
fifty = E_V + (R / 2) * (E_rec - E_V)
circ = E_V + (1 - A) * R * (E_rec - E_V)
for lab, v, e in [("framework", fw, 1140.0), ("cut-off", cut, 1100.0), ("avoided burden", avd, 260.0),
                  ("50:50", fifty, 680.0), ("circular footprint", circ, 428.0)]:
    num("R16", lab, v, "kJ/mol", e, 1e-9, rel=True)
cond("R16", "framework largest", fw == max(fw, cut, avd, fifty, circ), value=fw, expect="max of five")

# R17
m = 3
fw4 = E_V * (1 + m * (1 - R)) + (m + 1) * R * E_rec
cut4 = E_V + m * ((1 - R) * E_V + R * E_rec)
avd4 = (m + 1) * ((1 - R) * E_V + R * E_rec)
num("R17", "framework chain", fw4, "kJ/mol", 1920.0, 1e-9, rel=True)
num("R17", "cut-off chain", cut4, "kJ/mol", 1880.0, 1e-9, rel=True)
num("R17", "avoided-burden chain", avd4, "kJ/mol", 1040.0, 1e-9, rel=True)
num("R17", "framework - cut-off", fw4 - cut4, "kJ/mol", R * E_rec, 1e-9, rel=True, note="= R*E_rec = 40")
num("R17", "framework - avoided", fw4 - avd4, "kJ/mol", R * E_V, 1e-9, rel=True, note="= R*E_V = 880")

# R18
rng = np.random.default_rng(0)
EV = rng.uniform(100, 5000, 1000)
Er = rng.uniform(10, 500, 1000)
Rr = rng.uniform(0, 1, 1000)
mr = rng.integers(0, 11, 1000)
l = EV * (1 + mr * (1 - Rr)) + (mr + 1) * Rr * Er
r = (mr + 1) * ((1 - Rr) * EV + Rr * Er) + Rr * EV
mx = np.max(np.abs(l - r) / np.abs(r))
print(f"R18 | max rel diff = {mx:.3e}")
cond("R18", "mapping identity", mx < 1e-12, value=f"{mx:.3e}", expect="< 1e-12 relative")

# R19
n_x = 0.5
met = n_x * (2000.0 - 800.0)
sym = n_x * (500.0 - 60.0 + 250.0)
num("R19", "framework charge", met, "kJ", 600.0, 1e-9, rel=True)
num("R19", "framework charge / Tref", met * 1e3 / TREF, "J/K", 2012.41, 0.01)
num("R19", "symmetric charge", sym, "kJ", 345.0, 1e-9, rel=True)
num("R19", "symmetric charge / Tref", sym * 1e3 / TREF, "J/K", 1157.14, 0.01)
over = (met - sym) * 1e3 / TREF
num("R19", "overcharge", over, "J/K", 855.27, 0.01)
cond("R19", "overcharge positive", over > 0, value=over, expect="> 0")

# R20
S_g = 1500.0
v1 = S_g < met * 1e3 / TREF
v2 = S_g < sym * 1e3 / TREF
cond("R20", "S_g < S_s (framework 2012.41)", v1 is True or v1 == True, value=bool(v1), expect="True")
cond("R20", "S_g < S_s (symmetric 1157.14)", v2 == False, value=bool(v2), expect="False")

# R21
rng = np.random.default_rng(0)
Sg = rng.uniform(0, 1e4, 10000)
Ss = rng.uniform(0, 1e4, 10000)
dom = rng.uniform(0, 5e3, 10000)
rep = Sg < Ss
tru = Sg < Ss + dom
c1 = int(np.sum(rep & ~tru))
c2 = int(np.sum(~rep & tru))
cond("R21", "reported win, true loss count", c1 == 0, value=c1, expect="exactly 0")
cond("R21", "reported loss, true win count", c2 > 0, value=c2, expect="> 0")
summary()
