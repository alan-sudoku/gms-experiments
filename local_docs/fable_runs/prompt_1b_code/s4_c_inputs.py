"""S4 follow-up with the inputs S3 corrected (rows C02, C03, C05, C08, C13, B20).  Level: derived.

Purpose (stage S4, finaliser; S2 scripts are not edited):
 (a) C02/C03 with the Pt/C exchange current density read by S3 in Durst et al. 2015 (Table II and the
     literature values quoted there) instead of the plan's 0.2 A/cm2 at 298 K.
 (b) C05 with the NiFe-on-foam values read by S3 in Lu and Zhao 2015; the exchange current density the
     prompt's symmetric arcsinh form would assign to the same data point, against a Tafel-slope reading.
 (c) C08: where the -2.5 % miss comes from (sinh kinetics in eta_min against Tafel kinetics in E), and
     the volumetric exchange current a_v*j0 needed for eta_min to equal each Pt reference.
 (d) C13 with the cumulative energy demand values S3 read in Nuss and Eckelman 2014, Table S38.
 (e) B20 with the same source: production-mix and primary values for Cu and Al.
Inputs are printed.  All inputs remain unverified beyond what S3 states it saw.  numpy not needed.
Run: python3 s4_c_inputs.py > outputs/s4_c_inputs.txt
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import F_CONST, R_GAS, RHO_AL, RHO_CU, TAU_LIFE, ETA_FAN, best, plate_designs, head

print("S4 input recheck, electrochemistry and embodied energy  (level: derived, unverified)")
J = 1.0  # A/cm2


def b_of(alpha, T):
    return R_GAS * T / (alpha * F_CONST)


def eta(Jv, Rf, j0, b):
    return b * math.asinh(Jv / (2 * Rf * j0))


# ---------------------------------------------------------------- (a)
head("(a) Pt reference overpotential at 1 A/cm2 with S3's Pt/C exchange current densities")
cases = [
    ("plan P1: j0 = 0.2 A/cm2 at 298.15 K (S3: about 3x high for this temperature)", 0.2, 298.15),
    ("Durst 2015 quoted literature, 293-298 K: j0 = 0.06 A/cm2", 0.06, 298.15),
    ("Durst 2015 quoted literature, 293-298 K: j0 = 0.07 A/cm2", 0.07, 298.15),
    ("Durst 2015 Table II, 313 K: j0 = 0.135 A/cm2", 0.135, 313.15),
    ("Durst 2015 Table II, 353 K: j0 = 0.26 A/cm2", 0.26, 353.15),
    ("plan P2 (alkaline, not seen by S3): j0 = 6.0e-4 A/cm2 at 298.15 K", 6.0e-4, 298.15),
]
ref = {}
for name, j0, T in cases:
    b = b_of(0.5, T)
    vals = [eta(J, Rf, j0, b) for Rf in (1, 100, 200)]
    ref[name] = vals
    print("  %s\n      b = %.2f mV ; eta at R_f = 1, 100, 200: %.2f mV, %.3f mV, %.3f mV" % (name, b * 1e3, vals[0] * 1e3, vals[1] * 1e3, vals[2] * 1e3))
print("  required roughness R_c = R_f,Pt j0,Pt / j0,c (equal transfer coefficients), Pt/C R_f = 100:")
for j0pt, lab in ((0.06, "acid 0.06"), (0.07, "acid 0.07"), (0.2, "acid 0.2 (plan)"), (6.0e-4, "alkaline 6e-4")):
    print("     Pt %-16s j0,c = 1e-5: R_c = %.3g ; j0,c = 1e-6: R_c = %.3g" % (lab, 100 * j0pt / 1e-5, 100 * j0pt / 1e-6))
print("  acid/alkaline ratio of the Pt exchange current densities used: %.0f (0.06/6e-4), %.0f (0.07/6e-4), %.0f (0.2/6e-4)" % (
    0.06 / 6e-4, 0.07 / 6e-4, 0.2 / 6e-4))

# ---------------------------------------------------------------- (b)
head("(b) NiFe oxygen evolution: values read by S3 in Lu and Zhao 2015 against the plan's extrapolation")
print("  measured (10 M KOH, Tafel-plot values): 0.24 V at 0.5 A/cm2, 0.27 V at 1.0 A/cm2")
print("     apparent slope between these two points: %.1f mV/decade" % ((0.27 - 0.24) / math.log10(1.0 / 0.5) * 1e3))
print("  measured (30 wt% KOH): 0.27 V at 0.1 A/cm2, 0.34 V at 0.3 A/cm2 ; quoted Tafel slope 32 mV/decade")
sl = (0.34 - 0.27) / math.log10(0.3 / 0.1)
print("     apparent slope between these two points: %.1f mV/decade" % (sl * 1e3))
print("     extrapolated to 1 A/cm2 from 0.3 A/cm2: %.3f V with 32 mV/decade ; %.3f V with the apparent slope" % (
    0.34 + 0.032 * math.log10(1 / 0.3), 0.34 + sl * math.log10(1 / 0.3)))
print("  plan C05 extrapolation (S2): NiFe 0.31-0.47 V ; Ir oxide 0.40 V ; flat Pt 0.96-1.20 V (inputs not seen by S3)")
for e in (0.27, 0.31, 0.47):
    print("     NiFe at %.2f V: below flat Pt by %.2f to %.2f V ; relative to Ir oxide 0.40 V: %+.2f V" % (e, 0.96 - e, 1.20 - e, e - 0.40))
Rf = 50.0
jloc = J / Rf
print("  roughness factor reported: %.0f (double-layer capacitance) -> j_local = %.3f A/cm2_real at 1 A/cm2" % (Rf, jloc))
b05 = b_of(0.5, 298.15)
j0_sym = jloc / (2 * math.sinh(0.27 / b05))
b32 = 0.032 / math.log(10)
j0_tafel = jloc * math.exp(-0.27 / b32)
print("  exchange current density assigned to the point (0.27 V, 1 A/cm2, R_f = 50):")
print("     prompt's symmetric arcsinh form, alpha = 0.5 (b = %.2f mV): j0 = %.3e A/cm2_real" % (b05 * 1e3, j0_sym))
print("     Tafel form with the measured 32 mV/decade (b = %.2f mV):   j0 = %.3e A/cm2_real" % (b32 * 1e3, j0_tafel))
print("     ratio of the two: %.2e (the same data point; j0 is not defined without the slope)" % (j0_sym / j0_tafel))
print("  gain per decade of roughness: %.1f mV at alpha = 0.5 ; 32 mV at the measured slope" % (math.log(10) * b05 * 1e3))

# ---------------------------------------------------------------- (c)
head("(c) C08: source of the second-route miss, and the a_v*j0 needed to reach each Pt reference")
b = b05
Jm = 1.0e4
print("  X = J^2/(4 kappa_eff a_v j0 b). eta_min = b acosh(1+X) (sinh kinetics); Tafel semi-infinite form b ln(2X).")
print("  relative difference (b ln 2X)/(b acosh(1+X)) - 1 as a function of eta_min/b:")
for x in (3.0, 3.19, 4.0, 5.0, 5.3, 6.0, 8.0):
    X = math.cosh(x) - 1
    print("     eta_min/b = %.2f  X = %8.2f  Tafel/sinh - 1 = %+.4f" % (x, X, math.log(2 * X) / x - 1))
for kap, eg, av, j0 in ((140.0, 0.3, 6.25e5, 1.0), (140.0, 0.0, 6.25e5, 1.0), (62.0, 0.0, 6.25e5, 1.0)):
    ke = kap * (0.90 * (1 - eg)) ** 1.5
    X = Jm ** 2 / (4 * ke * av * j0 * b)
    emin = b * math.acosh(1 + X)
    etaf = b * math.log(2 * X)
    print("  foam R_f,tot=1000, j0=%g A/m2, kappa=%g, eps_g=%.1f: X=%.2f eta_min=%.5f V (%.2f b) ; Tafel semi-infinite %.5f V ; rel %+.4f" % (
        j0, kap, eg, X, emin, emin / b, etaf, etaf / emin - 1))
print("  S2 values for the same three cases (finite L = 16 mm, Tafel): eta_thick = 0.15962, 0.13254, 0.17389 V ; rel -2.506e-02, -4.655e-02, -1.802e-02")
print("  -> the miss equals the sinh-against-Tafel difference at X of order 10; the 2 % criterion needs eta_min > about 3.4 b, not 3 b.")
x = 3.0
while math.log(2 * (math.cosh(x) - 1)) / x - 1 < -0.02:
    x += 0.001
print("     smallest eta_min/b for which |Tafel/sinh - 1| <= 2 %%: %.3f" % x)

print("\n  a_v*j0 [A/m3] needed for eta_min = eta_ref:  a_v j0 = J^2/(4 kappa_eff b (cosh(eta_ref/b) - 1)), b at 298.15 K, alpha = 0.5")
refs = [
    ("flat Pt, alkaline (0.3812 V)", eta(J, 1, 6e-4, b)),
    ("Pt/C R_f=100, alkaline (0.1448 V)", eta(J, 100, 6e-4, b)),
    ("Pt/C R_f=200, alkaline (0.1097 V)", eta(J, 200, 6e-4, b)),
    ("flat Pt, acid j0=0.065", eta(J, 1, 0.065, b)),
    ("Pt/C R_f=100, acid j0=0.065", eta(J, 100, 0.065, b)),
]
print("  %-36s %10s | %s" % ("reference", "eta_ref[V]", "kappa=62,eg=0  kappa=62,eg=0.3  kappa=140,eg=0  kappa=140,eg=0.3   (eps = 0.5)"))
for name, er in refs:
    row = []
    for kap in (62.0, 140.0):
        for eg in (0.0, 0.3):
            ke = kap * (0.5 * (1 - eg)) ** 1.5
            row.append(Jm ** 2 / (4 * ke * b * (math.cosh(er / b) - 1)))
    print("  %-36s %10.5f | %12.3e %14.3e %14.3e %16.3e" % (name, er, row[0], row[1], row[2], row[3]))
print("  for scale: a_v = 4 eps/d_pore = 2e6 m2/m3 (1 um pores, eps 0.5), 2e7 (0.1 um); j0 = 0.1 A/m2 = 1e-5 A/cm2")
for er_name, er in refs[1:2] + refs[4:5]:
    ke = 62.0 * 0.5 ** 1.5
    need = Jm ** 2 / (4 * ke * b * (math.cosh(er / b) - 1))
    for j0 in (0.1, 1.0):
        av = need / j0
        print("     %s, kappa=62, eg=0, j0=%.1f A/m2: a_v = %.3e m2/m3 -> pore diameter 4 eps/a_v = %.3e m" % (er_name, j0, av, 4 * 0.5 / av))

# ---------------------------------------------------------------- (d)
head("(d) C13 break-even overpotential with the cumulative energy demand read by S3 (Nuss and Eckelman 2014, Table S38)")
tau_op = 1.44e8
print("  d_eta_be = e m''/(J tau_op), J = 1e4 A/m2, tau_op = %.3g s ; primary energy counted one-for-one with electricity" % tau_op)
for name, e in (("Pt production mix", 243000.0), ("Pt primary (ZA)", 308000.0), ("Pt primary (RU)", 327000.0), ("Pt secondary", 11900.0)):
    for m in (0.5, 3.0, 5.0):
        em = e * m * 1e-3
        print("     %-18s e = %7.0f MJ/kg, m'' = %.1f g/m2: e m'' = %7.1f MJ/m2, d_eta_be = %.4f mV, payback at 50 mV = %.1f d" % (
            name, e, m, em, em * 1e6 / (Jm * tau_op) * 1e3, em * 1e6 / (Jm * 0.05) / 86400))
for name, e in (("Ir (ZA)", 165000.0), ("Ir (RU)", 175000.0)):
    for m in (10.0, 20.0):
        em = e * m * 1e-3
        print("     %-18s e = %7.0f MJ/kg, m'' = %.1f g/m2 (assumed anode loading 1-2 mg/cm2, UNSURE): d_eta_be = %.3f mV" % (name, e, m, em * 1e6 / (Jm * tau_op) * 1e3))

# ---------------------------------------------------------------- (e)
head("(e) B20 with the same source: Cu and Al, production mix and primary")
eCu = {"mix": 53.7, "primary": 59.3}
eAl = {"mix": 131.0, "primary": 194.0}
for kk in ("mix", "primary"):
    print("  per-volume ratio (e_Al rho_Al)/(e_Cu rho_Cu), %s values: %.3f" % (kk, eAl[kk] * RHO_AL / (eCu[kk] * RHO_CU)))
mcu = best(plate_designs(390.0), 0.1)[1]["mass"]
mal = best(plate_designs(150.0), 0.1)[1]["mass"]
print("  sink masses (B05 optima at 0.1 W): Cu %.4f kg, Al plate k=150 %.4f kg" % (mcu, mal))
for kk in ("mix", "primary"):
    print("  metal embodied energy, %s: Cu %.2f MJ, Al %.2f MJ, Al - Cu = %+.2f MJ" % (kk, mcu * eCu[kk], mal * eAl[kk], mal * eAl[kk] - mcu * eCu[kk]))
for el in (100.0, 400.0):
    print("  LPBF processing at %.0f MJ/kg of part (not seen by S3, UNSURE): %.2f MJ" % (el, mal * el))
print("  extra fan electricity over tau_life = %.4g s at eta_fan = %.2f (B12): k=200 23.61 MJ, k=180 28.17 MJ, k=150 37.34 MJ, k=100 66.52 MJ" % (TAU_LIFE, ETA_FAN))
for dE, kk in ((23.61, 200), (37.34, 150), (66.52, 100)):
    print("     k=%d: fan penalty / Cu metal energy (mix) = %.2f ; / (Al primary + LPBF 100..400) = %.2f..%.2f" % (
        kk, dE / (mcu * eCu["mix"]), dE / (mal * (eAl["primary"] + 100)), dE / (mal * (eAl["primary"] + 400))))
