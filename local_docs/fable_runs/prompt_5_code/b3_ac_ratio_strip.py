#!/usr/bin/env python3
"""B3: same-geometry R_ac ratio Al/Cu against thickness; utilisation eta_u = 1/F.
Spec row B3. Claims G1.4, G2.1, G2.9. Level: derived (unverified).
Isolated strip, field on both faces: R_ac/R_dc = F(t/(2 delta)), F(xi) = xi (sinh2xi+sin2xi)/(cosh2xi-cos2xi).
Sweep t/delta_Cu in [0.05,50] (log, 200 points) at 50 Hz. Output R_ac,Al/R_ac,Cu = (sigma_Cu/sigma_Al) F(xi_Al)/F(xi_Cu), eta_u = 1/F.
Independent route: finite differences E'' = j omega mu0 sigma E on [-t/2,t/2] (x in units of delta -> E'' = 2j E),
E=1 at both faces, >=2001 nodes, complex banded solve (scipy.linalg.solve_banded); loss P = int sigma|E|^2/2, I = int sigma E,
R_ac = 2P/|I|^2, R_dc = 1/(sigma t); ratio = t int|E|^2 / |int E|^2 (trapezoid).
sigma_Cu 5.80e7, sigma_Al 3.54e7 S/m (MEMORY).
"""
import numpy as np
from scipy.linalg import solve_banded
mu0 = 1.25663706e-6; sCu, sAl = 5.80e7, 3.54e7; f = 50.0
dCu = np.sqrt(2/(2*np.pi*f*mu0*sCu)); dAl = np.sqrt(2/(2*np.pi*f*mu0*sAl))
def F(x): return x*(np.sinh(2*x)+np.sin(2*x))/(np.cosh(2*x)-np.cos(2*x))
def Ffd(xi):
    # slab thickness t = 2*xi*delta ; coordinate in delta units, half width xi
    n = max(2001, int(60*2*xi)) | 1
    x = np.linspace(-xi, xi, n); h = x[1]-x[0]
    m = n-2
    ab = np.zeros((3, m), dtype=complex)
    ab[0, 1:] = 1.0/h**2; ab[2, :-1] = 1.0/h**2; ab[1, :] = -2.0/h**2 - 2j
    rhs = np.zeros(m, dtype=complex); rhs[0] = -1.0/h**2; rhs[-1] = -1.0/h**2
    E = np.concatenate(([1.0], solve_banded((1, 1), ab, rhs), [1.0]))
    return (2*xi)*np.trapezoid(abs(E)**2, x)/abs(np.trapezoid(E, x))**2
tr = np.logspace(np.log10(0.05), np.log10(50), 200)
xi_cu = tr/2; xi_al = tr*dCu/dAl/2
Fc, Fa = F(xi_cu), F(xi_al)
ratio = (sCu/sAl)*Fa/Fc
print("INPUTS: f=50 Hz, sigma_Cu=5.80e7, sigma_Al=3.54e7 S/m (MEMORY); delta_Cu=%.4f mm, delta_Al=%.4f mm" % (dCu*1e3, dAl*1e3))
print("sweep t/delta_Cu in [0.05,50], 200 log points")
print(" t/delta_Cu   R_ac,Al/R_ac,Cu   eta_u,Cu   eta_u,Al")
for i in range(0, 200, 20): print(f"{tr[i]:10.4f} {ratio[i]:15.5f} {1/Fc[i]:10.4f} {1/Fa[i]:10.4f}")
print(f"{tr[-1]:10.4f} {ratio[-1]:15.5f} {1/Fc[-1]:10.4f} {1/Fa[-1]:10.4f}")
fails = 0
def chk(name, val, exp, tol):
    global fails
    ok = abs(val/exp-1) <= tol; fails += (not ok)
    print(f"CHECK {name}: {val:.5f} vs {exp:.5f} tol={tol*100:g}% -> {'PASS' if ok else 'FAIL'}")
print(f"sweep range of ratio: {ratio.min():.4f} .. {ratio.max():.4f}; it spans thin limit 1.638 and thick limit 1.280: {ratio[0] > 1.6 and ratio[-1] < 1.3} (sweep brackets the transition: {ratio[0] > 1.638*0.99 and ratio[-1] < 1.28*1.01})")
chk("thin limit", ratio[0], 1.638, 0.01); chk("thick limit", ratio[-1], 1.280, 0.01)
print("   (non-monotonic? max ratio %.4f at t/delta_Cu=%.3f, min %.4f at %.3f)" % (ratio.max(), tr[ratio.argmax()], ratio.min(), tr[ratio.argmin()]))
print("FD (independent) vs closed form F:")
worst = 0
for t_ in tr[::10]:
    for xi in (t_/2, t_*dCu/dAl/2):
        a, b = Ffd(xi), F(xi); worst = max(worst, abs(a/b-1))
print(f"  max |F_fd/F_closed - 1| over 20 thicknesses x 2 metals = {worst:.2e}")
ok = worst < 0.01; fails += (not ok); print(f"CHECK FD vs closed form <1% -> {'PASS' if ok else 'FAIL'}")
rfd = np.array([(sCu/sAl)*Ffd(t_*dCu/dAl/2)/Ffd(t_/2) for t_ in tr[::10]])
print(f"  FD ratio max deviation vs closed-form ratio at same points: {np.abs(rfd/ratio[::10]-1).max():.2e}")
print("IDENTITY CHECKS: none (FD solves the PDE, closed form is the analytic solution).")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
