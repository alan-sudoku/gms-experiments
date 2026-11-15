"""rv04: claim 6 - roots per segment with two restarting clocks, generalised inflection test.

Purpose: for f = c0 + c1 tau + Kg sqrt(tau - a) - Ks sqrt(tau - b) on a segment where both ages are
positive, prove that f'' has at most one sign change (a != b), none (a = b, Kg != Ks), or f is linear
(a = b, Kg = Ks); derive the generalised inflection test and check that it reduces to the plan's
Ks^2 > Kg^2 (m+1)^3; count roots exactly on proven-monotone pieces (bisection on f' between the
analytic inflection point and the ends, then sign changes of f on the monotone pieces); build
three-root examples by random search (a < b found; a > b is the plan's known window); check the end-point limits of f' and the segment count.
Task: S5 review task 5.
Assumptions: made-up coefficients; root counting by bracketing on pieces where monotonicity is proved
(f' monotone between inflection and ends; f monotone between zeros of f'); a dense grid only as a check.
Level: derived.
"""
import math

import sympy as sp
from mpmath import mp, mpf, sqrt as msqrt, findroot

mp.dps = 30

print("(a) symbolic sign of f''")
t, a, b, Kg, Ks, c0, c1 = sp.symbols("tau a b K_g K_s c0 c1", real=True)
f = c0 + c1 * t + Kg * sp.sqrt(t - a) - Ks * sp.sqrt(t - b)
f2 = sp.diff(f, t, 2)
print("  f'' =", sp.simplify(f2))
al, be = sp.symbols("alpha beta", positive=True)  # alpha = tau - a (g age), beta = tau - b (s age)
f2ab = sp.Rational(1, 4) * (Ks * be ** sp.Rational(-3, 2) - Kg * al ** sp.Rational(-3, 2))
print("  f'' * alpha^(3/2) beta^(3/2) * 4 =", sp.simplify(4 * f2ab * al ** sp.Rational(3, 2) * be ** sp.Rational(3, 2)))
print("  so sign f'' = sign(D), D = Ks^2 alpha^3 - Kg^2 beta^3 (Kg, Ks >= 0)")
h = (t - a) / (t - b)
print("  d/dtau [(tau-a)/(tau-b)] =", sp.simplify(sp.diff(h, t)), " -> strictly monotone iff a != b")
print("  zero of f'': (tau-a)/(tau-b) = (Kg/Ks)^(2/3) (answer's form); at most one zero when a != b")
print("  a = b: f'' = (Ks - Kg)/(4 (tau-a)^(3/2)), no zero unless Kg = Ks, then f is linear (f == 0 possible)")
print("  Kg = 0: f'' > 0 (convex, <= 2 roots); Ks = 0: f'' < 0 (concave, <= 2 roots)")

print("\n(b) generalised inflection test and reduction to the plan's test")
m, tw = sp.symbols("m tau_w", positive=True)
# old case: segment m of g, a = m tw, b = 0, local dt in (0, tw): alpha from 0+ to tw, beta from m tw to (m+1) tw
D = lambda alpha, beta: Ks ** 2 * alpha ** 3 - Kg ** 2 * beta ** 3
print("  D at left end (alpha -> 0+, beta = m tw):", sp.simplify(D(0, m * tw)), " < 0")
print("  D at right end (alpha = tw, beta = (m+1) tw):", sp.factor(D(tw, (m + 1) * tw)),
      " > 0 iff Ks^2 > Kg^2 (m+1)^3 (plan step 1)")
print("  General test: interior inflection iff sign D(L+) != sign D(U-), with alpha, beta the two ages at the"
      " segment ends; ages at the ends are differences of integer multiples, so the test can be made exact")


def roots_on_segment(c0v, c1v, Kgv, Ksv, av, bv, L, U, grid=True):
    """Exact-in-principle root count on (L, U): split f' at the analytic inflection, bisect f' on
    each monotone piece, then count sign changes of f on each monotone piece of f."""
    c0v, c1v, Kgv, Ksv, av, bv, L, U = map(mpf, (c0v, c1v, Kgv, Ksv, av, bv, L, U))
    F = lambda x: c0v + c1v * x + Kgv * msqrt(x - av) - Ksv * msqrt(x - bv)
    Fp = lambda x: c1v + Kgv / (2 * msqrt(x - av)) - Ksv / (2 * msqrt(x - bv))
    eps = mpf(10) ** -30
    lo, hi = L + eps * (U - L), U
    cuts = [lo]
    if Kgv > 0 and Ksv > 0 and av != bv:
        q = (Kgv / Ksv) ** (mpf(2) / 3)
        if q != 1:
            x_inf = (av - q * bv) / (1 - q)
            if lo < x_inf < hi:
                cuts.append(x_inf)
    cuts.append(hi)
    zeros = []
    for x0, x1 in zip(cuts[:-1], cuts[1:]):
        p0, p1 = Fp(x0), Fp(x1)
        if p0 == 0:
            zeros.append(x0)
        elif p0 * p1 < 0:
            for _ in range(110):
                xm = (x0 + x1) / 2
                if Fp(xm) * p0 > 0:
                    x0 = xm
                else:
                    x1 = xm
            zeros.append((x0 + x1) / 2)
    pts = [lo] + sorted(zeros) + [hi]
    n = 0
    for x0, x1 in zip(pts[:-1], pts[1:]):
        if F(x0) * F(x1) < 0:
            n += 1
    # grid supplement (float, only when asked)
    gs = None
    if grid:
        Ff = lambda x: float(c0v) + float(c1v) * x + float(Kgv) * math.sqrt(x - float(av)) - float(Ksv) * math.sqrt(x - float(bv))
        N = 20000
        lof, hif = float(lo), float(hi)
        g = [Ff(lof + (hif - lof) * k / N) for k in range(N + 1)]
        gs = sum(1 for k in range(N) if g[k] * g[k + 1] < 0)
    return n, gs, Fp(lo), len(cuts) == 3


