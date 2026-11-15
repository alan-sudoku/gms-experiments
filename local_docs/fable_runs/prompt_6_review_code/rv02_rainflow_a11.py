"""Prompt 6 review (S5), script 2: independent rainflow check of A11 (M1.6) and a phase sweep.

Level `derived` (unverified). Independent of prompt_6_code/rainflow_util.py: turning points are found
as roots of the analytic derivative (brentq on a fine bracket grid), not by sampling, and cycles are
counted with the ASTM E1049 four-point rule on the history rotated to start at its absolute maximum.
Dissipation per slow period = sum over cycles of amplitude^n; separate sum = s1^n + phi (s s1)^n.

Run: <gms-local>/.venv/bin/python rv02_rainflow_a11.py > outputs/rv02_rainflow_a11.txt
"""
import math
import numpy as np
from scipy.optimize import brentq


def turning_points(s, phi, ph=0.0, ngrid=20000):
    f = lambda t: math.sin(2 * math.pi * t) + s * math.sin(2 * math.pi * phi * t + ph)
    df = lambda t: 2 * math.pi * (math.cos(2 * math.pi * t) + s * phi * math.cos(2 * math.pi * phi * t + ph))
    tg = np.linspace(0, 1, ngrid * max(1, phi) + 1)
    d = np.array([df(t) for t in tg])
    roots = []
    for i in range(len(tg) - 1):
        if d[i] == 0.0:
            roots.append(tg[i])
        elif d[i] * d[i + 1] < 0:
            roots.append(brentq(df, tg[i], tg[i + 1], xtol=1e-15))
    roots = [r for r in roots if r < 1.0 - 1e-14]
    vals = [f(r) for r in roots]
    # keep only alternating extrema (drop inflection-type double roots)
    out = []
    for v in vals:
        if len(out) >= 2 and (out[-1] - out[-2]) * (v - out[-1]) > 0:
            out[-1] = v
        else:
            out.append(v)
    return out


def _four_point(seq):
    st, cyc = [], []
    for v in seq:
        st.append(v)
        while len(st) >= 4:
            a, b_, c, d = st[-4:]
            if abs(c - b_) <= abs(b_ - a) and abs(c - b_) <= abs(d - c):
                cyc.append(abs(c - b_) / 2)
                del st[-3:-1]
            else:
                break
    return cyc, st


def rainflow4(tp):
    """Four-point rule on the history rotated to its absolute maximum; the residue of a periodic
    history is closed by running the rule once more on residue + residue (ASTM practice for
    repeating histories); every cycle found there is a full cycle of the periodic history."""
    k = int(np.argmax(tp))
    seq = list(tp[k:]) + list(tp[:k]) + [tp[k]]
    cyc, res = _four_point(seq)
    if len(res) > 1:
        c2, _ = _four_point(res + res[1:])
        cyc += c2
    return cyc


S1 = 1.0
print("rv02: independent rainflow of sin(2 pi t) + s sin(2 pi phi t + ph), ratio to separate sum. Level derived.")
rows = []
for n in (2, 3):
    for phi in (1, 3, 9, 33):
        for s in (0.1, 1 / 3, 1.0):
            if phi == 1:
                rf = (1 + s) ** n
                ncyc = 1
                sep = 1 + s ** n
            else:
                tp = turning_points(s, phi)
                cyc = rainflow4(tp)
                rf = sum(a ** n for a in cyc)
                ncyc = len(cyc)
                sep = 1 + phi * s ** n
            ub = phi * (1 + s) ** n
            rows.append((n, phi, s, rf / sep, ub / rf, ncyc))
            print("n=%d phi=%2d s=%.4f: rainflow/separate = %.4f  UB/rainflow = %7.3f  full cycles = %d"
                  % (n, phi, s, rf / sep, ub / rf, ncyc))
r = np.array([x[3] for x in rows])
u = np.array([x[4] for x in rows])
print("range of rainflow/separate over the 24 cases: %.4f to %.4f ; max UB/rainflow = %.3f ; min UB/rainflow = %.4f" % (r.min(), r.max(), u.max(), u.min()))
print("  (answer M1.6 says 'up to 42.5 times the rainflow value'; 42.52 is the UB/separate ratio at n=3, phi=33, s=0.1)")

print("\nPhase sweep of the fast component (ph in degrees), ratio rainflow/separate:")
for n, phi, s in ((2, 3, 1 / 3), (2, 3, 1.0), (3, 3, 1 / 3), (2, 9, 1 / 3), (3, 9, 1 / 3)):
    vals = []
    for phd in range(0, 360, 15):
        tp = turning_points(s, phi, math.radians(phd), ngrid=4000)
        cyc = rainflow4(tp)
        vals.append(sum(a ** n for a in cyc) / (1 + phi * s ** n))
    print("  n=%d phi=%d s=%.3f: min %.4f (ph=%d) max %.4f (ph=%d)" % (n, phi, s, min(vals), 15 * int(np.argmin(vals)), max(vals), 15 * int(np.argmax(vals))))
print("All values level `derived`.")
