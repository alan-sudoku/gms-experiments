#!/usr/bin/env python3
"""OQ-22 Part B (Prompt 8 D4): decompose the supply-chain energy of Pt and estimate B_infra(Pt); decide configuration A, B or C.

Brief Part B items 1 to 3 and convention 10. Level: derived (unverified). Element: Pt (better data than Ir: stage-resolved operating energy
for the PGE industry from company reports (Buchspies et al. 2017), a CED row with a secondary route, ERC and M&M values; Ir has none of these).

Inputs
  LOOKUP  stage energy shares 34/26/28/12 percent (mine / concentrator / smelter and converter / refinery), electricity share 75 percent,
          CED fossil 0.60 TJ per kg 6E PGE, electricity 0.15 TJ per kg 6E PGE (Buchspies et al. 2017, Minerals 7:225, section 4.1)
  LOOKUP  Pt CED rows (Nuss and Eckelman 2014 SI Table S38), allocation shares (SI S28, S30)
  LOOKUP  Pt M&M cost 291667 MJ/kg (IntechOpen ch. 62189, Table 1)
  MEMORY (UNSURE) every entry of INFRA and STAGE_FIXED in oq22_common.py: capital-goods share c, avoidable capital fraction a_cap,
          attributable fraction alpha_x, fixed fraction of each stage's operating energy. These cannot be taken from the sources read.
Assumptions: CED stage split = delivered-energy stage split (not exact: electricity carries ~3x upstream factor, fuels less); CED ~ CExC (kappa = 1).
Not estimable here: the recycling loop (secondary route is 23 percent of supply by Nuss) and re-establishment of smelters/refineries.

Run: <gms-local>/.venv/bin/python local_docs/fable_runs/oq_22_code/oq22_part_b.py   (any directory)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oq22_common as C  # noqa: E402

fails = 0


def check(name, ok, detail=""):
    global fails
    fails += (not ok)
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")


def sec(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


e_mix = C.SCEN["kappa"] * C.CED[("Pt", "TOTAL (supply mix)")]      # J/kg
MJ = 1e6

sec("B1 SOURCE CONDITIONS, REQ-LIFECYCLE-CEXC-SOURCE items 1 to 6 (met / not met / not stated, with evidence)")
rows = [
    ("S1 Nuss and Eckelman 2014 CED (ecoinvent 2.2 reallocated)",
     ["NOT MET: CED counts primary energy carriers; the ore itself is not an energy resource (CED, not exergy; no 'metals' category)",
      "NOT MET: CED has no reference environment; b_ch (Szargut 2005) is from another environment than any CExC",
      "MET: revenue (2006-2010 prices) for PGMs, Cu, Ni; ecoinvent had price 1993-2002; mass only for ore-to-metal within PGM (SI Pt entry, Table S30)",
      "NOT STATED: the SI text contains no statement on infrastructure or capital goods; ecoinvent 2.x unit processes usually include infrastructure (MEMORY UNSURE) -> likely not excluded",
      "MET for Pt, Ir as metal 'at refinery'; NOT MET for IrO2 (anode form) and for Pt/C",
      "NOT STATED: no list of monitoring, assaying or maintaining flows"]),
    ("S2 Bosch et al. 2007 CExD (ecoinvent categories)",
     ["MET by definition: category 'non-renewable material resources, metals' (ESU report Table 1) counts the exergy of the metal ore",
      "PARTLY: ESU report says reference environment 298.15 K and cites Szargut 1988/2005; the exact b_ch table per element not read",
      "NOT STATED in the ESU report; revenue allocation inherited from ecoinvent (UNSURE)",
      "NOT STATED (same ecoinvent datasets as S1)",
      "NOT STATED for Pt, Ir (factors not read: Bosch SI table not obtained)",
      "NOT STATED"]),
    ("S3 Thanatia 'mining and metallurgical cost' of Pt, 291667 MJ/kg (IntechOpen ch. 62189 Table 1)",
     ["NOT STATED: cost of mining and metallurgy; whether it contains ore exergy is not said",
      "STATED: Szargut reference environment 'with some improvements' (chapter text); Ir b_ch not used",
      "NOT STATED for Pt",
      "NOT STATED",
      "ELEMENT only ('Platinum')",
      "NOT STATED"]),
    ("S4 Buchspies et al. 2017 (company-reported energy, 2015)",
     ["NOT APPLICABLE: operating energy of the industry, no CExC",
      "NOT APPLICABLE",
      "NOT MET: energy per kg of 6E PGE total (no split); price allocation to single PGEs in its Table S1, not read",
      "MET (by omission): consumption data of energy carriers only, no capital goods",
      "6E PGE mixture, not a form",
      "PARTLY: all consumed energy of mine, concentrator, smelter, refinery is included, i.e. includes ventilation, cooling, pumping, utilities"]),
]
for nm, conds in rows:
    print(nm)
    for i, c in enumerate(conds, 1):
        print(f"   {i}. {c}")

sec("B2 DECOMPOSITION OF THE SOURCE'S SUPPLY-CHAIN ENERGY (Pt supply mix, CED 243000 MJ/kg) BY STAGE (assumption: CED stage split = delivered-energy split)")
sh = C.stage_shares()
for k, v in sh.items():
    print(f"  {k:18s} {v*100:4.0f} percent -> {v*e_mix/MJ:9.0f} MJ/kg Pt")
check("stage shares sum to 1 (LOOKUP, read from text: 34+26+28+12)", abs(sum(sh.values()) - 1) < 1e-9)
print("  Capital (fixed, and proportional to throughput): NOT split by the source (S1 gives CED per kg only, no process list read; S4 contains no capital).")
print("  Operating split fixed / variable per stage: NOT in any source read. Bracket from STAGE_FIXED (MEMORY UNSURE):")
for k, v in C.STAGE_FIXED.items():
    print(f"    {k:18s} fixed fraction of operating energy {v[0]:.2f} / {v[1]:.2f} / {v[2]:.2f} (lo/mid/hi)")
print(f"  fixed fraction of the operating energy f_op: {C.f_op(0):.3f} / {C.f_op(1):.3f} / {C.f_op(2):.3f}")
print("  Maintenance: no source read separates maintenance energy or sustaining capital. Not split.")

sec("B3 INDEPENDENT CONSISTENCY CHECK: Nuss/ecoinvent Pt burden vs Buchspies 2015 company data (per kg of PGM, different basis; not true by construction)")
kgPt, rev = C.ALLOC[("ZA", "Pt")]
kgPGM, revPGM = C.ALLOC[("ZA", "PGM_sum")]
B_total_per_kgPt = C.CED[("Pt", "primary South Africa")] / rev        # J per kg Pt, all products
per_kg_pgm_all = B_total_per_kgPt * kgPt / kgPGM
per_kg_pgm_only = per_kg_pgm_all * revPGM
print(f"  Nuss ZA: total burden per kg Pt (all co-products) {B_total_per_kgPt/MJ:.3g} MJ; per kg PGM incl. base-metal share {per_kg_pgm_all/MJ:.3g} MJ; PGM share only {per_kg_pgm_only/MJ:.3g} MJ per kg PGM (S28 1970-92 production mix)")
print(f"  Buchspies 2015: CED fossil {C.BUCH['CEDfossil_per_kg_6E']*1e6:.3g} MJ per kg 6E PGE (all burden of the PGE operations, no base-metal split)")
ratio = C.BUCH["CEDfossil_per_kg_6E"] * 1e6 * MJ / per_kg_pgm_all
print(f"  ratio Buchspies / Nuss (per kg PGM incl. base metals) = {ratio:.2f}; vs PGM share only = {C.BUCH['CEDfossil_per_kg_6E']*1e6*MJ/per_kg_pgm_only:.2f}")
print("  Buchspies states <20 percent agreement with ecoinvent on its own basis (Figure 13, not read); here the simple per-kg comparison differs by about a factor 2 (ore-grade decline since the ecoinvent data, basis differences). The CED row may therefore UNDERSTATE the 2015 supply chain by up to ~2x (UNSURE).")
up = C.BUCH["CEDfossil_per_1000t_ore"] / (C.BUCH["electricity_per_1000t_ore"] / C.BUCH["share_electricity_of_total_energy"])
print(f"  upstream multiplier CED fossil / delivered energy (Buchspies) = {up:.2f} (coal-power dominated)")
check("Buchspies/Nuss within a factor 3 (loose independent check)", 1 / 3 < ratio < 3, f"ratio {ratio:.2f}")

sec("B4 B_infra(Pt): sunk / avoidable-fixed / variable split, per kg Pt through the loop (supply-mix CED 243000 MJ/kg as e_tot). ALL INPUTS MEMORY (UNSURE). Corners: lo/mid/hi change all inputs together")
parts = [C.infra_split(i, e_mix) for i in range(3)]
print(f"{'quantity':52s} {'lo':>12s} {'mid':>12s} {'hi':>12s}   (MJ per kg Pt unless stated)")
def line(label, key, unit=1.0, fmt="%12.4g"):
    print(f"{label:52s} " + " ".join(fmt % (p[key] / unit) for p in parts))
line("capital-goods share c (of source energy)", "c")
line("operating energy (1-c) e", "op", MJ)
line("  operating, variable (proportional to throughput)", "op_variable" if False else "op_var", MJ)
line("  operating, fixed (ventilation, cooling, holding, utilities)", "op_fixed", MJ)
line("loop capital goods inside source (c e)", "cap", MJ)
line("  of which sunk (establishing existing loop)", "cap_sunk", MJ)
line("  of which avoidable (sustaining + re-establishing within tau_infra)", "cap_avoid", MJ)
line("fixed part F = op_fixed + capital", "fixed_total", MJ)
line("avoidable-fixed part", "avoid_fixed", MJ)
line("alpha = avoidable-fixed / F  (brief: avoidable fraction of the fixed part)", "alpha_fixed")
line("alpha_x: share of avoidable-fixed that leaves with Pt", "alpha_x")
line("b_infra = alpha_x x avoidable-fixed", "b_infra", MJ)
print(f"{'b_infra in J/kg':52s} " + " ".join("%12.4g" % p["b_infra"] for p in parts))
line("b_infra / e_tot", "rho")
print("  bracket of b_infra: %.3g to %.3g J/kg (%.0f x spread), mid %.3g J/kg = %.0f MJ/kg" % (parts[0]["b_infra"], parts[2]["b_infra"], parts[2]["b_infra"] / parts[0]["b_infra"], parts[1]["b_infra"], parts[1]["b_infra"] / MJ))
print("  Cannot be estimated from the sources read: the true fixed fraction of operating energy; the loop capital (no capital inventory read); the recycling loop; the sunk fraction; alpha_x (needs a model of what stops when Pt leaves every product while Pd, Rh, Ni and Cu still use the Bushveld loop).")
print("  Note on definitions: B_infra counts destroyed exergy of monitoring, assaying and maintaining; here 'avoidable fixed operating energy' is used as its proxy, which includes ventilation and cooling (maintaining the loop).")
check("avoidable-fixed + sunk + variable = e_tot (BY CONSTRUCTION of the split)", all(abs(p["cap_sunk"] + p["avoid_fixed"] + p["op_var"] - e_mix) / e_mix < 1e-12 for p in parts))

sec("B5 CONFIGURATION (A: loop outside CExC; B: capital goods inside; C: loop operating flows inside) and what the source fails")
for i, nm in enumerate(("lo", "mid", "hi")):
    p = parts[i]
    print(f"  {nm}: inside the CED row: capital goods {p['cap']/e_mix*100:.1f} percent (config B part, UNSURE whether included), fixed operating flows {p['op_fixed']/e_mix*100:.1f} percent (config C part); avoidable-fixed {p['avoid_fixed']/e_mix*100:.1f} percent; b_infra {p['rho']*100:.1f} percent")
print("  Evidence (inference, not a statement of the source): (i) the CED row comes from mine, concentrator, smelter and refinery operating data (ecoinvent from company data; Buchspies company data agree in kind), which contain every energy flow of the sites including ventilation, cooling, pumping, utilities: config C is in the data by construction of how such inventories are built, independent of any number above;")
print("            (ii) capital goods: ecoinvent unit processes normally carry infrastructure (MEMORY UNSURE), the SI does not say: config B likely, not shown;")
print("            (iii) no stage or fixed/variable split is published, so A cannot be told from C inside the data, which is the problem named in prompt_8_review.")
print("  Configuration for this source: MIX of B (probable) and C (certain in kind). Not A.")
print("  Fails as published: condition 4 (capital goods not declared, probably included) and condition 6 (no declaration of which loop flows are contained; fixed operating flows are contained). Also 1, 2 (CED is not an exergy table) and 5 (metal, not IrO2/Pt-C).")
print("  What an evaluation would have to remove from CExC(Pt) to meet 4 and 6: capital goods c e = %.0f to %.0f MJ/kg (mid %.0f), plus the avoidable-fixed operating flows counted in B_infra: alpha_x x op_fixed = %.0f to %.0f MJ/kg (mid %.0f)." % (
    parts[0]["cap"] / MJ, parts[2]["cap"] / MJ, parts[1]["cap"] / MJ,
    parts[0]["alpha_x"] * parts[0]["op_fixed"] / MJ, parts[2]["alpha_x"] * parts[2]["op_fixed"] / MJ, parts[1]["alpha_x"] * parts[1]["op_fixed"] / MJ))
print("  Effect on the OQ-22 number: if the avoidable flows sit inside CExC, adding lambda double counts them (Part A 'lambda' rows are then an upper bound); moving them out of CExC and into lambda leaves Delta_eta_be unchanged. Delta_eta_be (Pt central) is unchanged to within the b_infra fraction: +%.1f / +%.1f / +%.1f percent (lo/mid/hi) of the extraction term." % (parts[0]["rho"] * 100, parts[1]["rho"] * 100, parts[2]["rho"] * 100))
print("  Under config B with lambda = 0, CExC returns an average share of the whole loop capital to the incumbent: the bypass named in REQ-LIFECYCLE-CEXC-SOURCE item 4; size c e = %.1f to %.1f percent of Sigma_s,init for this source." % (parts[0]["c"] * 100, parts[2]["c"] * 100))

sec("B6 OVERALL")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
