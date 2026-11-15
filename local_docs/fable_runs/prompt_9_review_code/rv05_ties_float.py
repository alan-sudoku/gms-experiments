"""rv05: claim 8 - tie convention and the floating-point claim about ceil(tau/tau_w) at integer ratios.

Purpose: (a) check the left-continuity of f, the closed/open ends of the g-wins set at g and s
breakpoints, and the jump R_g - R_s at a coincident breakpoint, with exact rationals; (b) count how often
float64 ceil(tau/tau_w) differs from the exact integer when tau/tau_w is an exact integer, for inputs given
as decimal years converted to seconds, and in which direction (a spurious extra s replacement lowers f).
Task: S5 review task 6.
Assumptions: made-up profiles; K = 0 in (a) so only jumps matter; 1 yr = 365.25 d (the conversion is an
assumption of this script, not of the spec).
Level: derived.
"""
import math
from fractions import Fraction as Fr


def m_exact(T, w):
    return max(0, math.ceil(Fr(T) / Fr(w)) - 1)


print("(a) ties with exact rationals (K = 0, Sigma_dot equal, d0 chosen so f(0+) = -0.5)")
Rg, Rs = Fr(2), Fr(3)
twg, tws = Fr(6), Fr(4)
d0 = Fr(-1, 2)


def f(T):
    return d0 + m_exact(T, twg) * Rg - m_exact(T, tws) * Rs


eps = Fr(1, 10 ** 9)
for bp in [Fr(4), Fr(6), Fr(8), Fr(12)]:
    print(f"  tau = {bp}: f(tau-) = {float(f(bp - eps)):+.3f}, f(tau) = {float(f(bp)):+.3f},"
          f" f(tau+) = {float(f(bp + eps)):+.3f}; jump = {float(f(bp + eps) - f(bp)):+.3f}")
print("  f(tau) equals the left limit at every breakpoint: left-continuous. At tau = 12 (both sides) the jump is"
      f" R_g - R_s = {float(Rg - Rs):+.1f}")
print("  g-wins set {f < 0}: at a g breakpoint (jump up) an interval ends closed (tau = 6 is in, 6+ may not be);"
      " at an s breakpoint (jump down) an interval starts open (tau = 4 is not in if f(4) >= 0, 4+ is)")

print("\n(b) float64 ceil(tau/tau_w) at exact integer ratios, decimal-year inputs converted to seconds")
YR = 365.25 * 86400
over = under = total = 0
example_over = example_under = None
for tw_tenths in range(1, 400):          # tau_w from 0.1 to 39.9 yr in steps of 0.1
    for j in range(1, 30):
        tw_yr = Fr(tw_tenths, 10)
        tau_yr = j * tw_yr
        if tau_yr > 100:
            break
        total += 1
        tw_f = float(tw_yr) * YR             # as a config loader would: decimal string -> float -> seconds
        tau_f = float(tau_yr) * YR
        m_f = max(0, math.ceil(tau_f / tw_f) - 1)
        m_x = j - 1
        if m_f > m_x:
            over += 1
            example_over = example_over or (str(tau_yr), str(tw_yr), m_f, m_x)
        elif m_f < m_x:
            under += 1
            example_under = example_under or (str(tau_yr), str(tw_yr), m_f, m_x)
print(f"  integer-ratio cases: {total}; float m too high (spurious replacement): {over};"
      f" float m too low: {under}")
print(f"  first too-high example (tau yr, tau_w yr, m float, m exact): {example_over}")
print(f"  first too-low example: {example_under}")
print("  on side s a too-high m adds a spurious -R_s (f too low: favours g, unsafe); on side g a spurious +R_g"
      " (safe). A too-low m on side s drops a real -R_s at a horizon just above the tie (f too high, safe).")
