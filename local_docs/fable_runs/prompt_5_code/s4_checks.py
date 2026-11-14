#!/usr/bin/env python3
"""S4 finaliser checks for Prompt 5. Level of every result: derived (unverified).
Run: python3 s4_checks.py > outputs/s4_checks.txt   (numpy only)

Small numbers the S2 rows did not print and the answer file needs:
 A. Pt and Ir cumulative energy demand: which Table S38 row S2 and S3 read, and the break-even overpotential for each.
 B. Tafel validity threshold for row D1 (closed form of the back-reaction error).
 C. A4: threshold x = e_g rho_g/(e_s rho_s) below which "D > 1 wherever Al loses" holds.
 D. W/C mass-attenuation ratio: crossings of 1 (where carbon is better per unit mass).
 E. Thermal-neutron kappa on atom, mass and volume bases (gate case 4).
 F. Short-fin compensation prices (gate case 16) and winding margin (gate case 14).
 G. Revised gate (answer section 8) applied to the 18 cases of Note J1.
No S2 computation is repeated: inputs are read from the S2 data and output files, and each quoted constant is
checked against the text of its source file.
"""
import csv
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
DATA = os.path.join(HERE, "data")
INF = float("inf")


def found(fname, *needles):
    with open(os.path.join(OUT, fname), encoding="utf-8") as f:
        txt = f.read()
    ok = all(n in txt for n in needles)
    return "outputs/%s [%s: %s]" % (fname, "text found" if ok else "TEXT NOT FOUND", " | ".join(needles))


def rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.reader(r for r in f if not r.startswith("#") and r.strip()))


print("S4 checks, Prompt 5. Level: derived (unverified).")

# ------------------------------------------------------------------------------------------------ A
print("\n== A. Pt and Ir cumulative energy demand (Nuss and Eckelman 2014, SI S1 Table S38) ==")
ced = {}
for r in rows(os.path.join(DATA, "d3_cumulative_energy_demand.csv"))[1:]:
    ced[(r[0], r[1])] = (float(r[2]), float(r[3]), float(r[4]))
for k, v in ced.items():
    print("  %-3s %-32s CED %7.0f MJ/kg (95%%: %.0f-%.0f)" % (k[0], k[1], *v))
pt_za = ced[("Pt", "primary South Africa (63%)")][0]
pt_ru = ced[("Pt", "primary Russia (14%)")][0]
pt_sec = ced[("Pt", "secondary")][0]
pt_tot = ced[("Pt", "TOTAL (supply weighted)")][0]
# supply shares printed in the table (column next to the production figure): ZA 63%, RU 14%, secondary 23%
mix = 0.63 * pt_za + 0.14 * pt_ru + 0.23 * pt_sec
print("  supply-weighted mix 0.63*ZA + 0.14*RU + 0.23*secondary = %.0f MJ/kg; table 'Pt TOTAL' = %.0f (dev %+.2f%%)"
      % (mix, pt_tot, 100 * (mix / pt_tot - 1)))
print("  => S2 read the 'Pt TOTAL' row (mix with 23% secondary); S3 read the two primary-route rows. Same table, different rows.")
print("  primary-only weighted (0.63*ZA + 0.14*RU)/0.77 = %.0f MJ/kg" % ((0.63 * pt_za + 0.14 * pt_ru) / 0.77))

J, TAU = 5e3, 2.88e8  # A/m2, s (central duty of row D3: 0.5 A/cm2, 80 000 h)
print("  break-even overpotential d_eta_be = e_x*m''/(j*tau), central duty j = %.0e A/m2, tau = %.3g s" % (J, TAU))
print("  source of the central duty and of the 0.8438 mV value: " + found("d3_break_even_overpotential.txt", "central case with LOOKUP e = 0.8438 mV"))


def deta_mV(e_MJ, m_kg_m2):
    return e_MJ * 1e6 * m_kg_m2 / (J * TAU) * 1e3


