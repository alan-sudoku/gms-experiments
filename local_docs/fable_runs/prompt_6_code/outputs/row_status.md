# Row status, Prompt 6 (rows A1 to E5)

All statuses are claims at level `derived` (unverified). Rows other than A10 and E1 to E5 copy the earlier implementers' saved outputs and issues files; they are not re-judged. 'status not stated' means the saved output gives no verdict line.

| Row | Script | Status | Identity checks flagged | Note |
|---|---|---|---|---|
| A1 | a1_a2_a3_multipliers.py | PASS | yes | p=2 and p=-1 hand values are algebraic restatements; Simpson route independent (max rel diff 5.3e-10) |
| A2 | a1_a2_a3_multipliers.py | PASS | no | extra general-p closed form added as third check (deviation) |
| A3 | a1_a2_a3_multipliers.py | PASS | no | all 18 roots bracketed |
| A4 | a4_a5_a12_simple.py | PASS | yes | (i) 1 - x_e is the formula itself; hand values within 0.3 % |
| A5 | a4_a5_a12_simple.py | PASS plausibility only | yes | 1 + R_f U_clean re-evaluates the same formula; life-average factors verified by Simpson |
| A6 | a6_arrhenius_dT.py | PASS | no | closed vs bisection 4.2e-13; all 40 cases bracketed |
| A7 | a7_a8_electrothermal.py | PASS | yes | fixed-point iteration solves the same linear equation as the closed form |
| A8 | a7_a8_electrothermal.py | PASS | yes | quadrature vs RK4 are independent numerics of the same model; ambiguity on time normalisation |
| A9 | a9_drying.py | PASS | no | hand 8.3 K vs 8.52 K (+2.6 %, inside +-5 %); one ambiguity on multiplier |
| A10 | e3_a10_shares.py | PASS plausibility only | yes | hand 1.25 restates the formula; Simpson route independent; w_fat from E3 (UNSURE) |
| A11 | a11_concurrent_hysteresis.py | FAIL | yes | (b) rainflow within 10 % of idealised ratio fails in 11 of 24 cases (worst -65.5 %); real bound test passes in all 24; (a) trig-orthogonality identity |
| A12 | a4_a5_a12_simple.py | PASS | no | hand values +1.3 %, inside limit |
| B1 | b1_b2_miner_vs_min.py | PASS | yes | R = 2 at s* true by construction; deviation m = 9.80392 |
| B2 | b1_b2_miner_vs_min.py | PASS | no | median 2.968 for L=5, w=0.1 is 1 % from the upper plausibility end |
| B3 | b3_damage_curve_extremes.py | PASS | no | golden vs analytic <= 7.8e-9; all extrema interior |
| B4 | b4_b5_concurrent.py | PASS | yes | tau1/tau_blk >= (1+s)^m true by construction; B5 is the independent check |
| B5 | b4_b5_concurrent.py | PASS | no | ambiguity: 'envelope cycle dominates' undefined; deviation: periodic turning points |
| B6 | b6_b7_slopes.py | PASS | yes | hand values are the same expressions (rounding checks only) |
| B7 | b6_b7_slopes.py | PASS | yes | hand values are the same expressions |
| C1 | c1_c2_baseline.py | PASS | no | sigma_a0 = 108.703 MPa; memory inputs, not independent evidence |
| C2 | c1_c2_baseline.py | status not stated | no | report only (no tolerance); N/N0 = 0.087 inside [0.03, 30]; L07 read in a third-party transcription |
| C3 | c3_c4_section_loss.py | PASS | no | M08 class limits are memory values |
| C4 | c3_c4_section_loss.py | PASS | no | hand values within 0.7 % |
| C5 | c5_rk4_verify.py | PASS | yes | RK4 and C4 closed form share the same ODE |
| C6 | c6_c7_worst_case.py | PASS | yes | grid/golden maximum at rho = 1 compared the C4 formula with itself; RK4 check added |
| C7 | c6_c7_worst_case.py | PASS | yes (partial) | no bracket for three rho_1 values (not verified by bisection); planner values reproduced |
| C8 | c8_lower_bound.py | PASS | no | ratio <= 1 at every grid point; minimum ratios 0.7364 / 0.7301 / 0.7272, interior |
| C9 | c9_parabolic.py | PASS | no | closed vs Simpson ~1e-10 |
| C10 | c10_c11_environment.py | PASS | yes | sweep did not bracket two crossovers (extended bracket did); k5 = k8 = 1 identity; L01 not found (UNSURE grid) |
| C11 | c10_c11_environment.py | PASS | no | 7 of 27 cases have no sign change on [0.01, 10] Hz; L01 not found |
| C12 | c12_c13_pits.py | PASS | no | L02, L06 not read at source; life factor 19.8 vs L06 range 2 to 10 or more |
| C13 | c12_c13_pits.py | PASS | yes (partial) | deviation: planner expectation 'cube-root life longer than linear for tau > 1 yr' does not hold for PF = 10, r = 10 |
| C14 | c14_damage_curve.py | UNDECIDED | yes | null case cannot run for rho = 1 and 10 (life >= t_c); q = 9.804 ratios inside [1, 2.5] |
| C15 | c15_displacement.py | PASS | no | rho* = 0.092559 bracketed (0.09, 0.095) |
| C16 | c16_dnv_anchor.py | PASS | yes | 'factor 3.0' is 10^(delta log a) by construction; knee check independent; 2010 edition |
| C17 | c17_nu_crit.py | PASS | yes | single division, no independent check; -0.97 % vs planner |
| D1 | d1_d2_paralinear.py | PASS | yes | 'm - theta -> 1' by construction at large theta; theta residual up to 2.7e-2 near theta 28 (y and m unaffected) |
| D2 | d1_d2_paralinear.py | PASS | yes (partial) | L05 from Opila-Hann (UNSURE conversion); fallback check is an identity; limiting thickness 10.4 um not reproduced vs 6.9 um |
| D3 | d3_d4_spallation.py | PASS | yes | sqrt(N) and 1 + 1/sqrt(N) ratios are identities; inequalities over 100001 points are the real test |
| D4 | d3_d4_spallation.py | status not stated | yes | slope ratio by construction; ensemble/parabolic 1.33 at t = n0 dt (spec text implies 1) and 3.27 at 10 n0 dt vs about 3.2 |
| D5 | d5_d7_scale_thresholds.py | PASS plausibility only | yes | hand values restate the formula; 9 of 24 grid cases in the 1 to 10 um range |
| D6 | d6_scale_cracking.py | PASS | no | sigma_a0 = 108.7 MPa matches C1 (108.703); all roots bracketed |
| D7 | d5_d7_scale_thresholds.py | PASS | yes | t_i vs dsigma^-4 slope is an identity; hand check passes; Y = 1.12 as stated |
| D8 | d8_breakaway.py | PASS | yes | ratio 1 for tau <= t_b by definition; construction re-derives the ratio only |
| E1 | e1_cost_sensitivity.py | PASS | yes | hand 2.70 and convex-combination bounds true by construction |
| E2 | e2_verdict_error.py | PASS | yes | verdict errors 5.653 / 3.580 / 1.565 (w_emb 1 / 0.5 / 0.1), all within 3 %; E1 cross-check is the same formula |
| E3 | e3_a10_shares.py | PASS plausibility only | yes | L04 not in SOURCES.md (planner UNSURE values); shares 0.0999 / 0.2138 / 0.6863 |
| E4 | e4_cost_bound.py | PASS | yes (partial) | margin 0.181 (accept 0.15 to 0.25); reduced sum 0.125; x* root bracketed; ambiguity on 0.3 tau0 reading |
| E5 | e5_coupling_numbers.py | PASS | no | ambiguity: weighted sum undefined; first-order life invalid for g (10.36 vs 6.03) |

Totals: FAIL 1, PASS 41, PASS plausibility only 4, UNDECIDED 1, status not stated 2; rows with identity checks flagged (including partial): 30 of 49.
