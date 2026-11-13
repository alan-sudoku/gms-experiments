"""S5 review, check RV4: gyroid porous-fin model, chi thresholds (claim B2.6), independent re-implementation.

Level: derived (unverified).  numpy + standard library; does not import gms_core.
Model (as stated in the plan/answer, re-derived here): sheet gyroid, wetted area per volume a_sf = 2*3.0915/a,
porosity phi = 1 - rho_bar, D_h = 4 phi / a_sf, interstitial velocity u = V/(phi W H),
Darcy friction f_D = c_f (133.33/Re_h + 2.333) (Ergun rewritten on D_h; I re-derived the two constants by hand),
h = chi (f_D/4) rho u c_p Pr^(-2/3), porous fin m = sqrt(h a_sf / k_eff), eps-NTU closure as for plates.
Checks:
  (a) chi_min against the Cu plate optimum (0.26794) and the Al k=150 plate optimum (0.30437) at 0.1 W,
      c_f in {1, 0.3, 0.1}, cell a <= 10 mm (three cells in the height), relative density 0.05-0.5.
  (b) Sensitivity to k_eff: Hashin-Shtrikman upper bound 2 rho/(3 - rho) (used by S2) against rho/2 and rho/3
      (assumed lower values for a sheet TPMS; UNSURE, no source read).
  (c) Plate-fin optimum's own chi (j/f_app incl. developing flow, excluding entrance/exit losses) for context.
Run: python3 rv4_gyroid.py > outputs/rv4_gyroid.txt
"""
import math

Q, W, L, H = 100.0, 0.060, 0.060, 0.030
RHO, CP, MU, KA, PR = 1.1614, 1007.0, 1.846e-5, 0.0263, 0.707
SG = 3.0915


def gy_R(a, rb, k, cf, chi, P, kfac="HS"):
    asf = 2 * SG / a
    phi = 1 - rb
    Dh = 4 * phi / asf
    A = phi * W * H

    def dp(V):
        u = V / A
        Re = RHO * u * Dh / MU
        return cf * (133.33 / Re + 2.333) * (L / Dh) * RHO * u * u / 2
    lo, hi = math.log(1e-7), math.log(0.5)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if math.exp(mid) * dp(math.exp(mid)) < P:
            lo = mid
        else:
            hi = mid
    V = math.exp(0.5 * (lo + hi))
    u = V / A
    Re = RHO * u * Dh / MU
    fD = cf * (133.33 / Re + 2.333)
    h = chi * fD / 4 * RHO * u * CP * PR ** (-2 / 3)
    keff = {"HS": k * 2 * rb / (3 - rb), "half": k * rb / 2, "third": k * rb / 3}[kfac]
    m = math.sqrt(h * asf / keff)
    eta = math.tanh(m * H) / (m * H)
    G = h * (eta * asf * W * L * H + phi * W * L)
    C = RHO * CP * V
    return 1 / (C * (1 - math.exp(-G / C))), Re


A_SET = [2e-3, 2.5e-3, 3e-3, 4e-3, 5e-3, 6e-3, 8e-3, 10e-3]
RB_SET = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]


def best(k, cf, chi, P, kfac):
    out = None
    for a in A_SET:
        for rb in RB_SET:
            if rb * a / SG < 0.3e-3:
                continue
            R, Re = gy_R(a, rb, k, cf, chi, P, kfac)
            if out is None or R < out[0]:
                out = (R, a, rb, Re)
    return out


def chi_min(k, cf, P, target, kfac):
    if best(k, cf, 1.0, P, kfac)[0] > target:
        return None
    lo, hi = 0.01, 1.0
    while hi - lo > 1e-4:
        mid = 0.5 * (lo + hi)
        if best(k, cf, mid, P, kfac)[0] > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


print("RV4 gyroid chi thresholds  (level: derived, unverified)")
TCU, TAL = 0.26794, 0.30437
for kfac in ("HS", "half", "third"):
    print("\n=== k_eff = %s, k_s = 150, P_air = 0.1 W, a <= 10 mm ===" % kfac)
    for cf in (1.0, 0.3, 0.1):
        c1 = chi_min(150.0, cf, 0.1, TCU, kfac)
        c2 = chi_min(150.0, cf, 0.1, TAL, kfac)
        b = best(150.0, cf, 0.35, 0.1, kfac)
        print("c_f=%.1f chi_min(Cu %.4f)=%s chi_min(Al plate %.4f)=%s ; at chi=0.35 best R=%.4f a=%.1f mm rho=%.2f Re_h=%.0f" % (
            cf, TCU, "none" if c1 is None else "%.3f" % c1, TAL, "none" if c2 is None else "%.3f" % c2, b[0], b[1] * 1e3, b[2], b[3]))

print("\n=== (c) chi of the plate-fin optima themselves (j / f_app, channel friction only) ===")
for nm, t, Nf, V in (("Cu 38 x 0.3 mm", 0.3e-3, 38, 3.8577e-3), ("Al k=150 37 x 0.4 mm", 0.4e-3, 37, 3.5615e-3)):
    s = (W - Nf * t) / (Nf - 1)
    u = V / ((Nf - 1) * s * H)
    Dh = 2 * s * H / (s + H)
    Re = RHO * u * Dh / MU
    b = s / H
    fRe = 24 * (1 - 1.3553 * b + 1.9467 * b**2 - 1.7012 * b**3 + 0.9564 * b**4 - 0.2537 * b**5)
    fapp = math.sqrt((3.44 / math.sqrt(L / (Dh * Re))) ** 2 + fRe**2) / Re
    Re2s = RHO * u * 2 * s / MU
    xs = L / (2 * s * Re2s * PR)
    Nu = 7.55 + 0.024 * xs**-1.14 / (1 + 0.0358 * PR**0.17 * xs**-0.64)
    h = Nu * KA / (2 * s)
    j = h / (RHO * u * CP) * PR ** (2 / 3)
    print("%-22s Re_Dh=%.0f f_app=%.4f j=%.4f chi=j/f_app=%.3f" % (nm, Re, fapp, j, j / fapp))

print("\n=== (d) chi_min when the plate targets use RV1's 2-D (height-unmixed) closure (Cu 0.2725, Al k=150 0.3159) ===")
print("    (the 1-D mixed-air closure suits a lattice better than a plate channel, so plate targets move up)")
for cf in (0.3, 0.1):
    c1 = chi_min(150.0, cf, 0.1, 0.27246, "HS")
    c2 = chi_min(150.0, cf, 0.1, 0.31590, "HS")
    print("c_f=%.1f HS: chi_min(Cu 2-D)=%s chi_min(Al plate 2-D)=%s" % (cf, "none" if c1 is None else "%.3f" % c1, "none" if c2 is None else "%.3f" % c2))
