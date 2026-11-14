"""A4, A5, A12: sign-reversal multipliers, series-resistance multiplier,
self-heating by reaction heat.

Spec rows A4, A5, A12 (plan 3.3).  Closed-form tabulations; hand values from the
spec are compared.  A5 additionally checks the life-average factors 1/2 and 2/3
by Simpson quadrature (independent of the stated factors).
Assumptions: PBR from M10 (1.28, 2.07, 1.65); R_f from M11; k_ox grid from M32;
1 um/yr = 3.16881e-14 m/s, 1 yr = 3.15576e7 s (3.1 conventions).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from p6_common import simpson, tag, UM_PER_YR

print("=== A4 ===")
PBR = {'Al2O3/Al': 1.28, 'Cr2O3/Cr': 2.07, 'NiO/Ni': 1.65}
for xe in [0.1, 0.5]:
    print(f"(i) constant voltage x_e={xe}: {1-xe:.4f}  (formula is 1-x_e itself; no independent check possible: identity)")
rows = {}
for D in [1.0, 10.0]:
    for h in [10.0, 100.0]:
        for k in [5, 4]:
            w = (1 + 2 * h * 1e-3 / D) ** (-k)
            line = f"D={D:4.0f} mm h={h:5.0f} um k={k}: widening={w:.4f}"
            for n, pb in PBR.items():
                base = 1 - 2 * (pb - 1) * h * 1e-3 / D
                if base <= 0:
                    line += f" | {n} PBR={pb}: base={base:.3f} <=0 channel closed"
                else:
                    line += f" | {n} PBR={pb}: narrowing={base**(-k):.4f}"
            print(line)
            rows[(D, h, k)] = w
def chk(name, val, hand, tol=0.01):
    ok = abs(val - hand) / hand < tol
    print(f"A4 hand {name}: hand={hand} calc={val:.4f} rel={abs(val-hand)/hand:.4f} {tag(ok)}")
chk('widening D=1 h=100 k=5', (1 + 0.2) ** -5, 0.402)
chk('narrowing PBR 2.07', (1 - 2 * 1.07 * 0.1) ** -5, 3.33)
chk('narrowing PBR 1.28', (1 - 2 * 0.28 * 0.1) ** -5, 1.33)
chk('widening D=10 h=100 k=5', (1 + 0.02) ** -5, 0.906)
sgn = all((1 + 2 * h * 1e-3 / D) ** (-k) < 1 for D in [1., 10.] for h in [10., 100.] for k in [4, 5]) and \
      all((1 - 2 * (pb - 1) * h * 1e-3 / D) ** (-k) > 1 for D in [1., 10.] for h in [10., 100.] for k in [4, 5] for pb in PBR.values() if 1 - 2 * (pb - 1) * h * 1e-3 / D > 0)
print(f"A4 signs: (i),(ii) < 1 and (iii) > 1 over the grid: {tag(sgn)}")

print("\n=== A5 ===")
Rf_M11 = [1e-4, 2e-4, 5e-4]
for U in [100, 1000, 5000]:
    for Rf in Rf_M11:
        end = 1 + Rf * U
        print(f"U={U:5d} R_f={Rf:.0e}: end={end:.4f} life-avg lin={1+0.5*Rf*U:.4f} par={1+2/3*Rf*U:.4f}")
print("oxide layers R_f = delta/k_ox:")
for d in [1, 10, 100]:
    for k in [2, 10, 30]:
        Rf = d * 1e-6 / k
        s = " ".join(f"U={U}:{1+Rf*U:.4f}" for U in [100, 1000, 5000])
        print(f"delta={d:3d} um k_ox={k:2d}: R_f={Rf:.2e} {s}")
c1 = 1 + 2e-4 * 1000
c2 = 1 + (100e-6 / 2) * 1000
print(f"A5 hand U=1000,R_f=2e-4: hand 1.20 calc={c1:.4f} {tag(abs(c1-1.20)/1.20<0.005)}")
print(f"A5 hand oxide 100um k=2: R_f={100e-6/2:.1e} (hand 5e-5), multiplier={c2:.4f} (hand 1.05) {tag(abs(c2-1.05)/1.05<0.005)}")
lin = simpson(lambda t: t, 0, 1)[0]
par = simpson(lambda t: np.sqrt(t), 0, 1, tol=1e-8, nmax=2**22)
print(f"A5 life-average factors by quadrature: linear growth int t dt = {lin:.8f} (stated 1/2); "
      f"parabolic int sqrt(t) dt = {par[0]:.8f} (stated 2/3; Simpson n={par[1]}, conv={par[3]}; sqrt singularity slows Simpson) "
      f"rel diff to 2/3 = {abs(par[0]-2/3)/(2/3):.1e}")
print("A5 note: plausibility only per spec; 1 + R_f*U is the formula itself, hand values re-evaluate it (identity).")

print("\n=== A12 ===")
rho_m, M, dH = 2780.0, 26.98e-3, 837.9e3
allbelow = True
for r in [1.0, 10.0]:
    rs = r * UM_PER_YR
    q = rs * (rho_m / M) * dH
    for hc in [5, 10, 100]:
        dT = q / hc
        allbelow &= dT < 0.01
        print(f"r={r:4.0f} um/yr: q''={q:.5f} W/m2 h_c={hc:3d}: dT={dT:.3e} K")
q10 = 10 * UM_PER_YR * (rho_m / M) * dH
print(f"A12 hand q''(10 um/yr)=0.027: calc={q10:.5f} rel={abs(q10-0.027)/0.027:.3f} {tag(abs(q10-0.027)/0.027<0.02)}")
print(f"A12 hand dT(10 um/yr, h_c=10)=2.7e-3: calc={q10/10:.3e} rel={abs(q10/10-2.7e-3)/2.7e-3:.3f} {tag(abs(q10/10-2.7e-3)/2.7e-3<0.02)}")
print(f"A12 all cases below 0.01 K: {tag(allbelow)} (max {10*UM_PER_YR*(rho_m/M)*dH/5:.3e} K)")
