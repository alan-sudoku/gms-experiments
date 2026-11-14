#!/usr/bin/env python3
"""S5 review, tasks (2) and (4): independent application of the revised gate (answer section 8) to the 18 J1 cases,
a mixed-route test of the gate's envelope step, and the dependence of G2 results on the Sigma_init currency.
numpy + scipy only. Usage: python3 r2_gate_independent.py   Level: derived (unverified).

Part A encodes each case from the Note J1 text of prompt_5_plan.md (not from s4_checks.py), under two readings of
the places where the answer's section 8 wording leaves a choice. Prices are the S2 numbers quoted in the answer.
Part B: fin with two capped dimensions (thickness, height). Each single route fails its cap, a combined design meets
the requirement. The fin model is the answer's own (G1.5): q' = theta_b sqrt(2 h k t) tanh(L sqrt(2h/(k t))).
Part C: margins of the G2.3 and G2.6 outcomes against a change of the Sigma_init currency.
Part D: P1 numbers under the fairness rule (pipe against pipe instead of pipe against solid Cu).
"""
import math
import numpy as np
from scipy.optimize import brentq
INF = float("inf")

print("== A. Revised gate (answer section 8), own encoding of the 18 Note J1 cases ==")
# fields: n, text, inputs_a_d_ok, thresholds [(name, 'pass'|'fail'|'missing')], envelope ('none' | 'qualitative' | dict q->slack),
#         margin (None = not stated, number = F_s/F_req), requirement_is_limit, routes {route: {q: price}}
# Reading A = strict literal; Reading B = the alternative reading noted per case.
def gate(c, reading):
    if not c["a_d"]:
        return "U", 1
    if c.get("no_solid_coeff"):
        return "N", 1
    for _, st in c["thr"](reading):
        if st == "fail": return "I", 2
    for _, st in c["thr"](reading):
        if st == "missing": return "U", 2
    routes = c["routes"](reading)
    env = c["env"](reading)
    if not routes:            # no deficit to make up
        return "II", 5
    # step 4 first rule: some route with pi <= 1
    def route_ok_le1(r):
        prices = routes[r]
        if reading == "B_any":   # pass if ANY quantity of the route has pi <= 1 (and no cap is violated)
            return any(p <= 1 for p in prices.values()) and all(p <= env.get(q, INF) for q, p in prices.items()) if isinstance(env, dict) else any(p <= 1 for p in prices.values())
        return all(p <= 1 for p in prices.values())
    if any(route_ok_le1(r) for r in routes):
        return "II", 4
    if env in ("none", "qualitative") or (c["req_limit"] and c["margin"] is None):
        return "U", 4
    slack = dict(env); slack["function"] = c["margin"] if c["margin"] is not None else 1.0
    def route_fits(r):
        return all(p <= slack.get(q, INF) for q, p in routes[r].items())
    if any(route_fits(r) for r in routes):
        return "II", 5
    return "I", 4

