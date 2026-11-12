"""A3 worked comparison: R_ac per metre of a 10 mm x 100 mm busbar envelope.

What it computes
    R' [uOhm/m] at 10 kHz and 100 kHz, dissipation and Sigma_dot = P/T0 at I_rms = 1 kA,
    mass per metre and the product R'*mass, for
      - solid Cu, solid Al,
      - Al lattice at relative density 0.3 as a homogenised bar, three sigma_eff choices,
      - hollow Al tube of the same outer envelope and the same mass as the lattice
        (uniform wall 1.399 mm), and a Cu tube with the same wall,
    each on three mesh levels (discretisation error = spread between levels).
    Also prints R_dc, the 1-D estimate 1/(sigma*delta*P) and the edge factor.

Which answer items it supports
    A3 (table), A2.1, A2.6 and the verdict.

Assumptions
    See eddy2d.py (isolated bar, return at infinity, 20 C conductivities).
    Lattice = homogeneous conductor with axial conductivity sigma_eff; the explicit
    strand-resolved check is in a2_strand_bundle_scan.py.

Run time: about 1 minute.
"""
import math

from eddy2d import (RHO_AL, RHO_CU, S_AL, S_CU, T0, delta, dowell_skin, run, solid_bar, tube)

a, b = 50e-3, 5e-3
A = 4 * a * b
P = 4 * (a + b)
RHOBAR = 0.3
I_RMS = 1000.0

# wall of the tube with metal area RHOBAR*A:  A - (2a-2w)(2b-2w) = RHOBAR*A
wall = (2 * (a + b) - math.sqrt(4 * (a + b) ** 2 - 4 * RHOBAR * A)) / 4
print(f"wall of equal-mass tube (area {RHOBAR}*A = {RHOBAR*A*1e6:.0f} mm2) = {wall*1e3:.4f} mm")

res = {}
for f in (1e4, 1e5):
    print(f"\n== A3  f = {f:.0f} Hz ==  delta_Cu={delta(S_CU,f)*1e3:.4f} mm  delta_Al={delta(S_AL,f)*1e3:.4f} mm")
    cases = [("solid Cu", S_CU, RHO_CU * A),
             ("solid Al", S_AL, RHO_AL * A),
             ("Al lattice homog. sigma_eff=0.300*sAl (all struts axial, tau=1)", RHOBAR * S_AL, RHO_AL * A * RHOBAR),
             ("Al lattice homog. sigma_eff=0.222*sAl (isotropic HS upper bound)", 2 * RHOBAR / (3 - RHOBAR) * S_AL, RHO_AL * A * RHOBAR),
             ("Al lattice homog. sigma_eff=0.100*sAl (rho/3, low-density strut foam)", RHOBAR / 3 * S_AL, RHO_AL * A * RHOBAR)]
    for name, sg, mass in cases:
        for lvl in (0, 1, 2):
            s = run(f"   {name[:48]} lvl{lvl}", solid_bar(a, b, sg, f, lvl), f)
        d = delta(sg, f)
        est = 1 / (sg * d * P)
        print(f"      sigma={sg:.4e} S/m delta={d*1e3:.4f} mm  Rdc={1/(sg*A)*1e6:8.2f}  1/(sigma*delta*P)={est*1e6:8.2f}"
              f"  edge factor={s['R']/est:6.3f}  Rac/Rdc={s['R']*sg*A:7.2f}")
        res[(name, f)] = (s["R"], mass)
    for lvl in (0, 1, 2):
        s = run(f"   Al tube 10x100, wall {wall*1e3:.3f} mm lvl{lvl}", tube(a, b, wall, S_AL, f, lvl), f)
    res[("Al tube, same envelope, wall 1.399 mm (equal mass to lattice)", f)] = (s["R"], RHO_AL * A * RHOBAR)
    print(f"      1-D estimate Dowell(wall/delta_Al={wall/delta(S_AL,f):.2f})/(sigma*wall*(P-4*wall))="
          f"{dowell_skin(wall/delta(S_AL,f))/(S_AL*wall*(P-4*wall))*1e6:8.2f} uOhm/m (no edge crowding)")
    for lvl in (0, 1, 2):
        s = run(f"   Cu tube 10x100, wall {wall*1e3:.3f} mm lvl{lvl}", tube(a, b, wall, S_CU, f, lvl), f)
    res[("Cu tube, same envelope, wall 1.399 mm", f)] = (s["R"], RHO_CU * A * RHOBAR)

print(f"\n== summary (finest mesh), I_rms = {I_RMS:.0f} A, T0 = {T0} K")
print(f"{'f [Hz]':>8s}  {'case':70s} {'R [uOhm/m]':>10s} {'R/R_Cu':>7s} {'P [W/m]':>8s} {'Sdot [W/(K m)]':>14s} {'m [kg/m]':>8s} {'R*m [uOhm kg/m2]':>16s}")
for (name, f), (r, mass) in res.items():
    rcu = res[("solid Cu", f)][0]
    print(f"{f:8.0f}  {name:70s} {r*1e6:10.2f} {r/rcu:7.3f} {r*I_RMS**2:8.1f} {r*I_RMS**2/T0:14.3f} {mass:8.2f} {r*1e6*mass:16.1f}")
