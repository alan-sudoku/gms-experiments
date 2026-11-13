"""Rows B10, B11, B13.

B10: exponent n in R_fa ~ P_air^n (least-squares slope of ln R_fa vs ln P_air over the five P_air values)
     for each optimised architecture (plates all k, pins favourable, gyroid c_f=0.3 chi=0.2).
B11: equal volume flow: the 0.1 W optima of Cu plate, Al plate (k=150), Al pin (k=150 fav) and two
     gyroid cases driven at V_dot of the Cu plate optimum.
B13: same fan instead of same fan power: operating point on dP = 60(1 - V/0.012) and R_fa.
Level: derived (unverified).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gms_core import *

print("Rows B10, B11, B13  (level: derived, unverified)")
print_inputs(P_air=P_SET, fan="dP=60*(1-V/0.012) Pa", eta_fan=ETA_FAN)

head("B10 exponent n")
names = ["Cu plate", "Al plate k=200", "Al plate k=180", "Al plate k=150", "Al plate k=100", "Al pin k=150 fav", "Gyroid ks=150 cf=0.3 chi=0.2"]
nvals = {}
extra = [("Pin k=390 fav", pin_designs(390.0, "min", "K")), ("Pin k=100 fav", pin_designs(100.0, "min", "K")),
         ("Gyroid ks=100 cf=0.3 chi=0.2", gy_designs(100.0, 0.3, 0.2)), ("Gyroid ks=180 cf=0.3 chi=0.2", gy_designs(180.0, 0.3, 0.2))]
allarch = [(n, arch_designs(n)) for n in names] + extra
for n, ds in allarch:
    Rs = [min_R(ds, P) for P in P_SET]
    slope = lnfit_slope(P_SET, Rs)
    nvals[n] = slope
    print("%-32s R_fa=%s  n=%.4f" % (n, " ".join("%.4f" % x for x in Rs), slope))
    ok = -0.40 <= slope <= -0.15
    print(("RANGE-OK    " if ok else "RANGE-MISS  ") + "n(%s)=%.4f in -0.40..-0.15" % (n, slope))
    if not ok:
        issue("B10 n=%.4f for %s outside expected -0.40..-0.15" % (slope, n))
    if slope > -0.05:
        issue("B10 n=%.4f for %s is positive/near zero: spec calls this an error" % (slope, n))
    # local slopes for non-power-law behaviour
    loc = [math.log(Rs[i + 1] / Rs[i]) / math.log(P_SET[i + 1] / P_SET[i]) for i in range(4)]
    print("    local slopes between neighbouring P_air: " + ", ".join("%.3f" % x for x in loc))

head("B11 equal volume flow V = V_Cu,opt (0.1 W)")
bcu = best(arch_designs("Cu plate"), 0.1)
Vcu = bcu[1]["V"]
print("V_Cu,opt = %.5e m3/s; Cu plate-fin optimum: %s" % (Vcu, bcu[2].label()))
fixed = ["Cu plate", "Al plate k=150", "Al pin k=150 fav", "Gyroid ks=150 cf=0.3 chi=0.2", "Gyroid ks=150 cf=1.0 chi=0.1"]
ref_R = None
rows = {}
for n in fixed:
    b = best(arch_designs(n), 0.1)
    d = b[2]
    r = d.eval(Vcu)
    rows[n] = r
    if ref_R is None:
        ref_R = r["R_fa"]
    print("%-32s design: %s" % (n, d.label()))
    print("     at V_Cu: R_fa=%.4f (x%.3f of Cu plate)  dP=%.3f Pa  P_air=%.4f W (x%.2f of 0.1 W)  dT=%.3f  1/C=%.4f  NTU=%.3f  [R_fa at 0.1 W: %.4f]%s" % (
        r["R_fa"], r["R_fa"] / ref_R, r["dP"], r["P_air"], r["P_air"] / 0.1, r["dT"], r["invC"], r["NTU"], b[0], "  Re>=2300 for plate!" if r["excluded"] else ""))
dTs = [rows[n]["dT"] for n in fixed]
check("B11 energy balance: dT_air identical for all", max(dTs) - min(dTs) < 1e-9, "spread %.3e K" % (max(dTs) - min(dTs)))
check("B11 R_fa >= 1/C for all", all(rows[n]["R_fa"] >= rows[n]["invC"] for n in fixed), "")
issue("B11 both checks (dT_air identical; R_fa >= 1/C) are true by construction: dT=Q/(rho V cp) and R_fa = 1/(C(1-exp(-NTU))) > 1/C for any NTU>0; flagged per instructions")
for n in fixed[2:]:
    r = rows[n]
    beats = r["R_fa"] <= ref_R
    print("    %s: %s Cu plate at equal V (R ratio %.3f) while using %.2f x the air power" % (n, "beats or matches" if beats else "does not beat", r["R_fa"] / ref_R, r["P_air"] / 0.1))

if not any(rows[n]["R_fa"] <= ref_R * 1.02 for n in fixed[2:]):
    issue("B11 hand expectation 'pin and gyroid R_fa approach or beat plate fins at equal V' missed: R ratios to Cu plate = %s (pin, gyroid 0.3/0.2, gyroid 1.0/0.1); they use 3.3x, 1.4x, 3.0x the air power" % ", ".join("%.3f" % (rows[n]["R_fa"] / ref_R) for n in fixed[2:]))

head("B13 same fan (dP = 60(1 - V/0.012))")
res13 = {}
for n in fixed:
    b = best(arch_designs(n), 0.1)
    d = b[2]
    V = solve_fan_point(d)
    r = d.eval(V)
    res13[n] = r
    print("%-32s V=%.4e m3/s dP=%.3f Pa P_air=%.4f W R_fa=%.4f  (fan-curve residual %.2e Pa)  %s" % (
        n, V, r["dP"], r["P_air"], r["R_fa"], abs(r["dP"] - FAN_A * (1 - V / FAN_V)), "[Re>=2300]" if r["excluded"] else ""))
mx = max(r["P_air"] for r in res13.values())
check("B13 P_air at operating point <= 0.18 W", mx <= 0.18 + 1e-9, "max %.5f W" % mx)
issue("B13 check 'P_air <= dP_max*V_max/4 = 0.18 W' is true by construction for any (V, dP) on a linear fan curve (spec says so itself); flagged per instructions")
order13 = sorted(fixed[:4], key=lambda n: res13[n]["R_fa"])
order_p = sorted(fixed[:4], key=lambda n: best(arch_designs(n), 0.1)[0])
print("Ranking at fan operating point (first four, best first):", order13)
print("Ranking at equal 0.1 W optimum                        :", order_p)
if order13 != order_p:
    issue("B13 ranking at fixed-fan operating point differs from ranking at 0.1 W: %s vs %s" % (order13, order_p))
