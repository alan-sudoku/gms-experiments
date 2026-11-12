"""A2 test of the homogenisation: explicit parallel-strand bundles vs the homogenised bar.

What it computes
    R' of a bundle of square Al strands on a square pitch filling the 10 x 100 mm
    envelope (metal fraction 0.3, 0.6, 0.85), every strand resolved with sub-cells,
    all strands connected in parallel (same voltage drop per metre), NOT transposed.
    Compared with the homogenised bar sigma_eff = fill*sigma_Al, solid Al and solid Cu.
    This is the most favourable geometry for Claim A: all metal runs along the
    current (tortuosity 1) and strands are perfectly insulated from one another.
    Also prints a sub-cell resolution check and the difference between 1x1 and 2x2
    sub-cells (strand-level proximity loss).

Which answer items it supports
    A2.1 (homogenised model verified), A2.2 (where homogenisation breaks down),
    A2.3 (no regime beats solid Al or solid Cu), A1.4 (strut-level proximity loss).

Assumptions
    As eddy2d.py.  z-invariant: there are no transverse struts or nodes, which in a
    real 3-D lattice only remove axial metal (lower sigma_eff).

Usage
    python3 a2_strand_bundle_scan.py            # full default scan (about 6 minutes)
    python3 a2_strand_bundle_scan.py quick      # 10 kHz, fill 0.3 only (about 1 minute)
"""
import math
import sys

from eddy2d import S_AL, S_CU, delta, solid_bar, solve, strand_array

a, b = 50e-3, 5e-3


def scan(f, nys, fills, res):
    d = delta(S_AL, f)
    rcu = solve(solid_bar(a, b, S_CU, f, 2), f)["R"]
    ral = solve(solid_bar(a, b, S_AL, f, 2), f)["R"]
    print(f"\nf={f:.0f} Hz  delta_Al={d*1e3:.4f} mm  solid Cu {rcu*1e6:.2f}  solid Al {ral*1e6:.2f} uOhm/m"
          f"   (sub-cells <= {res} delta)", flush=True)
    for fill in fills:
        rh = solve(solid_bar(a, b, fill * S_AL, f, 2), f)["R"]
        print(f" fill={fill:.2f}: homogenised bar sigma_eff=fill*sAl -> {rh*1e6:.2f} uOhm/m (R/R_Cu={rh/rcu:.3f})", flush=True)
        for ny in nys:
            p = b / ny
            t = math.sqrt(fill) * p
            nsub = max(2, math.ceil(t / (res * d)))
            n_unknown = 10 * ny * ny * nsub * nsub
            if n_unknown > 9200:
                print(f"   ny={ny} skipped (N={n_unknown})")
                continue
            c, t, p = strand_array(a, b, 10 * ny, ny, fill, S_AL, nsub)
            s = solve(c, f)
            print(f"   pitch={p*1e3:6.3f} mm t={t*1e3:6.3f} mm t/delta_Al={t/d:5.2f} pitch/delta_eff={p/delta(fill*S_AL,f):5.2f} "
                  f"nsub={nsub:2d} N={s['n']:5d}  R'={s['R']*1e6:8.2f} uOhm/m  R/R_homog={s['R']/rh:5.3f} "
                  f"R/R_solidAl={s['R']/ral:5.3f} R/R_solidCu={s['R']/rcu:5.3f}", flush=True)


if __name__ == "__main__":
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    if quick:
        scan(1e4, [1, 2, 3, 4, 6, 8], [0.3], 0.35)
    else:
        scan(1e4, [1, 2, 3, 4, 6, 8, 12], [0.3, 0.6, 0.85], 0.35)
        scan(1e5, [2, 3, 5, 8, 12], [0.3], 0.45)
        print("\n-- sub-cell resolution check (10 kHz, fill 0.3, pitch 2.5 and 1.25 mm)")
        scan(1e4, [2, 4], [0.3], 0.17)
        scan(1e4, [2, 4], [0.3], 0.45)
        print("\n-- strand-level proximity loss: one cell per strand (none) vs 2x2 cells, pitch 0.417 mm, fill 0.3")
        for f in (1e4, 1e5):
            d = delta(S_AL, f)
            r1 = solve(strand_array(a, b, 120, 12, 0.3, S_AL, 1)[0], f)["R"]
            c, t, p = strand_array(a, b, 120, 12, 0.3, S_AL, 2)
            r2 = solve(c, f)["R"]
            print(f"   f={f:.0f} t/delta={t/d:.2f}: 1x1 {r1*1e6:.2f}  2x2 {r2*1e6:.2f} uOhm/m  increase {r2/r1-1:.4f}"
                  f"   estimate fill*(t/delta)^2/6 = {0.3*(t/d)**2/6:.4f} (x0.75 captured by 2x2 = {0.75*0.3*(t/d)**2/6:.4f})",
                  flush=True)
