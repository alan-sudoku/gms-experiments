"""Reviewer checks for L3 (Q2 closure), L10 (scrap), L6/L7/L11 (recovery test), L8 (lambda),
L4 (basis). All results are claims at level `derived` (unverified). numpy only.
Run: python3 rv03_ledger_and_misc.py > outputs/rv03_ledger_and_misc.txt
"""
import numpy as np

SIG = 5.670374419e-8
TREF = 298.15

# ---------------------------------------------------------------- A. Q2 closure, independent of S4-B
# Exergy balance from MASS FLOWS only (not from per-event charge increments):
#   resource exergy drawn  = CExC x (virgin moles drawn)
#   exergy still held      = b x (metal moles held at the end)
#   committed destruction  = drawn - held
# compared with the ANSWER's corrected formulas (L3) assembled through the prompt's structure
#   Sigma_init + m*R_g + Sigma_EOL, with w_conv = transport = mfg = 0 and w_rm = 0
#   (remelt is pure destruction with no stock, so it does not enter the balance).
rng = np.random.default_rng(7)
N = 100000
n = rng.uniform(0.1, 50, N)
b = rng.uniform(10, 1000, N)
CExC = b * (1 + rng.uniform(0.05, 20, N))
R = rng.uniform(0, 1, N)
m = rng.integers(0, 15, N)

virgin_moles = n + m * (1 - R) * n          # unit 0 fully virgin; each rebuild needs (1-R)n make-up
held_H2 = R * n                             # every unit retired at tau: only recovered stock held
held_H1 = n                                 # last unit still in service: n held
drawn = CExC * virgin_moles
init = n * (CExC - b)
ret = n * (1 - R) * CExC                    # answer: Sigma^ret = R w_rm + (1-R) CExC
eol = n * (1 - R) * b                       # answer: Sigma_g,EOL = R w_rm + (1-R) b
answer_total = init + m * ret + eol
prompt_total = init + m * n * (1 - R) * (CExC - b)   # as written: Sigma^ret has (1-R) w_ext, EOL no b
rel = lambda a, c: np.max(np.abs(a - c) / np.abs(c))
print(f"A1 answer's corrected total vs (drawn - held, all retired): max rel diff = {rel(answer_total, drawn - b*held_H2):.2e}")
print(f"A2 prompt as written vs (drawn - held, all retired): shortfall/(n b) min {np.min((drawn-b*held_H2-prompt_total)/(n*b)):.3f}, "
      f"equals (m+1)(1-R): {rel(drawn-b*held_H2-prompt_total, (m+1)*(1-R)*n*b):.2e}")
print(f"A3 answer's corrected total vs (drawn - held, last unit in service): (excess - (1-R)nb), max abs / (n b): "
      f"{np.max(np.abs(answer_total-(drawn-b*held_H1)-(1-R)*n*b)/(n*b)):.2e}  (the in-service unit's dispersal is charged before it occurs)")
# double count check: charge make-up at full CExC in Sigma^ret AND add (1-R) b at every dispersal
dd = init + m * (n * (1 - R) * CExC + n * (1 - R) * b) + eol
print(f"A4 'full CExC make-up + b at every dispersal' over-count minus m(1-R)nb, max abs / (n b): {np.max(np.abs(dd-(drawn-b*held_H2)-m*(1-R)*n*b)/(n*b)):.2e}")

# ---------------------------------------------------------------- B. L10 scrap formula vs V1
n_net, y, w_ext, w_conv, w_rm, Rs, b_ill = 20.0, 0.6, 1820.0, 100.0, 50.0, 0.95, 400.0   # b_ill made up
n_s = n_net * (1 / y - 1)
ans = n_s * ((1 - Rs) * w_ext + Rs * w_rm + w_conv)
v1 = n_s * ((1 - Rs) * (w_ext + b_ill) + Rs * w_rm + w_conv)
print(f"B  L10 scrap burden: answer {ans:.1f} kJ; with V1 dispersal of unrecovered scrap (b = {b_ill} kJ/mol, made up) {v1:.1f} kJ; "
      f"omitted {v1-ans:.1f} kJ ({(v1-ans)*1e3/TREF:.1f} J/K)")

