"""rv03: claims 4 and 5 - given life versus chosen replacement interval.

Purpose: re-derive the renewal stationarity condition int_0^T a sigma'(a) da = R, T* = sqrt(2R/beta),
the K sqrt(a) and mixed forms; the finite-horizon condition R < beta tau^2/4 for one replacement;
and test by brute force (over n and over unequal splits) that equal intervals are optimal for
convex per-unit loss L, plus the K sqrt(a) and mixed (sigma0 + beta a plus K sqrt a) cases, with and
without a given life (failure or performance limit) t_max.
Task: S5 review task 4.
Assumptions: per-unit loss L(t) = int_0^t sigma(a) da; n units in sequence with lengths t_i summing to
tau; cost (n-1) R + sum L(t_i); all numbers made up; optimisation by scipy SLSQP from many starts
(a numerical supplement, the convex case is also proved by Jensen).
Level: derived.
"""
import math

import numpy as np
import sympy as sp
from scipy.optimize import minimize

print("(a) symbolic")
a, T, R, beta, K, s0 = sp.symbols("a T R beta K sigma0", positive=True)
sig = sp.Function("sigma")
c = (R + sp.Integral(sig(a), (a, 0, T))) / T
num = sp.simplify(sp.diff(c, T) * T ** 2)
print("  T^2 dc/dT =", num, " -> zero iff T sigma(T) - int sigma = R = int_0^T a sigma'(a) da (by parts)")
lin = sp.integrate(a * sp.diff(s0 + beta * a, a), (a, 0, T))
print("  linear sigma: int a sigma' =", lin, "; T* =", sp.solve(sp.Eq(lin, R), T))
sq = sp.integrate(a * sp.diff(sp.diff(K * sp.sqrt(a), a), a), (a, 0, T))
print("  K sqrt(a) loss (sigma = K/(2 sqrt a)): int a sigma' =", sp.simplify(sq), "< 0, never replace voluntarily")
mix = sp.simplify(lin + sq)
print("  mixed: int a sigma' =", mix, "= R")
tau = sp.symbols("tau", positive=True)
L = lambda t: s0 * t + beta * t ** 2 / 2
print("  finite horizon, linear: L(tau) - [R + 2 L(tau/2)] =", sp.simplify(L(tau) - (R + 2 * L(tau / 2))),
      "> 0 iff R < beta tau^2/4")
n = sp.symbols("n", positive=True, integer=True)
gain_n = sp.simplify(L(tau) - ((n - 1) * R + n * L(tau / n)))
print("  gain of n equal units over 1 unit:", sp.factor(gain_n), "; per extra replacement the break-even R is beta tau^2/(2n),"
      " largest at n = 2, so 'replacing at all pays iff R < beta tau^2/4' holds")


def best_split(Lf, n, tau_, tmax=None, starts=40, seed=0):
    rng = np.random.default_rng(seed)
    best = (math.inf, None)
    bounds = [(1e-9, tmax if tmax else tau_)] * n
    cons = [{"type": "eq", "fun": lambda x: np.sum(x) - tau_}]
    for _ in range(starts):
        x0 = rng.dirichlet(np.ones(n)) * tau_
        if tmax:
            x0 = np.minimum(x0, tmax)
            x0 = x0 * tau_ / x0.sum()
        res = minimize(lambda x: sum(Lf(t) for t in x), x0, bounds=bounds, constraints=cons, method="SLSQP",
                       options={"ftol": 1e-12, "maxiter": 500})
        if res.success and abs(res.x.sum() - tau_) < 1e-6 and (tmax is None or res.x.max() <= tmax + 1e-6):
            if res.fun < best[0]:
                best = (res.fun, np.sort(res.x))
    return best


def report(name, Lf, Rv, tau_, tmax=None, nmax=8):
    print(f"\n  case {name}: R = {Rv}, tau = {tau_}, t_max = {tmax}")
    nmin = 1 if tmax is None else math.ceil(tau_ / tmax - 1e-12)
    rows = []
    for nn in range(max(1, nmin), nmax + 1):
        if tmax and tau_ / nn > tmax + 1e-12 and nn < nmin:
            continue
        eq = (nn - 1) * Rv + nn * Lf(tau_ / nn) if (tmax is None or tau_ / nn <= tmax + 1e-12) else math.inf
        bs = best_split(Lf, nn, tau_, tmax)
        opt = (nn - 1) * Rv + bs[0]
        rows.append((nn, eq, opt, bs[1]))
        print(f"    n={nn}: equal split {eq:9.4f}; best split {opt:9.4f}; lengths {np.round(bs[1], 3)}")
    nbest = min(rows, key=lambda r: r[2])
    print(f"    optimum n = {nbest[0]}, cost {nbest[2]:.4f}; equal split optimal at that n: "
          f"{abs(nbest[1] - nbest[2]) < 1e-6}")
    return rows


