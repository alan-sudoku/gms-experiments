#!/usr/bin/env python3
"""A2: Kelvin optimum cross-section A*, Sigma*, and ratio Sigma*_Al/Sigma*_Cu.
Spec row A2 (prompt_5_plan.md section 3). Claim G2.2.  Level: derived (unverified).
Model: Sigma(A) = e*rho*A*L/T0 + I^2*L*tau/(sigma*A*T0); numerical minimiser = scipy minimize_scalar (bounded, in x=ln A).
Closed form: A* = I*sqrt(tau/(sigma*rho*e)); Sigma* = 2*I*L*sqrt(rho*e*tau/sigma)/T0.
Spec bracket A in [1e-7, 1] m2. Where the optimum lies outside it the minimiser hits the bound; the script then reruns on the
widened bracket [1e-12, 1e6] m2 and counts these cases (recorded in issues_a.md).
Inputs MEMORY: sigma_Cu 5.80e7, sigma_Al 3.54e7 S/m; rho_Cu 8960, rho_Al 2700 kg/m3; e_Al 200, e_Cu 55 MJ/kg central (LOOKUP: A3).
"""
import numpy as np
from scipy.optimize import minimize_scalar
T0 = 298.15
MAT = {"Cu": (5.80e7, 8960.0), "Al": (3.54e7, 2700.0)}
widened = [0]
def sigma(A, m, e, I, L, tau):
    s, r = MAT[m]
    return (e*r*A*L + I*I*L*tau/(s*A))/T0
def numeric(m, e, I, L, tau, lo=1e-7, hi=1.0):
    f = lambda x: sigma(np.exp(x), m, e, I, L, tau)/ (2*I*L*np.sqrt(MAT[m][1]*e*tau/MAT[m][0])/T0)   # scaled for conditioning only
    res = minimize_scalar(f, bounds=(np.log(lo), np.log(hi)), method="bounded", options={"xatol": 1e-11})
    A = np.exp(res.x)
    if A < lo*(1+1e-6) or A > hi*(1-1e-6):
        widened[0] += 1
        res = minimize_scalar(f, bounds=(np.log(1e-12), np.log(1e6)), method="bounded", options={"xatol": 1e-11})
        A = np.exp(res.x)
    return A, sigma(A, m, e, I, L, tau)
def closed(m, e, I, L, tau):
    s, r = MAT[m]
    return I*np.sqrt(tau/(s*r*e)), 2*I*L*np.sqrt(r*e*tau/s)/T0
