#!/usr/bin/env python3
"""OQ-22 review, script rv01: independent re-derivation of the answer's central set, and the regimes the answer did not test.

Level: derived (unverified). Written by the opus reviewer, 2026-11-15. Does NOT import the answer's scripts or read its CSVs;
every LOOKUP value is typed in here from the raw source text, with its location.

Method (independent of the answer's rearranged formula): each side's lifecycle irreversibility is built from GMS-100's terms in MOLAR
form (n in mol per m2, CExC and b_ch in J/mol), then f(tau) = Sigma_g(tau) - Sigma_s(tau) - lambda (EQ-LIFECYCLE-PARITY-FUNCTION)
is evaluated with Sigma_dot_g - Sigma_dot_s = j*d_eta/T0, and d_eta_be is found as the root of f in d_eta by bisection
(not by the closed form). The closed form is printed beside it as a second route.

Inputs
  LOOKUP  CED [MJ/kg], Nuss and Eckelman 2014 SI S1 Table S38 (answer's raw/nuss/s1.txt lines 7512-7620, read by the reviewer):
          Ir ZA 165000, Ir RU 175000, Ir TOTAL 169000; Pt ZA 308000, Pt RU 327000, Pt secondary 11900, Pt TOTAL 243000.
          Price column of the same rows: Ir 15,919.87 $/kg, Pt 43,627.17 $/kg (2006-2010 averages used for the revenue allocation).
  LOOKUP  Ni TOTAL 111, Fe TOTAL (pig iron) 23.1 MJ/kg (same table; taken from the answer's CSV header note, not re-read: UNSURE).
  LOOKUP  b_ch Szargut 2005 [kJ/mol]: Pt 140.97, Ir 256.56, Ni 232.71, Fe 376.99 (Exergoecology Portal table, as the answer).
  LOOKUP  Thanatia Table 1 of IntechOpen ch. 62189 (answer's raw/intechopen/c.txt, reviewer grep): ERC / M&M [GJ/t]:
          Platinum 4,491,688 / 291,667; Palladium 8,983,377 / 583,333; 'PGM (average value for all PGM)' 2,695,013 / 175,000. No Ir row.
  SNIPPET (web search 2026-11-15, UNSURE): Ir price 2024 average 4762 $/oz (JM base prices via a secondary site); Aug-Oct 2026
          7850-8200 $/oz (JM). Alkaline OER eta_10: NiFe LDH 247-270 mV vs IrOx/IrO2 281-318 mV (two papers). AEM cell 1.61-1.90 V at
          1 A/cm2 in KOH, 2.72 V in pure water (round robin); PEM best 1.56 V at 1 A/cm2 (90 C). Voltage drift: PEM 1.5-35 uV/h;
          NiFe AEM 0.7-84 uV/h.
  MEMORY (UNSURE) molar masses (standard atomic weights); side-g cases (copied as declared by the answer so the numbers compare);
          renewable duty scenarios; Ni PTL areal mass; basket revenue factor r.
Run: <gms-local>/.venv/bin/python -I local_docs/fable_runs/oq_22_review_code/rv01_independent_check.py
"""
import math

T0 = 298.15
HOUR = 3600.0
M = {"Pt": 0.195084, "Ir": 0.192217, "Ni": 0.058693, "Fe": 0.055845}          # kg/mol, MEMORY (standard values)
BCH = {"Pt": 140.97e3, "Ir": 256.56e3, "Ni": 232.71e3, "Fe": 376.99e3}        # J/mol, LOOKUP Szargut 2005
CED = {("Pt", "mix"): 243000e6, ("Pt", "ZA"): 308000e6, ("Pt", "RU"): 327000e6, ("Pt", "sec"): 11900e6,
       ("Ir", "mix"): 169000e6, ("Ir", "ZA"): 165000e6, ("Ir", "RU"): 175000e6,
       ("Ni", "mix"): 111e6, ("Fe", "mix"): 23.1e6}                              # J/kg, LOOKUP Table S38
