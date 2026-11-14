# Issues, all rows (merged)

This file merges the three group issue files (`issues_a.md`, `issues_b.md`, `issues_c.md`, left in place, copied verbatim below) and adds the issues of row J1 (the gate test matrix, `j1_gate_matrix.py`, output `j1_gate_matrix.txt`). Level of everything: `derived` (unverified). Section headings inside the group files are kept as they were, so they sit one level below the group titles here only by position.

## Group A (rows A–E)

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

## Group B (rows F, N)

# Issues, group B (rows F1-F7, N1-N6). All results are level `derived`.

## Failed checks against the spec or the planner's UNSURE values
1. **F2 upper crossing of W/C = 2**: 7.58 MeV (found by brentq on the log-log interpolated XCOM table), the plan expects about 6 MeV (+-10%). Fails by +26%. Lower crossing 0.403 MeV passes.
2. **F2 minimum value of W/C**: 0.9654 at 1.5 MeV; plan UNSURE range 0.98-1.05. Fails. Minimum energy 1.5 MeV passes. Ratio at 10 MeV (2.42) passes. The interpolated minimum sits on a table vertex (1.5 MeV), so its energy is only as good as the grid (neighbours: 1.25 MeV 0.980, 2 MeV 0.998).
3. **N2 B-10 RI**: 1733.1 b against the UNSURE range 1720-1730 b (0.2% above). The spec check (B-10 ratio to 0.45*sigma0 within 0.95-1.05) passes (1.0045); only the UNSURE range misses.
4. **N1 Gd-157 thermal (Sears 1992)**: 259 000 b, outside the UNSURE range 253 000-255 000 b. ENDF/B-VII.1 gives 253 550 b (inside).
5. **F2 sweep bracketing, W/Fe**: the 0.03-20 MeV range does not bracket the upper crossing of 2 (ratio at 20 MeV is 1.83). Extra run to 100 MeV puts it at 55.7 MeV. The other four W/X sweeps bracket both crossings and the minimum.

## Lookups not available or substituted (deviations)
6. **N1 sources**: the Mughabghab Atlas (2006 or 2018), INDC(NDS)-440, ENDF/B-VIII.0 summaries and JENDL-5 were not reachable as text. Substitutes, all recorded in the data headers:
   - thermal sigma_a at 2200 m/s: Sears 1992 Table 1 (NIST NCNR web copy) is the primary value here (spec called for it only as cross-check);
   - resonance integral: **I computed it** from reconstructed pointwise ENDF/B-VII.1 (not VIII.0) cross sections downloaded from NNDC Sigma, as the integral of (n,gamma)+(n,p)+(n,t)+(n,alpha) over dE/E from 0.5 eV to 20 MeV; natural-element RI = abundance-weighted isotope sum (Sears abundances). This is not a tabulated RI. Upper limit convention (20 MeV versus infinity or 100 keV) is not stated in the spec; both 20 MeV and 100 keV are printed. For C, Al and Fe the 20 MeV integral is inflated by MeV threshold reactions (for C 0.092 b against 0.0018 b at 100 keV); for the nuclides used in the claims the two agree to under 1%.
   - ENDF/B-VII.1 thermal values were printed beside Sears: nat C differs by 10% (0.00386 against 0.0035 b), nat Dy by 5%, others within 4%.
