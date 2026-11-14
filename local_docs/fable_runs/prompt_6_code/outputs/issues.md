# Issues, Prompt 6 S2 (all domains)

All entries are claims at level `derived` (unverified). Counts are of issue entries; an entry is classified by keyword priority in its kind field (identity, tolerance, ambiguity, deviation, input, no bracket, fail, undecided, none) (an entry such as `identity check (partial)` counts as identity; `FAIL (plausibility)` as fail; a combined `tolerance (near edge)` as tolerance).

Total entries: 77. By kind: ambiguity 8, deviation 8, fail 1, identity 27, input 12, no bracket 2, none 3, not done 1, note 1, tolerance 13, undecided 1.

| Domain | Entries | By kind |
|---|---|---|
| Rows A, B | 23 | ambiguity 3, deviation 3, fail 1, identity 9, none 3, not done 1, tolerance 3 |
| Rows C | 24 | ambiguity 1, deviation 3, identity 6, input 6, no bracket 2, tolerance 5, undecided 1 |
| Rows D | 12 | ambiguity 1, deviation 1, identity 7, input 2, tolerance 1 |
| Rows A10, E | 18 | ambiguity 3, deviation 1, identity 5, input 4, note 1, tolerance 4 |

## Rows A, B

# Issues, rows A1-A9, A11, A12, B1-B7 (S2 implementer; all claims level `derived`, unverified)

No LOOKUP inputs are used by these rows, so `data/SOURCES.md` was not appended.

