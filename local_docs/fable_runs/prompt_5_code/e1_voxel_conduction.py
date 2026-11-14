#!/usr/bin/env python3
"""E1: conduction bound for porous / lattice solids (Hashin-Shtrikman, Wiener) with a voxel solve (Note E1).
Spec row E1. Claim G1.8. Level: derived (unverified).
Cell of N^3 voxels, N = 32; three square struts of width w voxels along x, y, z (all starting at index s=(N-w)//2), phi = (3 w^2 N - 2 w^3)/N^3.
Potential at voxel centres; face conductance = harmonic mean of the two voxel conductivities; potential 1 and 0 on the two z faces with a half-cell
conductance 2*sigma to the face; periodic in x and y. scipy.sparse + spsolve. sigma_eff = I N/(N^2 dV) in voxel units. Void conductivity 1e-9.
Current conservation between the first and last z face checked to 1e-8 (relative).
Extra geometries: full solid; plates parallel to z of thickness w.
Bounds: HS upper 2 phi/(3 - phi); Wiener upper phi. Limit: sigma_eff -> phi/3 as phi -> 0 (within 15% at phi <= 0.05).
No LOOKUP values.
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve
N = 32; SV = 1e-9
def solve(sig):
    n = N
    idx = np.arange(n**3).reshape(n, n, n)
    rows = []; cols = []; vals = []; diag = np.zeros(n**3); rhs = np.zeros(n**3)
    def link(a, b, g):
        a = a.ravel(); b = b.ravel(); g = g.ravel()
        rows.extend([a, b]); cols.extend([b, a]); vals.extend([-g, -g])
        np.add.at(diag, a, g); np.add.at(diag, b, g)
    for ax in (0, 1):
        s2 = np.roll(sig, -1, axis=ax); i2 = np.roll(idx, -1, axis=ax)
        link(idx, i2, 2*sig*s2/(sig+s2))
    gz = 2*sig[:, :, :-1]*sig[:, :, 1:]/(sig[:, :, :-1]+sig[:, :, 1:])
    link(idx[:, :, :-1], idx[:, :, 1:], gz)
    g0 = 2*sig[:, :, 0].ravel(); i0 = idx[:, :, 0].ravel()
    np.add.at(diag, i0, g0); rhs[i0] += g0*1.0
    gN = 2*sig[:, :, -1].ravel(); iN = idx[:, :, -1].ravel()
    np.add.at(diag, iN, gN)
    A = sp.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n**3, n**3)).tocsr() + sp.diags(diag)
    V = spsolve(A.tocsc(), rhs).reshape(n, n, n)
    I_in = np.sum(g0*(1.0 - V[:, :, 0].ravel()))
    I_out = np.sum(gN*(V[:, :, -1].ravel() - 0.0))
    # interior plane (k=N//2 -> N//2+1)
    kk = N//2
    I_mid = np.sum(gz[:, :, kk]*(V[:, :, kk]-V[:, :, kk+1]))
    return I_in*N/(N*N), I_out*N/(N*N), I_mid*N/(N*N)
def strut(w):
    s = (N-w)//2; m = np.zeros((N, N, N), bool); sl = slice(s, s+w)
    m[:, sl, sl] = True; m[sl, :, sl] = True; m[sl, sl, :] = True
    return m
fails = 0
print("INPUTS: N=32, void conductivity 1e-9, solid 1; strut widths w (voxels); no lookup")
sg = np.full((N, N, N), 1.0)
a = solve(sg)
print(f"full solid: sigma_eff = {a[0]:.9f} (in), {a[1]:.9f} (out), {a[2]:.9f} (mid)")
ok = abs(a[0]-1) < 1e-8; fails += (not ok); print(f"CHECK full solid = 1.000 -> {'PASS' if ok else 'FAIL'}")
for w in (4, 8):
    m = np.zeros((N, N, N), bool); m[:w, :, :] = True
    sg = np.where(m, 1.0, SV); a = solve(sg); phi = w/N
    print(f"plates parallel to z, w={w}: phi={phi:.5f}, sigma_eff={a[0]:.9f}, expected phi + (1-phi)*1e-9 = {phi+(1-phi)*SV:.9f}")
    ok = abs(a[0]-phi) < 1e-6; fails += (not ok); print(f"CHECK plates sigma_eff = phi (1e-6) -> {'PASS' if ok else 'FAIL'}")
print("\nstrut lattice: w, phi, sigma_eff, HS=2phi/(3-phi), Wiener=phi, phi/3, sigma_eff/(phi/3), utilisation sigma_eff/phi, conservation |Iin-Iout|/Iin")
res = []
for w in (1, 2, 3, 4, 6, 8, 12, 16, 20, 24, 28, 30, 32):
    m = strut(w) if w < N else np.ones((N, N, N), bool)
    phi_calc = m.mean(); phi = (3*w*w*N-2*w**3)/N**3
    assert abs(phi_calc-phi) < 1e-12
    a = solve(np.where(m, 1.0, SV))
    se = a[0]; hs = 2*phi/(3-phi)
    cons = max(abs(a[0]-a[1])/a[0], abs(a[0]-a[2])/a[0])
    res.append((w, phi, se, hs, cons))
    print(f"{w:3d} {phi:8.5f} {se:10.6f} {hs:10.6f} {phi:8.5f} {phi/3:9.6f} {se/(phi/3):8.4f} {se/phi:8.4f} {cons:9.2e}")
res = np.array(res)
viol = (res[:, 2] - res[:, 3]).max()
print(f"max(sigma_eff - HS bound) = {viol:.3e} (negative = no violation); max(sigma_eff - phi) = {(res[:,2]-res[:,1]).max():.3e}")
ok = viol <= 1e-6 and (res[:, 2]-res[:, 1]).max() <= 1e-6; fails += (not ok); print(f"CHECK no HS / Wiener violation beyond 1e-6 -> {'PASS' if ok else 'FAIL'}")
ok = (res[:, 2]/res[:, 1] <= 1+1e-6).all(); fails += (not ok); print(f"CHECK specific utilisation sigma_eff/(phi sigma_s) <= 1 everywhere -> {'PASS' if ok else 'FAIL'}")
low = res[:, 1] <= 0.05
dev = np.abs(res[low, 2]/(res[low, 1]/3)-1)
print(f"phi<=0.05 points {low.sum()}: max |sigma_eff/(phi/3) - 1| = {dev.max()*100:.2f}% ; spec tolerance 15%")
ok = dev.max() <= 0.15; fails += (not ok); print(f"CHECK phi/3 limit within 15% -> {'PASS' if ok else 'FAIL'}")
ok = res[:, 4].max() < 1e-8; fails += (not ok)
print(f"CHECK current conservation (first/last/middle plane) < 1e-8 -> {'PASS' if ok else 'FAIL'} (max {res[:,4].max():.2e})")
print(f"phi values: {len(res)}; range {res[0,1]:.4f}..{res[-1,1]:.2f}; spec asks phi in [0.02,1] with >= 8 values: {((res[:,1]>=0.02)).sum()} values >= 0.02")
print("note: HS is an upper bound for isotropic composites; the strut lattice is cubic-symmetric so its effective conductivity is isotropic (tensor reduces to a scalar), so the HS bound applies.")
print("IDENTITY CHECKS: none (voxel solve vs analytic bounds). Full-solid and plate checks are exactness tests of the discretisation.")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
