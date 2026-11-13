"""S5 review, check RV3: base spreading with a concentrated source, independent of the Lee et al. closed form.

Level: derived (unverified).  numpy + standard library only.
  (a) Exact Fourier-series solution for a rectangular plate (60 x 60 mm, thickness t_b, conductivity k),
      centred 20 x 20 mm uniform-flux source on top, adiabatic sides and top elsewhere, uniform heat-transfer
      coefficient h = 1/(R0 A_p) on the bottom (fin side lumped as in S2's B14).  Gives R_base,max (centre)
      and R_base,avg (source mean) to compare with the circular-equivalent closed form used by S2
      (B14: Cu 0.0808/0.0594, Al k=150 0.2054/0.1512 K/W at t_b = 5 mm).
  (b) T_hot: flux-weighted harmonic mean against arithmetic mean and maximum of the source surface (B1.5).
  (c) 3-D finite-volume conduction (matrix-free CG) cross-checked against (a), then used for a fair-design
      variant S2 did not test: aluminium base with a copper slug under the source.
  (d) Hybrid: copper base with aluminium fins (fin side R0 of the Al k=150 optimum).
R0 values (fin side, 0.1 W air power) are S2's B05 optima: Cu 0.26794, Al k=150 0.30437, Al k=100 0.32479 K/W.
Run: python3 rv3_spreading.py > outputs/rv3_spreading.txt
"""
import math
import numpy as np

Q, LX, LY = 100.0, 0.060, 0.060
CS = 0.020
T0 = 298.15
AP = LX * LY


def fourier(k, tb, R0, nmodes=600, grid=41):
    h = 1.0 / (R0 * AP)
    q0 = Q / (CS * CS)
    m = np.arange(nmodes)
    lam = m * math.pi / LX
    x1, x2 = LX / 2 - CS / 2, LX / 2 + CS / 2
    a = np.zeros(nmodes)
    a[0] = CS / LX
    a[1:] = 2.0 / (m[1:] * math.pi) * (np.sin(m[1:] * math.pi * x2 / LX) - np.sin(m[1:] * math.pi * x1 / LX))
    g = np.ones(nmodes)                        # mean of cos over the source
    g[1:] = a[1:] * LX / (2 * CS)
    B = np.sqrt(lam[:, None] ** 2 + lam[None, :] ** 2)
    B[0, 0] = 1.0
    th = np.tanh(B * tb)
    phi = (k * B + h * th) / (k * B * th + h)
    Amn = q0 * np.outer(a, a) / (k * B) * phi
    Amn[0, 0] = Q / AP * (tb / k + 1.0 / h)
    cen = np.cos(m * math.pi / 2)              # cos(lambda_m * LX/2)
    Tc = float(cen @ Amn @ cen)
    Tavg = float(g @ Amn @ g)
    xs = np.linspace(x1, x2, grid)
    Cx = np.cos(np.outer(xs, lam))
    field = Cx @ Amn @ Cx.T                    # temperature excess over the source
    return Tc, Tavg, field


def lee(k, tb, R0, a_s=math.sqrt(4e-4 / math.pi), b_p=math.sqrt(AP / math.pi)):
    # S2's closed form, re-typed here only for the side-by-side comparison
    eps, tau = a_s / b_p, tb / b_p
    Bi = 1.0 / (math.pi * k * b_p * R0)
    lam = math.pi + 1 / (math.sqrt(math.pi) * eps)
    t = math.tanh(lam * tau)
    Phi = (t + lam / Bi) / (1 + (lam / Bi) * t)
    sp = math.sqrt(math.pi)
    pm = eps * tau / sp + (1 - eps) * Phi / sp
    pa = eps * tau / sp + 0.5 * (1 - eps) ** 1.5 * Phi
    return pm / (sp * k * a_s), pa / (sp * k * a_s)


def fv(kfun, tb, R0, nx=60, nz=10, tol=1e-10):
    """3-D FV, cell-centred, kfun(x, y, z) -> k.  Returns (T_centre_top, T_avg_source)."""
    h = 1.0 / (R0 * AP)
    dx = LX / nx
    dz = tb / nz
    xc = (np.arange(nx) + 0.5) * dx
    zc = (np.arange(nz) + 0.5) * dz
    X, Y, Z = np.meshgrid(xc, xc, zc, indexing="ij")
    K = kfun(X, Y, Z)
    # face conductances (harmonic mean)
    Gx = (dx * dz) / (dx / (2 * K[:-1]) + dx / (2 * K[1:]))
    Gy = (dx * dz) / (dx / (2 * K[:, :-1]) + dx / (2 * K[:, 1:]))
    Gz = (dx * dx) / (dz / (2 * K[:, :, :-1]) + dz / (2 * K[:, :, 1:]))
    Gb = (dx * dx) / (dz / (2 * K[:, :, -1]) + 1.0 / h)      # bottom (z = tb) to ambient
    src = (np.abs(X[:, :, 0] - LX / 2) < CS / 2) & (np.abs(Y[:, :, 0] - LY / 2) < CS / 2)
    b = np.zeros_like(K)
    b[:, :, 0][src] = Q / (src.sum())

    def Aop(T):
        r = np.zeros_like(T)
        d = T[:-1] - T[1:]
        r[:-1] += Gx * d
        r[1:] -= Gx * d
        d = T[:, :-1] - T[:, 1:]
        r[:, :-1] += Gy * d
        r[:, 1:] -= Gy * d
        d = T[:, :, :-1] - T[:, :, 1:]
        r[:, :, :-1] += Gz * d
        r[:, :, 1:] -= Gz * d
        r[:, :, -1] += Gb * T[:, :, -1]
        return r
    diag = np.zeros_like(K)
    diag[:-1] += Gx
    diag[1:] += Gx
    diag[:, :-1] += Gy
    diag[:, 1:] += Gy
    diag[:, :, :-1] += Gz
    diag[:, :, 1:] += Gz
    diag[:, :, -1] += Gb
    T = np.zeros_like(K)
    r = b - Aop(T)
    z = r / diag
    p = z.copy()
    rz = (r * z).sum()
    bn = math.sqrt((b * b).sum())
    for it in range(20000):
        Ap = Aop(p)
        al = rz / (p * Ap).sum()
        T += al * p
        r -= al * Ap
        if math.sqrt((r * r).sum()) < tol * bn:
            break
        z = r / diag
        rz2 = (r * z).sum()
        p = z + rz2 / rz * p
        rz = rz2
    # top-surface temperature: extrapolate half a cell (top is adiabatic except source flux)
    Ttop = T[:, :, 0] + b[:, :, 0] * (dz / 2) / (K[:, :, 0] * dx * dx)
    ic = nx // 2
    Tcen = 0.25 * (Ttop[ic - 1, ic - 1] + Ttop[ic, ic] + Ttop[ic - 1, ic] + Ttop[ic, ic - 1])
    return Tcen, float(Ttop[src].mean()), it


