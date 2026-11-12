"""A2: the same strand bundle, parallel-connected vs ideally transposed (Litz-like).

What it computes
    R' of the Al strand bundle of a2_strand_bundle_scan.py (fill 0.3, 10 x 100 mm
    envelope) when every strand is forced to carry the same net current.  That is what
    strand insulation plus transposition enforces on average over one transposition
    pitch.  Unknowns: J per sub-cell and one voltage drop V'_k per strand:

        J_i/sigma + j*omega*A_i - V'_{k(i)} = 0 ,     sum_{i in strand k} J_i a_i = 1

    R' = total loss / |I_total|^2.  Printed next to it: R_dc of the bundle, the
    low-frequency 1-D estimate of the proximity-loss ratio for square strands,
    fill^2 h^2 t^2 / (36 delta^4)  (h = bundle thickness 10 mm, t = strand side),
    the same estimate times the 2-D field factor g = 1.55 (see a1_analytic_numbers.py,
    section 6), and that times the share of the strand dipole loss which nsub x nsub
    sub-cells can represent (0.75 for 2x2, 0.889 for 3x3).

Which answer items it supports
    A2.4 (transposition, not strut size, is what removes the bar-scale skin effect),
    A2.7 (Litz alternative), verdict.

Assumptions
    As eddy2d.py.  'Ideal transposition' = equal strand currents; lay length, twist
    pitch, bundle-level construction and strand insulation thickness are not modelled.
    Strand-level proximity loss is captured only as far as nsub x nsub sub-cells
    resolve it (2x2: 75 %, 3x3: 89 % of the dipole moment), so the printed R' is a
    slight underestimate at 10 kHz and unreliable in detail at 100 kHz where
    t/delta ~ 1; the conclusion drawn from it is only the order of magnitude.

Run time: about 4 minutes (dense systems of 7200 and 10000 complex unknowns, ~2 GB RAM).
"""
import time

import numpy as np

from eddy2d import S_AL, build_M, delta, strand_array, uniform_current_h2_factor

a, b = 50e-3, 5e-3
fill = 0.3
g2d = sum(uniform_current_h2_factor(2 * a, 2 * b))
capture = {2: 0.75, 3: 8 / 9}
for f, nx, ny, nsub in ((1e4, 120, 12, 2), (1e5, 120, 12, 2), (1e4, 100, 10, 3), (1e5, 100, 10, 3)):
    t0 = time.time()
    c, t, p = strand_array(a, b, nx, ny, fill, S_AL, nsub)
    M, area, sg, images, xc, yc = build_M(c, f)
    n = area.size
    ns = nx * ny
    k = np.floor(xc / p).astype(int) * ny + np.floor(yc / p).astype(int)   # strand index of each cell
    S = np.zeros((n + ns, n + ns), complex)
    S[:n, :n] = M
    del M
    S[np.arange(n), n + k] = -1.0
    S[n + k, np.arange(n)] = area
    rhs = np.zeros(n + ns, complex)
    rhs[n:] = 1.0                      # 1 A per quarter-strand
    sol = np.linalg.solve(S, rhs)
    del S
    J, V = sol[:n], sol[n:]
    I = 4 * ns * 1.0
    R = 4 * np.sum(np.abs(J) ** 2 * area / sg) / I ** 2
    Rv = np.sum(V).real * 4 / I ** 2   # same quantity from Re(sum V_k I_k*)
    Rdc = 1 / (S_AL * fill * 4 * a * b)
    d = delta(S_AL, f)
    est = fill ** 2 * (2 * b) ** 2 * t ** 2 / (36 * d ** 4)
    print(f"f={f:.0f} pitch={p*1e3:.3f} t={t*1e3:.3f} mm (t/delta={t/d:.2f}) nsub={nsub} N={n}+{ns}: "
          f"R'_transposed={R*1e6:8.2f} uOhm/m (via V: {Rv*1e6:8.2f})  R_dc={Rdc*1e6:.2f}  "
          f"prox ratio sim={R/Rdc-1:.3f}  low-freq estimate: 1-D {est:.3f}, x g={g2d:.3f}: {g2d*est:.3f}, "
          f"x sub-cell capture: {g2d*est*capture[nsub]:.3f}  [{time.time()-t0:.0f}s]", flush=True)