| Row | Kind | Detail |
|---|---|---|
| A11 (b) | FAIL (plausibility) | "Rainflow within 10 % of idealised ratio" is not met in 11 of 24 (n, phi, s) cases; worst -65.5 % (n=3, phi=3, s=1/3). Listed spec hand values are the idealised ratios; the rainflow ratios are lower: n=2, s=1/3, phi=9: 1.085 vs 1.33; n=2, s=0.1, phi=9: 1.113 vs 1.18; n=3, s=1/3, phi=9: 1.845 vs 2.0. For phi=3 the rainflow ratio is below 1 (0.70 to 1.14). Cause visible in output: for small s*phi the fast component does not reverse the combined signal, so fewer than phi fast cycles are counted (for example 1 cycle at phi=3, s=0.1) and fast cycles riding on the slow wave have reduced amplitude. Not adjusted. The real test (upper bound of 2.3 >= rainflow value) passes in all 24 cases (min bound/rainflow = 1.0000, attained at phi=1). Sampling change on doubling < 5e-5 (limit 5e-3). |
| A11 (a) | identity check | For phi != 1 the numerical trapezoid mean versus sum w_l s_l^2 sin(delta)/(2E) tests trigonometric orthogonality (algebra of 2.3) only; ratio is 1 to 1e-9. |
| B5 | ambiguity | "Where the envelope cycle dominates" is undefined. I used envelope share (1/N(s1+s2))/d >= 0.5; with it every case is "dominant" and every Da/B4 ratio lies in [0.7, 1.05] (range 0.905 to 1.0000). All other B5 criteria hold (largest amplitude within 1e-5 for aligned phi, cycles <= phi, Db >= Da in all cases, change on doubling < 1e-4). |
| B5 | deviation | History treated as periodic: turning points taken cyclically before rotation to the global maximum (spec step 1 is not explicit about wrap-around). Residue after step 4 was 0 extra points in all cases. For small s (e.g. s=0.05, phi=9) only 1 cycle is counted; B4's "phi-1 cycles of amplitude s2" is not what rainflow sees there (damage ratio still 1.0000 because the envelope cycle dominates). |
| B4 | identity check | tau1/tau_blk >= (1+s)^m is true by construction (tau1/tau_blk = (1+s)^m + (phi-1) s^m). The ratios are closed-form arithmetic with no independent check inside B4; B5 is the independent check. Hand values (1+s)^m agree within 0.21 %. |
| B1 | identity check | R = 2 at s* is true by construction (printed, not counted as a check). Other B1 checks: 1 <= R <= 2 on all 231 grid points (min 1.000013, max 1.9973), s* = 0.79068 / 0.62517 / 0.49431, edges s/s* = 0.7907 and 1.2647, all bracketed and inside the sweep. |
| B1 | deviation | m taken as 1/0.102 = 9.80392 from M03 (b = -0.102); spec quotes m = 9.804. No effect beyond 4e-5. |
| B2 | tolerance (near edge) | Median for L=5, w=0.1 is 2.968, inside the plausibility range 1.5 to 3 but 1 % from its upper end. Monte Carlo SE < 1.1e-3 relative (mean and bootstrapped median), below 1 %. 1 <= R <= L in every sample for all 12 cases. |
| A1 | identity check | Hand values for p=2 (1/(1-x_e)) and p=-1 (1-x_e/2) are algebraic simplifications of the same closed form; only the quadrature comparison is independent (max rel diff 5.3e-10, all cases converged, p=5 x_e=0.9 needs n=4096). |
| A2 | deviation | Added an extra general-p closed form (substitution u = 1 - a s) as a third check; not in spec. Agrees with Simpson to 6e-10. |
| A3 | none | All 18 roots bracketed on [1e-6, 0.99] (f(lo) = -eps, f(hi) > 0); no extension needed; p=2 linear equals eps/(1+eps) to 4e-13. |
| A4 | identity check | (i) 1 - x_e is the formula itself, no independent check. Hand values 0.402, 3.33, 1.33, 0.906 match within 0.3 %. |
| A5 | identity check | 1 + R_f U_clean re-evaluates the same formula as the hand values (plausibility only per spec). Life-average factors 1/2 and 2/3 verified by Simpson (parabolic needs n=131072 because of the sqrt singularity; error 2.6e-9). |
| A6 | none | All 40 cases bracketed on [0, 500 K]; no extension to 5000 K needed. Closed form vs bisection max rel diff 4.2e-13. Hand values within 1.6 %. |
| A7 | identity check | The fixed-point iteration solves the same linear equation as the closed form (an independent numerical route, not an independent model). Max rel diff 3.8e-13 over 56 cases with G < 0.9; G >= 1 cases never converge. |
| A8 | identity check | (a) quadrature of 1/f and (b) RK4 of f are independent numerics of the same separable model. Rel diff <= 4.5e-7 (limit 2e-3). Step halving: time unchanged below 0.1 % at the first halving (200 -> 400 steps) in all 8 cases. Hand values within 1.6 % (alpha=0, dT0=20: 0.1931 vs 0.19). |
| A8 | ambiguity | "Time relative to isothermal at T_env" read as t(x_a)/(x_a t_c); t_c set to 1. |
| A9 | tolerance (inside limit) | Hand 8.3 K for 20 C, 1.00 -> 0.60: calc 8.52 K (+2.6 %, inside the +-5 % limit). 0.95 -> 0.80 gives 2.805 K and 1.00 -> 0.80 gives 3.654 K, inside the stated ranges. All 18 cases bracketed on [0, 30 K]. |
| A9 | ambiguity | "Arrhenius multiplier at that dT" read as exp[(Q/R)(1/T - 1/(T+dT))] with T = theta + 273.15 (value > 1: the rate increase caused by the heating). |
| A12 | tolerance (inside limit) | q'' = 0.02736 W/m2 vs hand 0.027 (+1.3 %); dT = 2.736e-3 K vs 2.7e-3. All cases below 0.01 K (max 5.5e-3 K at r=10, h_c=5). |
| B3 | none | All six extrema interior of the grid; golden vs analytic |du| <= 7.8e-9; hand values within the 0.005 limit. |
| B6, B7 | identity check | Hand values are evaluations of the same expressions (rounding checks only). |
| A10, E rows | not done | Out of scope for this pass. |

## Rows C

# Issues, rows C1-C17 (level `derived`; all UNSURE unless stated)

