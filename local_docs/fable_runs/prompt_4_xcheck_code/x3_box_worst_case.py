"""X3: C4/C5 corner claim with a global optimiser (scipy.optimize.differential_evolution, fixed seed).

Claim (C5, with C4 for tw): for a box of coefficient intervals and a fixed tau, for every point in the box
   f(optimistic corner) <= f(point) <= f(pessimistic corner),
pessimistic = a, Kg, d0, Rg at their upper bound and Ks, tw, lambda_E at their lower bound (as stated in the
synthesis Result table; derived there, here only tested).  f(tau) uses m = floor(tau/tw), dt = tau - m tw,
d' = d0 - lambda + m Rg + m Kg sqrt(tw).
Method: random boxes (300; every interval non-degenerate, relative width 1%-300%), fixed tau including tau < tw_lo,
tau near j*tw for tw in the box (tau = fl(j*tw_pt) and its neighbours), and tau = j*tw_lo, j*tw_hi exactly.
For each box maximise and minimise f over the box with differential_evolution (seed fixed; f is discontinuous in tw,
so a gradient-free global method).  Violation test is EXACT: m via fractions.Fraction, dt and d' in 50-digit mpmath.
A float-only excess (DE point beats the float corner value by > 1e-9 relative scale) is counted separately and is
re-evaluated exactly before being called a violation.  Reported 'tightness' = how close DE gets to the corner value
(1 = reaches it), to show the search is not vacuous.
Run: <gms-local>/.venv/bin/python x3_box_worst_case.py
"""
import sys, os, math, random
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
import numpy as np
import mpmath as mp
from scipy.optimize import differential_evolution
from xc_common import f_full

mp.mp.dps = 50
NAMES = ['a', 'Kg', 'Ks', 'd0', 'Rg', 'tw', 'lam']


def f_exact(tau, p):
    """Exact-m, 50-digit evaluation. p = dict of floats."""
    m = int(Fraction(tau) / Fraction(p['tw']))   # floor for positive
    M = mp.mpf
    dt = M(tau) - M(m) * M(p['tw'])
    tm = M(m) * M(p['tw'])
    dp = M(p['d0']) - M(p['lam']) + M(m) * M(p['Rg']) + M(m) * M(p['Kg']) * mp.sqrt(M(p['tw']))
    return M(p['a']) * (tm + dt) + M(p['Kg']) * mp.sqrt(dt) - M(p['Ks']) * mp.sqrt(tm + dt) + dp


def fp(tau, x):
    a, Kg, Ks, d0, Rg, tw, lam = x
    return f_full(tau, a, Kg, Ks, Rg, d0, tw, lam)


def make_box(rng):
    lo, hi = {}, {}

    def interval(centre, lo_clip=None):
        w = 10 ** rng.uniform(-2, math.log10(3.0))
        l = centre * (1 - w / 2) if w < 1.8 else centre * 0.1
        h = centre * (1 + w / 2)
        return l, h
    a_c = rng.choice([-1, 1]) * 10 ** rng.uniform(-6, -2)
    w = 10 ** rng.uniform(-2, 0.5)
    lo['a'], hi['a'] = a_c - abs(a_c) * w, a_c + abs(a_c) * w
    for k, (e0, e1) in {'Kg': (-4, 0), 'Ks': (-4, 0.5), 'Rg': (-3, 2)}.items():
        c = 10 ** rng.uniform(e0, e1)
        lo[k], hi[k] = interval(c)
    c = rng.choice([-1, 1]) * 10 ** rng.uniform(-2, 3)
    w = 10 ** rng.uniform(-2, 0.5)
    lo['d0'], hi['d0'] = c - abs(c) * w, c + abs(c) * w
    c = 10 ** rng.uniform(0, 4)
    lo['tw'], hi['tw'] = interval(c)
    c = 10 ** rng.uniform(-2, 2)
    lo['lam'], hi['lam'] = interval(c)
    return lo, hi


def pick_tau(rng, lo, hi, mode):
    if mode == 'below':
        return lo['tw'] * rng.uniform(0.05, 0.99)
    if mode == 'tie_lo':
        return rng.randint(1, 30) * lo['tw']
    if mode == 'tie_hi':
        return rng.randint(1, 30) * hi['tw']
    if mode == 'tie_mid':
        j = rng.randint(1, 30)
        t = j * (lo['tw'] + rng.random() * (hi['tw'] - lo['tw']))
        return t + rng.choice([-1, 0, 1]) * math.ulp(t)
    return rng.uniform(1, 30) * lo['tw']


