#!/usr/bin/env python3
"""Row J1: apply the 5-step gate (plan section 5, PROVISIONAL) to the 18 cases of Note J1.
Level of every result: derived (unverified). numpy only. Run: python3 j1_gate_matrix.py > outputs/j1_gate_matrix.txt
Every numeric input is a constant copied from an output file of another row (OUT/<file>); at run time the script checks
that the quoted text appears in that file and prints OK or NOT FOUND. Nothing is invented: a missing input is None and
the case is reported as undecided with the blocked step.
"""
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
INF = float("inf")
_cache = {}


def src(fname, *needles):
    """Return 'file [OK]' if every needle string is found in OUT/fname."""
    if fname not in _cache:
        with open(os.path.join(OUT, fname), encoding="utf-8") as f:
            _cache[fname] = f.read()
    ok = all(n in _cache[fname] for n in needles)
    return f"outputs/{fname} [{'text found' if ok else 'TEXT NOT FOUND'}: {' | '.join(needles)}]"


# ----------------------------------------------------------------------------------------------
# Constants copied from other rows (each comment names the output file and the printed text).
# ----------------------------------------------------------------------------------------------
# F1: total mu/rho with coherent scattering, cm2/g (NIST XCOM, as recorded by row F1)
MU_W_01, MU_C_01 = 4.437, 0.1514          # 0.1 MeV
MU_W_1, MU_C_1 = 0.06618, 0.06362         # 1 MeV
# F3: thickness-basis ratio (mu*rho)_W/(mu*rho)_C at 1 MeV
THK_1MEV = {1.70: 11.81, 2.26: 8.883}     # rho_C g/cm3 -> ratio; also min over energy 10.96 / 8.245
# F6: buildup-corrected areal-density ratio x_C/x_W, 1 MeV, T_E = 1e-2 and 1e-3
XCXW_1MEV = (1.1629, 1.1436)
# N1: Sears 1992 thermal sigma_a (b)
SIG = {"nat Cd": 2520.0, "nat B": 767.0, "B-10": 3835.0, "Al": 0.231, "C": 0.0035}
# N5: water against Cd sheet, thermal attenuation 1e-3 (thickness ratio, areal-mass ratio), Sears sigma
N5_THK, N5_MASS = 332.8, 38.40
# N3: tau of a 1 mm sheet (Sears)
N3_TAU = {"Cd": 11.7, "B4C": 8.4}
# H3 central case: E in Wh/kg, P in kW/kg (MEMORY UNSURE inputs of row H3) and the 16-corner ranges
H3 = dict(Ec=6.0, Pc=10.0, Eb=200.0, Pb=1.5)
H3_RANGE = dict(Ec=(4.0, 8.0), Pc=(5.0, 15.0), Eb=(150.0, 260.0), Pb=(0.3, 3.0))  # ranges are the row's spec ranges (see h3 output header 'range corners')
# H1/H2
CSP_CEIL = 551.6                          # F/g, geometric ceiling single electrode (H2)
E_LIFEPO4_WHKG = 385.0                    # H1: LiFePO4+6C theoretical, reactant basis
# M5 (magnet circuit)
BH_NDFEB, BH_FERR = 345.3, 31.8           # kJ/m3 (M5)
VOL_RATIO_FERR_NDFEB = 10.84              # M5
HM_FERR_KAM, HCJ_FERR_LOW = 155.4, 250.0  # kA/m (M5; HcJ is a MEMORY UNSURE range 250-400)
# A1
AREA_RATIO_AL_CU = 1.63842                # A1
# C1
FIN_RATIO_AL200 = 0.93734                 # eta_Al(k=200)/eta_Cu at h=50, L=30 mm, t=1 mm (C1)
K_CU, K_AL = 400.0, 200.0                 # W/mK (C1 MEMORY inputs)