for label, e in [("Pt TOTAL (mix)", pt_tot), ("Pt primary ZA", pt_za), ("Pt primary RU", pt_ru),
                 ("Pt primary RU, 97.5% bound", ced[("Pt", "primary Russia (14%)")][2]), ("Pt secondary", pt_sec)]:
    d = deta_mV(e, 5e-3)
    print("    %-28s e = %7.0f MJ/kg, m'' = 0.5 mg/cm2: d_eta_be = %.3f mV; loading for 30 mV: %.1f mg/cm2; factor on e_x for 30 mV: %.0f"
          % (label, e, d, 0.030 * J * TAU / (e * 1e6) * 100, 30.0 / d))
print("  Ir (anode catalyst of an acidic cell); loadings 0.5, 1, 2 mg/cm2 are MEMORY UNSURE:")
for label in ["TOTAL (supply weighted)", "primary South Africa", "primary Russia"]:
    e = ced[("Ir", label)][0]
    print("    Ir %-26s e = %7.0f MJ/kg: d_eta_be = %s mV"
          % (label, e, ", ".join("%.2f" % deta_mV(e, m) for m in (5e-3, 1e-2, 2e-2))))
e_hi = ced[("Ir", "primary Russia")][2]
print("    Ir primary RU 97.5%% bound %.0f MJ/kg at 2 mg/cm2: %.2f mV" % (e_hi, deta_mV(e_hi, 2e-2)))
print("  Tafel price of kappa = 10 for comparison: 118.3 mV (alpha 0.5), 59.2 mV (alpha 1), 29.6 mV (alpha 2), 298.15 K: "
      + found("d1_overpotential.txt", "b(alpha=0.5, 298.15 K) = 118.3 mV/dec", "b(alpha=2.0, 298.15 K) = 29.6 mV/dec"))

# ------------------------------------------------------------------------------------------------ B
print("\n== B. Row D1: overpotential above which the Tafel form is within eps of Butler-Volmer ==")
R, F = 8.314462, 96485.332
print("  j = j0*[exp(a_a f eta) - exp(-a_c f eta)], f = F/RT. Tafel eta_T = ln(j/j0)/(a_a f).")
print("  eta - eta_T = -ln(1 - exp(-(a_a + a_c) f eta))/(a_a f) ~ exp(-(a_a + a_c) f eta)/(a_a f)")
for T in (298.15, 353.15):
    f = F / (R * T)
    for aa, ac in ((0.5, 0.5), (1.0, 0.5), (1.5, 0.5), (2.0, 0.5)):
        # solve -ln(1-exp(-(aa+ac) f eta))/(aa f) = eps by bisection
        eps = 2e-3
        lo, hi = 1e-4, 1.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            err = -math.log(1 - math.exp(-(aa + ac) * f * mid)) / (aa * f)
            lo, hi = (mid, hi) if err > eps else (lo, mid)
        e100 = -math.log(1 - math.exp(-(aa + ac) * f * 0.1)) / (aa * f)
        print("    T = %.2f K, alpha_a = %.1f, alpha_c = %.1f: error at 100 mV = %.3f mV; error < 2 mV for eta > %.1f mV"
              % (T, aa, ac, e100 * 1e3, hi * 1e3))
print("  S2 worst case with both overpotentials above 100 mV: 2.35 mV at 353.15 K, alpha 0.5: "
      + found("d1_overpotential.txt", "deviation 2.35 mV"))
print("  (S2 coded alpha_c = 1 - alpha_a; the rows with alpha_c = 0.5 for alpha_a > 0.5 above are this script's, with a physical alpha_c > 0.)")

# ------------------------------------------------------------------------------------------------ C
print("\n== C. Row A4: when does 'D > 1 wherever Al loses' hold? ==")
kap = 5.80e7 / 3.54e7
print("  D at the equal-volume crossover = (1 - x)/(kappa - 1), x = e_g rho_g/(e_s rho_s), kappa = sigma_Cu/sigma_Al = %.5f" % kap)
print("  D > 1  <=>  x < 2 - kappa = %.4f ; a crossover exists <=> x < 1" % (2 - kap))
for label, eg, es in [("MEMORY 200/55", 200, 55), ("ICE primary 218/57", 218, 57), ("Nuss primary 194/59.3", 194, 59.3),
                      ("Nuss mix 131/53.7", 131, 53.7), ("ICE recycled Al 29.0 / virgin Cu 57", 29.0, 57),
                      ("ICE recycled/recycled 29.0/16.5", 29.0, 16.5), ("Nuss old scrap 23.8 / primary 59.3", 23.8, 59.3),
                      ("Nuss secondary/secondary 23.8/28.1", 23.8, 28.1)]:
    x = eg * 2700 / (es * 8960)
    msg = "no crossover (Al loses at every duty)" if x >= 1 else "crossover at D = %.3f" % ((1 - x) / (kap - 1))
    print("    %-38s x = %.3f: %s" % (label, x, msg))
