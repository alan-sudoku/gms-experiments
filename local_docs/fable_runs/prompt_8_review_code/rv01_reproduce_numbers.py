"""rv01: reproduce every number in prompt_8_web_answer.md (claims 1-7) and rv03 D1-D3.

Task 1 of the Prompt 8 S5 review. Linear model of the question block:
B_infra = F + v*N, credit for "all users leave" only, d_k = Sigma_g - Sigma_s per position,
W(S) = sum_{k in S} N_k (v/T - d_k) + [S = all] F/T  (J/K, positive = irreversibility saved).
Inputs are the made-up numbers of rv03 D1-D3. T = T_ref = 298.15 K (the question's T; the spec uses T0).
Level `derived` (unverified). numpy only.
Run: python rv01_reproduce_numbers.py
"""
import itertools

T = 298.15
F, v = 4.0e13, 2.0e4
N1, N2 = 9.0e8, 1.0e8
N = N1 + N2
d1, d2 = 150.0, 400.0
lo = v / T


def W(S, d, Ns, Fav=F):
    w = sum(Ns[k] * (lo - d[k]) for k in S)
    if len(S) == len(Ns):
        w += Fav / T
    return w


print("== rv03 D1-D3 recomputed independently ==")
print(f"lambda_avg = (F + v N)/(T N) = {(F + v*N)/(T*N):.4f} J/K")
print(f"v/T = {lo:.4f} J/K ; under-credit when both switch = {(F + v*N)/(T*N) - lo:.4f} J/K")
print(f"N1 d1 + N2 d2 = {N1*d1 + N2*d2:.4e} J/K ; B_infra/T = {(F + v*N)/T:.5e} J/K")

print("\n== claim 1 ==")
e1, e2 = N1 * max(0, d1 - lo), N2 * max(0, d2 - lo)
print(f"F/T = {F/T:.5e} J/K ; N1(d1-v/T) = {e1:.4e} ; N2(d2-v/T) = {e2:.4e} ; sum = {e1+e2:.5e}")
d, Ns = [d1, d2], [N1, N2]
for S in [(), (0,), (1,), (0, 1)]:
    print(f"W({[k+1 for k in S]}) = {W(S, d, Ns):+.4e} J/K")

print("\n== claim 2 ==")
d2b = 700.0
print(f"d2=700: N1 d1 + N2 d2 = {N1*d1 + N2*d2b:.4e} J/K vs B/T = {(F+v*N)/T:.5e}")
for S in [(), (0,), (1,), (0, 1)]:
    print(f"  W({[k+1 for k in S]}) at d2=700 = {W(S, [d1, d2b], Ns):+.4e} J/K")
print(f"flip d2* = ((F+vN)/T - N1 d1)/N2 = {((F+v*N)/T - N1*d1)/N2:.4f} J/K")

print("\n== claim 3 ==")
phi1 = N1 * (d1 - lo) * T / F
phi2 = N2 * (d2 - lo) * T / F
print(f"phi1 = {phi1:.5f}, phi2 = {phi2:.5f}, sum = {phi1+phi2:.5f}")
print(f"supporting interval f1/F in ({phi1:.4f}, {1-phi2:.4f})")
print(f"per-position split f1/F = N1/N = {N1/N:.3f} -> lambda = {lo + F*N1/N/(T*N1):.4f} J/K for both")
print(f"Shapley (products as players, F/2 each): lambda1 = {lo + F/2/(T*N1):.4f}, lambda2 = {lo + F/2/(T*N2):.4f} J/K")
print(f"uniform-lambda condition: max d_k = {max(d1,d2)} < B/(T N) = {(F+v*N)/(T*N):.4f}: {max(d1,d2) < (F+v*N)/(T*N)}")

print("\n== claim 4 ==")
print(f"lambda_hi,1 = {lo + F/(T*N1):.4f} J/K ; lambda_hi,2 = {lo + F/(T*N2):.4f} J/K")

print("\n== claim 5 ==")
d1c = 50.0
print(f"d1=50: W({{1}}) = {N1*(lo - d1c):+.4e} J/K ; W(all) at d1=50,d2=400 = {W((0,1), [d1c, d2], Ns):+.4e} J/K ; "
      f"W(none) = 0")

print("\n== claim 6 (alpha) ==")
for a in (0.8, phi1 + phi2):
    print(f"alpha = {a:.5f}: W(all) = {W((0,1), d, Ns, Fav=a*F):+.4e} J/K")

print("\n== claim 7 ==")
print(f"bracket widths F/(T N1) = {F/(T*N1):.4f} J/K, F/(T N2) = {F/(T*N2):.4f} J/K")
best = max((W(S, d, Ns), S) for S in [(), (0,), (1,), (0, 1)])
print(f"optimum W = {best[0]:.4e} J/K at S = {[k+1 for k in best[1]]}; marginal-only picks S_m = [] (W=0) -> forgoes {best[0]:.4e}")
print(f"average rule, product 1 alone: W({{1}}) = {W((0,), d, Ns):+.4e} J/K (vs none); loss vs optimum = {best[0]-W((0,), d, Ns):.4e} J/K")
