"""S5 review, check RV5: porous-electrode utilisation and the pore-ionic overpotential floor (claims C2.6, C2.7),
plus the arithmetic of C2.3, C2.4 and C2.10.

Level: derived (unverified).  numpy + standard library; does not import gms_core.
Model: one-dimensional porous electrode, metal phase equipotential, electrolyte conductivity
kappa_eff = kappa (eps (1 - eps_g))^1.5 (Bruggeman, as in S2), kinetics either Tafel a j0 exp(eta/b) or
symmetric Butler-Volmer 2 a j0 sinh(eta/b), b = RT/(alpha F).  Solved by finite volumes on a geometric grid
with Newton iteration (different method from S2's closed form and RK4 shooting).
  kappa_eff d2(eta)/dy2 = a r(eta);  -kappa_eff deta/dy = J at the separator (y = 0); deta/dy = 0 at the back.
Utilisation E = J / (a L r(eta_front)); for Tafel kinetics E depends only on delta = J L/(kappa_eff b).
Run: python3 rv5_electrode.py > outputs/rv5_electrode.txt
"""
import math
import numpy as np

R, F, T = 8.314462, 96485.33, 298.15
B = R * T / (0.5 * F)          # natural-log slope, alpha = 0.5


def grid(Lc, n=1500, ratio=1.004):
    w = ratio ** np.arange(n)
    w = w / w.sum() * Lc
    return w                    # cell widths, finest at the separator (y = 0)


def solve(J, Lc, kef, aj0, b, kin="tafel", n=1500):
    w = grid(Lc, n)
    yc = np.cumsum(w) - w / 2
    dists = np.diff(yc)
    G = kef / dists             # conductance between cell centres
    eta = np.full(n, b * 2.0)
    if kin == "tafel":
        eta[:] = b * math.log(max(J / (aj0 * Lc), 1e-30)) + b
    for it in range(200):
        if kin == "tafel":
            r = aj0 * np.exp(eta / b)
            dr = r / b
        else:
            r = 2 * aj0 * np.sinh(eta / b)
            dr = 2 * aj0 * np.cosh(eta / b) / b
        # residual: flux balance per cell (current leaving electrolyte into metal = a r w)
        Fv = r * w
        Fv[0] -= J                                  # ionic current entering cell 0 from the separator
        flux = G * (eta[:-1] - eta[1:])             # ionic current from cell i to i+1 (eta falls inward)
        Fv[:-1] += flux
        Fv[1:] -= flux
        # Jacobian tridiagonal
        d = dr * w
        d[:-1] += G
        d[1:] += G
        lo = -G.copy()
        up = -G.copy()
        # Thomas
        cp = np.zeros(n - 1)
        dp = np.zeros(n)
        cp[0] = up[0] / d[0]
        dp[0] = -Fv[0] / d[0]
        for i in range(1, n):
            den = d[i] - lo[i - 1] * cp[i - 1]
            if i < n - 1:
                cp[i] = up[i] / den
            dp[i] = (-Fv[i] - lo[i - 1] * dp[i - 1]) / den
        dx = np.zeros(n)
        dx[-1] = dp[-1]
        for i in range(n - 2, -1, -1):
            dx[i] = dp[i] - cp[i] * dx[i + 1]
        dx = np.clip(dx, -5 * b, 5 * b)
        eta += dx
        if np.max(np.abs(dx)) < 1e-12:
            break
    # front value: extrapolate to the separator face (half cell)
    eta_f = eta[0] + J * (w[0] / 2) / kef
    if kin == "tafel":
        rf = aj0 * math.exp(eta_f / b)
    else:
        rf = 2 * aj0 * math.sinh(eta_f / b)
    return eta_f, J / (Lc * rf), it


def E_closed(delta):
    lo, hi = 1e-12, math.pi / 2 - 1e-12
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 2 * mid * math.tan(mid) < delta:
            lo = mid
        else:
            hi = mid
    th = 0.5 * (lo + hi)
    return math.sin(2 * th) / (2 * th)


keff = lambda kap, eps, eg: kap * (eps * (1 - eg)) ** 1.5
J = 1.0e4
print("RV5 porous electrode  (level: derived, unverified)")
print("b(alpha=0.5, 298.15 K) = %.5f V" % B)

print("\n=== (a) utilisation, 1.6 mm foam, 30 wt% KOH kappa = 62 S/m (assumed), eps = 0.9, Tafel kinetics ===")
for b, lab in ((B, "alpha=0.5"), (0.04 / math.log(10), "40 mV/dec")):
    for eg in (0.0, 0.3):
        kef = keff(62, 0.9, eg)
        delta = J * 1.6e-3 / (kef * b)
        ef, E, it = solve(J, 1.6e-3, kef, 1.0, b, "tafel")
        print("%-10s eps_g=%.1f kappa_eff=%.2f delta=%.3f  E_FV=%.4f  E_closed=%.4f  (Newton its %d)" % (lab, eg, kef, delta, E, E_closed(delta), it))