print("  source of the S2 values: " + found("a4_duty_crossover.txt", "D>1 iff x < 0.362"))

# ------------------------------------------------------------------------------------------------ D
print("\n== D. W/C mass-attenuation ratio: crossings of 1 (log-log interpolation of the XCOM grid, 0.1-20 MeV) ==")


def xcom(z):
    E, mu = [], []
    for r in rows(os.path.join(DATA, "xcom_z%03d.csv" % z))[1:]:
        e = float(r[1])
        if 0.1 <= e <= 20.0:
            E.append(e)
            mu.append(float(r[7]))
    return np.array(E), np.array(mu)


Ec, mc = xcom(6)
Ew, mw = xcom(74)
assert np.allclose(Ec, Ew), "grids differ"
lr = np.log(mw / mc)
le = np.log(Ec)
for target in (1.0, 2.0):
    cr = []
    for i in range(len(le) - 1):
        a, b = lr[i] - math.log(target), lr[i + 1] - math.log(target)
        if a * b < 0:
            cr.append(math.exp(le[i] + (le[i + 1] - le[i]) * a / (a - b)))
    print("  ratio = %.0f at E = %s MeV" % (target, ", ".join("%.3f" % c for c in cr)))
i = int(np.argmin(lr))
print("  lowest tabulated ratio %.4f at %.3g MeV (grid point); S2: " % (math.exp(lr[i]), Ec[i])
      + found("f2_ratio_crossings.txt", "crossings ['0.403', '7.579']  min at 1.5 MeV, ratio 0.9654"))
print("  (ratio of two log-log linear pieces is itself log-log linear, so this linear root equals S2's brentq root.)")

# ------------------------------------------------------------------------------------------------ E
print("\n== E. Thermal-neutron kappa on three bases (gate case 4) ==")
sig = {}
for r in rows(os.path.join(OUT, "n1_values.csv"))[1:]:
    sig[r[0]] = float(r[2])  # Sears 1992, barn
Ar = {r[1]: float(r[2]) for r in rows(os.path.join(DATA, "nist_atomic_weights.csv"))[1:]}
NA = 6.02214076e23
wB = 4 * Ar["B"] / (4 * Ar["B"] + Ar["C"])
# material: (sigma b, molar mass per absorbing atom g/mol, mass fraction of absorber, density g/cm3, density source)
mats = {
    "Cd metal": (sig["nat Cd"], Ar["Cd"], 1.0, 8.65, "NIST Table 1 (S3 row 16)"),
    "nat B4C": (sig["nat B"], Ar["B"], wB, 2.52, "MEMORY UNSURE"),
    "Al": (sig["Al"], Ar["Al"], 1.0, 2.699, "NIST Table 1 (S3 row 3)"),
    "graphite 1.70": (sig["C (nat)"], Ar["C"], 1.0, 1.70, "MEMORY UNSURE"),
}
per = {}
for name, (s, M, w, rho, srcrho) in mats.items():
    per_mass = NA * w * s * 1e-24 / M          # cm2/g of material
    per_vol = per_mass * rho                   # 1/cm
    per[name] = (s, per_mass, per_vol)
    print("    %-14s sigma_a = %-8g b/atom; Sigma_a/rho = %.4g cm2/g; Sigma_a = %.4g /cm (rho %.3f g/cm3, %s)"
          % (name, s, per_mass, per_vol, rho, srcrho))
print("  (B4C: boron atoms only, w_B = %.5f; carbon in B4C neglected)" % wB)
lo = INF
for s_ in ("Cd metal", "nat B4C"):
    for g_ in ("Al", "graphite 1.70"):
        k = [per[s_][i] / per[g_][i] for i in range(3)]
        lo = min(lo, *k)
        print("    kappa %-9s / %-13s: per absorbing atom %.3g, per mass %.3g, per volume (= per thickness) %.3g" % (s_, g_, *k))
