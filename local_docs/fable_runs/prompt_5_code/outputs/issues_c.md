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
