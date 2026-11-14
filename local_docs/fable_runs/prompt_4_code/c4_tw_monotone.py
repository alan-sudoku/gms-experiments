"""C4: for fixed tau >= tw, h(s) = Kg [ m sqrt(s) + sqrt(tau - m s) ], m = floor(tau/s), is strictly
decreasing in s = tw; m R is non-increasing in s; hence f(tau) is non-increasing in tw (shorter tw never
favourable to geometry).

Assumptions: common.py conventions; tie tau = j*s gives m = j (remainder 0).
Run: <gms-local>/.venv/bin/python c4_tw_monotone.py
Method:
 (1) SymPy: dh/ds on an interval of constant m; sign from remainder r = tau - m s < s; continuity of h
     at s = tau/k (limits from both sides); the jump of m R at s = tau/k.
 (2) Hypothesis, exact (Fractions + mp 60 digits), >= 3000 examples per property: h(s1) > h(s2) for s1<s2<=tau
     (Kg>0); equal if Kg = 0; flat for s >= tau; m(s) non-increasing; f(tau;s1) >= f(tau;s2) all tau incl.
     s2 > tau; tie points s = tau/k exact.
 (3) float64 hazard: floor(tau/s) with tau = j*s computed in float; effect on f of a wrong m (size R).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
from fractions import Fraction
import sympy as sp
import mpmath as mp
from hypothesis import given, settings, strategies as st, HealthCheck
from common import f_mp, f_float, Cov, logfloat, _mpf

# ---------------------------------------------------------------- (1)
s, tau, k, Kg, r = sp.symbols("s tau k K_g r", positive=True)
mm = sp.symbols("m", positive=True)
h = Kg * (mm * sp.sqrt(s) + sp.sqrt(tau - mm * s))
dh = sp.simplify(sp.diff(h, s))
print("(1) dh/ds on constant m =", dh)
# with r = tau - m s: dh/ds = Kg m/2 (1/sqrt(s) - 1/sqrt(r)); sign: r < s  => 1/sqrt(r) > 1/sqrt(s) => negative
chk = sp.simplify(dh - Kg * mm / 2 * (1 / sp.sqrt(s) - 1 / sp.sqrt(tau - mm * s)))
print("    dh/ds - Kg m/2 (1/sqrt(s) - 1/sqrt(r)) =", chk, "[algebra]")
print("    m = floor(tau/s) => 0 <= r = tau - m s < s => 1/sqrt(r) > 1/sqrt(s) => dh/ds < 0 for m>=1, Kg>0 (proof, not numeric)")
# continuity at s = tau/k
hk_left = h.subs(mm, k).subs(s, tau / k)             # from below (m = k): h(s) at s=tau/k with m=k
hk_right = h.subs(mm, k - 1).subs(s, tau / k)        # from above (m = k-1)
print("    h at s=tau/k using m=k:", sp.simplify(hk_left), "; using m=k-1:", sp.simplify(hk_right),
      "; difference:", sp.simplify(hk_left - hk_right), " -> h continuous across the change of m")
print("    m R jumps DOWN by R when s increases through tau/k (m: k -> k-1) -> m R non-increasing, left-continuous in s.")
# s > tau: m = 0, h = Kg sqrt(tau): constant. h(tau) = Kg(1*sqrt(tau) + 0)
print("    s>=tau: m=0 or 1,r=0 -> h = Kg sqrt(tau) constant (so 'strictly decreasing' holds on (0,tau] only; weakly on (0,inf)).")

# ---------------------------------------------------------------- (2)
cov = Cov()
S = dict(database=None, derandomize=True, deadline=None, max_examples=3000, suppress_health_check=list(HealthCheck))

def h_mp(tau_q, s_q, Kg_):
    tau_q, s_q = Fraction(tau_q), Fraction(s_q)
    m = math.floor(tau_q / s_q)
    rem = tau_q - m * s_q
    return _mpf(Kg_) * (m * mp.sqrt(_mpf(s_q)) + mp.sqrt(_mpf(rem))), m

taus = st.one_of(st.sampled_from([1e3, 1e9, 1e10, 1.0, 3.0]), logfloat(st, 0, 10, zero=False))
ratios = st.one_of(st.sampled_from([1.0, 1.0000001, 2.0, 3.0, 7.0, 1e3]), st.floats(1.0, 1e4))

@settings(**S)
@given(tau=taus, r1=ratios, r2=ratios, Kg=logfloat(st, -3, 3), tie1=st.booleans(), tie2=st.booleans(),
       kk1=st.integers(1, 10 ** 6), kk2=st.integers(1, 10 ** 6))
def prop_h(tau, r1, r2, Kg, tie1, tie2, kk1, kk2):
    tq = Fraction(tau)
    # two values of s in (0, tau]: s = tau / ratio (ratio >= 1), or exact tie s = tau/k
    sA = tq / Fraction(kk1 if tie1 else 1) / (1 if tie1 else Fraction(r1))
    sB = tq / Fraction(kk2 if tie2 else 1) / (1 if tie2 else Fraction(r2))
    s1, s2 = sorted([sA, sB])
    cov.hit("h:Kg=0", Kg == 0); cov.hit("h:tie s=tau/k", tie1 or tie2); cov.hit("h:s1==s2", s1 == s2)
    cov.hit("h:m>=1000", tq / s1 >= 1000)
    h1, m1 = h_mp(tq, s1, Kg); h2, m2 = h_mp(tq, s2, Kg)
    assert m1 >= m2
    tol = mp.mpf(10) ** -40 * (1 + abs(h1))
    if s1 == s2:
        return
    if Kg > 0:
        assert h1 > h2 - tol, ("h not decreasing", float(tq), float(s1), float(s2), h1, h2)
        cov.hit("h:strict gap > 1e-30 rel", h1 - h2 > mp.mpf(10) ** -30 * h1)
    else:
        assert h1 == 0 and h2 == 0

prop_h()
print("(2a) hypothesis h(s1) >= h(s2), m non-increasing, exact floor (3000 examples)")
cov.report(["h:Kg=0", "h:tie s=tau/k", "h:m>=1000", "h:strict gap > 1e-30 rel"])

# tie continuity checked at 60 digits: h(tau/k) vs h(tau/k * (1 +- 1e-30))
@settings(**S)
@given(tau=taus, kk=st.integers(1, 10 ** 5), Kg=logfloat(st, -3, 3, zero=False))
def prop_cont(tau, kk, Kg):
    tq = Fraction(tau); s0 = tq / kk
    e = Fraction(1, 10 ** 30)
    hm, m_a = h_mp(tq, s0 * (1 - e), Kg); h0, m_0 = h_mp(tq, s0, Kg); hp, m_b = h_mp(tq, s0 * (1 + e), Kg)
    assert m_0 == kk and m_b == kk - 1 and m_a >= kk
    # |h(s0+) - h(s0)| must be tiny (continuity) while R-term jump is a full R
    assert abs(hp - h0) < mp.mpf(10) ** -10 * (1 + h0) and abs(hm - h0) < mp.mpf(10) ** -10 * (1 + h0)
prop_cont()
print("(2b) hypothesis: h is continuous at s = tau/k at 1e-30 relative offsets; m(tau/k) = k, m(just above) = k-1 (3000 examples)")

cov2 = Cov()
@settings(**S)
@given(tau=taus, r1=ratios, r2=st.one_of(ratios, st.floats(0.001, 1.0)), a=st.floats(-1e-3, 1e-3), Kg=logfloat(st, -3, 3),
       Ks=logfloat(st, -3, 3), R=logfloat(st, -3, 6), d0=st.floats(-1e6, 1e6), tie=st.booleans(), kk=st.integers(1, 10 ** 4))
def prop_f_tw(tau, r1, r2, a, Kg, Ks, R, d0, tie, kk):
    tq = Fraction(tau)
    sA = tq / Fraction(r1)
    sB = tq / (Fraction(kk) if tie else 1) / Fraction(r2) if True else sA
    # sB may exceed tau (r2<1 -> s>tau): covers tau < tw branch, which is outside the literal domain of C4
    s1, s2 = sorted([sA, sB])
    cov2.hit("f:s2>tau (tau<tw branch)", s2 > tq); cov2.hit("f:tie", tie); cov2.hit("f:R=0", R == 0); cov2.hit("f:Kg=0", Kg == 0)
    f1 = f_mp(tq, s1, a, Kg, Ks, R, d0); f2 = f_mp(tq, s2, a, Kg, Ks, R, d0)
    tol = mp.mpf(10) ** -40 * (1 + abs(f1) + abs(f2))
    assert f1 >= f2 - tol, ("f(tau;tw small) < f(tau; tw big)", float(tq), float(s1), float(s2), f1, f2)
prop_f_tw()
print("(2c) hypothesis: f(tau; s1) >= f(tau; s2) for s1 < s2, any tau, including s2 > tau (3000 examples)")
cov2.report(["f:s2>tau (tau<tw branch)", "f:tie", "f:R=0", "f:Kg=0"])

# ---------------------------------------------------------------- (3) float hazard at ties
print("(3) float64 hazard: m = floor(tau/s) when tau is the FLOAT product j*s (intended tie), float vs exact floor of the double values")
import random
rng = random.Random(3)
wrong_float = 0; wrong_exactdouble = 0; N = 200000; ex_ = None
for _ in range(N):
    sf = 10 ** rng.uniform(-3, 9); j = rng.randint(2, 10 ** 6)
    tf = j * sf                              # rounded product
    mf = math.floor(tf / sf)                 # float floor
    me = math.floor(Fraction(tf) / Fraction(sf))   # exact floor of the doubles' ratio
    if mf != j: wrong_float += 1
    if me != j:
        wrong_exactdouble += 1
        if ex_ is None: ex_ = (sf, j, tf, mf, me)
print(f"    over {N} random (s, j): float floor(j*s/s) != j in {wrong_float} cases; exact floor of the double values != j in {wrong_exactdouble} cases")
if ex_:
    sf, j, tf, mf, me = ex_
    print(f"    first case with exact floor != j: s={sf!r}, j={j}, tau=j*s={tf!r}; float floor={mf}, exact floor={me}")
    R_, Kg_ = 7.0, 2.0
    print(f"      effect of a wrong m (j vs j-1): m*R differs by exactly R = {R_}; Kg*[m sqrt(tw)+sqrt(dt)] changes continuously (no jump)")
    print("      (f jumps by R at a tie; a one-ulp error in tau=j*s therefore flips the verdict side by R_g -> solver must not rely on exact ties.)")
# dt cancellation just across a tie: sqrt(dt) amplification
tw_ = 1e9; j = 10
tau_below = math.nextafter(j * tw_, 0.0)
print("    dt = tau - m*tw cancellation: tau one ulp below 1e10 with tw=1e9: dt_float =", tau_below - 9 * tw_, "(exact dt = tw - 1.9e-6)")
dtf = tau_above = math.nextafter(j * tw_, 1e11) - j * tw_
print("    tau one ulp above 1e10: dt_float =", dtf, "-> Kg*sqrt(dt) = Kg*%.4g where exact sqrt(1.9e-6)=1.38e-3 is the ulp-scale noise floor" % math.sqrt(dtf))
