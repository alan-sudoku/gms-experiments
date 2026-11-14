"""X4: C4 cost h(s) = Kg [ m sqrt(s) + sqrt(tau - m s) ], m = floor(tau/s), strictly decreasing in s on (0, tau].

Claim (C4): for Kg>0 and fixed tau >= tw, h is strictly decreasing in s = tw; m*Rg is non-increasing in s;
h is continuous at the points s = tau/k where m changes (left and right limits agree).
Method (independent of earlier scripts):
 (a) numpy dense sampling of h on (0, tau] (log grid 4000 + linear grid 4000 + points tau/k and tau/k +- 1,2,3 ulp for
     k = 1..60), sorted by s, check np.diff(h) <= tol (tol = 8 eps * h) in float64, and count strictly negative steps;
 (b) for the ulp neighbours of tau/k, evaluate h EXACTLY (Fraction m, 50-digit mpmath) and check h(prev) > h(s_k)
     > h(next) in exact arithmetic (strict) -- this is the non-trivial check across jumps of m;
 (c) left/right limits at s = tau/k in 50 digits: m=k branch vs m=k-1 branch evaluated at the same s;
 (d) numeric derivative sign on each constant-m piece: dh/ds = Kg m (1/(2 sqrt s) - 1/(2 sqrt(tau - m s))) < 0
     iff tau < (m+1) s, which holds because m = floor(tau/s) > tau/s - 1  (identity-level argument; the numeric check
     samples dh/ds with the analytic formula at random interior points and counts non-negative values);
 (e) m non-increasing in s (np.diff of floor(tau/s) <= 0).
Run: <gms-local>/.venv/bin/python x4_h_monotone.py
"""
import sys, os, math, random
sys.dont_write_bytecode = True
from fractions import Fraction
import numpy as np
import mpmath as mp

mp.mp.dps = 50
M = mp.mpf


def h_float(s, tau, Kg):
    m = np.floor(tau / s)
    return Kg * (m * np.sqrt(s) + np.sqrt(np.maximum(tau - m * s, 0.0))), m


def h_exact(s, tau, Kg, m=None):
    if m is None:
        m = int(Fraction(tau) / Fraction(s))
    return M(Kg) * (M(m) * mp.sqrt(M(s)) + mp.sqrt(M(tau) - M(m) * M(s)))