print("\n(b) brute force")
tau_, b_, s0_, K_ = 20.0, 0.1, 1.0, 3.0
report("linear (convex)", lambda t: s0_ * t + b_ * t * t / 2, 1.0, tau_)
print(f"    T* = sqrt(2R/beta) = {math.sqrt(2 * 1.0 / b_):.4f}; tau/T* = {tau_ / math.sqrt(2 / b_):.3f}")
print(f"    beta tau^2/4 = {b_ * tau_ ** 2 / 4}: with R = 12 (> 10) one replacement does not pay:")
report("linear, R=12", lambda t: s0_ * t + b_ * t * t / 2, 12.0, tau_, nmax=3)
rows = report("K sqrt(a) with given life t_max = 6 (concave)", lambda t: K_ * math.sqrt(t), 1.0, tau_, tmax=6.0, nmax=6)
full = 3 * K_ * math.sqrt(6.0) + K_ * math.sqrt(2.0) + 3 * 1.0
print(f"    spec schedule (3 full lives of 6 + remainder 2): cost {full:.4f}")
rows = report("mixed sigma0 + beta a + K sqrt a, no limit", lambda t: s0_ * t + 0.02 * t * t / 2 + 8.0 * math.sqrt(t),
              1.0, tau_, nmax=5)
rows = report("mixed, strong sqrt (K=30), beta=0.05, R=0.5", lambda t: s0_ * t + 0.05 * t * t / 2 + 30.0 * math.sqrt(t),
              0.5, tau_, nmax=5)

print("\n(c) equal split versus 'full lives plus remainder' at a chosen interval (linear case)")
Lf = lambda t: s0_ * t + b_ * t * t / 2
Ts = math.sqrt(2 * 1.0 / b_)
mm = math.ceil(tau_ / Ts) - 1
rem = tau_ - mm * Ts
fl = mm * 1.0 + mm * Lf(Ts) + Lf(rem)
nn = mm + 1
eq = (nn - 1) * 1.0 + nn * Lf(tau_ / nn)
print(f"  T* = {Ts:.4f}: full lives + remainder ({mm} x T* + {rem:.3f}) cost {fl:.4f}; equal split n={nn}: {eq:.4f}")

print("\n(d) mixed L = t + beta t^2/2 + K sqrt(t): does any unequal split beat the best equal split? (grid, supplement)")
found = 0
total = 0
for bb in [0.2, 0.5, 1.0]:
    for KK in [2.0, 5.0, 10.0]:
        for RR in [0.5, 2.0, 5.0]:
            total += 1
            Lm = lambda t, bb=bb, KK=KK: t + bb * t * t / 2 + KK * math.sqrt(t)
            res = []
            for nn in range(1, 9):
                eqv = (nn - 1) * RR + nn * Lm(tau_ / nn)
                bs = best_split(Lm, nn, tau_, starts=30, seed=1)
                res.append((nn, eqv, (nn - 1) * RR + bs[0]))
            nb = min(res, key=lambda r: r[2])
            ne = min(res, key=lambda r: r[1])
            if abs(nb[2] - ne[1]) > 1e-4:
                found += 1
                print(f"  counterexample beta={bb} K={KK} R={RR}: best {nb[2]:.4f} (n={nb[0]}) vs best equal {ne[1]:.4f}")
print(f"  grid cases: {total}; cases where an unequal split beats the best equal split: {found}")

print("\n(e) claim 4's 'tau_w = min(tau_fail, T*)' fed to the spec's full-lives-plus-remainder count, finite horizon")
for RR in [12.0, 15.0]:
    Lf = lambda t: s0_ * t + b_ * t * t / 2
    Ts = math.sqrt(2 * RR / b_)
    mm = math.ceil(tau_ / Ts) - 1
    rem = tau_ - mm * Ts
    cost_rule = mm * RR + mm * Lf(Ts) + Lf(rem)
    best_n = min(((nn - 1) * RR + nn * Lf(tau_ / nn), nn) for nn in range(1, 10))
    print(f"  R = {RR}: T* = {Ts:.3f} < tau = {tau_} so the rule replaces (m = {mm}); cost {cost_rule:.4f};"
          f" finite-horizon optimum n = {best_n[1]} cost {best_n[0]:.4f}; overstatement {cost_rule - best_n[0]:.4f}"
          f" (R > beta tau^2/4 = {b_ * tau_ ** 2 / 4})")
