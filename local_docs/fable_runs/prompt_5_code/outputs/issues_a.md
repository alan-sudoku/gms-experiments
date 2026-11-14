# Issues, group A (rows A1-A4, B1-B3, C1-C4, D1-D3, E1). Level of everything: derived (unverified).

## Failed checks

1. **D1, spec-literal check FAIL.** Tafel Delta-eta = b*log10(kappa/r) versus the full Butler-Volmer root: for eta_s > 100 mV the maximum deviation is 104 mV (script output `d1_overpotential.txt`). Cause: with R_f,g/R_f,s = r > kappa the candidate's own overpotential falls below 100 mV (Tafel not valid for g), so the spec condition "eta_s > 100 mV" is insufficient. Restricted to cases with Tafel price > 0 (kappa/r > 1) the maximum is 0.64 mV. Requiring both eta_s and eta_g > 100 mV the maximum is 2.35 mV (worst case: T = 353.15 K, alpha = 0.5, j = 5e3 A/m2, j0_s = 10 A/m2, r = 100, kappa = 1, eta_g = 100.3 mV), 0.35 mV over the 2 mV tolerance. Not resolved; the spec's tolerance statement needs a condition on both overpotentials, and a threshold above 100 mV for alpha = 0.5.
2. **D1, spec ambiguity on alpha > 1.** The row writes the cathodic exponent as -(1-alpha)F eta/RT. For alpha = 1.5 and 2 this becomes a positive exponent subtracted from the anodic term (alpha_c negative). The script follows the formula literally; it is harmless for eta > 0 above 100 mV but unphysical in general. Plan section D6 writes separate alpha_a and alpha_c. Not resolved.
3. **A4 independent check as stated is false in general.** "D = (J/J*)^2 must exceed 1 wherever Al loses". At the crossover D = (1-x)/(sigma_Cu/sigma_Al - 1), x = e_g*rho_g/(e_s*rho_s), so D > 1 only for x < 0.362. Results: MEMORY 20/55: D = 1.40 (holds); ICE 29.0 vs 57: 1.33 (holds); Nuss old-scrap 23.8 vs 59.3: 1.38 (holds); Nuss secondary/secondary 23.8 vs 28.1: 1.17 (holds); ICE recycled/recycled 29.0 vs 16.5: 0.74 (FAIL; Al loses for 0.74 < D < 1); Nuss primary/primary 194 vs 59.3: 0.022 (FAIL). Not resolved.
4. **A4 expectation "no crossover with primary Al" fails for the Nuss primary pair** (e_Al = 194, e_Cu = 59.3 MJ/kg): e*rho is Al 5.24e11 < Cu 5.31e11 J/m3, so a crossover exists at (J^2 tau)* = 6.8e17 A2 s/m4 (tau = 6.8e5 s at 1 A/mm2). It holds for the MEMORY pair (200/55) and the ICE primary pair (218/57). The result depends on which source is used for e.

## Deviations from the spec

5. **A2 bracket.** The spec bracket A in [1e-7, 1] m2 is too narrow: the optimum lies outside it (large I with small e, or the reverse) in 19 of the runs. The script detects a bound hit and reruns on [1e-12, 1e6] m2, minimising over ln A. All reported agreement (1e-6) is with that widened rerun where needed.
6. **B2 minimiser.** A plain bounded `minimize_scalar` on [0.1, 10] returns a local minimum (xi = 7.854, F/xi = 1.0000), because F/xi is not unimodal (it oscillates about 1 at large xi). The global minimum (xi = pi/2, F/xi = 0.91715) is found only by first bracketing with a coarse scan. The spec says the interval "brackets the minimum"; it contains it, but a bracket-free minimiser does not find it.
7. **C4 deficits.** The spec says "the Row C1 deficits (6% and 29%)". I read 6.3% as 1 - 0.937 (Al 200 at baseline) and 29.3% as 1 - sqrt(0.5) (thick limit for k 200/400), modelled as a reduction of h*A*eta_f. NTU uses A = fin surface only (2*H*L_f*N), as written in the spec; the base area between fins is left out. These readings are mine, not the spec's.
8. **C4 laminar validity.** For V above about 1e-2 m3/s the channel Reynolds number exceeds 2300 and the laminar formulas (Nu = 7.54, dP = 12 mu L U/b^2) no longer apply; those rows are printed but marked. For the 29% deficit, flow compensation is possible only for NTU0 of order 1 or larger and costs a P ratio of 1.4 at V0 = 3e-3 m3/s and about 200 at V0 = 1e-2 m3/s; for V0 >= 3e-2 it is "not compensable by flow".
9. **D2 geometry.** Metal-foam a = 5e3-1e4 m2/m3 (MEMORY UNSURE) lies at or below the lower edge of the spec sweep a in [1e4, 1e8]; at a = 5e3 L/lambda only reaches 0.004-1.35 at L = 3 mm. The FD route computes the current from flux balance, -phi'(0) = (1/lambda^2) times the integral of phi, because the one-sided derivative on a graded mesh lost accuracy; phi itself is the FD solution, so the check is still independent of the tanh formula.
10. **E1 range.** The spec asks for phi in [0.02, 1]; I added w = 1 and 2 (phi = 0.0029, 0.011) for the phi -> 0 limit. At phi <= 0.05 the deviation from phi/3 is 13.9% at phi = 0.043 (limit 15%; the margin is small). Struts of 1-2 voxels are discretisation-limited at N = 32.

