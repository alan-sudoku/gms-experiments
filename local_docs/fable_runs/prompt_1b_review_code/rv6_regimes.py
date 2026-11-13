"""S5 review, check RV6: regimes and fair comparisons the answer did not compute.

Level: derived (unverified).  numpy + standard library.  Uses RV1's independent plate-fin model (set S, 1-D
closure, same correlations as S2) and a copy of RV3's Fourier spreading solution.
  (a) Same fan instead of same air power, with the designs RE-OPTIMISED on each fan curve (S2's B13 kept the
      0.1 W designs).  Linear fan curves dP = dP0 (1 - V/Vmax): (30 Pa, 8 L/s), (60 Pa, 12 L/s), (150 Pa, 20 L/s)
      (assumed; not fan data).
  (b) Mass-limited instead of volume-limited: copper sink with total mass <= the Al k=150 plate optimum
      (0.1192 kg), base thickness free (1-5 mm) with the envelope height kept at 35 mm (fin height 35 mm - t_b);
      uniform source and 20 x 20 mm source.
  (c) Equal envelope with a thicker Al base: S2's B14 10 mm-base case kept H = 30 mm fins (envelope 40 mm).
      Here: t_b = 10 mm and fin height 25 mm, re-optimised.
  (d) Natural convection order of magnitude (Bar-Cohen and Rohsenow optimum-spacing form, constants from
      memory: s_opt = 2.714 (L nu alpha / (g beta dT))^(1/4), Nu_s ~ 1.31 at the optimum; UNSURE).
Run: python3 rv6_regimes.py > outputs/rv6_regimes.txt
"""
import math
import numpy as np
import rv1_plate_independent as rv

Q, T0 = 100.0, 298.15
AP = 0.06 * 0.06


def fourier_max(k, tb, R0, nmodes=400):
    LX = 0.06
    CS = 0.02
    h = 1.0 / (R0 * AP)
    q0 = Q / (CS * CS)
    m = np.arange(nmodes)
    lam = m * math.pi / LX
    x1, x2 = LX / 2 - CS / 2, LX / 2 + CS / 2
    a = np.zeros(nmodes)
    a[0] = CS / LX
    a[1:] = 2.0 / (m[1:] * math.pi) * (np.sin(m[1:] * math.pi * x2 / LX) - np.sin(m[1:] * math.pi * x1 / LX))
    Bm = np.sqrt(lam[:, None] ** 2 + lam[None, :] ** 2)
    Bm[0, 0] = 1.0
    th = np.tanh(Bm * tb)
    phi = (k * Bm + h * th) / (k * Bm * th + h)
    A = q0 * np.outer(a, a) / (k * Bm) * phi
    A[0, 0] = Q / AP * (tb / k + 1.0 / h)
    c = np.cos(m * math.pi / 2)
    return float(c @ A @ c) / Q - R0          # base resistance to the peak


def fan_opt(k, tlist, dp0, vmax):
    best = None
    for t, Nf in rv.designs(tlist):
        s, Nch = rv.geom(t, Nf)
        A = Nch * s * rv.H
        sigma = Nch * s / rv.W
        f = lambda V: rv.dp_S(s, V / A, sigma)[0] - dp0 * (1 - V / vmax)
        lo, hi = 1e-9, vmax
        if f(lo) > 0 or f(hi) < 0:
            continue
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if f(mid) < 0:
                lo = mid
            else:
                hi = mid
        V = 0.5 * (lo + hi)
        dP, Re = rv.dp_S(s, V / A, sigma)
        if Re >= 2300:
            continue
        h = rv.h_S(s, V / A)
        R = rv.R_1d(t, Nf, k, V, h)[0]
        if best is None or R < best[0]:
            best = (R, t, Nf, V, dP)
    return best


print("RV6 regimes  (level: derived, unverified)")
print("\n=== (a) same fan, designs re-optimised on the fan curve ===")
for dp0, vmax in ((30.0, 0.008), (60.0, 0.012), (150.0, 0.020)):
    cu = fan_opt(390.0, rv.CU_T, dp0, vmax)
    out = []
    for k in (150, 100):
        al = fan_opt(float(k), rv.AL_T, dp0, vmax)
        out.append("Al k=%d R=%.4f (x%.3f, Nf=%d, P_air=%.3f W)" % (k, al[0], al[0] / cu[0], al[2], al[3] * al[4]))
    print("fan (%3.0f Pa, %4.1f L/s): Cu R=%.4f (Nf=%d, P_air=%.3f W) ; %s" % (dp0, vmax * 1e3, cu[0], cu[2], cu[3] * cu[4], " ; ".join(out)))

