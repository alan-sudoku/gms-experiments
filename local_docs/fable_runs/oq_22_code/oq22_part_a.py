#!/usr/bin/env python3
"""OQ-22 Part A: does GMS-100's Sigma_init price a scarce catalyst? Break-even overpotential penalty of a NiFe candidate against Pt or Ir.

Brief conventions 1 to 13 (local_docs/fable_runs/oq_22_brief.md). Level: derived (unverified).
Terms used exactly: EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL, -INCUMBENT-EOL, -GEOMETRY-INITIAL-CAPITAL (tooling = computation = 0), -GEOMETRY-EOL,
EQ-LIFECYCLE-SUPPLY-CHAIN-COST. Delta_eta_be = T0 [S_s,init + S_s,EOL + lam - S_g,init - S_g,EOL] / (j tau). No replacement (tau_wearout = inf both sides, K_ox = 0).
Basis: 1 m2 of geometric electrode area, T0 = 298.15 K. Catalyst mass only (supports and shared layers cancel; stated assumption).

Inputs (status in oq22_common.py docstring and printed below): LOOKUP CED, b_ch, ERC, allocation shares; MEMORY (UNSURE) kappa, b_transport, atomic masses,
side-g bounds, lambda estimate (from the Part B bracket), w_lost,remelt proxy, omitted-stage multipliers.
Not a GMS-100 term: the ERC table. Outside GMS-100's boundary: the omitted-stage column.

Run: <gms-local>/.venv/bin/python local_docs/fable_runs/oq_22_code/oq22_part_a.py   (any directory)
"""
import os
import sys
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oq22_common as C  # noqa: E402

fails = 0


def check(name, ok, detail=""):
    global fails
    fails += (not ok)
    print(f"CHECK {name}: {'PASS' if ok else 'FAIL'} {detail}")


