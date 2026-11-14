#!/usr/bin/env python3
"""C2: optimum rectangular fin (beta_opt, constant C, mass ratio, crossover conductivity); C3: embodied index for fins.
Spec rows C2, C3. Claims G1.5, G2.2, G2.3. Level: derived (unverified).
C2: maximise q'(t) = theta_b sqrt(2 h k t) tanh(A_p sqrt(2h/k) t^-1.5) over t at fixed A_p (minimize_scalar, in ln t), report beta=mL and
C in A_p = C (q'/theta_b)^3/(h^2 k). Mass ratio at equal duty is found independently: for each material solve A_p (brentq) such that max_t q' = target.
Crossover k_g = rho_g k_s/rho_s found by brentq on the numerically computed mass ratio. Published values: beta=1.4192, C=0.504 (Schmidt 1926; Kraus, Aziz, Welty 2001):
NOT confirmed from a source by this script (see issues_a.md for whether confirmed).
C3: ratio (e_g rho_g/k_g)/(e_s rho_s/k_s); break-even e_g/e_s from brentq on a sweep e_g/e_s in [0.2,10].
Inputs MEMORY: k_Cu 400, rho_Cu 8960, rho_Al 2700, rho_AlSi10Mg 2670; embodied e: MEMORY 200/55 and LOOKUP (data/a3_embodied_energy.csv: ICE v2.0; Nuss and Eckelman 2014 Table S38).
"""
import numpy as np
from scipy.optimize import minimize_scalar, brentq
kCu, rCu, rAl, rAS = 400.0, 8960.0, 2700.0, 2670.0
def qprime(t, h, Ap, k): return np.sqrt(2*h*k*t)*np.tanh(Ap*np.sqrt(2*h/k)*t**-1.5)   # per theta_b
def opt(h, Ap, k):
    f = lambda lt: -qprime(np.exp(lt), h, Ap, k)
    r = minimize_scalar(f, bounds=(np.log(1e-7), np.log(1.0)), method="bounded", options={"xatol": 1e-12})
    t = np.exp(r.x); return t, -r.fun
fails = 0
def chk(name, val, exp, tol, absolute=True):
    global fails
    ok = abs(val-exp) <= tol if absolute else abs(val/exp-1) <= tol; fails += (not ok)
    print(f"CHECK {name}: {val:.5f} vs {exp} tol={'+-'+str(tol) if absolute else str(tol*100)+'%'} -> {'PASS' if ok else 'FAIL'}")
print("INPUTS: k_Cu=400, rho_Cu=8960, rho_Al=2700, rho_AlSi10Mg=2670 (MEMORY); h in {10,50,1000}, A_p in {1e-6,1e-5,1e-4} m2; k in {400, 237, 200, 130}")
bm = []; Cm = []; hit = 0
for k in (400., 237., 200., 130.):
    for h in (10., 50., 1000.):
        for Ap in (1e-6, 1e-5, 1e-4):
            t, q = opt(h, Ap, k)
            if t < 1.0001e-7 or t > 0.9999: hit += 1
            beta = Ap*np.sqrt(2*h/k)*t**-1.5; C = Ap*h*h*k/q**3
            bm.append(beta); Cm.append(C)
bm = np.array(bm); Cm = np.array(Cm)
print(f"36 cases: beta_opt range {bm.min():.5f}..{bm.max():.5f}; C range {Cm.min():.5f}..{Cm.max():.5f}; optimum at bracket edge in {hit} cases")
beta_exact = brentq(lambda b: np.tanh(b) - 3*b/np.cosh(b)**2, 1.0, 2.0, xtol=1e-14)
print(f"stationarity root tanh(b)=3b sech^2(b) (brentq on [1,2]): {beta_exact:.6f}; C = b/(4 tanh^3 b) = {beta_exact/(4*np.tanh(beta_exact)**3):.6f}")
chk("beta_opt (all cases within 0.001 of 1.4192)", np.abs(bm-1.4192).max(), 0.0, 0.001)
chk("C (all cases within 0.002 of 0.504)", np.abs(Cm-0.504).max(), 0.0, 0.002)
# mass ratio independent: equal duty target
h = 50.0; target = 20.0   # q'/theta_b [W/(m K)]
def Ap_for(k, tg):
    g = lambda lAp: opt(h, np.exp(lAp), k)[1] - tg
    return np.exp(brentq(g, np.log(1e-9), np.log(1e-1), xtol=1e-12))
