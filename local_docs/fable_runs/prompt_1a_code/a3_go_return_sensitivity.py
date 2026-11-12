"""A3 sensitivity to the 'isolated bar' assumption: go/return pair of identical bars.

What it computes
    R' per conductor [uOhm/m] for two identical 10 mm x 100 mm conductors placed
    broadside (wide faces facing) with a gap of 2 mm or 20 mm, carrying equal and
    opposite currents: solid Cu, solid Al, homogenised Al lattice (0.3*sigma_Al) and
    the equal-mass Al tube (wall 1.399 mm).  Loop resistance is twice the printed value.

Which answer items it supports
    A3 (stated error of the isolated-bar assumption), A3.5.

Assumptions
    As eddy2d.py, except that the return conductor is the mirror image in the plane
    y = 0 (J even in x, odd in y).

Run time: about 20 s.
"""
import numpy as np

from eddy2d import (MESH_H0_DIV, MESH_HMAX, MESH_RATIO, S_AL, S_CU, delta, graded, solve, tensor_cells)

a, b = 50e-3, 5e-3
WALL = 1.3992e-3


def pair_cells(sigma, f, g, hollow=False, lvl=1):
    d = delta(sigma, f)
    h0, r, hmax = d / MESH_H0_DIV[lvl], MESH_RATIO[lvl], MESH_HMAX[lvl]
    if not hollow:
        return tensor_cells(graded(a, h0, r, hmax, "hi"), g / 2 + graded(2 * b, h0, r, hmax, "both"), sigma)
    xe = np.concatenate([graded(a - WALL, h0, r, hmax, "hi"), (a - WALL) + graded(WALL, h0, r, hmax, "both")[1:]])
    w = graded(WALL, h0, r, hmax, "both")
    mid = WALL + graded(2 * b - 2 * WALL, h0, r, hmax, "both")
    ye = g / 2 + np.concatenate([w, mid[1:], (2 * b - WALL) + w[1:]])
    return tensor_cells(xe, ye, sigma,
                        mask=lambda x, y: (x > a - WALL) | (y < g / 2 + WALL) | (y > g / 2 + 2 * b - WALL))


for g in (2e-3, 20e-3):
    for f in (1e4, 1e5):
        out = {}
        for name, sg, hol in (("solid Cu", S_CU, False), ("solid Al", S_AL, False),
                              ("Al lattice homog 0.3*sAl", 0.3 * S_AL, False),
                              ("Al tube wall 1.399 mm", S_AL, True)):
            s = solve(pair_cells(sg, f, g, hol, 1), f, sym=(1, -1))
            out[name] = s["R"]
            print(f"gap={g*1e3:4.0f} mm f={f:7.0f} {name:26s} N={s['n']:5d} R'={s['R']*1e6:8.2f} uOhm/m per conductor "
                  f"(loss-based {s['R_loss']*1e6:8.2f})  R/R_Cu={s['R']/out['solid Cu']:5.3f}  "
                  f"1/(sigma*delta*w)={1/(sg*delta(sg,f)*2*a)*1e6:8.2f}", flush=True)
