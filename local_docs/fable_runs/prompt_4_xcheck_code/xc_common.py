"""Shared evaluator for the Prompt 4 cross-check (written independently from the block in fable_questions.md).

f(dt) = a*(tm+dt) + Kg*sqrt(dt) - Ks*sqrt(tm+dt) + dprime,  tm = m*tw,
dprime = d0 + m*Rg + m*Kg*sqrt(tw).  Win means f < 0.
Provides float, mpmath (50 digits) and exact-m helpers.  Not runnable on its own.
"""
import math
from fractions import Fraction
import mpmath as mp

mp.mp.dps = 50


def dprime(d0, m, Rg, Kg, tw):
    return d0 + m * Rg + m * Kg * math.sqrt(tw)


def f_seg(dt, tm, a, Kg, Ks, dp):
    """f on a segment in local time, dprime given."""
    return a * (tm + dt) + Kg * math.sqrt(dt) - Ks * math.sqrt(tm + dt) + dp


def fp_seg(dt, tm, a, Kg, Ks):
    return a + Kg / (2 * math.sqrt(dt)) - Ks / (2 * math.sqrt(tm + dt))


def f_full(tau, a, Kg, Ks, Rg, d0, tw, lam=0.0, j=None):
    """f at absolute tau (float). j: optional integer segment index (tie carried as integer, dt=0)."""
    if j is None:
        m = int(math.floor(tau / tw))
        dt = tau - m * tw
    else:
        m = j
        dt = tau - j * tw if tau != j * tw else 0.0
    tm = m * tw
    dp = d0 - lam + m * Rg + m * Kg * math.sqrt(tw)
    return a * (tm + dt) + Kg * math.sqrt(dt) - Ks * math.sqrt(tm + dt) + dp


def f_full_mp(tau, a, Kg, Ks, Rg, d0, tw, lam=0.0, m=None):
    """f at absolute tau, everything converted exactly to 50-digit mpf. tau, a, ... may be float/Fraction/mpf.
    m: exact integer segment index (default floor of exact tau/tw)."""
    M = mp.mpf
    conv = lambda x: M(x.numerator) / M(x.denominator) if isinstance(x, Fraction) else M(x)
    tau, a, Kg, Ks, Rg, d0, tw, lam = [conv(x) for x in (tau, a, Kg, Ks, Rg, d0, tw, lam)]
    if m is None:
        m = int(mp.floor(tau / tw))
    dt = tau - m * tw
    tm = m * tw
    dp = d0 - lam + m * Rg + m * Kg * mp.sqrt(tw)
    return a * (tm + dt) + Kg * mp.sqrt(dt) - Ks * mp.sqrt(tm + dt) + dp
