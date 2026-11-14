#!/usr/bin/env python3
"""Row N1 (claims G3.6, G3.7): thermal absorption cross sections at 2200 m/s and resonance integrals above 0.5 eV.

LOOKUP sources (see data headers):
  * thermal sigma_a (2200 m/s): Sears (1992) Table 1 via NIST NCNR, data/sears_1992_table1.csv (isotopes AND natural elements).
  * resonance integral RI = integral_{0.5 eV}^{20 MeV} sigma_abs(E)/E dE, with sigma_abs = (n,gamma) + (n,p) + (n,t) + (n,alpha)
    (MT102+103+105+107), from reconstructed POINTWISE ENDF/B-VII.1 evaluations retrieved from NNDC Sigma
    (data/raw/endf_sigma/<nuclide>_mt<MT>.txt, access 2026-11-14), integrated here by exact integration of a lin-lin pointwise table.
    Natural-element RI = sum over isotopes of (Sears natural abundance) x RI(isotope). Natural carbon is a natural-element evaluation.
  * Thermal value from the same ENDF files at 0.0253 eV is printed as a cross-check of Sears.
NOT USED (not reachable / not available as text): Mughabghab Atlas of Neutron Resonances (2006/2018), INDC(NDS)-440, ENDF/B-VIII.0 (only
VII.1 pointwise service reachable), JENDL-5. This is a deviation from the plan's first-choice sources; see outputs/issues_b.md.
Writes outputs/n1_values.csv for rows N2, N3, N5. Level `derived`.
"""
import os, re, csv, math, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "data"); RAW = os.path.join(D, "raw", "endf_sigma")
FAILS = []
def check(name, ok, detail):
    print("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok: FAILS.append(name)

# ---- Sears
SEARS = {}
for r in csv.DictReader(l for l in open(os.path.join(D, "sears_1992_table1.csv")) if not l.startswith("#")):
    SEARS[r["label"]] = (r["conc"], float(r["abs_xs_b"])) if re.match(r"^[0-9.]+$", r["abs_xs_b"].rstrip(".")) else (r["conc"], float("nan"))
def sears(label): return SEARS[label][1]
def conc(label):
    try: return float(SEARS[label][0])/100.0
    except ValueError: return float("nan")

# ---- ENDF pointwise
def load_mt(nuc, mt):
    fn = os.path.join(RAW, "%s_mt%d.txt" % (nuc, mt))
    if not os.path.exists(fn): return None
    E = []; S = []
    for ln in open(fn):
        if ln.startswith("#"): continue
        p = ln.strip().split(",")
        if len(p) != 2: continue
        try: E.append(float(p[0])); S.append(float(p[1]))
        except ValueError: continue
    E = np.array(E); S = np.array(S)
    o = np.argsort(E, kind="stable"); return E[o], S[o]
def total(nuc, mts=(102, 103, 105, 107)):
    tabs = [t for t in (load_mt(nuc, m) for m in mts) if t is not None]
    grid = np.unique(np.concatenate([t[0] for t in tabs]))
    s = np.zeros_like(grid)
    for E, S in tabs:
        s += np.interp(grid, E, S, left=0.0, right=0.0)
    return grid, s
def ri(grid, s, lo=0.5, hi=2.0e7):
    g = np.unique(np.concatenate([grid[(grid > lo) & (grid < hi)], [lo, hi]]))
    sv = np.interp(g, grid, s, left=0.0, right=0.0)
    E1, E2, s1, s2 = g[:-1], g[1:], sv[:-1], sv[1:]
    b = (s2 - s1)/(E2 - E1); a = s1 - b*E1
    return float(np.sum(a*np.log(E2/E1) + b*(E2 - E1)))
def thermal(grid, s, E=0.0253): return float(np.interp(E, grid, s))

ISO = {  # Sears label -> ENDF file name; element -> list of isotopes
 "H":  [("1H", "H-1")], "B": [("10B", "B-10"), ("11B", "B-11")],
 "Al": [("Al", "Al-27")],
 "Fe": [("54Fe", "Fe-54"), ("56Fe", "Fe-56"), ("57Fe", "Fe-57"), ("58Fe", "Fe-58")],
 "Ag": [("107Ag", "Ag-107"), ("109Ag", "Ag-109")],
 "Cd": [(m+"Cd", "Cd-"+m) for m in "106 108 110 111 112 113 114 116".split()],
 "In": [("113In", "In-113"), ("115In", "In-115")],
 "Sm": [(m+"Sm", "Sm-"+m) for m in "144 147 148 149 150 152 154".split()],
 "Eu": [("151Eu", "Eu-151"), ("153Eu", "Eu-153")],
 "Gd": [(m+"Gd", "Gd-"+m) for m in "152 154 155 156 157 158 160".split()],
 "Dy": [(m+"Dy", "Dy-"+m) for m in "156 158 160 161 162 163 164".split()],
 "Hf": [(m+"Hf", "Hf-"+m) for m in "174 176 177 178 179 180".split()],
}
print("N1: LOOKUP sources")
print("  thermal sigma_a (2200 m/s): Sears V.F. 1992 Neutron News 3(3) Table 1, NIST NCNR web copy, data/sears_1992_table1.csv, access 2026-11-14")
print("  RI and ENDF thermal: ENDF/B-VII.1 pointwise (NNDC Sigma), files in data/raw/endf_sigma/, access 2026-11-14; RI = int_{0.5 eV}^{20 MeV} sigma_abs dE/E,")
print("      sigma_abs = MT102+103+105+107. Natural elements: abundance-weighted with Sears abundances.")
ISOCACHE = {}
def iso_vals(label, f):
    g, s = total(f)
    return dict(th=thermal(g, s), ri=ri(g, s), ri100k=ri(g, s, 0.5, 1e5), ri_cap=ri(*total(f, (102,))), npts=len(g))
for el, lst in ISO.items():
    for lab, f in lst:
        ISOCACHE[lab] = iso_vals(lab, f)
ISOCACHE["Li6"] = iso_vals("6Li", "Li-6"); ISOCACHE["B10"] = ISOCACHE["10B"]; ISOCACHE["Cd113"] = ISOCACHE["113Cd"]
ISOCACHE["C"] = iso_vals("C", "C-0")
ISOCACHE["6Li"] = ISOCACHE["Li6"]
def natural(el):
    lst = ISO[el]; w = np.array([conc(l) for l, _ in lst])
    tot = {k: float(sum(wi*ISOCACHE[l][k] for wi, (l, _) in zip(w, lst))) for k in ("th", "ri", "ri100k", "ri_cap")}
    tot["wsum"] = float(w.sum()); return tot

ENTRIES = [  # name, sears label, endf values
 ("H (1H)", "H", ISOCACHE["1H"]), ("Li-6", "6Li", ISOCACHE["6Li"]), ("B-10", "10B", ISOCACHE["10B"]), ("nat B", "B", natural("B")),
 ("C (nat)", "C", ISOCACHE["C"]), ("Al", "Al", ISOCACHE["Al"]), ("nat Fe", "Fe", natural("Fe")), ("nat Ag", "Ag", natural("Ag")),
 ("Cd-113", "113Cd", ISOCACHE["113Cd"]), ("nat Cd", "Cd", natural("Cd")), ("nat In", "In", natural("In")), ("nat Sm", "Sm", natural("Sm")),
 ("nat Eu", "Eu", natural("Eu")), ("Gd-155", "155Gd", ISOCACHE["155Gd"]), ("Gd-157", "157Gd", ISOCACHE["157Gd"]), ("nat Gd", "Gd", natural("Gd")),
 ("nat Dy", "Dy", natural("Dy")), ("nat Hf", "Hf", natural("Hf")),
]
RANGE = {"B-10": (3835, 3845), "nat B": (760, 770), "C (nat)": (0.0034, 0.0039), "Al": (0.230, 0.233), "H (1H)": (0.332, 0.333),
         "Cd-113": (19900, 20700), "nat Cd": (2450, 2530), "Gd-157": (253000, 255000), "Gd-155": (60300, 61100), "nat Gd": (48800, 49700),
         "nat Hf": (104, 106), "nat In": (193, 194), "nat Ag": (63, 64), "Li-6": (938, 941), "nat Dy": (940, 1000), "nat Eu": (4500, 4600), "nat Sm": (5600, 5950)}
print("\n--- Table N1 (barn) ---")
print("%-8s %12s %12s %9s %12s %12s %12s   %s" % ("entry", "Sears 2200", "ENDF 0.0253", "ENDF/Sears", "RI abs 20MeV", "RI abs 100keV", "RI (n,g) only", "planner UNSURE range vs Sears"))
out = []
for name, lab, e in ENTRIES:
    ss = sears(lab); rng = RANGE.get(name)
    st = "n/a" if not rng else ("inside" if rng[0] <= ss <= rng[1] else "OUTSIDE [%g, %g]" % rng)
    print("%-8s %12.5g %12.5g %9.3f %12.5g %12.5g %12.5g   %s" % (name, ss, e["th"], e["th"]/ss, e["ri"], e["ri100k"], e["ri_cap"], st))
    out.append((name, lab, ss, e["th"], e["ri"], e["ri100k"], e["ri_cap"]))
print("\nAbundance sums used for natural elements (should be ~1 when every isotope was found):", {el: round(natural(el)["wsum"], 4) for el in ISO if len(ISO[el]) > 1})
print("\nThermal ENDF vs Sears (info; ENDF/B-VII.1 vs Sears 1992 are different evaluations, 5% informational band):")
for name, lab, ss, et, *_ in out:
    print("   %-8s ENDF/Sears = %.3f %s" % (name, et/ss, "" if abs(et/ss-1) < 0.05 else "  <-- differs by more than 5%"))
print("\n--- Isotopic checks (natural from isotopes, 3% tolerance) ---")
sb10, sb11 = sears("10B"), sears("11B"); nb = 0.199*sb10 + 0.801*sb11
check("nat B = 0.199*s(B-10) + small, vs Sears natural B (3%)", abs(nb/sears("B")-1) <= 0.03, "%.5g vs %.5g (%+.2f%%)" % (nb, sears("B"), 100*(nb/sears("B")-1)))
nc = 0.1222*sears("113Cd"); check("nat Cd ~ 0.1222*s(Cd-113) vs Sears natural Cd (3%)", abs(nc/sears("Cd")-1) <= 0.03, "%.5g vs %.5g (%+.2f%%)" % (nc, sears("Cd"), 100*(nc/sears("Cd")-1)))
ng = 0.148*sears("155Gd") + 0.1565*sears("157Gd"); check("nat Gd ~ 0.148*s(Gd-155)+0.1565*s(Gd-157) vs Sears natural Gd (3%)", abs(ng/sears("Gd")-1) <= 0.03, "%.5g vs %.5g (%+.2f%%)" % (ng, sears("Gd"), 100*(ng/sears("Gd")-1)))
print("  same checks with the ENDF thermal values: nat B %+.2f%%, nat Cd %+.2f%%, nat Gd %+.2f%%" % (
    100*((0.199*ISOCACHE["10B"]["th"]+0.801*ISOCACHE["11B"]["th"])/natural("B")["th"]-1),
    100*(0.1222*ISOCACHE["113Cd"]["th"]/natural("Cd")["th"]-1),
    100*((0.148*ISOCACHE["155Gd"]["th"]+0.1565*ISOCACHE["157Gd"]["th"])/natural("Gd")["th"]-1)))
print("  [note] these isotopic checks compare Sears isotopes with Sears natural values (one source, partly built from the same data); not fully independent.")
print("\n--- Ratios of thermal sigma_a (Sears) to C and to Al ---")
sC, sAl = sears("C"), sears("Al")
for name, lab, ss, *_ in out:
    print("   %-8s /C = %.4g   /Al = %.4g" % (name, ss/sC, ss/sAl))
print("  G3.7 MEMORY check: sigma(B-10)/sigma(C) = %.3g (claimed ~1e6); sigma(nat Cd)/sigma(Al) = %.3g (claimed ~1e4)" % (sears("10B")/sC, sears("Cd")/sAl))
check("B-10/C is about 1e6 (within a factor 2)", 0.5e6 <= sears("10B")/sC <= 2e6, "%.3g" % (sears("10B")/sC))
check("nat Cd/Al is about 1e4 (within a factor 2)", 0.5e4 <= sears("Cd")/sAl <= 2e4, "%.3g" % (sears("Cd")/sAl))
with open(os.path.join(HERE, "outputs", "n1_values.csv"), "w") as f:
    f.write("# generated by n1_thermal_ri.py (level derived). sigma_sears_b: Sears 1992 2200 m/s absorption; sigma_endf_b: ENDF/B-VII.1 at 0.0253 eV; ri_*: ENDF/B-VII.1 resonance integral (abs = 102+103+105+107)\n")
    f.write("entry,sears_label,sigma_sears_b,sigma_endf_b,ri_abs_20MeV_b,ri_abs_100keV_b,ri_gamma_only_20MeV_b\n")
    for r in out: f.write("%s,%s,%.6g,%.6g,%.6g,%.6g,%.6g\n" % r)
print("\nWrote outputs/n1_values.csv")
print("FAILED CHECKS:", FAILS if FAILS else "none")
