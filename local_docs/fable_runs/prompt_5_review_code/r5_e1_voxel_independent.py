#!/usr/bin/env python3
"""S5 review, task (2): independent voxel conduction solve for the simple-cubic strut lattice (row E1, claim G1.8).
Differences from e1_voxel_conduction.py: fully periodic cell with an imposed mean gradient (unknown = periodic part
of the potential), void conductivity exactly 0 (only solid voxels are unknowns), conjugate-gradient solve, and a
grid refinement (N = 64 with doubled strut width) to estimate discretisation error at fixed phi.
Same voxel geometry as E1 at N = 32 (struts of width w through the cell centre). Compares with the S2 values and with
the Hashin-Shtrikman bound 2 phi/(3 - phi). Usage: python3 r5_e1_voxel_independent.py   Level: derived.
"""
import numpy as np, scipy.sparse as sp, time
from scipy.sparse.linalg import cg
S2 = {1: 0.000977, 2: 0.003959, 4: 0.016310, 8: 0.069289, 16: 0.312858, 24: 0.729382}   # outputs/e1_voxel_conduction.txt
def lattice(N, w):
    s = (N - w)//2; m = np.zeros((N, N, N), bool); sl = slice(s, s + w)
    m[:, sl, sl] = True; m[sl, :, sl] = True; m[sl, sl, :] = True
    return m
def sigma_eff(m):
    N = m.shape[0]; ids = -np.ones(m.shape, int); ids[m] = np.arange(m.sum()); n = int(m.sum())
    rows, cols, vals = [], [], []; diag = np.zeros(n); b = np.zeros(n)
    zlinks = []
    for ax in range(3):
        nb = np.roll(ids, -1, axis=ax)
        both = (ids >= 0) & (nb >= 0)
        a, c = ids[both], nb[both]          # conductance 1 between two solid voxels (harmonic mean of 1 and 1)
        rows += [a, c]; cols += [c, a]; vals += [-np.ones(len(a)), -np.ones(len(a))]
        np.add.at(diag, a, 1.0); np.add.at(diag, c, 1.0)
        if ax == 2:
            # potential V = psi - z ; current a->c = psi_a - psi_c + 1 ; balance: L psi = -(sum out-links - sum in-links)
            np.add.at(b, a, -1.0); np.add.at(b, c, +1.0)
            zlinks = (a, c, both)
    A = sp.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)).tocsr() + sp.diags(diag)
    A = A + sp.diags(np.full(n, 1e-12))     # gauge regularisation (b sums to zero)
    psi, info = cg(A, b, rtol=1e-12, maxiter=20000)
    a, c, both = zlinks
    # current through the plane between z = N//2 - 1 and N//2 : links whose start voxel has z index N//2 - 1
    zidx = np.nonzero(both)[2]
    sel = zidx == N//2 - 1
    I = np.sum(psi[a[sel]] - psi[c[sel]] + 1.0)
    I_all = np.sum(psi[a] - psi[c] + 1.0)/N     # mean over all planes (conservation check)
    return I/N**2, abs(I - I_all)/I, info
print("N   w   phi       sigma_eff(own)  S2 (N=32)   own/S2-1    HS bound   own/HS   conservation  cg_info")
res = {}
for N, ws in ((32, (1, 2, 4, 8, 16, 24)), (64, (2, 4, 8, 16, 32, 48))):
    for w in ws:
        t0 = time.time(); m = lattice(N, w); phi = m.mean()
        se, cons, info = sigma_eff(m); hs = 2*phi/(3 - phi)
        res[(N, w)] = (phi, se)
        s2 = S2.get(w) if N == 32 else None
        print("%-3d %-3d %.5f   %.6f        %-10s  %-10s  %.6f   %.4f   %.1e       %d  (%.0f s)" % (
            N, w, phi, se, "%.6f" % s2 if s2 else "-", "%+.1e" % (se/s2 - 1) if s2 else "-", hs, se/hs, cons, info, time.time() - t0))
print("\nGrid refinement at fixed phi (N=32, w) -> (N=64, 2w):")
for w in (1, 2, 4, 8, 12 if False else 16, 24):
    if (64, 2*w) in res:
        p32, s32 = res[(32, w)]; p64, s64 = res[(64, 2*w)]
        print("  phi %.5f: sigma_eff N=32 %.6f, N=64 %.6f, change %+.2f%%; specific utilisation sigma/phi %.4f -> %.4f" % (p32, s32, s64, 100*(s64/s32 - 1), s32/p32, s64/p64))
