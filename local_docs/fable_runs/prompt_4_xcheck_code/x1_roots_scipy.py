"""X1: C1 roots per segment, two independent SciPy/numpy routes.

Claim (C1): f'' has at most one zero on (0, tw); f has at most 3 roots per segment; 3 roots only when
K_g>0 and 1 <= m < rho-1 (K_s^2 > K_g^2 (m+1)^3).
Route A: zeros of f'' (sign-change search on phi = Ks x^1.5 - Kg (tm+x)^1.5 then brentq on f''),
  critical points of f via brentq on f' on each f'-monotone piece, roots of f via brentq on each monotone piece.
Route B: square out the radical, quartic in s = sqrt(dt):  (a s^2 + Kg s + a tm + d')^2 = Ks^2 (s^2 + tm),
  numpy.polynomial.polynomial.polyroots, keep real s in [0, sqrt(tw)) that satisfy the unsquared equation.
Disagreements are adjudicated with mpmath (50 digits, mp.polyroots on the quartic + unsquared residual filter).
Cases: (i) 3-root reference (tw=1,m=1), (ii) window cases + generic, (iii) m=0 and Ks<=Kg.
Run: <gms-local>/.venv/bin/python x1_roots_scipy.py
"""
import sys, os, math, random
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from numpy.polynomial import polynomial as P
from scipy.optimize import brentq
import mpmath as mp
from xc_common import f_seg, fp_seg

EPS = 2.0 ** -52


def _brent(fun, lo, hi):
    return brentq(fun, lo, hi, xtol=1e-300, rtol=4 * EPS, maxiter=500)


def fpp(x, tm, Kg, Ks):
    return -Kg / (4 * x ** 1.5) + Ks / (4 * (tm + x) ** 1.5)


def route_a(tm, tw, a, Kg, Ks, dp):
    """Return sorted roots (dt in [0,tw)) by critical-point decomposition. tw is the segment length."""
    f = lambda x: f_seg(x, tm, a, Kg, Ks, dp)
    fp = lambda x: fp_seg(x, tm, a, Kg, Ks)
    if (Kg == 0 and Ks == 0 and a == 0) or (tm == 0 and Kg == Ks and a == 0):
        return None if dp == 0 else []
    tiny = tw * 1e-18
    # zeros of f'' via sign changes of phi on log grid (independent of the closed form)
    xs = [0.0] + list(np.geomspace(tw * 1e-14, tw, 400))
    def phi(x):
        return Ks * x ** 1.5 - Kg * (tm + x) ** 1.5
    zs = []
    for u, v in zip(xs[:-1], xs[1:]):
        pu, pv = phi(u), phi(v)
        if pu == 0 and u > 0:
            zs.append(u)
        elif pu * pv < 0:
            zs.append(_brent(lambda x: fpp(x, tm, Kg, Ks) if x > 0 else -1e300, max(u, tiny * 1e-6), v) if u > 0 else
                      _brent(phi, max(u, tiny * 1e-6), v))
    zs = sorted(set(zs))
    if len(zs) > 1 and Kg == Ks and tm == 0:
        zs = []  # f'' identically 0
    # f' monotone pieces: breakpoints 0, zs, tw
    pts = [0.0] + zs + [tw]
    crit = []
    for u, v in zip(pts[:-1], pts[1:]):
        uu = max(u, tw * 1e-300) if u == 0 else u
        # f' at u: +inf if Kg>0 and u==0
        if u > 0:
            fu = fp(uu)
        elif tm > 0:
            fu = math.inf if Kg > 0 else a - Ks / (2 * math.sqrt(tm))
        else:  # m = 0: f'(0+) = a + (Kg-Ks)/(2 sqrt(x)) -> sign(Kg-Ks) * inf, or a if Kg == Ks
            fu = a if Kg == Ks else math.copysign(math.inf, Kg - Ks)
        fv = fp(v)
        if fu == 0.0 and u > 0:
            crit.append(u)
        if math.isinf(fu):
            fu_s = 1.0 if fu > 0 else -1.0
        else:
            fu_s = fu
        if fu_s * fv < 0:
            if u == 0:
                # shrink left end until sign is the sign of fu
                l = tw * 1e-300
                if math.isinf(fu) and fp(l) * fv > 0:
                    continue
                l2 = l
                while fp(l2) * fv > 0 and l2 < v:
                    l2 *= 1e3
                if l2 >= v:
                    continue
                crit.append(_brent(fp, l2, v))
            else:
                crit.append(_brent(fp, u, v))
    crit = sorted(set(crit))
    bps = [0.0] + [c for c in crit if 0 < c < tw] + [tw]
    roots = []
    for u, v in zip(bps[:-1], bps[1:]):
        fu, fv = f(u), f(v)
        if fu == 0.0 and u == 0.0:
            roots.append(0.0)
        if fu * fv < 0:
            roots.append(_brent(f, u, v))
        elif fv == 0.0 and v < tw:
            roots.append(v)
    return sorted(set(roots))


