"""A11: hysteresis under two concurrent load cases versus the separate-case sum.

Spec row A11 (plan 3.3; formulas of 2.3).  Uses rainflow_util.rainflow (B5 routine, plan 3.2).
(a) Linear viscoelastic: sigma = s1 sin(w1 t) + s2 sin(phi w1 t); eps = sum (s_l/E) sin(w_l t - delta);
    mean power = trapezoid mean of sigma * d(eps)/dt over one common period (1/nu1 = 1 s for integer phi),
    4096 points per fast period, versus sum_l w_l s_l^2 sin(delta)/(2E); tan(delta) = 1e-3; E = 73 GPa (M05).
    Ratio to the separate-case sum; phi = 1 (same frequency, in phase) ratio (1+s)^2/(1+s^2) expected.
(b) Rate-independent: rainflow cycles of the combined history, dissipation sum_k sigma_a,k^n per
    slow period versus s1^n + phi s2^n; idealised ratio [(1+s)^n + (phi-1) s^n]/(1 + phi s^n);
    upper bound of 2.3: phi (1+s)^n/(1 + phi s^n).  Sampling 256 and 512 points per fast period,
    (also 1024) change on doubling checked < 0.5 %.  Real test: upper bound >= rainflow ratio.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from p6_common import tag
from rainflow_util import rainflow

E = 73e3        # MPa (M05 73 GPa)
S1 = 100.0      # MPa
delta = np.arctan(1e-3)
fails = 0

print("=== A11 (a) linear viscoelastic ===")
for phi in [1, 3, 9, 33]:
    for s in [0.1, 1 / 3, 1.0]:
        npf = 4096
        n = npf * phi                 # points over one common period of 1 s (phi fast periods)
        t = np.linspace(0, 1.0, n + 1)  # trapezoid incl. both end points
        w1 = 2 * np.pi
        if phi == 1:
            # same frequency, in phase: two load cases act together
            sig = S1 * np.sin(w1 * t) + s * S1 * np.sin(w1 * t)
            epsdot = (S1 * w1 / E) * np.cos(w1 * t - delta) + (s * S1 * w1 / E) * np.cos(w1 * t - delta)
        else:
            w2 = phi * w1
            sig = S1 * np.sin(w1 * t) + s * S1 * np.sin(w2 * t)
            epsdot = (S1 * w1 / E) * np.cos(w1 * t - delta) + (s * S1 * w2 / E) * np.cos(w2 * t - delta)
        p = sig * epsdot
        mean = np.trapz(p, t) / 1.0 if hasattr(np, 'trapz') else np.trapezoid(p, t) / 1.0
        sep = (w1 * S1 ** 2 + phi * w1 * (s * S1) ** 2) * np.sin(delta) / (2 * E)
        ratio = mean / sep
        exp = (1 + s) ** 2 / (1 + s ** 2) if phi == 1 else 1.0
        ok = abs(ratio - exp) < 1e-6
        fails += not ok
        print(f"phi={phi:2d} s={s:.4f}: mean power={mean:.6e} separate sum={sep:.6e} ratio={ratio:.9f} expected {exp:.6f} {tag(ok)}")
print("A11(a) note: for phi != 1 the check is trigonometric orthogonality (numerical trapezoid vs algebraic sum), "
      "tests the algebra of 2.3, not an independent physical model.")

print("\n=== A11 (b) rate-independent ===")
def history(s, phi, npts):
    N = phi * npts
    t = np.arange(N) / N
    return S1 * np.sin(2 * np.pi * t) + s * S1 * np.sin(2 * np.pi * phi * t)

def diss(s, phi, npts, n):
    cyc, res, st = rainflow(history(s, phi, npts))
    return sum((0.5 * c[0]) ** n for c in cyc), len(cyc), len(res)

worst_ub = 1e9; worst_dev = 0
for n in [2, 3]:
    for phi in [1, 3, 9, 33]:
        for s in [0.1, 1 / 3, 1.0]:
            sep = S1 ** n + phi * (s * S1) ** n
            ideal = ((1 + s) ** n + (phi - 1) * s ** n) / (1 + phi * s ** n)
            ub = phi * (1 + s) ** n / (1 + phi * s ** n)
            vals = {}
            for npts in [256, 512, 1024]:
                d, nc, nres = diss(s, phi, npts, n)
                vals[npts] = (d / sep, nc, nres)
            r512 = vals[512][0]
            ch = abs(vals[512][0] - vals[256][0]) / vals[512][0]
            ch2 = abs(vals[1024][0] - vals[512][0]) / vals[1024][0]
            dev = (r512 - ideal) / ideal
            ok_ub = ub >= r512 * (1 - 1e-12)
            worst_ub = min(worst_ub, ub / r512)
            worst_dev = max(worst_dev, abs(dev))
            fails += (not ok_ub) or ch > 5e-3 or ch2 > 5e-3
            print(f"n={n} phi={phi:2d} s={s:.4f}: rainflow ratio(256/512/1024)={vals[256][0]:.4f}/{vals[512][0]:.4f}/{vals[1024][0]:.4f} "
                  f"cycles={vals[512][1]} residue={vals[512][2]} ideal={ideal:.4f} dev={dev:+.3%} {'within10%' if abs(dev)<0.10 else 'OUTSIDE10%'} "
                  f"upper bound={ub:.4f} UB>=RF {tag(ok_ub)} | change on doubling 256->512 {ch:.1e}, 512->1024 {ch2:.1e} {tag(max(ch,ch2)<5e-3)}")
print(f"A11(b) minimum UB/rainflow over all cases = {worst_ub:.4f}; max |deviation from idealised ratio| = {worst_dev:.3%}")
# hand values
for (n, s, phi, h, lab) in [(2, 1/3, 9, 1.33, 'n=2 s=1/3 phi=9'), (2, 0.1, 9, 1.18, 'n=2 s=0.1 phi=9'), (3, 1/3, 9, 2.0, 'n=3 s=1/3 phi=9')]:
    sep = S1 ** n + phi * (s * S1) ** n
    d, nc, nr = diss(s, phi, 512, n)
    r = d / sep
    ideal = ((1 + s) ** n + (phi - 1) * s ** n) / (1 + phi * s ** n)
    print(f"A11 hand {lab}: hand about {h}; rainflow {r:.4f}; idealised {ideal:.4f} (plausibility, +-5% {tag(abs(r-h)/h<0.05)})")
print(f"TOTAL non-passing A11 checks: {fails}")
