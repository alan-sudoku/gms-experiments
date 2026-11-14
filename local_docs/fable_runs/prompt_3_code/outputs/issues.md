# Prompt 3, S2: issues log

Level: derived (unverified). Nothing here was resolved by the implementer; each item is recorded as found.
Scripts: `p3_unit_cells.py` (R1-R9), `p3_q4_limits.py` (R10-R15), `p3_q4_entropy.py` (R16-R21), `p3_sensitivity.py` (R22-R25), `p3_q3_normalisation.py` (R26-R27), `p3_mismatch.py` (R28-R32). Outputs in this folder are `<script>.txt`.

## 0. Environment and method

- System `python3` has no numpy and nothing may be installed. All scripts are pure Python (own 6x6 inverse). The shared helper block (inputs, octet model, BCC model, topology table) is copied verbatim into every script so each runs standalone.
- The `SUMMARY` block at the end of each output counts PASS/FAIL/IDENTITY/FLAG per row. R16 shows FLAG=6: these are the six "inconsistent pair" labels the spec asked for, not problems.
- R19 uses a 3000-point log grid (spec asks for at least 80) because a 3 % tolerance is marginal on an 80-point grid near a kink.

## 1. Tolerance misses (computed as specified; the spec's expected value differs by more than the stated tolerance)

All look like rounding of the spec's expected values except where marked.

| Row | Check | Computed | Spec | Err | Tol |
|---|---|---|---|---|---|
| R5 | kappa(3) rectangular | 1.6875 | 1.69 | 0.15 % | 0.1 % (spec quoted to 3 s.f.) |
| R5 | kappa(3) circular | 1.7643 | 1.76 | 0.24 % | 0.1 % (spec quoted to 3 s.f.) |
| R11 | C [100] collapse vs orchestrator 17 MPa | 16.667 | 17 | 2.0 % | 0.5 % (orchestrator's own rounding) |
| R14 | N_x for b = -0.10 | 6.34 | "about 6" | 5.7 % | 1 % |
| R20 | melt floor | 1624.6 | 1.6e3 | 1.5 % | 1 % |
| R20 | LPBF 50 and 500 MJ/kg | 8.9e4, 8.9e5 | 0.9e5, 9e5 | 1.1 % | 1 % |
| R20 | primary Al 200 MJ/kg | 3.56e5 | 3.6e5 | 1.1 % | 1 % |
| R23 | psi_TE(1 Hz), t = 2 mm | 1.137e-3 | 1.1e-3 | 3.4 % | 2 % |
| R29 | min S (BCC, rho 0.1, steel) | 4.34e-4 | about 5e-4 | 13 % | 2 % (spec used the 0.1838 coefficient with rounding; the argmin/argmax identification itself passes) |
| R29 | max S (A, rho 0.4, Ti) | 0.0926 | about 0.09 | 2.9 % | 2 % |
| R28, R30, R31 | the S term, see 3a | | | | |

## 2. Identity cells (true by construction, not reported as PASS)

- R5: kappa(2) = 1 (both sections).
- R8: collapse / bending-only first yield = 16/(3 pi) (closed-form algebra; the numeric version at rho 0.02 is a real check of the stiffness route and passes).
- R14: implied sigma_f' for b = -0.1434 (b was derived from sigma_f' = 668 MPa); fatigue/collapse ratio independent of rho for A, C [100], C [110] (but see 4a for B).
- R17: topology A strut-form Sdot (r^2 = 25 defines sigma_rms).
- R18: S(N)/S(1e7) = (N/1e7)^(1+2b).
- R22: n_d = 2 factor = 1.
- R24: S scaling with psi, sigma_w7^2, K_n^-2, E_s^-1 (verified exact for A, B, C [100]; the b dependence is not an identity and is reported).
- R25: R = -1 returns R14.
- R27: rho-independence of the fatigue/first-yield ratio.
- R32: gamma/eps_m = L/(2 H_L).
- Not identities but worth knowing: R3 and R9 energy equalities test the implementation (Clapeyron on one linear model by two routes), not the pin-jointed or beam assumptions. R7 "biaxial modulus = E*/(1-nu)" is an identity of cubic elasticity but is computed by two separate numeric solves, so it is a real implementation check.

