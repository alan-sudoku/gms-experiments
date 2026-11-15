"""rv02: Tasks 2 and 3 of the Prompt 8 S5 review.

Task 3: enumerate all subsets for random linear profiles (2-6 products, including ties d_k = v/T,
d_k < v/T, and F/T = sum N_k max(0, d_k - v/T) exactly) and check claim 1: the optimum value equals
max(W(S_m), W(all)) and "all switch iff F/T > sum N_k max(0, d_k - v/T)".
Task 2: (a) for own-product data (F, v, N, N_k, d_k), construct two profiles of the other products that
give opposite optimal verdicts for product k; show this exists exactly when v/T < d_k < v/T + F/(T N_k)
and N > N_k; (b) check that the answer's three-way rule is sound (never a wrong unconditional verdict)
in the linear model and is complete only outside that band.
Model: linear B_infra = F + v N, F avoided only when every user leaves, no outside users, simultaneous.
Level `derived` (unverified). numpy only. Run: python rv02_impossibility_and_enumeration.py
"""
import itertools
import numpy as np

T = 298.15
rng = np.random.default_rng(20261115)


def W(S, d, Ns, F, v):
    w = sum(Ns[k] * (v / T - d[k]) for k in S)
    if len(S) == len(Ns):
        w += F / T
    return w


def enum(d, Ns, F, v):
    n = len(d)
    vals = {S: W(S, d, Ns, F, v) for r in range(n + 1) for S in itertools.combinations(range(n), r)}
    best = max(vals.values())
    return vals, best


# ------------------------------------------------------------------ Task 3
n_cases, viol_val, viol_cond, ties_seen = 0, 0, 0, 0
for trial in range(20000):
    n = int(rng.integers(2, 7))
    F = 10 ** rng.uniform(10, 14)
    v = 10 ** rng.uniform(2, 5)
    Ns = 10 ** rng.uniform(5, 9, n)
    lo = v / T
    d = lo + rng.normal(0, 1, n) * (F / T / Ns.sum()) * rng.uniform(0.1, 5)
    kind = trial % 4
    if kind == 1:                      # ties at d_k = v/T
        d[rng.integers(0, n)] = lo
    if kind == 2:                      # force exact tie in the switching condition
        excess = np.maximum(0, d - lo) * Ns
        if excess.sum() > 0:
            F = T * excess.sum()
            ties_seen += 1
    if kind == 3:                      # some products below v/T
        d[: max(1, n // 2)] = lo - np.abs(d[: max(1, n // 2)] - lo)
    vals, best = enum(d, Ns, F, v)
    Sm = tuple(k for k in range(n) if d[k] < lo)
    two = max(W(Sm, d, Ns, F, v), W(tuple(range(n)), d, Ns, F, v))
    scale = F / T + Ns.sum() * abs(d).max()
    if abs(best - two) > 1e-9 * scale:
        viol_val += 1
    cond_all = F / T > (Ns * np.maximum(0, d - lo)).sum()
    allbest = W(tuple(range(n)), d, Ns, F, v) >= best - 1e-9 * scale
    smbest = W(Sm, d, Ns, F, v) >= best - 1e-9 * scale
    # claim 1: all is optimal iff condition (ties: both optimal)
    if cond_all and not allbest:
        viol_cond += 1
    if (not cond_all) and not smbest:
        viol_cond += 1
    n_cases += 1
print(f"T3 enumerated {n_cases} random profiles (n = 2..6; {ties_seen} with exact tie F/T = sum excess):")
print(f"T3 optimum != max(W(S_m), W(all)): {viol_val} cases; switching-condition violations: {viol_cond} cases")

# ------------------------------------------------------------------ Task 2a: impossibility exists exactly in the band
F, v = 4.0e13, 2.0e4
lo = v / T
Nk, Nother = 9.0e8, 1.0e8
hi = lo + F / (T * Nk)
print(f"\nT2a band for product 1 (N1=9e8, N=1e9): ({lo:.4f}, {hi:.4f}) J/K")
for dk in (60.0, lo + 1e-6, 100.0, 150.0, 216.0, hi + 1e-3, 300.0):
    # profile A: the other product has d_j = v/T - 1 (phi_j = 0) -> all optimal iff phi_k < 1
    # profile B: the other product has d_j huge -> all never optimal
    res = []
    for dj in (lo - 1.0, 1e6):
        vals, best = enum([dk, dj], [Nk, Nother], F, v)
        opt = [S for S, w in vals.items() if w >= best - 1e-6]
        res.append(sorted({0 in S for S in opt}))
    print(f"T2a d1 = {dk:10.4f}: product-1 membership in optimum, profile A (d2 = v/T-1): {res[0]}, "
          f"profile B (d2 = 1e6): {res[1]} -> own data decide: {res[0] == res[1] and len(res[0]) == 1}")
# no other product: N = N_k
vals, best = enum([150.0], [Nk], F, v)
print(f"T2a sole user (N = N_k): d1 = 150, W(all) = {W((0,), [150.0], [Nk], F, v):+.4e} J/K -> own data decide "
      f"(no impossibility)")

# ------------------------------------------------------------------ Task 2b: soundness of the answer's three-way rule
wrong_uncond, conditional, total = 0, 0, 0
for trial in range(20000):
    n = int(rng.integers(2, 7))
    F = 10 ** rng.uniform(10, 14)
    v = 10 ** rng.uniform(2, 5)
    Ns = 10 ** rng.uniform(5, 9, n)
    lo = v / T
    d = lo + rng.normal(0, 1, n) * (F / T / Ns.sum()) * rng.uniform(0.1, 5)
    vals, best = enum(d, Ns, F, v)
    scale = F / T + Ns.sum() * abs(d).max()
    opt = [S for S, w in vals.items() if w >= best - 1e-9 * scale]
    for k in range(n):
        total += 1
        in_all = all(k in S for S in opt)
        in_none = all(k not in S for S in opt)
        if d[k] < lo:
            wrong_uncond += not in_all
        elif d[k] > lo + F / (T * Ns[k]):
            wrong_uncond += not in_none
        else:
            conditional += 1
print(f"\nT2b answer's three-way rule over {total} product verdicts: wrong unconditional verdicts = {wrong_uncond}; "
      f"conditional = {conditional} ({100*conditional/total:.1f} %)")
