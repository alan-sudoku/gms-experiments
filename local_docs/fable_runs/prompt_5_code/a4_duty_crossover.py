#!/usr/bin/env python3
"""A4: equal-volume duty crossover, Al (g) vs Cu (s).
Spec row A4. Claims G2.4, G2.5. Level: derived (unverified).
Delta Sigma = (e_g rho_g - e_s rho_s) A L/T0 + I^2 L tau (1/sigma_g - 1/sigma_s)/(A T0), I = J*A.
Sweep J in [0.1,10] A/mm2 and tau in [1e5,1e9] s; crossover located along tau at each J by brentq on Delta Sigma;
compared with (J^2 tau)* = (e_s rho_s - e_g rho_g)/(1/sigma_g - 1/sigma_s).
Independent check: D = (J/J*)^2 (J* = Kelvin optimum current density of Cu, A2) must exceed 1 wherever Al loses.
e values MJ/kg: MEMORY (200, 55, 20) and LOOKUP (data/a3_embodied_energy.csv: ICE v2.0 2011, Nuss and Eckelman 2014 SI Table S38).
"""
import numpy as np
from scipy.optimize import brentq
T0 = 298.15; A = 1e-4; L = 1.0
sCu, rCu, sAl, rAl = 5.80e7, 8960.0, 3.54e7, 2700.0
def dSigma(J_Amm2, tau, eAl, eCu):
    J = J_Amm2*1e6; I = J*A
    return ((eAl*rAl - eCu*rCu)*A*L + I*I*L*tau*(1/sAl - 1/sCu)/A)/T0
cases = [("MEMORY primary/primary 200/55", 200e6, 55e6), ("MEMORY secondary Al 20 / primary Cu 55", 20e6, 55e6),
         ("ICE primary/primary 218/57", 218e6, 57e6), ("ICE secondary Al 29.0 / primary Cu 57", 29.0e6, 57e6),
         ("ICE secondary/secondary 29.0/16.5", 29.0e6, 16.5e6), ("Nuss primary/primary 194/59.3", 194e6, 59.3e6),
         ("Nuss old-scrap Al 23.8 / primary Cu 59.3", 23.8e6, 59.3e6), ("Nuss secondary/secondary 23.8/28.1", 23.8e6, 28.1e6)]
Js = np.logspace(-1, 1, 41); taus = np.logspace(5, 9, 400)
fails = 0
print("INPUTS: sigma_Cu 5.80e7, sigma_Al 3.54e7 S/m; rho_Cu 8960, rho_Al 2700 (MEMORY). Lookup sources: ICE v2.0 summary tables (Hammond and Jones 2011), Nuss and Eckelman 2014 SI Table S38, access 2026-11-14")
for name, eAl, eCu in cases:
    x = eAl*rAl; y = eCu*rCu
    print(f"\nCASE {name}: e*rho Al={x:.3e}, Cu={y:.3e} J/m3")
    if x >= y:
        # expect no sign change anywhere
        sg = [(dSigma(J, t, eAl, eCu) > 0) for J in Js for t in taus]
        ok = all(sg)
        print(f"  no crossover expected (e_g rho_g >= e_s rho_s); Delta Sigma > 0 on whole grid: {ok} -> {'PASS' if ok else 'FAIL'}; (sweep cannot bracket a crossover: none exists)")
        fails += (not ok); continue
    ex = (y - x)/(1/sAl - 1/sCu)
    worst = 0; Dmin = 1e99; brk_all = True; nbr = 0
    for J in Js:
        f = lambda lt: dSigma(J, 10**lt, eAl, eCu)
        if f(5)*f(9) > 0: brk_all = False; continue
        nbr += 1
        lt = brentq(f, 5, 9, xtol=1e-13); tau_c = 10**lt
        worst = max(worst, abs((J*1e6)**2*tau_c/ex - 1))
    print(f"  analytic (J^2 tau)* = {ex:.4e} A2 s/m4 ; max rel. deviation of brentq crossover over J grid = {worst:.2e}")
    print(f"  at J=1 A/mm2: tau* = {ex/1e12:.3e} s ({ex/1e12/3.156e7:.2f} full-load years); sweep brackets the crossover (tau in [1e5,1e9]) at {nbr} of {len(Js)} J values; at the others the crossover tau lies outside the tau range")
    ok = worst < 0.05; fails += (not ok)
    print(f"  CHECK crossover vs analytic +-5%: {'PASS' if ok else 'FAIL'}")
    if name.startswith("MEMORY secondary"):
        okv = abs(ex/4.0e19 - 1) < 0.05; fails += (not okv)
        print(f"  CHECK (J^2 tau)* vs spec 4.0e19 +-5%: {ex:.3e} -> {'PASS' if okv else 'FAIL'}")
    # D check: D = (J/J*)^2 at the crossover; J* = Kelvin optimum of Cu with its own e and tau
    # at crossover J^2 tau = ex ; J*^2 tau = sigma_Cu rho_Cu e_Cu  -> D = ex/(sCu rCu eCu)
    D = ex/(sCu*rCu*eCu)
    print(f"  D = (J/J*)^2 at crossover = {D:.3f} (analytic (1-x)/(sigma_s/sigma_g-1) with x={x/y:.3f}); Al loses for D > {D:.3f}")
    ok = D > 1; fails += (not ok)
    print(f"  CHECK 'D must exceed 1 wherever Al loses' -> {'PASS' if ok else 'FAIL (Al loses for D between %.2f and 1 as well)' % D}")
print("\nNOTE: the sweep is deterministic arithmetic of the closed-form crossover, so brentq vs analytic is a numerical-root check, not independent physics.")
print("D-check: D at crossover = (1-x)/(sigma_s/sigma_g-1), x = e_g rho_g/(e_s rho_s); D>1 iff x < 0.362 (sigma_Cu/sigma_Al = 1.638) -- the plan's claim holds only for x < 0.362.")
print("OVERALL", "PASS" if fails == 0 else f"PARTIAL/FAIL ({fails} checks failed)")