class Case:
    def __init__(self, num, title, expected_text, expected_set):
        self.num, self.title, self.expected_text, self.expected_set = num, title, expected_text, expected_set
        self.inputs = []      # (description, value text, source text)
        self.step1 = None     # None = passes; else reason string (-> out of scope)
        self.step2 = []       # (name, status in {'pass','fail','unavailable'}, detail)
        self.kappa = None
        self.n = None
        self.slack = None     # None = not supplied by case text
        self.slack_note = ""
        self.kappa_note = ""
        self.ambig = []       # (text of ambiguity, what the other reading gives)
        self.missing = []     # (input, step blocked)

    def inp(self, d, v, s):
        self.inputs.append((d, v, s))


def gate(c, slack=None, use_case_slack=True):
    """Literal 5-step gate. Returns (outcome, deciding step, trace)."""
    sl = c.slack if use_case_slack else slack
    t = []
    if c.step1:
        return "out of scope", "1", [f"step 1: {c.step1}"]
    t.append("step 1: requirement, envelope and coefficient stated, a solid coefficient enters, same environment -> pass")
    blocked = None
    for name, st, det in c.step2:
        t.append(f"step 2 [{name}]: {st}: {det}")
        if st == "fail":
            return "Class I", "2", t
        if st == "unavailable" and blocked is None:
            blocked = name
    if c.kappa is None or c.n is None:
        t.append("step 3: kappa or n not available")
        return "undecided", "3 (blocked)" if blocked is None else "2 (blocked)", t
    price = c.kappa ** c.n
    if sl is None:
        if price <= 1.0:
            t.append(f"step 3: price kappa^n = {price:.4g}; slack not supplied but any slack >= 1 (cap >= incumbent usage) -> price within slack")
        else:
            t.append(f"step 3: price kappa^n = {price:.4g}; slack NOT supplied by the case text -> cannot compare")
            return "undecided", "3 (blocked)" if blocked is None else "2 (blocked)", t
    elif price > sl:
        t.append(f"step 3: price kappa^n = {price:.4g} > slack {sl:g} -> Class I")
        if blocked:
            t.append(f"  (step 2 item '{blocked}' was unavailable; step 3 decides Class I regardless)")
        return "Class I", "3", t
    else:
        t.append(f"step 3: price kappa^n = {price:.4g} <= slack {sl:g} -> pass")
    if blocked:
        t.append(f"step 2 item '{blocked}' unavailable: step 2 cannot be completed")
        return "undecided", "2 (blocked)", t
    t.append("step 4: fair comparator s' defined by the Sigma comparison stage (not numerically evaluated here; changes no class)")
    t.append("step 5: Class II (pass g, s', D to the Sigma comparison; no statement about the winner)")
    return "Class II", "5 (after step 3 pass)", t


cases = []

# ---- case 1
c = Case(1, "Photon attenuation, 100 keV, mass capped at 3x incumbent (C against W)", "Class I (step 3, kappa ~ 29)", {"Class I"})
k = MU_W_01 / MU_C_01
c.inp("mu/rho W, C at 0.1 MeV (cm2/g)", f"{MU_W_01}, {MU_C_01}", src("f1_mass_attenuation.txt", "W/C=29.31", "XCOM total(w/coh)=4.437", "XCOM total(w/coh)=0.1514"))
c.inp("g = C, s = W (case text 'C against W')", "", "case text")
c.kappa, c.n, c.slack = k, 1.0, 3.0
c.inp("n = 1 (narrow-beam attenuation, bulk-limited linear)", "1", "plan G1.1 / section 5 step 3")
c.inp("slack = mass cap 3x / incumbent usage 1", "3", "case text")
cases.append(c)

# ---- case 2
c = Case(2, "Photon attenuation, 1 MeV, mass capped at 3x, thickness free", "Class II", {"Class II"})
c.kappa, c.n, c.slack = MU_W_1 / MU_C_1, 1.0, 3.0
c.inp("mu/rho W, C at 1 MeV (cm2/g)", f"{MU_W_1}, {MU_C_1}", src("f1_mass_attenuation.txt", "XCOM total(w/coh)=0.06618", "XCOM total(w/coh)=0.06362", "W/C=1.04"))
c.inp("buildup-corrected x_C/x_W at 1 MeV (T_E 1e-2, 1e-3), broad beam", f"{XCXW_1MEV}", src("f6_buildup_mc.txt", "x_C/x_W = 1.1629", "x_C/x_W = 1.1436"))
c.inp("slack = mass cap 3x; thickness free", "3 (mass), inf (thickness)", "case text")
c.kappa_note = f"alt kappa (buildup, F6) = {XCXW_1MEV[0]} / {XCXW_1MEV[1]}: also <= 3, same outcome"
cases.append(c)

