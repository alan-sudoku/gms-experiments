"""A2: conductivity sweep, tube-wall sweep, and Al tubes that match solid Cu.

What it computes
    1. R'(sigma) for the fixed solid 10 x 100 mm envelope at 10 kHz and 100 kHz,
       sigma from 1e5 to 1.2e8 S/m, with a flag if R' ever increases with sigma.
       (Tests: 'for the same shape a lower effective conductivity never lowers R_ac'.)
    2. R' of a hollow Al tube with the 10 x 100 mm outer envelope vs wall thickness at
       10 kHz (location and depth of the optimum near wall = 1.57 delta).
    3. R' of wider Al tubes (10 mm x W, wall 1.6 delta_Al) relative to the solid
       10 x 100 mm Cu bar: which width W gives R_Al = R_Cu, and at what mass.

Which answer items it supports
    A2.1, A2.5, A2.6, A5 (restated claim: macro-shape substitution).

Assumptions
    As eddy2d.py (isolated conductor, 20 C conductivities).

Run time: about 1 minute.
"""
import numpy as np

from eddy2d import RHO_AL, RHO_CU, S_AL, S_CU, delta, solid_bar, solve, tube

a, b = 50e-3, 5e-3
A = 4 * a * b

print("== 1. monotonicity: R'(sigma) for the fixed 10x100 mm solid envelope")
for f in (1e4, 1e5):
    prev = None
    for sg in np.geomspace(1e5, 1.2e8, 16):
        s = solve(solid_bar(a, b, sg, f, 1), f)
        flag = "" if prev is None or s["R"] < prev else "   <-- NOT monotone"
        print(f"   f={f:.0f} sigma={sg:10.3e} b/delta={b/delta(sg,f):6.2f} R'={s['R']*1e6:9.2f} uOhm/m{flag}")
        prev = s["R"]

print("\n== 2. tube wall sweep, Al, 10x100 envelope, 10 kHz")
f = 1e4
d = delta(S_AL, f)
rsolid = solve(solid_bar(a, b, S_AL, f, 1), f)["R"]
for wd in (0.5, 0.8, 1.0, 1.2, 1.4, 1.57, 1.8, 2.2, 3.0, 4.0):
    s = solve(tube(a, b, wd * d, S_AL, f, 1), f)
    print(f"   wall={wd:4.2f} delta = {wd*d*1e3:5.3f} mm  area={(A-4*(a-wd*d)*(b-wd*d))*1e6:6.1f} mm2 "
          f"R'={s['R']*1e6:8.2f} uOhm/m  R/R_solidAl={s['R']/rsolid:5.3f}")

print("\n== 3. Al tubes 10 mm x W, wall 1.6 delta_Al, vs solid Cu 10x100 "
      f"(solid Cu mass {RHO_CU*A:.2f} kg/m)")
for f in (1e4, 1e5):
    d = delta(S_AL, f)
    rcu = solve(solid_bar(a, b, S_CU, f, 1), f)["R"]
    for width in (100e-3, 115e-3, 126e-3, 135e-3, 150e-3):
        wl = 1.6 * d
        s = solve(tube(width / 2, b, wl, S_AL, f, 1), f)
        ar = width * 2 * b - (width - 2 * wl) * (2 * b - 2 * wl)
        print(f"   f={f:.0f} Al tube {width*1e3:.0f}x10 mm wall {wl*1e3:.3f} mm area {ar*1e6:6.1f} mm2 "
              f"mass {ar*RHO_AL:5.2f} kg/m  R'={s['R']*1e6:8.2f}  R/R_solidCu={s['R']/rcu:5.3f}")