def route_b(tm, tw, a, Kg, Ks, dp):
    """Quartic in s=sqrt(dt)."""
    if (Kg == 0 and Ks == 0 and a == 0) or (tm == 0 and Kg == Ks and a == 0):
        return None if dp == 0 else []
    c0 = a * tm + dp
    Pc = np.array([c0, Kg, a])  # P(s) = c0 + Kg s + a s^2 (ascending)
    if Ks == 0:
        q = Pc
        r = P.polyroots(q) if np.any(q[1:] != 0) else np.array([])
        cand = [z for z in r]
    else:
        q = P.polysub(P.polymul(Pc, Pc), Ks ** 2 * np.array([tm, 0, 1.0]))
        # trim leading zeros
        while len(q) > 1 and q[-1] == 0:
            q = q[:-1]
        cand = list(P.polyroots(q)) if len(q) > 1 else []
    out = []
    scale = max(abs(c0), abs(Kg), abs(a), 1e-300)
    for z in cand:
        if abs(z.imag) > 1e-7 * max(abs(z), 1e-300) + 1e-14 * math.sqrt(tw):
            continue
        s = z.real
        dq = P.polyder(q) if len(q) > 1 else q
        for _ in range(8):  # Newton polish on the polynomial itself (keeps the candidate's identity)
            dv = P.polyval(s, dq)
            if dv == 0:
                break
            step = P.polyval(s, q) / dv
            if not math.isfinite(step) or abs(step) > 1e-3 * max(abs(s), 1e-12):
                break
            s -= step
        if s < 0 or s * s >= tw:
            continue
        x = s * s
        res = f_seg(x, tm, a, Kg, Ks, dp)
        Pv = a * s * s + Kg * s + c0
        mag = abs(Pv) + abs(Ks * math.sqrt(tm + x))  # size of the two sides of  P(s) = Ks r
        if (Ks == 0 or Pv >= 0) and abs(res) <= 1e-6 * (mag if Ks > 0 else abs(a * s * s) + abs(Kg * s) + abs(c0) + 1e-300):
            out.append(x)
    # merge near-duplicates (double roots)
    out.sort()
    merged = []
    for x in out:
        if merged and abs(x - merged[-1]) <= 1e-9 * max(x, 1e-300):
            continue
        merged.append(x)
    return merged


def truth_mp(tm, tw, a, Kg, Ks, dp):
    """50-digit count of distinct real roots in [0,tw) of the unsquared f."""
    M = mp.mpf
    tm, tw, a, Kg, Ks, dp = map(M, (tm, tw, a, Kg, Ks, dp))
    if (Kg == 0 and Ks == 0 and a == 0) or (tm == 0 and Kg == Ks and a == 0):
        return None if dp == 0 else 0
    c0 = a * tm + dp
    if Ks == 0:
        coeffs = [a, Kg, c0]
    else:
        # (a s^2 + Kg s + c0)^2 - Ks^2 s^2 - Ks^2 tm
        coeffs = [a * a, 2 * a * Kg, Kg * Kg + 2 * a * c0 - Ks * Ks, 2 * Kg * c0, c0 * c0 - Ks * Ks * tm]
    while coeffs and coeffs[0] == 0:
        coeffs = coeffs[1:]
    if len(coeffs) < 2:
        return 0
    rts = mp.polyroots(coeffs, maxsteps=2000, extraprec=400)
    found = []
    for z in rts:
        if abs(mp.im(z)) > M(10) ** -25 * max(abs(z), 1):
            continue
        s = mp.re(z)
        if s < 0 or s * s >= tw:
            continue
        x = s * s
        res = a * (tm + x) + Kg * s - Ks * mp.sqrt(tm + x) + dp
        if abs(res) < M(10) ** -20 * (abs(a * (tm + x)) + abs(Kg * s) + abs(Ks * mp.sqrt(tm + x)) + abs(dp) + 1e-300):
            if all(abs(x - y) > M(10) ** -20 * max(x, 1e-300) for y in found):
                found.append(x)
    return len(found)