# ---- case 3
c = Case(3, "Photon attenuation, 1 MeV, thickness capped at 3x", "Class I (step 3, kappa ~ 9-11)", {"Class I"})
c.kappa, c.n, c.slack = THK_1MEV[1.70], 1.0, 3.0
c.inp("thickness-basis ratio W/C at 1 MeV, rho_C = 1.70 / 2.26 g/cm3", f"{THK_1MEV[1.70]} / {THK_1MEV[2.26]}", src("f3_thickness_ratio.txt", "at 1 MeV 11.81", "at 1 MeV 8.883"))
c.inp("slack = thickness cap 3x", "3", "case text")
c.ambig.append(("rho_C is not stated in the case; F3 gives 11.81 (1.70) and 8.883 (2.26), both > 3", "none (same class)"))
cases.append(c)

# ---- case 4
c = Case(4, "Thermal-neutron absorption in a thin sheet (Al or C against Cd or B)", "Class I (step 3, kappa >= 1e4)", {"Class I"})
pairs = {"Cd/Al": SIG["nat Cd"] / SIG["Al"], "Cd/C": SIG["nat Cd"] / SIG["C"], "nat B/Al": SIG["nat B"] / SIG["Al"],
         "nat B/C": SIG["nat B"] / SIG["C"], "B-10/Al": SIG["B-10"] / SIG["Al"], "B-10/C": SIG["B-10"] / SIG["C"]}
c.inp("sigma_a (b, Sears 1992): nat Cd, nat B, B-10, Al, C", f"{SIG['nat Cd']}, {SIG['nat B']}, {SIG['B-10']}, {SIG['Al']}, {SIG['C']}",
      "outputs/n1_values.csv (columns sigma_sears_b), " + src("n1_thermal_ri.txt", "nat Cd", "2520", "767"))
c.inp("kappa per atom, all four pairs and enriched B-10", ", ".join(f"{k_}={v:.3g}" for k_, v in pairs.items()), "computed from the sigma_a above")
c.kappa, c.n, c.slack = pairs["Cd/Al"], 1.0, None  # representative pair; all pairs reported
c.kappa_note = "kappa shown for Cd/Al (the pair that sets the case's 'kappa >= 1e4' threshold): nat B/Al = 3.3e3 is BELOW 1e4"
c.missing.append(("envelope slack (cap/usage) for a thin sheet and the binding basis (per atom, mass, area)", "step 3"))
c.ambig.append(("case names no cap, so slack is not supplied", "if no cap = uncapped (slack inf): Class II; if slack = 1 (incumbent at its cap): Class I for every pair; Class I whenever slack < kappa"))
c.ambig.append(("n for a thin sheet: bulk-limited n = 1 chosen; a black sheet (tau >= 3, n = 0) would make kappa^n = 1 and Class II", "Class II if the sheet is black for g too"))
cases.append(c)

# ---- case 5
c = Case(5, "Bulk neutron shield, fast source, thickness free (water or concrete against absorber-loaded)", "Class II", {"Class II"})
c.kappa, c.n, c.slack = N5_THK, 1.0, INF
c.inp("water/Cd thickness and areal-mass ratios (thermal attenuation 1e-3)", f"{N5_THK}, {N5_MASS}", src("n5_water_vs_cd.txt", "ratio areal mass water/Cd = 38.40", "ratio thickness water/Cd = 332.8"))
c.inp("slack: 'thickness free'", "inf", "case text")
c.ambig.append(("only thickness is stated free; an areal-mass cap is not mentioned; read as no binding cap", f"if a mass cap equal to the incumbent's usage (slack 1) were binding: price {N5_MASS} > 1 -> Class I"))
c.ambig.append(("N5 is an order-of-magnitude row for a thermal flux and a Cd sheet; the 'fast source' needs the N4 moderation step first (18-25 collisions for H, D)", "no change in class"))
cases.append(c)

