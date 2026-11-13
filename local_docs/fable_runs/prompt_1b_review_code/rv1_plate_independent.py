"""S5 review, check RV1: independent plate-fin model and a 2-D (height-unmixed) air closure.

Level: derived (unverified).  numpy + standard library only.  Does NOT import gms_core.
Purpose
  (a) Re-implement the plate-fin optimisation from the formulas as I derive/recall them, to check the
      headline Cu optimum (0.268 K/W at 0.1 W air power) and the Al/Cu ratios (9-21 %).
  (b) Replace the 1-D closure "air mixed over the fin height + eps-NTU" by a 2-D closure in which every
      height strip of air keeps its own temperature (no mixing over the height: in laminar flow in a
      1.3 mm x 30 mm channel nothing mixes the air over 30 mm).  Fin conduction in z, air advection in x.
      Linear problem solved exactly in x by matrix exponential (eigen-decomposition) of the z-discretised
      system; cross-checked by backward-Euler marching for one case.
  (c) Correlation sensitivity: hydraulics/heat-transfer set S (as used by S2: Shah-London rectangular
      fRe polynomial + Muzychka-type developing term 3.44; Stephan Nu) and set B (Shah 1978 parallel
      plate apparent friction, constants recalled from memory = UNSURE; Nu = fully developed 7.541 only,
      a deliberately pessimistic heat-transfer bound).
Inputs: same geometry and air properties as plan section 3.0 (60 x 60 mm base, H = 30 mm, Q = 100 W,
  air at 298.15 K, rho 1.1614, cp 1007, mu 1.846e-5, k 0.0263, Pr 0.707), min gap 0.8 mm, Re < 2300.
Run: python3 rv1_plate_independent.py > outputs/rv1_plate_independent.txt
"""
import math
import numpy as np

Q, W, L, H = 100.0, 0.060, 0.060, 0.030
RHO, CP, MU, KA, PR = 1.1614, 1007.0, 1.846e-5, 0.0263, 0.707
SMIN = 0.8e-3
NZ = 60


def geom(t, Nf):
    s = (W - Nf * t) / (Nf - 1)
    return s, Nf - 1


# ------------------------------------------------------------------ hydraulics
def dp_S(s, u, sigma):
    Dh = 2 * s * H / (s + H)
    Re = RHO * u * Dh / MU
    b = s / H
    fRe = 24 * (1 - 1.3553 * b + 1.9467 * b**2 - 1.7012 * b**3 + 0.9564 * b**4 - 0.2537 * b**5)
    xp = L / (Dh * Re)
    fapp = math.sqrt((3.44 / math.sqrt(xp)) ** 2 + fRe**2) / Re
    Kc, Ke = 0.42 * (1 - sigma**2), (1 - sigma**2) ** 2
    return (4 * fapp * L / Dh + Kc + Ke) * RHO * u * u / 2, Re


def dp_B(s, u, sigma):
    # parallel plates, D_h = 2 s; Shah (1978) apparent friction for plates (constants from memory, UNSURE)
    Dh = 2 * s
    Re = RHO * u * Dh / MU
    xp = L / (Dh * Re)
    fappRe = 3.44 / math.sqrt(xp) + (24 + 0.674 / (4 * xp) - 3.44 / math.sqrt(xp)) / (1 + 0.000029 * xp**-2)
    fapp = fappRe / Re
    Kc, Ke = 0.42 * (1 - sigma**2), (1 - sigma**2) ** 2
    return (4 * fapp * L / Dh + Kc + Ke) * RHO * u * u / 2, RHO * u * (2 * s * H / (s + H)) / MU


def h_S(s, u):
    Re2s = RHO * u * 2 * s / MU
    xs = L / (2 * s * Re2s * PR)
    Nu = 7.55 + 0.024 * xs**-1.14 / (1 + 0.0358 * PR**0.17 * xs**-0.64)
    return Nu * KA / (2 * s)


def h_B(s, u):
    return 7.541 * KA / (2 * s)


SETS = {"S": (dp_S, h_S), "B": (dp_B, h_B)}


