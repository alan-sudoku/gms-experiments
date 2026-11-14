"""Review of prompt 4: float64 issues raised by the answer (tie hazard, cancellation in dt, Ks = Kg at m = 0)
and the solver-tolerance model they imply.

Purpose
  (1) Re-draw the implementer's c4 part-3 sample (random.Random(3), same call order) and split the cases:
      float floor(tau/tw) != j, exact floor of the doubles != j, and float floor != exact floor of the doubles
      (the quantity a solver actually gets wrong). Width of the ambiguous band in ulps; size of the f error.
  (2) Empirical error model of the float64 evaluator when m is right:
        |f_float - f_exact| <= c1 * eps * S + c2 * Kg * ulp(tau) / sqrt(dt + ulp(tau)),
        S = |a tau| + Ks sqrt(tau) + |d0| + m R + m Kg sqrt(tw) + Kg sqrt(dt) + lam.
      Reports max c1-type and c2-type ratios over random realistic inputs incl. near-tie tau.
  (3) The c2 part-3 table: which rows are a sqrt(ulp) effect and which are plain rounding of f.
  (4) tau one ulp above 1e10 with tw = 1e9: is the float dt exact (Sterbenz)? Conditioning vs rounding.
  (5) Other float hazards in the claims' formulas: rho - 1 rounding to 0, Kg = 0 division, sign of abar under
      cancellation, Ks = Kg at m = 0 absorbing a tiny a.
Exact reference: inputs read as exact rationals of the doubles, exact floor, 60-digit sqrt (mpmath).
Run: <gms-local>/.venv/bin/python r4_float64.py   (fixed seeds)
Level: derived.
"""
import math
import random
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 60
EPS = 2.0 ** -52


def M(q):
    q = Fr(q)
    return mp.mpf(q.numerator) / q.denominator


def floor_exact(x, y):
    x, y = Fr(x), Fr(y)
    return (x.numerator * y.denominator) // (x.denominator * y.numerator)


def f_float(tau, tw, a, Kg, Ks, R, d0, lam=0.0):  # same as the implementer's common.f_float
    m = math.floor(tau / tw)
    dt = max(tau - m * tw, 0.0)
    return (a * tau + Kg * math.sqrt(dt) - Ks * math.sqrt(tau)
            + d0 - lam + m * R + m * Kg * math.sqrt(tw))


def f_exact(tau, tw, a, Kg, Ks, R, d0, lam=0.0):
    m = floor_exact(tau, tw)
    dt = Fr(tau) - m * Fr(tw)
    return (M(a) * M(tau) + M(Kg) * mp.sqrt(M(dt)) - M(Ks) * mp.sqrt(M(tau)) + M(d0) - M(lam)
            + m * M(R) + m * M(Kg) * mp.sqrt(M(tw))), m, dt


def ulp(x):
    return math.ulp(x)


def part1():
    rng = random.Random(3)
    N = 200000
    nf = ne = nfe = 0
    band = 0.0
    ex_fe = None
    for _ in range(N):
        sf = 10 ** rng.uniform(-3, 9)
        j = rng.randint(2, 10 ** 6)
        tf = j * sf
        mf = math.floor(tf / sf)
        me = floor_exact(tf, sf)
        nf += mf != j
        ne += me != j
        if mf != me:
            nfe += 1
            band = max(band, abs(float(Fr(tf) - j * Fr(sf))) / ulp(tf))
            if ex_fe is None:
                ex_fe = (sf, j, tf, mf, me)
    print("(1) tau = fl(j*tw), 200000 draws (implementer's seed and call order):")
    print("    float floor != j:", nf, "; exact floor of the doubles != j:", ne,
          "; float floor != exact floor of the doubles:", nfe)
    print("    |tau - j*tw| (exact) in the disagreeing cases: max %.3g ulp(tau)" % band)
    sf, j, tf, mf, me = ex_fe
    R, Kg = 7.0, 2.0
    ff = f_float(tf, sf, 0.0, Kg, 0.0, R, 0.0)
    fe, _, dte = f_exact(tf, sf, 0.0, Kg, 0.0, R, 0.0)
    print("    first disagreement: tw=%r j=%d tau=%r float m=%d exact m=%d exact dt=tw-%.3g;"
          " with R=7, Kg=2: f_float - f_exact = %s (R_g = 7)"
          % (sf, j, tf, mf, me, float(Fr(sf) - dte), mp.nstr(ff - fe, 8)))
    print("    implementer's cited example tw=0.0367344509464381, j=960439: float m =",
          math.floor((960439 * 0.0367344509464381) / 0.0367344509464381), ", exact m =",
          floor_exact(960439 * 0.0367344509464381, 0.0367344509464381),
          "-> it is a float-vs-exact disagreement case, not one of the 'float floor != j' cases")