## 3. Ambiguities and assumptions (spec unclear; implementer's reading stated)

a. **R28/R30/R31, the S term.** The spec's expected values (21.7 and 65 MPa; N(50 K) = 5.7e6; 3.7e-6 J/K and 0.041 J/K) match the formula with S = 0. With the octet S = 0.0135 (rho 0.2, H_L = H_2, Ti) the values move: 21.41 and 64.23 MPa (1.2-1.3 % low, FAIL at 1 %); N(50 K) = 6.22e6 (+9.1 %, FAIL at 3 %); dT_x = 124.1 K (+1.7 %, passes); dissipation total 0.0399 J/K (2.8 % low, FAIL at 2 %); per cycle 3.64e-6 passes at 2 %; A/octet ratio 1.682 (1.9 % from 1.714, passes). Both variants are printed; the S = 0 version reproduces the spec.
b. **R28, which lattice's S goes with which c.** Not stated. Implemented: all lattices (octet, BCC, A) with all three c values at H_L = H_2; the partner x dT table uses octet S and c = 1. "Not elastic" is flagged where K_n c E_s eps_m > 250 MPa (106 of 360 partner x dT x K_n x c cells over all c values; asterisks in the c = 1 table).
c. **R28, c_BCC definition.** Taken as sigma_peak/(E_s eps_m) from R7 (equibiaxial, Euler-Bernoulli): 0.676, 0.943, 1.286 at rho 0.1, 0.2, 0.4.
d. **R30, Goodman mean stress.** Implemented as sigma_ar = sigma_a,loc/(1 - sigma_m/sigma_u) with sigma_m = min(sigma_y, E_s dalpha dT_ref) and no K_n or c on the mean. UNSURE reading. Result (Ti, K_n = 3, c = 1, b = -0.1434): dT_x = 45.9 K for dT_ref = 300 K (below 50 K, consistent with the spec's "possibly < 50 K"); 122.5 K without mean.
e. **R30, elastic flag.** The spec flags only the K_n = 1 case (dT_x = 367 K). By the same criterion (K_n c E_s eps_m > sigma_y) the K_n = 3 value dT_x = 122 K is also not elastic: the local amplitude at N = 10 958 is 159.5 MPa in both cases, and K_n c E_s eps_m = 319 MPa. The output marks it NOT-ELASTIC.
f. **R30, partners with dT_x beyond the sweep.** dT_x > 500 K (the 1-500 K bisection does not bracket) for steel (K_n = 1, b = -0.1434), and for 316L and Cu (K_n = 1, both b). Flagged in the output.
g. **R22, kappa.** Circular-section bending kappa used for A and B (B also carries an axial stress share that kappa ignores); kappa = 1 for C [100]. The spec says "kappa from R5" without naming the section.
h. **R25.** Limits on sigma_a from collapse and first yield applied to sigma_max are read as sigma_a <= (1-R)/2 x limit. Goodman and Morrow applied to the local amplitude with sigma_m,loc = m sigma_a,loc, m = (1+R)/(1-R). R = 10 is flagged, with no mean-stress factor; its limits on |sigma_min| use (R-1)/(2R).
i. **R27.** Goodman variant computed for AlSi10Mg only; the inputs table has no sigma_u for Ti-6Al-4V (flag). The R = 0.1 basis is read as (2/(1-R)) x amplitude ratio, with sigma_w replaced by sigma_w/(1+m sigma_w/sigma_u) for Goodman.
j. **R24.** Central b = -0.1434 (as-built). sigma_a,max is taken at N = 1e7 and S at 1 Hz, tau_s = 20 y, K_n = 1, for A, B and C [100]. The `sy` and `Es` ranges are applied through the topology function, so E* for B and k_peak for A with f move consistently.
k. **R14.** b = -0.10 is used for the spec's N_x and sigma_f' figures although it is not in the b set {-0.07, -0.095, -0.1434, -0.20}; computed in addition.
l. **R16.** The 1 MPa and 2 MPa rows are labelled "fixed amplitude (not a topology pair)", not "inconsistent pair". Only the off-diagonal cells of the central-amplitude x E_eff block carry that label.
m. **R6 trap check.** The axial force was kept as instructed. As an extra check, the variant that sets Delta.n = 0 and uses only the transverse force k_t*Delta_t gives a modulus low by exactly 1.5000, matching the planner's note. Setting k_a = 0 instead (a different, wrong variant) gives zero stiffness.

## 4. Findings that differ from the spec's expectation

a. **R14, B is not rho-independent.** The fatigue/collapse ratio for B varies from 0.1387 to 0.1331 (4.1 %) over rho 0.05-0.5 because k_peak carries the axial 1/rho term. A, C [100] and C [110] are exactly independent.
b. **R12.** "Yield governs over the whole sweep" holds for rho >= 0.05 (main sweep, PASS). With the 0.01-0.04 extension C buckles first for rho < 0.0386 (D2 already says yield governs only for rho >= 0.05). A never buckles first (crossover rho = 4.6e-4).
c. **R14 sweep coverage.** The crossover N_x lies outside the N grid 1e2-1e10 for 45 of 60 (b, sigma_w7, K_n) combinations (for example b = -0.07 gives N_x < 1 cycle even at K_n = 1). The sweep brackets it for the central case (476 cycles; spec 475) but not for most of the grid.
d. **R22 range.** Computed 0.353-12.0 against the spec's "about 0.2-6". The maximum 12.0 is C [100] at n_d = 3, sigma_ref = 5 MPa; A and B alone give 0.353-5.94, which matches the upper figure. The minimum 0.353 (A, n_d = 3, sigma_ref = 60 MPa) is above 0.2.
e. **R23.** Maximum psi_TE = 1.21e-2 is 2.42 x the assumed 5e-3, and psi_TE/5e-3 at 1 Hz reaches 1.31 for t = 5 mm (k = 130; 1.62 for k = 100). Thermoelastic damping exceeds the assumed psi at the thick-strut end of the grid. At 1/86 400 Hz psi_TE < 2e-7 everywhere.
f. **R24.** sigma_y has no effect on sigma_a,max or S_max over 200-280 MPa (fatigue binds throughout); E_s, psi and b have no effect on sigma_a,max at N = 1e7 (anchored). Ranking by effect on S_max (A, B, C [100] alike except f): K_n (16x), psi (10x), sigma_w7 (6.25x), b (2.94x between -0.07 and -0.20), f (A only, 0.78), E_s (0.87), sigma_y (none).
g. **R6/R7 Timoshenko.** Timoshenko shear lowers C1 by 1.1 % at rho 0.02, 9.6 % at 0.2, 20.6 % at 0.5. The equibiaxial crossover (sigma_peak = E_s eps_m) moves from 0.2267 (Euler-Bernoulli, inside the spec's 0.19-0.23) to 0.3093 (Timoshenko, outside it).
h. **R29 at H_L/H_2 = 10.** S reaches about 0.93 (A, rho 0.4, Ti), so "1/(1+S) >= 0.91" holds only at H_L = H_2.

## 5. Sweep brackets checked

- R7 crossover bisection: f(0.02) = -0.698, f(0.6) = +0.514, bracketed.
- R19: all 36 (topology x nu x b x tau_s) maxima are interior to the grid and below first yield; the grid maximum matches the analytic location and value within 0.4 %. No widening needed.
- R12: the C crossover rho 0.0386 lies inside the 0.01-0.05 extension.
- R14 N_x: not bracketed for most parameter combinations (see 4c).
- R30 dT_x: not bracketed (> 500 K) for the cases in 3f.