R0 = {390: 0.26794, 150: 0.30437, 100: 0.32479}
print("RV3 spreading check  (level: derived, unverified)")
print("\n=== (a) Fourier series against S2's closed form (t_b = 5 mm), R_base = T/Q - R0 ===")
for k in (390, 150, 100):
    for nm in (300, 600):
        Tc, Ta, F = fourier(float(k), 0.005, R0[k], nmodes=nm)
        print("k=%3d modes=%d: Fourier R_base,max=%.5f R_base,avg=%.5f" % (k, nm, Tc / Q - R0[k], Ta / Q - R0[k]))
    lm, la = lee(float(k), 0.005, R0[k])
    print("        S2 closed form (circular equivalent): R_max=%.5f R_avg=%.5f" % (lm, la))
Tc_cu, Ta_cu, _ = fourier(390.0, 0.005, R0[390])
Tc_al, Ta_al, _ = fourier(150.0, 0.005, R0[150])
print("Al(150) - Cu penalty at t_b = 5 mm: Fourier max %.4f avg %.4f K/W; S2 0.1247 / 0.0918" % (
    (Tc_al - Tc_cu) / Q - (R0[150] - R0[390]), (Ta_al - Ta_cu) / Q - (R0[150] - R0[390])))

print("\n=== (b) T_hot over the source surface (uniform flux): harmonic, arithmetic, max ===")
for k in (390, 150):
    Tc, Ta, F = fourier(float(k), 0.005, R0[k], nmodes=600, grid=81)
    T = T0 + F
    harm = 1.0 / np.mean(1.0 / T)
    ar = T.mean()
    tmax = T0 + Tc
    Sh = Q * (1 / T0 - 1 / harm)
    Sm = Q * (1 / T0 - 1 / tmax)
    print("k=%3d: T_harm=%.4f T_arith=%.4f (diff %.4f K) T_max=%.3f ; Q(1/T0-1/T_max) / Q(1/T0-1/T_harm) - 1 = %.4f" % (
        k, harm, ar, ar - harm, tmax, Sm / Sh - 1))

print("\n=== (c) 3-D finite volume: check against Fourier, then Al base with Cu slug ===")
for k in (390, 150):
    Tc, Ta, it = fv(lambda X, Y, Z, kk=k: np.full(X.shape, float(kk)), 0.005, R0[k])
    Tcf, Taf, _ = fourier(float(k), 0.005, R0[k])
    print("k=%3d FV(60x60x10): R_max=%.5f R_avg=%.5f (CG its %d) ; Fourier R_max=%.5f R_avg=%.5f" % (
        k, Tc / Q - R0[k], Ta / Q - R0[k], it, Tcf / Q - R0[k], Taf / Q - R0[k]))
for slug in (0.020, 0.030, 0.040):
    kf = lambda X, Y, Z, s=slug: np.where((np.abs(X - LX / 2) < s / 2) & (np.abs(Y - LY / 2) < s / 2), 390.0, 150.0)
    Tc, Ta, it = fv(kf, 0.005, R0[150])
    mass_cu = slug * slug * 0.005 * 8960
    print("Al k=150 base with Cu slug %2.0f x %2.0f x 5 mm (Cu %.3f kg), Al fins R0=0.30437: base R_max=%.5f, total peak R=%.4f K/W" % (
        slug * 1e3, slug * 1e3, mass_cu, Tc / Q - R0[150], Tc / Q))

print("\n=== (d) Peak resistance (base max + fin side), t_b = 5 mm, uniform-h fin side, no TIM ===")
rows = [("all Cu (Cu fins, Cu base)", 390.0, R0[390], 0.3451),
        ("Cu base + Al k=150 fins", 390.0, R0[150], 0.005 * AP * 8960),
        ("all Al k=150", 150.0, R0[150], 0.1192),
        ("all Al k=100", 100.0, R0[100], 0.1230)]
for nm, k, r0, cu in rows:
    Tc, Ta, _ = fourier(k, 0.005, r0)
    print("%-28s peak R = %.4f K/W (T_max - T_in = %.1f K); copper mass %.3f kg" % (nm, Tc / Q, Tc, cu if k == 390 else 0.0))
