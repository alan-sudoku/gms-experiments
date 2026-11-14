"""Review of prompt 4, claim C1: exact root counting per segment, independent of any grid.

Purpose
  The implementer counted roots of f on a segment with a dense grid (40000 points), which can miss
  close root pairs. This script counts roots exactly, by an algebraic route the implementer did not use:
  with tw = 1 (scale invariance, x = dt/tw), y = sqrt(x) in [0,1), z = sqrt(m + y^2),
      f = L(y) - S z,   L(y) = a (m + y^2) + G y + d,
  so f = 0  <=>  L(y) >= 0  and  P(y) = L(y)^2 - S^2 (m + y^2) = 0     (S > 0),
      f = 0  <=>  L(y) = 0                                              (S = 0).
  P is a quartic with rational coefficients (inputs are exact rationals of doubles). Its real roots in
  [0,1] are isolated exactly by SymPy (Sturm/continued fractions); the sign of L at each root is then
  bounded away from 0 (|L| = S z >= S sqrt(m)), so a 60-digit evaluation decides it.
Claims: C1 (<= 3 roots per segment; 3 attained only if 1 <= m < rho - 1 and Ks > Kg > 0).
Also: how often the implementer's grid count (replicated) under-counts, and 3-root examples at large m.
Assumptions: brief conventions; segment [0, tw) in dt, i.e. y in [0, 1).
Run: <gms-local>/.venv/bin/python r1_c1_exact_roots.py   (fixed seed, ~1-3 min)
Level: derived.
"""
import math
import random
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np
import sympy as sp

mp.mp.dps = 60
Y = sp.symbols("y")


def exact_count(m, a, G, S, d):
    """Number of distinct roots of f in y in [0,1) (x in [0,1)); None if f is identically 0."""
    m, a, G, S, d = (sp.Rational(Fr(v).numerator, Fr(v).denominator) for v in (m, a, G, S, d))
    L = a * (m + Y ** 2) + G * Y + d
    if S == 0:
        P = sp.Poly(sp.expand(L), Y)
        if P.is_zero:
            return None
        if P.degree() == 0:
            return 0
        iv = P.intervals(inf=0, sup=1, eps=sp.Rational(1, 10 ** 40))
        return sum(1 for (lo, hi), _ in iv if not (lo == 1 and hi == 1))
    P = sp.Poly(sp.expand(L ** 2 - S ** 2 * (m + Y ** 2)), Y)
    if P.is_zero:
        return None
    if P.degree() == 0:
        return 0
    cnt = 0
    for (lo, hi), _ in P.intervals(inf=0, sup=1, eps=sp.Rational(1, 10 ** 40)):
        if lo == 1 and hi == 1:
            continue  # y = 1 is dt = tw: next segment
        yv = (mp.mpf(lo.p) / lo.q + mp.mpf(hi.p) / hi.q) / 2
        Lv = mp.mpf(a.p) / a.q * (m + yv ** 2) + mp.mpf(G.p) / G.q * yv + mp.mpf(d.p) / d.q
        if Lv > -mp.mpf(10) ** -30:  # |L| = S z at a true root; tiny only if m = 0, y = 0, d = 0 (L = 0 is valid)
            cnt += 1
    return cnt


# implementer's grid counter, replicated verbatim in logic (c1_root_count.grid_roots)
U = np.linspace(0.0, 1.0, 40001)[:-1]
XG = U ** 2


def grid_roots(m, a_, G, S, dp):
    v = a_ * (m + XG) + G * np.sqrt(XG) - S * np.sqrt(m + XG) + dp
    s = np.sign(v)
    zeros = int(np.sum(s == 0))
    nz = s[s != 0]
    changes = int(np.sum(nz[1:] != nz[:-1])) if nz.size > 1 else 0
    return changes + zeros


def fprime(x, m, a, G, S):
    return a + G / (2 * mp.sqrt(x)) - S / (2 * mp.sqrt(m + x))


def fval(x, m, a, G, S, d):
    return a * (m + x) + G * mp.sqrt(x) - S * mp.sqrt(m + x) + d


