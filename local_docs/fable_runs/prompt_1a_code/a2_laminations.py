"""A2 fair alternatives: laminated Al strips with and without go/return interleaving.

What it computes
    (a) Isolated stack of n parallel-connected, mutually insulated Al strips, each
        100 mm wide, filling the 10 mm thickness (10 % insulation), NOT interleaved
        and not transposed.  Expected: same R' as the solid Al bar.
    (b) Interleaved go/return stack G R G R ... (laminated busbar): ngo 'go' foils and
        ngo 'return' foils alternate.  R' is per polarity (all go foils in parallel).
        Compared with two 1-D formulas:
          - Claim A's formula with xi = t/delta applied to every foil (Dowell, m = 1);
          - the corrected 1-D model: interior foils carry twice the current of the two
            end foils and see equal and opposite H on their two faces, so they obey the
            same formula with xi = t/(2 delta); end foils obey it with xi = t/delta:
            R' = [4(ngo-1) F(t/2delta) + F(t/delta)] / (2 ngo - 1)^2 / (sigma t w).

Which answer items it supports
    A1.1 and A1.2 (which geometry Claim A's formula is valid for), A2.7.

Assumptions
    As eddy2d.py.  Stack (b) is antisymmetric about its mid-plane: J even in x, odd in y.

Run time: about 3 minutes.
"""
import numpy as np

from eddy2d import (MESH_H0_DIV, MESH_HMAX, MESH_RATIO, S_AL, delta, dowell_skin, graded, solve, tensor_cells)

a = 50e-3


def strips(y_edges_list, sigma, f, lvl=1):
    d = delta(sigma, f)
    cs = []
    for (ya, yb) in y_edges_list:
        t = yb - ya
        h0, r, hmax = min(d, t) / MESH_H0_DIV[lvl], MESH_RATIO[lvl], MESH_HMAX[lvl]
        cs.append(tensor_cells(graded(a, h0, r, hmax, "hi"), ya + graded(t, h0, r, hmax, "both"), sigma))
    return {k: np.concatenate([c[k] for c in cs]) for k in cs[0]}, [c["x0"].size for c in cs]


for f in (1e4, 1e5):
    d = delta(S_AL, f)
    print(f"f={f:.0f} Hz delta_Al={d*1e3:.4f} mm")
    for n in (10, 20):
        pitch = 10e-3 / n
        t = 0.9 * pitch
        ylist = [(k * pitch + 0.05 * pitch, k * pitch + 0.05 * pitch + t) for k in range(n // 2)]
        c, _ = strips(ylist, S_AL, f)
        s = solve(c, f)
        print(f"  (a) isolated stack of {n} parallel Al strips {t*1e3:.2f} mm (t/delta={t/d:.2f}), not interleaved: "
              f"N={s['n']} R'={s['R']*1e6:8.2f} uOhm/m", flush=True)
    for t, g, ngo in ((1.0e-3, 0.2e-3, 5), (0.25e-3, 0.1e-3, 20)):
        npl = 2 * ngo
        pitch = t + g
        ylist = [(g / 2 + k * pitch, g / 2 + k * pitch + t) for k in range(ngo)]   # upper half of the stack
        c, counts = strips(ylist, S_AL, f)
        sign = np.concatenate([np.full(m, 1.0 if k % 2 == 0 else -1.0) for k, m in enumerate(counts)])
        s = solve(c, f, sym=(1, -1), rhs=sign)
        area = (c["x1"] - c["x0"]) * (c["y1"] - c["y0"])
        Igo = 2 * np.sum(sign * s["J"] * area)
        Pgo = 2 * np.sum(np.abs(s["J"]) ** 2 * area / S_AL)
        xi = t / d
        claim = dowell_skin(xi) / (S_AL * ngo * t * 2 * a)
        corrected = (4 * (ngo - 1) * dowell_skin(xi / 2) + dowell_skin(xi)) / (2 * ngo - 1) ** 2 / (S_AL * t * 2 * a)
        print(f"  (b) interleaved {ngo} go + {ngo} return Al foils {t*1e3:.2f} mm x 100 mm, gap {g*1e3:.2f} mm, "
              f"stack {(npl*t + (npl-1)*g)*1e3:.1f} mm: N={s['n']} R'_go={(1/Igo).real*1e6:8.2f} uOhm/m "
              f"(loss-based {Pgo/abs(Igo)**2*1e6:8.2f}); Claim-A formula xi=t/delta={xi:.2f}: {claim*1e6:8.2f}; "
              f"corrected 1-D model: {corrected*1e6:8.2f}", flush=True)