ERC = {"Pt": 4491688e6, "Pd": 8983377e6, "PGMavg": 2695013e6}                  # J/kg, LOOKUP IntechOpen Table 1
PRICE_0610 = {"Ir": 15919.87, "Pt": 43627.17}                                  # $/kg, LOOKUP Table S38 price column
OZ = 0.0311034768                                                              # kg per troy ounce (definition)
B_TR = 1.0e6                                                                    # J/kg (the answer's scenario value, inside the spec range)
WREM = 11900.0 / 243000.0                                                       # answer's remelt proxy ratio, copied to compare
NI_FRAC = 3 * M["Ni"] / (3 * M["Ni"] + M["Fe"])
G = {"g_low": dict(L=0.01, psi=1.0, Bmfg=0.0), "g_high": dict(L=0.05, psi=3.0, Bmfg=50e6)}
LOADS = [("Ir", 0.2), ("Ir", 1.0), ("Ir", 2.0), ("Pt", 0.1), ("Pt", 0.5)]
RHO = {"lo": 0.008466, "mid": 0.08456, "hi": 0.2902}                           # answer's b_infra/CExC (oq22_part_b.txt line 78), copied


def kgm2(mg_cm2):
    return mg_cm2 * 1e-2


def side_s_profile(el, mg, ced_kg, R=0.9, kappa=1.0, extra_kg=0.0, wrem_ratio=WREM):
    """GMS-100 molar form. Returns (Sigma_s,init, Sigma_s,EOL) in J/K per m2."""
    m = kgm2(mg)
    n = m / M[el]                                    # mol/m2
    cexc = (kappa * ced_kg + extra_kg) * M[el]       # J/mol
    bch = BCH[el]
    w_rem = wrem_ratio * kappa * ced_kg * M[el]      # J/mol
    s_init = (n * (cexc - bch) + m * B_TR) / T0      # EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL (M_s = catalyst mass)
    s_eol = n / T0 * (R * w_rem + (1 - R) * bch)     # EQ-LIFECYCLE-INCUMBENT-EOL
    return s_init, s_eol


def side_g_profile(case, kappa=1.0, extra=None):
    c = G[case]
    num = 0.0
    eol = 0.0
    for el, frac in (("Ni", NI_FRAC), ("Fe", 1 - NI_FRAC)):
        n = c["L"] * frac / M[el]
        cexc = (kappa * CED[(el, "mix")] + (extra or {}).get(el, 0.0)) * M[el]
        num += n * c["psi"] * (cexc - BCH[el])       # w_lost,prec = psi * w_lost,ext (psi >= 1 keeps extraction inside)
        eol += n * BCH[el]                           # EQ-LIFECYCLE-GEOMETRY-EOL, R_rec = 0
    Mg = c["L"] / 0.6
    init = (num + Mg * B_TR) / T0 + c["Bmfg"] / T0   # EQ-LIFECYCLE-GEOMETRY-INITIAL-CAPITAL, tooling = computation = 0
    return init, eol / T0


def f_parity(d_eta, j_Acm2, tau_h, s, g, lam):
    """EQ-LIFECYCLE-PARITY-FUNCTION with EQ-LIFECYCLE-SIDE-IRREVERSIBILITY (tau_wearout = inf, K_ox = 0). Sigma_dot_s := 0 reference."""
    j = j_Acm2 * 1e4
    tau = tau_h * HOUR
    Sg = g[0] + (j * d_eta / T0) * tau + g[1]
    Ss = s[0] + 0.0 * tau + s[1]
    return Sg - Ss - lam


def root_deta(j, tau_h, s, g, lam):
    lo, hi = -1.0, 1.0
    flo, fhi = f_parity(lo, j, tau_h, s, g, lam), f_parity(hi, j, tau_h, s, g, lam)
    assert flo < 0 < fhi
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f_parity(mid, j, tau_h, s, g, lam) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def closed(j, tau_h, s, g, lam):
    return T0 * (s[0] + s[1] + lam - g[0] - g[1]) / (j * 1e4 * tau_h * HOUR)


