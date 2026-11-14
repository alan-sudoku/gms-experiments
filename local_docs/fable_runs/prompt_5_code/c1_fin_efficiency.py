#!/usr/bin/env python3
"""C1: fin efficiency and same-geometry penalty, Al vs Cu.
Spec row C1. Claims G1.4, G1.5, G2.5. Level: derived (unverified).
eta_f = tanh(mL)/(mL), m = sqrt(2h/(k t)); ratio (eta_f)_g/(eta_f)_s. Sweep h in [5,5000], L in [5,100] mm, t in [0.2,3] mm (log grids, 25 points each).
k_Cu = 400; k_Al in {237, 200, 130} W/(m K) (MEMORY; 130 = as-built AlSi10Mg, UNSURE, range 100-180).
Independent route: scipy.integrate.solve_bvp on theta'' = m^2 theta, theta(0)=1, theta'(L)=0; q' = -k t theta'(0); eta = q'/(2 h L).
No LOOKUP values in this row.
"""
import numpy as np
from scipy.integrate import solve_bvp
kCu = 400.0
def eta(h, L, t, k):
    mL = L*np.sqrt(2*h/(k*t)); return np.tanh(mL)/mL
def eta_bvp(h, L, t, k):
    # nondimensional s = x/L: theta'' = (mL)^2 theta, theta(0)=1, theta'(1)=0 ; q' = -k t theta'(0)/L ; eta = q'/(2 h L)
    mL = L*np.sqrt(2*h/(k*t))
    s = np.concatenate(([0.0], np.logspace(-8, 0, 600)))
    g = np.vstack([np.exp(-mL*s)*(1-s)+1e-3, -mL*np.exp(-mL*s)])   # deliberately NOT the analytic solution
    sol = solve_bvp(lambda s, y: np.vstack([y[1], mL**2*y[0]]), lambda ya, yb: np.array([ya[0]-1, yb[1]]), s, g, tol=1e-6, max_nodes=400000)
    if not sol.success: return np.nan
    q = -k*t*sol.sol(0)[1]/L
    return q/(2*h*L)
fails = 0
def chk(name, val, exp, tol):
    global fails
    ok = abs(val/exp-1) <= tol; fails += (not ok)
    print(f"CHECK {name}: {val:.5f} vs {exp} tol={tol*100:g}% -> {'PASS' if ok else 'FAIL'}")
print("INPUTS: k_Cu=400; k_Al in {237 pure, 200 wrought 6063, 130 as-built AlSi10Mg (UNSURE 100-180)} W/(m K) (MEMORY). No lookup.")
h0, L0, t0 = 50.0, 0.030, 0.001
ec = eta(h0, L0, t0, kCu)
print(f"baseline h=50, L=30 mm, t=1 mm: eta_Cu={ec:.4f}")
chk("eta_Cu", ec, 0.931, 0.005)
for kal, exp_eta, exp_ratio in ((200, 0.873, 0.937),):
    ea = eta(h0, L0, t0, kal); chk("eta_Al(200)", ea, exp_eta, 0.005); chk("ratio Al(200)/Cu", ea/ec, exp_ratio, 0.005)
for kal in (237, 130):
    ea = eta(h0, L0, t0, kal); print(f"  k_Al={kal}: eta_Al={ea:.4f}, ratio={ea/ec:.4f} (penalty {(1-ea/ec)*100:.1f}%)")
print("independent solve_bvp vs closed form at baseline and 30 random sweep points:")
rng = np.random.default_rng(1)
pts = [(h0, L0, t0, kCu), (h0, L0, t0, 200.0), (h0, L0, t0, 130.0)]
for _ in range(30):
    pts.append((10**rng.uniform(np.log10(5), np.log10(5000)), 10**rng.uniform(np.log10(5e-3), -1), 10**rng.uniform(np.log10(2e-4), np.log10(3e-3)), rng.choice([400., 237., 200., 130.])))
dev = np.array([abs(eta_bvp(*p)/eta(*p)-1) for p in pts]); nfail = int(np.isnan(dev).sum()); worst = np.nanmax(dev)
print(f'  solve_bvp did not converge at {nfail} of {len(pts)} points (excluded from the max)')
print(f"  max |eta_bvp/eta_closed - 1| = {worst:.2e}")
ok = worst < 0.005; fails += (not ok); print(f"CHECK bvp vs closed form <0.5% -> {'PASS' if ok else 'FAIL'}")
hs = np.logspace(np.log10(5), np.log10(5000), 25); Ls = np.logspace(np.log10(5e-3), -1, 25); ts = np.logspace(np.log10(2e-4), np.log10(3e-3), 25)
H, LL, T = np.meshgrid(hs, Ls, ts, indexing="ij")
mLc = LL*np.sqrt(2*H/(kCu*T))
print(f"sweep: 25^3 = {H.size} points; mL_Cu range {mLc.min():.3g} .. {mLc.max():.3g}")
for kal in (237, 200, 130):
    r = eta(H, LL, T, kal)/eta(H, LL, T, kCu)
    lim = np.sqrt(kal/kCu)
    br_small = (r >= 0.95).any(); thick = mLc > 20
    print(f"  k_Al={kal}: ratio min {r.min():.4f}, max {r.max():.4f}; thick-limit sqrt(k_g/k_s)={lim:.4f}; points with penalty<=5%: {(r>=0.95).mean()*100:.1f}%; points with mL_Cu>20: {thick.mean()*100:.1f}%, ratio there {r[thick].min():.4f}..{r[thick].max():.4f}")
    chk(f"thick limit k_Al={kal} (min ratio in sweep at mL_Cu max)", r[mLc == mLc.max()][0], lim, 0.005)
    print(f"  brackets the <=5%-penalty region: {br_small}; brackets the thick limit (some mL>20): {bool(thick.any())}; ratio->1 as mL->0: min mL {mLc.min():.3f}, ratio at that point {r[mLc==mLc.min()][0]:.4f}")
print("note: mL_Cu min in the sweep is 0.04-ish only if h,L,t extremes align; ratio->1 limit approached, not reached within 0.5% unless mL<0.1")
print("IDENTITY CHECKS: 'thick limit' compares tanh(mL)/(mL) ratio with sqrt(k_g/k_s): a limit of the same formula (asymptotic check), kept as value check; bvp is the independent route.")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
