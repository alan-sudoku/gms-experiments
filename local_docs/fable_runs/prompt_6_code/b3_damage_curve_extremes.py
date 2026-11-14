"""B3: extremes of the Miner sum at failure for two-level loading, damage-curve approach.

Spec row B3.  f(u) = u + 1 - u^a, a = (N1/N2)^0.4 (M14).  Coarse grid u in [1e-4, 1-1e-4]
(log-ish + linear mix), check the extremum is interior, golden-section to 1e-10,
compare with u* = a^(1/(1-a)).  Minima expected for N1/N2 < 1 (high then low), maxima for > 1.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from p6_common import golden_max, golden_min, tag

hand = {1e-3: (0.222, 0.052), 1e-2: (0.405, 0.112), 1e-1: (0.673, 0.217),
        10: (1.327, 0.544), 100: (1.595, 0.707), 1000: (1.778, 0.830)}
for r, (hv, hu) in hand.items():
    a = r ** 0.4
    f = lambda u: u + 1 - u ** a
    grid = np.unique(np.concatenate((np.linspace(1e-4, 1 - 1e-4, 20001), np.geomspace(1e-4, 0.5, 2000))))
    v = f(grid)
    if a < 1:
        i = int(np.argmin(v)); kind = 'min'
    else:
        i = int(np.argmax(v)); kind = 'max'
    interior = 0 < i < len(grid) - 1
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    if kind == 'min':
        u, fv = golden_min(f, lo, hi, 1e-10)
    else:
        u, fv = golden_max(f, lo, hi, 1e-10)
    ustar = a ** (1 / (1 - a))
    # note: golden-section on a flat extremum limits u accuracy to ~sqrt(machine eps); compare u and f
    ok = abs(u - ustar) < 1e-6 and abs(fv - (ustar + 1 - ustar ** a)) < 1e-12
    okh = abs(fv - hv) <= 0.005 and abs(u - hu) <= 0.005
    print(f"N1/N2={r:g}: a={a:.5f} {kind} grid u={grid[i]:.5f} interior={interior}; golden u={u:.8f} f={fv:.8f}; "
          f"analytic u*={ustar:.8f} f*={ustar+1-ustar**a:.8f} |du|={abs(u-ustar):.1e} {tag(ok)}; "
          f"hand (f={hv}, u={hu}) {tag(okh)}")
