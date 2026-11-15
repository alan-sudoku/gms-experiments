"""rv01: reproduce the example arithmetic of the Prompt 9 answer.

Purpose: recompute f_inf = 4.4e6, f = 4.4e6 - 2 R_s, the flip at 2.2e6, the omitted-stage
thresholds 1.2e6 and 0.8e6, the value -2.1e6, and test omega* = f/(m_s+1) when the omitted
first-unit stage and the omitted replacement stage differ.
Task: S5 review task 1 and task 3 (omega*).
Assumptions: the block's made-up example (tau = 20 yr, all K = 0, equal Sigma_dot, so the
Sigma_dot terms cancel); m_k = max(0, ceil(tau/tau_w) - 1) evaluated with exact rationals.
Level: derived (arithmetic only; no external evidence).
"""
from fractions import Fraction as F
import math


def m_count(tau, tw):
    # exact ceil on rationals
    q = F(tau) / F(tw)
    return max(0, math.ceil(q) - 1)


M = F(10) ** 6
tau = 20
g = dict(init=F(3) * M, R=F(2) * M, EOL=F(2, 10) * M, tw=6)
s = dict(init=F(4) * M, EOL=F(3, 10) * M, tw=8)
lam = F(5, 10) * M

mg = m_count(tau, g["tw"])
ms = m_count(tau, s["tw"])
print(f"m_g = {mg}, m_s = {ms}")
Sg = g["init"] + mg * g["R"] + g["EOL"]
Ss_inf = s["init"] + s["EOL"]
f_inf = Sg - Ss_inf - lam
print(f"Sigma_g = {float(Sg):.4g} J/K; Sigma_s(inf) = {float(Ss_inf):.4g} J/K")
print(f"f_inf = {float(f_inf):.4g} J/K  (answer: 4.4e6)")


def f_of_Rs(Rs, extra_init=0):
    return Sg - (s["init"] + extra_init + ms * Rs + s["EOL"]) - lam


print(f"f(R_s) = {float(f_inf):.4g} - {ms}*R_s")
print(f"flip at R_s = f_inf/m_s = {float(f_inf / ms):.4g} J/K  (answer: 2.2e6)")
print(f"f(R_s=1.0e6) = {float(f_of_Rs(M)):.4g} J/K  (block: 2.4e6)")
print(f"f(R_s=2.5e6) = {float(f_of_Rs(F(25, 10) * M)):.4g} J/K  (block: -0.6e6)")
f_decl = f_of_Rs(M)
print(f"omega_rep threshold (replacement only, m_s units) = {float(f_decl / ms):.4g} J/K  (answer: 1.2e6)")
print(f"omega threshold (first unit too, m_s+1 units) = {float(f_decl / (ms + 1)):.4g} J/K  (answer: 0.8e6)")
print(f"f(R_s=2.5e6, Sigma_s,init + 1.5e6) = {float(f_of_Rs(F(25, 10) * M, F(15, 10) * M)):.4g} J/K  (answer: -2.1e6)")
print(f"same via 2.4e6 - 3*1.5e6 = {float(f_decl - 3 * F(15, 10) * M):.4g} J/K")

print("\n-- omega* = f/(m_s+1) when omega_init != omega_rep --")
# omitted totals Omega = omega_init + m_s*omega_rep; 'g loses' is wrong iff Omega > f
cases = [(F(8, 10) * M, F(8, 10) * M), (F(2) * M, F(3, 10) * M), (F(1, 10) * M, F(11, 10) * M)]
for wi, wr in cases:
    Om = wi + ms * wr
    flip = Om > f_decl
    per_unit_test = max(wi, wr) > f_decl / (ms + 1)
    mean_test = Om / (ms + 1) > f_decl / (ms + 1)
    print(f"omega_init={float(wi):.3g}, omega_rep={float(wr):.3g}: Omega={float(Om):.3g}, "
          f"true flip={flip}; 'max(omega) > omega*'={per_unit_test}; 'mean omega > omega*'={mean_test}")
print("omega* is exact only as the per-unit mean of the omitted total Omega = omega_init + m_s*omega_rep;"
      " the break-even quantity is Omega* = f (J/K) itself.")