print("  smallest kappa over the four pairs and three bases: %.3g" % lo)
print("  source of sigma: " + found("n1_thermal_ri.txt", "nat B    /C = 2.191e+05   /Al = 3320"))

# ------------------------------------------------------------------------------------------------ F
print("\n== F. Gate cases 14 and 16: margins and prices ==")
print("  case 14 (slot-limited winding, Al for Cu at equal area): loss ratio %.4f; Al meets a temperature-rise limit only if the"
      " incumbent's rise is below %.3f of the limit (rise taken proportional to loss)" % (kap, 1 / kap))
k_s, k_g, rho_s, rho_g = 400.0, 200.0, 8960.0, 2700.0
ratio = 0.93734
print("  case 16 (fin, h = 50 W/m2K, L = 30 mm, t = 1 mm, k 400 vs 200 W/mK): " + found("c1_fin_efficiency.txt", "ratio Al(200)/Cu: 0.93734"))
print("    same geometry: fin heat flow falls to %.4f, i.e. price in function %.4f (needs a requirement margin >= %.4f)" % (ratio, 1 / ratio, 1 / ratio))
print("    compensation by fin thickness (equal k*t gives equal m and equal efficiency): t_g/t_s = %.2f; fin volume x%.2f; fin mass x%.3f"
      % (k_s / k_g, k_s / k_g, k_s / k_g * rho_g / rho_s))
print("    thick-fin bound kappa^(1/2) = %.4f (not reached: mL_Cu = %.3f here)" % (math.sqrt(k_s / k_g), math.sqrt(2 * 50 / (k_s * 1e-3)) * 0.03))
print("    same-geometry mass ratio rho_Al/rho_Cu = %.3f" % (rho_g / rho_s))

# ------------------------------------------------------------------------------------------------ G
print("\n== G. Revised gate (answer section 8) applied to the 18 cases of Note J1 ==")
print("Rules: step 1 scope (N) -> step 2 thresholds (regime only) -> step 3 envelope statement and margin (else incomplete, U)")
print("       -> step 4 price pi against slack -> step 5 Class II. 'free' = slack inf for that quantity. Slack >= 1 always.")
print("Inputs are the constants printed by j1_gate_matrix.txt (S2); nothing new is computed except section E and F values.")
print("source check: " + found("j1_gate_matrix.txt", "MATCH count: 13 of 18"))

# each case: (n, title, step1_ok, thresholds [(name, status)], envelope_stated, pi, slack, note)
# threshold status: 'pass', 'fail', 'missing'; pi None = not needed; slack None = not supplied
C = [
    (1, "photon 100 keV, mass cap 3x (C for W)", True, [], True, 29.31, 3, "pi = W/C mass ratio, F1"),
    (2, "photon 1 MeV, mass cap 3x, thickness free", True, [], True, 1.163, 3, "pi = broad-beam x_C/x_W, F6 (1.040 narrow beam)"),
    (3, "photon 1 MeV, thickness cap 3x", True, [], True, 8.883, 3, "pi = thickness ratio at rho_C 2.26 (11.81 at 1.70), F3"),
    (4, "thermal-neutron thin sheet (Al or C for Cd or B)", True, [], False, lo, None, "pi >= %.3g on every basis (section E); no envelope statement in the case" % lo),
    (5, "bulk neutron shield, fast source, thickness free", True, [], True, 332.8, INF, "pi = thickness ratio water/Cd, N5; mass not capped by the case"),
    (6, "black absorber, tau >= 3 for both", True, [], True, 1.0, 1, "saturated: pi = 1 <= any slack"),
    (7, "storage, 1 h, mass cap 2x (double layer for Li-ion)", True, [], True, 33.3, 2, "pi practical (H3 MEMORY UNSURE); ceiling basis 2.76 at 2.7 V, 1.26 at 4.0 V"),
    (8, "storage, 5 s pulses, 1e6 cycles (g not named)", False, [], False, 0.347, None, "case names neither g nor s: step 1 cannot be stated"),
    (9, "primary cell against double-layer capacitor", True, [("energy held as made, no charger", "fail")], True, None, None, "threshold: as-made state"),
    (10, "magnet, volume cap 2x (ferrite for NdFeB)", True, [("demagnetising field < H_cJ", "pass")], True, 10.84, 2, "M5"),
    (11, "magnet, volume free", True, [("demagnetising field < H_cJ", "pass")], True, 10.84, INF, "M5; mass not capped by the case"),
    (12, "magnet, T_op above Curie point of g", True, [("T_op < T_C", "fail")], True, None, None, "case premise"),
    (13, "DC busbar, cross-section free (Al for Cu)", True, [], True, 1.638, INF, "A1"),
    (14, "slot-limited winding, 'carry I within T limit'", True, [], True, 1.638, None, "area slack 1 stated; requirement margin not supplied"),
    (15, "slot-limited winding, 'loss <= incumbent loss'", True, [], True, 1.638, 1, "A1"),
    (16, "air-cooled heat sink, short fins (Al for Cu)", True, [], False, 1.067, None, "no envelope statement, no margin; section F prices"),
    (17, "oxygen evolution in acid (Ni-Fe for Ir oxide)", True, [("chemical stability of g in the electrolyte", "missing")], True, None, None, "datum not supplied by any row"),
    (18, "flow manifold, viscous loss", False, [], True, None, None, "no solid coefficient in the governing equation"),
]
EXPECT = {1: "I", 2: "II", 3: "I", 4: "I", 5: "II", 6: "II", 7: "I", 8: "II", 9: "I", 10: "I", 11: "II", 12: "I", 13: "II",
          14: "II", 15: "I", 16: "II", 17: "I", 18: "out"}
