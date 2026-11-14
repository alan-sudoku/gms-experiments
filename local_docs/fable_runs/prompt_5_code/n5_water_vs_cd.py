#!/usr/bin/env python3
"""Row N5 (claim G3.8): water without absorber against a Cd sheet, thermal attenuation 1e-3. Order-of-magnitude row.

Water: x = L*ln(1e3), L from data/n5_water_diffusion.csv (LLNL/NCSP Hand Calculation Methods Table 2-2: L = 2.85 cm, D = 0.16 cm; LOOKUP,
substitute for Lamarsh and Baratta 2001 which was not reachable), areal mass rho*x with rho = 0.998 g/cm3.
Cd: x = ln(1e3)/Sigma_a(Cd) (beam), Sigma_a from n3 formula with Sears natural sigma_a (outputs/n1_values.csv), rho 8.65 g/cm3 (MEMORY).
Independent check of the table: Sigma_a(water) = N_H*sigma_H(2200 m/s)*sqrt(pi)/2 vs D/L^2 from the table (5%).
Caveats printed below. Level `derived`. Run n1_thermal_ri.py first.
"""
import os, csv, math
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data")
NA = 6.02214076e23; FAILS = []
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)
AW = {r["symbol"]: float(r["A_r"]) for r in csv.DictReader(l for l in open(os.path.join(D, "nist_atomic_weights.csv")) if not l.startswith("#"))}
W = {r["quantity"]: float(r["value"]) for r in csv.DictReader(l for l in open(os.path.join(D, "n5_water_diffusion.csv")) if not l.startswith("#"))}
N1 = {r["entry"]: r for r in csv.DictReader(l for l in open(os.path.join(HERE, "outputs", "n1_values.csv")) if not l.startswith("#"))}
L, Dw = W["L_th_H2O"], W["D_th_H2O"]; rw = 0.998
print("N5 LOOKUP: L, D for H2O <- data/n5_water_diffusion.csv (LLNL/NCSP Table 2-2; plan UNSURE range for L 2.7-2.9 cm: %s)" % ("inside" if 2.7 <= L <= 2.9 else "OUTSIDE"))
print("  sigma_H, sigma_Cd <- outputs/n1_values.csv (Sears 1992, NIST NCNR); A_r <- data/nist_atomic_weights.csv; rho_water 0.998, rho_Cd 8.65 g/cm3")
MH2O = 2*AW["H"] + 15.999
NH = 2*rw*NA/MH2O; NO = rw*NA/MH2O
sH = float(N1["H (1H)"]["sigma_sears_b"])*1e-24
sO = 0.00019e-24   # Sears natural O, 0.00019 b (data/sears_1992_table1.csv row O)
S2200 = NH*sH + NO*sO; Sm = S2200*math.sqrt(math.pi)/2
Stab = Dw/L**2
print("\nWater Sigma_a: N_H = %.4e /cm3; N_H*sigma_H(2200) = %.5f /cm (plan ~0.0222); with O %.5f; x sqrt(pi)/2 = %.5f /cm (plan ~0.0197)" % (NH, NH*sH, S2200, Sm))
print("  table-derived Sigma_a = D/L^2 = %.5f /cm" % Stab)
check("first-principles Sigma_a vs table D/L^2 within 5%", abs(Sm/Stab-1) <= 0.05, "%.5f vs %.5f (%+.2f%%)" % (Sm, Stab, 100*(Sm/Stab-1)))
Lfp = math.sqrt(Dw/Sm); print("  L = sqrt(D/Sigma_a) with first-principles Sigma_a = %.4f cm (table 2.85)" % Lfp)
xw = L*math.log(1e3); mw = rw*xw
print("\nWater: x = L ln(1e3) = %.3f cm, areal mass = %.3f g/cm2" % (xw, mw))
for col, lab in (("sigma_sears_b", "Sears"), ("sigma_endf_b", "ENDF/B-VII.1")):
    sCd = float(N1["nat Cd"][col])*1e-24; SCd = 8.65*NA*sCd/AW["Cd"]
    xc = math.log(1e3)/SCd; mc = 8.65*xc
    print("Cd (sigma_a %s = %.5g b): Sigma_a = %.2f /cm; x = %.5f cm = %.4f mm, areal mass = %.4f g/cm2" % (lab, sCd*1e24, SCd, xc, 10*xc, mc))
    print("   ratio areal mass water/Cd = %.2f (plan ~40); ratio thickness water/Cd = %.1f (plan ~300)" % (mw/mc, xw/xc))
    check("areal-mass ratio within factor 1.5 of 40 (%s)" % lab, 40/1.5 <= mw/mc <= 40*1.5, "%.2f" % (mw/mc))
    check("thickness ratio within factor 1.5 of 300 (%s)" % lab, 300/1.5 <= xw/xc <= 300*1.5, "%.1f" % (xw/xc))
print("\nCaveats: (1) the Cd sheet uses the 2200 m/s cross section, not a Maxwellian average (Cd-113 is not 1/v; non-1/v factor ~1.3 in the literature, UNSURE) and a beam, not an isotropic flux;")
print("(2) water attenuation exp(-x/L) is the diffusion asymptote of a thermal flux, not narrow-beam attenuation; the row is order-of-magnitude only;")
print("(3) the check Sigma_a first-principles vs D/L^2 is a consistency test of the table, not an identity.")
print("FAILED CHECKS:", FAILS if FAILS else "none")