- C1 | input | M02/M03/M04 are planner memory values, not looked up. sigma_a0 = 108.703 MPa is an arithmetic re-computation; expected-vs-computed agreement is not independent evidence.
- C2 | input | L07 equation read only in a third-party transcription (KasperCalc) of MIL-HDBK-5 Fig. 3.2.3.1.8(e); edition unconfirmed; the handbook cautions R = -1 may lie outside the fitted data (S_eq formula). N/N0 = 0.087 (inside [0.03, 30]); no tolerance, report only.
- C3 | input | M08 ISO 9223 class limits are memory values; ISO 9223 not read. Class placement C4/C5/CX for r = 1/3/10 um/yr depends on them.
- C5 | identity check | The RK4 route and the C4 closed form share the same ODE; C5 verifies the integration algebra, not the model. The route is independent in method (pointwise integrand vs analytic antiderivative). Agreement 1e-9 to 1e-14, far better than the 0.1 % criterion (the integrand does not depend on D, so RK4 acts as a quadrature rule).
- C6 | identity check | Comparing the grid/golden maximum at rho = 1 with 1/(1 - q^(-1/(q-1))) compares the C4 formula with itself (the grid contains rho = 1). An RK4-based F_min(rho=1) was added as the independent check (agrees to <3e-9).
- C6 | deviation (minor) | Golden-section on each side of the kink returns the kink (rho = 1) because the function is monotone on each side and the bracket end is the kink; it adds no information beyond monotonicity.
- C7 | no bracket | rho_1 for (q = 9.804, x_allow = 0.8) = 1.6e5; (q = 19.608, x_allow = 0.5) = 2.1e4; (q = 19.608, x_allow = 0.8) = 5.5e11: bisection of tau_c - tau_rec has no sign change on [1e-3, 1e3] nor on the once-extended [1e-4, 1e4]. Not verified by bisection; only the closed form is available for these. x_allow = 1.0 has no rho_1 (infinite). Planner values (max F_min 1.84, 2.87, 3.79, 4.38; rho_1 0.70) reproduced.
- C7 | identity check (partial) | The rho_1 bisection shares the C4 formula; it is independent only of the algebraic inversion.
- C7 | deviation (minor) | The maximum was located at rho = x_allow by golden-section with the kink as bracket end (same remark as C6).
- C8 | tolerance (none) | Ratio <= 1 on all 121 grid points for all three q (max 0.9977, 0.9952, 0.9905 at rho = 1e-3). Minimum ratios 0.7364 (q = 4.5585, rho = 1.84), 0.7301 (q = 9.804, rho = 1.32), 0.7272 (q = 19.608, rho = 0.83), all interior. Planner values reproduced (0.73, x* = 0.167, 0.109, ~0.80 at rho = 100: computed 0.7947).
- C9 | tolerance | Closed form vs Simpson route agree to ~1e-10 (< 1e-6). Hand value reproduced (tau/t_c = 0.0858, F_min = 11.66). Small-tau check ratio 1.0066 at u = 1e-6 (a first-order correction of order q*sqrt(u), not exact 1) is not a failure.
- C10 | no bracket | The 61-point sweep in [100, 400] MPa does not bracket the crossover for (k5, k8) = (0.8, 0.6) [447.6 MPa] and (0.9, 0.8) [486.7 MPa]; the once-extended bracket [10, 4000] did, and the power-law closed form agrees. (0.8, 0.8): parallel curves, no crossover (ln F = 2.19 at both ends). k5 = 1.0: crossover at N = 1e5 by construction (not a check). k5 = k8 = 1: F = 1 identically (identity check; no crossover defined). For k8 = 1.0 with k5 < 1 the crossover sits at N = 1e8 (sigma = 128.1 MPa), not near 1e5, because k(N) rises towards 1 at 1e8.
- C10, C11 | input | L01 not found (ASM Handbook Vol. 19 paywalled); the planner's UNSURE grid used. All C10/C11 results are conditional on that grid.
- C10 | identity check | The crossover closed form was computed independently of the bisection and agrees; this is a check of algebra only.
- C11 | tolerance | Wall hand values reproduced within 0.2 %. nu(F = 1.05) = 0.3096 Hz (wall, 0.3 mm, n_s 2, r 10), inside 0.1 to 1 Hz. On the full C3 grid, 7 of 27 cases have F_sec,env < 1.05 at 0.01 Hz (no sign change on [0.01, 10] Hz; reported, not extended).
- C12 | input | L02 not read at source (UNSURE); baseline 3.0. Life factor at 100 um is 19.8 vs the planner's L06 range 2 to 10 or more (L06 not read at source; secondary reports of 6 to 8 for 7075-T6 pre-pitted). The model assumption (sigma_a0/K scaling the whole S-N curve) is medium/low confidence per the plan and was not tested.
- C13 | deviation | Cube-root growth (b): for PF = 10, r = 10 the life is 1.186 yr, shorter than the linear (a) value 1.310 yr although tau_a > 1 yr; the planner expectation "(b) longer than (a) for tau > 1 yr" does not hold in that case (a(t) of the cube-root form exceeds the linear form for t < 1 yr). Reported, not adjusted. Perforation time uses the linear PF*r as spec (c).
- C13 | identity check (partial) | (a) closed form vs Simpson+bisection agree to 1e-12; independent in method.
- C14 | UNDECIDED (null case, rho >= 1) | With q = 0 the life is tau0 = rho*t_c >= t_c, beyond the t_c(1-1e-12) integration limit, so the null case cannot be run for rho = 1 and 10; rho = 0.01 and 0.1 return tau0 exactly. The null case is an identity check of the step/event logic (the second term is multiplied by q).
- C14 | tolerance | q = 9.804: ratio tau_DCA/tau_c = 1.0091, 1.0540, 1.0809, 1.0496 for rho = 0.01, 0.1, 1, 10: all >= 1 and inside [1, 2.5]. RK4 converges after one halving (change < 1e-8); the u ln u singularity at u = 0 did not degrade it visibly.
- C15 | ambiguity (minor) | Planner quoted rho* = 0.0926; computed 0.092559 (identical to the quoted digits). Bracket 0.09 / 0.095 confirmed by Simpson D(1). Bisection of Simpson D(1) - 1 gives rho* independent of 1/((m+1) rho).
- C16 | identity check | "Factor 3.0 at and above 52.63 MPa" equals 10^(12.164 - 11.687) = 2.9992 by construction (not independent). The knee-consistency check is the real check: m = 3 branch 1.0007e7, m = 5 branch 9.9962e6 at 52.63 MPa (within 0.07 %). Constants read from the April 2010 edition of DNV-RP-C203; the current edition may differ (UNSURE).
- C17 | tolerance | 3.169e-4 and 3.169e-3 Hz vs planner 3.2e-4, 3.2e-3 (-0.97 %, within 1 %). Single division: no independent check.
- General | input | m = 1/0.102 = 9.8039 used (planner rounded 9.804; effect < 1e-4). Hand-value expected figures are the planner's own arithmetic from the same formulas.