if __name__ == "__main__":
    print("INPUTS: sigma_Cu=5.80e7, sigma_Al=3.54e7 S/m; rho_Cu=8960, rho_Al=2700 kg/m3 (MEMORY); T0=298.15 K")
    print("LOOKUP sources for e: see a3 (ICE v2.0 2011; Nuss and Eckelman 2014 SI Table S38). Central e_Al=200, e_Cu=55 MJ/kg are MEMORY.")
    fails = 0
    Is, Ls, taus = (10, 1e3, 1e5), (0.1, 1, 100), (1e6, 6.31e8)
    maxdA = maxdS = maxterm = 0.0; ratios = []
    for e_Al, e_Cu in [(200e6, 55e6)]:
        for I in Is:
            for L in Ls:
                for tau in taus:
                    out = {}
                    for m, e in (("Al", e_Al), ("Cu", e_Cu)):
                        A, S = numeric(m, e, I, L, tau); Ac, Sc = closed(m, e, I, L, tau)
                        s, r = MAT[m]
                        emb = e*r*A*L/T0; op = I*I*L*tau/(s*A*T0)
                        maxdA = max(maxdA, abs(A/Ac-1)); maxdS = max(maxdS, abs(S/Sc-1)); maxterm = max(maxterm, abs(emb/op-1))
                        out[m] = (A, S, Ac, Sc)
                    ratios.append(out["Al"][1]/out["Cu"][1])
    print(f"central case e_Al=200, e_Cu=55 MJ/kg over 18 (I,L,tau) combinations:")
    print(f"  max |A_num/A_closed-1| = {maxdA:.3e} ; max |S_num/S_closed-1| = {maxdS:.3e} ; max |embodied/operating-1| = {maxterm:.3e}")
    ok = maxdS < 1e-6; fails += (not ok)
    print(f"CHECK Sigma* numeric vs closed form < 1e-6 relative -> {'PASS' if ok else 'FAIL'}")
    ok = maxdA < 1e-6; fails += (not ok)
    print(f"CHECK A* numeric vs closed form < 1e-6 relative (spec tolerance applies to closed-form agreement) -> {'PASS' if ok else 'FAIL'}  (value {maxdA:.2e})")
    ok = maxterm < 1e-6; fails += (not ok)
    print(f"CHECK embodied term = operating term at optimum (ratio 1) within 1e-6 -> {'PASS' if ok else 'FAIL'}  (value {maxterm:.2e})")
    rat = np.array(ratios); spread = (rat.max()-rat.min())/rat.mean()
    exact = np.sqrt((200e6*2700/3.54e7)/(55e6*8960/5.8e7))
    print(f"  ratio Sigma*_Al/Sigma*_Cu: mean {rat.mean():.6f}, spread (max-min)/mean {spread:.2e}; closed-form independent value {exact:.6f}")
    ok = spread < 1e-6; fails += (not ok)
    print(f"CHECK ratio independent of I, L, tau (spread < 1e-6) -> {'PASS' if ok else 'FAIL'}")
    print("  note: the closed-form A*, Sigma* are the analytic stationary point of the same Sigma(A); 'numeric vs closed form' is a real check (minimiser vs algebra), 'terms equal' follows from the same stationarity: label IDENTITY-ADJACENT (it verifies the minimiser, not the physics)")
    # swept e
    eal = np.linspace(10e6, 300e6, 7); ecu = np.linspace(10e6, 150e6, 6)
    maxd = 0.0; rs = []
    for ea in eal:
        for ec in ecu:
            row = []
            for I, L, tau in ((10, 0.1, 1e6), (1e5, 100, 6.31e8), (1e3, 1, 1e6)):
                Sa = numeric("Al", ea, I, L, tau)[1]; Sc = numeric("Cu", ec, I, L, tau)[1]
                row.append(Sa/Sc)
            ex = np.sqrt((ea*2700/3.54e7)/(ec*8960/5.8e7))
            maxd = max(maxd, abs(np.array(row)/ex-1).max(), (max(row)-min(row))/ex)
            rs.append((ea/1e6, ec/1e6, row[0], ex))
    print("swept e_Al in [10,300], e_Cu in [10,150] MJ/kg (7x6 grid, 3 load cases each):")
    print("  e_Al e_Cu  ratio(num)  ratio(closed)   (first load case)")
    for a in rs[::5]: print(f"  {a[0]:5.0f} {a[1]:4.0f} {a[2]:10.5f} {a[3]:10.5f}")
    ok = maxd < 1e-6; fails += (not ok)
    print(f"CHECK swept ratio equals closed form and is load-independent, max deviation {maxd:.2e} (<1e-6) -> {'PASS' if ok else 'FAIL'}")
    A, S = numeric("Cu", 55e6, 1.0, 1.0, 6.31e8); Jstar = 1.0/A/1e6
    print(f"J* = I/A* for Cu at e=55 MJ/kg, tau=6.31e8 s: {Jstar:.3f} A/mm2 (closed form {1/closed('Cu',55e6,1,1,6.31e8)[0]/1e6:.3f}); spec expected ~0.21 (range 0.05-1)")
    ok = 0.05 <= Jstar <= 1; fails += (not ok)
    print(f"CHECK J* within planner range 0.05-1 A/mm2 -> {'PASS' if ok else 'FAIL'} (computed J* is {Jstar/0.21:.1f}x the plan's 0.21; hand check: J*^2*tau = sigma*rho*e = {5.8e7*8960*55e6:.3e} A2 s/m4 -> J* = sqrt of that / sqrt(tau) = {np.sqrt(5.8e7*8960*55e6/6.31e8)/1e6:.2f} A/mm2)")
    print(f"minimiser hit the spec bracket [1e-7,1] m2 in {widened[0]} runs (reran on widened bracket)")
    print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails} checks)")