print("\n=== (b) thick electrode (L = 16 mm), sinh kinetics: eta_front against b acosh(1 + J^2/(4 kappa_eff a j0 b)) ===")
for av, j0, kap, eps, eg in ((6.25e5, 1.0, 140, 0.9, 0.3), (6.25e5, 0.1, 62, 0.9, 0.0), (2e6, 0.1, 62, 0.5, 0.0), (2e7, 0.1, 62, 0.5, 0.0), (2e7, 1.0, 140, 0.5, 0.3)):
    kef = keff(kap, eps, eg)
    ef, E, it = solve(J, 0.016, kef, av * j0, B, "sinh", n=2500)
    emin = B * math.acosh(1 + J * J / (4 * kef * av * j0 * B))
    Reff = J / (2 * j0 * math.sinh(emin / B))
    print("a_v=%.3g j0=%g kappa=%g eps=%.1f eg=%.1f: eta_FV=%.5f V, eta_min closed=%.5f V (rel %.1e), effective roughness %.0f" % (
        av, j0, kap, eps, eg, ef, emin, ef / emin - 1, Reff))

print("\n=== (c) a_v j0 needed for eta_min = eta(Pt/C alkaline, R_f 100) ===")
eta_pt = B * math.asinh(1.0 / 100 / (2 * 6e-4))
print("Pt/C alkaline reference (j0 6e-4 A/cm2 per real area, R_f 100, 1 A/cm2): %.4f V" % eta_pt)
for kap, eps, eg in ((62, 0.9, 0.0), (140, 0.9, 0.0), (62, 0.5, 0.0), (62, 0.5, 0.3), (20, 0.5, 0.3)):
    kef = keff(kap, eps, eg)
    need = J * J / (4 * kef * B * (math.cosh(eta_pt / B) - 1))
    print("kappa=%3g eps=%.1f eg=%.1f kappa_eff=%.2f: a_v j0 >= %.3e A/m3 ; pore size at j0=1e-5 A/cm2 (0.1 A/m2) for a_v = 4 eps/d_p: d_p = %.3g um" % (
        kap, eps, eg, kef, need, 4 * eps / (need / 0.1) * 1e6))
eta_pt_acid = B * math.asinh(1.0 / 100 / (2 * 0.06))
print("Pt/C acid reference (j0 0.06, R_f 100): %.5f V -> a_v j0 >= %.3e A/m3 at kappa_eff = 52.9 S/m" % (
    eta_pt_acid, J * J / (4 * keff(62, 0.9, 0) * B * (math.cosh(eta_pt_acid / B) - 1))))

print("\n=== (d) arithmetic of C2.3, C2.4, C2.10 ===")
for j0pt, rfpt, lab in ((6e-4, 1, "flat Pt alkali"), (6e-4, 100, "Pt/C alkali"), (0.06, 100, "Pt/C acid 298 K"), (0.07, 100, "Pt/C acid 298 K hi")):
    print("%-20s required R_f for candidate j0 1e-5 / 1e-6: %.3g / %.3g" % (lab, rfpt * j0pt / 1e-5, rfpt * j0pt / 1e-6))
for j0, Rf, TT in ((0.06, 100, 298.15), (0.06, 200, 298.15), (0.26, 100, 353.15), (0.26, 200, 353.15)):
    bb = R * TT / (0.5 * F)
    print("Pt/C acid HER at 1 A/cm2: j0=%.2f R_f=%d T=%.0f K: eta = %.2f mV" % (j0, Rf, TT, 1e3 * bb * math.asinh(1.0 / Rf / (2 * j0))))
jl = 1.0 / 50
j0_sym = jl / (2 * math.sinh(0.27 / B))
j0_taf = jl / 10 ** (0.27 / 0.032)
print("C2.10: NiFe 0.27 V at 1 A/cm2, R_f 50: j0 (symmetric alpha 0.5) = %.3e ; j0 (32 mV/dec Tafel) = %.3e ; ratio %.3g" % (j0_sym, j0_taf, j0_sym / j0_taf))

print("\n=== (e) Lu and Zhao 2015 data as read by S5 (Europe PMC full text): electrolyte dependence ===")
print("10 M KOH, from the Tafel plot, 75 % iR-compensated polarisation curve: 0.24 V at 0.5 A/cm2, 0.27 V at 1 A/cm2")
eta30 = 0.34 + 0.032 * math.log10(1.0 / 0.3)
print("30 wt%% KOH: 0.27 V at 0.1 A/cm2, 0.34 V at 0.3 A/cm2, 32 mV/dec -> extrapolated to 1 A/cm2: %.3f V (S5 extrapolation)" % eta30)
