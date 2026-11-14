"""B6, B7: stress change equivalent to a life factor; conservatism of Basquin without endurance limit.

Spec rows B6, B7 (plan 3.3).  Pure closed-form arithmetic, hand values compared at the stated rounding.
B6: 2^(1/m), 10^(1/m), m in {3, 5, 9.804, 12, 19.608}.
B7: N/N_e = (s/s_e)^(-m) (extension), (s/s_e)^(-(2m-1)) (Haibach slope), infinity (cut-off);
    s/s_e in {0.95, 0.9, 0.8, 0.7, 0.5}; m in {5, 12}.
Both tables are formula evaluations compared with hand values from the same formulas: identity-level checks.
"""
import numpy as np
print("=== B6 ===")
ms = [3, 5, 9.804, 12, 19.608]
for m in ms:
    print(f"m={m}: 2^(1/m)={2**(1/m):.5f} 10^(1/m)={10**(1/m):.5f}")
hand2 = [1.260, 1.149, 1.073, 1.059, 1.036]
for m, h in zip(ms, hand2):
    v = 2 ** (1 / m)
    print(f"B6 hand 2^(1/m) m={m}: {h} calc {v:.4f} rounds to {round(v,3)} {'PASS' if round(v,3)==h else 'FAIL'}")
v = 10 ** (1 / 9.804)
print(f"B6 hand 10^(1/9.804): 1.265 calc {v:.4f} rounds to {round(v,3)} {'PASS' if round(v,3)==1.265 else 'FAIL'}")
print("B6 identity: hand values are the same expression 2^(1/m); only a rounding check.")
print("\n=== B7 ===")
for m in [5, 12]:
    for r in [0.95, 0.9, 0.8, 0.7, 0.5]:
        print(f"m={m:2d} s/s_e={r}: extension={r**-m:.4g} Haibach={r**-(2*m-1):.4g} cut-off=inf")
for lab, v, h in [("m=12 0.9 ext", 0.9**-12, 3.54), ("m=12 0.8 ext", 0.8**-12, 14.6), ("m=12 0.5 ext", 0.5**-12, 4096),
                  ("Haibach 0.9", 0.9**-23, 11.3), ("Haibach 0.8", 0.8**-23, 169), ("Haibach 0.5", 0.5**-23, 8.4e6)]:
    print(f"B7 hand {lab}: hand {h} calc {v:.5g} rel={abs(v-h)/h:.4f} {'PASS' if abs(v-h)/h<0.01 else 'FAIL'}")
print("B7 identity: hand values are the same expressions; no independent check.")