def part2():
    rng = random.Random(11)
    c1max = c2max = 0.0
    wrong_m = 0
    n = 0
    worst_ratio = 0.0
    for _ in range(40000):
        tw = 10 ** rng.uniform(-1, 9)
        mode = rng.random()
        if mode < 0.4:
            tau = 10 ** rng.uniform(-1, 10)
        else:
            j = rng.randint(1, 10 ** 7)
            tau = j * tw
            k = rng.choice([-3, -2, -1, 0, 1, 2, 3, 50, 10 ** 4])
            for _ in range(abs(k)):
                tau = math.nextafter(tau, math.inf if k > 0 else 0.0)
        a = rng.choice([0.0, rng.uniform(-1e-3, 1e-3)])
        Kg = rng.choice([0.0, 10 ** rng.uniform(-3, 3)])
        Ks = rng.choice([0.0, 10 ** rng.uniform(-3, 3)])
        R = rng.choice([0.0, 10 ** rng.uniform(-3, 6)])
        d0 = rng.uniform(-1e6, 1e6)
        ff = f_float(tau, tw, a, Kg, Ks, R, d0)
        fe, me, dte = f_exact(tau, tw, a, Kg, Ks, R, d0)
        if math.floor(tau / tw) != me:
            wrong_m += 1
            continue
        n += 1
        dtf = float(dte)
        S = (abs(a * tau) + Ks * math.sqrt(tau) + abs(d0) + me * R + me * Kg * math.sqrt(tw) + Kg * math.sqrt(dtf))
        err = abs(float(M(ff) - fe))
        t1 = EPS * S
        t2 = Kg * ulp(tau) / math.sqrt(dtf + ulp(tau)) if Kg > 0 else 0.0
        worst_ratio = max(worst_ratio, err / (4 * t1 + 2 * t2 + 1e-300))
        if t2 < 1e-3 * t1:
            c1max = max(c1max, err / t1)
        elif t1 < 1e-3 * t2:
            c2max = max(c2max, err / t2)
    print("(2) float64 evaluator error when float m equals exact m (%d cases; %d draws had float m != exact m):" % (n, wrong_m))
    print("    rounding-dominated cases: max err/(eps*S) = %.3g ; dt-dominated cases: max err/(Kg ulp(tau)/sqrt(dt+ulp(tau))) = %.3g"
          % (c1max, c2max))
    print("    max err / (4 eps S + 2 Kg ulp(tau)/sqrt(dt+ulp(tau))) over all = %.3g (<= 1 means the model bounds every case)" % worst_ratio)


def part3():
    print("(3) implementer's c2 part-3 rows (Kg = 3, R = 5, a = Ks = d0 = 0):")
    for tw, m in ((1e9, 10 ** 7), (1e3, 10 ** 6), (0.1, 3)):
        t = m * tw
        ff = f_float(t, tw, 0.0, 3.0, 0.0, 5.0, 0.0)
        fe, me, dte = f_exact(t, tw, 0.0, 3.0, 0.0, 5.0, 0.0)
        print("    tw=%g m=%d: float dt = %r, exact dt of the doubles = %.3g, 3 sqrt(exact dt) = %.3g, "
              "|f_float - f_exact| = %.3g, ulp(f)/2 = %.3g"
              % (tw, m, max(t - math.floor(t / tw) * tw, 0.0), float(dte), 3 * math.sqrt(float(dte)),
                 abs(float(M(ff) - fe)), ulp(ff) / 2))