## Findings that contradict the plan's wording (not check failures)

11. **B3 is not monotonic.** R_ac,Al/R_ac,Cu does not go from 1.638 to 1.280 monotonically: it dips to 1.2158 at t/delta_Cu = 4.72 (below the thick-limit value 1.280) before returning to 1.280. Limits 1.638 and 1.280 both reproduced (FD and closed form agree to 7e-5). The sweep brackets the transition.
12. **A3 lookups, outside the planner ranges.** Nuss and Eckelman secondary copper (refinery, 28.1 MJ/kg) is above the range 10-20; Nuss secondary Al from new scrap (8.3) is below 10-30. All other values fall inside (table below).

## Identity or true-by-construction checks (labelled "identity" in the outputs)

- A1: expected 1.64 and 0.49 are the plan's hand arithmetic of the same formula (restatement). The IEC 60228 check is independent.
- A2: "embodied term = operating term at the optimum" follows from the same stationarity; it checks the minimiser, not the physics. Ratio independence of I, L, tau holds by algebra and the check only guards against a coding error.
- A3: the 1.34 and 0.70 expected ratios are the same formula as the code; the root check compares brentq on the numerical minimiser with algebra.
- B1: the six delta_Al/delta_Cu = 1.28 checks are the same expression sqrt(sigma_Cu/sigma_Al) at every frequency.
- C1: the thick-limit check compares the same formula in its asymptote; solve_bvp is the independent route (max deviation 6e-10 from a deliberately wrong initial guess).
- C2/C3: break-even "2.2", 1.66 and 1.08 restate the formula; the independent element is the numerical mass ratio from the optimised fin (agreement 1e-10).
- C4: (a) exponent 3.4375 and (c) exponent -3.00 follow from the coded power laws and from dP = 12 mu L U/b^2 with U = V/(N b H); the limit checks R_th -> 1/(mdot cp) and -> 1/(hA eta) are limits of the same expression.
- D2: thin and thick limits are the same closed form in two regimes; the FD route is independent.

## Sweep bracketing

- A3: sweep r in [0.2, 10] brackets the crossover (f = -0.686 at 0.2, +1.222 at 10); root 2.0254.
- A4: for each case with a crossover, tau in [1e5, 1e9] s brackets it at only 34-39 of 41 J values (J from 0.1 to 10 A/mm2); at low J the crossover tau exceeds 1e9 s. Where e_g*rho_g >= e_s*rho_s there is no crossover and none is bracketed.
- B2: [0.1, 10] contains the minimum but is not unimodal (item 6).
- B3: brackets the transition (ratio 1.638 at the low end, 1.280 at the high end).
- C1: sweep (25^3 points) covers mL_Cu from 0.014 to 35 and brackets both the <= 5% penalty region and the thick limit. The thick limit is only approached at mL_Cu > 20 (0.4% of points). The spec's own sweep ranges never reach mL ~ 1e3.
- C2: k_g in [80, 240] brackets the mass crossover (+0.507 at 80, -0.498 at 240); beta, C are insensitive to the sweep.
- C3: e_g/e_s in [0.2, 10] brackets both break-evens.
- C4: V0 in [1e-4, 1e-1] m3/s gives NTU0 from 78 to 0.078: brackets NTU >> 1 and NTU << 1 (NTU << 1 only at the top end: 0.078).
- D1: kappa in [1, 1e6] brackets the Tafel regime; eta_s <= 100 mV occurs in 700 of 6400 cases.
- D2: L/lambda from 2e-6 to 191 brackets thin and thick.
- D3: the sweep spans 0.09 uV to 13.9 V and brackets 30-360 mV; 13.8% of points exceed 30 mV (not at the central duty: that needs m'' > 18 mg/cm2).
- E1: the phi grid spans 0.003-1, with current conservation 1e-12.

