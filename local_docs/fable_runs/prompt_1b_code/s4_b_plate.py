"""S4 follow-up for rows B02, B05 (and PF5, B2.9).  Level: derived (unverified).

Purpose (stage S4, finaliser; S2 scripts are not edited):
 (a) diagnose the B05 (iii) FAIL: PF12 / X1 ratio at the plate optima, with the real fins and with
     isothermal fins (k -> 1e12), to separate the correlation mismatch from the fin-coupling mismatch;
     and the Al/Cu ratio when the designs are optimised under PF12 instead of PF8/X1.
 (b) separate conductivity from the minimum-thickness limit in the Al/Cu ratio: optimum with the plan's
     limits (Cu 0.3 mm, Al 0.4 mm), with equal limits (0.4 and 0.3 mm) and with a free thickness grid.
     Conductivities include the values S3 read for AlSi10Mg (100-130 as built, 155-166 heat treated).
 (c) B02 with the 0.8 mm gap limit enforced: fins that fit at the equal-efficiency thickness.
 (d) PF5 length scale: apparent friction factor built on D_h and on sqrt(A) for the B03 design.
Inputs: gms_core constants and models (plan sections 3.0, 3.1).  Assumptions as in the plan.
Run: python3 s4_b_plate.py > outputs/s4_b_plate.txt
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *  # noqa: F401,F403

print("S4 plate-fin follow-up  (level: derived, unverified)")


def sweep(k, tlist, smin=S_MIN):
    out = []
    for t in tlist:
        Nf = 6
        while (W - Nf * t) / (Nf - 1) >= smin - 1e-12:
            out.append(PF(t, Nf, float(k)))
            Nf += 1
    return out


def best_by(designs, P, key="R_fa"):
    bestv = None
    for d in designs:
        V = V_at_P(d, P)
        if V is None:
            continue
        r = d.eval(V)
        if r["excluded"]:
            continue
        if bestv is None or r[key] < bestv[0]:
            bestv = (r[key], r, d)
    return bestv


# ---------------------------------------------------------------- (a)
head("(a) B05 (iii): PF12 / X1 ratio at the X1 optima, real fins and isothermal fins")
print("   k    P_air   design                      eta   NTU   R_X1     R_PF12   ratio   | isothermal fins: R_X1  R_PF12  ratio")
worst_iso = 0.0
rows = []
for P in P_SET:
    for k in [390, 200, 180, 150, 120, 100]:
        R, r, d = best(plate_designs(float(k)), P)
        diso = PF(d.t, d.Nf, 1e12)
        ri = diso.eval(r["V"])
        ratio = r["R_faT"] / r["R_fa"]
        ratio_iso = ri["R_faT"] / ri["R_fa"]
        worst_iso = max(worst_iso, abs(ratio_iso - 1))
        rows.append((k, P, r["eta"], ratio, ratio_iso))
        print("  %3d  %5.2f   t=%.2f Nf=%2d s=%.3f mm   %.3f %.3f  %.4f   %.4f   %.3f   |   %.4f  %.4f  %.3f" % (
            k, P, d.t * 1e3, d.Nf, d.s * 1e3, r["eta"], r["NTU"], r["R_fa"], r["R_faT"], ratio, ri["R_fa"], ri["R_faT"], ratio_iso))
print("max |ratio_iso - 1| over the 30 optima = %.4f ; range of ratio_iso = %.3f to %.3f" % (
    worst_iso, min(x[4] for x in rows), max(x[4] for x in rows)))
print("range of real-fin ratio = %.3f to %.3f" % (min(x[3] for x in rows), max(x[3] for x in rows)))
# correlation of (ratio/ratio_iso - 1) with (1 - eta)
xs = [1 - x[2] for x in rows]
ys = [x[3] / x[4] - 1 for x in rows]
n = len(xs)
mx, my = sum(xs) / n, sum(ys) / n
cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
r_p = cov / math.sqrt(sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys))
print("Pearson correlation of (ratio/ratio_iso - 1) with (1 - eta_f) over the 30 optima: %.3f" % r_p)
print("fin-coupling part ratio/ratio_iso: min %.3f max %.3f" % (min(a / b for _, _, _, a, b in rows), max(a / b for _, _, _, a, b in rows)))

head("(a2) Al/Cu ratio at 0.1 W when each design is optimised under PF12 instead of PF8/X1")
bcu = best_by(plate_designs(390.0), 0.1, "R_faT")
print("Cu  PF12-optimum: R_PF12=%.4f (X1 value of that design %.4f)  %s" % (bcu[0], bcu[1]["R_fa"], bcu[2].label()))
xcu = best(plate_designs(390.0), 0.1)[0]
for k in [200, 180, 150, 120, 100]:
    b = best_by(plate_designs(float(k)), 0.1, "R_faT")
    x = best(plate_designs(float(k)), 0.1)[0]
    print("k=%3d PF12-optimum: R_PF12=%.4f  ratio to Cu (PF12) = %.3f   [X1 optimum ratio = %.3f]  %s" % (
        k, b[0], b[0] / bcu[0], x / xcu, b[2].label()))

# ---------------------------------------------------------------- (b)
head("(b) Al/Cu ratio at equal P_air: plan thickness limits, equal limits, free thickness")
KLIST = [390, 200, 180, 166, 165, 160, 155, 150, 130, 120, 115, 110, 100]
tfree = [round(0.05e-3 * i, 7) for i in range(1, 41)]          # 0.05 ... 2.00 mm
rules = [
    ("plan (Cu t>=0.3, Al t>=0.4)", lambda k: CU_T if k >= 390 else AL_T),
    ("equal t>=0.4 mm", lambda k: [t for t in tfree if t >= 0.4e-3 - 1e-12]),
    ("equal t>=0.3 mm", lambda k: [t for t in tfree if t >= 0.3e-3 - 1e-12]),
    ("free t (0.05-2.0 mm grid)", lambda k: tfree),
]
for P in [0.03, 0.1, 0.3]:
    print("\nP_air = %g W" % P)
    for name, tl in rules:
        ref = None
        print("  rule: %s" % name)
        for k in KLIST:
            b = best(sweep(k, tl(k)), P)
            if k == 390:
                ref = b[0]
            d, r = b[2], b[1]
            edge = "t at grid minimum" if abs(d.t - min(tl(k))) < 1e-12 else "t interior"
            gap = "; gap limit active" if (W - (d.Nf + 1) * d.t) / d.Nf < S_MIN else ""
            print("     k=%3d  R_fa=%.4f  ratio to Cu=%.3f  t=%.2f mm Nf=%2d s=%.3f mm eta=%.3f NTU=%.3f  (%s%s)" % (
                k, b[0], b[0] / ref, d.t * 1e3, d.Nf, d.s * 1e3, r["eta"], r["NTU"], edge, gap))

# ---------------------------------------------------------------- (c)
head("(c) B02 with the gap limit: fins that fit at the equal-efficiency thickness (s >= 0.8 mm)")
tCu, Nf0 = 0.4e-3, 32
print("Cu: t=0.40 mm, N_f=32, gap %.3f mm, open-area ratio %.3f" % ((W - Nf0 * tCu) / (Nf0 - 1) * 1e3, 1 - Nf0 * tCu / W))
for k in [100, 120, 150, 180, 200]:
    tAl = tCu * K_CU / k
    Nmax = int(math.floor((W + S_MIN) / (tAl + S_MIN) + 1e-9))
    N = min(Nf0, Nmax)
    s = (W - N * tAl) / (N - 1)
    print("k=%3d  t_Al=%.3f mm  N_f(max at 0.8 mm gap)=%2d  used N_f=%2d  gap=%.3f mm  open-area ratio=%.3f  fin area relative to Cu=%.3f" % (
        k, tAl * 1e3, Nmax, N, s * 1e3, 1 - N * tAl / W, (N - 1) / (Nf0 - 1)))
    d = PF(tAl, N, float(k))
    V = V_at_P(d, 0.1)
    r = d.eval(V)
    print("        at 0.1 W: R_fa=%.4f K/W eta=%.3f  (plate optimum for this k at 0.1 W: %.4f)" % (
        r["R_fa"], r["eta"], best(plate_designs(float(k)), 0.1)[0]))

# ---------------------------------------------------------------- (d)
head("(d) PF5 length scale: f_app built on D_h and on sqrt(A)")
d = PF(0.4e-3, 32, 390.0)
V = V_at_P(d, 0.1)
u = V / d.Aflow
s = d.s
Dh = 2 * s * H / (s + H)
Re = RHO * u * Dh / MU
b = s / H
fRe = 24 * (1 - 1.3553 * b + 1.9467 * b ** 2 - 1.7012 * b ** 3 + 0.9564 * b ** 4 - 0.2537 * b ** 5)
f_dh = math.sqrt((3.44 / math.sqrt(L / (Dh * Re))) ** 2 + fRe ** 2) / Re
sA = math.sqrt(s * H)
ReA = RHO * u * sA / MU
fReA = fRe * sA / Dh            # same Fanning factor, Reynolds number on sqrt(A)
f_sa = math.sqrt((3.44 / math.sqrt(L / (sA * ReA))) ** 2 + fReA ** 2) / ReA
print("B03 design: D_h=%.4e m, sqrt(A)=%.4e m, Re_Dh=%.1f, Re_sqrtA=%.1f" % (Dh, sA, Re, ReA))
print("f_app (D_h form)     = %.8f" % f_dh)
print("f_app (sqrt(A) form) = %.8f   relative difference %.2e" % (f_sa, f_sa / f_dh - 1))
print("developing-flow term alone: 3.44/sqrt(Re_L) = %.8f (Re_L = rho u L/mu = %.1f); D_h form gives %.8f" % (
    3.44 / math.sqrt(RHO * u * L / MU), RHO * u * L / MU, 3.44 / math.sqrt(L / (Dh * Re)) / Re))
eps = s / H
fReA_MY = 12.0 / (math.sqrt(eps) * (1 + eps) * (1 - 192 * eps / math.pi ** 5 * math.tanh(math.pi / (2 * eps))))
print("independent comparison (formula from memory, UNSURE): Muzychka-Yovanovich rectangular-duct value")
print("   fRe_sqrtA = 12/[sqrt(eps)(1+eps)(1-192 eps/pi^5 tanh(pi/(2 eps)))] = %.4f at eps = s/H = %.4f" % (fReA_MY, eps))
print("   Shah-London polynomial converted to sqrt(A): %.4f   relative difference %.2e" % (fReA, fReA_MY / fReA - 1))
print("The equality of the two f_app values above is an identity (same Fanning factor, consistent conversion);")
print("the only non-trivial comparison is the fully developed constant in the two lines just above.")
print("Note: with the Fanning factor defined on wall shear, both terms are independent of the length scale,")
print("      so PF5 gives the same f_app on D_h and on sqrt(A) provided fRe is converted consistently.")
print("      The fully developed constant itself (Shah-London polynomial) is still not confirmed by S3.")
