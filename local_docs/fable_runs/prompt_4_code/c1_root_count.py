"""C1: f'' has at most one zero on (0, tw), only if Ks > Kg, at dt = t_m/(rho-1),
rho = (Ks/Kg)^(2/3); hence at most 3 roots of f per segment.

Assumptions: common.py conventions. Segment m, local time dt in [0, tw).
Scale invariance: dt = tw*x gives f = a tw (m+x) + Kg sqrt(tw) sqrt x - Ks sqrt(tw) sqrt(m+x) + d',
so tw = 1 is wlog for root counting; d' (= d0 + m R + m Kg sqrt tw) is a free real.
Run: <gms-local>/.venv/bin/python c1_root_count.py

Parts:
 (1) SymPy: f'', its zero, sign pattern.
 (2) Constructive search for the maximum number of roots per segment: monotone pieces
     of f from the zeros of f', levels chosen at critical values, then a dense grid.
 (3) Hypothesis (>= 2000 per property): zero count of f'' on (0,tw) <= 1 and location
     formula; grid root count of f <= 3; edge classes sampled and counted.
 (4) mp-60-digit confirmation of the 3-root example and of degenerate examples.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math, random
import numpy as np
import sympy as sp
import mpmath as mp
from hypothesis import given, settings, strategies as st, HealthCheck
from common import Cov, logfloat

mp.mp.dps = 60
# ---------------------------------------------------------------- (1) SymPy
x, tm, Kg, Ks, a, d = sp.symbols("x t_m K_g K_s a d", positive=True)
fl = a * (tm + x) + Kg * sp.sqrt(x) - Ks * sp.sqrt(tm + x) + d
f2 = sp.simplify(sp.diff(fl, x, 2))
print("(1) f'' =", f2)
phi = Ks * x ** sp.Rational(3, 2) - Kg * (tm + x) ** sp.Rational(3, 2)
chk = sp.simplify(f2 - phi / (4 * x ** sp.Rational(3, 2) * (tm + x) ** sp.Rational(3, 2)))
print("    f'' - phi/(4 x^(3/2) (t_m+x)^(3/2)) =", chk, " (phi := Ks x^(3/2) - Kg (t_m+x)^(3/2); same sign as f'')")
rho = (Ks / Kg) ** sp.Rational(2, 3)
xstar = tm / (rho - 1)
# phi(xstar) = 0 check: Ks xstar^(3/2) = Kg (tm+xstar)^(3/2); with xstar/(tm+xstar)=1/rho ->  (1/rho)^(3/2)=Kg/Ks
val = sp.simplify(((xstar / (tm + xstar)) ** sp.Rational(3, 2)) - Kg / Ks)
print("    (x*/(t_m+x*))^(3/2) - Kg/Ks =", val, " (zero of f'' at x* = t_m/(rho-1) confirmed)")
print("    Monotonic argument: psi(x)=x/(t_m+x) is strictly increasing for t_m>0 => psi^(3/2)=Kg/Ks has <= 1 solution on x>0;")
print("    f''<0 for x<x* (Kg term dominates), f''>0 for x>x* => f concave-then-convex, f'(0+)=+inf (Kg>0),")
print("    f' decreasing then increasing => <= 2 zeros of f' => f has <= 3 monotone pieces => <= 3 roots (if f not identically 0).")

# ---------------------------------------------------------------- helpers (tw = 1)
def fx(xx, m, a_, G, S, dp):
    return a_ * (m + xx) + G * math.sqrt(xx) - S * math.sqrt(m + xx) + dp

def gp(xx, m, a_, G, S):
    return a_ + (G / (2 * math.sqrt(xx)) if xx > 0 else math.inf) - S / (2 * math.sqrt(m + xx))

def bis(fun, lo, hi, it=200):
    flo = fun(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if (fun(mid) > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def crit_points(m, a_, G, S):
    """Zeros of f' on (0,1) (tw=1). Pieces split at the zero of f''."""
    pts = []
    if G > 0 and S > G and m >= 1:
        rho_ = (S / G) ** (2 / 3)
        xs = m / (rho_ - 1)
    else:
        xs = None
    # break points of monotonicity of f' inside (0,1)
    br = [0.0] + ([xs] if xs is not None and 0 < xs < 1 else []) + [1.0]
    for lo, hi in zip(br[:-1], br[1:]):
        lo_ = max(lo, 1e-300) if lo == 0 else lo
        flo, fhi = gp(lo_, m, a_, G, S), gp(hi, m, a_, G, S)
        if flo == 0:
            pts.append(lo_)
        if flo * fhi < 0:
            pts.append(bis(lambda t: gp(t, m, a_, G, S), lo_, hi))
    return sorted(set(pts))