def sec(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


KAPPA = C.SCEN["kappa"]
T0 = C.T0

# ---------------------------------------------------------------- inputs
sec("A0 INPUTS (value, unit, status, source)")
print("T0 = 298.15 K (convention 1)")
print("kappa (CED -> CExC) = %.2f  MEMORY (UNSURE): assumed because CED counts primary energy carriers (exergy/energy of fuels ~1, electricity 1); swept 0.8..1.5 in A6" % KAPPA)
for (m, r), v in C.CED.items():
    print(f"  CED {m:2s} {r:24s} {v/1e6:>10.1f} MJ/kg  LOOKUP Nuss and Eckelman 2014 SI S1 Table S38 (data/ced_nuss_eckelman_2014.csv)")
for el in ("Pt", "Ir", "Ni", "Fe"):
    print(f"  b_ch {el}: {C.BCH_MOL[el]/1e3:.2f} kJ/mol = {C.bch_kg(el)/1e6:.4f} MJ/kg   LOOKUP Szargut et al. 2005 (Exergoecology Portal Table 1); molar mass {C.MOLAR_MASS[el]*1e3:.3f} g/mol MEMORY (UNSURE)")
print(f"  Thanatia: Pt ERC {C.THANATIA['Pt']['ERC_MJ_per_kg']/1e6:.0f} MJ/kg, Pt M&M {C.THANATIA_PT_MM/1e6:.0f} MJ/kg (IntechOpen ch. 62189 Table 1, LOOKUP); Ni ERC {C.THANATIA['Ni']['ERC_MJ_per_kg']/1e6:.1f}, Fe ERC {C.THANATIA['Fe']['ERC_MJ_per_kg']/1e6:.2f} MJ/kg (Torres et al. 2026 dataset, LOOKUP); Ir: no value readable")
print(f"  b_transport = {C.SCEN['b_transport']:.1e} J/kg  (inside the spec range 0.5e6 to 1.5e6; scenario value, not a source)")
print(f"  R_rec central = {C.SCEN['R_rec_central']}, set {C.R_REC_SET}; w_lost,remelt proxy = {C.SCEN['wremelt_ratio_Pt']:.4f} x CExC (ratio of Pt secondary CED 11900 to Pt supply-mix CED 243000, LOOKUP ratio, proxy use UNSURE)")
print(f"  side g: NiFe oxyhydroxide, Ni:Fe = 3:1 molar -> mass fractions Ni {C.SCEN['ni_mass_frac']:.3f}, Fe {C.SCEN['fe_mass_frac']:.3f} (derived from molar masses); loading is metal mass")
for k, v in C.G_CASES.items():
    print(f"    {k}: loading {v['L']*100:.0f} mg/cm2 metal, w_lost,prec = {v['psi']:.0f} x (CExC - b_ch), B_mfg = {v['B_mfg']/1e6:.0f} MJ/m2 (MEMORY UNSURE bounds), tooling = computation = 0, R_rec(Ni) = R_rec(Fe) = 0")
infra_mid = C.infra_split(1, 1.0)
print(f"  lambda estimate: b_infra/CExC = {C.infra_split(0,1.0)['rho']:.4f} (lo) / {infra_mid['rho']:.4f} (mid) / {C.infra_split(2,1.0)['rho']:.4f} (hi), from Part B bracket (MEMORY UNSURE). For Ir the same fraction is assumed (same loop, UNSURE).")
print("  lambda = b_infra m''/T0 assumes every position has the same loading m'' and N_alloc = (mass of x through the loop over tau_infra)/m''.")
print("  Replacement: tau_wearout = inf both sides. A candidate replacement would add R_g to side g and could only lower Delta_eta_be.")

# ---------------------------------------------------------------- helpers
def row_cexc(el, name, rule="revenue"):
    """CExC per kg of the row in J/kg (kappa x CED x allocation factor)."""
    for rn, key, country in C.SOURCE_ROWS[el]:
        if rn == name:
            f = C.alloc_factor(country, el, rule) if country else 1.0
            if country is None and rule != "revenue":
                raise ValueError("allocation variants only for primary rows")
            return KAPPA * C.CED[key] * f
    raise KeyError(name)


def rho_infra(idx=1):
    return C.infra_split(idx, 1.0)["rho"]


def dbe(el, mgcm2, cexc_kg, g_case, j=C.J_CENTRAL, tau=C.TAU_CENTRAL_H, R=None, lam_idx=None, r_el=1.0, erc_s=0.0, erc_g=False, omit=0.0, wscale=1.0):
    R = C.SCEN["R_rec_central"] if R is None else R
    m = C.mg_cm2_to_kg_m2(mgcm2)
    binfra = 0.0 if lam_idx is None else rho_infra(lam_idx) * cexc_kg
    s = C.side_s(el, m, cexc_kg, R, binfra=binfra, extra_cexc_kg=erc_s, wremelt_scale=wscale)
    if omit:
        s = dict(s)
        s["init"] += omit * m * (cexc_kg - C.bch_kg(el)) / T0     # omitted synthesis, ink, coating as a fraction of extraction work
    g = C.side_g(g_case, erc=erc_g)
    return C.delta_eta_be(s, g, j, tau, r_el), s, g


mv = lambda x: x * 1e3

# ---------------------------------------------------------------- G2.6 reproduction
sec("A1 G2.6 REPRODUCTION (Pt 0.5 mg/cm2, 0.5 A/cm2, 8e4 h) from its own formula d_eta = e m'' / (j tau)")
m = 5e-3; jj = 5e3; tt = 2.88e8
for nm, key in (("supply mix", ("Pt", "TOTAL (supply mix)")), ("primary ZA", ("Pt", "primary South Africa")), ("primary RU", ("Pt", "primary Russia"))):
    d = C.CED[key] * m / (jj * tt)
    print(f"  {nm:12s} e = {C.CED[key]/1e6:8.0f} MJ/kg -> {mv(d):.3f} mV")
d_up = 430000e6 * m / (jj * tt)
print(f"  upper bound (97.5% of the RU row, 430000 MJ/kg) -> {mv(d_up):.3f} mV")
check("G2.6 values 0.84, 1.07, 1.13, 1.5 mV (ARITHMETIC REPRODUCTION, same formula as the claim, not an independent check)",
      abs(mv(C.CED[('Pt','TOTAL (supply mix)')]*m/(jj*tt)) - 0.84) < 0.01 and abs(mv(C.CED[('Pt','primary South Africa')]*m/(jj*tt)) - 1.07) < 0.01 and abs(mv(d_up) - 1.5) < 0.02)
print("  GMS-100 terms at the same point (g-high / g-low, R_rec = 0.9, lambda = 0 and lambda = estimate):")
for lam in (None, 1):
    for gc in ("g_high", "g_low"):
        d, s, g = dbe("Pt", 0.5, row_cexc("Pt", "mix"), gc, j=0.5, tau=8e4, lam_idx=lam)
        print(f"    lambda={'0' if lam is None else 'mid'} {gc}: {mv(d):.4f} mV   [S_s,init {s['init']:.4g}, S_s,EOL {s['eol']:.4g}, lam {s['lam']:.4g}, S_g,init {g['init']:.4g}, S_g,EOL {g['eol']:.4g} J/K per m2]")
d0, s0, _ = dbe("Pt", 0.5, row_cexc("Pt", "mix"), "g_high", j=0.5, tau=8e4)
bch_share_pt = C.bch_kg("Pt") / row_cexc("Pt", "mix")
print(f"  what GMS-100 changes relative to G2.6: (1) -b_ch: b_ch/CExC(Pt mix) = {bch_share_pt:.3e}, effect on S_s,init {-bch_share_pt*100:.5f} percent;")
print(f"    (2) transport term share of S_s,init: {s0['init_tr']/s0['init']:.3e};  (3) EOL term at R_rec=0.9 adds {s0['eol']/s0['init']*100:.2f} percent of S_s,init (remelt proxy, UNSURE);")
dd, ss, gg = dbe("Pt", 0.5, row_cexc("Pt", "mix"), "g_high", j=0.5, tau=8e4, R=0.0)
print(f"    at R_rec=0 the EOL term is only b_ch: {ss['eol']/ss['init']*100:.2e} percent of S_s,init; (4) side g subtracts {gg['init']/s0['init']*100:.2f} percent (g_high) of S_s,init; (5) lambda: see A3.")

# ---------------------------------------------------------------- term tables
sec("A2 TERM TABLE per loading (J/K per m2), central duty j = 1 A/cm2, tau = 8e4 h, R_rec = 0.9, supply-mix row")
print(f"{'x':3s} {'mg/cm2':>7s} {'S_s,init':>11s} {'(ext)':>11s} {'(transp)':>10s} {'S_s,EOL':>11s} {'lam_mid':>11s} {'lam_lo':>10s} {'lam_hi':>10s} {'S_g,init hi':>11s} {'S_g,EOL hi':>10s} {'S_g,init lo':>11s}")
for el, ld in C.LOADINGS:
    cx = row_cexc(el, "mix")
    d, s, g = dbe(el, ld, cx, "g_high", lam_idx=1)
    gl = C.side_g("g_low")
    lamlo = rho_infra(0) * cx * C.mg_cm2_to_kg_m2(ld) / T0
    lamhi = rho_infra(2) * cx * C.mg_cm2_to_kg_m2(ld) / T0
    print(f"{el:3s} {ld:7.1f} {s['init']:11.4g} {s['init_ext']:11.4g} {s['init_tr']:10.3g} {s['eol']:11.4g} {s['lam']:11.4g} {lamlo:10.3g} {lamhi:10.3g} {g['init']:11.4g} {g['eol']:10.3g} {gl['init']:11.4g}")
gh = C.side_g("g_high")
print(f"side g (high) parts: precursor {gh['init_prec']:.4g}, transport {gh['init_tr']:.3g}, manufacturing {gh['init_mfg']:.4g}, EOL {gh['eol']:.4g} J/K per m2  -> upper bound on S_g,init = {gh['init']:.4g} J/K per m2 = {gh['init']*T0/1e6:.1f} MJ/m2")
gl = C.side_g("g_low")
print(f"side g (low): S_g,init = {gl['init']:.4g} J/K per m2 = {gl['init']*T0/1e6:.3f} MJ/m2")
print("g side share of S_s,init (g_high / g_low), supply-mix row:")
for el, ld in C.LOADINGS:
    cx = row_cexc(el, "mix"); s = C.side_s(el, C.mg_cm2_to_kg_m2(ld), cx, 0.9)
    print(f"  {el} {ld:4.1f} mg/cm2: {C.side_g('g_high')['init']/s['init']*100:6.2f} percent / {C.side_g('g_low')['init']/s['init']*100:6.3f} percent")
print("  -> the g side is NOT negligible for the lowest loadings (Pt 0.1, Ir 0.2) at the stated upper bound (it is dominated by the 50 MJ/m2 manufacturing bound); g_high and g_low are both reported.")

# ---------------------------------------------------------------- central case classes
sec("A3 CENTRAL CASE (j = 1 A/cm2, tau = 8e4 h, r_el = 1, R_rec = 0.9): Delta_eta_be in mV and class (nearly free < 10, priced > 30, between otherwise)")
rows_pt = [("mix", None), ("ZA", None), ("RU", None)]
hdr = f"{'x':3s} {'mg/cm2':>6s} {'row':>12s} | {'lam=0 g_high':>13s} {'class':>11s} | {'lam=0 g_low':>12s} {'class':>11s} | {'lam_mid g_high':>14s} {'class':>11s} | {'lam_hi g_low':>12s} {'class':>11s}"
print(hdr)
central_classes = {}
allrows = []
for el, ld in C.LOADINGS:
    names = ["mix", "ZA", "RU"] + (["ThanatiaMM"] if el == "Pt" else [])
    for nm in names:
        if nm == "ThanatiaMM":
            cx = C.THANATIA_PT_MM            # exergy, no kappa
        else:
            cx = row_cexc(el, nm)
        out = []
        for lam, gc in ((None, "g_high"), (None, "g_low"), (1, "g_high"), (2, "g_low")):
            d, _, _ = dbe(el, ld, cx, gc, lam_idx=lam)
            out.append((mv(d), C.classify(d)))
            central_classes[(el, ld, nm, lam, gc)] = (mv(d), C.classify(d))
        allrows.append((el, ld, nm))
        label = nm + ("*" if nm == "ThanatiaMM" else "")
        print(f"{el:3s} {ld:6.1f} {label:>12s} | {out[0][0]:13.4f} {out[0][1]:>11s} | {out[1][0]:12.4f} {out[1][1]:>11s} | {out[2][0]:14.4f} {out[2][1]:>11s} | {out[3][0]:12.4f} {out[3][1]:>11s}")
print("  * Thanatia 'mining and metallurgical cost' of Pt (exergy, MJ/kg 291667), not a CED row. lam_mid uses the mid b_infra fraction, lam_hi the high one (Part B bracket).")
vals = [v[0] for v in central_classes.values()]
print(f"  range over all central rows: {min(vals):.4f} to {max(vals):.4f} mV ; classes present: {sorted(set(v[1] for v in central_classes.values()))}")
for el in ("Ir", "Pt"):
    vv = [v[0] for k, v in central_classes.items() if k[0] == el]
    print(f"  {el}: {min(vv):.4f} to {max(vv):.4f} mV")
for el, ld in C.LOADINGS:
    vv = [v[0] for k, v in central_classes.items() if k[0] == el and k[1] == ld]
    cl = sorted(set(v[1] for k, v in central_classes.items() if k[0] == el and k[1] == ld))
    print(f"  {el} {ld} mg/cm2: {min(vv):.4f} to {max(vv):.4f} mV, class {cl}")

# ---------------------------------------------------------------- grid
sec("A4 DUTY GRID: Delta_eta_be in mV (rows j, columns tau). R_rec = 0.9, r_el = 1. Shown: supply-mix row, side g = g_high (lowest) and g_low (highest); lambda = 0 and lambda_mid / lambda_hi")
def grid(el, ld, nm, gc, lam):
    cx = row_cexc(el, nm)
    print(f"--- {el} {ld} mg/cm2, row {nm}, {gc}, lambda={'0' if lam is None else ['lo','mid','hi'][lam]}")
    print("   j\\tau[h]  " + "  ".join(f"{t:>10.0e}" for t in C.TAU_GRID_H))
    for j in C.J_GRID:
        print(f"   {j:5.1f}      " + "  ".join(f"{mv(dbe(el, ld, cx, gc, j=j, tau=t, lam_idx=lam)[0]):10.4f}" for t in C.TAU_GRID_H))
for el, ld in C.LOADINGS:
    grid(el, ld, "mix", "g_high", None)
for el, ld in C.LOADINGS:
    grid(el, ld, "mix", "g_low", 2)
# extreme corner over everything
print("\nExtremes over the whole grid, all rows, g cases, lambda in {0, hi}: ")
for el, ld in C.LOADINGS:
    vals = []
    for nm in ["mix", "ZA", "RU"]:
        cx = row_cexc(el, nm)
        for gc, lam in (("g_high", None), ("g_low", 2)):
            for j in C.J_GRID:
                for t in C.TAU_GRID_H:
                    vals.append(mv(dbe(el, ld, cx, gc, j=j, tau=t, lam_idx=lam)[0]))
    nf = sum(v < 10 for v in vals); pr = sum(v > 30 for v in vals)
    print(f"  {el} {ld:4.1f} mg/cm2: min {min(vals):8.4f}  max {max(vals):8.4f} mV; points < 10 mV: {nf}/{len(vals)}; > 30 mV: {pr}/{len(vals)}")
print("  10 mV is reached inside the grid by Ir 1 and 2 mg/cm2 and Pt 0.5 mg/cm2 (low j, short tau); never by Ir 0.2 and Pt 0.1. 30 mV is reached only by Ir 2 mg/cm2 with lambda_hi and g_low at j = 0.2 A/cm2, tau = 2e4 h; for the other loadings the grid cannot bracket 30 mV (A6 gives the factors).")

# G2.6 point
print("\nG2.6 point (j = 0.5 A/cm2, tau = 8e4 h), supply-mix row, lambda = 0 / lambda_mid, g_high / g_low (mV):")
for el, ld in C.LOADINGS:
    cx = row_cexc(el, "mix")
    a = mv(dbe(el, ld, cx, "g_high", j=0.5, tau=8e4)[0]); b = mv(dbe(el, ld, cx, "g_low", j=0.5, tau=8e4)[0])
    c2 = mv(dbe(el, ld, cx, "g_high", j=0.5, tau=8e4, lam_idx=1)[0]); d2 = mv(dbe(el, ld, cx, "g_low", j=0.5, tau=8e4, lam_idx=1)[0])
    print(f"  {el} {ld:4.1f}: lam0 {a:.4f} / {b:.4f} ; lam_mid {c2:.4f} / {d2:.4f}")

# ---------------------------------------------------------------- allocation (Ir co-product)
sec("A5 BY-PRODUCT ALLOCATION RULE (convention 7): central case, lambda = 0, g_high (mV); factor = per-kg burden under the rule / published revenue burden (derived from SI S28, S30)")
print(f"{'x':3s} {'mg/cm2':>6s} {'row':>4s} {'rule':>24s} {'factor':>9s} {'CED MJ/kg':>11s} {'d_eta mV':>10s} {'class':>12s}")
for el, ld in ((("Ir", 2.0), ("Ir", 0.2), ("Pt", 0.5), ("Pt", 0.1))):
    for nm in ("ZA", "RU"):
        for rule in ("revenue", "pgm_revenue_then_mass", "mass_all"):
            country = nm
            f = C.alloc_factor(country, el, rule)
            cx = row_cexc(el, nm, rule)
            d, _, _ = dbe(el, ld, cx, "g_high")
            print(f"{el:3s} {ld:6.1f} {nm:>4s} {rule:>24s} {f:9.4g} {cx/1e6:11.1f} {mv(d):10.4f} {C.classify(d):>12s}")
print("  Revenue = the rule of Nuss and Eckelman Table S38 as published. 'mass_all' spreads the ore burden per kg over PGM, Cu and Ni alike; Ir then costs about as much per kg as Ni. Both are derived here from S28/S30 shares, not published rows. Negative values: Sigma_s,init is below Sigma_g (g_high) at zero penalty, so the candidate wins for any Delta_eta >= 0; a mass rule makes the scarce catalyst nearly free by construction of the rule (it prices Ir like Ni).")
ir_mass_share = C.ALLOC[("ZA", "Ir")][0] / C.ALLOC[("ZA", "ALL_incl_CuNi")][0]
check("S28-derived Ir ZA mass share vs S30 printed 0.003 percent (independent derivation from period sums; S30 is rounded)", abs(ir_mass_share - 3e-5) / 3e-5 < 0.25, f"derived {ir_mass_share*100:.5f} percent")
check("S30 revenue shares ZA sum (PGM_sum 0.872 + Cu .0155 + Ni .1125 = 1)", abs(0.872 + 0.0155 + 0.1125 - 1) < 1e-3)

# ---------------------------------------------------------------- levers
sec("A6 LEVER FACTORS: factor by which one input must change for Delta_eta_be to reach 30 mV (central, supply-mix row, lambda = 0, g_high, R_rec = 0.9); others fixed")
def lever_block(el, ld, nm="mix", gc="g_high"):
    cx0 = row_cexc(el, nm)
    base = dbe(el, ld, cx0, gc)[0]
    f_cexc = brentq(lambda f: dbe(el, ld, cx0 * f, gc)[0] - 0.03, 1, 1e4)
    f_load = brentq(lambda f: dbe(el, ld * f, cx0, gc)[0] - 0.03, 1, 1e4)
    f_jt = base / 0.03       # exact: delta_eta ~ 1/(j tau)
    # lambda: b_infra needed
    m = C.mg_cm2_to_kg_m2(ld)
    s = C.side_s(el, m, cx0, C.SCEN["R_rec_central"]); g = C.side_g(gc)
    need = 0.03 * (C.J_CENTRAL * 1e4) * (C.TAU_CENTRAL_H * 3600) / T0 - (s["init"] + s["eol"] - g["init"] - g["eol"])   # J/K per m2 of lambda
    b_need = need * T0 / m
    # R_rec lever
    dR = [dbe(el, ld, cx0, gc, R=R)[0] * 1e3 for R in (0, 0.5, 0.9, 0.95, 1.0)]
    # kappa
    f_k = f_cexc / 1.0
    print(f"{el} {ld} mg/cm2 ({nm}): base {mv(base):.4f} mV")
    print(f"    CExC: x{f_cexc:.1f} (kappa would need to be {KAPPA*f_k:.1f} instead of {KAPPA}); loading: x{f_load:.1f} ({ld*f_load:.1f} mg/cm2); j*tau: divided by {1/f_jt:.1f} (j*tau = {C.J_CENTRAL*C.TAU_CENTRAL_H*f_jt:.3g} A h/cm2 instead of {C.J_CENTRAL*C.TAU_CENTRAL_H:.3g}; i.e. {C.TAU_CENTRAL_H*f_jt:.3g} h at 1 A/cm2)")
    print(f"    lambda: b_infra needed {b_need:.4g} J/kg = {b_need/1e6:.4g} MJ/kg = {b_need/cx0:.1f} x CExC (mid estimate is {rho_infra(1):.3f} x, hi {rho_infra(2):.3f} x); factor on the mid estimate x{b_need/(rho_infra(1)*cx0):.0f}")
    print(f"    R_rec 0, 0.5, 0.9, 0.95, 1.0 -> {', '.join(f'{x:.4f}' for x in dR)} mV: R_rec cannot reach 30 mV (the remelt term is at most {C.SCEN['wremelt_ratio_Pt']*100:.1f} percent of CExC by the proxy; see Not settled)")
    return b_need, base
bn = {}
for el, ld in (("Ir", 2.0), ("Ir", 1.0), ("Ir", 0.2), ("Pt", 0.5), ("Pt", 0.1)):
    bn[(el, ld)] = lever_block(el, ld)
print("\n  Sweep over the CExC multiplier f (central Pt 0.5 and Ir 2 mg/cm2, lambda = 0, g_high): where Delta_eta_be crosses 10 and 30 mV")
for el, ld in (("Pt", 0.5), ("Ir", 2.0)):
    cx0 = row_cexc(el, "mix")
    f10 = brentq(lambda f: dbe(el, ld, cx0 * f, "g_high")[0] - 0.01, 1, 1e5)
    f30 = brentq(lambda f: dbe(el, ld, cx0 * f, "g_high")[0] - 0.03, 1, 1e5)
    print(f"    {el} {ld}: 10 mV at f = {f10:.1f}, 30 mV at f = {f30:.1f}; kappa sweep 0.8..1.5 -> {mv(dbe(el, ld, 0.8/KAPPA*cx0, 'g_high')[0]):.4f} .. {mv(dbe(el, ld, 1.5/KAPPA*cx0, 'g_high')[0]):.4f} mV")
check("30 mV lever solutions reproduce 30 mV (TRUE BY CONSTRUCTION of the root finder, not a physical check)",
      abs(dbe("Pt", 0.5, row_cexc("Pt", "mix") * brentq(lambda f: dbe("Pt", 0.5, row_cexc("Pt", "mix") * f, "g_high")[0] - 0.03, 1, 1e4), "g_high")[0] - 0.03) < 1e-9)

# ---------------------------------------------------------------- diagnostics
sec("A7 DIAGNOSTICS")
print("(a) r_el = 2.5 on the operating term (OQ-15), diagnostic only: Delta_eta_be / 2.5 (central, supply-mix row, lambda = 0, g_high):")
for el, ld in C.LOADINGS:
    cx = row_cexc(el, "mix")
    d1 = dbe(el, ld, cx, "g_high")[0]; d25 = dbe(el, ld, cx, "g_high", r_el=2.5)[0]
    d1l = dbe(el, ld, cx, "g_low")[0]; d25l = dbe(el, ld, cx, "g_low", r_el=2.5)[0]
    print(f"    {el} {ld:4.1f}: r_el=1 {mv(d1):.4f} ({C.classify(d1)}) -> r_el=2.5 {mv(d25):.4f} ({C.classify(d25)})   [g_low: {mv(d1l):.4f} -> {mv(d25l):.4f} ({C.classify(d25l)})]")
print("    r_el = 2.5 moves every central value down by 2.5; the classes do not move toward 'priced'.")
print("\n(b) Exergy replacement cost, NOT A GMS-100 TERM: CExC replaced by CExC + ERC (Pt ERC 4491688 MJ/kg, LOOKUP; Ni, Fe ERC LOOKUP; Ir: no readable value, not computed)")
print(f"{'x':3s} {'mg/cm2':>6s} | {'GMS-100 (mV)':>12s} | {'+ERC (mV)':>10s} {'class':>12s} | {'+ERC j=.5 8e4h':>14s} | {'+ERC j=.2 2e4h':>14s} {'class':>10s}")
for el, ld in (("Pt", 0.1), ("Pt", 0.5)):
    cx = row_cexc(el, "mix")
    d0_ = dbe(el, ld, cx, "g_high")[0]
    erc = C.THANATIA["Pt"]["ERC_MJ_per_kg"]
    d1_ = dbe(el, ld, cx, "g_high", erc_s=erc, erc_g=True)[0]
    d2_ = dbe(el, ld, cx, "g_high", j=0.5, tau=8e4, erc_s=erc, erc_g=True)[0]
    d3_ = dbe(el, ld, cx, "g_high", j=0.2, tau=2e4, erc_s=erc, erc_g=True)[0]
    print(f"{el:3s} {ld:6.1f} | {mv(d0_):12.4f} | {mv(d1_):10.4f} {C.classify(d1_):>12s} | {mv(d2_):14.4f} | {mv(d3_):14.4f} {C.classify(d3_):>10s}")
print("    ERC/CED of the Pt supply-mix row = %.1f; ERC/(M&M of Pt) = %.1f. With an ERC term Pt stays 'nearly free' at the central case (8.2 mV at 0.5 mg/cm2, just under 10), is 'between' at the G2.6 point for 0.5 mg/cm2 (16 mV) and 'priced' at the low-duty corner." % (C.THANATIA["Pt"]["ERC_MJ_per_kg"] / C.CED[("Pt", "TOTAL (supply mix)")], C.THANATIA["Pt"]["ERC_MJ_per_kg"] / C.THANATIA_PT_MM))
print("    (the ERC is also added to Ni and Fe on side g, which lowers the value slightly). Ir ERC: not readable in any source reached; not estimated.")

print("\n(c) Omitted side-s stages (synthesis, ink, coating): OUTSIDE GMS-100's BOUNDARY. No source bound found. Illustration: omitted stages = omega x extraction work (omega MEMORY UNSURE, 0.5 and 1.0), lambda = 0, g_high:")
for el, ld in C.LOADINGS:
    cx = row_cexc(el, "mix")
    v = [mv(dbe(el, ld, cx, "g_high", omit=o)[0]) for o in (0, 0.5, 1.0)]
    print(f"    {el} {ld:4.1f}: {v[0]:.4f} / {v[1]:.4f} / {v[2]:.4f} mV ({C.classify(v[2]/1e3)} at omega=1)")
print("    Omitting these stages lowers Delta_eta_be; the stated value is a lower bound under GMS-100's boundary. A multiplier of 1 does not change any class.")

print("\n(d) b_ch share of CExC (condition 2 of REQ-LIFECYCLE-CEXC-SOURCE not met: b_ch is Szargut's, CExC is a CED stand-in):")
for el in ("Pt", "Ir", "Ni", "Fe"):
    key = (el, "TOTAL (supply mix)") if el != "Fe" else (el, "TOTAL (pig iron)")
    print(f"    {el}: b_ch = {C.bch_kg(el)/1e6:.3f} MJ/kg, CED = {C.CED[key]/1e6:.1f} MJ/kg, share {C.bch_kg(el)/C.CED[key]*100:.4g} percent")
print("    Dispersal at low R_rec on side s adds only b_ch(x) (not CExC): Pt %.2f MJ per kg (= %.0f J/K per m2 at 0.5 mg/cm2 and R_rec=0), Ir %.2f MJ per kg (= %.0f J/K per m2 at 2 mg/cm2)." % (
        C.bch_kg("Pt")/1e6, C.mg_cm2_to_kg_m2(0.5)*C.bch_kg("Pt")/T0, C.bch_kg("Ir")/1e6, C.mg_cm2_to_kg_m2(2.0)*C.bch_kg("Ir")/T0))
print("    Versus the extraction term this is a factor of ~%.0e smaller." % (C.bch_kg("Pt") / C.CED[("Pt", "TOTAL (supply mix)")]))

print("\n(e) R_rec set (supply-mix row, central duty, lambda = 0, g_high), mV:")
for el, ld in C.LOADINGS:
    cx = row_cexc(el, "mix")
    print("    %s %4.1f: " % (el, ld) + "  ".join(f"R={R}: {mv(dbe(el, ld, cx, 'g_high', R=R)[0]):.4f}" for R in C.R_REC_SET))
print("    With the proxy, w_lost,remelt is 4.9 percent of CExC, so R_rec raises Delta_eta_be by at most ~5 percent (a remelt cost on side s is a credit for the candidate). UNSURE: if remelt of CCM catalyst is ten times the proxy the effect is 50 percent.")

# ---------------------------------------------------------------- consistency checks
sec("A8 CHECKS")
check("REQ-LIFECYCLE-EXTRACTION-WORK-NONNEGATIVE: CExC >= b_ch for Pt, Ir, Ni, Fe (stand-in values; not an identity but trivially satisfied: b_ch/CED <= 1e-4 for Pt, Ir)",
      all(KAPPA * C.CED[(el, "TOTAL (supply mix)" if el != "Fe" else "TOTAL (pig iron)")] >= C.bch_kg(el) for el in ("Pt", "Ir", "Ni", "Fe")))
check("Thanatia Pt M&M cost vs Nuss CED supply mix within 25 percent (independent sources, different method; ratio printed)",
      abs(C.THANATIA_PT_MM / C.CED[("Pt", "TOTAL (supply mix)")] - 1) < 0.25, f"ratio {C.THANATIA_PT_MM/C.CED[('Pt','TOTAL (supply mix)')]:.3f}")
check("Thanatia Ni M&M cost (115.5 MJ/kg) vs Nuss Ni CED total (111) within 10 percent", abs(C.THANATIA["Ni"]["MM_total_MJ_per_kg"] / C.CED[("Ni", "TOTAL (supply mix)")] - 1) < 0.10,
      f"ratio {C.THANATIA['Ni']['MM_total_MJ_per_kg']/C.CED[('Ni','TOTAL (supply mix)')]:.3f}")
check("Szargut 2005 b_ch of Ni vs Szargut 2007 table (MIT appendix, 232.7 kJ/mol) within 0.1 percent", abs(C.BCH_MOL["Ni"] / 1e3 / 232.7 - 1) < 1e-3)
check("Szargut 2005 b_ch of Fe vs Szargut 2007 table (MIT appendix, 374.3 kJ/mol) within 1 percent (editions differ: 376.99 vs 374.3)", abs(C.BCH_MOL["Fe"] / 1e3 / 374.3 - 1) < 0.01,
      f"ratio {C.BCH_MOL['Fe']/1e3/374.3:.4f}")
# terms-in-J/K consistency: delta_eta from J/K terms vs direct J/m2
el, ld = "Pt", 0.5
cx = row_cexc(el, "mix"); m = C.mg_cm2_to_kg_m2(ld)
d, s, g = dbe(el, ld, cx, "g_high")
direct = (m * (cx - C.bch_kg(el)) + m * C.SCEN["b_transport"] + (m * 0.9 * C.w_remelt_kg(el, cx) + m * 0.1 * C.bch_kg(el)) - (g["init"] + g["eol"]) * T0) / (1e4 * 8e4 * 3600)
check("Delta_eta_be from J/K terms equals direct J/m2 form (SAME FORMULA REWRITTEN: true by construction, not counted as a pass)", abs(d - direct) < 1e-15)
check("g-side per-element masses sum to loading (BY CONSTRUCTION)", abs(C.SCEN["ni_mass_frac"] + C.SCEN["fe_mass_frac"] - 1) < 1e-15)

sec("A9 CENTRAL-CASE SUMMARY (R_rec = 0.9, j = 1 A/cm2, tau = 8e4 h, r_el = 1): range over rows and g cases, lambda = 0")
for el, ld in C.LOADINGS:
    vv = []
    for nm in ["mix", "ZA", "RU"]:
        for gc in ("g_high", "g_low"):
            vv.append(mv(dbe(el, ld, row_cexc(el, nm), gc)[0]))
    vl = []
    for nm in ["mix", "ZA", "RU"]:
        for gc, lam in (("g_high", 1), ("g_low", 2)):
            vl.append(mv(dbe(el, ld, row_cexc(el, nm), gc, lam_idx=lam)[0]))
    print(f"  {el} {ld:4.1f} mg/cm2: lambda=0: {min(vv):.3f} to {max(vv):.3f} mV ({C.classify(min(vv)/1e3)} / {C.classify(max(vv)/1e3)});  with lambda (mid..hi): {min(vl):.3f} to {max(vl):.3f} mV ({C.classify(min(vl)/1e3)} / {C.classify(max(vl)/1e3)})")
print("\nOVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
