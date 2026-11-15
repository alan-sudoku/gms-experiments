"""rv05: Task 5 cases (iv) staggered switching and (vi) uncertainty in d_k, Prompt 8 S5 review.

(iv) Assumptions (made up): rv03 numbers; the build part of F is sunk (existing incumbent), F is all
maintenance at rate m = F/H over a remaining infrastructure life H = 30 yr counted from now; v is a one-off
saving per position (U6); product k, if it switches, does so at its own date t_k. F_av(t_last) =
m max(0, H - t_last). Myopic sequential test: at t_k a product credits v/T only, unless every other user has
already left, in which case it credits v/T + F_av(t_k)/(T N_k).
(vi) d_k ~ Normal(mean, sd) independent; decisions are taken on the means; W(S) is linear in d for fixed S,
so the decision on means maximises expected W; the script reports the probability that the decision (or an
"unconditional" label) is wrong ex post, and the expected regret.
Level `derived` (unverified). numpy only. Run: python rv05_staggered_and_uncertainty.py
"""
import numpy as np

T = 298.15
F, v = 4e13, 2e4
N = np.array([9e8, 1e8])
d = np.array([150.0, 400.0])
H = 30.0
m = F / H
lo = v / T

print("== (iv) staggered switching ==")
phi = N * (d - lo) * T / F
print(f"sum phi (F_av = F) = {phi.sum():.5f}; all-exit worth it iff F_av(t_last) > sum phi * F, "
      f"i.e. t_last < H (1 - sum phi) = {H*(1-phi.sum()):.3f} yr")
for dates in ((2.0, 4.0), (2.0, 8.0), (0.0, 0.0)):
    tl = max(dates)
    Fav = m * max(0.0, H - tl)
    Wall = (v * N.sum() + Fav) / T - (N * d).sum()
    lam_hi_last = lo + Fav / (T * N[np.argmax(dates)])
    # myopic sequential: earliest first; a product sees lambda_hi only if all others already left
    left = []
    for k in np.argsort(dates):
        others_left = all(j in left for j in range(2) if j != k)
        lam = lo + (m * max(0.0, H - dates[k]) / (T * N[k]) if others_left else 0.0)
        if d[k] < lam:
            left.append(k)
    print(f"dates {dates}: F_av = {Fav:.4e} J, W(all, committed) = {Wall:+.4e} J/K, lambda_hi of last mover = "
          f"{lam_hi_last:.2f} J/K; myopic sequential outcome: {[k+1 for k in left]} (W = 0)")
print(f"E16 average share ignores dates: lambda = {(F + v*N.sum())/(T*N.sum()):.2f} J/K at any t_last")

print("\n== (vi) uncertainty in d_k, rv03 case, decision 'all switch' on the means ==")
rng = np.random.default_rng(6)
M = 400000
B_T = (F + v * N.sum()) / T
print(f"system-verdict edges: d1* = {(B_T - N[1]*d[1])/N[0]:.3f} J/K (mean 150), d2* = {(B_T - N[0]*d[0])/N[1]:.3f} J/K (mean 400)")
for rel in (0.05, 0.10, 0.20, 0.30):
    D = d + rng.normal(0, 1, (M, 2)) * d * rel
    Wall = B_T - D @ N
    W1 = N[0] * (lo - D[:, 0]); W2 = N[1] * (lo - D[:, 1])
    best = np.maximum.reduce([np.zeros(M), W1, W2, Wall])
    regret = best - Wall
    print(f"sd = {rel*100:4.0f} % of each d: P(all-switch is not the ex-post optimum) = {np.mean(regret > 0):.4f}, "
          f"E[regret] = {regret.mean():.3e} J/K, E[W(all)] = {Wall.mean():+.3e} J/K")
print("\n-- 'unconditional pass' label near the lower edge v/T (product with N = 1e8, sd = 10 J/K) --")
for mean in (40.0, 55.0, 60.0, 65.0):
    D = mean + rng.normal(0, 10.0, M)
    print(f"mean d = {mean} J/K: label 'unconditional pass' (mean < {lo:.2f}); P(true d > v/T) = {np.mean(D > lo):.4f}")
print("\n-- F_av uncertainty: alpha margin --")
print(f"verdict flips at alpha = sum phi = {phi.sum():.4f}; margin {1-phi.sum():.4f} of F")
