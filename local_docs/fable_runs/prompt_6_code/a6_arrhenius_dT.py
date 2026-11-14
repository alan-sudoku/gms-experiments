"""A6: self-heating dT that changes an Arrhenius rate by eps.

Spec row A6.  Closed form dT = T^2 c/(1 - T c), c = R ln(1+eps)/Q, versus
independent bisection of exp[(Q/R)(1/T - 1/(T+dT))] - (1+eps) on [0, 500 K];
if no sign change, extend to 5000 K and report (plan 3.2).  R = M01.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from p6_common import bisect, tag, R_GAS as R

maxrd = 0; fails = 0
for eps in [0.05, 0.10]:
    for Q in [50e3, 100e3, 200e3, 300e3]:
        for T in [300, 600, 900, 1200, 1500]:
            c = R * np.log1p(eps) / Q
            den = 1 - T * c
            cf = T * T * c / den if den > 0 else float('nan')
            f = lambda d: np.exp((Q / R) * (1 / T - 1 / (T + d))) - (1 + eps)
            r = bisect(f, 0.0, 500.0, extend_limit=5000.0)
            note = ""
            if r['extended']:
                note = f" [no sign change on [0,500]: f ends ({r['flo']:.3e},{r['fhi']:.3e}); extended to {r.get('hi_ext')}: f={r.get('fhi_ext'):.3e}]"
            if not r['bracketed']:
                print(f"eps={eps} Q={Q/1e3:.0f} T={T}: closed={cf:.5g} bisection NO BRACKET (T c={T*c:.3f}, closed form {'invalid (T c >= 1)' if den<=0 else 'valid'}){note}")
                continue
            bs = r['root']
            rd = abs(bs - cf) / cf if den > 0 else float('nan')
            maxrd = max(maxrd, rd) if den > 0 else maxrd
            print(f"eps={eps} Q={Q/1e3:3.0f} kJ/mol T={T:4d} K: closed={cf:9.4f} K bisect={bs:9.4f} K rel={rd:.1e} first-order={T*T*c:.4f}{note}")
print(f"A6 max rel diff closed vs bisection = {maxrd:.2e} {tag(maxrd<1e-6)}")
hand = [(0.05, 50e3, 300, 0.73), (0.05, 200e3, 1200, 2.9), (0.05, 300e3, 1500, 3.0), (0.05, 50e3, 1500, (18.0, 19.0))]
for eps, Q, T, h in hand:
    c = R * np.log1p(eps) / Q
    cf = T * T * c / (1 - T * c)
    if isinstance(h, tuple):
        ok = h[0] <= cf <= h[1]
        print(f"A6 hand eps={eps} Q={Q/1e3:.0f} T={T}: hand {h} calc={cf:.3f} {tag(ok)}")
    else:
        ok = abs(cf - h) / h < 0.03
        print(f"A6 hand eps={eps} Q={Q/1e3:.0f} T={T}: hand {h} calc={cf:.3f} rel={abs(cf-h)/h:.3f} {tag(ok)}")
