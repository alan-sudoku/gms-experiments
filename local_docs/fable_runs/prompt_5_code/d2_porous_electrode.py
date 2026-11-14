#!/usr/bin/env python3
"""D2: porous-electrode utilisation and thick-limit exponent.
Spec row D2. Claims G1.4, G1.7, G2.9. Level: derived (unverified).
eta_u = tanh(L/lam)/(L/lam), lam = sqrt(sigma_ion,eff R T/(a j0 F)), j0,eff = j0 a lam tanh(L/lam).
Sweep j0 in [1e-3,1e2] A/m2, L in [1e-6,3e-3] m, a in [1e4,1e8] m2/m3 (25 log points each). T = 353.15 K.
LOOKUP: bulk 30 wt% KOH at 80 C from Gilliam et al. 2007 correlation (data/d2_koh_conductivity.csv; PARTIALLY confirmed, see data file),
times porosity^1.5, porosity 0.5-0.9.
Independent route: finite differences on phi'' = phi/lam^2, phi(0)=1, phi'(L)=0, j0,eff = -(sigma R T/F) phi'(0), graded mesh, N=4001.
"""
import numpy as np
from scipy.linalg import solve_banded
R, F, T = 8.314462, 96485.332, 353.15
def gilliam_Spcm(M, T):
    return -2.041*M - 0.0028*M**2 + 0.005332*M*T + 207.2*M/T + 0.001043*M**3 - 3e-7*M**2*T**2
print("INPUTS: T=353.15 K, R=8.314462, F=96485.332")
print("LOOKUP SOURCE: Gilliam, Graydon, Kirk, Thorpe 2007, Int. J. Hydrogen Energy 32, 359-364; correlation as quoted by citing works (secondary), accessed 2026-11-14; see data/d2_koh_conductivity.csv")
chk = gilliam_Spcm(0.01, 298.15)*1e3
print(f"consistency check of the quoted form: M=0.01, 298.15 K -> {chk:.3f} mS/cm (ACS SI quotes the equation giving 2.43 mS/cm): {'agrees' if abs(chk-2.43) < 0.03 else 'DISAGREES'}")
fails = 0
sig = {}
for M in (6.7, 6.89):
    s = gilliam_Spcm(M, T)*100
    sig[M] = s
    print(f"  30 wt% KOH, M={M}: sigma(353.15 K) = {s:.1f} S/m ; planner UNSURE range 120-150 S/m: {'inside' if 120 <= s <= 150 else 'OUTSIDE'}")
sig0 = sig[6.89]
print("  (value at 80 C of 30 wt% is 'by correlation'; M at 80 C depends on density; see data file)")
for eps in (0.5, 0.7, 0.9): print(f"  sigma_eff = sigma*eps^1.5: eps={eps}: {sig0*eps**1.5:.1f} S/m")
sg = sig0*0.7**1.5
print(f"central: sigma_eff = {sg:.1f} S/m (M=6.89, eps=0.7)")
def lam(j0, a, s=sg): return np.sqrt(s*R*T/(a*j0*F))
def j0eff(j0, a, L, s=sg): l = lam(j0, a, s); return j0*a*l*np.tanh(L/l)
def j0eff_fd(j0, a, L, s=sg, N=4001):
    l = lam(j0, a, s); s_ = np.linspace(0, 1, N)**2*L   # graded towards x=0
    # nonuniform FD for phi'' = phi/l^2 ; unknowns phi_1..phi_{N-1}, phi_0=1, Neumann at end by ghost point
    x = s_; n = N
    A = np.zeros((3, n-1)); rhs = np.zeros(n-1)
    for k in range(1, n):
        hm = x[k]-x[k-1]; hp = (x[k+1]-x[k]) if k < n-1 else hm   # ghost: phi_{n}=phi_{n-2}
        c_m = 2/(hm*(hm+hp)); c_p = 2/(hp*(hm+hp)); c_0 = -(c_m + c_p) - 1/l**2
        i = k-1
        A[1, i] = c_0
        if k > 1: A[2, i-1] = c_m
        else: rhs[i] -= c_m*1.0
        if k < n-1: A[0, i+1] = c_p
        else: A[2, i-1] = c_m + c_p
    phi = np.concatenate(([1.0], solve_banded((1, 1), A, rhs)))
    # -phi'(0) = (1/lam^2) * int phi dx (from phi''=phi/lam^2 and phi'(L)=0): flux balance, avoids a one-sided derivative on the graded mesh
    d0 = -np.trapezoid(phi, x)/l**2
    return -(s*R*T/F)*d0