def part4():
    tw = 1e9
    tau = math.nextafter(1e10, math.inf)
    dtf = tau - math.floor(tau / tw) * tw
    dte = Fr(tau) - floor_exact(tau, tw) * Fr(tw)
    print("(4) tau = nextafter(1e10, inf), tw = 1e9: float dt = %r, exact dt = %r, equal: %s;"
          " Kg sqrt(dt) = %.4g Kg is the exact value for this input (no rounding);"
          " df/dtau = Kg/(2 sqrt dt) = %.4g Kg per second, so ONE ulp of tau (%.3g s) moves f by %.3g Kg"
          % (dtf, float(dte), Fr(dtf) == dte, math.sqrt(dtf), 1 / (2 * math.sqrt(dtf)), ulp(1e10), math.sqrt(dtf)))


def part5():
    Kg, Ks = 1.0, 1.0 + 2 ** -52
    rho = (Ks / Kg) ** (2 / 3)
    true_rm1 = mp.power(M(Ks) / M(Kg), mp.mpf(2) / 3) - 1
    print("(5a) Kg = 1, Ks = 1 + 2^-52: float rho - 1 = %.4g, exact rho - 1 = %s (relative error %.2g); x* = t_m/(rho-1)"
          " is then > 1e15 t_m, far outside (0, tw) for m >= 1, so harmless" % (rho - 1, mp.nstr(true_rm1, 6),
                                                                              float((M(rho - 1) - true_rm1) / true_rm1)))
    try:
        xs = 1.0 / ((1.0 / 1.0) ** (2 / 3) - 1)
        msg = "x* = %r" % xs
    except ZeroDivisionError:
        msg = "ZeroDivisionError"
    print("     Ks == Kg exactly: t_m/(rho-1) -> %s; test 'm >= 1 and Ks^2 > Kg^2 (m+1)^3' instead of forming x*" % msg)
    try:
        _ = (1.0 / 0.0)
        print("(5b) Kg = 0: Ks/Kg -> inf")
    except ZeroDivisionError:
        print("(5b) Kg = 0: Python float Ks/Kg raises ZeroDivisionError (numpy gives inf) -> branch on Kg = 0")
    rng = random.Random(5)
    signs = {1: 0, -1: 0, 0: 0}
    Tmin = math.inf
    for _ in range(10000):
        tw = 10 ** rng.uniform(3, 9)
        R = 10 ** rng.uniform(-3, 6)
        Kg = 10 ** rng.uniform(-3, 3)
        Ks = 10 ** rng.uniform(-3, 3)
        a = -R / tw - Kg / math.sqrt(tw)        # intended abar = 0, written in an algebraically equal form
        ab = a + (R + Kg * math.sqrt(tw)) / tw  # float abar as the claim writes it
        s = (ab > 0) - (ab < 0)
        signs[s] += 1
        if s > 0:
            Tmin = min(Tmin, (Ks / ab) ** 2)    # loss time scale implied by a spurious positive abar (Ks term)
    print("(5c) intended abar = 0, a written as -R/tw - Kg/sqrt(tw), abar evaluated in float (10000 draws): sign(+,-,0) =",
          signs[1], signs[-1], signs[0], "; smallest (Ks/abar)^2 for spurious abar > 0 = %.3g s (horizon ~1e10 s)" % Tmin)
    a = 7e-146
    xs = [k / 1000 for k in range(1, 1000)]
    zeros = sum(1 for x in xs if (a * (0 + x) + 1.0 * math.sqrt(x) - 1.0 * math.sqrt(0 + x) + 0.0) == 0.0)
    print("(5d) m = 0, Ks = Kg = 1, a = 7e-146, d' = 0: float f == 0 at %d of 999 points (exact f = a dt > 0: a loss, float says tie)" % zeros)


def main():
    part1()
    part2()
    part3()
    part4()
    part5()


if __name__ == "__main__":
    main()
