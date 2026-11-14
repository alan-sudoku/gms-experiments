#!/usr/bin/env python3
"""B1 (skin depth Cu, Al) and B2 (Dowell factor F(xi), minimum of F/xi, small-xi series).
Spec rows B1, B2. Claim G1.4. Level: derived (unverified).
B1: delta = sqrt(2/(2 pi f mu0 sigma)), f in {50,60,400,1e4,1e5,1e6} Hz, sigma_Cu 5.80e7, sigma_Al 3.54e7 S/m (MEMORY).
B2: F(xi) = xi (sinh2xi + sin2xi)/(cosh2xi - cos2xi); minimise F/xi on [0.1,10] with minimize_scalar (bounded; the interval
brackets the minimum if F/xi is larger at both ends: checked); series F-1 = 4 xi^4/45 fitted on [0.05,0.3].
The 'widely tabulated' skin depths (9.35, 8.5 mm Cu; 12.0 mm Al) were taken from the plan and NOT confirmed from a source.
"""
import numpy as np
from scipy.optimize import minimize_scalar
mu0 = 1.25663706e-6; sCu, sAl = 5.80e7, 3.54e7
fails = 0
def chk(name, val, exp, tol):
    global fails
    ok = abs(val/exp-1) <= tol; fails += (not ok)
    print(f"CHECK {name}: {val:.5g} vs {exp} tol={tol*100:g}% -> {'PASS' if ok else 'FAIL'}")
print("B1 INPUTS: mu0=1.25663706e-6, sigma_Cu=5.80e7, sigma_Al=3.54e7 (MEMORY)")
print("   f [Hz]    delta_Cu [mm]  delta_Al [mm]  ratio")
for f in (50, 60, 400, 1e4, 1e5, 1e6):
    d = [np.sqrt(2/(2*np.pi*f*mu0*s)) for s in (sCu, sAl)]
    print(f"{f:9.0f} {d[0]*1e3:13.4f} {d[1]*1e3:13.4f} {d[1]/d[0]:8.4f}")
    chk(f"delta_Al/delta_Cu at {f:g} Hz", d[1]/d[0], 1.28, 0.02)
    if f == 50: chk("Cu 50 Hz 9.35 mm (plan; not confirmed from source)", d[0]*1e3, 9.35, 0.02); chk("Al 50 Hz 12.0 mm (plan)", d[1]*1e3, 12.0, 0.02)
    if f == 60: chk("Cu 60 Hz 8.5 mm (plan)", d[0]*1e3, 8.5, 0.02)
print("   (the ratio sqrt(sigma_Cu/sigma_Al)=1.2800 is the same expression at every f: those 6 ratio checks are IDENTITY-like in f; they test the sigma inputs only.)")
def F(x): return x*(np.sinh(2*x)+np.sin(2*x))/(np.cosh(2*x)-np.cos(2*x))
def G(x): return (np.sinh(2*x)+np.sin(2*x))/(np.cosh(2*x)-np.cos(2*x))   # F/xi
print("\nB2")
print(f"F/xi at ends of bracket: G(0.1)={G(0.1):.4f}, G(10)={G(10):.6f} (the interval contains the global minimum 0.917 near pi/2, but F/xi is NOT unimodal on it)")
r0 = minimize_scalar(G, bounds=(0.1, 10), method="bounded", options={"xatol": 1e-12})
print(f"plain bounded minimisation on [0.1,10] returned xi={r0.x:.6f}, F/xi={r0.fun:.6f}: a LOCAL minimum (F/xi oscillates about 1 for large xi, so it is not unimodal); the global minimum is found by bracketing with a coarse scan then refining")
xg = np.linspace(0.1, 10, 991); ig = int(np.argmin(G(xg)))
r = minimize_scalar(G, bounds=(xg[ig-1], xg[ig+1]), method="bounded", options={"xatol": 1e-12})
print(f"scan bracket [{xg[ig-1]:.3f},{xg[ig+1]:.3f}] used only to bracket; the minimum is the refined value")
print(f"minimum of F/xi: xi = {r.x:.6f} (pi/2 = {np.pi/2:.6f}), F/xi = {r.fun:.6f}")
print("  note: the refined minimiser lands on pi/2 to 1e-6 (dG/dxi vanishes at pi/2 analytically)")
chk("xi_min vs pi/2", r.x, np.pi/2, 0.005)
chk("min F/xi vs 0.917", r.fun, 0.917, 0.005)
chk("F/xi at xi=pi/2 (analytic point)", G(np.pi/2), 0.917, 0.005)
xs = np.linspace(0.05, 0.3, 40)
c = np.sum((F(xs)-1)*xs**4)/np.sum(xs**8)
print(f"series fit F-1 = c xi^4 on [0.05,0.3] (least squares through origin): c = {c:.5f}; 4/45 = {4/45:.5f}")
chk("series coefficient vs 0.0889", c, 0.0889, 0.005)
cc = np.polyfit(xs**4, F(xs)-1, 1)
print(f"  (linear fit of F-1 on xi^4 with intercept: slope {cc[0]:.5f}, intercept {cc[1]:.2e}; limit xi->0 slope 4/45 = {4/45:.5f}; slope on this range is shifted slightly by the xi^8 term)")
print(f"F/xi at xi=10: {G(10):.6f}")
chk("F/xi -> 1 at xi=10", G(10), 1.0, 0.005)
print("IDENTITY CHECKS: 'F/xi at pi/2' is an evaluation of the same formula the minimiser uses; kept as a value check only.")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails} checks)")