# ---- case 6
c = Case(6, "Black control absorber (natural B4C against Ag-In-Cd or Hf), tau >= 3 for both", "Class II (n = 0)", {"Class II"})
c.kappa, c.n, c.slack = 1.0, 0.0, None   # kappa value irrelevant when n = 0; slack not needed
c.kappa_note = "kappa not computed: n = 0, price = kappa^0 = 1 for any kappa"
c.inp("tau of a 1 mm sheet: Cd, natural B4C (premise 'tau >= 3 for both' is the case's own)", f"{N3_TAU}", src("n3_self_shielding.txt", "1 mm Cd tau = 11.7", "1 mm B4C tau = 8.4"))
c.inp("tau of Ag-In-Cd and Hf", "not available", "no row computed it; the case premise supplies tau >= 3")
c.inp("n = 0 (saturated absorber)", "0", "plan section 5 step 3")
c.ambig.append(("slack not supplied; since n = 0 the price is 1 and slack >= 1 by definition (incumbent fits its own cap)", "none"))
c.ambig.append(("N3 tau values are thermal (2200 m/s); at epithermal energies B4C (1/v) falls below tau = 3 while Ag-In-Cd resonances do not; the case does not state the spectrum", "if the spectrum were epithermal and tau(B4C) < 3: n = 1 and the outcome would need a slack"))
cases.append(c)

# ---- case 7
Eb, Ec = H3["Eb"], H3["Ec"]
req = Eb / 2.0
bound = 0.5 * (CSP_CEIL / 4.0) * 2.7 ** 2 / 3.6          # Wh/kg, carbon only, electrolyte excluded
bound4 = 0.5 * (CSP_CEIL / 4.0) * 4.0 ** 2 / 3.6
c = Case(7, "Energy storage, 1 h discharge, mass capped at 2x (double layer against Li-ion)", "Class I (step 3; stoichiometric bound)", {"Class I"})
c.inp("Li-ion cell specific energy E_b, double-layer cell E_c (Wh/kg, MEMORY UNSURE)", f"{Eb}, {Ec}", src("h3_ragone_crossover.txt", "central: E_c=6 Wh/kg", "E_b=200 Wh/kg"))
c.inp("double-layer geometric ceiling C_sp (F/g), carbon only, electrolyte excluded", f"{CSP_CEIL}", src("h1_h2_redox_dl_energy.txt", "C_sp ceiling = 21 uF/cm2 * SSA = 551.6 F/g"))
c.inp("ceiling energy 0.5*(C_sp/4)*V^2 at 2.7 V and 4.0 V (Wh/kg)", f"{bound:.1f}, {bound4:.1f}", "computed here from C_sp (H2 gives it per atom: 0.06257 and 0.13733 eV/atom)")
c.inp("LiFePO4+6C theoretical (Wh/kg, reactant basis)", f"{E_LIFEPO4_WHKG}", src("h1_h2_redox_dl_energy.txt", "LiFePO4+6C: n=1 V=3.3 M=229.82 g/mol N_at=13  E=385 Wh/kg"))
c.inp("slack = mass cap 2x", "2", "case text")
c.step2.append(("required specific energy vs stoichiometric bound of g", "pass" if bound >= req else "fail",
                f"required = E_b/slack = {req:.0f} Wh/kg; g bound (ceiling, 2.7 V, carbon only) = {bound:.1f} Wh/kg. The bound excludes electrolyte, separator, collectors, so a pass is not conclusive"))
c.kappa, c.n, c.slack = Eb / Ec, 1.0, 2.0
c.kappa_note = f"kappa = E_b/E_c = {Eb/Ec:.1f} (practical, H3 central)"
c.ambig.append(("expected text says 'step 3; stoichiometric bound' but the gate puts the stoichiometric bound in step 2", "the gate as written decides at step 3 on practical values; step 2 does not fail (140 >= 100 Wh/kg)"))
c.ambig.append(("which c_g to use in step 3: practical 6 Wh/kg (used) or geometric ceiling",
                f"ceiling 2.7 V: kappa = {E_LIFEPO4_WHKG/bound:.2f} (theoretical LiFePO4 / ceiling) > 2 -> Class I; ceiling 4.0 V: kappa = {E_LIFEPO4_WHKG/bound4:.2f} <= 2 -> Class II"))
