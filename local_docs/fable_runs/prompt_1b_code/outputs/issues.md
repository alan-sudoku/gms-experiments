# Prompt 1b S2 issues (level: derived, unverified)

Source: the `ISSUE:` lines of the scripts in `../` (`grep -h '^ISSUE' *.txt` reproduces every line; the 30 per-case boundary lines of B05 and the per-case B06 lines are summarised here, not repeated). Nothing below was resolved or corrected; formulas and inputs are as written in plan section 3.

## A. Failed checks and hand-range misses

1. **B05 (iii) PF12 ratio outside 0.85-1.15** at three optima: k=100 W/m/K at 0.3 W (1.164), k=120 at 1 W (1.152), k=100 at 1 W (1.168). Cause not investigated; PF12 gives 15-17 % higher R_fa than PF8/X1 at these points.
2. **B06 cross-method ratios outside the stated range.** f_K/f_J outside 0.65-1.6 at p=1.5/Re_d=100 (1.80), p=2.5 at all four Re_d (1.72-1.92) and p=3.0 at all four Re_d (2.46-2.51). Nu_Z/Nu_K at p=1.5, Re_d=300 is 0.5496 (printed 0.550), just below the 0.55 limit.
3. **B06 f_K is non-monotone in p (plan's suspicion confirmed).** At every Re_d in {100, 300, 500, 1000}, f_K falls from p=1.5 to p=2.0 (minimum near p=2.0-2.25) and then rises with p (for example Re_d=500: 0.891, 0.713, 0.847, 1.115 at p=1.5, 2, 2.5, 3). Fine scan to p=4: f_K reaches 1.98-2.40 at p=4, while f_J falls monotonically (0.42-0.55). For p=1.25 f_K is 1.5-3.5. Physically the friction coefficient should not rise as the pitch opens. B07 uses the favourable friction `min(f_K, f_J)`, so f_K is rarely the active branch at p>=2.5 (f_J is lower there); the four pure combinations in B07 still include f_K at p up to 3.0.
4. **B08 is not a failure, but a low-power check** (see C).
5. **B11 hand expectation missed.** Plan expected pin and gyroid R_fa to approach or beat plate fins at equal V. At V = V_Cu,opt: Cu plate 0.2679 K/W (reference), Al plate k=150 0.2905 (x1.084), Al pin k=150 0.2956 (x1.103, 3.32x the air power), gyroid c_f=0.3, chi=0.2 0.3222 (x1.202, 1.39x), gyroid c_f=1.0, chi=0.1 0.3073 (x1.147, 3.03x). None beats the Cu plate; the pin is 1.8 % above the Al plate at 3.3x the power.
6. **B02 hand range, rounding only:** sigma_Al = 0.168 (k=100) vs stated 0.17-0.58, and 0.584 (k=200) vs 0.58. Differences are in the third digit.
7. **B14 hand range:** Cu R_sp,avg at t_b = 5 mm = 0.0594 K/W vs 0.06-0.10 (the plan's range does not say whether it is for R_sp,max or R_sp,avg; R_sp,max = 0.0808 is inside it).
8. **C05 outside range:** NiFe maximum 0.470 V (eta_ref 0.35 V, b10 = 60 mV/decade) exceeds the reported 0.27-0.45 V band; the plan's own hand range 0.31-0.47 V is met.
9. **C06 hand range:** in-plane drop for rho_bar = 0.10 with Lemlich sigma_eff is 0.164 mV vs hand 0.2-2 mV (0.546 and 0.328 mV for rho_bar 0.03, 0.05 are inside). Through-thickness claim holds (max 0.217 mV < 1 mV).
10. **C08 second route FAILS in one case out of 23:** foam R_f,total=1000 (a_v=6.25e5), j0=1 A/m2, kappa=140, eps_g=0.3: eta_thick vs eta_min differ by -2.5 % (limit 2 %); eta_min = 0.1637 V is only just above 3b = 0.154 V. Another case with eta_min = 0.139 V (kappa=140, eps_g=0) is below 3b, so not counted (-4.7 %). Differences grow as eta_min approaches 3b because the comparison mixes sinh kinetics (eta_min) with Tafel kinetics (E).
11. **C09 hand range, edge only:** 1 M, 10 um gives 5.085 A/cm2 (range max 5); 6.9 M, 10 um gives 35.09 A/cm2 (range max 35). The ranges are the exact end points of the delta_N sweep rounded to two digits.
12. **C13 hand range, edge only:** maximum break-even difference over the input grid is 1.042 mV vs stated range 0.03-1.0 mV (e_Pt 3.0e5, m'' 5 g/m2).

## B. Findings the plan asked to be reported

13. **B05 boundary optima: every one of the 30 plate-fin optima sits at the minimum thickness of its sweep** (Cu at t = 0.3 mm, all Al at t = 0.4 mm). At 1 W, k=100-180 the optimum also sits at the s = 0.8 mm gap limit (N_f = 50). Also the same for B12 (all four Al plate optima at t = 0.4 mm). The Cu and Al sweeps start at different minimum thicknesses (0.3 vs 0.4 mm), so the Al/Cu ratios (1.07-1.29) include the manufacturing-limit difference as well as the conductivity difference; with an equal t_min the ratios would differ. B04 (fixed t = 0.4 mm) is not affected by this.
14. **B07 pin optima:** 6 of 30 favourable winners sit on a d edge (d = 1.0 mm), 2 on a p edge (p = 3.0 at k=390, 0.01 and 0.03 W). Pin winners are not flagged for Re_d (none outside 40-1000) or N_L (none below 10). No disagreement above a factor 1.5 between the four pure correlation combinations.
15. **B09 gyroid sweep does not bracket the optimum:** 139 of 180 winners lie on an a or rho_bar edge; 64 of 180 winners have H/a < 3 (homogenisation doubtful, mostly a = 12 or 15 mm). B12's gyroid winner (a = 12 mm, rho_bar = 0.30) is also flagged H/a = 2.5. The gyroid Re_h reaches 1200-1650 in these winners; the spec states no Re limit for the gyroid, so none was applied.
16. **B09 coupling of c_f and chi:** (GY4) gives h = chi*(f_D/4)*..., and f_D contains c_f, so c_f scales h as well as dP. Lowering c_f therefore does not give a free gain; chi_min for the Cu target at 0.1 W, k_s=150 is 0.500 (c_f=0.3) and 0.535 (c_f=0.1). Hand expectation (chi_min 0.2-0.6 for c_f=0.3, 0.1; no match for c_f=1.0 at P_air <= 0.3 W) is met. The monotonic fall of R_fa with chi was verified on a 0.01 chi grid (no violations).
17. **B12:** for plates, no design has Re < 2300 and a V root inside [1e-6, 0.2] m3/s above about 23.6 W, so min R_fa is infinite at 30 W. The search upper bound was lowered to 23.566 W (printed in the output); all four Al plate targets are reached below 0.21 W, so the bound has no effect on the results.
18. **B13/B11 results:** at the fan operating point Cu 0.2299, Al plate 0.2666, gyroid (0.3, 0.2) 0.3099, Al pin 0.3773 K/W; ranking equals the 0.1 W ranking.
19. **B10 exponents** lie between -0.261 and -0.293 for all architectures (within the expected -0.40 to -0.15, none positive or near zero), and the local slope magnitudes decrease with P_air in every case (for example Cu -0.303 to -0.283).
20. **C03 / C04 R_c below 1.** For P2 flat with j0c = 1e-3 A/cm2 R_c = 0.6 (3 of 90 C03 cases). C04 with alpha_c = 1.0 and 1.5 against flat Pt (P2, R_f = 1) gives R_c = 0.36, 0.036, 2.2e-4, 2.2e-5: R_c < 1 is not a physical roughness factor; it only says the candidate beats Pt on a flat surface. C04 at Pt R_f = 100, alpha_c = 0.5: Δη per decade is 105.8 mV vs b10 = 118.3 mV, but J/(2 R_c j0c) = 8.3 < 10 so the 2 % criterion does not apply.

## C. Checks that are true by construction, identities or low power (flagged, not counted as evidence)

- B01 limit checks (k=1e6, k=1): the limits of the same tanh expression. The FD comparison (diff 6e-6) is independent.
- B02 equal-eta substitution: identity (m depends on k*t only).
- B03 (iii) Nu at L = 100 m: returns the constant 7.55 written in PF8 once the developing term vanishes, so it checks the code, not the constant (exact value is 7.541). B03 (ii) tests the PF3-PF7 chain against 12*mu*u*L/s^2 and is partly independent of the code (it uses the polynomial's beta -> 0 value 24).
- B04 V and dP identical for all k: true by construction (hydraulics function takes no k; V is also cached).
- B08: porous inputs are algebraic rearrangements of the plate inputs (m differs by sqrt(31/32)); and the script re-implements GY6/X1 inline, so the GY class used in B09-B13 is not exercised by B08.
- B11 (dT_air identical, R_fa >= 1/C): both by construction.
- B13 (P_air <= 0.18 W): true for any point on the linear fan curve.
- B14 (i) A_s = A_p: algebraic (the (1-eps) factor removes Phi). B14 (ii) R_sp,max limit is also independent of Bi and R0 once lambda*tau is large (it checks the leading constants only; 1.0004 and 0.2822 vs 0.2702 = +4.45 %, within the 6 % limit).
- B16 (iv) closure sums and the E(T_lm) vs E(T0) statement are identities (printed, not counted). B16 (i)-(iii) are genuine quadrature checks (residuals 1e-6 to 5 % for the series limit, which is -4.7 to -5.2 %).
- B18 (a): Taylor expansion of ln(1+x); true for any dP. T_rho = 303.93 K (vs 300 K), as the plan predicted. B18 (c): arithmetic.
- B15 and B20: plausibility only (B15 bound 100 K; B20 report only).
- C02 limit checks: asymptotes of the same asinh expression with the same b (valid limit checks). C03: algebraic inverse pair (code check only). C12 ratio: identity. C13 cross-check: shares J and tau_op (units and magnitude only). C11: no check exists.

## D. Inputs and conventions that are inconsistent or ambiguous between rows

- **B02 vs 3.1 limits:** with N_f = 32 and t_Al = 1.56 mm (k=100) or 1.30 mm (k=120) the channel gap is 0.325 and 0.594 mm, below the 0.8 mm manufacturing limit of the sweeps; t_Al = 1.56 mm is within the Al sweep (max 2.0 mm) but the N_f = 32 pairing is not feasible.
- **C07/C08 temperature:** kappa = 140 S/m (30 wt% KOH at 80 C) is combined with b at 298.15 K, as the spec instructs; kappa and b refer to different temperatures for that case.
- **C06 vs C07/C08:** C06 rho_bar of 0.03 and 0.05 (eps = 0.97, 0.95) are not used elsewhere; the C07/C08 foam cases use eps = 0.90 (rho_bar = 0.10).
- **B07 "favourable" definition** was implemented as: Nu version K with friction = min(f_K, f_J) at each flow rate. This is the reading of "whichever friction version gives the lower dP at the operating point"; at fixed P_air it equals taking the version with the higher V. The plan could also mean selecting one version per design after solving each separately (same result at fixed P_air, possibly different at fixed V in B11/B13).
- **B05/B12 Re exclusion** (Re >= 2300) is applied to plates only; pin Re_d is flagged (40-1000) but not excluded, and the gyroid has no limit (see 15).
- **B15 total** printed both without and with R_TIM; the 100 K check uses the version with R_TIM (stricter); all designs pass either way (max 65.2 K).
- **PF8/X1:** PF8 is described as a mean Nusselt number on the log-mean temperature difference, while X1 applies eps-NTU on top of G = h*(eta*A_fin + A_base); both were used as written (not investigated for double counting).
- **B17 gap bound** uses a source temperature range of 2*(T_max - T_avg), the plan's assumption.
- **N_T, N_L floors** for pins use floor(W/S_T + 1e-9) to avoid float error at exact ratios (for example 0.06/0.002 = 29.999999999999996); the plan does not specify this.
- **Hand values read as "~"** (B06: f_K ~ 0.70, f_J ~ 0.54, Nu_K ~ 17.4, Nu_Z ~ 14.0) were compared with a 10 % tolerance, my reading; all four are within 2 %.

## E. Row status summary

PASS means every counted check passed; hand-range misses are listed above and not counted as FAIL unless a pass/fail check was missed.

- PASS: B01, B03, B07, B09 (plausibility only), B10 (range only), B12, B16, B17, B18, B19, C01, C02, C03, C04, C07, C10.
- PASS on the counted checks but only identities or plausibility available: B02, B04, B08, B11 (hand expectation missed), B13, B14 (one hand-range miss), B15, B20 (report only), C05 (one outside-range miss), C06 (one hand-range miss), C09 (edge misses), C11 (no check), C12 (identity), C13 (magnitude only; edge miss).
- FAIL: B05 (iii) PF12 ratio at 3 of 30 optima; B06 cross-method ratios (and f_K non-monotone); C08 second route in 1 of 23 cases.
