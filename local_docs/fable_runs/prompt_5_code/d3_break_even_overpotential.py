#!/usr/bin/env python3
"""D3: break-even overpotential against a scarce catalyst: d_eta_be = e_x m''_x / (j tau).
Spec row D3. Claim G2.6. Level: derived (unverified).
Sweep m'' in [1e-4,5e-2] kg/m2, e_x in [1e4,1e6] MJ/kg, j in [1e3,3e4] A/m2, tau in [3.6e6,3.6e8] s (each 21 log points).
LOOKUP: cumulative energy demand of Pt and Ir, Nuss and Eckelman 2014, SI S1 Table S38 (data/d3_cumulative_energy_demand.csv).
Bookkeeping check: 2 F V / M_H2 at V = 1.481 V must equal HHV of hydrogen 141.8 MJ/kg (39.4 kWh/kg); at 1.8 V: 47.9 kWh/kg.
(The 141.8 MJ/kg HHV was taken from the plan; not confirmed from a source in this run.)
"""
import csv, os
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
F = 96485.332; MH2 = 2.01588e-3
fails = 0
def chk(name, val, exp, tol):
    global fails
    ok = abs(val/exp-1) <= tol; fails += (not ok)
    print(f"CHECK {name}: {val:.5g} vs {exp} tol={tol*100:g}% -> {'PASS' if ok else 'FAIL'}")
rows = {}
with open(os.path.join(here, "data", "d3_cumulative_energy_demand.csv")) as f:
    for r in csv.reader(l for l in f if not l.startswith("#")):
        if r[0] == "metal": continue
        rows[(r[0], r[1])] = tuple(map(float, r[2:]))
print("LOOKUP SOURCE: Nuss and Eckelman 2014, PLoS ONE 9(7) e101298, SI S1 Table S38 column 'CED [MJ/kg]', https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0101298.s001, accessed 2026-11-14")
for k, v in rows.items(): print(f"   {k[0]} {k[1]}: CED {v[0]:.0f} MJ/kg (95%: {v[1]:.0f}-{v[2]:.0f})")
pt = rows[("Pt", "TOTAL (supply weighted)")][0]; ir = rows[("Ir", "TOTAL (supply weighted)")][0]
print(f"Pt total {pt:.0f} MJ/kg: planner UNSURE range 1e5-3e5 -> {'inside' if 1e5 <= pt <= 3e5 else 'outside'}; Ir total {ir:.0f}: 'same order' -> ratio Ir/Pt = {ir/pt:.2f}")
def be(m, e, j, tau): return e*1e6*m/(j*tau)
c = be(5e-3, 2.4e5, 5e3, 2.88e8)
print(f"central case (m''=5e-3 kg/m2, e=2.4e5 MJ/kg MEMORY, j=5e3 A/m2, tau=2.88e8 s): {c*1e3:.4f} mV (spec ~0.8)")
chk("central ~0.8 mV (exact arithmetic; plan value is rounded)", c*1e3, 0.8, 0.05)
for nm, e in (("Pt (Table S38 total)", pt), ("Ir (Table S38 total)", ir)):
    print(f"  {nm}: central case with LOOKUP e = {be(5e-3, e, 5e3, 2.88e8)*1e3:.4f} mV")
ms = np.logspace(-4, np.log10(5e-2), 21); es = np.logspace(4, 6, 21); js = np.logspace(3, np.log10(3e4), 21); ts = np.logspace(np.log10(3.6e6), np.log10(3.6e8), 21)
M, E_, J, T = np.meshgrid(ms, es, js, ts, indexing="ij")
D = be(M, E_, J, T)
print(f"sweep 21^4 points: d_eta_be from {D.min()*1e6:.3g} uV to {D.max():.3g} V; brackets 30-360 mV range: {D.min() < 0.03 and D.max() > 0.36}")
print(f"fraction with d_eta_be > 30 mV: {(D > 0.03).mean()*100:.2f}% ; > 360 mV: {(D > 0.36).mean()*100:.2f}%")
sel = D > 0.03
print("region d_eta_be > 30 mV (min / max over the region):  m'' [mg/cm2] %.3g..%.3g ; e_x %.3g..%.3g MJ/kg ; j %.3g..%.3g A/m2 ; tau %.3g..%.3g s" % (M[sel].min()*100, M[sel].max()*100, E_[sel].min(), E_[sel].max(), J[sel].min(), J[sel].max(), T[sel].min(), T[sel].max()))
print("   condition for > 30 mV: m'' e_x/(j tau) > 0.03 -> m'' > 0.03 j tau/(e_x*1e6); at e=2.4e5 MJ/kg, j=5e3, tau=2.88e8: m'' > %.3g kg/m2 (%.1f mg/cm2)" % (0.03*5e3*2.88e8/2.4e11, 0.03*5e3*2.88e8/2.4e11*100))
print("   i.e. the loading would have to exceed 0.18 kg/m2 (18 mg/cm2) at the central duty: above the 5 mg/cm2 sweep ceiling, so the > 30 mV region needs lower j, shorter tau or higher e_x than the central case")
for V in (1.481, 1.8):
    e = 2*F*V/MH2
    print(f"bookkeeping: 2FV/M_H2 at V={V}: {e/1e6:.3f} MJ/kg = {e/3.6e6:.3f} kWh/kg")
chk("2F*1.481/M_H2 vs HHV 141.8 MJ/kg", 2*F*1.481/MH2/1e6, 141.8, 0.01)
chk("2F*1.8/M_H2 vs 47.9 kWh/kg", 2*F*1.8/MH2/3.6e6, 47.9, 0.01)
print("IDENTITY CHECKS: the bookkeeping check compares 2FV/M with a published constant: not an identity. d_eta_be itself is exact arithmetic (no independent route).")
print("NOTE: e_x is cumulative energy demand, not exergy destroyed; the framework definition of Sigma_init is UNSURE (plan section header).")
print("OVERALL", "PASS" if fails == 0 else f"FAIL ({fails})")