c.ambig.append(("required specific energy taken as the incumbent's delivered 200 Wh/kg / 2; if taken as theoretical 385/2 = 192.5", f"{E_LIFEPO4_WHKG/2:.1f} > {bound:.1f}: Class I at step 2 (2.7 V); passes at 4.0 V ({bound4:.0f})"))
cases.append(c)

# ---- case 8
def deliver(E, P, t_s):
    return min(E, P * 1000.0 * t_s / 3600.0)

t = 5.0
cap5, bat5 = deliver(H3["Ec"], H3["Pc"], t), deliver(H3["Eb"], H3["Pb"], t)
ks = []
for Ec_ in H3_RANGE["Ec"]:
    for Pc_ in H3_RANGE["Pc"]:
        for Eb_ in H3_RANGE["Eb"]:
            for Pb_ in H3_RANGE["Pb"]:
                ks.append(deliver(Eb_, Pb_, t) / deliver(Ec_, Pc_, t))
c = Case(8, "Energy storage, 5 s pulses, 1e6 cycles", "Class II", {"Class II"})
c.inp("H3 central: E_c, P_c, E_b, P_b", f"{H3}", src("h3_ragone_crossover.txt", "central: E_c=6 Wh/kg P_c=10 kW/kg ; E_b=200 Wh/kg P_b=1.5 kW/kg"))
c.inp("t* range over the 16 corners (s)", "4.80 .. 96.00 (central 14.4)", src("h3_ragone_crossover.txt", "t*(A) range 4.80 .. 96.00 s"))
c.inp("deliverable specific energy at 5 s: capacitor, battery (Wh/kg)", f"{cap5:.3f}, {bat5:.3f}", "computed here: min(E, P*t)")
c.inp("assignment g = double layer, s = Li-ion", "assumed", "NOT in the case text; inherited from case 7")
c.kappa, c.n, c.slack = bat5 / cap5, 1.0, None
c.kappa_note = f"kappa = c_s/c_g = {bat5/cap5:.3f} (central); over the 16 corners {min(ks):.3f} .. {max(ks):.3f}"
c.step2.append(("1e6-cycle life of g", "unavailable", "stated in the case, but no row produced a cycle-life datum for the double-layer cell or the Li-ion cell"))
c.missing.append(("cycle life of g at 1e6 cycles (and which of the pair is g)", "step 2"))
c.ambig.append(("case does not say which device is g", "if g = Li-ion: kappa = c_s/c_g = %.2f > 1, slack not supplied -> undecided at step 3 and the Li-ion cycle-life datum at step 2 is equally unavailable" % (cap5 / bat5)))
c.ambig.append(("no cap stated; with kappa^n < 1 the price passes for any slack >= 1, but at the corner t* = 4.8 s kappa is %.3f > 1" % max(ks), "central case passes, one corner does not"))
cases.append(c)

# ---- case 9
c = Case(9, "Primary (non-rechargeable, charged as made) cell against a double-layer capacitor", "Class I at step 2, or out of scope at step 1", {"Class I", "out of scope"})
c.inp("energy stored by g (capacitor) as manufactured", "0 (no stored energy)", "case text ('charged as made' for the primary cell only); plan G3.11")
c.step2.append(("required specific energy vs stoichiometric bound of g", "fail",
                "required = the primary cell's specific energy > 0; bound of g as manufactured = 0 (it holds no energy until charged)"))
c.kappa = None
c.ambig.append(("step 1 clause 3 ('cannot operate in the same environment and the function cannot be restated') does not trigger: same environment, and G3.11 restates the function as 'deliver E in time t'", "if the restated function is judged impossible without charging: out of scope at step 1"))
c.ambig.append(("'stoichiometric bound of g' for a capacitor is undefined; read as stored energy in the as-made state = 0", "if read as the charged-state ceiling 1/2*C*V^2 (about 140 Wh/kg at 2.7 V) step 2 passes; step 3 then has c_g = 0, kappa = inf -> Class I at step 3"))
cases.append(c)

