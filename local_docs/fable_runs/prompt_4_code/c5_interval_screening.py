"""C5: interval screening. f is coordinatewise monotone (pointwise in tau) in a, Kg, Ks, d0, R, tw, lambda, so
winning set(pessimistic corner) <= winning set(any input in the box) <= winning set(optimistic corner).

Definitions (brief): lam = lambda_E >= 0 with f containing -lam (d0 = D - lam); winning set = {tau>=0: f<0}.
Directions derived here (not assumed): df/da = tau >= 0, df/dKg = sqrt(dt) + m sqrt(tw) >= 0, df/dKs = -sqrt(tau) <= 0,
df/dd0 = +1, df/dR = m >= 0, df/dlam = -1, df/dtw <= 0 (C4).
 pessimistic corner (worst for geometry = largest f): a max, Kg max, Ks MIN, d0 max, R max, tw MIN, lam MIN.
 optimistic corner: a min, Kg min, Ks MAX, d0 min, R min, tw MAX, lam MAX.
Run: <gms-local>/.venv/bin/python c5_interval_screening.py
Method:
 (1) SymPy partial derivatives (within a segment) and sign table.
 (2) Hypothesis (exact Fractions + mp 60 digits, >= 3000 examples each): single-coordinate monotonicity incl.
     tw across segment boundaries; box inclusion at random tau, tau = j*tw for corner and interior tw, and tau +- 1 ulp.
 (3) Does C5 for tw follow from C4? Logic check in text + the s2 > tau extension.
 (4) float64 f_float inclusion violations (counts and magnitude), to size the solver tolerance.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math, random
from fractions import Fraction
import sympy as sp
import mpmath as mp
from hypothesis import given, settings, strategies as st, HealthCheck
from common import f_mp, f_float, Cov, logfloat, _mpf

# ---------------------------------------------------------------- (1)
tau, tw, a, Kg, Ks, R, D, lam, m, dtv = sp.symbols("tau tw a K_g K_s R D lam m dt", positive=True)
f_sym = a * tau + Kg * sp.sqrt(tau - m * tw) - Ks * sp.sqrt(tau) + D - lam + m * R + m * Kg * sp.sqrt(tw)
print("(1) partial derivatives of f within a segment (m = floor(tau/tw) held fixed):")
for v in (a, Kg, Ks, D, R, lam, tw):
    print("    df/d%s = %s" % (v, sp.simplify(sp.diff(f_sym, v))))
print("    df/dtw (m fixed) = m*Kg*(1/(2 sqrt(tw)) - 1/(2 sqrt(dt))) <= 0 since dt < tw; across m-changes: m R jumps down, Kg-part continuous (c4).")
print("    signs: a:+(tau>=0)  Kg:+  Ks:-  d0:+  R:+(m>=0)  lam:-  tw:-   (so pessimistic uses Ks MIN, lam MIN, tw MIN)")

# ---------------------------------------------------------------- helpers
cov = Cov()
S = dict(database=None, derandomize=True, deadline=None, max_examples=3000, suppress_health_check=list(HealthCheck))
NAMES = ["a", "Kg", "Ks", "d0", "R", "tw", "lam"]

def F(taq, p):
    return f_mp(taq, p["tw"], p["a"], p["Kg"], p["Ks"], p["R"], p["d0"], p["lam"])

def corners(lo, hi):
    pess = dict(a=hi["a"], Kg=hi["Kg"], Ks=lo["Ks"], d0=hi["d0"], R=hi["R"], tw=lo["tw"], lam=lo["lam"])
    opt = dict(a=lo["a"], Kg=lo["Kg"], Ks=hi["Ks"], d0=lo["d0"], R=lo["R"], tw=hi["tw"], lam=hi["lam"])
    return pess, opt

def ulp_nb(x):
    return [math.nextafter(x, 0.0), x, math.nextafter(x, math.inf)]

def pair(st_lo, st_hi_extra):
    """strategy producing (lo, hi) with lo<=hi, degenerate lo==hi mixed in"""
    return st.builds(lambda x, y, deg: (x, x) if deg else (min(x, y), max(x, y)), st_lo, st_hi_extra, st.booleans())

TW = st.one_of(st.sampled_from([1e3, 1e9, 1.0, 0.5]), logfloat(st, 0, 9, zero=False))
pos = logfloat(st, -3, 3)
A = st.one_of(st.just(0.0), st.floats(-1e-3, 1e-3))
box = st.fixed_dictionaries(dict(
    a=pair(A, A), Kg=pair(pos, pos), Ks=pair(pos, pos), d0=pair(st.floats(-1e6, 1e6), st.floats(-1e6, 1e6)),
    R=pair(logfloat(st, -3, 6), logfloat(st, -3, 6)), tw=pair(TW, TW), lam=pair(logfloat(st, -3, 6), logfloat(st, -3, 6))))
pt = st.fixed_dictionaries(dict(a=st.floats(0, 1), Kg=st.floats(0, 1), Ks=st.floats(0, 1), d0=st.floats(0, 1),
                                R=st.floats(0, 1), tw=st.floats(0, 1), lam=st.floats(0, 1), vtx=st.integers(0, 127)))

def pick(lo, hi, u, mode_vertex, vtx):
    """interior point or vertex of the box; coordinates as floats within [lo,hi]"""
    out = {}
    for i, n in enumerate(NAMES):
        if mode_vertex:
            out[n] = hi[n] if (vtx >> i) & 1 else lo[n]
        else:
            v = lo[n] + u[n] * (hi[n] - lo[n])
            out[n] = min(max(v, lo[n]), hi[n])
    return out

# ---------------------------------------------------------------- (2a) single-coordinate monotonicity
tau_strategy = st.one_of(st.sampled_from([0.0, 1.0, 1e3, 1e9, 1e10]), logfloat(st, -2, 10, zero=False))
@settings(**S)
@given(base=box, u=pt, tauf=tau_strategy, which=st.sampled_from(NAMES), jj=st.integers(1, 10 ** 5),
       mode=st.sampled_from(["rand", "tie_lo", "tie_hi", "tie_mid", "ulp"]))
def prop_single(base, u, tauf, which, jj, mode):
    lo = {n: base[n][0] for n in NAMES}; hi = {n: base[n][1] for n in NAMES}
    p0 = pick(lo, hi, u, False, 0)
    # perturb one coordinate up
    p1 = dict(p0)
    if which == "tw":
        p1["tw"] = p0["tw"] * (1 + 10 ** u["tw"] * 1e-3) if u["tw"] > 0.2 else math.nextafter(p0["tw"], math.inf)
    elif which == "a":
        p1["a"] = p0["a"] + 10 ** -(1 + 5 * u["a"])
    elif which == "d0":
        p1["d0"] = p0["d0"] + 10 ** (-3 + 6 * u["d0"])
    else:
        p1[which] = p0[which] + 10 ** (-3 + 6 * u[which])
    # tau choices incl. exact ties for either tw
    if mode == "rand": taus = [Fraction(tauf)]
    elif mode == "tie_lo": taus = [Fraction(jj) * Fraction(p0["tw"])]
    elif mode == "tie_hi": taus = [Fraction(jj) * Fraction(p1["tw"])]
    elif mode == "tie_mid": taus = [Fraction(jj) * Fraction(p0["tw"])  + Fraction(p1["tw"] - p0["tw"]) / 2 * jj]
    else: taus = [Fraction(x) for x in ulp_nb(jj * p0["tw"])]
    cov.hit("s:" + which); cov.hit("s:mode=" + mode)
    cov.hit("s:tw_cross_segment", which == "tw" and any(math.floor(t / Fraction(p0["tw"])) != math.floor(t / Fraction(p1["tw"])) for t in taus))
    sign = {"a": +1, "Kg": +1, "Ks": -1, "d0": +1, "R": +1, "lam": -1, "tw": -1}[which]
    for t in taus:
        f0 = F(t, p0); f1 = F(t, p1)
        tol = mp.mpf(10) ** -40 * (1 + abs(f0) + abs(f1))
        d = (f1 - f0) * sign       # must be >= 0
        assert d >= -tol, ("monotonicity violated", which, p0, p1, float(t), f0, f1)

prop_single()
print("(2a) hypothesis: f coordinatewise monotone in each of 7 coefficients at random tau, exact ties, ulp neighbours (3000 examples)")
cov.report(["s:" + n for n in NAMES] + ["s:mode=tie_lo", "s:mode=tie_hi", "s:mode=tie_mid", "s:mode=ulp", "s:tw_cross_segment"])

# ---------------------------------------------------------------- (2b) box inclusion
cov2 = Cov()
viol_f = {"n": 0, "max": 0.0}
@settings(**S)
@given(b=box, u=pt, tauf=tau_strategy, jj=st.integers(0, 10 ** 5), vertex=st.booleans(),
       mode=st.sampled_from(["rand", "tie_pess", "tie_opt", "tie_any", "tie_ulp", "tau0", "tau<tw"]))
def prop_box(b, u, tauf, jj, vertex, mode):
    lo = {n: b[n][0] for n in NAMES}; hi = {n: b[n][1] for n in NAMES}
    pess, opt = corners(lo, hi)
    anyp = pick(lo, hi, u, vertex, u["vtx"])
    if mode == "rand": ts = [Fraction(tauf)]
    elif mode == "tie_pess": ts = [Fraction(jj) * Fraction(pess["tw"])]
    elif mode == "tie_opt": ts = [Fraction(jj) * Fraction(opt["tw"])]
    elif mode == "tie_any": ts = [Fraction(jj) * Fraction(anyp["tw"])]
    elif mode == "tie_ulp": ts = [Fraction(x) for x in ulp_nb(jj * pess["tw"]) + ulp_nb(jj * opt["tw"])]
    elif mode == "tau0": ts = [Fraction(0)]
    else: ts = [Fraction(pess["tw"]) * Fraction(u["tw"]) * Fraction(9, 10)]    # tau < tw(pess) (so m=0 for pess)
    cov2.hit("b:" + mode); cov2.hit("b:vertex", vertex); cov2.hit("b:degenerate coord", any(lo[n] == hi[n] for n in NAMES))
    cov2.hit("b:Kg=0", lo["Kg"] == 0 or anyp["Kg"] == 0); cov2.hit("b:a=0", anyp["a"] == 0)
    cov2.hit("b:tw distinct", lo["tw"] < hi["tw"]); cov2.hit("b:R=0", lo["R"] == 0)
    for t in ts:
        fp, fa, fo = F(t, pess), F(t, anyp), F(t, opt)
        tol = mp.mpf(10) ** -40 * (1 + abs(fp) + abs(fa) + abs(fo))
        assert fp >= fa - tol and fa >= fo - tol, ("ordering violated", pess, anyp, opt, float(t), fp, fa, fo)
        # win-set inclusion pointwise: strictly f<0 (tol-free test on exactly computed values)
        if fp < -tol: assert fa < 0 and fo < 0
        if fa < -tol: assert fo < 0
        cov2.hit("b:pess wins (f<0)", fp < -tol); cov2.hit("b:opt wins, pess loses", fo < -tol and fp > tol)
        # float64 size of the artefact
        ff = [f_float(float(t), c["tw"], c["a"], c["Kg"], c["Ks"], c["R"], c["d0"], c["lam"]) for c in (pess, anyp, opt)]
        if not (ff[0] >= ff[1] and ff[1] >= ff[2]):
            viol_f["n"] += 1
            viol_f["max"] = max(viol_f["max"], float(max(ff[1] - ff[0], ff[2] - ff[1])))

prop_box()
print("(2b) hypothesis: f_pess >= f_any >= f_opt pointwise, hence win-set inclusion (3000 examples; exact ties, ulp neighbours)")
cov2.report(["b:rand", "b:tie_pess", "b:tie_opt", "b:tie_any", "b:tie_ulp", "b:tau0", "b:tau<tw", "b:vertex",
             "b:degenerate coord", "b:Kg=0", "b:a=0", "b:tw distinct", "b:R=0", "b:pess wins (f<0)", "b:opt wins, pess loses"])
print("(4) float64 f_float ordering violations among the same cases (f_pess>=f_any>=f_opt in float):", viol_f["n"],
      "max reversal size = %.3e (absolute, in f units)" % viol_f["max"])

# ---------------------------------------------------------------- (3) does C5(tw) follow from C4?
print("(3) C5 for tw from C4: yes, with two additions, both checked above.")
print("    f(tau) depends on tw only via G(tw) = Kg [m sqrt(tw) + sqrt(tau - m tw)] + m R, m = floor(tau/tw); the other terms")
print("    (a tau - Ks sqrt(tau) + d0 - lam) do not contain tw. C4 gives Kg-part non-increasing in tw (for tw <= tau) and m R non-increasing.")
print("    Additions: (i) C4 is stated for tau >= tw; for tw > tau, m = 0 and G = Kg sqrt(tau) = G(tw=tau): flat, so monotone on all tw>0 (prop 2c in c4).")
print("    (ii) the extreme corners need coordinatewise monotonicity in the OTHER six coefficients too (derivatives above), and the box")
print("    must be a product of independent intervals (no coupling such as a or Kg depending on tw).")
print("    Counter-scenario NOT excluded by the claim: if a coefficient is a function of tw (e.g. K_g or a re-fitted per tw), C5 can fail. UNSURE: not tested.")
