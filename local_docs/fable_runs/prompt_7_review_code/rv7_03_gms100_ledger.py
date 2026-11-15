"""S5 review of prompt_7_web_answer.md, tasks 3 and 4: the answer's claims against GMS-100 as written.

Purpose
  (a) Show that the answer's currency (A) equals GMS-100's EQ-LIFECYCLE-LOST-WORK-CURRENCY when the
      evaluation dead state is the operational environment (DEF-DEAD-STATE: one dead state per
      evaluation; Sdot_gen,phys = Bdot_lost,phys / T0).
  (b) Claim 8 ("T0,eval is a pure scale factor"): true when every lost work is fixed independently
      of T0 (dissipated work), false in GMS-100 for losses whose lost work is T0 * S_gen with S_gen
      fixed by the process (heat transfer between given temperatures), because in GMS-100 the
      evaluation T0 is also the dead state that prices operational losses.
  (c) Claim 3 under DEF-DEAD-STATE: one T0 for both phases; for dissipated work the GMS-100
      ranking is 100 J vs 60 J at any T0.
  (d) Claim 6 in the GMS-100 ledger: Sigma_s,init uses CExC - b_ch; Sigma_s,EOL charges the
      dispersal of b_ch; Sigma_EOL^ret charges CExC (dispersal + make-up). Totals over the life.

Assumptions
  Illustrative inputs only (stated in the code); no data source. CExC and b_ch values for the
  ledger are placeholders chosen so that CExC > b_ch. Everything is a claim at level `derived`.

Run: <repo>/.venv/bin/python rv7_03_gms100_ledger.py  (from any directory)
"""
TREF = 298.15

print("== (a) answer's (A) vs GMS-100 currency, one dead state T0 = T0,op ==")
U = {"D1": 1000e6, "D2": 950e6}       # upstream lost work at T_ref [J], not converted (E15)
W = {"D1": 10e6, "D2": 50e6}          # operational lost work at T0,op [J]
for T0 in (150.0, 200.0, 290.0):
    gms = {d: (U[d] + W[d]) / T0 for d in U}                 # (1/T0) sum_c B_lost,c
    ansA = {d: (U[d] + T0 * (W[d] / T0)) / T0 for d in U}    # sum_k T0,k S_gen,k / T0,eval
    same = all(abs(gms[d] - ansA[d]) < 1e-9 * gms[d] for d in U)
    print(f"  T0={T0:.0f}: GMS-100 D1 {gms['D1']:.4e}, D2 {gms['D2']:.4e} J/K; identical to answer's (A): {same}")

print("== (b) claim 8: is T0,eval a pure scale factor in GMS-100? ==")
# Design pair: upstream difference fixed in J at T_ref; operational loss is heat transfer
# Q from T_h to T_c (process temperatures fixed by the design, independent of T0), so S_gen is
# fixed and the GMS-100 lost work is B_lost = T0 * S_gen.
dU = -50e6                       # D2 - D1 upstream lost work [J]
Q, Th, Tc = 1.0e9, 400.0, 300.0  # heat transferred over the life [J], temperatures [K]
Sgen_hx = Q * (1 / Tc - 1 / Th)  # [J/K]
dS_hx = 0.30e6                   # D2 - D1 operational S_gen [J/K] (illustrative)
print(f"  heat-transfer S_gen per 1e9 J across 400->300 K: {Sgen_hx:.4e} J/K (independent of T0)")
for T0 in (150.0, 200.0, 290.0):
    sigma = dU / T0 + dS_hx      # GMS-100: (dU + T0*dS)/T0
    print(f"  heat-transfer loss, T0={T0:.0f}: dSigma(D2-D1) = {sigma:+.4e} J/K -> prefers {'D2' if sigma < 0 else 'D1'}")
dW = 0.30e6 * 200.0              # dissipated work difference [J], fixed (same at every T0)
for T0 in (150.0, 200.0, 290.0):
    sigma = (dU + dW) / T0
    print(f"  dissipated work,    T0={T0:.0f}: dSigma(D2-D1) = {sigma:+.4e} J/K -> prefers {'D2' if sigma < 0 else 'D1'}")
print("  -> with T0-dependent lost work the GMS-100 ranking changes with T0; claim 8's falsifier")
print("     ('any rank change means the code re-references losses') would misdiagnose this.")

print("== (c) claim 3 under DEF-DEAD-STATE (one T0 for both phases) ==")
for T0 in (150.0, 220.0, 290.0):
    s1, s2 = 100 / T0, 60 / T0
    print(f"  T0={T0:.0f}: GMS-100 Sigma D1 {s1:.4f}, D2 {s2:.4f} J/K -> prefers {'D1' if s1 < s2 else 'D2'}")
print("  per-phase T0 (currency B) needs two dead states in one evaluation, which DEF-DEAD-STATE forbids.")

print("== (d) claim 6 in the GMS-100 ledger (per mol of x; placeholder numbers) ==")
CExC, bch, wrem, T0 = 3000e3, 888.4e3, 300e3, 200.0   # J/mol, J/mol, J/mol, K (illustrative)
for R in (0.0, 0.5, 1.0):
    init = (CExC - bch) / T0                       # EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL (no transport)
    eol = (R * wrem + (1 - R) * bch) / T0          # EQ-LIFECYCLE-INCUMBENT-EOL
    ret = (R * wrem + (1 - R) * CExC) / T0         # EQ-LIFECYCLE-RETIRED-UNIT-EOL
    print(f"  R_rec={R:.1f}: init {init:.1f}, horizon EOL {eol:.1f}, init+EOL {init+eol:.1f} J/(mol K); "
          f"CExC/T0 = {CExC/T0:.1f}; retired-unit EOL {ret:.1f}")
print("  -> init uses CExC - b_ch (claim 6's quantity); with R_rec = 0 init + EOL = CExC/T0 exactly,")
print("     so CExC over the life is not an overstatement once dispersal is counted.")
print(f"  claim 6's 'overstatement' b_ch/T_ref for this placeholder: {bch/TREF:.1f} J/(mol K) "
      f"(= the dispersal charge, moved in time and place)")
