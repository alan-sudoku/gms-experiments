"""C2: f(t_m-) - f(t_m) = -R_g at every boundary m >= 1.

Assumptions: conventions in common.py. m = 0 has no boundary (f starts at tau = 0).
Run: <gms-local>/.venv/bin/python c2_boundary_jump.py
Checks:
  (1) SymPy, symbolic m: difference of segment m-1 at dt = tw and segment m at dt = 0.
      NOTE: this is an algebraic identity of the stated formula for d_m'; it is
      true by construction of d_m' (d_m' was defined to give this jump). Flagged.
  (2) hypothesis (>= 2000 examples, mp 60 digits): left limit computed as the
      real limit of the global evaluator f_mp(t_m - eps) with eps = 1e-40*tw
      vs f_mp(t_m); jump -> -R. This is a genuine check of the global formula
      (m = floor(tau/tw)) against the local-form claim.
  (3) float64: size of the artefact in f_float one ulp below / at j*tw.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
from fractions import Fraction
import sympy as sp
import mpmath as mp
from hypothesis import given, settings, strategies as st, HealthCheck
from common import f_float, f_mp, Cov, logfloat

# (1) symbolic
m, tw, a, Kg, Ks, R, d0 = sp.symbols("m tw a K_g K_s R d0", real=True)
dt = sp.symbols("dt", positive=True)
def seg(mm, x):
    tm = mm * tw
    dprime = d0 + mm * R + mm * Kg * sp.sqrt(tw)
    return a * (tm + x) + Kg * sp.sqrt(x) - Ks * sp.sqrt(tm + x) + dprime
left = seg(m - 1, tw)     # f(t_m^-) from segment m-1 at dt = tw
right = seg(m, 0)         # f(t_m)  from segment m at dt = 0
print("(1) SymPy f(t_m-) - f(t_m) =", sp.simplify(left - right), " [identity by construction of d_m']")

cov = Cov()
@settings(database=None, derandomize=True, deadline=None, max_examples=2500,
          suppress_health_check=list(HealthCheck))
@given(tw=st.one_of(st.sampled_from([1e3, 1e9, 1.0, 1e-3]), logfloat(st, -3, 9, zero=False)),
       m=st.one_of(st.sampled_from([1, 2, 3, 10 ** 6]), st.integers(1, 10 ** 7)),
       a=st.one_of(st.just(0.0), st.floats(-1e-3, 1e-3)),
       Kg=logfloat(st, -3, 3), Ks=logfloat(st, -3, 3), R=logfloat(st, -3, 6),
       d0=st.one_of(st.just(0.0), st.floats(-1e6, 1e6)))
def prop(tw, m, a, Kg, Ks, R, d0):
    cov.hit("Kg=0", Kg == 0); cov.hit("a=0", a == 0); cov.hit("R=0", R == 0)
    cov.hit("Ks=0", Ks == 0); cov.hit("m>=1e6", m >= 10 ** 6); cov.hit("tw>=1e3", tw >= 1e3)
    tmq = Fraction(m) * Fraction(tw)
    eps = Fraction(tw) * Fraction(1, 10 ** 40)
    below = f_mp(tmq - eps, tw, a, Kg, Ks, R, d0)
    at = f_mp(tmq, tw, a, Kg, Ks, R, d0)
    # allow continuous part moving by <= (|a|+...)*eps: use generous bound
    slack = mp.mpf(10) ** -30 * (1 + abs(mp.mpf(a)) * mp.mpf(Fraction(tw).numerator) / Fraction(tw).denominator)
    jump = below - at
    assert abs(jump + mp.mpf(R)) < mp.mpf(10) ** -10 * (1 + mp.mpf(R)) , (tw, m, a, Kg, Ks, R, d0, jump)

prop()
print("(2) hypothesis C2 passed (2500 examples, tolerance 1e-10 relative on a sqrt(eps)-type term)")
cov.report(["Kg=0", "a=0", "R=0", "Ks=0", "m>=1e6", "tw>=1e3"])

# (3) float64 behaviour at ties
print("(3) float64 behaviour near t_m (exact value via f_mp):")
for (tw_, m_, R_, Kg_) in [(1e9, 10 ** 7, 5.0, 3.0), (1e3, 10 ** 6, 5.0, 3.0), (0.1, 3, 5.0, 3.0)]:
    t = m_ * tw_
    for lab, tau in [("t_m", t), ("nextbelow", math.nextafter(t, 0.0))]:
        ff = f_float(tau, tw_, 0.0, Kg_, 0.0, R_, 0.0)
        fe = f_mp(tau, tw_, 0.0, Kg_, 0.0, R_, 0.0)
        print(f"   tw={tw_:g} m={m_} {lab}: float={ff:.12g} exact={mp.nstr(fe, 15)} diff={float(ff - fe):.3e}")
