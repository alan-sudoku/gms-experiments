"""C1 baseline stress amplitude / air life and C2 cross-check against an independent S-N curve.

Spec rows: C1, C2. Inputs M02, M03, M04, L07 (MIL-HDBK-5J 2024-T3 equation, planner's value, UNSURE
because the source figure was not verified; see data/SOURCES.md).
Assumptions: C2 evaluates log10 N = 11.1 - 3.97 log10(S_eq - 15.8), S_eq = S_max (1-R)^0.56 (ksi),
R = -1, S_max = sigma_a0.  The implied shift in rho is N/N0 (rho = tau0/t_c scales with life).
C2 is plausibility only (no pass/fail tolerance), flagged if N/N0 outside [0.03, 30].
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
from c_common import *

s0 = sigma_a0()
print("C1  sigma_a0 = sigma_f' (2 N0)^b = %.6f MPa   <<<  (expected ~108.7, accept 105..112, tol 0.5%%)" % s0)
print("    deviation from 108.7: %.3f %%  -> %s" % ((s0 / 108.7 - 1) * 100, "PASS" if abs(s0 / 108.7 - 1) <= 0.005 else "FAIL"))
print("    m = -1/b = %.5f (expected 9.804) -> %s" % (M_EXP, "PASS" if abs(M_EXP / 9.804 - 1) <= 0.005 else "FAIL"))
exp = {0.01: 1584, 0.1: 158.4, 1: 15.84, 10: 1.584}
ok = True
for nu in (0.01, 0.1, 1, 10):
    t = tau0_years(nu)
    good = abs(t / exp[nu] - 1) <= 0.005
    ok &= good
    print("    nu=%-5g Hz tau0 = %.4f yr (expected %g) %s" % (nu, t, exp[nu], "PASS" if good else "FAIL"))
print("C1 overall:", "PASS" if (abs(s0/108.7-1)<=0.005 and ok) else "FAIL")
print("    note: expected values are the planner's own arithmetic from the same formula (M02-M04); the check is an arithmetic re-computation, not independent evidence.")

print()
S_max_ksi = s0 / KSI
R = -1.0
S_eq = S_max_ksi * (1 - R) ** 0.56
x = S_eq - 15.8
logN = 11.1 - 3.97 * math.log10(x)
N = 10 ** logN
print("C2  S_max = %.4f ksi, S_eq = %.4f ksi, S_eq-15.8 = %.4f, log10 N = %.4f" % (S_max_ksi, S_eq, x, logN))
print("    N = %.4e cycles; N/N0 = %.4f (planner expects ~4e7, ~0.09)" % (N, N / N0))
print("    plausibility window [0.03, 30]: %s" % ("inside" if 0.03 <= N / N0 <= 30 else "OUTSIDE: flag baseline"))
print("    implied shift in rho = N/N0 -> rho_(L07) = %.4f x rho_(baseline); life factor F would be scaled by the same %.4f" % (N / N0, N / N0))
print("    C2 verdict: report only (no tolerance). L07 coefficients are NOT verified from the source (UNSURE).")
