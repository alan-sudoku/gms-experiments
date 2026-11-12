"""S4 finaliser checks for prompt 2. All results are claims at level `derived` (unverified).

S4-A  R14 rebuilt literally from the prompt's formulas (Sigma_g,init, R_g, Sigma^ret_EOL,
      Sigma_g,EOL with w_conv = w_lost,prec - w_lost,ext) and compared with the closed form
      of plan claim C5. Same draws and units as r14_r21_closed_form_conventions.py
      (default_rng(0), kJ/mol -> J/mol, MJ/kg -> J/kg, T0 = 298.15 K).
S4-B  Event-by-event extraction ledger (plan D2), choices A-D as the plan defines them.
      Replaces the near-tautological "choice C equals choice B" part of R13.
S4-C  R7 repeated with r_el = 2.5 (the toy-chain value of R3) and the break-even r_el.
S4-D  R30 sink choice: bound at Tc = 0, 3, 270 K, sky temperature at which the verdict
      flips, and the effect of using the single-emitter value as if it were a bound.
Run: python3 s4_literal_r14_and_reconcile.py > outputs/s4_literal_r14_and_reconcile.txt
"""
import numpy as np

TREF = 298.15
SIG = 5.670374419e-8
_OK = {}


def check(row, label, ok, value):
    _OK[row] = _OK.get(row, True) and bool(ok)
    print(f"{row} | {label}: {value} | {'PASS' if ok else 'FAIL'}")


# ---------------------------------------------------------------- S4-A
rng = np.random.default_rng(0)
N = 1000
T0 = TREF
n_i = rng.uniform(0.1, 50, (N, 3))
w_ext = rng.uniform(100, 5000, (N, 3)) * 1e3
w_conv_in = rng.uniform(0, 500, (N, 3)) * 1e3
w_rm = rng.uniform(10, 200, (N, 3)) * 1e3
R_i = rng.uniform(0, 1, (N, 3))
M_G = rng.uniform(0.1, 10, N)
b_tr = rng.uniform(0.1, 5, N) * 1e6
mfg = rng.uniform(0, 1e4, N)
tool = rng.uniform(0, 1e4, N)
comp = rng.uniform(0, 1e4, N)
N_units = rng.integers(1, 1001, N)
m = rng.integers(0, 11, N)


def literal(w_ext, w_prec, w_rm, b_tr, mfg, tool, comp):
    """Sigma_g,init + m*R_g + Sigma_g,EOL exactly as the prompt writes each term."""
    w_conv = w_prec - w_ext                                   # prompt: w_conv = w_lost,prec - w_lost,ext
    s_init = ((n_i * w_prec).sum(axis=1) + M_G * b_tr) / T0 + mfg + tool / N_units + comp / N_units
    s_eol = (n_i * R_i * w_rm).sum(axis=1) / T0               # unit in service at the horizon
    s_ret = (n_i * (R_i * w_rm + (1 - R_i) * w_ext)).sum(axis=1) / T0   # retired unit
    r_g = ((n_i * w_conv).sum(axis=1) + M_G * b_tr) / T0 + mfg + s_ret
    return s_init + m * r_g + s_eol


def closed_c5(w_ext, w_conv, w_rm, b_tr, mfg, tool, comp):
    mm = m[:, None]
    br = w_ext * (1 + mm * (1 - R_i)) + (mm + 1) * w_conv + (mm + 1) * R_i * w_rm
    return (n_i * br).sum(axis=1) / T0 + (m + 1) * (M_G * b_tr / T0 + mfg) + (tool + comp) / N_units


lhs = literal(w_ext, w_ext + w_conv_in, w_rm, b_tr, mfg, tool, comp)
rhs = closed_c5(w_ext, w_conv_in, w_rm, b_tr, mfg, tool, comp)
d = np.max(np.abs(lhs - rhs) / np.abs(rhs))
check("S4-A", "literal prompt sum vs C5 closed form, max rel diff (< 1e-12)", d < 1e-12, f"{d:.3e}")

# multiplier of w_ext,i by linearity: unit w_ext on one element, w_conv held fixed (= 0), all else 0
z3, z1 = np.zeros((N, 3)), np.zeros(N)
worst = 0.0
for i in range(3):
    e = z3.copy()
    e[:, i] = 1.0
    mult = literal(e, e + z3, z3, z1, z1, z1, z1) * T0 / n_i[:, i]
    worst = max(worst, np.max(np.abs(mult - (1 + m * (1 - R_i[:, i]))) / (1 + m * (1 - R_i[:, i]))))
check("S4-A", "multiplier of w_ext,i vs 1+m(1-R_i), w_conv fixed, max rel diff (< 1e-12)",
      worst < 1e-12, f"{worst:.3e}")
# same test with w_lost,prec held fixed instead (then w_conv falls as w_ext rises)
worst2 = 0.0
for i in range(3):
    e = z3.copy()
    e[:, i] = 1.0
    mult = literal(e, z3, z3, z1, z1, z1, z1) * T0 / n_i[:, i]
    worst2 = max(worst2, np.max(np.abs(mult - (-m * R_i[:, i]))))
check("S4-A", "multiplier of w_ext,i with w_lost,prec fixed equals -m*R_i, max abs diff (< 1e-12)",
      worst2 < 1e-12, f"{worst2:.3e}")

