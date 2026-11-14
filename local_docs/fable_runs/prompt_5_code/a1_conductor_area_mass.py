#!/usr/bin/env python3
"""A1: equal-DC-resistance area and mass ratio, Al vs Cu.
Spec row: A1 (prompt_5_plan.md section 3). Claims G1.3, G2.5.  Level: derived (unverified).
Assumptions: A_g/A_s = sigma_s/sigma_g ; m_g/m_s = rho_g*sigma_s/(rho_s*sigma_g).
sigma_Cu = 5.80e7 S/m (IACS), sigma_Al = 3.54e7 S/m (61% IACS, MEMORY), rho_Cu 8960 (and 8890), rho_Al 2700 (MEMORY).
LOOKUP: IEC 60228:2004 Table 2 (data/a1_iec60228_class2.csv): Al conductor of equal DC resistance must have 1.6-1.7x the Cu area.
"""
import csv, os
here = os.path.dirname(os.path.abspath(__file__))
s_cu, s_al = 5.80e7, 3.54e7
fails = 0
def chk(name, val, exp, tol):
    global fails
    ok = abs(val/exp - 1) <= tol
    fails += (not ok)
    print(f"CHECK {name}: value={val:.5f} expected={exp} tol=+-{tol*100:.0f}% -> {'PASS' if ok else 'FAIL'}")
print("INPUTS: sigma_Cu=5.80e7 S/m (IACS), sigma_Al=3.54e7 S/m (MEMORY), rho_Al=2700, rho_Cu=8960 and 8890 kg/m3 (MEMORY)")
Ar = s_cu/s_al
print(f"area ratio A_Al/A_Cu = {Ar:.5f}")
chk("area ratio", Ar, 1.64, 0.03)
for rc in (8960, 8890):
    mr = 2700*s_cu/(rc*s_al)
    print(f"rho_Cu={rc}: mass ratio m_Al/m_Cu = {mr:.5f}")
    chk(f"mass ratio (rho_Cu={rc})", mr, 0.49, 0.03)
print("note: with rho_Cu=8890 the ratio is 0.4977 vs expected 0.49: deviation 1.6%, within the 3% tolerance")
print("LOOKUP SOURCE: IEC 60228:2004 ed 3.0 Table 2 cols 7 and 9, publisher preview PDF https://cdn.standards.iteh.ai/samples/12024/921fee9a88c24612b68340a7330c2262/IEC-60228-2004.pdf, accessed 2026-11-14")
rows = []
with open(os.path.join(here, "data", "a1_iec60228_class2.csv")) as f:
    for r in csv.reader(l for l in f if not l.startswith("#")):
        if r[0] == "area_mm2": continue
        rows.append(tuple(map(float, r)))
print("area_mm2  R_Cu   R_Al   R_Al/R_Cu (= Al area / Cu area for equal R at equal nominal-size lay)")
rat = []
for a, c, al in rows:
    rat.append(al/c); print(f"{a:7.0f} {c:7.4f} {al:7.4f} {al/c:7.4f}")
lo, hi = min(rat), max(rat)
print(f"range of IEC ratio: {lo:.3f}..{hi:.3f} ; implied sigma_Cu/sigma_Al from mean ratio {sum(rat)/len(rat):.3f}")
ok = all(1.6 <= x <= 1.7 for x in rat)
print(f"CHECK IEC ratio in 1.6-1.7 for all sizes -> {'PASS' if ok else 'FAIL'}")
fails += (not ok)
# note: ratio of resistance at equal area is the equal-R area ratio only to first order
print("note: the table gives R at EQUAL nominal area; the equal-R area ratio is the same number only because R is inversely proportional to area (sigma*A/L); lay factor assumed identical for both metals (UNSURE)")
print("IDENTITY CHECKS: none (expected values 1.64/0.49 come from the plan and the IEC data are independent of the sigma inputs)")
print("OVERALL", "PASS" if fails == 0 else "FAIL")