def dbe(el, mg, row="mix", gc="g_high", j=1.0, tau=8e4, R=0.9, lam_key=None, kappa=1.0, extra_kg=0.0, lam_scale=1.0, ced=None):
    ced_kg = CED[(el, row)] if ced is None else ced
    s = side_s_profile(el, mg, ced_kg, R=R, kappa=kappa, extra_kg=extra_kg)
    g = side_g_profile(gc, kappa=kappa)
    lam = 0.0 if lam_key is None else RHO[lam_key] * kappa * ced_kg * kgm2(mg) / T0 * lam_scale
    return root_deta(j, tau, s, g, lam), s, g, lam


def cls(mv):
    return "nearly free" if mv < 10 else ("priced" if mv > 30 else "between")


def sec(t):
    print("\n" + "=" * 96 + "\n" + t + "\n" + "=" * 96)


mv = lambda v: v * 1e3

# ------------------------------------------------------------------------------------------------ R1
sec("R1 DERIVATION CHECK: root of f(tau) in d_eta (bisection) vs closed form; sign of f just below / above the root")
for el, mg in LOADS:
    d, s, g, lam = dbe(el, mg)
    c = closed(1.0, 8e4, s, g, lam)
    fm = f_parity(d - 1e-4, 1.0, 8e4, s, g, lam)
    fp = f_parity(d + 1e-4, 1.0, 8e4, s, g, lam)
    print(f"  {el} {mg:3.1f}: root {mv(d):.4f} mV, closed {mv(c):.4f} mV, |diff| {abs(d-c):.1e} V; f(root-0.1mV) {fm:+.3e} (<0: candidate wins), f(root+0.1mV) {fp:+.3e}")
print("  units: n [mol/m2] x (CExC - b_ch) [J/mol] / T0 [K] = J/(K m2);  j [A/m2] x d_eta [V] x tau [s] / T0 = J/(K m2). Consistent.")

sec("R2 REPRODUCTION of the answer's central set (j = 1 A/cm2, tau = 8e4 h, R_rec = 0.9), reviewer's own code")
ANS = {  # answer's oq22_part_a.txt A3, lam=0 g_high / lam=0 g_low / lam_mid g_high / lam_hi g_low, copied for comparison
    ("Ir", 0.2, "mix"): (0.1006, 0.1222, 0.1105, 0.1563), ("Ir", 1.0, "mix"): (0.5908, 0.6124, 0.6404, 0.7827),
    ("Ir", 2.0, "mix"): (1.2034, 1.2250, 1.3027, 1.5656), ("Pt", 0.1, "mix"): (0.0662, 0.0878, 0.0733, 0.1123),
    ("Pt", 0.5, "mix"): (0.4186, 0.4402, 0.4542, 0.5626), ("Ir", 2.0, "RU"): (1.2469, 1.2685, 1.3497, 1.6212),
    ("Pt", 0.5, "RU"): (0.5708, 0.5924, 0.6188, 0.7572)}
worst = 0.0
for (el, mg, row), a in ANS.items():
    mine = [mv(dbe(el, mg, row, gc, lam_key=lk)[0]) for gc, lk in (("g_high", None), ("g_low", None), ("g_high", "mid"), ("g_low", "hi"))]
    dev = max(abs(x - y) for x, y in zip(mine, a))
    worst = max(worst, dev)
    print(f"  {el} {mg:3.1f} {row:3s}: reviewer " + " / ".join(f"{x:.4f}" for x in mine) + f"   answer " + " / ".join(f"{x:.4f}" for x in a) + f"   max |dev| {dev:.4f} mV")
print(f"  largest deviation over the rows compared: {worst:.4f} mV (answer printed 4 decimals)")
print("  Note: the reproduction uses the answer's own scenario inputs (side g, b_transport, remelt proxy, rho); it checks arithmetic and term")
print("  assembly, not the inputs.")

