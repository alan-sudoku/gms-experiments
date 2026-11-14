"""X2: C3 long-run verdict time T, SciPy brentq vs closed form, plus sign of f beyond T (mpmath 50 digits).

Claim (C3): abar = a + (Rg + Kg sqrt(tw))/tw.  Writing tau = m tw + dt:
  f = abar*tau - Ks sqrt(tau) + d0 + Kg (sqrt(dt) - dt/sqrt(tw)) - Rg dt/tw.
  Bounds (Result table of the synthesis, restated by me):
     L(tau) = abar tau - Ks sqrt(tau) + d0 - Rg   <  f  <=  U(tau) = abar tau - Ks sqrt(tau) + d0 + Kg sqrt(tw)/4.
  abar>0: f>0 once L>=0 (geometry loses); abar<0: f<0 once U<0 (wins); abar=0,Ks>0: f<0 once U<0;
  abar=0,Ks=0: f periodic in tau with period tw.
The Result table gives no closed form for T, so the closed form compared here is MY derivation (UNSURE whether it
matches the earlier one): with u=sqrt(tau),
  abar>0: T = u+^2, u+ = (Ks + sqrt(Ks^2 - 4 abar c))/(2 abar), c = d0-Rg  (T=0 if discriminant < 0)
  abar<0: T = ((-Ks + sqrt(Ks^2 + 4|abar| c2))/(2|abar|))^2 if c2>0 else 0, c2 = d0 + Kg sqrt(tw)/4
  abar=0,Ks>0: T = (c2/Ks)^2 if c2>0 else 0.
Method: brentq on the float bound function (bracket from its extremum, doubling), compare with closed form
(rel tol 1e-6; flagged: both use the same bound, so this part checks algebra only); then f evaluated at 50 digits at
tau = T*(1+1e-9, 1.0001, 1.5, 2, 10, 1e3) and at exact ties j*tw and tw-limits just below ties, beyond T.  The bounds
L < f <= U are also tested at random tau (this is the non-trivial check).  abar=0 uses a = -(Rg+Kg sqrt tw)/tw in
mp arithmetic, so abar is exactly 0 at 50 digits.
Run: <gms-local>/.venv/bin/python x2_long_run_T.py
"""
import sys, os, math, random
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
from scipy.optimize import brentq
from xc_common import f_full_mp

mp.mp.dps = 50


def closed_T(abar, Ks, c, c2, naive=False):
    if abar > 0:
        disc = Ks * Ks - 4 * abar * c
        if disc < 0:
            return 0.0
        up = (Ks + math.sqrt(disc)) / (2 * abar)
        return up * up
    if abar < 0:
        if c2 <= 0:
            return 0.0
        ab = -abar
        if naive:
            up = (-Ks + math.sqrt(Ks * Ks + 4 * ab * c2)) / (2 * ab)   # cancels when 4|abar|c2 << Ks^2
        else:
            up = 2 * c2 / (Ks + math.sqrt(Ks * Ks + 4 * ab * c2))      # algebraically identical, no cancellation
        return up * up
    if Ks > 0:
        return (c2 / Ks) ** 2 if c2 > 0 else 0.0
    return None


def brent_T(abar, Ks, c, c2):
    """T from brentq on the bound function (L for abar>0 : sign 'L>=0'; U for abar<=0: 'U<0')."""
    if abar > 0:
        g = lambda t: abar * t - Ks * math.sqrt(t) + c      # want g>=0 beyond T
        tmin = (Ks / (2 * abar)) ** 2
        if g(tmin) >= 0:
            return 0.0
        hi = max(2 * tmin, 1.0)
        while g(hi) < 0:
            hi *= 2
        return brentq(g, tmin, hi, xtol=1e-300, rtol=1e-14, maxiter=1000)
    g = lambda t: -(abar * t - Ks * math.sqrt(t) + c2)      # want g>0 beyond T  (g = -U)
    if abar < 0:
        # -U = |abar| t + Ks sqrt t - c2 is increasing
        if c2 <= 0:
            return 0.0
        hi = 1.0
        while g(hi) < 0:
            hi *= 2
        return brentq(g, 0.0, hi, xtol=1e-300, rtol=1e-14, maxiter=1000)
    if Ks > 0:
        if c2 <= 0:
            return 0.0
        hi = 1.0
        while g(hi) < 0:
            hi *= 2
        return brentq(g, 0.0, hi, xtol=1e-300, rtol=1e-14, maxiter=1000)
    return None


