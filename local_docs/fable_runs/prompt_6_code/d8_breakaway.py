"""D8: breakaway, metal loss relative to the parabolic law.

Spec row: D8.  Claim level: derived (unverified).

h(tau)/h_par(tau) = [1 + kappa (tau/t_b - 1)/2] / sqrt(tau/t_b) for tau > t_b, else 1.
Independent construction: h_par = sqrt(2 kp tau); after t_b the loss continues
linearly at r_b = kappa * h_b/(2 t_b), h_b = sqrt(2 kp t_b), so
h = h_b + r_b (tau - t_b).  Ratio computed from that (kp = 1e-17, t_b = 3600 s,
which cancel).  Tau/t_b grid {0.5, 0.9, 1, 1.1, 2, 10, 100}; kappa {1, 10, 100}.
numpy only.
"""
import math

KP, TB = 1e-17, 3600.0
KAPPAS = [1, 10, 100]
X = [0.5, 0.9, 1.0, 1.1, 2.0, 10.0, 100.0]


def ratio_formula(x, k):
    return 1.0 if x <= 1 else (1 + k * (x - 1) / 2) / math.sqrt(x)


def ratio_construct(x, k):
    tau = x * TB
    hpar = math.sqrt(2 * KP * tau)
    if x <= 1:
        return hpar / hpar
    hb = math.sqrt(2 * KP * TB)
    rb = k * hb / (2 * TB)
    return (hb + rb * (tau - TB)) / hpar


print("=" * 70)
print("D8: breakaway metal loss relative to the parabolic law  (level: derived)")
print("=" * 70)
print(f"{'tau/t_b':>8} " + " ".join(f"kappa={k:>4}" .rjust(14) for k in KAPPAS))
worst = 0.0
for x in X:
    row = []
    for k in KAPPAS:
        a, b = ratio_formula(x, k), ratio_construct(x, k)
        worst = max(worst, abs(a / b - 1))
        row.append(f"{a:14.6f}")
    print(f"{x:8g} " + " ".join(row))
print(f"\nformula vs independent construction (h_b + r_b (tau - t_b)): max rel diff {worst:.2e} "
      f"-> {'PASS' if worst < 1e-12 else 'FAIL'} (tolerance exact)")
below = all(ratio_formula(x, k) == 1.0 for x in X if x <= 1 for k in KAPPAS)
print(f"ratio = 1 for tau/t_b <= 1: {'PASS' if below else 'FAIL'}.  The sweep brackets the onset: "
      "points below (0.5, 0.9), at (1.0) and above (1.1) t_b are all present.  "
      "At tau/t_b = 1.1 the ratio is " + ", ".join(f"{ratio_formula(1.1,k):.4f} (kappa {k})" for k in KAPPAS)
      + ", i.e. > 1 for every kappa, so the departure from 1 is visible on the grid.")
print("  (the ratio for tau <= t_b is 1 by definition: that part is an IDENTITY; the first-segment "
      "'construct' branch divides hpar by itself.)")
print("\nHand values (exact tolerance, stated to 3 digits):")
for x, k, h in [(2, 1, 1.06), (10, 1, 1.74), (10, 10, 14.5)]:
    v = ratio_formula(x, k)
    print(f"  kappa = {k}, tau/t_b = {x}: {v:.4f} vs hand {h} -> dev {abs(v/h-1):.2%} "
          f"{'PASS' if f'{v:.3g}' == f'{h:.3g}' else 'FAIL'} (3 significant digits)")