sec("R3 TEXT-vs-OUTPUT checks the answer's prose depends on")
for el, mg in LOADS:
    s = side_s_profile(el, mg, CED[(el, "mix")])
    tr = kgm2(mg) * B_TR / T0
    print(f"  transport term {el} {mg:3.1f}: {tr:.3g} J/K per m2, share of Sigma_s,init {tr/s[0]:.2e}")
for el, mg in (("Ir", 2.0), ("Pt", 0.1)):
    d = dbe(el, mg)[0]
    print(f"  j*tau lever {el} {mg}: base {mv(d):.4f} mV -> j*tau must fall by x{0.03/d:.1f} for 30 mV (Delta_eta_be ~ 1/(j tau) exactly)")

# ------------------------------------------------------------------------------------------------ allocation sign
sec("R4 MASS ALLOCATION (answer A5 'mass_all'): sign and meaning of a negative d_eta_be")
for el, mg, ced_mass in (("Ir", 2.0, 969.8e6), ("Ir", 0.2, 969.8e6), ("Ir", 2.0, 110.2e6)):
    for gc in ("g_high", "g_low"):
        d, s, g, lam = dbe(el, mg, gc=gc, ced=ced_mass)
        f0 = f_parity(0.0, 1.0, 8e4, s, g, lam)
        who = "candidate wins" if f0 < 0 else "INCUMBENT wins (f > 0)"
        print(f"  {el} {mg} CED {ced_mass/1e6:6.1f} MJ/kg {gc}: d_eta_be {mv(d):+.4f} mV; f at d_eta = 0: {f0:+.4g} J/K per m2 -> {who}")
print("  A negative d_eta_be means the candidate must be MORE active than the incumbent to win; at zero penalty the incumbent wins.")

# ------------------------------------------------------------------------------------------------ dispersal
sec("R5 WHAT GMS-100 CHARGES FOR DISPERSING 1 kg (R_rec = 0, horizon unit): b_ch per kg, against CED and ERC")
for el in ("Pt", "Ir", "Ni", "Fe"):
    print(f"  {el}: b_ch {BCH[el]/M[el]/1e6:7.3f} MJ/kg; CED {CED[(el,'mix')]/1e6:10.1f} MJ/kg" + (f"; ERC {ERC[el]/1e6:.0f} MJ/kg" if el in ERC else ""))
print(f"  ratio b_ch(Fe)/b_ch(Pt) per kg = {(BCH['Fe']/M['Fe'])/(BCH['Pt']/M['Pt']):.2f}: dispersing a kg of Fe costs more in GMS-100 than a kg of Pt.")

# ------------------------------------------------------------------------------------------------ regimes
sec("R6 THROUGHPUT (duty) REGIME: d_eta_be is exactly proportional to 1/(j tau). Throughput Q = j*tau in A h/cm2")
Q0 = 1.0 * 8e4
for el, mg in LOADS:
    d0 = dbe(el, mg)[0]
    dhi = dbe(el, mg, gc="g_low", lam_key="hi")[0]
    print(f"  {el} {mg:3.1f}: central {mv(d0):.4f} mV; Q for 10 mV {Q0*mv(d0)/10:8.0f}, for 30 mV {Q0*mv(d0)/30:8.0f} A h/cm2"
          f"   [lam_hi,g_low: 10 mV at {Q0*mv(dhi)/10:7.0f}, 30 mV at {Q0*mv(dhi)/30:7.0f}]")
print("  Renewable-coupled scenarios (MEMORY, UNSURE): Q = j_avg x CF x 8760 h x years of stack life")
SCN = [("grid baseload (central)", 1.0, 0.913, 10.0), ("wind+PV hybrid", 1.0, 0.45, 10.0), ("PV only, long life", 1.0, 0.22, 10.0),
       ("PV only, part load, 7 y", 0.5, 0.20, 7.0), ("off-grid PV, start-stop limited, 5 y", 0.5, 0.15, 5.0)]