def window_case(rng, m, tw=1.0):
    """3-root-window case with both critical points inside (0,tw). Returns params or None."""
    tm = m * tw
    for _ in range(200):
        rho = (m + 1) * math.exp(rng.uniform(1e-3, 3.0))
        Kg = math.exp(rng.uniform(-6, 2))
        Ks = Kg * rho ** 1.5
        xstar = tm / (rho - 1)
        h = lambda x: Kg / (2 * math.sqrt(x)) - Ks / (2 * math.sqrt(tm + x))
        lo_a, hi_a = -h(tw), -h(xstar)
        if not lo_a < hi_a:
            continue
        a = rng.uniform(lo_a, hi_a)
        fp = lambda x: fp_seg(x, tm, a, Kg, Ks)
        try:
            xmax = _brent(fp, tw * 1e-300 * 1e290 if False else 1e-14 * xstar, xstar)
            xmin = _brent(fp, xstar, tw)
        except Exception:
            continue
        F = lambda x: f_seg(x, tm, a, Kg, Ks, 0.0)
        lo_d = max(-F(xmax), -F(tw))
        hi_d = min(-F(0.0), -F(xmin))
        if not lo_d < hi_d:
            continue
        dp = rng.uniform(lo_d, hi_d)
        return (tm, tw, a, Kg, Ks, dp)
    return None


def run_case(case, tag, stats, disagreements, limit3=True):
    tm, tw, a, Kg, Ks, dp = case
    A = route_a(tm, tw, a, Kg, Ks, dp)
    B = route_b(tm, tw, a, Kg, Ks, dp)
    stats['n'] += 1
    stats.setdefault('tag', {}).setdefault(tag, 0)
    stats['tag'][tag] += 1
    if A is None or B is None:
        stats['identically0'] += 1
        return
    ca, cb = len(A), len(B)
    stats['hist_A'][ca] = stats['hist_A'].get(ca, 0) + 1
    stats['hist_B'][cb] = stats['hist_B'].get(cb, 0) + 1
    stats.setdefault('three', {}).setdefault(tag, [0, 0])
    stats['three'][tag][0] += (ca == 3)
    stats['three'][tag][1] += (cb == 3)
    stats['maxA'] = max(stats['maxA'], ca)
    stats['maxB'] = max(stats['maxB'], cb)
    if ca == cb:
        stats['agree'] += 1
        if ca >= 1 and max(abs(x - y) / max(abs(y), 1e-300) for x, y in zip(A, B)) > 1e-6:
            stats['root_val_mismatch'] += 1
    else:
        t = truth_mp(tm, tw, a, Kg, Ks, dp)
        who = 'A' if t == ca else ('B' if t == cb else 'neither')
        disagreements.append((tag, case, ca, cb, t, who))


