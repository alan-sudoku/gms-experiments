"""A9: self-heating dT that dries a surface below the critical humidity.

Spec row A9.  Bisection on dT in [0, 30 K] of RH_amb*psat(th)/psat(th+dT) - RH_crit,
psat from M12 (Magnus, th in C); then the Arrhenius multiplier at that dT for
Q = 50 kJ/mol (T_env = th + 273.15 K).  RH_crit = 0.8 is M13.
Cases with RH_amb <= RH_crit have f(0) <= 0: no drying needed, reported, no root.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from p6_common import bisect, tag, R_GAS as R

psat = lambda th: 610.94 * np.exp(17.625 * th / (th + 243.04))
Q = 50e3
res = {}
for th in [5.0, 20.0, 35.0]:
    for rh in [0.85, 0.95, 1.00]:
        for rc in [0.6, 0.8]:
            f = lambda d: rh * psat(th) / psat(th + d) - rc
            if f(0.0) <= 0:
                print(f"th={th} RH_amb={rh} RH_crit={rc}: f(0)={f(0.0):.3f} <= 0, already below critical; no root")
                continue
            r = bisect(f, 0.0, 30.0, extend_limit=300.0)
            if not r['bracketed']:
                print(f"th={th} RH_amb={rh} RH_crit={rc}: NO BRACKET f(0)={r['flo']:.3f} f(30)={r['fhi']:.3f} ext={r.get('fhi_ext')}")
                continue
            d = r['root']
            T = th + 273.15
            m = np.exp((Q / R) * (1 / T - 1 / (T + d)))
            res[(th, rh, rc)] = (d, m)
            print(f"th={th:4.1f} C RH_amb={rh:.2f} RH_crit={rc}: bracket f=({r['flo']:.3f},{r['fhi']:.3f}) dT={d:.4f} K, Arrhenius multiplier(Q=50 kJ/mol)={m:.4f}")
def inr(name, v, lo, hi, tol=0.05):
    ok = lo * (1 - tol) <= v <= hi * (1 + tol)
    print(f"A9 hand {name}: range [{lo},{hi}] (+-5%) calc={v:.3f} {tag(ok)}")
inr("20C 0.95->0.80", res[(20.0, 0.95, 0.8)][0], 2.6, 3.0)
inr("20C 1.00->0.80", res[(20.0, 1.00, 0.8)][0], 3.4, 3.8)
inr("20C 1.00->0.60", res[(20.0, 1.00, 0.6)][0], 8.3, 8.3)
T = 293.15
m28 = np.exp((Q / R) * (1 / T - 1 / (T + 2.8)))
print(f"A9 hand Arrhenius multiplier at 2.8 K (20 C): about 1.2; calc {m28:.4f} {tag(abs(m28-1.2)/1.2<0.05)}")