U = np.linspace(0.0, 1.0, 40001)[:-1]
XG = U ** 2          # x in [0,1), dense near 0 (sqrt singularity)

def grid_roots(m, a_, G, S, dp):
    v = a_ * (m + XG) + G * np.sqrt(XG) - S * np.sqrt(m + XG) + dp
    s = np.sign(v)
    zeros = int(np.sum(s == 0))
    nz = s[s != 0]
    changes = int(np.sum(nz[1:] != nz[:-1])) if nz.size > 1 else 0
    return changes + zeros

# ---------------------------------------------------------------- (2) search for 3 roots
rng = random.Random(20261114)
best = {"count": 0, "ex": None}
three = []
hist = {}
for it in range(60000):
    m = rng.choice([1, 2, 3, 5, 10, 30, 100, 1000])
    G = 10 ** rng.uniform(-2, 1)
    S = G * 10 ** rng.uniform(0.0, 2.5)   # Ks > Kg
    a_ = -10 ** rng.uniform(-3, 1) * rng.choice([1, 1, 1, -0.1])
    cp = crit_points(m, a_, G, S)
    if len(cp) == 2:
        M, n = fx(cp[0], m, a_, G, S, 0.0), fx(cp[1], m, a_, G, S, 0.0)
        g0, g1 = fx(0.0, m, a_, G, S, 0.0), fx(1.0, m, a_, G, S, 0.0)
        lo, hi = max(n, g0), min(M, g1)
        if lo < hi and M > n:
            L = 0.5 * (lo + hi)
            c = grid_roots(m, a_, G, S, -L)
            hist[c] = hist.get(c, 0) + 1
            if c >= best["count"]:
                if c > best["count"] or (c == 3 and (hi - lo) > best["ex"][-1]):
                    best = {"count": c, "ex": (m, a_, G, S, -L, hi - lo)}
            if c == 3:
                three.append((m, a_, G, S, -L, hi - lo))
print(f"(2) search over 60000 random (m,a,Kg,Ks<=316 Kg) with level in the 3-root window:")
print("    grid root-count histogram over examples with two f' zeros in (0,1):", dict(sorted(hist.items())))
print("    max roots found per segment:", best["count"])
print("    number of 3-root examples:", len(three))
ex = best["ex"]
print("    chosen example (tw=1): m=%d a=%r Kg=%r Ks=%r d'=%r  level-window width=%.3e" % ex)

# random generic search (random d' not chosen at critical level) and edge level search
mx_generic = 0
for it in range(60000):
    m = rng.choice([0, 1, 2, 3, 5, 10, 100])
    G = rng.choice([0.0, 1.0, 10 ** rng.uniform(-2, 1)])
    S = rng.choice([0.0, G, 10 ** rng.uniform(-2, 1.5)])
    a_ = rng.choice([0.0, rng.uniform(-3, 3)])
    dp = rng.uniform(-30, 30)
    if G == 0 and S == 0 and a_ == 0:
        continue
    mx_generic = max(mx_generic, grid_roots(m, a_, G, S, dp))
print("    max roots with generic random d' over 60000 draws incl. edge classes (excluding f==const):", mx_generic)

# ---------------------------------------------------------------- (4) mp confirmation of 3-root example
m, a_, G, S, dp, w = ex
cp = crit_points(m, a_, G, S)
def fmp(xx):
    xx = mp.mpf(xx)
    return mp.mpf(a_) * (m + xx) + mp.mpf(G) * mp.sqrt(xx) - mp.mpf(S) * mp.sqrt(m + xx) + mp.mpf(dp)