# ---------------------------------------------------------------- S4-B
rng = np.random.default_rng(0)
n = rng.uniform(0.1, 50, N)
b = rng.uniform(10, 1000, N)
CExC = b * (1 + rng.uniform(0.1, 50, N))
R = rng.uniform(0, 1, N)
mB = rng.integers(0, 11, N)
res_in = n * CExC                 # build first unit
destroyed = n * (CExC - b)
stock = n * b
chA = n * (CExC - b)              # A: as written, never charge b
chB = n * (CExC - b)              # B: make-up at CExC-b, (1-R)b at every dispersal
chC = n * (CExC - b)              # C: make-up at full CExC, (1-R)b at the final retirement only
chD = n * (CExC - b)              # D: make-up at full CExC and (1-R)b at every dispersal
for j in range(1, 11):
    act = j <= mB
    disp = np.where(act, (1 - R) * n, 0.0)
    destroyed += disp * b                      # dispersal of the retired unit
    stock -= disp * b
    res_in += disp * CExC                      # make-up extraction
    destroyed += disp * (CExC - b)
    stock += disp * b
    chA += disp * (CExC - b)
    chB += disp * (CExC - b) + disp * b
    chC += disp * CExC
    chD += disp * CExC + disp * b
gapH1 = res_in - stock - chA                   # last unit in service
dH1 = np.max(np.abs(gapH1 - mB * (1 - R) * n * b) / (n * b))
check("S4-B", "H1: IN - stock - A equals m(1-R)nb, max diff / nb (< 1e-12)", dH1 < 1e-12, f"{dH1:.3e}")
last = (1 - R) * n * b                         # final retirement, no successor (H2)
destroyed += last
stock -= last
chB += last
chC += last
chD += last
rel = lambda x, y: np.max(np.abs(x - y) / np.abs(y))
check("S4-B", "H2: destroyed equals IN - stock (ledger closes), max rel diff", rel(destroyed, res_in - stock) < 1e-12,
      f"{rel(destroyed, res_in - stock):.3e}")
check("S4-B", "H2: stock equals R*n*b, max rel diff", rel(stock + 1e-300, R * n * b + 1e-300) < 1e-9,
      f"{rel(stock + 1e-300, R * n * b + 1e-300):.3e}")
check("S4-B", "choice B equals destroyed, max rel diff", rel(chB, destroyed) < 1e-12, f"{rel(chB, destroyed):.3e}")
check("S4-B", "choice C (plan definition) equals choice B, max rel diff", rel(chC, chB) < 1e-12, f"{rel(chC, chB):.3e}")
sA = np.max(np.abs((destroyed - chA) - (mB + 1) * (1 - R) * n * b) / (n * b))
sD = np.max(np.abs((chD - destroyed) - mB * (1 - R) * n * b) / (n * b))
check("S4-B", "choice A short by (m+1)(1-R)nb, max diff / nb", sA < 1e-12, f"{sA:.3e}")
check("S4-B", "choice D over by m(1-R)nb, max diff / nb", sD < 1e-12, f"{sD:.3e}")

# ---------------------------------------------------------------- S4-C
P_g, P_s, tau, D = 10.0, 12.0, 10 * 365.25 * 86400, 4.0e6
adv = (P_s - P_g) * tau / TREF                 # R5
for r_el in (1.0, 2.5, 3.0):
    print(f"S4-C | margin Sigma_g - Sigma_s at r_el = {r_el}: {D - r_el * adv:.3f} J/K")
r_star = D / adv
print(f"S4-C | break-even r_el = D / R5 = {r_star:.6f}")
check("S4-C", "flip holds for r_el = 2.5 and 3.0 (both above break-even), not for 1.0",
      (D - 2.5 * adv < 0) and (D - 3.0 * adv < 0) and (D - adv > 0), f"r* = {r_star:.4f}")

# ---------------------------------------------------------------- S4-D
Ta, eta, q, A, t = 300.0, 0.933, 200.0, 1.0, 86400.0
P = lambda Tc: SIG * (Ta**4 / 3 - 4 / 3 * Ta * Tc**3 + Tc**4)
U_fw = eta * q * A * t
for Tc in (0.0, 3.0, 270.0):
    print(f"S4-D | cold-sink bound at Tc = {Tc:g} K: {P(Tc):.6f} W/m2; U = {(U_fw + P(Tc) * A * t) / 1e6:.6f} MJ")
print(f"S4-D | bound(0 K) - bound(3 K) = {P(0.0) - P(3.0):.3e} W/m2")
demand = 20e6
need = (demand - U_fw) / (A * t)
lo, hi = 0.0, Ta                               # P decreases with Tc on [0, Ta]
for _ in range(200):
    mid = 0.5 * (lo + hi)
    lo, hi = (mid, hi) if P(mid) > need else (lo, mid)
print(f"S4-D | extra flux needed for demand 20 MJ: {need:.4f} W/m2; verdict flips at sky Tc = {lo:.2f} K")
check("S4-D", "verdict 'not excluded' only for sky colder than the flip temperature",
      P(lo - 1) > need > P(lo + 1), f"{lo:.2f} K")
P_dev = 27 / 256 * SIG * Ta**4                 # single emitter + Carnot engine (R29), a device value
U_dev = U_fw + P_dev * A * t
U_ult = U_fw + P(0.0) * A * t
print(f"S4-D | U with single-emitter value {P_dev:.4f} W/m2: {U_dev / 1e6:.6f} MJ; with ultimate bound: {U_ult / 1e6:.6f} MJ")
d2 = 25e6
check("S4-D", "demand 25 MJ: 'infeasible' if the device value is used as the bound, 'not excluded' with the ultimate bound",
      (d2 > U_dev) and not (d2 > U_ult), (d2 > U_dev, d2 > U_ult))

print("\n=== ROW SUMMARY ===")
for r, ok in _OK.items():
    print(f"{r}: {'PASS' if ok else 'FAIL'}")
