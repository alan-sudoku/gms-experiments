"""Shared helpers for the prompt 4 solver-lemma red-team scripts.

Not a claim script. Provides:
  f_float  float64 evaluator of f(tau) (global form, m = floor(tau/tw)).
  f_mp     exact-interpretation evaluator: float inputs are read as exact
           rationals, m is an exact floor, sqrt in mpmath at 60 digits.
  f_loc    local-form evaluator on a segment (tw = 1 normalised or general).
  edge-coverage counter helpers.
Conventions (brief): segments [t_m, t_m+1), m = floor(tau/tw); tie tau = j*tw
belongs to segment j. a real; Kg, Ks, R >= 0; d0 real; lam = lambda_E >= 0 with
f containing  - lam.
All results are claims at level `derived`.
"""
import math
from fractions import Fraction
import mpmath as mp

mp.mp.dps = 60


def f_float(tau, tw, a, Kg, Ks, R, d0, lam=0.0):
    m = math.floor(tau / tw)
    dt = max(tau - m * tw, 0.0)
    return (a * tau + Kg * math.sqrt(dt) - Ks * math.sqrt(tau)
            + d0 - lam + m * R + m * Kg * math.sqrt(tw))


def _mpf(q):
    q = Fraction(q)
    return mp.mpf(q.numerator) / mp.mpf(q.denominator)


def f_mp(tau, tw, a, Kg, Ks, R, d0, lam=0):
    """Exact reading of the inputs (floats or Fractions), 60-digit sqrt."""
    tau, tw = Fraction(tau), Fraction(tw)
    m = math.floor(tau / tw)
    dt = tau - m * tw  # exact, 0 <= dt < tw
    return (_mpf(a) * _mpf(tau) + _mpf(Kg) * mp.sqrt(_mpf(dt))
            - _mpf(Ks) * mp.sqrt(_mpf(tau)) + _mpf(d0) - _mpf(lam)
            + m * _mpf(R) + m * _mpf(Kg) * mp.sqrt(_mpf(tw)))


def f_loc(dt, m, tw, a, Kg, Ks, dprime):
    """Local form: f(dt) = a(t_m+dt) + Kg sqrt(dt) - Ks sqrt(t_m+dt) + d'_m (float)."""
    tm = m * tw
    return a * (tm + dt) + Kg * math.sqrt(dt) - Ks * math.sqrt(tm + dt) + dprime


class Cov:
    """Edge-case coverage counter; assert_min fails loudly if a case is vacuous."""
    def __init__(self):
        self.c = {}

    def hit(self, key, cond=True):
        if cond:
            self.c[key] = self.c.get(key, 0) + 1

    def report(self, names, minimum=20):
        ok = True
        for n in names:
            v = self.c.get(n, 0)
            flag = "" if v >= minimum else "   <-- BELOW MINIMUM (vacuous?)"
            if v < minimum:
                ok = False
            print(f"  coverage {n}: {v}{flag}")
        return ok


def logfloat(st, lo, hi, zero=True):
    """Strategy: log-uniform positive float in [10^lo, 10^hi], optionally 0.0 mixed in."""
    base = st.builds(lambda e: 10.0 ** e, st.floats(lo, hi, allow_nan=False))
    return st.one_of(st.just(0.0), base) if zero else base
