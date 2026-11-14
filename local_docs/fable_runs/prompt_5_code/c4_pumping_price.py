#!/usr/bin/env python3
"""C4: pumping-power price of compensating a fin deficit by flow.
Spec row C4. Claim G1.5. Level: derived (unverified).
Baseline sink: base 100 x 100 mm, fin height H = 30 mm, pitch p = 3 mm, t = 1 mm (gap b = 2 mm), flow length L_f = 100 mm; N = 33 fins (floor(100/3)), 32 channels.
Air at 300 K. LOOKUP: Incropera et al., Table A.4, air 300 K (data/c4_air_300K.csv): rho 1.1614 (plan MEMORY: 1.177), mu 1.846e-5, k 0.0263, cp 1007, Pr 0.707.
(a) turbulent duct Nu = 0.023 Re^0.8 Pr^0.4, f = 0.316 Re^-0.25, P = f (L_f/D_h)(rho U^2/2) U A_flow; m = dlnP/dln h over Re in [1e4,1e5].
(b) laminar plate channels, Nu = 7.54 on D_h = 2b, dP = 12 mu L_f U/b^2; R_th(V) = 1/(mdot cp (1-exp(-NTU))), NTU = h A eta_f/(mdot cp)
    with A = fin surface 2 H L_f N (spec formula; base area between fins is NOT included, see issues) and eta_f the fin efficiency, here the
    deficit-reduced value: eta_f,g = (1-d) eta_f,s with d = 6.3% (Al 200 at baseline, from C1: ratio 0.937) and d = 29.3% (1 - sqrt(0.5), thick limit for k 200/400).
    For each baseline volumetric flow V0 in [1e-4, 1e-1] m3/s: find V (brentq) with R_th,g(V) = R_th,s(V0); P ratio = (V/V0)^2 (laminar: dP ~ U, P = dP V).
    The laminar formulas are only valid for Re_Dh < 2300; Re is reported and cases beyond are marked.
(c) blockage: b in [0.5,3] mm at fixed pitch 3 mm and fixed V; fitted exponent of P(b).
"""
import numpy as np
from scipy.optimize import brentq
rho, mu, kair, cp, Pr = 1.1614, 1.846e-5, 0.0263, 1007.0, 0.707
kCu, k200 = 400.0, 200.0
W = 0.100; Lf = 0.100; H = 0.030; p = 0.003; t = 0.001; b = p - t
N = int(W//p); Nch = N - 1
fails = 0
def chk(name, val, exp, tol, absolute=True):
    global fails
    ok = abs(val-exp) <= tol if absolute else abs(val/exp-1) <= tol; fails += (not ok)
    print(f"CHECK {name}: {val:.5g} vs {exp} tol={tol} -> {'PASS' if ok else 'FAIL'}")
print("INPUTS: air 300 K rho=1.1614 (Incropera Table A.4; plan MEMORY 1.177), mu=1.846e-5, k=0.0263, cp=1007, Pr=0.707; geometry W=100 mm, L_f=100 mm, H=30 mm, p=3 mm, t=1 mm, N=%d fins, %d channels" % (N, Nch))
print("LOOKUP SOURCE: Incropera, DeWitt, Bergman, Lavine, Fundamentals of Heat and Mass Transfer, App. A Table A.4 (page 911 in the scanned copy read, edition not printed; plan cites 6th ed. 2007), https://www.mohsin-sies.com/sktn3224/notes/Appendix.Incropera%20DeWitt%20-%20Fundamentals%20of%20Heat%20and%20Mass%20Transfer.pdf, accessed 2026-11-14")
print("   lookup vs plan MEMORY: mu 1.846e-5 equal, k 0.0263 equal, cp 1007 equal, Pr 0.707 equal, rho 1.1614 vs 1.177 (1.3% lower)")
# (a)
Dh = 2*b; Aflow = Nch*b*H
Re = np.logspace(4, 5, 60)
Nu = 0.023*Re**0.8*Pr**0.4; h = Nu*kair/Dh
U = Re*mu/(rho*Dh); f = 0.316*Re**-0.25
P = f*(Lf/Dh)*(rho*U**2/2)*U*Aflow
m = np.polyfit(np.log(h), np.log(P), 1)[0]
mloc = np.gradient(np.log(P), np.log(h))
print(f"(a) duct D_h={Dh*1e3:.1f} mm: fitted m = dlnP/dlnh = {m:.4f} (local min/max {mloc.min():.4f}/{mloc.max():.4f}); analytic 2.75/0.8 = {2.75/0.8:.4f}")
chk("(a) m = 3.44 +-0.05", m, 3.44, 0.05)
print("   IDENTITY note: the exponent follows from the power laws as coded (Re^0.8, Re^-0.25); the fit tests the algebra, not the physics of the correlations.")
# (b)
h0 = 7.54*kair/Dh
print(f"(b) h = Nu k/D_h = 7.54*{kair}/{Dh:.4f} = {h0:.2f} W/(m2 K)")
chk("(b) h = 49.6 +-1%", h0, 49.6, 0.01, False)
m_f = np.sqrt(2*h0/(kCu*t)); eta_s = np.tanh(m_f*H)/(m_f*H)
eta_200 = np.tanh(np.sqrt(2*h0/(k200*t))*H)/(np.sqrt(2*h0/(k200*t))*H)
print(f"    fin efficiency at actual baseline h={h0:.2f}, L={H*1e3:.0f} mm, t=1 mm: eta_Cu={eta_s:.4f}, eta_Al200={eta_200:.4f}, ratio {eta_200/eta_s:.4f}")
Afin = 2*H*Lf*N
def Rth(V, eta):
    mdot = rho*V; C = mdot*cp
    NTU = h0*Afin*eta/C
    return 1.0/(C*(-np.expm1(-NTU))), NTU
def Aflow_U(V): return V/Aflow
print(f"    A_fin = {Afin:.4f} m2, A_flow = {Aflow*1e4:.2f} cm2; limits: R->1/(mdot cp) for NTU>>1, ->1/(h A eta) for NTU<<1")
Vs = np.logspace(-4, -1, 31)
for d in (1-0.937, 1-np.sqrt(0.5)):
    print(f"  deficit d = {d*100:.1f}% of h A eta_f")
    print("   V0 [m3/s]  NTU0    Re_Dh   V/V0     P ratio    note")
    nbr = 0; ncomp = 0
    for V0 in Vs:
        R0, N0 = Rth(V0, eta_s)
        Re0 = rho*(V0/Aflow)*Dh/mu
        g = lambda V: Rth(V, eta_s*(1-d))[0] - R0
        # R_g(V) - R_0 decreasing in V; root exists iff R_g(infty)=1/(hA eta (1-d)) < R0
        Rinf = 1.0/(h0*Afin*eta_s*(1-d))
        if Rinf >= R0:
            note = "not compensable by flow"
            if V0 in Vs[::5]: print(f"  {V0:10.2e} {N0:7.3f} {Re0:8.0f}     -        -     {note}")
            continue
        ncomp += 1
        Vroot = brentq(g, V0, V0*1e9, xtol=1e-18, rtol=1e-13)
        pr = (Vroot/V0)**2
        if V0 in Vs[::5]: print(f"  {V0:10.2e} {N0:7.3f} {Re0:8.0f} {Vroot/V0:8.3f} {pr:10.3f}    {'Re>2300: laminar formula invalid' if Re0*Vroot/V0 > 2300 else ''}")
    print(f"   compensable at {ncomp} of {len(Vs)} V0 values; NTU0 range {Rth(Vs[0],eta_s)[1]:.2f}..{Rth(Vs[-1],eta_s)[1]:.3f}: sweep brackets NTU>>1 and NTU<<1: {Rth(Vs[0],eta_s)[1] > 10 and Rth(Vs[-1],eta_s)[1] < 0.2}")
    # limiting checks
    assert abs(Rth(1e-7, eta_s)[0]*rho*1e-7*cp - 1) < 1e-6
    assert abs(Rth(1e3, eta_s)[0]*h0*Afin*eta_s - 1) < 1e-3
print("   limit checks R_th -> 1/(mdot cp) at V=1e-7 and -> 1/(h A eta) at V=1e3: PASS (asserted, both are limits of the same expression: IDENTITY-like)")
# (c)
bs = np.linspace(0.5e-3, 3e-3, 30); Vfix = 5e-3
Pb = []
for bb in bs:
    Af = Nch*bb*H; Ub = Vfix/Af; Pb.append(12*mu*Lf*Ub/bb**2*Vfix)
ex = np.polyfit(np.log(bs), np.log(Pb), 1)[0]
print(f"(c) b in [0.5,3] mm at fixed V and fixed pitch: fitted exponent {ex:.4f}")
chk("(c) exponent -3.00 +-0.05", ex, -3.0, 0.05)
print("   IDENTITY note: dP = 12 mu L U/b^2 with U = V/(N b H) gives b^-3 by construction; the fit confirms the algebra only. Real ducts have entrance effects and bypass (not modelled).")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
