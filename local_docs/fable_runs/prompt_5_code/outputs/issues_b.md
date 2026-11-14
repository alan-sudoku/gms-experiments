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