nothr = lambda rd: []
C = [
 dict(n=1, t="photon 100 keV, mass cap 3x (C for W)", a_d=True, thr=nothr, env=lambda rd: {"mass": 3}, margin=1.0, req_limit=False,
      routes=lambda rd: {"areal mass": {"mass": 29.31}}),
 dict(n=2, t="photon 1 MeV, mass cap 3x, thickness free", a_d=True, thr=nothr, env=lambda rd: {"mass": 3, "thickness": INF}, margin=1.0, req_limit=False,
      routes=lambda rd: {"areal mass (broad beam)": {"mass": 1.163, "thickness": 11.81 * 1.163 / 1.040}}),
 dict(n=3, t="photon 1 MeV, thickness cap 3x", a_d=True, thr=nothr, env=lambda rd: {"thickness": 3}, margin=1.0, req_limit=False,
      routes=lambda rd: {"thickness": {"thickness": 8.883}}),
 dict(n=4, t="thermal neutron, thin sheet (Al or C for Cd or B)", a_d=True, thr=nothr,
      env=lambda rd: "qualitative" if rd == "A" else {"thickness": 3},   # B: read 'thin sheet' as a thickness cap of order the incumbent's
      margin=1.0, req_limit=False, routes=lambda rd: {"areal amount": {"mass": 2.62e3, "thickness": 8.39e3}}),
 dict(n=5, t="bulk neutron shield, thickness free", a_d=True, thr=nothr, env=lambda rd: {"thickness": INF}, margin=1.0, req_limit=False,
      routes=lambda rd: {"water thickness": {"thickness": 332.8, "mass": 38.4}}),
 dict(n=6, t="black absorber, tau >= 3 both", a_d=True, thr=nothr, env=lambda rd: "none", margin=1.0, req_limit=False,
      routes=lambda rd: {"same sheet": {"thickness": 1.0}}),
 dict(n=7, t="storage 1 h, mass cap 2x (DL for Li-ion)", a_d=True, thr=nothr, env=lambda rd: {"mass": 2}, margin=1.0, req_limit=False,
      routes=lambda rd: {"electrode mass": {"mass": 33.3}}),
 dict(n=8, t="storage 5 s pulses, 1e6 cycles (g, s not named)", a_d=False, thr=nothr, env=lambda rd: "none", margin=None, req_limit=False,
      routes=lambda rd: {}),
 dict(n=9, t="primary cell vs DL capacitor", a_d=True, thr=lambda rd: [("state at delivery", "fail")], env=lambda rd: "none", margin=None,
      req_limit=False, routes=lambda rd: {}),
 dict(n=10, t="magnet, volume cap 2x (ferrite for NdFeB)", a_d=True,
      thr=lambda rd: [] if rd == "A" else [("demag field vs H_cJ of g", "missing")],   # B: field threshold activated but no datum in case
      env=lambda rd: {"volume": 2}, margin=1.0, req_limit=False, routes=lambda rd: {"magnet volume": {"volume": 10.84, "mass": 7.08}}),
 dict(n=11, t="magnet, volume free, field below H_cJ", a_d=True, thr=lambda rd: [("demag field vs H_cJ of g", "pass")],
      env=lambda rd: {"volume": INF}, margin=1.0, req_limit=False, routes=lambda rd: {"magnet volume": {"volume": 10.84, "mass": 7.08}}),
 dict(n=12, t="magnet, T_op above Curie of g", a_d=True, thr=lambda rd: [("T_op < T_C", "fail")], env=lambda rd: "none", margin=None,
      req_limit=False, routes=lambda rd: {}),
 dict(n=13, t="DC busbar, cross-section free", a_d=True, thr=nothr, env=lambda rd: {"area": INF}, margin=1.0, req_limit=False,
      routes=lambda rd: {"area": {"area": 1.638, "mass": 0.494}}),
 dict(n=14, t="slot winding, 'within T limit'", a_d=True, thr=nothr, env=lambda rd: {"area": 1.0}, margin=None, req_limit=True,
      routes=lambda rd: {"area": {"area": 1.638}, "accept loss": {"function": 1.638}}),
 dict(n=15, t="slot winding, 'loss <= incumbent loss'", a_d=True, thr=nothr, env=lambda rd: {"area": 1.0, "loss": 1.0}, margin=1.0,
      req_limit=False, routes=lambda rd: {"area": {"area": 1.638}, "accept loss": {"loss": 1.638}}),
 dict(n=16, t="air-cooled sink, short fins (Al for Cu)", a_d=True, thr=nothr, env=lambda rd: "none", margin=None, req_limit=False,
      routes=lambda rd: {"same geometry": {"function": 1.0668}, "thicker fins": {"thickness": 2.0, "mass": 0.6027}}),
 dict(n=17, t="OER in acid (Ni-Fe for Ir oxide)", a_d=True, thr=lambda rd: [("stability of g in electrolyte", "missing")],
      env=lambda rd: "none", margin=None, req_limit=False, routes=lambda rd: {}),
 dict(n=18, t="flow manifold, viscous loss", a_d=True, no_solid_coeff=True, thr=nothr, env=lambda rd: "none", margin=None,
      req_limit=False, routes=lambda rd: {}),
]
EXPECT = {1: "I", 2: "II", 3: "I", 4: "I", 5: "II", 6: "II", 7: "I", 8: "II", 9: "I", 10: "I", 11: "II", 12: "I", 13: "II",
          14: "II", 15: "I", 16: "II", 17: "I", 18: "N"}
S4 = {1: "I", 2: "II", 3: "I", 4: "U", 5: "II", 6: "II", 7: "I", 8: "U", 9: "I", 10: "I", 11: "II", 12: "I", 13: "II",
      14: "U", 15: "I", 16: "U", 17: "U", 18: "N"}
for rd, label in (("A", "reading A (literal; route passes step 4 only if all its prices <= 1)"),
                  ("B_any", "reading B ('some route with pi <= 1' read per quantity; case 4 'thin' = thickness cap 3x; case 10 field threshold activated without datum)")):
    print("\n" + label)
    tally = {"expected": 0, "U": 0, "opposite": 0, "differs_from_S4": 0}
    for c in C:
        rr = "B" if (rd == "B_any" and c["n"] in (4, 10)) else rd
        res, step = gate(c, rr if c["n"] in (4, 10) else rd)
        e = EXPECT[c["n"]]
        if res == e: tally["expected"] += 1
        elif res == "U": tally["U"] += 1
        else: tally["opposite"] += 1
        if res != S4[c["n"]]: tally["differs_from_S4"] += 1
        print("  %2d %-45s -> %-3s (step %d)  plan expected %-3s  S4 %-3s %s" % (c["n"], c["t"], res, step, e, S4[c["n"]],
              "" if res == S4[c["n"]] else "<-- differs from S4"))
    print("  tally:", tally)

