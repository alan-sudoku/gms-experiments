"""Rows B18, B19, B20.

B18: pumping term: ideal-gas form vs incompressible form (Cu plate-fin optimum at 0.1 W), local vs dead-state
     temperature, air power vs electrical.  B19: radiation from the envelope vs a linearised second method.
B20: mass and embodied energy of each B15 design (report only; no independent check).
Assumptions as in plan 3.2; embodied-energy values are UNSURE.  Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B18, B19, B20  (level: derived, unverified)")
R, r, d = best(arch_designs("Cu plate"), 0.1)
print_inputs(design=d.label(), V=r["V"], dP=r["dP"], T_out=r["T_out"])
head("B18 pumping term")
V, dP = r["V"], r["dP"]
mdot = RHO * V
Trho = P0 / (RHO * RAIR)
ideal = mdot * RAIR * math.log((P0 + dP) / P0)
incomp = V * dP / Trho
rel = 1 - ideal / incomp
pred = dP / (2 * P0)
print("T_rho = p0/(rho R_air) = %.3f K (not 300 K / not T0 = %.2f K)" % (Trho, T0))
print("(a) ideal-gas mdot R ln(p_in/p_out) = %.8e W/K ; V dP/T_rho = %.8e W/K ; rel diff = %.4e ; dP/(2 p0) = %.4e" % (ideal, incomp, rel, pred))
check("B18 (a) relative difference = dP/(2 p0) within 10 % of that number", abs(rel - pred) < 0.1 * pred, "rel %.4e vs %.4e (ratio %.4f)" % (rel, pred, rel / pred))
Tlm = (r["T_out"] - T0) / math.log(r["T_out"] / T0)
b1, b2 = V * dP / T0, V * dP / Tlm
print("(b) V dP/T0 = %.6e ; V dP/T_lm = %.6e (T_lm=%.3f K) ; difference = %.3f %%" % (b1, b2, Tlm, (b1 / b2 - 1) * 100))
check("B18 (b) difference below 10 %", abs(b1 / b2 - 1) < 0.10, "%.3f %%" % ((b1 / b2 - 1) * 100))
for ef in (0.1, 0.25, 0.4):
    print("(c) eta_fan=%.2f: V dP/(eta T0) = %.6e W/K  (%.2f x the air-power term)" % (ef, V * dP / (ef * T0), 1 / ef))
info("T_rho note", "T_rho = %.2f K, i.e. %.2f K above 300 K (tabulated rho and R_air not exactly consistent)" % (Trho, Trho - 300))
issue("B18 (a) is a Taylor expansion of ln(1+x) with x = dP/p0 against the same quantity; it holds for any dP, V and does not test the design or the physics (mathematical identity to second order)")
issue("B18 (c) is arithmetic (division by eta_fan); no check is possible or claimed. T_rho = %.2f K as predicted by the spec (about 304 K)." % Trho)

head("B19 radiation")
SIG = 5.670e-8
Aext = W * L + 2 * L * H
rows = {}
for nm, key, er in (("Cu", "Cu plate", 0.05), ("Al k=150", "Al plate k=150", 0.8)):
    Rr, rr, dd = best(arch_designs(key), 0.1)
    Tr = rr["T_root"]
    qrad = er * SIG * Aext * (Tr ** 4 - T0 ** 4)
    Tm = 0.5 * (Tr + T0)
    qlin = 4 * er * SIG * Tm ** 3 * Aext * (Tr - T0)
    rows[nm] = qrad
    print("%-9s T_root=%.3f K eps=%.2f A_ext=%.4f m2: Q_rad=%.5f W; linearised %.5f W; rel diff %.4f %%" % (nm, Tr, er, Aext, qrad, qlin, (qlin / qrad - 1) * 100))
    check("B19 %s linearised within 2 %%" % nm, abs(qlin / qrad - 1) < 0.02, "%.4f %%" % ((qlin / qrad - 1) * 100))
rng("Q_rad Cu", rows["Cu"], 0.0, 0.2)
rng("Q_rad Al", rows["Al k=150"], 0.8, 1.8)
# cross emissivity for scale
for nm, key in (("Cu", "Cu plate"), ("Al k=150", "Al plate k=150")):
    Tr = best(arch_designs(key), 0.1)[1]["T_root"]
    for er in (0.05, 0.8):
        print("  scale: %s with eps=%.2f -> %.5f W" % (nm, er, er * SIG * Aext * (Tr ** 4 - T0 ** 4)))
info("B19 note", "T_root = T_in + Q R_fa is used as the radiating temperature for the whole envelope (as specified); the base is hotter than T_root only by Q R_base,1D")

head("B20 mass and embodied energy")
designs = [("Cu plate (skived)", "Cu plate", False), ("Al plate k=150 (LPBF)", "Al plate k=150", True), ("Al pin k=150 (LPBF)", "Al pin k=150 fav", True), ("Gyroid ks=150 (LPBF)", "Gyroid ks=150 cf=0.3 chi=0.2", True)]
ecu, eal, elp = [30, 54, 70], [131, 200], [100, 400]
masses = {}
for nm, key, am in designs:
    b = best(arch_designs(key), 0.1)
    m = b[1]["mass"]
    masses[nm] = m
    print("%-24s mass=%.4f kg  [%s]" % (nm, m, b[2].label()))
    if nm.startswith("Cu"):
        print("    E_emb = " + ", ".join("%g MJ/kg -> %.2f MJ" % (e, m * e) for e in ecu))
    else:
        print("    E_emb(primary Al) = " + ", ".join("%g MJ/kg -> %.2f MJ" % (e, m * e) for e in eal))
        print("    E_LPBF = " + ", ".join("%g MJ/kg -> %.2f MJ" % (e, m * e) for e in elp))
        print("    E_emb + E_LPBF range = %.2f to %.2f MJ" % (m * (eal[0] + elp[0]), m * (eal[1] + elp[1])))
print("CED per volume ratio (e_Al rho_Al)/(e_Cu rho_Cu):")
for a in eal:
    print("   " + ", ".join("e_Al=%g,e_Cu=%g: %.3f" % (a, c, a * RHO_AL / (c * RHO_CU)) for c in ecu))
allr = [a * RHO_AL / (c * RHO_CU) for a in eal for c in ecu]
rng("CED ratio min", min(allr), 0.5, 2.0); rng("CED ratio max", max(allr), 0.5, 2.0)
rng("Cu sink mass", masses["Cu plate (skived)"], 0.30, 0.45)
rng("Al plate sink mass", masses["Al plate k=150 (LPBF)"], 0.10, 0.20)
cu_e = [masses["Cu plate (skived)"] * e for e in ecu]
rng("Cu E_emb min [MJ]", min(cu_e), 10, 40); rng("Cu E_emb max [MJ]", max(cu_e), 10, 40)
al_e = [masses["Al plate k=150 (LPBF)"] * e for e in eal]
rng("Al plate E_emb(primary) min [MJ]", min(al_e), 10, 40); rng("Al plate E_emb(primary) max [MJ]", max(al_e), 10, 40)
# comparison with B12
Pp, note = required_power(arch_designs("Al plate k=150"), best(arch_designs("Cu plate"), 0.1)[0])
dE = (Pp - 0.1) / ETA_FAN * TAU_LIFE / 1e6
print("Comparison with B12: Al plate k=150 extra fan energy over 5 years dE = %.2f MJ (electrical)" % dE)
for en in (min(al_e), max(al_e)):
    print("   E_emb Al plate (primary) %.2f MJ vs Cu plate E_emb(54) %.2f MJ vs dE %.2f MJ" % (en, masses["Cu plate (skived)"] * 54, dE))
info("B20", "no independent check exists; values are reported only. Electricity vs primary energy not converted (dE is electrical).")
