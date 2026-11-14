"""Review of prompt 4, claim C3: long-run verdict from abar, checked with exact abar and targeted tau.

Purpose
  (1) abar = 0 exactly with Ks > 0: tw = q^2 with q rational, so sqrt(tw) = q and a = -(R + Kg q)/q^2 is an
      exact rational; no rounding margin is needed (the implementer's part 5 used a margin |a| 2^-52 tau).
      Verdict 'wins for tau > T0 = (max(d0 + Kg sqrt(tw)/4, 0)/Ks)^2' tested at tau just above T0 and at
      the dt where the upper bound is tight (dt = tw/4).
  (2) How large the implementer's part-5 margin |a| 2^-52 tau was relative to |f| (same strategy shape,
      re-implemented here; not the identical draws).
  (3) abar > 0 and abar < 0 with tiny |abar| (exact rationals): implementer's explicit T, sampled at
      tau in [T, 1.01 T] at the dt where each bound is tight (dt -> tw for the lower bound, dt = tw/4 for the
      upper bound), and exact ties tau = j tw.
  (4) Textbook vs stable root for abar < 0 with |abar| ~ 1e-263 (the implementer reports this only in prose).
Claims: C3. Conventions: brief. Exact rationals + 60-digit mpmath sqrt. Fixed seed.
Run: <gms-local>/.venv/bin/python r2_c3_long_run.py
Level: derived.
"""
import math
import random
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 60


def M(q):
    q = Fr(q)
    return mp.mpf(q.numerator) / q.denominator


def f_exact(tau, tw, a, Kg, Ks, R, d0):
    """Independent exact evaluator: tau, tw Fractions; m exact floor; sqrt at 60 digits."""
    m = (tau.numerator * tw.denominator) // (tau.denominator * tw.numerator)
    dt = tau - m * tw
    return (M(a) * M(tau) + M(Kg) * mp.sqrt(M(dt)) - M(Ks) * mp.sqrt(M(tau)) + M(d0)
            + m * M(R) + m * M(Kg) * mp.sqrt(M(tw)))


def up_frac(x):
    """mp number -> Fraction >= x (resolution 2^-200 relative is ample)."""
    e = int(mp.floor(mp.log(abs(x) + 1, 2))) + 200
    return Fr(int(mp.ceil(x * mp.mpf(2) ** e)), 2 ** e)


def T_impl(tw, a, Kg, Ks, R, d0):
    """Implementer's explicit T (c3_long_run.T_explicit), re-implemented from the answer's formulas."""
    ab = M(a) + (M(R) + M(Kg) * mp.sqrt(M(tw))) / M(tw)
    K = M(Ks)
    if ab > 0:
        c = M(d0) - M(R)
        disc = K * K - 4 * ab * c
        y = (K + mp.sqrt(disc)) / (2 * ab) if disc >= 0 else mp.mpf(0)
        return "loses", y * y, ab
    if ab < 0:
        c = M(d0) + M(Kg) * mp.sqrt(M(tw)) / 4
        if c <= 0:
            return "wins", mp.mpf(0), ab
        y = 2 * c / (K + mp.sqrt(K * K + 4 * (-ab) * c))
        return "wins", y * y, ab
    if K > 0:
        c = M(d0) + M(Kg) * mp.sqrt(M(tw)) / 4
        return "wins", (max(c, 0) / K) ** 2, ab
    return "periodic", mp.mpf(0), ab


def taus_above(T, tw, rng):
    """Targeted tau >= T: dt = tw/4 (upper bound tight), dt = tw (1 - 1e-12) (lower bound nearly tight),
    exact tie j tw, and a random point in [T, 1.01 T]."""
    Tq = up_frac(T) if T > 0 else Fr(0)
    j = (Tq.numerator * tw.denominator) // (Tq.denominator * tw.numerator) + 1
    out = [j * tw + tw / 4, j * tw + tw * (1 - Fr(1, 10 ** 12)), j * tw,
           Tq * (1 + Fr(rng.randint(1, 10 ** 6), 10 ** 8)) + Fr(1, 10 ** 30)]
    return [t for t in out if t > Tq]