print("\n== B. Mixed compensation routes: the gate's step 4 tests one route at a time ==")
h, L0, t0, ks, kg = 50.0, 0.030, 0.001, 400.0, 200.0
q = lambda k, t, L: math.sqrt(2*h*k*t)*math.tanh(L*math.sqrt(2*h/(k*t)))   # W/m per K of base excess
qs = q(ks, t0, L0)
print("  incumbent Cu fin: h = 50 W/m2K, L = 30 mm, t = 1 mm: q'/theta_b = %.4f W/(m K)" % qs)
t_only = brentq(lambda t: q(kg, t, L0) - qs, 1e-4, 1e-2) / t0
L_only = brentq(lambda L: q(kg, t0, L) - qs, 1e-3, 1.0) / L0
print("  Al(200) single routes at equal function: thickness only pi_t = %.4f (height fixed); height only pi_L = %.4f (thickness fixed); same geometry pi_F = %.4f" % (t_only, L_only, qs / q(kg, t0, L0)))
cap_t, cap_L = 1.5, 1.05
print("  scenario: thickness cap %.2fx, height cap %.2fx, no requirement margin (slack_F = 1)" % (cap_t, cap_L))
print("  gate, answer step 4: thickness route %.3f > %.2f, height route %.3f > %.2f, same-geometry route %.3f > 1 -> every route fails -> Class I" % (t_only, cap_t, L_only, cap_L, qs / q(kg, t0, L0)))
qc = q(kg, cap_t*t0, cap_L*L0)
print("  combined design t = %.2fx, L = %.2fx: q'_g/q'_s = %.4f (>= 1 means feasible); fin volume %.3fx; fin mass %.3fx of Cu (rho 2700/8960)" % (cap_t, cap_L, qc/qs, cap_t*cap_L, cap_t*cap_L*2700/8960))
print("  => a constrained comparison finds a feasible g that the gate classified Class I. G4.3 ('same result as a constrained Sigma comparison') fails for the gate as worded.")
# how large is the region where this happens?
tt = np.linspace(1.0, t_only, 200); LL = np.linspace(1.0, L_only, 200)
cnt = 0; tot = 0
for a in tt[1:-1]:
    for b in LL[1:-1]:
        tot += 1
        if q(kg, a*t0, b*L0) >= qs: cnt += 1
print("  caps strictly below both single-route prices: %d of %d (t, L) cap pairs admit a combined feasible design (%.0f%%)" % (cnt, tot, 100*cnt/tot))

print("\n== C. Dependence on the Sigma_init currency (answer G2.3, G2.6) ==")
rho_cu, rho_al, s_cu, s_al = 8960.0, 2700.0, 5.80e7, 3.54e7
be = (rho_cu/s_cu)/(rho_al/s_al)
print("  break-even e_Al/e_Cu = %.4f" % be)
pairs = [("ICE virgin 218/57.0", 218/57.0, True), ("Nuss primary 194/59.3", 194/59.3, True), ("Nuss mix 131/53.7", 131/53.7, True),
         ("ICE recycled Al / virgin Cu 29.0/57.0", 29.0/57.0, False), ("Nuss old scrap / primary 23.8/59.3", 23.8/59.3, False),
         ("ICE recycled/recycled 29.0/16.5", 29.0/16.5, True), ("Nuss secondary/secondary 23.8/28.1", 23.8/28.1, True)]
for name, r, sym in pairs:
    print("  %-40s e-ratio %.3f  Sigma ratio %.3f  %s  relative change of the e-ratio that flips it: %+.0f%%  %s" % (
        name, r, math.sqrt(r/be), "Al wins" if r < be else "Al loses", 100*(be/r - 1), "" if sym else "[asymmetric supply route: Al recycled, Cu primary]"))
print("  symmetric-route Sigma ratios with secondary metal: %.3f (ICE), %.3f (Nuss); asymmetric pairs used in R1: %.3f, %.3f" % (
    math.sqrt((29.0/16.5)/be), math.sqrt((23.8/28.1)/be), math.sqrt((29.0/57.0)/be), math.sqrt((23.8/59.3)/be)))
for name, e in (("Pt TOTAL", 243000), ("Pt ZA", 308000), ("Pt RU", 327000), ("Pt RU 97.5%", 430000)):
    d = e*1e6*0.5e-2/(5e3*2.88e8)
    print("  G2.6 %-12s d_eta_be = %.3f mV; factor on e_x to reach 30 mV: %.1f" % (name, 1e3*d, 0.030/d))
print("  The gate of section 8 takes no Sigma_init input (inputs a-f), so its class does not depend on the currency;")
print("  only the hand-off (who wins in Class II) does.")

print("\n== D. G2.7 heat pipe under the fairness rule (numbers from outputs/p1_heat_pipe.txt) ==")
keff = {400: 1.13e5, 200: 1.07e5, 16: 4.8e4}
print("  answer compares pipe with solid Cu: %.0fx, %.0fx, %.0fx" % (keff[400]/400, keff[200]/400, keff[16]/400))
print("  fair comparison (incumbent may use the same pipe geometry): k_eff(k_wall)/k_eff(Cu wall): 200 -> %.3f, 16 -> %.3f" % (keff[200]/keff[400], keff[16]/keff[400]))
print("  i.e. a series-resistance dilution (regime R2, penalty phi*(kappa-1)), not a separate door; water/Al exclusion leaves steel (0.425).")
