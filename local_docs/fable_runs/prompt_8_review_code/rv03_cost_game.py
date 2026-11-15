"""rv03: Task 4 of the Prompt 8 S5 review (claim 3, cooperative cost game).

Checks: (1) c(S) = F + v N_S (S non-empty), c(empty) = 0 is submodular (concave cost game);
(2) its core is {y_k = v N_k + f_k, f_k >= 0, sum f_k = F} (LP bounds on each y_k);
(3) the supporting-split interval for rv03's case; (4) the Shapley value depends on who the players are
(products vs equal blocks of positions); (5) the uniform-lambda condition; (6) the claim-6 "core may be
empty" under capacity steps c(S) = v N_S + F0 + F_step ceil(N_S/Q) (LP feasibility).
Level `derived` (unverified). numpy, scipy. Run: python rv03_cost_game.py
"""
import itertools
import math
import numpy as np
from scipy.optimize import linprog

T = 298.15
rng = np.random.default_rng(3)


def subsets(n):
    for r in range(1, n + 1):
        yield from itertools.combinations(range(n), r)


def shapley(c, n):
    phi = np.zeros(n)
    for k in range(n):
        others = [j for j in range(n) if j != k]
        for r in range(n):
            for S in itertools.combinations(others, r):
                w = math.factorial(r) * math.factorial(n - r - 1) / math.factorial(n)
                phi[k] += w * (c(tuple(sorted(S + (k,)))) - c(S))
    return phi


def core_bounds(c, n):
    """min and max of each y_k over the core {sum y = c(N), y(S) <= c(S)}; None if empty."""
    A, b = [], []
    for S in subsets(n):
        if len(S) < n:
            row = np.zeros(n); row[list(S)] = 1; A.append(row); b.append(c(S))
    Aeq, beq = [np.ones(n)], [c(tuple(range(n)))]
    out = []
    for k in range(n):
        for sgn in (1, -1):
            obj = np.zeros(n); obj[k] = sgn
            r = linprog(obj, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * n, method="highs")
            if r.status != 0:
                return None
            out.append(sgn * r.fun)
    return np.array(out).reshape(n, 2)


# (1)+(2) linear game
viol, core_ok = 0, 0
for _ in range(300):
    n = int(rng.integers(2, 6)); F = rng.uniform(1, 10); v = rng.uniform(0.1, 2); Ns = rng.uniform(1, 10, n)
    c = lambda S: 0.0 if len(S) == 0 else F + v * sum(Ns[list(S)])
    for S in itertools.chain([()], subsets(n)):
        for U in itertools.chain([()], subsets(n)):
            if c(tuple(sorted(set(S) | set(U)))) + c(tuple(sorted(set(S) & set(U)))) > c(S) + c(U) + 1e-9:
                viol += 1
    cb = core_bounds(c, n)
    if cb is not None and np.allclose(cb[:, 0], v * Ns, atol=1e-7) and np.allclose(cb[:, 1], v * Ns + F, atol=1e-7):
        core_ok += 1
print(f"G1 linear game: submodularity violations over 300 random games: {viol}")
print(f"G2 core equals {{v N_k <= y_k <= v N_k + F, sum = c(N)}} in {core_ok}/300 games")

# (3) supporting split, rv03 case
F, v, N1, N2, d1, d2 = 4e13, 2e4, 9e8, 1e8, 150.0, 400.0
lo = v / T
fs = np.linspace(0, 1, 100001)
ok = (lo + fs * F / (T * N1) > d1) & (lo + (1 - fs) * F / (T * N2) > d2)
print(f"G3 grid: splits f1/F where both per-product tests pass: [{fs[ok].min():.4f}, {fs[ok].max():.4f}]")

# (4) Shapley depends on the player definition
c2 = lambda S: 0.0 if len(S) == 0 else F + v * sum([N1, N2][k] for k in S)
sh = shapley(c2, 2)
print(f"G4 products as players: f1/F = {(sh[0]-v*N1)/F:.4f}, lambda1 = {sh[0]/(T*N1):.4f}, lambda2 = {sh[1]/(T*N2):.4f} J/K")
blocks = [1e8] * 10          # product 1 = blocks 0..8, product 2 = block 9 (equal blocks of 1e8 positions)
c10 = lambda S: 0.0 if len(S) == 0 else F + v * sum(blocks[k] for k in S)
sh10 = shapley(c10, 10)
f1 = sh10[:9].sum() - v * N1
print(f"G4 equal blocks of 1e8 positions as players: f1/F = {f1/F:.4f}, lambda1 = {sh10[:9].sum()/(T*N1):.4f}, "
      f"lambda2 = {sh10[9]/(T*N2):.4f} J/K (= per-position average share)")

# (5) uniform lambda: exists with N*lambda <= B/T and all tests passing iff max d < B/(T N)
mism = 0
for _ in range(20000):
    n = int(rng.integers(2, 6)); F = 10 ** rng.uniform(10, 14); v = 10 ** rng.uniform(2, 5)
    Ns = 10 ** rng.uniform(5, 9, n); B = F + v * Ns.sum()
    d = rng.uniform(0, 3, n) * B / (T * Ns.sum())
    exists = d.max() < B / (T * Ns.sum())       # lambda in (max d, B/(T N)]
    mism += exists != (d.max() < B / (T * Ns.sum()))
print(f"G5 uniform lambda condition is the definition itself (lambda in (max d_k, B/(T N)]); tautology check mismatches: {mism}")

# (6) capacity steps: can the core be empty?
F0, Fs, Q, vv = 1.0, 3.0, 10.0, 0.5
Ns3 = [4.0, 4.0, 4.0]
cs = lambda S: 0.0 if len(S) == 0 else vv * sum(Ns3[k] for k in S) + F0 + Fs * math.ceil(sum(Ns3[k] for k in S) / Q)
print(f"G6 steps (F0={F0}, F_step={Fs}, Q={Q}, N_k=4,4,4): c(i)={cs((0,)):.2f}, c(ij)={cs((0,1)):.2f}, c(N)={cs((0,1,2)):.2f}; "
      f"core {'EMPTY' if core_bounds(cs, 3) is None else 'non-empty'}")
Fs = 0.5
print(f"G6 steps with F_step={Fs} <= F0: core {'EMPTY' if core_bounds(cs, 3) is None else 'non-empty'}")