## Rows D

# Issues D1 to D8 (S2 implementer; level: derived, unverified)

1. D1 / tolerance. Bisection stopped at relative bracket width 1e-12 in y leaves a relative theta-residual up to 2.7e-2 (at theta = 28.2) for theta between about 20 and 30, because 1-y ~ exp(-theta) is below the 1e-12 resolution in y. y is correct to 1e-12 absolute and m = y + theta is unaffected, so every D1 result is unaffected; the stated tolerance is satisfied in y and m, not in theta(y). Not resolved (spec rule followed).
2. D1 / identity check. "m - theta -> 1 at large theta" evaluates y = 1 - exp(-theta-1), the formula used for theta > 30, so the value 1 is by construction (flagged identity). The small-theta limit (m - sqrt(2 theta))/(theta/3) is 1.0024 at theta = 1e-4 (O(sqrt(theta)) correction), so it is not an identity.
3. D1 / ambiguity. The coarse-grid maximum of m/L sits next to the kink at theta = 2; golden section was applied on each side of theta = 2 and returns the kink itself (1.473765). Maximum of U/m: 1.369277 at theta = 3.3222 (inside the grid; PASS). Golden-section position of a flat maximum is good only to about 1e-8 in ln theta.
4. D2 / identity (partial). D2 is independent of D1 numerically (differential equation, series start and RK4 versus the integrated relation and a root solve) but shares the dimensionless ODE derivation. It checks the integration, not the derivation from d(delta)/dt = kp'/delta - kl. Agreement is 6e-13. At theta = 100, y = 1.000000 to 8 digits, so that target tests little.
5. D2 / deviation. RK4 step: "geometric step growth" implemented as h = min(eps*theta, eps) (the cap eps is needed for RK4 stability at large theta where dy/dtheta ~ (1-y)). Converged at eps = 0.05 (change 9.5e-8 vs eps = 0.1).
6. D2 / input (L05). Paralinear constants for SiC at 1200 C read from Opila and Hann 1997 (see data/SOURCES.md): kp' = 6.94e-17 m^2/s, kl = 6.69e-12 m/s, converted by the implementer; UNSURE. Limiting thickness 10.4 um versus the paper's 6.9 um is not reproduced. The planner's expected values (delta_lim = 10 um, t = 2e7 s) were checked for the fallback; for the L05 constants t(theta = 2) = 3.10e6 s. The fallback "check" is an arithmetic identity (flagged). Tedmon 1966 constants were not read (paywalled).
7. D3 / identity check. The values m/parabolic = sqrt(N) and U/m = 1 + 1/sqrt(N) at t = N dt are algebraic identities of the formula (deviation 2e-16); the inequalities parabolic <= m <= U over 100001 grid points are the real test (PASS). The smallest (m - parabolic)/parabolic is -2.3e-16 (rounding at interval starts, within tolerance).
8. D4 / identity-class and ambiguity. The slope ratio (1.0000, 0.9999) follows from the patch formula by construction (spec says so). The spec's "m_ens/parabolic ~ sqrt(t/(n0 dt))" is asymptotic: at t = n0 dt the ratio is 1.33, at 10 n0 dt it is 3.27 versus the spec's "about 3.2" (2 % off), at 100 n0 dt it is 10.03. The spec text gives crossover at t = n0 dt; the computed ensemble is 1.33 times the parabolic law there, not 1. Bookkeeping assumption (first spall of patch j at interval j, regrowth from zero) is the implementer's reading.
9. D5 / identity-class. Hand values restate the same formula; passes (0.55 to 0.70 % from rounded hand values). Plausibility of 1 to 10 um: 9 of 24 grid cases lie in range (0.027 to 101 um across the grid); plausibility only.
10. D6 / input. sigma_a0 = 108.7 MPa is the planner's value, not computed from C1; the final pass must re-run D6 if C1 gives a different value. eps_a = 1.489e-3. c_x values: 0.198, 0.793, 3.17, 12.68 um for K_Ic 0.5, 1, 2, 4; all roots bracketed in [1e-9, 1e-3] m.
11. D7 / identity check. The t_i versus dsigma^-4 slope check is an algebraic identity (-4.000000). Hand check passes (39.65 um, 7.86e6 s). The spec uses Y = 1.12 in D7 although M15 lists 1.12 as the edge-crack f and 0.713 as the semicircular-crack Y; implemented as stated.
12. D8 / identity check. The ratio for tau <= t_b is 1 by definition (identity); the construction h_b + r_b (tau - t_b) reproduces the closed form for tau > t_b to 4e-16 and is an independent re-derivation of the ratio, not of the breakaway model. The sweep brackets the onset (0.5, 0.9, 1.0 below or at, 1.1 above).

