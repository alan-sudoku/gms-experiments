#!/usr/bin/env python3
"""Row F5 (claims G1.1, G1.8, G3.4): non-uniform shield at equal mean areal density (Jensen).

No LOOKUP. a = mu*xbar in [0.1, 10], 200 log-spaced points + the points 0.1, 1, 5, 10.
(a) x uniform on [0, 2 xbar]: E = (1 - exp(-2a))/(2a) analytic; checked against scipy.integrate.quad (1e-9) and a
    Monte Carlo with 1e6 samples (fixed seed 20261114), 3 sigma.
(b) two-level: fraction q of the area at xbar/q, rest open (x = 0): E = q*exp(-a/q) + (1-q), q in {0.5, 0.8, 0.95};
    Monte Carlo 1e6 samples, 3 sigma. (Mean areal density is q*(xbar/q) = xbar for every q.)
Ratio R = E[exp(-mu x)]/exp(-mu xbar) must be >= 1 everywhere (Jensen). Level `derived`.
"""
import numpy as np
from scipy.integrate import quad
SEED=20261114; N=1_000_000; FAILS=[]
rng=np.random.default_rng(SEED)
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
a_grid=np.unique(np.concatenate([np.logspace(-1,1,200),[0.1,1,5,10]]))
print("F5 inputs: seed=%d, N=%d samples per (case, a); a grid: %d points in [0.1, 10]" % (SEED,N,len(a_grid)))
# (a)
analytic=lambda a:(1-np.exp(-2*a))/(2*a)
worst_q=0; mc_fail=0; minR=1e9
u_a=rng.random(N)   # x/(2 xbar) uniform [0,1]
for a in a_grid:
    A=analytic(a); qi,_=quad(lambda t:np.exp(-a*t),0,2,epsabs=1e-13,epsrel=1e-13); q=qi/2
    worst_q=max(worst_q,abs(A-q))
    s=np.exp(-2*a*u_a); m=s.mean(); se=s.std(ddof=1)/np.sqrt(N)
    if abs(m-A)>3*se: mc_fail+=1
    minR=min(minR,A/np.exp(-a))
print("\n(a) uniform on [0, 2 xbar]")
check("analytic vs quad to 1e-9 over the sweep (independent: closed form vs numerical integral)", worst_q<1e-9, "max |diff| = %.2e" % worst_q)
print("  MC vs analytic outside 3 sigma at %d of %d sweep points (expected by chance ~0.27%% -> %.1f)" % (mc_fail,len(a_grid),0.0027*len(a_grid)))
check("MC agrees with analytic within 3 sigma at (nearly) all points (allow at most 2 chance excursions)", mc_fail<=2, "%d excursions" % mc_fail)
check("ratio >= 1 at every a", minR>=1.0, "min ratio = %.6f" % minR)
a=5.0; A=analytic(a)
print("  at a=5: E = %.5f, exp(-a) = %.5e, ratio = %.3f (plan: 0.100, 6.7e-3, ~15)" % (A,np.exp(-a),A/np.exp(-a)))
check("a=5 values 0.100 and 6.7e-3", abs(A-0.100)<5e-4 and abs(np.exp(-a)-6.7e-3)<5e-5, "%.5f, %.3e" % (A,np.exp(-a)))
s=np.exp(-2*a*u_a); print("  MC at a=5: %.5f +- %.5f" % (s.mean(), s.std(ddof=1)/np.sqrt(N)))
# (b)
for q in (0.5,0.8,0.95):
    mcf=0; minR=1e9; 
    cov=rng.random(N)<q          # fraction q covered at xbar/q
    for a in a_grid:
        A=q*np.exp(-a/q)+(1-q)
        s=np.where(cov,np.exp(-a/q),1.0); m=s.mean(); se=s.std(ddof=1)/np.sqrt(N)
        if abs(m-A)>3*se+1e-15: mcf+=1
        minR=min(minR,A/np.exp(-a))
    print("\n(b) two-level q=%.2f (x = xbar/q on fraction q, open elsewhere)" % q)
    print("  MC vs formula outside 3 sigma at %d of %d points (chance ~%.1f)" % (mcf,len(a_grid),0.0027*len(a_grid)))
    check("q=%.2f MC agrees (<=2 chance excursions)" % q, mcf<=2, "%d" % mcf)
    check("q=%.2f ratio >= 1 at every a" % q, minR>=1.0, "min ratio = %.6f (at a=%.3g the minimum of the sweep)" % (minR, a_grid[0]))
    a=5.0; A=q*np.exp(-a/q)+(1-q); print("  at a=5: E=%.5e, ratio=%.4g" % (A, A/np.exp(-a)))
print("\nNotes: (1) the ratio >= 1 outcome is Jensen's inequality; the check is numerical (Monte Carlo and quadrature are independent of the closed forms), not an identity.")
print("(3) The same sample set is reused across the a-grid, so the excursion counts are correlated; the count is a rough guide only.")
print("(2) For two-level at fixed q the MC sample mean of exp(-mu x) uses the exact two values, so MC variance reflects only the coverage Bernoulli draw.")
print("FAILED CHECKS:", FAILS if FAILS else "none")