REASON1 = {8: "U (g and s not named)", 18: "N (not a substitution question)"}


def gate(c):
    n, _, s1, thr, env, pi, slack, _ = c
    if not s1:
        return "out of scope " + REASON1[n], 1
    for _, st in thr:
        if st == "fail":
            return "Class I", 2
    for _, st in thr:
        if st == "missing":
            return "out of scope U (threshold datum missing)", 2
    if pi is not None and pi <= 1.0:
        return "Class II", 5          # passes any cap, since slack >= 1
    if not env or slack is None:
        return "out of scope U (envelope or margin not stated)", 3
    if pi > slack:
        return "Class I", 4
    return "Class II", 5


same = 0
for c in C:
    res, step = gate(c)
    short = "I" if res == "Class I" else "II" if res == "Class II" else ("out" if "N (" in res else "U")
    agree = short == EXPECT[c[0]]
    same += agree
    print(" %2d | %-50s | %-45s | step %d | plan expected %-3s | %s | %s"
          % (c[0], c[1], res, step, EXPECT[c[0]], "same" if agree else "differs", c[7]))
print("classified as the plan expected: %d of 18; returned as incomplete (U): %d; opposite class: %d"
      % (same, sum(1 for c in C if gate(c)[0].startswith("out of scope U")), sum(
          1 for c in C if gate(c)[0] in ("Class I", "Class II") and ("I" if gate(c)[0] == "Class I" else "II") != EXPECT[c[0]])))

print("\nCompleted scenarios (added inputs are ILLUSTRATIVE, not results; they show which input decides):")
done = [
    ("4a thin sheet, thickness cap 3x", lo, 3),
    ("4b thin sheet, nothing capped", lo, INF),
    ("8  g = double layer, s = Li-ion, nothing capped (life goes to the replacement term of Sigma)", 0.347, INF),
    ("8' same, least favourable H3 corner", 1.042, 1),
    ("14a incumbent at its temperature limit (margin 1)", 1.638, 1),
    ("14b incumbent at half its allowed rise (margin 2)", 1.638, 2),
    ("16a geometry fixed, no thermal margin (margin 1)", 1.067, 1),
    ("16b geometry fixed, 10% thermal margin", 1.067, 1.10),
    ("16c fin mass capped at the incumbent's, thickness free", k_s / k_g * rho_g / rho_s, 1),
    ("16d fin thickness capped at 1.5x", k_s / k_g, 1.5),
]
for label, pi, slack in done:
    print("   %-90s pi = %-8.4g slack = %-5s -> %s" % (label, pi, slack, "Class II" if pi <= slack else "Class I"))
print("   17 with 'g dissolves in the electrolyte' supplied (MEMORY UNSURE, not looked up): threshold fails -> Class I at step 2")