def main():
    rng = random.Random(424242)
    modes = ['below', 'tie_lo', 'tie_hi', 'tie_mid', 'generic']
    n_boxes = 300
    stats = dict(boxes=0, float_excess=0, exact_viol=0)
    tight_max, tight_min = [], []
    viols = []
    per_mode = {m: 0 for m in modes}
    straddle = 0
    seed_counter = 1000
    for i in range(n_boxes):
        mode = modes[i % len(modes)]
        lo, hi = make_box(rng)
        tau = pick_tau(rng, lo, hi, mode)
        assert all(hi[k] > lo[k] for k in NAMES)
        per_mode[mode] += 1
        if math.floor(tau / hi['tw']) != math.floor(tau / lo['tw']):
            straddle += 1
        bounds = [(lo[k], hi[k]) for k in NAMES]
        pess = [hi['a'], hi['Kg'], lo['Ks'], hi['d0'], hi['Rg'], lo['tw'], lo['lam']]
        opt = [lo['a'], lo['Kg'], hi['Ks'], lo['d0'], lo['Rg'], hi['tw'], hi['lam']]
        fpe_f, fop_f = fp(tau, pess), fp(tau, opt)
        scale = abs(fpe_f) + abs(fop_f) + 1e-300
        seed_counter += 1
        rmax = differential_evolution(lambda x: -fp(tau, x), bounds, seed=seed_counter, maxiter=120, popsize=12,
                                      tol=0, polish=False, init='sobol')
        rmin = differential_evolution(lambda x: fp(tau, x), bounds, seed=seed_counter + 7, maxiter=120, popsize=12,
                                      tol=0, polish=False, init='sobol')
        fmax, fmin = -rmax.fun, rmin.fun
        stats['boxes'] += 1
        tight_max.append((fmax - fop_f) / (fpe_f - fop_f) if fpe_f != fop_f else 1.0)
        tight_min.append((fpe_f - fmin) / (fpe_f - fop_f) if fpe_f != fop_f else 1.0)
        tol = 1e-9 * scale
        flag = (fmax > fpe_f + tol) or (fmin < fop_f - tol)
        if flag:
            stats['float_excess'] += 1
        # exact check always (cheap)
        P = lambda x: dict(zip(NAMES, x))
        ex_pess, ex_opt = f_exact(tau, P(pess)), f_exact(tau, P(opt))
        ex_max, ex_min = f_exact(tau, P(rmax.x)), f_exact(tau, P(rmin.x))
        if ex_max > ex_pess or ex_min < ex_opt:
            stats['exact_viol'] += 1
            viols.append((mode, tau, lo, hi, list(rmax.x), list(rmin.x), float(ex_max - ex_pess), float(ex_min - ex_opt)))
    tm_, tn_ = np.array(tight_max), np.array(tight_min)
    print("X3 C4/C5 corner bounds via differential_evolution; boxes:", stats['boxes'], "modes:", per_mode)
    print("boxes where tw interval straddles a segment change at fixed tau:", straddle)
    print("float-only excess beyond 1e-9 relative scale:", stats['float_excess'])
    print("EXACT violations (Fraction m, mp-50 f): max>pessimistic or min<optimistic:", stats['exact_viol'])
    print("tightness of DE max vs pessimistic corner (fraction of the corner-to-corner range reached by DE max):",
          "median %.4f, min %.4f, boxes >= 0.9: %d/%d" % (np.median(tm_), tm_.min(), int((tm_ >= 0.9).sum()), len(tm_)))
    print("tightness of DE min vs optimistic corner (range fraction):",
          "median %.4f, min %.4f, boxes >= 0.9: %d/%d" % (np.median(tn_), tn_.min(), int((tn_ >= 0.9).sum()), len(tn_)))
    for v in viols[:10]:
        print("VIOLATION", v)
    print("NOTE: DE reaching close to the corner value (tightness near 1) shows the corners are attained and nothing beats them;")
    print("      it is evidence, not proof (DE is a heuristic).  Tightness is capped at <=1 up to the exact check above.")


if __name__ == "__main__":
    main()