for nm, j, cf, yr in SCN:
    Q = j * cf * 8760 * yr
    row = []
    for el, mg in LOADS:
        d = dbe(el, mg, j=j, tau=cf * 8760 * yr)[0]
        row.append(f"{el}{mg}: {mv(d):6.2f} {cls(mv(d))[:7]}")
    print(f"  {nm:38s} Q = {Q:7.0f} A h/cm2 | " + " | ".join(row))

sec("R7 REPLACEMENT REGIMES (horizon H = 8e4 h at 1 A/cm2)")
print("  (a) incumbent replaced every L h, GMS-100 Open-item form R_s = M_s b_tr/T0 + Sigma_s,EOL^ret (EQ-LIFECYCLE-RETIRED-UNIT-EOL, k = s);")
print("      NOT evaluable in GMS-100 0.1 (m_s = 0 always; f >= 0 with tau_wearout,s < tau gives 'no outcome'). Shown as a diagnostic.")
for el, mg in (("Ir", 2.0), ("Pt", 0.5)):
    for R in (0.0, 0.5, 0.9):
        out = []
        for L in (8e4, 4e4, 2e4, 1e4):
            m_s = max(0, math.ceil(8e4 / L) - 1)
            m = kgm2(mg)
            n = m / M[el]
            cexc = CED[(el, "mix")] * M[el]
            s0, se = side_s_profile(el, mg, CED[(el, "mix")], R=R)
            Rs = m * B_TR / T0 + n / T0 * (R * WREM * cexc + (1 - R) * cexc)
            g = side_g_profile("g_high")
            d = T0 * (s0 + se + m_s * Rs - g[0] - g[1]) / (1e4 * 8e4 * HOUR)
            out.append(f"L={L:.0e}: {mv(d):6.3f}")
        print(f"      {el} {mg} R_rec={R}: " + "  ".join(out) + " mV")
print("  (b) candidate (NiFe, g_high) replaced every L_g h (EQ-LIFECYCLE-GEOMETRY-REPLACEMENT-COST; w_conv = (psi-1) w_ext; R_rec = 0 -> CExC):")
for el, mg in (("Ir", 0.2), ("Ir", 2.0), ("Pt", 0.1), ("Pt", 0.5)):
    out = []
    for Lg in (8e4, 2e4, 1e4, 5e3):
        mg_ = max(0, math.ceil(8e4 / Lg) - 1)
        c = G["g_high"]
        Rg = 0.0
        for e2, fr in (("Ni", NI_FRAC), ("Fe", 1 - NI_FRAC)):
            n = c["L"] * fr / M[e2]
            cexc = CED[(e2, "mix")] * M[e2]
            wext = cexc - BCH[e2]
            Rg += n * ((c["psi"] - 1) * wext + cexc)
        Rg = Rg / T0 + (c["L"] / 0.6) * B_TR / T0 + c["Bmfg"] / T0
        s0, se = side_s_profile(el, mg, CED[(el, "mix")])
        g0, ge = side_g_profile("g_high")
        d = T0 * (s0 + se - g0 - ge - mg_ * Rg) / (1e4 * 8e4 * HOUR)
        out.append(f"L_g={Lg:.0e}: {mv(d):+7.3f}")
    print(f"      {el} {mg}: " + "  ".join(out) + " mV")