pts = [mp.mpf(0), mp.mpf(cp[0]), mp.mpf(cp[1]), mp.mpf(1) - mp.mpf(10) ** -12]
print("(4) mp-60 sign pattern of f at x = 0, x_max, x_min, 1-1e-12 (tw=1):",
      [mp.nstr(fmp(p), 6) for p in pts], "signs:", [int(mp.sign(fmp(p))) for p in pts])
print("    critical points x_max, x_min =", cp, " (f'' zero x* = m/(rho-1) =",
      m / ((S / G) ** (2 / 3) - 1), ")")
roots = []
for lo, hi in zip(pts[:-1], pts[1:]):
    if mp.sign(fmp(lo)) != mp.sign(fmp(hi)):
        roots.append(mp.findroot(fmp, (lo, hi), solver="anderson", tol=1e-45, maxsteps=200))
print("    roots in (0,1) found by mp.findroot bracket:", [mp.nstr(r, 20) for r in roots], "count =", len(roots))

# 3-roots-including-x=0 variant: f(0) = 0 exactly (d' held as an exact mp value), then roots at 0,
# one in (x_max,x_min), one in (x_min,1).  Search for parameters with g(0) > g(x_min) and g(0) < min(g(x_max), g(1)).
found0 = None
for (m0, a0, G0, S0, dp0_, w0) in three + [None] * 0:
    c0 = crit_points(m0, a0, G0, S0)
    g0_ = fx(0.0, m0, a0, G0, S0, 0.0)
    n0 = fx(c0[1], m0, a0, G0, S0, 0.0); M0 = fx(c0[0], m0, a0, G0, S0, 0.0); g10 = fx(1.0, m0, a0, G0, S0, 0.0)
    if n0 < g0_ < min(M0, g10):
        found0 = (m0, a0, G0, S0, c0)
        break
if found0 is None:
    for it in range(200000):
        m0 = rng.choice([1, 2, 3]); G0 = 10 ** rng.uniform(-2, 0); S0 = G0 * (m0 + 1) ** 1.5 * (1 + 10 ** rng.uniform(-1, 1.7))
        a0 = -10 ** rng.uniform(-3, 0)
        c0 = crit_points(m0, a0, G0, S0)
        if len(c0) != 2: continue
        g0_ = fx(0.0, m0, a0, G0, S0, 0.0)
        n0 = fx(c0[1], m0, a0, G0, S0, 0.0); M0 = fx(c0[0], m0, a0, G0, S0, 0.0); g10 = fx(1.0, m0, a0, G0, S0, 0.0)
        if n0 < g0_ < min(M0, g10):
            found0 = (m0, a0, G0, S0, c0); break
if found0:
    m0, a0, G0, S0, c0 = found0
    d_exact = -(mp.mpf(a0) * m0 - mp.mpf(S0) * mp.sqrt(m0))   # makes f(0) = 0 exactly (60 digits)
    def f0mp(xx):
        xx = mp.mpf(xx)
        return mp.mpf(a0) * (m0 + xx) + mp.mpf(G0) * mp.sqrt(xx) - mp.mpf(S0) * mp.sqrt(m0 + xx) + d_exact
    pp = [mp.mpf(0), mp.mpf(c0[0]), mp.mpf(c0[1]), mp.mpf(1) - mp.mpf(10) ** -12]
    print("    variant f(0)=0: m=%d a=%r Kg=%r Ks=%r; mp signs at 0,x_max,x_min,1-1e-12: %s -> roots at x=0, in (x_max,x_min), in (x_min,1): 3 roots in [0,1)"
          % (m0, a0, G0, S0, [int(mp.sign(f0mp(t))) if abs(f0mp(t)) > mp.mpf(10) ** -50 else 0 for t in pp]))
else:
    print("    variant f(0)=0: no example found (UNSURE)")

# ---------------------------------------------------------------- (3) hypothesis
cov = Cov()
mode = st.sampled_from(["free", "free", "eqKg", "Ks0", "Kg0", "both0"])