print("\n=== (b) mass-limited: Cu sink at the Al k=150 optimum's mass (0.1192 kg), 0.1 W air power, envelope 35 mm ===")
MLIM = 0.1192
H_SAVE = rv.H
res = []
for tb in (1.0e-3, 1.5e-3, 2.0e-3, 3.0e-3, 5.0e-3):
    rv.H = 0.035 - tb
    mbase = 8960 * AP * tb
    for t, Nf in rv.designs(rv.CU_T):
        mass = mbase + 8960 * Nf * t * rv.H * rv.L
        if mass > MLIM:
            continue
        sol = rv.solve_V(t, Nf, 0.1, "S")
        if sol is None or sol[2] >= 2300:
            continue
        V = sol[0]
        s, Nch = rv.geom(t, Nf)
        h = rv.h_S(s, V / (Nch * s * rv.H))
        Rfa = rv.R_1d(t, Nf, 390.0, V, h)[0]
        res.append((Rfa + tb / (390 * AP), Rfa + fourier_max(390.0, tb, Rfa), tb, t, Nf, mass, Rfa))
rv.H = H_SAVE
bu = min(res, key=lambda x: x[0])
bs = min(res, key=lambda x: x[1])
print("best Cu, uniform source:       R_total=%.4f (R_fa=%.4f, t_b=%.1f mm, t=%.1f mm, Nf=%d, mass %.4f kg)" % (bu[0], bu[6], bu[2] * 1e3, bu[3] * 1e3, bu[4], bu[5]))
print("best Cu, 20 x 20 mm source:    R_peak =%.4f (R_fa=%.4f, t_b=%.1f mm, t=%.1f mm, Nf=%d, mass %.4f kg)" % (bs[1], bs[6], bs[2] * 1e3, bs[3] * 1e3, bs[4], bs[5]))
Ral = 0.30437
print("Al k=150 plate optimum (5 mm base, 30 mm fins, 0.1192 kg): uniform %.4f ; 20 mm source peak %.4f" % (
    Ral + 0.005 / (150 * AP), Ral + fourier_max(150.0, 0.005, Ral)))

print("\n=== (c) equal envelope (35 mm), Al k=150 with 10 mm base and 25 mm fins, 0.1 W ===")
rv.H = 0.025
b = rv.optimise(150.0, 0.1, "S", "1D", rv.AL_T)
rv.H = H_SAVE
print("Al k=150, t_b 10 mm, H 25 mm: R_fa=%.4f (Nf=%d t=%.1f mm) ; peak with 20 mm source = %.4f ; vs t_b 5 mm/H 30 mm: %.4f" % (
    b[0], b[2], b[1] * 1e3, b[0] + fourier_max(150.0, 0.010, b[0]), Ral + fourier_max(150.0, 0.005, Ral)))
print("Cu reference (t_b 5 mm, H 30 mm) peak with 20 mm source: %.4f" % (0.26794 + fourier_max(390.0, 0.005, 0.26794)))

print("\n=== (d) natural convection, vertical fins 60 mm tall, 30 mm deep, dT = 50 K ===")
nu, alpha, kair, g = 1.589e-5, 2.25e-5, 0.0263, 9.81
dT = 50.0
beta = 1 / (T0 + dT / 2)
sopt = 2.714 * (0.06 * nu * alpha / (g * beta * dT)) ** 0.25
for t in (0.3e-3, 1.0e-3):
    Nf = int((0.06 + sopt) / (sopt + t))
    hnc = 1.31 * kair / sopt
    A = 2 * Nf * 0.03 * 0.06
    print("s_opt=%.2f mm, t=%.1f mm, Nf=%d, h=%.2f W/m2K, area %.4f m2 -> R >= %.2f K/W (isothermal fins), dT at 100 W >= %.0f K" % (
        sopt * 1e3, t * 1e3, Nf, hnc, A, 1 / (hnc * A), 100 / (hnc * A)))