def main():
    rng = random.Random(7)
    M = mp.mpf
    stats = dict(n=0, T_ok=0, T_bad=0, sign_pts=0, sign_viol=0, bound_pts=0, bound_viol=0, per_ok=0, per_bad=0)
    bad = []
    kinds = ['pos'] * 1000 + ['neg'] * 1000 + ['zero_Ks'] * 500 + ['zero_noKs'] * 500
    never_win = never_lose = 0
    per_signs = {'both': 0, 'win_only': 0, 'lose_only': 0, 'zero': 0}
    for kind in kinds:
        tw = 10 ** rng.uniform(-2, 6)
        Kg = rng.choice([0.0, 10 ** rng.uniform(-5, 1)])
        Rg = rng.choice([0.0, 10 ** rng.uniform(-5, 2)])
        Ks = 0.0 if kind == 'zero_noKs' else 10 ** rng.uniform(-5, 1)
        d0 = rng.choice([-1, 1]) * 10 ** rng.uniform(-3, 5)
        abar0 = (Rg + Kg * math.sqrt(tw)) / tw
        if kind in ('zero_Ks', 'zero_noKs'):
            a = -(M(Rg) + M(Kg) * mp.sqrt(M(tw))) / M(tw)   # mp number: abar exactly 0
        else:
            delta = 10 ** rng.uniform(-6, 0) * max(abar0, 1e-3)
            a = M(-abar0) + M(delta) * (1 if kind == 'pos' else -1)
            a = M(float(a))  # a is a float input
        abar = a + (M(Rg) + M(Kg) * mp.sqrt(M(tw))) / M(tw)
        c = d0 - Rg
        c2 = d0 + Kg * math.sqrt(tw) / 4
        abar_f = float(abar)
        stats['n'] += 1
        if kind == 'zero_noKs':
            # periodicity: f(tau + tw) == f(tau) at 50 digits, plus sign mix over one period
            ok = True
            signs = set()
            for _ in range(40):
                tau = M(rng.random()) * M(tw) * rng.randint(1, 50)
                f1 = f_full_mp(tau, a, Kg, Ks, Rg, d0, tw)
                f2 = f_full_mp(tau + 7 * M(tw), a, Kg, Ks, Rg, d0, tw)
                if abs(f1 - f2) > M(10) ** -30 * (abs(f1) + abs(d0) + 1):
                    ok = False
                signs.add(1 if f1 > 0 else (-1 if f1 < 0 else 0))
            stats['per_ok' if ok else 'per_bad'] += 1
            if not ok:
                bad.append(('periodicity', (tw, Kg, Rg, d0)))
            # sign over one period at fine grid
            fs = [f_full_mp(M(tw) * M(i) / 200 + 5 * M(tw), a, Kg, Ks, Rg, d0, tw) for i in range(200)]
            neg = any(v < 0 for v in fs); pos = any(v > 0 for v in fs)
            per_signs['both' if neg and pos else 'win_only' if neg else 'lose_only' if pos else 'zero'] += 1
            continue
        Tc = closed_T(abar_f if kind in ('pos', 'neg') else 0.0, Ks, c, c2)
        Tn = closed_T(abar_f if kind in ('pos', 'neg') else 0.0, Ks, c, c2, naive=True)
        if Tc is not None and abs(Tn - Tc) > 1e-6 * max(Tc, Tn) + 1e-12:
            stats['naive_bad'] = stats.get('naive_bad', 0) + 1
        Tb = brent_T(abar_f if kind in ('pos', 'neg') else 0.0, Ks, c, c2)
        if Tc is None or abs(Tc - Tb) > 1e-6 * max(Tc, Tb) + 1e-12:
            stats['T_bad'] += 1
            bad.append(('T', kind, Tc, Tb, (tw, Kg, Ks, Rg, d0, float(a))))
            continue
        stats['T_ok'] += 1
        # f sign beyond T
        taus = []
        T = max(Tc, 1e-9)
        for fac in (1 + 1e-9, 1.0001, 1.5, 2, 10, 1e3):
            taus.append((M(T) * M(fac), None))
        j0 = int(math.ceil(T / tw)) + 1
        for k in range(0, 4):
            j = j0 + k
            taus.append((M(j) * M(tw), j))                       # exact tie, segment j
            taus.append((M(j) * M(tw) * (1 - M(10) ** -30), j - 1))  # just below tie, segment j-1
        want = 1 if kind == 'pos' else -1
        for tau, mseg in taus:
            if tau < M(Tc) * (1 + M(10) ** -12):
                continue
            fv = f_full_mp(tau, a, Kg, Ks, Rg, d0, tw, m=mseg)
            stats['sign_pts'] += 1
            if (fv > 0) != (want > 0) or fv == 0:
                stats['sign_viol'] += 1
                bad.append(('sign', kind, float(tau), float(fv), (tw, Kg, Ks, Rg, d0, float(a))))
        # bounds L < f <= U at random tau (including small tau)
        for _ in range(20):
            tau = M(10) ** M(rng.uniform(-3, math.log10(tw) + 4)) * M(rng.random() + 0.01)
            fv = f_full_mp(tau, a, Kg, Ks, Rg, d0, tw)
            L = abar * tau - M(Ks) * mp.sqrt(tau) + c - 0  # c = d0-Rg
            U = abar * tau - M(Ks) * mp.sqrt(tau) + M(d0) + M(Kg) * mp.sqrt(M(tw)) / 4
            stats['bound_pts'] += 1
            if not (L < fv <= U + M(10) ** -35 * (abs(U) + 1)) and not (Rg == 0 and Kg == 0 and fv == L):
                if not (L <= fv):
                    stats['bound_viol'] += 1
                    bad.append(('bound', float(tau), float(L), float(fv), float(U)))
                elif not fv <= U + M(10) ** -35 * (abs(U) + 1):
                    stats['bound_viol'] += 1
                    bad.append(('bound', float(tau), float(L), float(fv), float(U)))
    print("X2 C3 T (brentq vs closed form) and sign beyond T; 3000 cases")
    print("kinds: abar>0 1000, abar<0 1000, abar=0 with Ks>0 500, abar=0 with Ks=0 500")
    print("T agreement brentq vs closed form (rel 1e-6): ok", stats['T_ok'], " bad", stats['T_bad'], "(of", stats['n'] - 1000 // 2, "non-periodic)")
    print("float cancellation: the textbook form (-Ks+sqrt(Ks^2+4|abar|c2))/(2|abar|) differs from the stable form 2 c2/(Ks+sqrt(..)) by >1e-6 rel in", stats.get('naive_bad', 0), "cases (the stable form is used above; the naive form loses digits when 4|abar|c2 << Ks^2)")
    print("sign of f beyond T checked at", stats['sign_pts'], "points (50-digit): violations", stats['sign_viol'])
    print("bounds L < f <= U checked at", stats['bound_pts'], "points: violations", stats['bound_viol'])
    print("abar=0, Ks=0: f periodic (tau vs tau+7 tw) in", stats['per_ok'], "of", stats['per_ok'] + stats['per_bad'], "cases;",
          "sign mix over one period:", per_signs, "(so neither 'always wins' nor 'always loses' in general)")
    print("violations / disagreements listed:", len(bad))
    for b in bad[:15]:
        print("  ", b)
    print("FLAG: the brentq-vs-closed-form comparison uses the same bound function on both sides (true up to algebra);")
    print("      the substantive checks are the sign check beyond T and the bounds L<f<=U at 50 digits.")


if __name__ == "__main__":
    main()