j0g = np.logspace(-3, 2, 25); Lg = np.logspace(-6, np.log10(3e-3), 25); ag = np.logspace(4, 8, 25)
J, LL, AA = np.meshgrid(j0g, Lg, ag, indexing="ij")
x_ = LL/lam(J, AA)
print(f"sweep: 25^3 points; L/lambda range {x_.min():.2e} .. {x_.max():.1f}; brackets L/lam << 1 and >> 1: {x_.min() < 0.01 and x_.max() > 10}")
eta_u = np.tanh(x_)/x_
print(f"eta_u range {eta_u.min():.4f} .. {eta_u.max():.6f}; thin limit j0,eff -> j0 a L, thick limit -> sqrt(a j0 sigma R T/F)")
thin = x_ < 0.01; thick = x_ > 5
print(f"  max |j0eff/(j0 a L) - 1| for L/lam<0.01: {np.abs(J*AA*LL/ (J*AA*lam(J,AA)*np.tanh(x_))-1)[thin].max():.2e}; thick: max |j0eff/sqrt(a j0 sigma RT/F) - 1| for L/lam>5: {np.abs(J*AA*lam(J,AA)*np.tanh(x_)/np.sqrt(AA*J*sg*R*T/F)-1)[thick].max():.2e}")
print("  (thin and thick limits are the same closed form evaluated in two regimes: IDENTITY-like)")
# slopes
print("slope dln(j0,eff)/dln(j0) vs j0 at L=3e-3 m, a=1e7 m2/m3 (central sigma_eff):")
j0s = np.logspace(-3, 2, 51); y = np.log(j0eff(j0s, 1e7, 3e-3)); sl = np.gradient(y, np.log(j0s))
for i in range(0, 51, 10): print(f"   j0={j0s[i]:9.3g}  L/lam={3e-3/lam(j0s[i],1e7):9.3g}  slope={sl[i]:.4f}")
thick_mask = 3e-3/lam(j0s, 1e7) > 5
print(f"  thick-limit slope (L/lam>5): {sl[thick_mask].min():.5f}..{sl[thick_mask].max():.5f}")
ok = np.abs(sl[thick_mask]-0.5).max() < 0.01; fails += (not ok)
print(f"CHECK thick-limit slope 0.500 +-0.01 -> {'PASS' if ok else 'FAIL'}")
# FD route slope too
ly = np.array([np.log(j0eff_fd(j, 1e7, 3e-3)) for j in j0s]); slf = np.gradient(ly, np.log(j0s))
print(f"  FD route thick-limit slope: {slf[thick_mask].min():.5f}..{slf[thick_mask].max():.5f}")
ok = np.abs(slf[thick_mask]-0.5).max() < 0.01; fails += (not ok); print(f"CHECK FD thick slope 0.500 +-0.01 -> {'PASS' if ok else 'FAIL'}")
rng = np.random.default_rng(2); worst = 0
for _ in range(40):
    j, a, L = 10**rng.uniform(-3, 2), 10**rng.uniform(4, 8), 10**rng.uniform(-6, np.log10(3e-3))
    worst = max(worst, abs(j0eff_fd(j, a, L)/j0eff(j, a, L)-1))
print(f"FD vs closed form j0,eff on 40 random sweep points: max rel. deviation {worst:.2e}")
ok = worst < 0.01; fails += (not ok); print(f"CHECK FD vs closed form within 1% -> {'PASS' if ok else 'FAIL'}")
print("metal-foam a = 5e3-1e4 m2/m3 (MEMORY UNSURE) is at or below the lower edge of the swept a range [1e4,1e8]; with a=5e3, j0=1e-3..1e2: L/lam from", f"{3e-3/lam(1e-3,5e3):.3f} to {3e-3/lam(1e2,5e3):.2f}")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