def bisect(fun, lo, hi, it=220):
    """Plain bisection in mp; fun(lo) and fun(hi) have opposite signs (checked by the caller's construction)."""
    slo = mp.sign(fun(lo))
    for _ in range(it):
        mid = (lo + hi) / 2
        if mp.sign(fun(mid)) == slo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def window_case(rng, m, rho, G, level_mode):
    """Build (a, d) with two critical points in (0,1) and d inside the 3-root window (mp construction).
    level_mode: 'mid' (middle of window) or 'edge' (1e-12 relative from a window end -> close root pair)."""
    G = mp.mpf(G)
    S = G * mp.mpf(rho) ** 1.5
    xs = m / (mp.mpf(rho) - 1)  # f'' zero
    if not (0 < xs < 1):
        return None
    q = lambda x: G / (2 * mp.sqrt(x)) - S / (2 * mp.sqrt(m + x))
    lo, hi = -q(1), -q(xs)  # a in (lo, hi) gives f' zeros on both sides of xs
    if not lo < hi:
        return None
    a = lo + mp.mpf(rng.uniform(0.05, 0.95)) * (hi - lo)
    c1 = bisect(lambda t: fprime(t, m, a, G, S), mp.mpf(10) ** -40, xs)
    c2 = bisect(lambda t: fprime(t, m, a, G, S), xs, mp.mpf(1))
    vals = dict(f0=fval(0, m, a, G, S, 0), fmax=fval(c1, m, a, G, S, 0),
                fmin=fval(c2, m, a, G, S, 0), f1=fval(1, m, a, G, S, 0))
    wlo, whi = max(vals["f0"], vals["fmin"]), min(vals["fmax"], vals["f1"])
    if not wlo < whi:
        return None
    if level_mode == "mid":
        L = (wlo + whi) / 2
    else:
        L = whi - (whi - wlo) * mp.mpf(10) ** -12 if rng.random() < 0.5 else wlo + (whi - wlo) * mp.mpf(10) ** -12
    return float(a), float(G), float(S), float(-L)


def main():
    rng = random.Random(4242)
    hist = {}
    undercount = 0
    undercount_ex = None
    three = []
    violations = []
    n = 0
    cls_count = {}
    uc_cls = {}

    def record(cls, m, a, G, S, d):
        nonlocal undercount, undercount_ex, n
        c = exact_count(m, a, G, S, d)
        n += 1
        cls_count[cls] = cls_count.get(cls, 0) + 1
        if c is None:
            hist["identically0"] = hist.get("identically0", 0) + 1
            return
        hist[c] = hist.get(c, 0) + 1
        if c > 3:
            violations.append((cls, m, a, G, S, d, c))
        if c == 3:
            three.append((cls, m, a, G, S, d))
            Gq, Sq = Fr(G), Fr(S)
            ok = m >= 1 and Sq > Gq > 0 and Sq ** 2 > Gq ** 2 * (m + 1) ** 3
            if not ok:
                violations.append(("3 roots outside 1<=m<rho-1", cls, m, a, G, S, d))
        g = grid_roots(m, a, G, S, d)
        if g < c:
            undercount += 1
            uc_cls[cls.split("_m")[0]] = uc_cls.get(cls.split("_m")[0], 0) + 1
            if undercount_ex is None:
                undercount_ex = (cls, m, a, G, S, d, c, g)

    # (A) implementer's 3-root example and f(0)=0 variant parameters
    ex = (1, 0.27462901204136775, 0.06913552752653546, 0.8205556354592521, 0.5436108308140535)
    print("(A) implementer's 3-root example (tw=1, m=1): exact quartic count =", exact_count(*ex),
          "; grid count =", grid_roots(*ex))

    # (B) constructed 3-root windows incl. large m and near-tangent levels
    for m in (1, 2, 3, 10, 100, 1000, 10 ** 6):
        for _ in range(60 if m < 1000 else 25):
            rho = (m + 1) * 10 ** rng.uniform(0.01, 2.0)
            G = 10 ** rng.uniform(-3, 2)
            for mode in ("mid", "edge"):
                w = window_case(rng, m, rho, G, mode)
                if w is not None:
                    record("window_" + mode + "_m" + str(m), m, *w)
    # (C) generic and edge classes
    for _ in range(1500):
        m = rng.choice([0, 0, 1, 2, 3, 5, 10, 100, 10 ** 4, 10 ** 6])
        G = rng.choice([0.0, 1.0, 10 ** rng.uniform(-3, 2)])
        S = rng.choice([0.0, G, G * (1 + 2 ** -50), 10 ** rng.uniform(-3, 3)])
        a = rng.choice([0.0, rng.uniform(-3, 3), -10 ** rng.uniform(-6, 2)])
        d = rng.choice([0.0, rng.uniform(-30, 30), -(a * m - S * math.sqrt(m))])
        record("generic", m, a, G, S, d)

    print("(B,C) cases:", n, " classes:", dict(sorted(cls_count.items())))
    print("    exact root-count histogram (distinct roots in dt in [0,tw)):", {str(k): v for k, v in sorted(hist.items(), key=lambda kv: str(kv[0]))})
    print("    violations of '<= 3' or of '3 only if 1<=m<rho-1, Ks>Kg>0':", len(violations), violations[:3])
    big = [t for t in three if t[1] >= 1000]
    print("    3-root cases:", len(three), "; with m >= 1000:", len(big))
    if big:
        cls, m, a, G, S, d = max(big, key=lambda t: t[1])
        print("    largest-m 3-root example (tw=1): m=%d a=%r Kg=%r Ks=%r d'=%r" % (m, a, G, S, d))
    print("    grid (implementer's method) under-counts the exact count in", undercount, "of", n, "cases")
    print("    under-counts by class:", uc_cls)
    if undercount_ex:
        print("    first under-count:", undercount_ex)


if __name__ == "__main__":
    main()