@settings(database=None, derandomize=True, deadline=None, max_examples=3000,
          suppress_health_check=list(HealthCheck))
@given(tw=st.one_of(st.sampled_from([1e3, 1e9, 1.0]), logfloat(st, -3, 9, zero=False)),
       m=st.one_of(st.sampled_from([0, 1, 2, 3, 10 ** 6]), st.integers(0, 10 ** 4)),
       Kg0=logfloat(st, -3, 3, zero=False), ratio=st.floats(0.01, 100.0), mode=mode)
def prop_fpp(tw, m, Kg0, ratio, mode):
    """zeros of f'' in (0,tw): <=1; exists iff Ks>Kg>0, m>=1, m < rho-1; located at t_m/(rho-1)."""
    Kg_, Ks_ = Kg0, Kg0 * ratio
    if mode == "eqKg": Ks_ = Kg_
    if mode == "Ks0": Ks_ = 0.0
    if mode == "Kg0": Kg_ = 0.0
    if mode == "both0": Kg_, Ks_ = 0.0, 0.0
    cov.hit("fpp:" + mode); cov.hit("fpp:m=0", m == 0); cov.hit("fpp:m>=1", m >= 1)
    cov.hit("fpp:Ks>Kg>0", Ks_ > Kg_ > 0)
    tmv = m * tw
    xs = np.geomspace(tw * 1e-12, tw, 6001)[:-1]  # (0,tw)
    with np.errstate(all="ignore"):
        fpp = -Kg_ / 4 * xs ** -1.5 + Ks_ / 4 * (tmv + xs) ** -1.5
    sg = np.sign(fpp)
    nz = sg[sg != 0]
    changes = int(np.sum(nz[1:] != nz[:-1])) if nz.size > 1 else 0
    assert changes <= 1, ("f'' sign changes", changes, tw, m, Kg_, Ks_)
    if Ks_ > Kg_ > 0 and m >= 1:
        rho_ = (Ks_ / Kg_) ** (2 / 3)
        xstar = tmv / (rho_ - 1) if rho_ > 1 else math.inf
        inside = 1e-12 * tw < xstar < tw
        if inside:
            cov.hit("fpp:zero inside (0,tw)")
            assert changes == 1, ("expected zero inside", xstar, tw, m, Kg_, Ks_)
            # location: f'' sign flips between grid neighbours around xstar
            i = np.searchsorted(xs, xstar)
            assert sg[max(i - 1, 0)] <= 0 <= sg[min(i, len(xs) - 1)] or abs(xs[min(i, len(xs)-1)] - xstar) < 1e-6 * xstar
        if xstar >= tw: cov.hit("fpp:zero beyond tw")
    else:
        assert changes == 0 or (Ks_ == Kg_ and m == 0), ("unexpected zero w/o Ks>Kg>0,m>=1", tw, m, Kg_, Ks_, changes)

prop_fpp()
print("(3a) hypothesis f'' zero property passed (3000 examples)")
cov.report(["fpp:free", "fpp:eqKg", "fpp:Ks0", "fpp:Kg0", "fpp:both0", "fpp:m=0", "fpp:m>=1",
            "fpp:Ks>Kg>0", "fpp:zero inside (0,tw)", "fpp:zero beyond tw"])

cov2 = Cov()
@settings(database=None, derandomize=True, deadline=None, max_examples=3000,
          suppress_health_check=list(HealthCheck))
@given(m=st.one_of(st.sampled_from([0, 1, 2, 3, 5, 10, 100, 1000]), st.integers(0, 2000)),
       Gk=logfloat(st, -2, 1, zero=False), ratio=st.floats(0.0, 300.0),
       asc=st.floats(-3.0, 3.0), mode=st.sampled_from(["free", "free", "eqKg", "Ks0", "Kg0", "a0", "tuned", "tuned", "tuned"]),
       lvl=st.floats(0.0, 1.0), pick=st.sampled_from(["window", "window", "rand", "f0=0"]))