# ---------------------------------------------------------------- C. L6 flip temperature, L7 sign convention, L11 crossover
Ta = 300.0
P = lambda Tc: SIG * (Ta**4 / 3 - 4 / 3 * Ta * Tc**3 + Tc**4)
need = (20e6 - 0.933 * 200 * 86400) / 86400
Tc_grid = np.linspace(0, Ta, 3000001)
Tflip = Tc_grid[np.argmin(np.abs(P(Tc_grid) - need))]
print(f"C1 extra flux needed {need:.4f} W/m2; sky temperature at which the verdict flips (grid) {Tflip:.3f} K")
q_mag, T0, Tsrc = 100.0, 300.0, 250.0
q_signed = -q_mag                 # standard convention: heat INTO the converter from the source; cold source -> negative
print(f"C2 cold source, q as magnitude: q(1-T0/Ts) = {q_mag*(1-T0/Tsrc):+.1f} W/m2; "
      f"q signed (into converter): {q_signed*(1-T0/Tsrc):+.1f} W/m2 (standard exergy-of-heat formula, already correct)")
eta = lambda T0, Ts: 1 - 4/3*T0/Ts + (T0/Ts)**4/3
lo, hi = 100.0, 400.0
for _ in range(200):
    mid = 0.5*(lo+hi)
    lo, hi = (mid, hi) if eta(mid, 5772.0) > 0.933 else (lo, mid)
print(f"C3 fixed 0.933 equals eta(T0, 5772 K) at T0 = {lo:.2f} K; at 300 K eta = {eta(300,5772):.6f} (fixed value safe); "
      f"at 250 K eta = {eta(250,5772):.6f}; at 200 K eta = {eta(200,5772):.6f}")
print(f"C4 relative understatement of the solar line at 200 K: {(eta(200,5772)-0.933)/eta(200,5772)*100:.2f} %; at 250 K: {(eta(250,5772)-0.933)/eta(250,5772)*100:.2f} %")

# ---------------------------------------------------------------- D. L8 lambda under the framework's own scope
F, v, Nu = 4.0e13, 2.0e4, 1.0e9
avoided_all = F + v * Nu
print(f"D1 'x leaves the whole system' (all N units switch): avoided {avoided_all:.3e} J = N x average share "
      f"({Nu*(F/Nu+v):.3e} J); per unit {avoided_all/Nu/TREF:.3f} J/K = lambda_avg")
print(f"D2 V7 default (marginal v) per unit in that same scenario: {v/TREF:.3f} J/K -> under-credits by "
      f"{(avoided_all/Nu - v)/TREF:.3f} J/K per unit if F is avoidable")
# per-unit test passing for one product does not imply the system test
N1, N2 = 9.0e8, 1.0e8
d1, d2 = 150.0, 400.0                 # Sigma_g - Sigma_s per unit [J/K], made up
lam = (F + v * (N1 + N2)) / (N1 + N2) / TREF
sys_ok = N1 * d1 + N2 * d2 < (F + v * (N1 + N2)) / TREF
print(f"D3 lambda = {lam:.3f} J/K; product 1 per-unit test {d1} < lambda: {d1 < lam}; product 2: {d2 < lam}; "
      f"system test (all switch): {sys_ok}. Per-unit rule keeps x in product 2, so x does not leave the system and the "
      f"lambda credited to product 1 is not earned; yet switching both passes the system test.")

# ---------------------------------------------------------------- E. L4 threshold is set by the made-up D
adv = 2.0 * 10 * 365.25 * 86400 / TREF
for D in (1e6, 4e6, 1e7):
    print(f"E  D = {D:.0e} J/K: break-even r_el = {D/adv:.3f}")