# ---- case 10
c = Case(10, "Permanent-magnet excitation, volume capped at 2x (ferrite against NdFeB)", "Class I (step 3, kappa ~ 11)", {"Class I"})
c.kappa, c.n, c.slack = VOL_RATIO_FERR_NDFEB, 1.0, 2.0
c.inp("BH_max NdFeB, ferrite (kJ/m3); volume ratio", f"{BH_NDFEB}, {BH_FERR}; {VOL_RATIO_FERR_NDFEB}", src("m5_magnet_circuit.txt", "BHmax=345.3", "BHmax=31.8", "volume ratio ferrite/NdFeB=10.84"))
c.inp("operating |H_m| of ferrite vs H_cJ (kA/m, H_cJ MEMORY UNSURE 250-400)", f"{HM_FERR_KAM} vs >= {HCJ_FERR_LOW}", src("m5_magnet_circuit.txt", "Hm=-155.4 kA/m", "HcJ(UNSURE)=250-400"))
c.step2.append(("demagnetising field vs H_cJ of ferrite", "pass" if HM_FERR_KAM < HCJ_FERR_LOW else "fail", f"|H_m| = {HM_FERR_KAM} kA/m < H_cJ low end {HCJ_FERR_LOW} kA/m (UNSURE input)"))
c.step2.append(("T_op vs Curie of ferrite", "pass", "not stated in the case; not checked (regime variable absent)"))
c.inp("slack = volume cap 2x", "2", "case text")
cases.append(c)

# ---- case 11
c = Case(11, "Permanent-magnet excitation, volume free, demagnetising field below H_cJ of ferrite", "Class II", {"Class II"})
c.kappa, c.n, c.slack = VOL_RATIO_FERR_NDFEB, 1.0, INF
c.inp("volume ratio ferrite/NdFeB; |H_m| vs H_cJ", f"{VOL_RATIO_FERR_NDFEB}; {HM_FERR_KAM} vs >= {HCJ_FERR_LOW} kA/m", src("m5_magnet_circuit.txt", "volume ratio ferrite/NdFeB=10.84", "Hm=-155.4 kA/m"))
c.step2.append(("demagnetising field vs H_cJ of ferrite", "pass", "premise of the case and M5 agree (155.4 < 250 kA/m, H_cJ UNSURE)"))
c.inp("slack: volume free", "inf", "case text")
c.ambig.append(("only volume is stated free; mass (ferrite 7.08x heavier, M5) not mentioned; read as no binding cap", "with a mass cap at the incumbent's usage (slack 1): Class I"))
cases.append(c)

# ---- case 12
c = Case(12, "Permanent magnet, T_op above the candidate's Curie temperature", "Class I (step 2)", {"Class I"})
c.inp("Curie temperature of the candidate and T_op", "not numeric", "case premise states the comparison; M1 output has no Curie temperature (it prints mu0*Ms only)")
c.step2.append(("T_op vs Curie of g", "fail", "case premise: T_op above the candidate's Curie temperature"))
c.ambig.append(("the threshold failure is the case premise itself, so the case tests nothing numeric", "none"))
cases.append(c)

# ---- case 13
c = Case(13, "DC busbar, cross-section free (Al against Cu)", "Class II", {"Class II"})
c.kappa, c.n, c.slack = AREA_RATIO_AL_CU, 1.0, INF
c.inp("area ratio A_Al/A_Cu = sigma_Cu/sigma_Al", f"{AREA_RATIO_AL_CU}", src("a1_conductor_area_mass.txt", "area ratio A_Al/A_Cu = 1.63842"))
c.inp("slack: cross-section free", "inf", "case text")
cases.append(c)