def main():
    rng = random.Random(99)
    nrng = np.random.default_rng(99)
    n_tau = 300
    tot = dict(float_steps=0, float_pos_steps=0, float_pos_max_rel=0.0, ex_pairs=0, ex_bad=0, lim_pts=0, lim_max=0.0,
               ex_cross_pairs=0, deriv_pts=0, deriv_bad=0, m_bad=0, left_right_float_max=0.0)
    for it in range(n_tau):
        tau = 10 ** rng.uniform(-3, 10) * rng.choice([1.0, 1.0, 1.0 / 3.0, math.pi])
        Kg = 10 ** rng.uniform(-6, 1)
        ks = np.arange(1, 61)
        sk = tau / ks
        pts = [sk]
        for u in (1, 2, 3):
            lo = sk.copy(); hi = sk.copy()
            for _ in range(u):
                lo = np.nextafter(lo, 0.0); hi = np.nextafter(hi, np.inf)
            pts += [lo, hi]
        grid_log = np.geomspace(tau * 1e-9, tau, 4000)
        grid_lin = np.linspace(tau / 1e4, tau, 4000)
        s = np.unique(np.concatenate(pts + [grid_log, grid_lin, np.array([tau])]))
        s = s[(s > 0) & (s <= tau)]
        h, m = h_float(s, tau, Kg)
        d = np.diff(h)
        tol = 8 * 2.0 ** -52 * np.maximum(np.abs(h[:-1]), np.abs(h[1:]))
        tot['float_steps'] += len(d)
        pos = d > tol
        tot['float_pos_steps'] += int(pos.sum())
        if pos.any():
            tot['float_pos_max_rel'] = max(tot['float_pos_max_rel'], float((d[pos] / h[:-1][pos]).max()))
        tot['m_bad'] += int((np.diff(m) > 0).sum())
        # (b) exact strict monotone on ulp triples around tau/k
        for k in range(1, 61, 3):
            s0 = float(tau / k)
            trip = [math.nextafter(s0, 0.0), s0, math.nextafter(s0, math.inf)]
            if trip[2] > tau:
                trip = trip[:2]
            vals = [h_exact(x, tau, Kg) for x in trip]
            ms = [int(Fraction(tau) / Fraction(x)) for x in trip]
            for i in range(len(vals) - 1):
                tot['ex_pairs'] += 1
                if ms[i] != ms[i + 1]:
                    tot['ex_cross_pairs'] += 1
                if not vals[i] > vals[i + 1]:
                    tot['ex_bad'] += 1
        # (c) limits at s = tau/k (exact rational point), branches m=k and m=k-1
        for k in range(2, 40, 5):
            sx = M(tau) / k          # rounded to 50 digits ...
            tx = k * sx              # ... and tau redefined as k*sx so that s = tau/k holds exactly in mp
            hl = M(Kg) * (k * mp.sqrt(sx) + mp.sqrt(tx - k * sx))
            hr = M(Kg) * ((k - 1) * mp.sqrt(sx) + mp.sqrt(tx - (k - 1) * sx))
            tot['lim_pts'] += 1
            tot['lim_max'] = max(tot['lim_max'], float(abs(hl - hr) / abs(hl)))
        # float limit gap across the tie: h(prev ulp) vs h(next ulp)
        for k in range(2, 60, 7):
            s0 = float(tau / k)
            a_, _ = h_float(np.array([math.nextafter(s0, 0.0)]), tau, Kg)
            b_, _ = h_float(np.array([math.nextafter(s0, math.inf)]), tau, Kg)
            tot['left_right_float_max'] = max(tot['left_right_float_max'], float(abs(a_[0] - b_[0]) / a_[0]))
        # (d) derivative sign on constant-m pieces
        for _ in range(60):
            sv = tau * 10 ** rng.uniform(-6, 0)
            mv = math.floor(tau / sv)
            if mv < 1:
                continue
            rad = tau - mv * sv
            if rad <= 0:
                continue
            dh = Kg * mv * (1 / (2 * math.sqrt(sv)) - 1 / (2 * math.sqrt(rad)))
            tot['deriv_pts'] += 1
            if dh >= 0 and not (tau - mv * sv) >= sv * (1 - 1e-12):
                tot['deriv_bad'] += 1
    print("X4 h(s) monotone; random tau count:", n_tau, " Kg>0 random")
    print("(a) float sample steps:", tot['float_steps'], " steps with increase > 8 eps*h:", tot['float_pos_steps'],
          " max relative increase: %.3g" % tot['float_pos_max_rel'])
    print("(e) m non-increasing: violations", tot['m_bad'])
    print("(b) exact adjacent ulp pairs around tau/k:", tot['ex_pairs'], " of which m changes across the pair:",
          tot['ex_cross_pairs'], " pairs not strictly decreasing:", tot['ex_bad'])
    print("(c) exact left/right limit at s=tau/k: points", tot['lim_pts'], " max relative gap %.3g (50-digit)" % tot['lim_max'])
    print("    float h just below vs just above tau/k: max relative gap %.3g" % tot['left_right_float_max'])
    print("    (this gap is real, not an artefact: on the m=k side sqrt(tau - k s) has infinite slope at s -> tau/k, so one ulp moves h by ~sqrt(ulp) relative)")
    print("(d) dh/ds sign on constant-m pieces: points", tot['deriv_pts'], " non-negative (outside rounding 1e-12):", tot['deriv_bad'])
    print("FLAG: (d) restates the algebraic proof; it is a sanity check of the sign identity, not independent evidence.")


if __name__ == "__main__":
    main()