sec("R8 CELL-LEVEL AND ACTIVITY REGIMES: the d_eta the comparison actually faces (SNIPPET values, UNSURE)")
maxbe = max(mv(dbe(el, mg, row=r, gc="g_low", lam_key="hi")[0]) for el, mg in LOADS for r in (("mix", "ZA", "RU")))
print(f"  largest d_eta_be of the central set (any row, lam_hi, g_low): {maxbe:.3f} mV")
cases = [("alkaline half-cell, NiFe LDH vs IrOx (247 vs 281 mV at 10 mA/cm2)", 247 - 281),
         ("alkaline half-cell, NiFe LDH vs IrO2 (270 vs 318 mV)", 270 - 318),
         ("cell: AEM NiFe2O4 in KOH 1.61 V vs best PEM 1.56 V (1 A/cm2)", 1610 - 1560),
         ("cell: AEM NiFe-LDH/NiMo 1.90 V vs best PEM 1.56 V", 1900 - 1560),
         ("cell: AEM pure water round robin 2.72 V vs best PEM 1.56 V", 2720 - 1560)]
for nm, d in cases:
    verdict = "moot: candidate wins on Sigma_dot alone" if d <= 0 else f"d_eta / d_eta_be(max) = {d/maxbe:.0f}: decided by Sigma_dot"
    print(f"  {nm:66s} d_eta = {d:+5d} mV -> {verdict}")
print("  Cell-level material change (PEM -> AEM) on side g, e.g. a Ni porous transport layer of 0.35 kg/m2 (MEMORY, UNSURE), psi = 1:")
nPTL = 0.35 / M["Ni"]
dPTL = (nPTL * (CED[("Ni", "mix")] * M["Ni"] - BCH["Ni"]) + 0.35 * B_TR) / (1e4 * 8e4 * HOUR)
print(f"    lowers d_eta_be by {mv(dPTL):.4f} mV at the central duty")

sec("R9 DRIFT (incumbent or candidate loss rising with age): drift-rate difference that equals d_eta_be")
print("  If d_eta(t) = d_eta0 + dr*t, the time-average over tau is d_eta0 + dr*tau/2; with d_eta0 = 0 the break-even drift is dr_be = 2 d_eta_be / tau.")
for el, mg in LOADS:
    d = dbe(el, mg)[0]
    dmax = dbe(el, mg, row="RU", gc="g_low", lam_key="hi")[0]
    print(f"  {el} {mg:3.1f}: dr_be = {2*d/8e4*1e6:.4f} uV/h (central), {2*dmax/8e4*1e6:.4f} uV/h (largest row)")
print("  Reported drift (SNIPPET, UNSURE): PEM 1.5-35 uV/h; NiFe AEM 0.7-84 uV/h. A drift DIFFERENCE of 0.03 uV/h equals the whole")
print("  material term of Ir 2 mg/cm2; GMS-100's profile cannot represent a rising rate (Open items), and a constant-rate fit absorbs it into Sigma_dot.")

sec("R10 CExC WELL ABOVE CED, and scarcity terms (central duty, lam = 0, g_high)")
for el, mg in LOADS:
    out = []
    for k in (1.0, 2.0, 3.0, 5.0):
        out.append(f"kappa={k:.0f}: {mv(dbe(el, mg, kappa=k)[0]):6.3f}")
    kneed = 10.0 / mv(dbe(el, mg)[0])
    print(f"  {el} {mg:3.1f}: " + "  ".join(out) + f" mV; kappa for 10 mV ~ {kneed:.1f} (side g held fixed)")
print("  ERC added (NOT a GMS-100 term). Ir has no ERC row; the 'PGM average' row of the same table is used as a labelled proxy (UNSURE):")
for el, mg, key in (("Pt", 0.1, "Pt"), ("Pt", 0.5, "Pt"), ("Ir", 0.2, "PGMavg"), ("Ir", 1.0, "PGMavg"), ("Ir", 2.0, "PGMavg")):
    out = []
    for j, tau in ((1.0, 8e4), (0.5, 8e4), (0.2, 2e4)):
        d = mv(dbe(el, mg, j=j, tau=tau, extra_kg=ERC[key])[0])
        out.append(f"j={j} tau={tau:.0e}: {d:8.2f} {cls(d)}")
    print(f"    {el} {mg:3.1f} (+ERC {key}): " + " | ".join(out))