def prop_roots(m, Gk, ratio, asc, mode, lvl, pick):
    G_, S_, a_ = Gk, Gk * ratio, asc * 10 ** -1.0
    if mode == "eqKg": S_ = G_
    if mode == "Ks0": S_ = 0.0
    if mode == "Kg0": G_ = 0.0
    if mode == "a0": a_ = 0.0
    if mode == "tuned":      # force two zeros of f' in (0,1): x*<1 and f'(x*)<0<f'(1)
        m = max(m % 4, 1)
        S_ = G_ * (m + 1) ** 1.5 * (1.0 + 10 ** (-1 + 2.7 * lvl))
        xs_ = m / ((S_ / G_) ** (2 / 3) - 1)
        fn = lambda t: G_ / (2 * math.sqrt(t)) - S_ / (2 * math.sqrt(m + t))
        a_ = -(fn(xs_) + (0.1 + 0.8 * min(max(abs(asc) / 3, 0.0), 1.0)) * (fn(1.0) - fn(xs_)))
    cov2.hit("roots:" + mode); cov2.hit("roots:m=0", m == 0)
    cp = crit_points(m, a_, G_, S_)
    g0 = fx(0.0, m, a_, G_, S_, 0.0); g1 = fx(1.0, m, a_, G_, S_, 0.0)
    if pick == "f0=0":
        dp = -g0
    elif pick == "window" and len(cp) >= 1:
        vals = [g0, g1] + [fx(c, m, a_, G_, S_, 0.0) for c in cp]
        lo_, hi_ = min(vals), max(vals)
        dp = -(lo_ + lvl * (hi_ - lo_))
    else:
        dp = -(g0 + (lvl - 0.5) * 10)
    cov2.hit("roots:2 crit pts", len(cp) == 2)
    if G_ == S_ and m == 0:
        # f = a*dt + d' exactly linear; the float grid loses a*dt against G*sqrt - S*sqrt cancellation
        c_float = grid_roots(m, a_, G_, S_, dp)
        cov2.hit("roots:m=0,Ks=Kg (f linear)")
        if c_float > 3:
            cov2.hit("roots:FLOAT ARTEFACT m=0,Ks=Kg grid count>3")
        return
    c = grid_roots(m, a_, G_, S_, dp)
    degenerate = (G_ == S_ and m == 0 and a_ == 0 and dp == 0) or (G_ == 0 and S_ == 0 and a_ == 0 and dp == 0)
    if degenerate:
        cov2.hit("roots:degenerate f==0")
        return
    assert c <= 3, ("roots >3", m, a_, G_, S_, dp, c)
    cov2.hit("roots:count=3", c == 3); cov2.hit("roots:count=2", c == 2)

prop_roots()
print("(3b) hypothesis root-count property (<=3 per segment) passed (3000 examples)")
cov2.report(["roots:free", "roots:eqKg", "roots:Ks0", "roots:Kg0", "roots:a0", "roots:m=0",
             "roots:2 crit pts", "roots:count=3", "roots:count=2", "roots:m=0,Ks=Kg (f linear)", "roots:tuned"], minimum=20)
print("  (informational) float artefact count:", cov2.c.get("roots:FLOAT ARTEFACT m=0,Ks=Kg grid count>3", 0))

# ---------------------------------------------------------------- degenerate cases (exact)
print("(5) degenerate cases (exact, SymPy):")
dd = sp.symbols("dd", positive=True)
f_eq = sp.simplify((a * (0 + dd) + Kg * sp.sqrt(dd) - Kg * sp.sqrt(0 + dd) + d).subs({a: 0, d: 0}))
print("    m=0, Ks=Kg, a=0, d'=0: f(dt) =", f_eq, "-> identically 0, infinitely many roots (claim silent; fails literally)")
print("    m=0, Ks=Kg: f''=0 identically, so 'f'' has at most one zero' is false (zero set = whole interval);")
print("    Ks=Kg, m>=1: rho=1, formula divides by zero, f''<0 on (0,tw) (no zero) -> consistent with the 'only when Ks>Kg' clause;")
print("    Kg=0: rho=infinity, x*=0 not in (0,tw); f''>0 (Ks>0) -> f convex, <=2 roots; formula undefined (division by Kg=0).")