7. **N6 crustal abundance**: the CRC Handbook table is not reachable. Per the run rules the row uses the planner's values, labelled "NOT A LOOKUP". A Wikipedia reproduction of CRC column C1 (secondary, UNSURE edition) is stored as `data/crust_abundance_secondary.csv` for comparison only; it equals the planner's values for all 18 elements that have both. The planner has no value for C, Ni, Sm, Eu, Bi. The two sets are not independent (the planner's values look like the CRC numbers). G3.9 check passes in both (B/Gd = 1.6 is the narrowest margin).
8. **N6 production**: USGS MCS 2026 (data year 2025e) used. No world total exists for B (USGS says it cannot be calculated), Ir, Hf, Gd, Dy, Eu, Sm, Nd individually (rare earths only as a total, 390 000 t REO). The Ir, Hf and rare-earth rows therefore have no production number. The values in `data/usgs_mcs2026_world_production.csv` were transcribed by hand from the PDFs.
9. **N5**: Lamarsh and Baratta 2001 not reachable. L = 2.85 cm and D = 0.16 cm for H2O were taken from LLNL/NCSP "Hand Calculation Methods for Nuclear Criticality Safety" Table 2-2 (textbook origin not stated, UNSURE). That table has no Sigma_a column, so Sigma_a = D/L^2 = 0.0197 /cm is derived.
10. **N4**: the published collision counts (18, 25, 115) were taken from the spec; the book was not consulted.
11. **F6 check (iv)** (ANSI/ANS-6.4.3-1991 exposure buildup factors, Shultis and Faw): NOT RUN. The tables are not available online in a form I could read (standard behind a paywall; RSICC DLC-129 and a UNLV thesis exist but were not retrieved). G3.4's buildup number therefore stays low confidence.
12. **XCOM version**: the XCOM result pages do not print a version number. The files say "UNSURE: 3.1". NISTIR 5632 pages (Table 3, Table 4) do not state an edition either; recorded as "UNSURE v1.4". The NISTIR 5632 element totals and XCOM totals agree to the table's rounding (4 digits).
13. **Atomic weights** (N3, N5): taken from the NIST/IUPAC table; for interval elements (B 10.8135, C 12.0106, H) the midpoint is used.

## Spec ambiguities
14. **F3 lattice relative density**: the spec does not say whether the relative density {0.1, 0.3, 0.5} refers to 1.70 or 2.26 g/cm3. Both were run; the ranking does not depend on it.
15. **F1 Klein-Nishina check**: the spec says the closed formula must reproduce carbon's tabulated value within 2% at 0.5 and 1 MeV, which passes (-0.18%, -0.13%). At 0.1 MeV it is -2.1% against the total with coherent scattering (+1.1% against XCOM incoherent) and at 5 MeV -8% (pair production not in KN). These are not spec checks.
16. **F6 mu**: free-electron KN plus XCOM photoelectric differs from XCOM total-without-coherent by +1.10% for W at 0.5 MeV (+0.51% for W at 1 MeV, under 0.1% for C). Binding in the XCOM incoherent term causes it. The spec prescribes KN, so the spec value was used. Printed as info only.
17. **F6 statistics**: 1e6 histories per case (the spec value); the whole run took about 85 s, so no reduction was needed. Fixed seed 20261114 (SeedSequence per case). Statistical error of x_C/x_W at 1 MeV is about 0.003-0.006 (1 sigma, from shifting ln T_E at the root; approximate). x_C/x_W at 1 MeV is 1.163 (T_E=1e-2) and 1.144 (T_E=1e-3), inside the UNSURE 1.1-1.4. At 0.5 MeV it is 1.96 and 1.88. Coherent scattering, fluorescence (W K x-rays) and electron transport are neglected, as the note says; results are energy buildup of a 1D infinite slab, not an exposure buildup.
18. **N5**: the Cd sheet uses sigma at 2200 m/s for a beam while water uses the diffusion asymptote exp(-x/L); the plan calls the row order-of-magnitude. Ratios found: 38.4 (areal mass) and 333 (thickness) with Sears sigma; 37.3 and 323 with ENDF thermal sigma.
19. **G3.5 wider set (F7)**: the Sn/W/Pb ranking at 60, 80, 100 keV matches the claim. When Bi, Gd, Ba are included they lead at 40 keV (Ba), 60 keV (Gd), 100 keV (Bi); only at 80 keV W leads. The claim names only Sn, W, Pb, so it is not falsified.

## Identity and by-construction checks (flagged, not counted as evidence)
- **F3** "energy of minimum equals the F2 minimum energy": the thickness ratio is a constant multiple of the mass ratio, so true by construction (labelled identity in output). The lattice trend "all values >= solid case" is also by construction (1/rel scaling).
- **F6 (ii)** energy balance T+R+A = 1: tallies sum from the same deposits and exits, so it holds to rounding (9e-16) unless photons are lost or duplicated; bookkeeping only.
- **F1, F7 "XCOM vs NISTIR 5632 Table 3"**: two downloads of the same NIST evaluation; this only tests transcription, not physics.
- **N1 isotopic checks** (nat B, Cd, Gd from isotopes): Sears isotope values against Sears natural-element values, not fully independent. They pass (-0.50%, -0.11%, -0.25%).
- **N4 gain factors** compared with the plan's rounded numbers are arithmetic ties.

## Sweep bracketing statements
- F2: W/C, W/Al, W/water, W/concrete: bracket both crossings of 2 and the minimum. W/Fe: does not (item 5).
- F5: a = mu*x-bar in [0.1, 10]; ratio >= 1 everywhere (smallest margin 1.0003 at q = 0.95, a = 0.1).
- F6: mu*x in 0.5-12 brackets both T_E targets (1e-2 and 1e-3) for all four (material, energy) cases.
- N3: tau in [1e-3, 1e2] brackets f = 0.9 (tau = 0.0511) and f = 0.5 (tau = 0.636).

## Group C (rows H, M, P, T)

# Issues, group C (H1-H3, M1-M5, P1, T1). Level: derived (unverified).

## Unavailable or substituted lookups (all rows below carry this flag)
1. H1: Linden and Reddy 2002 Table 1.2 not readable (book). The 1 470 Wh/kg check is against an unverified reference, so it is NOT a lookup. Web snippets of secondary pages gave 1 470 and 1 500 Wh/kg (and one page 2 567); none recorded. Computed 1 473 Wh/kg. Atomic masses were typed from memory (UNSURE), not read from the IUPAC table.
2. M1/M2/M3: Coey 2011, Coey 2010, Skomski and Coey 2016 Table 1 not readable (paywalled; only abstract pages seen). Substitute: Granados-Miralles et al., arXiv:2310.02106, Table 1 (secondary review, which cites its own reference [34], not identified). It gives room-temperature Bs (taken as mu0*Ms, UNSURE) and K1. All planner UNSURE ranges for mu0Ms are met (Fe65Co35 2.45 at the top of 2.43-2.45; SmCo5 1.07 in 1.05-1.14). K1 values equal planner's expected values (Nd 4.9, SmCo5 17.2, BaM 0.33, Fe 0.048). Fe65Co35 K1 in the source is 0.018 MJ/m3 (not in spec).
3. M2: Co is not in the readable table. Co kappa_h uses planner endpoints (0.41-0.53 MJ/m3) and mu0Ms=1.82 T from memory (UNSURE); labelled "not a lookup"; the check is circular and not scored. The "published" kappa_h values (Nd 1.54, SmCo5 4.3-4.4, Ba 1.35, Fe 0.12) are the planner's, not read; they may derive from the same K1 and Ms, so agreement is weak evidence. Fe: 0.114 vs 0.12 is -4.8%, outside 3% (FAIL as scored). Either the planner's 0.12 is rounded or uses a different Ms/K1.
4. M3: Skomski et al. 2010 (J. Appl. Phys. 107, 09A739) not read. Whether it states mu0Ms^2/12 is UNKNOWN.
5. M4: Skomski and Coey 1993 not read; the 1 090 kJ/m3 "published" value is the spec's memory. The formulas reproduce 1 091 kJ/m3 from the MEMORY inputs, but the inputs may have been chosen to give that value: agreement is not independent. A for Sm2Fe17N3 is not given; 8 pJ/m (Nd2Fe14B value) reused for the wall width (Sm: 2.57 nm, no check specified).
6. P1: Incropera Table A.6 not readable. Substitute: Cengel and Cimbala 2014, Fluid Mechanics, 3rd ed., Table A-3, row 60 C (rho 983.3, sigma 0.0662, hfg 2 359 kJ/kg, mu 0.467e-3). All four inside the planner ranges. Reay, Kew and McGlen 2014 not readable: the worked-example reproduction (within 20%) was NOT performed.
7. T1: Ellmer 2012 not readable (paywalled; abstract page only). The film values are the planner's UNSURE endpoints (best/mid/worst), not a lookup. The In mass fraction 0.74 and film density 7 140 are MEMORY UNSURE.
8. H3: input ranges are MEMORY UNSURE; Christen and Carlen 2000 not read. Model B (E_d = P t/(1+P t/E)) is my reading of "matched-load form, half energy at t=E/P_max"; not verified against the paper.

## Spec ambiguities
- H1 "0.26 eV" expected value: LiCoO2 + 3C with n=0.5 on the reactant basis (6 atoms) gives 0.308; LiFePO4 + 6C (13 atoms) gives 0.254. Neither is within 2% of 0.26 (LiFePO4 is -2.3%). The atom basis for the LiCoO2 cell is not defined in the spec (half-lithiation could imply a different formula unit). Both scored FAIL against 0.26; not resolved.
- H1: Pb + PbO2 + 2H2SO4 per-atom value (0.228) and the "no per-atom expected value" for it are not in the spec.
- H2: the expected values 0.0016, 0.011, 0.062, 0.14 are 2 significant figures; 1% tolerance fails by rounding for 0.0016 (0.00156), 0.011 (0.01134) and 0.14 (0.1373). Computed values agree with the planner's to the rounding.
- H3: 16-corner sweep shows A/B ratio up to 2.46 (limit "factor 2"): FAIL at some corners. Central case 1.14. t* (Model A) 4.8-96 s over the corners, inside 1-1 000 s; sweep [0.1, 1e4] s brackets t* at all corners.
- P1: A_e (evaporator/condenser area) and A_x (cross-section for k_eff) are not defined in the spec; used pi*OD*L_e and pi*OD^2/4. k_eff = L_eff/(A_x R_total) is independent of Q, K and r_eff; the K, r_eff sweep therefore only varies Q_max and not the wall share or k_eff (the sweep brackets only the 10-100 W window). Wall share depends strongly on the wick: 10.7% at k_wick=40 but 23% at 100 and 37.5% at 200 W/mK (above 20% from about k_wick=90); with k_wall=16, 60%. Axial wall conduction, vapour pressure drop and gravity are neglected (spec).
- T1: FoM T^10/R_s grows linearly in t at fixed f, so no interior optimum in t: the maximum is at the upper edge (2 um) and is set by process limits (not supplied). Optimum f is 1/21 for any t (minimize_scalar on [0.005, 0.2] brackets it). Mesh T=(1-f)^2 ignores diffraction and haze. R_s = 1/(sigma t f) counts the conductance of one set of lines, but mass uses both sets (2f-f^2). Minimum line width (process input) not provided; not reported as a number. Result: 97% (Cu) and 92.5% (Al) of the sweep exceed the best film FoM (0.070), so the G2.8 falsifier does not trigger, but the film side is not a lookup.
- M5: optimiser vs formula agree to 1e-14. This is close to an identity: with Bm fixed by the constraint, V_m = Bg*Ag*Hg*lg/|Bm Hm| exactly; the only non-trivial content is that the minimum is at Bm = Br/2. Same ideal-iron, no-leakage model, so it does not test leakage or fringing. HcJ (UNSURE) comfortably exceeds the operating |Hm| for NdFeB (512 vs >=900 kA/m) and ferrite (155 vs 250-400 kA/m).
- M3: the 2 000 x 2 000 grid maximum vs the analytic optimum of the same function is a numerical consistency check, not evidence for the shape-anisotropy model (planner's derivation). Grid max is 1/12 to better than 1e-6; grid p resolution ~5e-4. The p<=0.5 restricted maximum (1/16) is at the bracket edge by construction.

## Identity-labelled checks
- T1: "limit w/p -> 1 gives R_s = 1/(sigma t)" (same formula).
- H3: "t* = E_c/P_b" (root of the same model vs its closed form); "limit t = 1e4: ratio = E_b/E_c" (both curves saturated at their E, true by construction).
- M5: optimiser vs formula (see above).
- M3: grid vs analytic (see above).
- M1: "realised below ceiling" with realised upper endpoints from MEMORY; Alnico 5/9 are compared with the AlNiCo5 Bs (no Alnico 9 Ms read), and the Alnico5 shape-anisotropy ceiling mu0Ms^2/4 is far above realised values (0.11, 0.22), so the check is weak.

## Failed checks (as scored)
H1 0.26 eV (both cells), H2 rounding (3 values), H3 A/B within factor 2 at some corners, M2 Fe kappa_h (-4.8% vs 3%).

## Brackets
H3 t*: bracketed at all 16 corners. M3: grid and bracket [0.5,1] contain p=2/3. T1: f bracket contains 1/21. P1: sweeps bracket only 10-100 W (no crossover in this row). M5: no sweep root; BH sweep 10-450 kJ/m3 spans ferrite to NdFeB.

## Row J1

Result: 13 of 18 cases match (1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 15, 18). Five are undecided because an input is missing, so they count as MISMATCH against the expected class: 4, 8, 14, 16, 17. No case decided to a class opposite to the expected one. Expected outcomes and the gate were not changed.

### Missing inputs (G4.2 says a case that needs one falsifies the claim)

- Case 4: no envelope slack and no binding basis (per atom, mass or area) in the case text. Blocks step 3. kappa per atom: Cd/Al 1.09e4, Cd/C 7.2e5, nat B/Al 3.3e3, nat B/C 2.2e5, B-10/Al 1.7e4, B-10/C 1.1e6. The expected "kappa >= 1e4" does not hold for natural boron against Al (3.3e3). Class I holds for any slack below these values.
- Case 8: (a) the case does not say which device is g; (b) no row produced a 1e6-cycle life for either device, so step 2 cannot be completed. Step 3 would pass for g = double layer (kappa = 0.347 at 5 s, central H3 inputs; 0.05 to 1.04 over the 16 corners, so one corner is above 1).
- Case 14: the incumbent's temperature margin (the slack of "carry I within the temperature limit") is not supplied. Blocks step 3. kappa = 1.638 (A1). Class II only if the incumbent runs below 61% of its allowed rise. A4 is a step-5 comparison and supplies no margin.
- Case 16: no envelope slack for the heat sink (allowed resistance rise, fin mass or height). Blocks step 3. kappa = 2.0, n = 1/2 gives 1.414; the C1 same-geometry price is 1.067; both exceed 1.
- Case 17: no row produced the Pourbaix datum (stability of Ni–Fe oxide in acid at the OER potential). Blocks step 2. The plan listed a LOOKUP but no row carried it.

### Gate wording ambiguities

1. Unstated envelope. Step 1 says "if the binding envelope cannot be stated: out of scope". Read literally, every case without a stated cap (4, 6, 8, 12, 14, 16, 17) exits at step 1. I did not read it that way (that would make cases 12 and 17 out of scope, contradicting their expected Class I). Rule used: a cap the case does not state is "slack not supplied" and blocks step 3 only when the price exceeds 1. The cost: cases 4, 14, 16 are undecided. Reading "no cap" as uncapped gives Class II for 4, 14, 16; reading it as slack 1 gives Class I.
2. Slack of 1 or more. The gate does not say slack >= 1. I used it (the incumbent fits its own cap). It decides cases 6 (n = 0) and 8 (price < 1). Without it, both would be undecided.
3. "Free" caps. Cases 5, 11, 13 state one quantity free (thickness, volume, cross-section). I read that as no binding cap (slack inf). If mass (cases 5, 11) were capped at the incumbent's usage, both would be Class I (areal-mass ratio 38.4; ferrite mass ratio 7.08).
4. Step 2 versus step 3 for the stoichiometric bound (case 7). The gate puts "required specific energy against the stoichiometric bound of g" in step 2; the expected text says "step 3; stoichiometric bound". With the carbon-only geometric ceiling (140 Wh/kg at 2.7 V) against a required 100 Wh/kg, step 2 passes (and the bound excludes electrolyte, so a pass is weak). Step 3 on practical values (kappa 33 against slack 2) decides Class I. On the ceiling basis kappa is 2.76 at 2.7 V (Class I) and 1.26 at 4.0 V (Class II). The result depends on c_g (practical or ceiling) and on the voltage. The gate does not say which.
5. Case 9. Step 1 clause 3 ("cannot operate in the same environment and the function cannot be restated") does not trigger, because the environments are the same and G3.11 restates the function. Step 2 then fails if "stoichiometric bound of g" is read as the stored energy as manufactured (0). If it is read as the charged-state ceiling, step 2 passes and step 3 gives kappa = inf, still Class I. Out of scope at step 1 only if the restated function is judged impossible. The gate text does not make this unambiguous, and the clause "stoichiometric bound" is undefined for a capacitor.
6. Case 17. Step 1 clause 3 (g and s cannot share the environment) and step 2 (chemical stability window) overlap. In the literal order, an unstable Ni–Fe exits at step 1 as out of scope, not at step 2 as Class I. Same overlap as case 9.
7. Choice of n (cases 4, 6, 16). Step 3 gives n = 1/2 for "thick against fin length" and does not say what applies to a short fin (mL about 0.5, case 16) or a thin sheet (case 4). A black sheet (n = 0) would pass; a short fin is between 0 and 1/2.
8. Step 2 scope. The gate says "list the intensive conditions the regime imposes" but the case text gives only some. I checked the named ones and skipped the rest (for example T_op for the magnet cases 10 and 11). A named threshold with no datum (cases 8, 17) blocks step 2.
9. Pair assignment. Case 8 does not say which of the pair is g. I inherited g = double layer from case 7. With g = Li-ion kappa is 2.88 and the slack is missing.
10. Basis of kappa (case 7). Practical (H3 MEMORY UNSURE inputs), theoretical (H1) or ceiling (H2). Case 3: rho_C is not stated; F3 values 11.81 (1.70) and 8.883 (2.26) both exceed the slack of 3, so the class does not change.
11. Cases 12 and 18 are decided by the case's own premise (T_op above the Curie point; no solid coefficient in Hagen–Poiseuille). Neither tests a number. M1 printed no Curie temperatures; case 18 rests on the plan's equation (no row), with the G1.6 falsifiers (slip, roughness, wall strength) not excluded.
12. Steps 4 and 5 add nothing to the class. Step 4 (the thrifted comparator s') and step 5 were not evaluated numerically: no row builds s'. Every Class II is "step 3 passed", which is what the matrix shows as deciding step "5 (after step 3 pass)".

### Input quality

- Cases 7, 8: H3 inputs are MEMORY UNSURE (see group C, item 8) and H3 failed its own A/B check at some corners.
- Cases 10, 11: H_cJ of ferrite is a MEMORY UNSURE range (250 to 400 kA/m); the pass at 155 kA/m uses the low end.
- Case 2 buildup number (F6, x_C/x_W = 1.16) is from a Monte Carlo whose check (iv) against published buildup factors was not run (group B, item 11). The class does not depend on it (1.04 also passes).
- Case 4: sigma_a from Sears 1992 as recorded by N1. Per-atom ratios only; no mass or volume basis was computed.
- Each constant in `j1_gate_matrix.py` is checked at run time against the quoted text of its source output file; all found.