print("\n(c)-(d) random search for > 3 roots and three-root examples (exact method; grid only to confirm examples)")
import random
random.seed(4)
mx = 0
examples = {}
for _ in range(1500):
    av = random.choice([0.0, random.uniform(0, 2)])
    bv = random.choice([0.0, random.uniform(0, 2)])
    L = max(av, bv)
    U = L + random.uniform(0.2, 3)
    Kgv, Ksv = random.uniform(0, 5), random.uniform(0, 5)
    c1v = random.uniform(-3, 3)
    xm = (L + U) / 2
    c0v = -(c1v * xm + Kgv * math.sqrt(xm - av) - Ksv * math.sqrt(xm - bv)) + random.uniform(-0.05, 0.05)
    n, gs, _, _ = roots_on_segment(c0v, c1v, Kgv, Ksv, av, bv, L, U, grid=False)
    mx = max(mx, n)
    key = "a > b" if av > bv else ("a < b" if av < bv else "a = b")
    if n == 3 and key not in examples:
        n2, gs2, fpl2, _ = roots_on_segment(c0v, c1v, Kgv, Ksv, av, bv, L, U, grid=True)
        examples[key] = (av, bv, L, U, Kgv, Ksv, c1v, c0v, n2, gs2, float(fpl2))
print(f"  max exact root count over 1500 random segments: {mx}")
for key, e in examples.items():
    av, bv, L, U, Kgv, Ksv, c1v, c0v, n2, gs2, fpl2 = e
    print(f"  three-root example, {key}: a={av:.4f}, b={bv:.4f}, segment ({L:.4f},{U:.4f}), Kg={Kgv:.4f}, Ks={Ksv:.4f},"
          f" c1={c1v:.5f}, c0={c0v:.6f}: exact roots {n2}, float grid sign changes {gs2}, f'(L+) = {fpl2:.3e}")

print("\n(e) end-point limits of f' and jumps")
print("  just after an s restart (beta -> 0+, alpha > 0): f' ~ -Ks/(2 sqrt beta) -> -inf (answer correct)")
print("  just after a g restart: f' -> +inf; coincident restart: f' ~ (Kg - Ks)/(2 sqrt dt), sign of Kg - Ks,"
      " finite (c1) if Kg = Ks -> plan step 2 ('sign at the left end is +1') must be generalised")
print("  at tau = i tau_w,s: Ks term continuous (Ks sqrt(tau_w,s) + Ks sqrt(0+)); only -R_s jumps; f(i tau_w,s) is the"
      " left value, so a sign change across the jump has no root (answer correct)")

print("\n(f) segment count on [0, tau_max]")
from fractions import Fraction as Fr
tmax = Fr(20); twg = Fr(6); tws = Fr(4)
bg = {j * twg for j in range(1, 100) if j * twg < tmax}
bs = {i * tws for i in range(1, 100) if i * tws < tmax}
print(f"  tau_w,g = 6, tau_w,s = 4, tau_max = 20: g breakpoints {sorted(map(int, bg))}, s breakpoints {sorted(map(int, bs))},"
      f" coincident {sorted(map(int, bg & bs))}; segments = {len(bg | bs) + 1} = m_g + m_s + 1 - coincidences"
      f" = {len(bg)} + {len(bs)} + 1 - {len(bg & bs)}")

print("\n(g) if an age-linear rate term (beta_k a, restarting clock) were added to the profile")
bg_, bs_ = sp.symbols("beta_g beta_s", real=True)
fb = f + bg_ / 2 * (t - a) ** 2 - bs_ / 2 * (t - b) ** 2
print("  f''' =", sp.simplify(sp.diff(fb, t, 3)), " -> same ratio argument: at most one zero of f''' (a != b),")
print("  so f'' has at most 2 zeros and f at most 4 roots per segment: the argument no longer gives 3 (whether 4 occur: UNSURE)")
