#!/usr/bin/env python3
"""Shared inputs and functions for the OQ-22 check (imported by oq22_part_a.py and oq22_part_b.py).

Not run on its own. Level: derived (unverified). Conventions refer to local_docs/fable_runs/oq_22_brief.md.

Inputs and status
  LOOKUP  data/ced_nuss_eckelman_2014.csv   CED of Pt, Ir, Ni, Fe (Nuss and Eckelman 2014, SI S1 Table S38)
  LOOKUP  data/bch_szargut_2005.csv         b_ch of Pt, Ir, Ni, Fe (Szargut et al. 2005, Exergoecology Portal table)
  LOOKUP  data/thanatia_erc.csv             ERC and M&M cost (Valero et al.; Torres et al. 2026 dataset)
  LOOKUP  data/nuss_pgm_allocation.csv      PGM production and allocation shares (Nuss and Eckelman SI S28, S30)
  LOOKUP  data/buchspies_2017_pge.csv       stage energy shares of PGE production (Buchspies et al. 2017)
  MEMORY (UNSURE) atomic masses Pt 195.084, Ir 192.217, Ni 58.693, Fe 55.845 g/mol (standard values)
  MEMORY (UNSURE) all scenario bounds listed in the SCEN and INFRA dictionaries below
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
T0 = 298.15            # K, convention 1
HOUR = 3600.0

MOLAR_MASS = {"Pt": 0.195084, "Ir": 0.192217, "Ni": 0.058693, "Fe": 0.055845}   # kg/mol, MEMORY (UNSURE)


def read_csv(name):
    with open(os.path.join(DATA, name), newline="") as f:
        lines = [l for l in f if not l.startswith("#")]
    return list(csv.DictReader(lines))


def _load():
    ced = {}
    for r in read_csv("ced_nuss_eckelman_2014.csv"):
        ced[(r["metal"], r["row"])] = float(r["CED_MJ_per_kg"]) * 1e6        # J/kg
    bch = {r["element"]: float(r["bch_kJ_per_mol"]) * 1e3 for r in read_csv("bch_szargut_2005.csv")}  # J/mol
    erc = {}
    for r in read_csv("thanatia_erc.csv"):
        erc[r["element"]] = {k: (float(v) * 1e6 if v else None) for k, v in r.items() if k != "element"}
    alloc = {(r["country"], r["item"]): (float(r["kg_1970_1992"]), float(r["rev_share_S30"])) for r in read_csv("nuss_pgm_allocation.csv")}
    buch = {r["quantity"]: float(r["value"]) for r in read_csv("buchspies_2017_pge.csv")}
    return ced, bch, erc, alloc, buch


CED, BCH_MOL, THANATIA, ALLOC, BUCH = _load()


def bch_kg(el):
    """b_ch per kg, J/kg."""
    return BCH_MOL[el] / MOLAR_MASS[el]


# Scenario inputs (all MEMORY / UNSURE unless stated)
SCEN = dict(
    kappa=1.0,            # CED-to-CExC factor (MEMORY UNSURE; swept 0.8 to 1.5 in the lever table)
    b_transport=1.0e6,    # J/kg; inside the 0.5e6 to 1.5e6 range of EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL (spec range, not a source)
    R_rec_central=0.9,    # central recycling efficiency (scenario value)
    wremelt_ratio_Pt=None,  # filled below from LOOKUP: secondary CED / primary CED of Pt
    hydroxide_mass_factor=1.0 / 0.6,   # M_g = metal mass / 0.6 (MEMORY UNSURE)
    ni_mass_frac=3 * MOLAR_MASS["Ni"] / (3 * MOLAR_MASS["Ni"] + MOLAR_MASS["Fe"]),   # Ni:Fe = 3:1 molar, derived
)
SCEN["fe_mass_frac"] = 1.0 - SCEN["ni_mass_frac"]
SCEN["wremelt_ratio_Pt"] = CED[("Pt", "secondary")] / CED[("Pt", "TOTAL (supply mix)")]   # LOOKUP ratio, used as proxy for w_lost,remelt/CExC

# Side g cases. Composition: NiFe oxyhydroxide/LDH, Ni:Fe = 3:1 (molar), loading as metal mass.
G_CASES = {
    # loading kg metal/m2, psi = w_lost,prec / (CExC - b_ch) multiplier, B_mfg J/m2 (yield-adjusted manufacturing, delivered energy)
    "g_low":  dict(L=0.01, psi=1.0, B_mfg=0.0),        # 1 mg/cm2, precursor adds nothing, manufacturing 0
    "g_high": dict(L=0.05, psi=3.0, B_mfg=50e6),       # 5 mg/cm2, precursor 3x extraction work, manufacturing 50 MJ/m2 (MEMORY UNSURE upper bound)
}

# Sources rows: (element, row name) -> CExC per kg before kappa, J/kg; plus the allocation country
SOURCE_ROWS = {
    "Pt": [("mix", ("Pt", "TOTAL (supply mix)"), None), ("ZA", ("Pt", "primary South Africa"), "ZA"), ("RU", ("Pt", "primary Russia"), "RU")],
    "Ir": [("mix", ("Ir", "TOTAL (supply mix)"), None), ("ZA", ("Ir", "primary South Africa"), "ZA"), ("RU", ("Ir", "primary Russia"), "RU")],
}
THANATIA_PT_MM = THANATIA["Pt"]["MM_total_MJ_per_kg"]          # J/kg (exergy cost of mining and metallurgy, Pt)

LOADINGS = [("Ir", 0.2), ("Ir", 1.0), ("Ir", 2.0), ("Pt", 0.1), ("Pt", 0.5)]   # mg/cm2 (convention 6)
J_GRID = [0.2, 0.5, 1.0, 2.0]               # A/cm2
TAU_GRID_H = [2e4, 4e4, 8e4]
J_CENTRAL, TAU_CENTRAL_H = 1.0, 8e4
R_REC_SET = [0.0, 0.5, 0.9, 0.95]


def mg_cm2_to_kg_m2(x):
    return x * 1e-2        # 1 mg/cm2 = 1e-6 kg / 1e-4 m2 = 1e-2 kg/m2


def alloc_factor(country, el, rule):
    """Per-kg burden of el under allocation rule, divided by the published (revenue) burden. Derived from SI S28 and S30 shares.
    per-kg burden under a rule = B_total * share_rule(el) / m_el, so the ratio to revenue = share_rule / rev_share."""
    kg_el, rev_el = ALLOC[(country, el)]
    kg_pgm, rev_pgm = ALLOC[(country, "PGM_sum")]
    kg_all, _ = ALLOC[(country, "ALL_incl_CuNi")]
    if rule == "revenue":
        return 1.0
    if rule == "mass_all":            # mass of all co-products incl. Cu and Ni
        return (kg_el / kg_all) / rev_el
    if rule == "pgm_revenue_then_mass":   # PGM group gets its revenue share, split among PGMs by mass
        return (rev_pgm * kg_el / kg_pgm) / rev_el
    raise ValueError(rule)


def w_remelt_kg(el, cexc_kg):
    """w_lost,remelt per kg (J/kg): proxy = (secondary-route CED / primary CED of Pt) x CExC of the row. UNSURE; for Pt the Pt ratio, for Ir the same ratio."""
    return SCEN["wremelt_ratio_Pt"] * cexc_kg


def side_s(el, m, cexc_kg, R, binfra=0.0, extra_cexc_kg=0.0, wremelt_scale=1.0):
    """Side s terms, J/K per m2. EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL, -EOL, EQ-LIFECYCLE-SUPPLY-CHAIN-COST. extra_cexc_kg is added to CExC (ERC diagnostic)."""
    bch = bch_kg(el)
    cx = cexc_kg + extra_cexc_kg
    s_init_ext = m * (cx - bch) / T0
    s_init_tr = m * SCEN["b_transport"] / T0
    s_eol = (m / T0) * (R * wremelt_scale * w_remelt_kg(el, cexc_kg) + (1 - R) * bch)
    lam = binfra * m / T0
    return dict(init_ext=s_init_ext, init_tr=s_init_tr, init=s_init_ext + s_init_tr, eol=s_eol, lam=lam)


def side_g(case, erc=False, kappa=None):
    """Side g terms, J/K per m2. EQ-LIFECYCLE-GEOMETRY-INITIAL-CAPITAL (tooling = computation = 0), EQ-LIFECYCLE-GEOMETRY-EOL with R_rec = 0 for Ni and Fe."""
    k = SCEN["kappa"] if kappa is None else kappa
    c = G_CASES[case]
    out_prec = 0.0
    out_eol = 0.0
    masses = {"Ni": c["L"] * SCEN["ni_mass_frac"], "Fe": c["L"] * SCEN["fe_mass_frac"]}
    for el, m in masses.items():
        cexc = k * CED[(el, "TOTAL (supply mix)" if el == "Ni" else "TOTAL (pig iron)")]
        if erc:
            cexc += THANATIA[el]["ERC_MJ_per_kg"]
        out_prec += m * c["psi"] * (cexc - bch_kg(el))
        out_eol += m * bch_kg(el)      # R_rec = 0: pays b_ch at dispersal
    M_g = c["L"] * SCEN["hydroxide_mass_factor"]
    init = (out_prec + M_g * SCEN["b_transport"] + c["B_mfg"]) / T0
    return dict(init=init, init_prec=out_prec / T0, init_tr=M_g * SCEN["b_transport"] / T0, init_mfg=c["B_mfg"] / T0, eol=out_eol / T0)


def delta_eta_be(s, g, j_A_cm2, tau_h, r_el=1.0):
    """Break-even overpotential penalty in V (convention 3): T0 [S_s,init + S_s,EOL + lam - S_g,init - S_g,EOL] / (j tau). r_el divides it (convention 11)."""
    j = j_A_cm2 * 1e4
    tau = tau_h * HOUR
    return T0 * (s["init"] + s["eol"] + s["lam"] - g["init"] - g["eol"]) / (j * tau) / r_el


def classify(d_V):
    mv = d_V * 1e3
    return "nearly free" if mv < 10 else ("priced" if mv > 30 else "between")


# ---------------- Part B estimate of b_infra (all MEMORY, UNSURE) ----------------
# b_infra = alpha_Pt * e_tot * [ f_op * (1 - c) + a_cap * c ]    (J per kg of Pt through the loop over tau_infra)
INFRA = {
    #            lo     mid    hi
    "c":       (0.01, 0.05, 0.30),   # capital-goods share of the source's supply-chain energy (ecoinvent-type infrastructure share 1 to 10 percent; financial-intensity route up to ~30 percent)
    "a_cap":   (0.20, 0.45, 0.70),   # avoidable fraction of loop capital within tau_infra (sustaining capital + re-establishment) ; the rest is sunk
    "alpha_x": (0.05, 0.30, 0.60),   # fraction of the avoidable-fixed loop exergy that leaves with x (co-product loop shared with Pd, Rh, Ni, Cu)
}
# fixed fraction of the operating energy of each stage (ventilation, cooling, dewatering, holding furnaces, utilities): lo, mid, hi (MEMORY UNSURE)
STAGE_FIXED = {"mine": (0.30, 0.45, 0.60), "concentrator": (0.05, 0.10, 0.15), "smelter_converter": (0.15, 0.25, 0.40), "refinery": (0.10, 0.20, 0.30)}


def stage_shares():
    return {"mine": BUCH["share_energy_mine"], "concentrator": BUCH["share_energy_concentrator"],
            "smelter_converter": BUCH["share_energy_smelter_converter"], "refinery": BUCH["share_energy_refinery"]}


def f_op(idx):
    sh = stage_shares()
    return sum(sh[k] * STAGE_FIXED[k][idx] for k in sh)


def infra_split(idx, e_tot_J_per_kg):
    """Return dict of the parts (J per kg of x) for bracket index idx (0 lo, 1 mid, 2 hi). Corner choice: all inputs at lo, mid or hi together."""
    c, a, al = INFRA["c"][idx], INFRA["a_cap"][idx], INFRA["alpha_x"][idx]
    fo = f_op(idx)
    cap = c * e_tot_J_per_kg
    op = (1 - c) * e_tot_J_per_kg
    op_fixed = fo * op
    op_var = (1 - fo) * op
    cap_sunk = (1 - a) * cap
    cap_avoid = a * cap
    fixed_total = op_fixed + cap                  # fixed part of the loop = fixed operating + all loop capital
    avoid_fixed = op_fixed + cap_avoid
    alpha_fixed = avoid_fixed / fixed_total       # brief: avoidable fraction of the fixed part
    b_infra = al * avoid_fixed
    return dict(c=c, a_cap=a, alpha_x=al, f_op=fo, cap=cap, op=op, op_fixed=op_fixed, op_var=op_var, cap_sunk=cap_sunk, cap_avoid=cap_avoid,
                fixed_total=fixed_total, avoid_fixed=avoid_fixed, alpha_fixed=alpha_fixed, b_infra=b_infra, rho=b_infra / e_tot_J_per_kg)
