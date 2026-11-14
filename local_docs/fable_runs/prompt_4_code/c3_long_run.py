"""C3: long-run verdict from abar = a + (R_g + K_g sqrt(tw))/tw.

Assumptions: common.py conventions (f<0 wins, ties f=0 are not wins).
Run: <gms-local>/.venv/bin/python c3_long_run.py
Method:
 (1) SymPy exact decomposition  f = abar*tau + (a-abar)*dt + Kg sqrt(dt) - Ks sqrt(tau) + d0
     (an identity; flagged) and the two bounds that give explicit T:
        f >= abar*tau - Ks sqrt(tau) + d0 - R         (lower)
        f <= abar*tau - Ks sqrt(tau) + d0 + Kg sqrt(tw)/4   (upper)
     proofs by SymPy/one-variable maximisation.
 (2) Hypothesis (>= 2000/property, mp 60 digits): both bounds hold at random tau.
 (3) Explicit T per case; hypothesis: verdict holds on sampled tau >= T incl. near ties j*tw.
 (4) abar = 0, Ks = 0: exact periodicity with Fractions (perfect-square dt, tw); SymPy symbolic.
 (5) abar = 0, Ks > 0: wins eventually for every d0, R, Kg (explicit T), edge Kg=0, R=0.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math
from fractions import Fraction
import sympy as sp
import mpmath as mp
from hypothesis import given, settings, strategies as st, HealthCheck
from common import f_mp, f_float, Cov, logfloat, _mpf

def mpq(x):
    """mp number -> Fraction (rounded up at 2^-80 resolution)."""
    return Fraction(int(mp.ceil(x * mp.mpf(2) ** 80)), 2 ** 80)

# ---------------------------------------------------------------- (1) SymPy
tau, tw, a, Kg, Ks, R, d0, dt, m = sp.symbols("tau tw a K_g K_s R d0 dt m", positive=True)
abar = a + (R + Kg * sp.sqrt(tw)) / tw
f_global = a * tau + Kg * sp.sqrt(dt) - Ks * sp.sqrt(tau) + d0 + m * R + m * Kg * sp.sqrt(tw)
f_dec = abar * tau + (a - abar) * dt + Kg * sp.sqrt(dt) - Ks * sp.sqrt(tau) + d0
# with tau = m*tw + dt
diff = sp.simplify((f_global - f_dec).subs(tau, m * tw + dt))
print("(1) f - [abar*tau + (a-abar)*dt + Kg sqrt(dt) - Ks sqrt(tau) + d0] =", diff, " [identity by algebra: flagged as true by construction]")
# remainder term r(dt) = (a-abar)dt + Kg sqrt(dt) = -(R/tw) dt + Kg (sqrt(dt) - dt/sqrt(tw))
r = -(R / tw) * dt + Kg * (sp.sqrt(dt) - dt / sp.sqrt(tw))
print("    remainder r(dt) - ((a-abar)dt + Kg sqrt(dt)) =", sp.simplify(r - ((a - abar) * dt + Kg * sp.sqrt(dt))))
u = sp.symbols("u", positive=True)  # u = sqrt(dt/tw) in (0,1)
rg = sp.simplify((sp.sqrt(u ** 2 * tw) - u ** 2 * tw / sp.sqrt(tw)).subs(tw, sp.symbols("w", positive=True)))
w = sp.symbols("w", positive=True)
q = sp.sqrt(w) * (u - u ** 2)
print("    Kg*(sqrt(dt)-dt/sqrt(tw)) = Kg sqrt(tw) (u - u^2): max at u=1/2 =", sp.simplify(q.subs(u, sp.Rational(1, 2))), " (=sqrt(tw)/4), >=0 on u in [0,1] since u>=u^2")
print("    => 0 - R <= r(dt) <= Kg sqrt(tw)/4  (as R dt/tw in [0,R)); hence the two bounds. Proof is closed-form, not numeric.")

# ---------------------------------------------------------------- (2) bounds property
cov = Cov()
settings_kw = dict(database=None, derandomize=True, deadline=None, max_examples=3000,
                   suppress_health_check=list(HealthCheck))
tws = st.one_of(st.sampled_from([1e3, 1e9, 1.0, 1e-3]), logfloat(st, -3, 9, zero=False))
taus = st.floats(0.0, 1.0)

@settings(**settings_kw)
@given(tw=tws, a=st.one_of(st.just(0.0), st.floats(-1e-2, 1e-2)), Kg=logfloat(st, -3, 3), Ks=logfloat(st, -3, 3),
       R=logfloat(st, -3, 6), d0=st.floats(-1e6, 1e6),
       mm=st.one_of(st.sampled_from([0, 1, 2, 3]), st.integers(0, 10 ** 6)),
       frac=st.one_of(st.sampled_from([0.0, 0.25, 0.5, 0.999999]), taus),
       tie=st.booleans())
def prop_bounds(tw, a, Kg, Ks, R, d0, mm, frac, tie):
    ab = mp.mpf(a) + (mp.mpf(R) + mp.mpf(Kg) * mp.sqrt(_mpf(tw))) / _mpf(tw)
    tq = Fraction(mm) * Fraction(tw) + (Fraction(0) if tie else Fraction(frac) * Fraction(tw))
    cov.hit("b:Kg=0", Kg == 0); cov.hit("b:R=0", R == 0); cov.hit("b:a=0", a == 0); cov.hit("b:Ks=0", Ks == 0)
    cov.hit("b:tie", tie); cov.hit("b:m=0", mm == 0)
    f = f_mp(tq, tw, a, Kg, Ks, R, d0)
    t = _mpf(tq)
    low = ab * t - _mpf(Ks) * mp.sqrt(t) + _mpf(d0) - _mpf(R)
    up = ab * t - _mpf(Ks) * mp.sqrt(t) + _mpf(d0) + _mpf(Kg) * mp.sqrt(_mpf(tw)) / 4
    eps = mp.mpf(10) ** -40 * (1 + abs(f) + abs(low) + abs(up))
    assert low - eps <= f <= up + eps, (tw, a, Kg, Ks, R, d0, mm, frac, tie, low, f, up)

prop_bounds()
print("(2) hypothesis: lower/upper bounds on f hold (3000 examples)")
cov.report(["b:Kg=0", "b:R=0", "b:a=0", "b:Ks=0", "b:tie", "b:m=0"])

# ---------------------------------------------------------------- (3) explicit T
def T_explicit(tw, a, Kg, Ks, R, d0):
    """Return (case, T) with the verdict valid for ALL tau >= T (from the bounds, in exact reals/mp)."""
    ab = mp.mpf(a) + (mp.mpf(R) + mp.mpf(Kg) * mp.sqrt(_mpf(tw))) / _mpf(tw)
    K = mp.mpf(Ks)
    if ab > 0:
        c = mp.mpf(d0) - mp.mpf(R)          # ab y^2 - K y + c > 0 for y > y+
        disc = K * K - 4 * ab * c
        y = (K + mp.sqrt(disc)) / (2 * ab) if disc >= 0 else mp.mpf(0)
        return "loses", y * y
    if ab < 0:
        c = mp.mpf(d0) + mp.mpf(Kg) * mp.sqrt(_mpf(tw)) / 4   # -|ab| y^2 - K y + c < 0 for y > y0
        if c <= 0:
            return "wins", mp.mpf(0)
        y = 2 * c / (K + mp.sqrt(K * K + 4 * (-ab) * c))   # stable form of the positive root (the textbook form cancels when |abar| is tiny)
        return "wins", y * y
    # ab == 0 (exactly in mp from float inputs only if constructed exactly; see (4))
    if K > 0:
        c = mp.mpf(d0) + mp.mpf(Kg) * mp.sqrt(_mpf(tw)) / 4
        y = max(c, 0) / K
        return "wins", y * y
    return "periodic", mp.mpf(0)

cov3 = Cov()
@settings(**settings_kw)
@given(tw=tws, a=st.floats(-1e-2, 1e-2), Kg=logfloat(st, -3, 3), Ks=logfloat(st, -3, 3), R=logfloat(st, -3, 6),
       d0=st.floats(-1e6, 1e6), mult=st.one_of(st.sampled_from([1.0, 1.0000001, 2.0, 10.0]), st.floats(1.0, 1e4)),
       jj=st.integers(0, 50), tie=st.booleans(), shift=st.sampled_from(["abar>0", "abar<0", "free"]),
       rel=logfloat(st, -3, 3, zero=False))
def prop_T(tw, a, Kg, Ks, R, d0, mult, jj, tie, shift, rel):
    if shift == "abar>0":
        a = -(R + Kg * math.sqrt(tw)) / tw + rel * 1e-3 / max(1.0, tw ** 0.5)
    elif shift == "abar<0":
        a = -(R + Kg * math.sqrt(tw)) / tw - rel * 1e-3 / max(1.0, tw ** 0.5)
    case, T = T_explicit(tw, a, Kg, Ks, R, d0)
    cov3.hit("T:" + case); cov3.hit("T:Ks=0", Ks == 0); cov3.hit("T:Kg=0", Kg == 0); cov3.hit("T:R=0", R == 0)
    cov3.hit("T:tie", tie)
    if case == "periodic":
        return
    # sample tau >= T: scale T by mult (+ tie at a multiple of tw just above T)
    Tf = mpq(T) * Fraction(mult) + Fraction(1, 1)
    jmin = math.ceil(Tf / Fraction(tw)) + jj
    tq = Fraction(jmin) * Fraction(tw) if tie else Tf + Fraction(jj) * Fraction(tw) / 7
    f = f_mp(tq, tw, a, Kg, Ks, R, d0)
    mag = abs(_mpf(a) * _mpf(tq)) + _mpf(Ks) * mp.sqrt(_mpf(tq)) + abs(_mpf(d0)) + _mpf(Kg) * mp.sqrt(_mpf(tw)) * (1 + _mpf(tq) / _mpf(tw)) + (_mpf(tq) / _mpf(tw)) * _mpf(R) + 1
    tol = mp.mpf(10) ** -40 * mag   # cancellation margin: terms may be huge when T is huge (abar tiny)
    if case == "loses":
        assert f > -tol, ("claimed permanent loss violated", tw, a, Kg, Ks, R, d0, float(tq), f)
    else:
        assert f < tol, ("claimed permanent win violated", tw, a, Kg, Ks, R, d0, float(tq), f)

prop_T()
print("(3) hypothesis: explicit-T verdict holds on sampled tau >= T incl. exact ties (3000 examples)")
cov3.report(["T:loses", "T:wins", "T:Ks=0", "T:Kg=0", "T:R=0", "T:tie"])
print("    NOTE: abar is computed in float64 inside the strategy (shift modes put abar within ~1e-3 relative of 0);")
print("    the exact abar sign is recomputed in mp inside T_explicit, so a float sign flip cannot hide.")

# ---------------------------------------------------------------- (4) abar = 0, Ks = 0 periodicity (exact)
print("(4) abar = 0, Ks = 0 periodicity:")
dtt = sp.symbols("dtt", positive=True)
mm_ = sp.symbols("mm", integer=True, nonnegative=True)
tw_s, Kg_s, R_s, d_s = sp.symbols("tw K_g R d", positive=True)
a_zero = -(R_s + Kg_s * sp.sqrt(tw_s)) / tw_s
def fseg(mv):
    return a_zero * (mv * tw_s + dtt) + Kg_s * sp.sqrt(dtt) + d_s + mv * R_s + mv * Kg_s * sp.sqrt(tw_s)
print("    SymPy f_{m+1}(dt) - f_m(dt) with a = -(R+Kg sqrt(tw))/tw, Ks = 0:", sp.simplify(fseg(mm_ + 1) - fseg(mm_)))
import random
rng = random.Random(7)
bad = 0; N = 4000
for _ in range(N):
    q = Fraction(rng.randint(1, 10 ** 6), rng.randint(1, 10 ** 3)) ** 2     # tw = q^2, sqrt(tw)=q exact
    sq = math.isqrt(q.numerator) ; sqtw = Fraction(math.isqrt(q.numerator), math.isqrt(q.denominator))
    assert sqtw * sqtw == q
    Kgq = Fraction(rng.randint(0, 50), rng.randint(1, 7)); Rq = Fraction(rng.randint(0, 50), rng.randint(1, 7))
    dq = Fraction(rng.randint(-50, 50), rng.randint(1, 7))
    aq = -(Rq + Kgq * sqtw) / q
    r_ = Fraction(rng.randint(0, 10 ** 3), 10 ** 3) * sqtw        # sqrt(dt) = r_ (dt = r_^2 < tw if r_<sqtw)
    if r_ >= sqtw: r_ = sqtw / 2
    dt_ = r_ * r_
    def fexact(mv):
        t = mv * q + dt_
        return aq * t + Kgq * r_ + dq + mv * Rq + mv * Kgq * sqtw
    vals = {fexact(k) for k in (0, 1, 2, 17, 10 ** 6)}
    if len(vals) != 1: bad += 1
print(f"    exact Fraction check, {N} random rational instances (tw=q^2, dt=r^2, m in 0,1,2,17,1e6): non-periodic instances = {bad}")
print("    Consequence: f takes the same values every period, so wins/loses are periodic with period tw (the claim says only 'periodic', which holds; it does not claim 'eventually wins' for Ks=0).")
# a concrete periodic example: Kg=1,R=0,tw=1,d0=-0.5,a=-1,Ks=0: f = -dt + sqrt(dt) - 0.5 ; max .25-.5 <0 => wins always; d0=+1 => never wins
for d0_ in (Fraction(-1, 2), Fraction(1, 1), Fraction(-1, 8)):
    pat = []
    for u_ in (Fraction(0), Fraction(1, 16), Fraction(1, 4), Fraction(9, 16), Fraction(15, 16)):
        # sqrt(dt)=u_ ... dt=u_^2, tw=1, Kg=1, R=0, a=-1
        pat.append(float(-(u_ * u_) + u_ + d0_))
    print(f"    tw=1,Kg=1,R=0,Ks=0,a=-1,d0={d0_}: f at sqrt(dt)=0,1/16,1/4,9/16,15/16 = {[round(x,4) for x in pat]}  (same on every segment)")

# ---------------------------------------------------------------- (5) abar = 0, Ks > 0 explicit
print("(5) abar = 0, Ks > 0: f <= -Ks sqrt(tau) + d0 + Kg sqrt(tw)/4 -> wins for tau > T0 = (max(d0+Kg sqrt(tw)/4,0)/Ks)^2")
cov5 = Cov()
@settings(**settings_kw)
@given(tw=tws, Kg=logfloat(st, -3, 3), R=logfloat(st, -3, 6), Ks=logfloat(st, -6, 3, zero=False),
       d0=st.one_of(st.just(0.0), st.floats(-1e8, 1e8)), k=st.integers(0, 200), tie=st.booleans())
def prop_zero(tw, Kg, R, Ks, d0, k, tie):
    # exact abar = 0: choose a as the exact rational? sqrt(tw) is irrational in general -> use tw perfect square float
    s = math.sqrt(tw)
    tw2 = s * s   # re-define tw := s*s (float); sqrt exact only to rounding; abar then ~1e-17 relative, handled by mp with a set from mp
    a_mp = -(mp.mpf(R) + mp.mpf(Kg) * mp.sqrt(_mpf(tw2))) / _mpf(tw2)
    a = float(a_mp)  # abar in the mp evaluation is then O(1e-17*|a|), so verify the final verdict with margin
    c = mp.mpf(d0) + mp.mpf(Kg) * mp.sqrt(_mpf(tw2)) / 4
    T0 = (max(c, 0) / mp.mpf(Ks)) ** 2
    cov5.hit("z:Kg=0", Kg == 0); cov5.hit("z:R=0", R == 0); cov5.hit("z:d0>0", d0 > 0); cov5.hit("z:tie", tie)
    # abar residual: |abar_float| <= 2^-52 * |a| ; contributes at most |abar|*tau; take tau = (1+k)*T0*4 + tw  with margin check
    tq = mpq(T0) * (4 + k) + Fraction(tw2)
    if tie:
        tq = Fraction(math.ceil(tq / Fraction(tw2))) * Fraction(tw2)
    f = f_mp(tq, tw2, a, Kg, Ks, R, d0)
    abar_res = abs(a) * mp.mpf(2) ** -52
    # f_true(abar=0) <= f(this) - abar_res*tau ... simply require f < abar_res*tau (exact-abar=0 f would be < 0)
    assert f < abar_res * _mpf(tq) + mp.mpf(10) ** -30, ("not eventually winning", tw2, Kg, R, Ks, d0, float(tq), f)

prop_zero()
print("    hypothesis passed (3000 examples); abar rounding residual |a|*2^-52*tau is subtracted as margin")
cov5.report(["z:Kg=0", "z:R=0", "z:d0>0", "z:tie"])
print("    Edge: Ks tiny (1e-6) makes T0 huge: T0 = (d0+Kg sqrt(tw)/4)^2/Ks^2. Example d0=1e6,Ks=1e-6 -> T0 ~ 1e24 s (valid but physically irrelevant).")