## Rows A10, E

- E3 | input (L04) | L04 (standard chemical exergy of Al) is not in data/SOURCES.md; not looked up. Planner UNSURE values used: 795.7 kJ/mol (main) and 888.2 kJ/mol (alternative). Result UNSURE. Shares (fat, corr, emb) = 0.0999, 0.2138, 0.6863 (main); 0.0975, 0.2329, 0.6697 (alternative).
- E3 | input | M21 (psi = 2e-3), M27 (e_emb = 200 MJ/kg; w_emb = 0.621 at 150, 0.706 at 220 MJ/kg), M05, M06, M07, M23 are planner memory values. Rates 1.1513e-10, 2.4638e-10 (2.7502e-10 alternative), 7.909e-10 W/K are within 3 % of the hand values (corrosion -1.45 %); the corrosion share is +1.8 % from the hand 0.21 (hand shares rounded to 2 digits). Plausibility only.
- E3 | ambiguity (minor) | Embodied rate uses the air life tau0 (15.844 yr at 1 Hz), as the spec formula says, not the coupled life.
- E3 | identity check | Single-pass arithmetic; the hand values restate the same formulas. No independent check exists.
- A10 | identity check | The hand value 1.25 (beta = 5, gamma = 1, w_fat = 0.1) restates the formula. The Simpson integral of 1 + beta s^gamma on [0,1] is an independent route (max rel diff 4.5e-10, 12 cases).
- A10 | input | The E3 w_fat (0.0999) inherits the UNSURE inputs of E3; total effect at beta = 10, gamma = 1 is 1.4995 with that share and 3.5 at w_fat = 0.5.
- E1 | identity check | The hand value 2.70 and the convex-combination bounds min(F, sqrt F, M) <= ratio <= max(...) are true by construction (0 violations). w_lin = 1 - w_emb - w_ox is -2.8e-17 (float rounding) at w_emb = 0.9, w_ox = 0.1.
- E2 | tolerance | F_g = 7.0336 (hand 7.0, +0.48 %), F_s = 1.2443 (1.24, +0.35 %), tau_c(g) = 2.2526 yr, F_min(g) = 6.659. Verdict error 5.653 (w_emb = 1; hand 5.7, -0.83 %), 3.580 (0.5; hand 3.6, -0.57 %), 1.565 (0.1; hand 1.56, +0.33 %); 4.406 at the planner's literal 0.687 and 4.403 at the E3 share 0.6863. All within 3 %.
- E2 | identity check | The cross-check of the verdict error against E1's cost_ratio (w_ox = 0, M = 1) uses the same formula (difference 0).
- E4 | ambiguity | "tau0 replaced by 0.3 tau0 in the tau_LB step" read as rho' = 0.3 rho in the x* equation with the ORIGINAL tau0 in the numerator of tau0/tau_LB. This reproduces the planner's tau_LB' = 1.087 yr and margin 0.125. The alternative reading (0.3 tau0 in the numerator too) gives margin 0.347 and does not match.
- E4 | tolerance | x* = 0.109263 (root bracketed by construction: f(0) = -rho = -1.05627, f(1) = +1; no extension needed), tau_LB = 1.6389 yr (hand 1.64). w_emb = 0.5, w_lin = 0.5, p_r = 2: c_U/c_model = 5.526 (hand 5.5), required margin 0.181 (accept 0.15 to 0.25); reduced sum: 7.979 and 0.1253 (hand 0.125). Margin ranges over the grid: 0.111 to 0.494 (standard), 0.074 to 0.397 (reduced).
- E4 | identity check (partial) | The bound c_U/c_model >= c_true/c_model (E1 with F_cur from C4 and M_lin by Simpson) holds in all 12 share cases; it follows from tau_LB <= tau_c (C8 verified) and (1 - x_e)^(-p_r) >= M_lin, so it tests the inequality chain on the single g case, not the bound in general. At w_emb = 0.5, w_ox = 0, p_r = 2: c_true/c_model = 4.105 versus the bound 5.526.
- E5 | tolerance | g: x_e = 0.1502 (hand 0.150); rate first-order 0.1502 vs exact 0.1767 (hand 0.177); life first-order 10.356 vs exact 6.034 (hand 6.0). s: x_e = 0.04244 (hand 0.042, +1.1 %); rate 0.02122 vs 0.02184; life 0.2589 vs 0.2443. Thermal (50 kJ/mol, 300 K): first-order 0.0668 vs exact 0.0689 at 1 K; 0.3341 vs 0.3890 at 5 K.
- E5 | tolerance (invalid regime) | First-order life estimate q rho/2 is invalid for g (rho = 1.056): it overestimates F_cur - 1 by 72 % (reported per spec).
- E5 | ambiguity | "Weighted sum with E3 shares" is undefined in the spec. Reading used: embodied share x life error, corrosion share x rate error (thermal error compounded as a separate line), fatigue share x 0. Shown for g only, because E3 shares belong to the worked strut. Result 7.14 (first-order) versus 4.18 (exact); not a spec figure.
- E5 | deviation | M_lin closed form and the Arrhenius multiplier are restated in e5_coupling_numbers.py (and the M_lin Simpson route in e4_cost_bound.py), not imported: a1_a2_a3_multipliers.py and a6_arrhenius_dT.py run their whole checks on import and have no main guard, and the earlier scripts were not to be edited. M_lin agrees with the saved A1 output to 4.6e-9 (45 rows); the multiplier at A6's saved dT (0.7320 K) is 1.050002.
- D6 | input (resolved) | C1 gave sigma_a0 = 108.703 MPa, matching the 108.7 MPa constant D6 used (0.003 %), so D6 needs no re-run.
- General | note | The 'A10, E rows not done' line in the A, B file is superseded by this section. No sweep in rows A10, E1 to E5 targets a root or crossover other than the C8 root x* in E4 (bracketed).