# ---- case 14
c = Case(14, "Slot-limited winding, requirement 'carry I within the temperature limit' (Al against Cu)", "Class II (g expected to lose at high duty)", {"Class II"})
c.kappa, c.n, c.slack = AREA_RATIO_AL_CU, 1.0, None
c.inp("loss ratio at equal area = sigma_Cu/sigma_Al", f"{AREA_RATIO_AL_CU}", src("a1_conductor_area_mass.txt", "area ratio A_Al/A_Cu = 1.63842"))
c.inp("incumbent's thermal margin (T_limit - T_ambient)/(operating rise)", "not available", "no row and not in the case text; A4 is a step-5 comparison and supplies no margin")
c.missing.append(("incumbent's temperature-rise margin (slack in the 'within the temperature limit' requirement)", "step 3"))
c.ambig.append(("'slot-limited' fixes the area (area slack 1) but the requirement is a temperature, so the slack is the thermal margin, not the area slack", "if the area slack 1 were the slack: price 1.638 > 1 -> Class I; Class II iff the incumbent's rise is below 1/1.638 = 61% of the limit"))
c.ambig.append(("no cap = uncapped reading", "slack inf -> Class II (matches expected)"))
cases.append(c)

# ---- case 15
c = Case(15, "Same as 14 with requirement 'loss <= incumbent's loss'", "Class I (step 3, kappa = 1.64, no slack)", {"Class I"})
c.kappa, c.n, c.slack = AREA_RATIO_AL_CU, 1.0, 1.0
c.inp("loss ratio at equal area", f"{AREA_RATIO_AL_CU}", src("a1_conductor_area_mass.txt", "area ratio A_Al/A_Cu = 1.63842"))
c.inp("slack: loss cap = incumbent's loss", "1", "case text (requirement itself)")
cases.append(c)

# ---- case 16
c = Case(16, "Air-cooled heat sink, short fins (Al against Cu)", "Class II", {"Class II"})
kap = K_CU / K_AL
c.kappa, c.n, c.slack = kap, 0.5, None
c.inp("fin efficiency ratio Al(k=200)/Cu at h=50, L=30 mm, t=1 mm", f"{FIN_RATIO_AL200} (same-geometry price 1/ratio = {1/FIN_RATIO_AL200:.4f})", src("c1_fin_efficiency.txt", "ratio Al(200)/Cu: 0.93734"))
c.inp("k_Cu, k_Al (W/mK, MEMORY inputs of C1)", f"{K_CU}, {K_AL}", src("c1_fin_efficiency.txt", "k_Cu=400", "200 wrought 6063"))
c.kappa_note = f"kappa = {kap:.2f}; n = 1/2 gives {kap**0.5:.4f} (thick-fin bound); C1 same-geometry price {1/FIN_RATIO_AL200:.4f}"
c.missing.append(("envelope slack (allowed rise of base-to-air resistance or fin mass/height cap)", "step 3"))
c.ambig.append(("n: step 3 gives n = 1/2 for 'thick against fin length'; a short fin (mL ~ 0.5) is not thick, so the rule does not say which n applies", "n = 1/2 gives 1.414 (upper bound); the C1 price 1.067 is the exact same-geometry value; both > 1, so slack is still needed"))
c.ambig.append(("no cap stated", "uncapped reading: Class II (matches expected); slack 1: Class I"))
cases.append(c)

# ---- case 17
c = Case(17, "Oxygen evolution in an acidic membrane cell (Ni-Fe against Ir oxide)", "Class I (step 2, stability window; Pourbaix LOOKUP)", {"Class I"})
c.inp("stability of Ni-Fe oxide at OER potential in acid (Pourbaix)", "not available", "no row produced it ('Inputs from: -' in Note J1; the plan lists a Pourbaix LOOKUP with no row)")
c.step2.append(("chemical stability window of g (Ni-Fe in acid)", "unavailable", "no Pourbaix datum in any row"))
c.missing.append(("Pourbaix stability window of Ni-Fe oxide in acid at the OER potential", "step 2 (and the environment clause of step 1)"))
c.ambig.append(("step 1 clause 3 ('g and s cannot operate in the same environment') and step 2 ('chemical stability window') overlap", "if Ni-Fe is unstable in the acid the literal order exits at step 1 as out of scope, not Class I at step 2"))
cases.append(c)