ApCu = Ap_for(kCu, target)
print(f"equal duty q'/theta_b = {target} W/(m K) at h=50: A_p,Cu = {ApCu:.4e} m2")
for kg in (200., 237., 130.):
    mr = rAl*Ap_for(kg, target)/(rCu*ApCu); form = (rAl/kg)/(rCu/kCu)
    print(f"  k_g={kg:5.0f}: numerical mass ratio {mr:.5f}; formula (rho_g/k_g)/(rho_s/k_s) = {form:.5f}")
    chk(f"mass ratio k_g={kg:.0f} numeric vs formula", mr, form, 0.005, False)
    if kg == 200: chk("mass ratio at k_g=200 vs spec 0.60", mr, 0.60, 0.02, False)
kgs = np.linspace(80, 240, 161)
mrs = np.array([(rAl*Ap_for(k, target))/(rCu*ApCu) - 1 for k in kgs[::8]])
print(f"mass-ratio sweep k_g in [80,240] (21 points, numerical): ratio-1 from {mrs[0]:+.3f} to {mrs[-1]:+.3f}; brackets the crossover: {mrs[0] > 0 > mrs[-1]}")
kx = brentq(lambda k: rAl*Ap_for(k, target)/(rCu*ApCu) - 1, 80, 240, xtol=1e-6)
print(f"numerical crossover k_g = {kx:.3f} W/(m K); formula rho_g k_s/rho_s = {rAl*kCu/rCu:.3f}; with rho=2670 (AlSi10Mg): {rAS*kCu/rCu:.3f}; spec ~120 +-2")
chk("crossover (numeric) vs formula", kx, rAl*kCu/rCu, 2.0)
chk("crossover vs spec ~120", kx, 120.0, 2.0)
print("\nC3: embodied index")
print("source LOOKUP: ICE v2.0 (Hammond and Jones 2011) and Nuss and Eckelman 2014 SI Table S38, see data/a3_embodied_energy.csv, access 2026-11-14")
def idx(eg, kg, rg, es=55e6): return (eg*rg/kg)/(es*rCu/kCu)
for kg in (200., 130.):
    r = np.logspace(np.log10(0.2), 1, 200)
    f = lambda x: (x*rAl/kg)/(rCu/kCu) - 1     # x = e_g/e_s
    sg = f(r); assert sg.min() < 0 < sg.max()
    be = brentq(f, 0.2, 10, xtol=1e-13)
    print(f"k_g={kg:.0f}: sweep e_g/e_s in [0.2,10] brackets break-even: True; break-even {be:.4f}; reciprocal of C2 mass ratio (formula) {1/((rAl/kg)/(rCu/kCu)):.4f}")
    chk(f"break-even vs reciprocal of C2 numeric mass ratio (k_g={kg:.0f})", be, 1.0/(rAl*Ap_for(kg, target)/(rCu*ApCu)), 0.02, False)
    if kg == 200: chk("break-even vs spec 1.66", be, 1.66, 0.02, False)
    if kg == 130: chk("break-even vs spec 1.08", be, 1.08, 0.02, False)
print("index with MEMORY e_Al=200, e_Cu=55 MJ/kg, k_g=200:", f"{idx(200e6,200,rAl):.4f}", "(spec ~2.2)")
chk("index vs 2.2", idx(200e6, 200, rAl), 2.2, 0.02, False)
print("  note: the 'index ~ 2.2' and break-even rows restate the same formula as the code (IDENTITY-like); the independent element is the numerical C2 mass ratio.")
print("LOOKUP evaluation (k_g=200 and 130; incumbent Cu with its own e):")
for name, ea, ec in (("ICE virgin/virgin", 218, 57), ("ICE recycled Al/virgin Cu", 29.0, 57), ("ICE recycled/recycled", 29.0, 16.5), ("Nuss primary/primary", 194, 59.3), ("Nuss old-scrap Al/primary Cu", 23.8, 59.3), ("Nuss secondary/secondary", 23.8, 28.1)):
    out = []
    for kg in (200., 130.):
        out.append((ea*1e6*rAl/kg)/(ec*1e6*rCu/kCu))
    print(f"  {name:32s} e_Al={ea:6.1f} e_Cu={ec:5.1f}  index k_g=200: {out[0]:.3f}  k_g=130: {out[1]:.3f}  (Al fin better in embodied terms if < 1)")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