## Published values: confirmed or only taken from the plan

- IEC 60228:2004 Table 2 (Cu and Al class 2 maximum DC resistance): confirmed from the publisher preview PDF (primary, section "Table 2").
- Embodied energy, ICE v2.0 summary tables and Nuss and Eckelman 2014 SI Table S38 (CED column): confirmed from the source files (raw copies in `data/raw/`). The column identification (first triple = CED MJ/kg) was checked against the Al and Cu totals and the Pt GWP.
- Incropera Table A.4 air 300 K: confirmed from a scanned appendix (page 911, edition not stated).
- Gilliam et al. 2007 KOH correlation: NOT read from the paper (paywalled). Coefficients taken from web-search summaries of citing works (Julich critical analysis; ACS SI Table S1 values C = 0.005332, E = 0.001043); they reproduce the 2.43 mS/cm at 0.01 M, 25 C quoted in the same summary. Status PARTIALLY confirmed. T in the formula is in K by the summary; a version with t in degrees C was also mentioned and not examined. The molarity of 30 wt% KOH at 80 C (6.7-6.9 M) uses MEMORY densities, UNSURE; the result is insensitive (138.1 vs 138.6 S/m).
- C2 beta = 1.4192: confirmed only from two secondary sources (a lecture deck and a J. Mech. Eng. paper found by search; tanh(1.4192) = 0.8894 quoted there); Schmidt 1926 and Kraus, Aziz and Welty 2001 not accessed. C = 0.504: not confirmed from a source; computed as beta/(4 tanh^3 beta) = 0.50425.
- B1 skin depths (9.35, 8.5, 12.0 mm), D3 HHV of hydrogen 141.8 MJ/kg, D1 59.16 mV: taken from the plan or textbook memory, not confirmed from a source in this run.
- Embodied energy is cumulative energy demand (ICE v2.0: "embodied energy"; Nuss: CED), not embodied exergy destroyed; the framework's definition of Sigma_init is UNSURE (planner's flag stands).

## LOOKUP values against the planner's UNSURE ranges

| Quantity | Value (source) | Planner range | Inside |
|---|---|---|---|
| primary Al, MJ/kg | 218 (ICE v2.0 virgin), 194 (Nuss primary) | 150-220 | yes, yes |
| secondary Al | 29.0 (ICE recycled), 23.8 (Nuss old scrap), 8.3 (Nuss new scrap) | 10-30 | yes, yes, no (below) |
| primary Cu | 57.0 (ICE virgin), 59.3 (Nuss, from Mo), 42.0 (ICE EU tube and sheet), 53.7 (Nuss supply-weighted) | 35-75 | yes |
| secondary Cu | 16.5 (ICE recycled), 28.1 (Nuss refinery), 1.8 (Nuss electronic scrap) | 10-20 | yes, no (above), no (below) |
| Pt, MJ/kg | 243 000 (Nuss total; 95%: 178 000-326 000) | 1e5-3e5 | yes |
| Ir, MJ/kg | 169 000 (Nuss total; 95%: 128 000-219 000) | same order | yes |
| KOH 30 wt% 80 C | 138.1-138.6 S/m (Gilliam, partial) | 120-150 | yes |
| air 300 K | rho 1.1614, mu 1.846e-5, k 0.0263, cp 1007, Pr 0.707 (Incropera Table A.4) | MEMORY rho 1.177 | rho differs by 1.3% |
| IEC 60228 Al/Cu resistance ratio | 1.651-1.683 over 17 sizes | 1.6-1.7 | yes |