# ---- case 18
c = Case(18, "Flow manifold, viscous loss", "Out of scope (step 1, no x-dependent coefficient)", {"out of scope"})
c.step1 = "no coefficient of the solid enters the governing equation (Hagen-Poiseuille P = 128*mu*L*Q^2/(pi*D^4) holds only fluid properties and D) -> out of scope"
c.inp("governing equation", "Hagen-Poiseuille, no solid coefficient", "plan G1.6 (analytic; no row computed it)")
c.ambig.append(("decided from the plan's equation only; no-slip walls assumed", "slip coatings, roughness set by process or wall strength limiting D would put a solid coefficient into the problem (G1.6 falsifier)"))
cases.append(c)

# ----------------------------------------------------------------------------------------------
print("J1 gate test matrix. Level: derived (unverified). Gate = plan section 5 (PROVISIONAL), applied literally.")
print("Rules used (see outputs/issues.md, Row J1):")
print(" R1 slack = cap / incumbent usage. 'free' in the case text = slack inf. A cap the case does not state = slack not supplied.")
print(" R2 slack >= 1 always (the incumbent fits its own cap), so a price kappa^n <= 1 passes step 3 without a stated slack.")
print(" R3 step 2 checks the thresholds the case names; a named threshold with no datum in any row is 'unavailable' and blocks step 2.")
print(" R4 'out of scope' needs step 1 to fail; an unstated envelope is NOT read as a step 1 failure (alternate reading listed per case).")
print()
n_match = 0
rows = []
for c in cases:
    out, step, trace = gate(c)
    ok = out in c.expected_set
    n_match += ok
    rows.append((c.num, out, c.expected_text, "MATCH" if ok else "MISMATCH", step))
    print("=" * 110)
    print(f"CASE {c.num}: {c.title}")
    print("Inputs and sources:")
    for d, v, s in c.inputs:
        print(f"  - {d}: {v}\n      source: {s}")
    if c.kappa is not None and c.n is not None and c.n == 0:
        print(f"  kappa: not needed (n = 0); {c.kappa_note}")
    elif c.kappa is not None:
        print(f"  kappa = {c.kappa:.5g}, n = {c.n:g}, price kappa^n = {c.kappa ** c.n:.5g}; slack = " + ("not supplied" if c.slack is None else ("inf (free)" if c.slack == INF else f"{c.slack:g}")))
        if c.kappa_note:
            print(f"  {c.kappa_note}")
    for m, st in c.missing:
        print(f"  INPUT NOT AVAILABLE: {m}; blocks {st}")
    print("Gate trace:")
    for ln in trace:
        print("  " + ln)
    if out == "undecided" and c.kappa is not None and c.slack is None and c.n is not None and c.n > 0:
        for lab, s_ in (("slack inf (no cap)", INF), ("slack 1 (incumbent at its cap)", 1.0)):
            o2, st2, _ = gate(c, slack=s_, use_case_slack=False)
            print(f"  conditional: with {lab}: {o2}" + (" (step 2 still open)" if c.step2 and any(x[1] == 'unavailable' for x in c.step2) else ""))
    for a, b in c.ambig:
        print(f"  AMBIGUITY: {a}\n      other reading: {b}")
    print(f"RESULT: outcome = {out}; deciding step = {step}")
    print(f"EXPECTED: {c.expected_text}")
    print(f"=> {'MATCH' if ok else 'MISMATCH'}")
print("=" * 110)
print("\nSUMMARY TABLE")
print(f"{'#':>2} | {'outcome':<12} | {'deciding step':<22} | {'match':<8} | expected")
for num, out, exp, m, st in rows:
    print(f"{num:>2} | {out:<12} | {st:<22} | {m:<8} | {exp}")
print(f"\nMATCH count: {n_match} of {len(cases)}")
print("MISMATCH cases: " + ", ".join(str(r[0]) for r in rows if r[3] == "MISMATCH"))
print("Undecided cases (missing input): " + ", ".join(str(r[0]) for r in rows if r[1] == "undecided"))
print("Level of all results: derived (unverified). Inputs marked MEMORY UNSURE in the source rows remain so.")
