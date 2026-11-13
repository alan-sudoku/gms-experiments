"""Rows C01-C05: Tafel slopes, Pt reference overpotentials, matching roughness, unequal slopes, OER extrapolation.

M-EC: b = R T/(alpha F); b10 = ln10 b; eta = b asinh(J/(2 R_f j0)); R_c = J/(2 j0c sinh(eta_ref/b_c)).
J and j0 in A/cm2 here.  All constants UNSURE in the plan are used as written.  Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *


def bslope(alpha, T=298.15):
    return R_GAS * T / (alpha * F_CONST)


def eta_bv(J, Rf, j0, alpha, T=298.15):
    return bslope(alpha, T) * math.asinh(J / (2 * Rf * j0))


print("Rows C01-C05  (level: derived, unverified)")
head("C01 Tafel slopes")
print("%8s %6s %12s %12s" % ("T [K]", "alpha", "b [mV]", "b10 [mV]"))
KB, E_CH = 1.380649e-23, 1.602176634e-19
mx = 0
for T in (298.15, 353.15):
    for a in (0.5, 1.0, 1.5, 2.0):
        b = bslope(a, T)
        ref = KB * T / (a * E_CH)
        mx = max(mx, abs(b / ref - 1))
        print("%8.2f %6.1f %12.5f %12.5f" % (T, a, b * 1e3, math.log(10) * b * 1e3))
check("C01 b agrees with k_B T/(alpha e) (independent CODATA 2018 constants) within 1e-6 rel", mx < 1e-6, "max rel diff %.3e" % mx)
b10 = math.log(10) * bslope(1.0) * 1e3
check("C01 b10(298.15 K, alpha=1) = 59.16 mV within 0.02 mV", abs(b10 - 59.16) < 0.02, "%.5f mV" % b10)
check("C01 hand: b = 51.39 mV at alpha=0.5, 298.15 K (to 0.01 mV)", abs(bslope(0.5) * 1e3 - 51.39) < 0.01, "%.5f mV" % (bslope(0.5) * 1e3))

head("C02 Pt reference overpotential at J = 1 A/cm2")
J = 1.0
scen = {"P1": 0.2, "P2": 6.0e-4}
print_inputs(alpha=0.5, T=298.15, J=J, P1_j0=0.2, P2_j0=6e-4, Rf=[1, 100, 200])
eta_ref = {}
b = bslope(0.5)
for sc, j0 in scen.items():
    for Rf in (1, 100, 200):
        e = eta_bv(J, Rf, j0, 0.5)
        eta_ref[(sc, Rf)] = e
        x = J / (2 * Rf * j0)
        tafel = b * math.log(J / (Rf * j0))
        lin = b * J / (2 * Rf * j0)
        msg = ""
        if x > 10:
            ok = abs(tafel / e - 1) < 0.01
            msg = "Tafel form %.5f V (rel diff %.3e) %s" % (tafel, tafel / e - 1, "PASS" if ok else "FAIL")
            if not ok: issue("C02 Tafel limit fails %s Rf=%g" % (sc, Rf))
        elif x < 0.1:
            ok = abs(lin / e - 1) < 0.01
            msg = "linear form %.6f V (rel diff %.3e) %s" % (lin, lin / e - 1, "PASS" if ok else "FAIL")
            if not ok: issue("C02 linear limit fails %s Rf=%g" % (sc, Rf))
        else:
            msg = "neither limit applies (J/(2 Rf j0)=%.3g)" % x
        print("  %s Rf=%3d: eta=%.6f V (J/(2 Rf j0)=%.4g); %s" % (sc, Rf, e, x, msg))
for key, val, tol in ((("P2", 1), 0.381, 0.01), (("P2", 100), 0.145, 0.01), (("P1", 1), 0.085, 0.01), (("P1", 100), 1.28e-3, 0.01)):
    e = eta_ref[key]
    ok = abs(e / val - 1) < tol
    print(("RANGE-OK    " if ok else "RANGE-MISS  ") + "eta %s Rf=%d = %.6g V vs hand %.4g (1%%)" % (key[0], key[1], e, val))
    if not ok: issue("C02 hand value miss %s Rf=%d: %.6g vs %.4g" % (key[0], key[1], e, val))
issue("C02 note: the P1/P2 limit checks compare the asinh form with its own Tafel/linear asymptotes; this is a valid limit check but depends on the same b")

head("C03 roughness needed to match Pt (equal alpha)")
j0cs = [1e-7, 1e-6, 1e-5, 1e-4, 1e-3]
maxrel = 0
lt1 = []
bad_J = 0
for (sc, Rf), _ in eta_ref.items():
    j0Pt = scen[sc]
    row = []
    for j0c in j0cs:
        Rcs = []
        for Jj in (0.1, 1.0, 2.0):
            eta = eta_bv(Jj, Rf, j0Pt, 0.5)
            Rc = Jj / (2 * j0c * math.sinh(eta / b))
            cf = Rf * j0Pt / j0c
            maxrel = max(maxrel, abs(Rc / cf - 1))
            Rcs.append(Rc)
            if Rc < 1: lt1.append((sc, Rf, j0c, Jj, Rc))
        if max(Rcs) / min(Rcs) - 1 > 1e-6: bad_J += 1
        row.append("%.4g" % Rcs[1])
    print("  %s Rf_Pt=%3d  R_c (J=1) for j0c=1e-7..1e-3: %s" % (sc, Rf, "  ".join(row)))
check("C03 R_c = Rf_Pt j0Pt/j0c within 1e-6 rel (all scenarios, j0c, J)", maxrel < 1e-6, "max rel diff %.3e" % maxrel)
check("C03 R_c identical for J = 0.1, 1, 2 (1e-6)", bad_J == 0, "cases failing: %d" % bad_J)
for nm, (sc, Rf, j0c), hand in (("P2 flat, j0c=1e-5", ("P2", 1, 1e-5), 60.0), ("P2 Rf=100, j0c=1e-6", ("P2", 100, 1e-6), 6.0e4), ("P1 Rf=100, j0c=1e-5", ("P1", 100, 1e-5), 2.0e6)):
    Rc = 1.0 / (2 * j0c * math.sinh(eta_ref[(sc, Rf)] / b))
    ok = abs(Rc / hand - 1) < 0.01
    print(("RANGE-OK    " if ok else "RANGE-MISS  ") + "%s: R_c=%.5g hand %.3g" % (nm, Rc, hand))
    if not ok: issue("C03 hand value miss %s: %.5g vs %.3g" % (nm, Rc, hand))
if lt1:
    issue("C03 %d of %d (scenario, j0c, J) combinations give R_c < 1 (candidate with that j0c needs no roughening; R_c<1 is not a physical roughness factor), e.g. %s" % (len(lt1), 6 * 5 * 3, lt1[:3]))
issue("C03 check is an algebraic identity of D7 (sinh/asinh inverse pair) when alphas are equal; the spec itself notes the check uses neither function, so it does verify the code, but not the physics")

head("C04 unequal Tafel slopes")
rows = []
c04_fail = 0
for Rf in (1, 100):
    eta0 = eta_ref[("P2", Rf)]
    for a_c in (0.5, 1.0, 1.5):
        bc = bslope(a_c)
        for j0c in (1e-6, 1e-5):
            Rc = J / (2 * j0c * math.sinh(eta0 / bc))
            d_dec = eta_bv(J, Rc, j0c, a_c) - eta_bv(J, 10 * Rc, j0c, a_c)
            b10c = math.log(10) * bc
            tafel_R = (J / j0c) * math.exp(-eta0 / bc)
            x = eta0 / bc
            sin_arg = J / (2 * Rc * j0c)
            lines = "Rf_Pt=%3d a_c=%.1f j0c=%.0e: R_c=%.4g eta_ref/b_c=%.2f; Tafel R_c=%.4g (rel %.2e); d_eta/decade=%.3f mV vs b10=%.3f mV (J/(2Rc j0c)=%.3g)" % (Rf, a_c, j0c, Rc, x, tafel_R, tafel_R / Rc - 1, d_dec * 1e3, b10c * 1e3, sin_arg)
            print("  " + lines)
            if a_c == 0.5:
                R03 = Rf * scen["P2"] / j0c
                if abs(Rc / R03 - 1) > 1e-6: c04_fail += 1; issue("C04 does not reduce to C03 at alpha_c=0.5: %s" % lines)
            if x > 3 and abs(tafel_R / Rc - 1) > 0.02: c04_fail += 1; issue("C04 Tafel R_c miss >2%%: %s" % lines)
            if sin_arg > 10 and abs(d_dec / b10c - 1) > 0.02: c04_fail += 1; issue("C04 d_eta per decade miss >2%%: %s" % lines)
            if Rc < 1: issue("C04 R_c = %.3g < 1 (alpha_c=%.1f, j0c=%.0e, Pt Rf=%d): not a physical roughness factor" % (Rc, a_c, j0c, Rf))
check("C04 reduces to C03 at alpha_c = 0.5; Tafel R_c within 2 %; d_eta/decade = b10 within 2 % (when applicable)", c04_fail == 0, "%d failures" % c04_fail)

head("C05 OER at 1 A/cm2 by Tafel extrapolation")
Jref = 0.010
res = []
for e0 in (0.25, 0.30, 0.35):
    for b10v in (0.030, 0.040, 0.060):
        eta = e0 + b10v * math.log10(1.0 / Jref)
        res.append(eta)
        print("  NiFe eta_ref=%.2f V, b10=%.3f V -> eta(1 A/cm2)=%.3f V" % (e0, b10v, eta))
nife = (min(res), max(res))
ir = 0.30 + 0.050 * math.log10(1.0 / Jref)
print("  Ir oxide eta=%.3f V" % ir)
pt = []
for j0 in (1e-10, 1e-9, 1e-8):
    e = 0.120 * math.log10(1.0 / j0)
    pt.append(e)
    print("  Pt j0=%.0e A/cm2 -> eta=%.3f V" % (j0, e))
rng("NiFe min", nife[0], 0.31, 0.47); rng("NiFe max", nife[1], 0.31, 0.47)
rng("Ir oxide", ir, 0.399, 0.401)
rng("Pt min", min(pt), 0.96, 1.20); rng("Pt max", max(pt), 0.96, 1.20)
rng("NiFe min vs reported 0.27-0.45 V", nife[0], 0.27, 0.45); rng("NiFe max vs reported 0.27-0.45 V", nife[1], 0.27, 0.45)
info("C05", "pure extrapolation over two decades; not a prediction")