print("  Revenue allocation at a later price basis (Table S38 used 2006-10 prices: Ir 15,919.87 $/kg = %.0f $/oz; Pt %.0f $/oz)." % (
    PRICE_0610["Ir"] * OZ, PRICE_0610["Pt"] * OZ))
p_old = PRICE_0610["Ir"] * OZ
for label, p_new in (("2024 avg 4762 $/oz (SNIPPET)", 4762.0), ("Aug 2026 7850 $/oz (SNIPPET)", 7850.0)):
    for r in (1.3, 1.0, 0.8):
        fac = (p_new / p_old) / r
        out = []
        for mg in (0.2, 1.0, 2.0):
            d = mv(dbe("Ir", mg, ced=CED[("Ir", "mix")] * fac)[0])
            out.append(f"Ir {mg}: {d:6.2f} {cls(d)}")
        print(f"    {label}, basket revenue factor r = {r} (MEMORY): Ir CED x{fac:5.1f} -> " + " | ".join(out))
print("  (revenue allocation: per-kg burden of Ir = B_total x p_Ir / sum p_j m_j; factor = (p_new/p_old)/r; ore inventory held fixed.)")

sec("R11 SHARED LOOP: GMS-100's actual verdict for Pt and Ir is REQ-LIFECYCLE-SHARED-INFRASTRUCTURE-VERDICT (N_share < N_alloc)")
print("  f0 uses lambda = 0; f_max credits B_infra/(T0 N_share) = b_infra m''/(T0 s), s = product's share of the loop's mass throughput.")
print("  Band: candidate wins unconditionally if d_eta < d_be(f0); incumbent wins unconditionally if d_eta >= d_be(f_max); otherwise 'conditional'.")
for el, mg in (("Ir", 2.0), ("Ir", 0.2), ("Pt", 0.5), ("Pt", 0.1)):
    d0 = dbe(el, mg)[0]
    out = []
    for s_ in (1.0, 0.1, 0.01, 0.001):
        for key in ("mid", "hi"):
            dm = dbe(el, mg, lam_key=key, lam_scale=1.0 / s_)[0]
            out.append(f"s={s_:g},{key}: {mv(dm):7.2f}")
    print(f"  {el} {mg}: d_be(f0) = {mv(d0):.3f} mV; d_be(f_max): " + "  ".join(out))
for el, mg in (("Ir", 2.0), ("Pt", 0.5)):
    d0 = dbe(el, mg)[0]
    lam1 = dbe(el, mg, lam_key="mid")[0] - d0
    lamh = dbe(el, mg, lam_key="hi")[0] - d0
    print(f"  {el} {mg}: s at which d_be(f_max) = 10 mV: mid {lam1/(0.01-d0):.4f}, hi {lamh/(0.01-d0):.4f}; = 30 mV: mid {lam1/(0.03-d0):.4f}, hi {lamh/(0.03-d0):.4f}")

sec("R12 PART B: alpha under the two readings of 'fixed part'")
# answer's bracket inputs (oq22_common.py INFRA, STAGE_FIXED; oq22_part_b.txt lines 48, 65-78), copied
for nm, c, a, fop in (("lo", 0.01, 0.20, 0.1690), ("mid", 0.05, 0.45, 0.2730), ("hi", 0.30, 0.70, 0.3910)):
    op_fixed = fop * (1 - c)
    alpha_answer = (op_fixed + a * c) / (op_fixed + c)
    print(f"  {nm}: alpha (answer: fixed = fixed operating + capital) = {alpha_answer:.3f};  alpha (fixed = loop capital only, the 'establishing' part) = {a:.2f}")
print("  Prompt 8's rv03 joint verdict flips at alpha = 0.804: the first reading lies above it, the second below it, for every corner.")

sec("R13 IDENTITY CHECKS (true by construction; not counted as passes)")
print("  R1 root-vs-closed agreement is algebra of the same terms; R2 reuses the answer's scenario inputs; R12 recomputes the answer's alpha.")