def main():
    rng = random.Random(9090)
    # (1) abar = 0 exactly, Ks > 0
    bad = 0
    n = 0
    worst = None
    for _ in range(3000):
        q = Fr(rng.randint(1, 10 ** 5), rng.randint(1, 10 ** 2)) if rng.random() < 0.7 else Fr(rng.choice([1, 10 ** 2, 31623]))
        tw = q * q
        Kg = Fr(0) if rng.random() < 0.3 else Fr(rng.randint(1, 10 ** 6), 10 ** 3)
        R = Fr(0) if rng.random() < 0.3 else Fr(rng.randint(1, 10 ** 9), 10 ** 3)
        Ks = Fr(rng.randint(1, 10 ** 6), 10 ** rng.randint(0, 9))
        d0 = Fr(rng.randint(-10 ** 9, 10 ** 9), 10 ** 3)
        a = -(R + Kg * q) / tw
        assert a + (R + Kg * q) / tw == 0
        c = M(d0) + M(Kg) * M(q) / 4
        T0 = (max(c, 0) / M(Ks)) ** 2
        for t in taus_above(T0, tw, rng):
            n += 1
            f = f_exact(t, tw, a, Kg, Ks, R, d0)
            if not f < 0:
                bad += 1
            rel = f / (M(Ks) * mp.sqrt(M(t)))
            if worst is None or rel > worst[0]:
                worst = (rel, float(t), float(tw))
    print("(1) abar = 0 exactly (rational sqrt(tw)), Ks > 0: tau > T0 points tested:", n, "; f >= 0 found:", bad)
    print("    closest approach to 0: max f/(Ks sqrt(tau)) =", mp.nstr(worst[0], 6), "(must be < 0)")

    # (2) size of the implementer's part-5 margin |a| 2^-52 tau relative to |f| at the tested tau
    ratios = []
    vac = 0
    for _ in range(3000):
        tw = 10 ** rng.uniform(-3, 9)
        Kg = 0.0 if rng.random() < 0.3 else 10 ** rng.uniform(-3, 3)
        R = 0.0 if rng.random() < 0.3 else 10 ** rng.uniform(-3, 6)
        Ks = 10 ** rng.uniform(-6, 3)
        d0 = 0.0 if rng.random() < 0.2 else rng.uniform(-1e8, 1e8)
        k = rng.randint(0, 200)
        s = math.sqrt(tw)
        tw2 = s * s
        a = float(-(M(R) + M(Kg) * mp.sqrt(M(tw2))) / M(tw2))
        c = M(d0) + M(Kg) * mp.sqrt(M(tw2)) / 4
        T0 = (max(c, 0) / M(Ks)) ** 2
        tq = up_frac(T0) * (4 + k) + Fr(tw2)
        f = f_exact(tq, Fr(tw2), a, Kg, Ks, R, d0)
        margin = abs(M(a)) * mp.mpf(2) ** -52 * M(tq)
        r = margin / abs(f)
        ratios.append(r)
        if r >= 1:
            vac += 1
    ratios.sort()
    print("(2) implementer's part-5 margin |a| 2^-52 tau versus |f| at the tested tau (3000 draws, same strategy shape):")
    print("    median ratio = %.3g, 99th pct = %.3g, max = %.3g; draws with margin >= |f| (assertion vacuous): %d"
          % (float(ratios[1500]), float(ratios[2970]), float(ratios[-1]), vac))

    # (3) tiny |abar| of both signs, exact rationals; implementer's T sampled where bounds are tight
    bad3 = 0
    sharp = 0
    tie0 = 0
    n3 = {"loses": 0, "wins": 0}
    for _ in range(3000):
        q = Fr(rng.randint(1, 10 ** 4), rng.randint(1, 10))
        tw = q * q
        Kg = Fr(0) if rng.random() < 0.3 else Fr(rng.randint(1, 10 ** 6), 10 ** 3)
        R = Fr(0) if rng.random() < 0.3 else Fr(rng.randint(1, 10 ** 9), 10 ** 3)
        Ks = Fr(0) if rng.random() < 0.3 else Fr(rng.randint(1, 10 ** 6), 10 ** 3)
        d0 = Fr(rng.randint(-10 ** 9, 10 ** 9), 10 ** 3)
        eps = Fr(rng.choice([-1, 1]), 10 ** rng.randint(1, 12)) / tw
        a = -(R + Kg * q) / tw + eps          # abar = eps exactly
        case, T, ab = T_impl(tw, a, Kg, Ks, R, d0)
        if case == "periodic":
            continue
        n3[case] += 1
        # strict margin: abar = a + (...) cancels by up to 1e17 here, so the 60-digit T is good to ~1e-43
        # relative; a tau within 1e-30 relative of T may equal the exact T, where f = 0 is possible (sharp bound)
        Tm = T * (1 + mp.mpf(10) ** -30)
        for t in taus_above(Tm, tw, rng):
            f = f_exact(t, tw, a, Kg, Ks, R, d0)
            if (case == "loses" and not f > 0) or (case == "wins" and not f < 0):
                bad3 += 1
                if bad3 <= 3:
                    print("    VIOLATION", case, float(t), float(tw), float(a), float(Kg), float(Ks), float(R), float(d0), f)
        # sharpness: at the tie j tw just at or below T with R = 0 the lower bound is attained (f = g(tau))
        if case == "loses" and R == 0 and T > 0:
            Tq = up_frac(T)
            j = (Tq.numerator * tw.denominator) // (Tq.denominator * tw.numerator)
            if j >= 1:
                t = j * tw
                g = M(a + (R + Kg * q) / tw) * M(t) - M(Ks) * mp.sqrt(M(t)) + M(d0) - M(R)
                if abs(f_exact(t, tw, a, Kg, Ks, R, d0) - g) <= mp.mpf(10) ** -40 * (1 + abs(g)):
                    sharp += 1
                    if f_exact(t, tw, a, Kg, Ks, R, d0) == 0:
                        tie0 += 1
    print("(3) tiny |abar| = 1e-1..1e-12 / tw, exact rationals: cases", n3,
          "; verdict violations at targeted tau > T (1+1e-30):", bad3)
    print("    R = 0, abar > 0: lower bound attained exactly at the tie j tw <= T in", sharp,
          "cases; f == 0 exactly there (tie at tau = T, not a win, not a loss-violation) in", tie0, "cases")

    # (4) textbook root vs stable root for abar < 0, |abar| = 1e-263
    ab = -mp.mpf(10) ** -263
    K, c = mp.mpf(1), mp.mpf(1)
    y_text = (-K + mp.sqrt(K * K + 4 * (-ab) * c)) / (2 * (-ab))
    y_stab = 2 * c / (K + mp.sqrt(K * K + 4 * (-ab) * c))
    print("(4) abar = -1e-263, Ks = 1, c = 1 at 60 digits: textbook root y =", mp.nstr(y_text, 6),
          "; stable root y =", mp.nstr(y_stab, 6), "(true y ~ c/Ks = 1)")


if __name__ == "__main__":
    main()