def main():
    print("X1 roots per segment (SciPy brentq route A vs numpy polyroots route B)")
    rng = random.Random(20261114)
    # (i) reference
    tw = 1.0; m = 1
    a, Kg, Ks, dp = 0.27462901204136775, 0.06913552752653546, 0.8205556354592521, 0.5436108308140535
    ref = [0.0012990843334213434082, 0.45843123476155969005, 0.904736521823163779]
    A = route_a(m * tw, tw, a, Kg, Ks, dp); B = route_b(m * tw, tw, a, Kg, Ks, dp)
    print("(i) reference tw=1 m=1: A roots", A, "B roots", B)
    for name, R in (("A", A), ("B", B)):
        ok = len(R) == 3 and all(abs(x - y) / y <= 1e-10 for x, y in zip(R, ref))
        print(f"    route {name}: count={len(R)}, max rel diff vs reference =",
              max(abs(x - y) / y for x, y in zip(R, ref)) if len(R) == 3 else None, "-> agree" if ok else "-> DISAGREE")
    print("    mp-50 truth count:", truth_mp(m * tw, tw, a, Kg, Ks, dp))

    stats = dict(n=0, identically0=0, hist_A={}, hist_B={}, maxA=0, maxB=0, agree=0, root_val_mismatch=0)
    dis = []
    # (ii) window cases
    ms = [1, 2, 3, 5, 10, 30, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6]
    nwin = 0
    tries = 0
    while nwin < 1100 and tries < 100000:
        tries += 1
        m = ms[nwin % len(ms)]
        tw = 1.0 if nwin % 3 else 10 ** rng.uniform(-3, 9)
        c = window_case(rng, m, 1.0)
        if c is None:
            continue
        tm, _, a, Kg, Ks, dp = c
        # rescale to tw: dt -> tw*dt, f scales: f(tw*x) with a'=a/ ... use tw=1 here; random tw handled via generic cases below
        run_case(c, f'window_m{m}', stats, dis)
        nwin += 1
    win_agree3 = sum(1 for _ in [0])  # placeholder
    print(f"(ii) window cases generated: {nwin} (tries {tries})")
    # generic cases, random tw, m from 0 to 1e6
    for i in range(1500):
        m = rng.choice([0, 1, 2, 3, 7, 50, 1000, 10 ** 6, rng.randint(0, 100)])
        tw = 10 ** rng.uniform(-3, 9)
        Kg = rng.choice([0.0, 10 ** rng.uniform(-6, 1)])
        Ks = rng.choice([0.0, Kg, 10 ** rng.uniform(-6, 2), Kg * 10 ** rng.uniform(0, 3)])
        a = rng.choice([0.0, rng.uniform(-1, 1) * 10 ** rng.uniform(-6, 1)])
        tm = m * tw
        # d' so that f has a sign change somewhere: pick level to cross value at random x
        x0 = tw * rng.random()
        dp = -(f_seg(x0, tm, a, Kg, Ks, 0.0)) + rng.uniform(-1, 1) * 1e-3 * (abs(Ks) * math.sqrt(tm + tw) + 1e-9)
        run_case((tm, tw, a, Kg, Ks, dp), 'generic', stats, dis)
    # (iii) m=0 and Ks<=Kg
    s2 = dict(n=0, identically0=0, hist_A={}, hist_B={}, maxA=0, maxB=0, agree=0, root_val_mismatch=0)
    dis2 = []
    for i in range(600):
        m = 0 if i % 2 == 0 else rng.randint(1, 50)
        tw = 10 ** rng.uniform(-3, 6)
        Kg = 10 ** rng.uniform(-4, 1)
        Ks = Kg * rng.choice([1.0, rng.random(), 0.0, rng.random() ** 3]) if m > 0 or i % 4 else Kg * rng.choice([1.0, 0.5, 0.0])
        if m == 0 and i % 4 == 0:
            Ks = Kg * rng.choice([1.0, 0.5, 0.0, 2.0])
        a = rng.choice([0.0, rng.uniform(-1, 1) * 10 ** rng.uniform(-5, 0)])
        tm = m * tw
        x0 = tw * rng.random()
        dp = -(f_seg(x0, tm, a, Kg, Ks, 0.0)) + rng.uniform(-1, 1) * 1e-3 * (abs(Ks) * math.sqrt(tm + tw) + 1e-9)
        run_case((tm, tw, a, Kg, Ks, dp), 'm0_or_Ks_le_Kg', s2, dis2)
    # special: m=0,Ks=Kg,a=0,dp=0 identically zero ; m=0 Ks=Kg a!=0
    run_case((0.0, 1.0, 0.0, 1.0, 1.0, 0.0), 'ident0', s2, dis2)

    for name, st, d in (("(ii) window+generic", stats, dis), ("(iii) m=0 / Ks<=Kg", s2, dis2)):
        print(f"{name}: cases={st['n']} identically-zero f={st['identically0']}")
        print("    root-count histogram A:", dict(sorted(st['hist_A'].items())), " B:", dict(sorted(st['hist_B'].items())))
        print("    max roots found: A", st['maxA'], " B", st['maxB'])
        print("    count agreement A vs B:", st['agree'], "of", st['n'] - st['identically0'], "; agreeing counts with root values differing >1e-6 rel:", st['root_val_mismatch'])
        print("    count disagreements:", len(d))
        from collections import Counter
        print("    adjudication (right route) by tag class:", dict(Counter((tg.split('_m')[0] if tg.startswith('window') else tg, who) for tg, _, _, _, _, who in d)))
        print("    adjudication by m for window cases:", dict(Counter((tg, who) for tg, _, _, _, _, who in d if tg.startswith('window'))))
        for tag, case, ca, cb, t, who in d[:12]:
            print("      e.g.", tag, case, "A", ca, "B", cb, "mp50 truth", t, "-> right route:", who)
        # which route matched mp truth overall
        print("    route A matches mp50 truth in", sum(1 for x in d if x[5] in ('A',)), "of", len(d), "; B in", sum(1 for x in d if x[5] == 'B'), "; neither", sum(1 for x in d if x[5] == 'neither'))
    # 3-root evidence in window
    print("\nNote: 3-root count in (ii) is the A=3 entry of the histogram above (window cases are tagged window_m*).")
    print("Tags (ii):", stats['tag'])
    print("3-root counts per tag [route A, route B] (of 100 each for window tags):", stats['three'])
    print("window cases with >=1 of A,B finding 3 roots: see above; window cases total", nwin)


if __name__ == "__main__":
    main()
