"""B1, B2: Miner sum versus minimum life for sequential load cases.

Spec rows B1 (two cases, deterministic sweep) and B2 (L cases, Monte Carlo).
B1: tau_l = N_l/nu_l, N = 0.5 (sigma/sigma_f')^(1/b) (Basquin as in plan 3.2), R = tau_min (1/tau1 + 1/tau2).
    s = sigma2/sigma1 in [0.25,1.4] step 0.005; phi = nu2/nu1 in {10,100,1000}.  s* by bisection on
    ln tau1 - ln tau2; window edges R >= 1.1 by bisection on each side of s*.
    R = 2 at s* holds by construction (flagged identity).
B2: sigma_l = sigma_ref exp(U_l), U uniform [-w,w], equal nu, R = tau_min sum 1/tau_l, 1e5 samples,
    rng = default_rng(20261115), m = 9.804 (M03).  Standard errors: SE(mean) = sd/sqrt(n);
    SE(median) by a full-sample bootstrap of 100 resamples.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from p6_common import bisect, tag, SEED
from rainflow_util import SIGMA_A0, basquin_N, B, SF

m = -1 / B
print(f"sigma_a0 (C1) = {SIGMA_A0:.4f} MPa, m = {m:.5f}")
def lntau(sig, nu):
    return np.log(float(basquin_N(sig)) / nu)

print("=== B1 ===")
s_grid = np.round(np.arange(0.25, 1.4 + 1e-9, 0.005), 6)
for phi in [10, 100, 1000]:
    s1 = SIGMA_A0
    def Rof(s):
        t1 = np.exp(lntau(s1, 1.0)); t2 = np.exp(lntau(s * s1, float(phi)))
        return min(t1, t2) * (1 / t1 + 1 / t2)
    Rv = np.array([Rof(s) for s in s_grid])
    ok_range = bool(np.all((Rv >= 1 - 1e-12) & (Rv <= 2 + 1e-12)))
    g = lambda s: lntau(s1, 1.0) - lntau(s * s1, float(phi))
    r = bisect(g, 0.25, 1.4)
    sst = r['root']
    ana = phi ** (-1 / m)
    print(f"phi={phi}: g ends=({r['flo']:.3f},{r['fhi']:.3f}) bracketed={r['bracketed']} s*={sst:.5f} (phi^(-1/m)={ana:.5f}) "
          f"R(s*)={Rof(sst):.6f} [identity: R=2 at s* by construction]")
    print(f"   1<=R<=2 at all {len(s_grid)} grid points: min R={Rv.min():.6f} max R={Rv.max():.6f} {tag(ok_range)}")
    h = lambda s: Rof(s) - 1.1
    hi = bisect(h, sst, 1.4)
    lo = bisect(h, 0.25, sst)
    for nm, rr in [('lower', lo), ('upper', hi)]:
        print(f"   {nm} edge: end values h=({rr['flo']:.4f},{rr['fhi']:.4f}) bracketed={rr['bracketed']} root={rr['root']:.5f}")
    print(f"   edges s/s* = {lo['root']/sst:.4f}, {hi['root']/sst:.4f} (hand 0.791, 1.265); inside sweep [0.25,1.4]: "
          f"{0.25 < lo['root'] and hi['root'] < 1.4}; "
          f"{tag(abs(lo['root']/sst-0.791)/0.791<0.01 and abs(hi['root']/sst-1.265)/1.265<0.01)}")
    print(f"   s* hand check: {tag(abs(sst-{10:0.791,100:0.625,1000:0.494}[phi])/{10:0.791,100:0.625,1000:0.494}[phi]<0.01)}")

print("\n=== B2 ===")
rng = np.random.default_rng(SEED)
n = 100000
for L in [2, 5, 10, 20]:
    for w in [0.05, 0.1, 0.2]:
        U = rng.uniform(-w, w, size=(n, L))
        a = np.exp(m * U)                 # 1/tau_l up to a common factor
        R = a.sum(axis=1) / a.max(axis=1)
        okb = bool(np.all((R >= 1 - 1e-12) & (R <= L + 1e-12)))
        med = np.median(R); p95 = np.percentile(R, 95)
        se_mean = R.std(ddof=1) / np.sqrt(n)
        bs = [np.median(rng.choice(R, size=n, replace=True)) for _ in range(100)]
        se_med = np.std(bs, ddof=1)
        print(f"L={L:2d} w={w}: median={med:.4f} p95={p95:.4f} mean={R.mean():.4f} min={R.min():.4f} max={R.max():.4f} "
              f"1<=R<=L {tag(okb)} | SE(mean)/mean={se_mean/R.mean():.2e} SE(median)/median={se_med/med:.2e} "
              f"{tag(max(se_mean/R.mean(), se_med/med)<0.01)}")
        if L == 5 and w == 0.1:
            print(f"   B2 plausibility L=5,w=0.1: median {med:.3f} in [1.5,3]: {tag(1.5<=med<=3)}")