def solve_V(t, Nf, P, cset):
    s, Nch = geom(t, Nf)
    A = Nch * s * H
    sigma = Nch * s / W
    dpf = SETS[cset][0]
    f = lambda lv: math.log(math.exp(lv) * dpf(s, math.exp(lv) / A, sigma)[0]) - math.log(P)
    lo, hi = math.log(1e-6), math.log(0.2)
    if f(lo) > 0 or f(hi) < 0:
        return None
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    V = math.exp(0.5 * (lo + hi))
    dP, Re = dpf(s, V / A, sigma)
    return V, dP, Re


# ------------------------------------------------------------------ closures
def R_1d(t, Nf, k, V, h):
    s, Nch = geom(t, Nf)
    m = math.sqrt(2 * h / (k * t))
    eta = math.tanh(m * H) / (m * H)
    G = h * (eta * 2 * Nch * H * L + Nch * s * L)
    C = RHO * CP * V
    return 1.0 / (C * (1 - math.exp(-G / C))), eta, G / C


def system_2d(t, Nf, k, V, h, nz=NZ):
    """dTa/dx = A Ta + c  (T_root = 1, inlet 0).  Fin per face: k (t/2) Tf'' = h (Tf - Ta)."""
    s, Nch = geom(t, Nf)
    u = V / (Nch * s * H)
    dz = H / nz
    kt = k * t / 2.0
    # fin: M Tf = h Ta + b   (cell-centred, Dirichlet 1 at root face, adiabatic tip)
    M = np.zeros((nz, nz))
    b = np.zeros(nz)
    for j in range(nz):
        M[j, j] = h
        if j > 0:
            M[j, j] += kt / dz**2
            M[j, j - 1] -= kt / dz**2
        else:
            M[j, j] += kt / (dz * dz / 2)
            b[j] += kt / (dz * dz / 2)
        if j < nz - 1:
            M[j, j] += kt / dz**2
            M[j, j + 1] -= kt / dz**2
    Minv = np.linalg.inv(M)
    S = Minv * h            # Tf = S Ta + r
    r = Minv @ b
    g = 2 * h / (RHO * u * s * CP)     # two faces per channel
    gb = h / (RHO * u * CP * dz)       # base strip into bottom cell
    A = g * (S - np.eye(nz))
    c = g * r
    A[0, 0] -= gb
    c[0] += gb
    return A, c, u, s, Nch, dz, S, r


def R_2d(t, Nf, k, V, h, nz=NZ):
    A, c, u, s, Nch, dz, S, r = system_2d(t, Nf, k, V, h, nz)
    # steady state Ta_ss = -A^-1 c (= 1 everywhere); Ta(x) = Ta_ss + expm(A x)(0 - Ta_ss)
    Tss = -np.linalg.solve(A, c)
    lam, X = np.linalg.eig(A)
    E = (X @ np.diag(np.exp(lam * L)) @ np.linalg.inv(X)).real
    Ta_out = Tss - E @ Tss
    Qch = RHO * u * s * CP * dz * Ta_out.sum()
    return 1.0 / (Nch * Qch), Ta_out, float(np.max(np.abs(Tss - 1)))


def R_2d_march(t, Nf, k, V, h, nz=NZ, nx=4000):
    A, c, u, s, Nch, dz, S, r = system_2d(t, Nf, k, V, h, nz)
    dx = L / nx
    Ta = np.zeros(nz)
    Mi = np.linalg.inv(np.eye(nz) - dx * A)
    for _ in range(nx):
        Ta = Mi @ (Ta + dx * c)
    return 1.0 / (Nch * RHO * u * s * CP * dz * Ta.sum())


def designs(tlist):
    out = []
    for t in tlist:
        Nf = 6
        while (W - Nf * t) / (Nf - 1) >= SMIN - 1e-12:
            out.append((t, Nf))
            Nf += 1
    return out


CU_T = [0.3e-3, 0.4e-3, 0.5e-3, 0.6e-3, 0.8e-3, 1.0e-3]
AL_T = [0.4e-3, 0.5e-3, 0.6e-3, 0.8e-3, 1.0e-3, 1.2e-3, 1.5e-3, 2.0e-3]


