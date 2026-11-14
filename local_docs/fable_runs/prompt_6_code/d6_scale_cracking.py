"""D6: scale cracking strain versus cyclic strain amplitude.

Spec row: D6.  Claim level: derived (unverified).

eps_c(K_Ic, c) = K_Ic/(f E_ox sqrt(pi c)); crossover flaw size
c_x = (1/pi) (K_Ic/(f E_ox eps_a))^2, confirmed independently by bisection on ln c
over [1e-9, 1e-3] m of eps_c(c) - eps_a.

NEEDS C1: sigma_a0 is a NAMED INPUT below, set to the planner's value 108.7 MPa
(not computed here).  If row C1 (computed by another agent) gives a different value,
the FINAL PASS MUST RE-RUN D6 with that value (edit SIGMA_A0_MPA at the top).

Inputs: K_Ic grid 0.5, 1, 2, 4 MPa sqrt(m) (M19); f = 1.12 (M15); E_ox = 380 GPa (M17);
E = 73 GPa (M05); flaw sizes 0.01 .. 100 um.  numpy/plain Python only.
"""
import math
import numpy as np

SIGMA_A0_MPA = 108.7          # MPa; planner's value for C1 (re-run D6 if C1 differs)
E_AL = 73e9
E_OX = 380e9
F = 1.12
KIC = [0.5, 1.0, 2.0, 4.0]    # MPa sqrt(m)
CS = [0.01e-6, 0.1e-6, 1e-6, 10e-6, 100e-6]

eps_a = SIGMA_A0_MPA * 1e6 / E_AL


def eps_c(K, c):
    return K * 1e6 / (F * E_OX * math.sqrt(math.pi * c))


def bisect_lnc(K, lo=1e-9, hi=1e-3):
    g = lambda lc: eps_c(K, math.exp(lc)) - eps_a
    a, b = math.log(lo), math.log(hi)
    ga, gb = g(a), g(b)
    if ga * gb > 0:
        return None, ga, gb
    for _ in range(300):
        mid = 0.5 * (a + b)
        gm = g(mid)
        if ga * gm <= 0:
            b, gb = mid, gm
        else:
            a, ga = mid, gm
        if (b - a) <= 1e-12 * max(abs(a), abs(b)):
            break
    return math.exp(0.5 * (a + b)), g(math.log(lo)), g(math.log(hi))


print("=" * 70)
print("D6: scale cracking strain vs cyclic strain amplitude  (level: derived)")
print("=" * 70)
print(f"INPUT sigma_a0 = {SIGMA_A0_MPA} MPa (planner value, NOT from C1 run); "
      f"eps_a = sigma_a0/E = {eps_a:.4e}")
print("FINAL PASS: re-run D6 if C1 gives a different sigma_a0.")
print(f"\neps_c [1e-3] (K_Ic rows, flaw size columns); '*' = eps_c < eps_a (scale cracks under eps_a)")
print(f"{'K_Ic':>6} " + " ".join(f"c={c*1e6:>7g}um" for c in CS))
for K in KIC:
    print(f"{K:6g} " + " ".join(f"{eps_c(K, c)*1e3:8.4f}{'*' if eps_c(K, c) < eps_a else ' '} " for c in CS))
v = eps_c(1.0, 1e-6)
print(f"\nhand check eps_c(c = 1 um, K_Ic = 1) = {v*1e3:.4f}e-3 (hand 1.33e-3): "
      f"{'PASS' if abs(v/1.33e-3-1) <= 0.02 else 'FAIL'}")
print(f"hand check eps_a = {eps_a*1e3:.4f}e-3 (hand 1.49e-3): "
      f"{'PASS' if abs(eps_a/1.49e-3-1) <= 0.02 else 'FAIL'}")
print("\nCrossover flaw size c_x [um]: closed form vs bisection on ln c in [1e-9, 1e-3] m")
hand = {1.0: 0.79, 0.5: 0.20, 4.0: 12.7}
for K in KIC:
    cx = (1 / math.pi) * (K * 1e6 / (F * E_OX * eps_a)) ** 2
    r, ga, gb = bisect_lnc(K)
    if r is None:
        print(f"  K_Ic = {K}: NO BRACKET: end values {ga:.4e}, {gb:.4e}")
        continue
    hs = f", hand {hand[K]} -> dev {abs(cx*1e6/hand[K]-1):.2%}" if K in hand else ""
    print(f"  K_Ic = {K:3g}: closed {cx*1e6:9.4f} um, bisection {r*1e6:9.4f} um, rel diff "
          f"{abs(r/cx-1):.2e}; bracket end values {ga:+.3e}, {gb:+.3e} (sign change: yes){hs}")
print("  (bisection works on eps_c(c) directly, independent of the closed-form inversion; "
      "its bracket genuinely contained each root. Hand values +-2 %.)")
