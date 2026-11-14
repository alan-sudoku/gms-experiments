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