def optimise(k, P, cset, closure, tlist):
    hfun = SETS[cset][1]
    best = None
    for t, Nf in designs(tlist):
        sol = solve_V(t, Nf, P, cset)
        if sol is None:
            continue
        V, dP, Re = sol
        if Re >= 2300:
            continue
        s, Nch = geom(t, Nf)
        h = hfun(s, V / (Nch * s * H))
        R1, eta, NTU = R_1d(t, Nf, k, V, h)
        R = R1 if closure == "1D" else R_2d(t, Nf, k, V, h)[0]
        if best is None or R < best[0]:
            best = (R, t, Nf, s, V, dP, Re, eta, NTU, R1)
    return best


def main():
    print("RV1 independent plate-fin check  (level: derived, unverified)")

    # --- (0) self-checks of the 2-D closure
    print("\n=== (0) 2-D closure self-checks ===")
    t, Nf, k = 0.3e-3, 38, 390.0
    V, dP, Re = solve_V(t, Nf, 0.1, "S")
    s, Nch = geom(t, Nf)
    h = h_S(s, V / (Nch * s * H))
    R1 = R_1d(t, Nf, k, V, h)[0]
    R2, Taout, sserr = R_2d(t, Nf, k, V, h)
    R2m = R_2d_march(t, Nf, k, V, h)
    R2n = R_2d(t, Nf, k, V, h, nz=120)[0]
    R2iso1 = R_1d(t, Nf, 1e12, V, h)[0]
    R2iso2 = R_2d(t, Nf, 1e12, V, h)[0]
    print("Cu 38 x 0.3 mm at 0.1 W (set S): V=%.4e m3/s dP=%.3f Pa Re=%.1f h=%.2f W/m2K" % (V, dP, Re, h))
    print("  R_1D (eps-NTU, mixed) = %.5f K/W ; R_2D (unmixed, eig) = %.5f ; R_2D marching nx=4000 = %.5f ; R_2D nz=120 = %.5f" % (R1, R2, R2m, R2n))
    print("  steady-state check max|Ta_ss-1| = %.2e ; isothermal fins (k=1e12): R_1D=%.5f R_2D=%.5f (differ only through the base-strip treatment)" % (sserr, R2iso1, R2iso2))
    print("  outlet air temperature (per unit root excess): bottom %.3f, mid %.3f, tip %.3f" % (Taout[0], Taout[NZ // 2], Taout[-1]))

    # --- (a) optimisation, set S, 1D closure (reproduction of S2 by independent code)
    for P in (0.03, 0.1, 0.3):
        print("\n=== P_air = %g W ===" % P)
        for cset in ("S", "B"):
            for closure in ("1D", "2D"):
                ref = optimise(390.0, P, cset, closure, CU_T)
                line = "set %s %s: Cu R=%.4f (t=%.1f mm Nf=%d s=%.3f mm V=%.3e dP=%.1f Re=%.0f eta=%.3f NTU=%.2f)" % (
                    cset, closure, ref[0], ref[1] * 1e3, ref[2], ref[3] * 1e3, ref[4], ref[5], ref[6], ref[7], ref[8])
                print(line)
                rats = []
                for k in (200, 180, 150, 120, 100):
                    b = optimise(float(k), P, cset, closure, AL_T)
                    rats.append("k=%d %.4f (x%.3f, t=%.1f Nf=%d)" % (k, b[0], b[0] / ref[0], b[1] * 1e3, b[2]))
                print("     Al: " + "; ".join(rats))

    # --- (b) with the same minimum thickness 0.3 mm for both (removes the t_min asymmetry), 2D, set S, 0.1 W
    print("\n=== equal t_min = 0.3 mm, set S, 0.1 W ===")
    TL = [0.3e-3, 0.35e-3, 0.4e-3, 0.5e-3, 0.6e-3, 0.8e-3, 1.0e-3]
    for closure in ("1D", "2D"):
        ref = optimise(390.0, 0.1, "S", closure, TL)
        out = []
        for k in (200, 150, 100):
            b = optimise(float(k), 0.1, "S", closure, TL)
            out.append("k=%d x%.3f" % (k, b[0] / ref[0]))
        print("%s: Cu %.4f ; %s" % (closure, ref[0], "; ".join(out)))


if __name__ == "__main__":
    main()
