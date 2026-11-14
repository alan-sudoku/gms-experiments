# Prompt 5 review (S5): Class I / Class II demarcation (GMS-300 gate)

Stage: S5 adversarial reviewer. Date: 2026-11-14. Level of everything in this file: `derived` (unverified). Agreeing with the answer does not validate it.

Inputs read: the Prompt 5 fenced block in `local_docs/fable_questions.md`; `prompt_5_answer.md` (S4); `prompt_5_plan.md` (S1); `prompt_5_code/` (scripts, `data/`, `outputs/`, including `s4_checks.txt` and `j1_gate_matrix.txt`); `prompt_5_citations.md` (S3).

Review scripts: `local_docs/fable_runs/prompt_5_review_code/`, outputs in `prompt_5_review_code/outputs/`. Each is standalone (`python3 <script>`; numpy, scipy, sympy).

| Script | What it does |
|---|---|
| `r0_rerun_all.py <scratch>` | copies `prompt_5_code/` to a scratch directory, rebuilds every data CSV from `data/raw/`, reruns all 36 analysis scripts, diffs against the committed outputs |
| `r1_answer_numbers.py` | finds each numeric token in the answer and looks for it in the outputs and data (a rough check) |
| `r2_gate_independent.py` | applies the section 8 gate to the 18 J1 cases using my own encoding, under two readings; a mixed-route test of step 4; Σ_init sensitivity; the P1 numbers under the fairness rule |
| `r3_f6_mc_independent.py` | independent slab Monte Carlo (Kahn sampler, 3-D directions, own interpolation and target fit) |
| `r4_n1_ri_independent.py` | independent resonance-integral quadrature from the same ENDF/B-VII.1 pointwise files (lin-lin, log-log, trapezoid in ln E) |
| `r5_e1_voxel_independent.py` | independent voxel conduction: periodic cell, imposed mean gradient, void conductivity 0, CG solver, grid refinement N = 32 → 64 |
| `r6_derivations.py` | sympy and numeric checks of A4, D1, the shape-anisotropy ceiling, the exchange-spring formulas, the G1.4 limits, B3 by quadrature, Kelvin, the optimum fin, the H1 atom counts |

## 1. Summary verdict

1. The numbers reproduce exactly (36 of 36 scripts, all 33 data CSVs rebuilt byte-for-byte), and four independent re-implementations (F6 Monte Carlo, N1 RI, E1 voxel, B3) agree to 0.3% or better. The verdict "valid with restated scope" follows.
2. The proposed gate does not implement the restated demarcation it comes with. Step 4 tests one compensation route at a time, so it can return Class I for a candidate that is feasible with combined routes. G4.3 ("same result as a constrained Σ comparison") is therefore false for the gate as worded, and holds by construction (an identity) once step 4 tests joint feasibility.
3. Under the fairness rule, two of the "pay" regimes are not separate doors. The heat pipe (R5) is series dilution: a steel-walled pipe reaches 0.425 of a Cu-walled pipe. The catalyst area route (R4) is the material index again. Restated sentence 2 overstates what geometry can do.
4. G1.4's high-confidence limit law is wrong for two of the four problems it names (fin, absorber slab). There is also one coding bug (H1 atom count: 0.308 should be 0.264 eV/atom). Neither changes the verdict.
5. "Incomplete" in 5 of 18 cases does not make the gate unusable. It does show that the class is set by the envelope the scenario declares; the class is not a property of the function. The 13/5/0 tally is in-sample and depends on how the wording is read (14/4/0 under another defensible reading).

## 2. Findings table

| # | Severity | Location | Finding | Evidence or script |
|---|---|---|---|---|
| 1 | MAJOR | §8 step 4; G4.3; G5.1 | Step 4 classifies Class I when "every compensation route has π above the slack of some capped quantity", taking routes one at a time. Counterexample: a fin (h = 50 W/(m²·K), L = 30 mm, t = 1 mm, Al k = 200 for Cu k = 400) with thickness capped at 1.5× and height capped at 1.05×. The single-route prices are 2.000 (thickness) and 1.092 (height), and same geometry needs 1.067 with no margin, so the gate returns Class I. The combined design at 1.5× thickness and 1.05× height delivers q′_g/q′_s = 1.018 at 0.475 of the Cu fin mass. 64% of the cap pairs that lie below both single-route prices admit such a design. So G4.3 is false for the procedure as written. Restated sentence 1 (joint "does not fit inside the envelope") is right; the procedure does not implement it. | `r2_gate_independent.py` part B |
| 2 | MAJOR | G2.5 (R4, R5); G2.7; §7 sentence 2 | The fairness rule lets the incumbent use the same pipe geometry. The fair ratio is k_eff(steel wall)/k_eff(Cu wall) = 0.425 and k_eff(k = 200)/k_eff(Cu) = 0.947 [p1]. This is series-resistance dilution (R2, penalty φ·(κ − 1)), not a separate door. The answer's headline "283×, 268×, 120× solid Cu" compares a pipe with a solid bar, which breaks the prompt's fairness rule. R4 (catalyst area route) is open to the incumbent too, so it reduces to the material index (R1). No Σ computation supports it, and G2.6's own finding (x at mg/cm² costs about 1 mV-equivalent in CED) cuts against it. Only R6 (decoupling) is a door that the incumbent cannot use. "A switch of transport mechanism" in restated sentence 2 is unsupported. | `r2` part D; answer G2.6 |
| 3 | MAJOR | G1.4 (confidence high); §9 item 6 | Claim: "in the thick limit the function scales as c^(1/2)", with penalty κ^(1/2) thick and κ thin, "kept for the tanh problems". The same-geometry penalty with κ = 2 actually behaves as follows. Fin: from 1.000 (thin) to 1.414 (thick), so the fin has no penalty in the thin limit. Slab absorber: from 1.996 (thin) to 1.000 (black). Porous electrode: from 2.000 to 1.414, the only one of the three that spans [κ^(1/2), κ]. Strip: dips to 1.32 at κ = 2. The isotropic slab absorber does not obey u″ = u/λ²; it is an E₃ transport problem. G1.4 also mixes the penalty at the same geometry with the compensation price: for a fin, t_g/t_s = κ at every mL. Gate step 3 is protected because it says to evaluate the regime function. | `r6_derivations.py` §5 |
| 4 | MAJOR | G4.2; §8 wording | My own encoding of the 18 cases reproduces S4 under a literal reading (13 expected, 5 U, 0 opposite). Three cases change under defensible alternative readings. Case 16: S4 gives U; reading "some route with π ≤ 1" per quantity (thicker fins: mass price 0.603) gives Class II. Case 4: S4 gives U; reading "thin sheet" as a thickness cap gives Class I. Case 10: S4 gives Class I; treating the demagnetising-field threshold as activated without a datum gives U. The tally becomes 14/4/0 with a different U set. The procedure was revised after it failed on these same 18 cases, so the test is in-sample. S4's application is a hand-encoded table (`s4_checks.py` list `C`), so "13 of 18" holds by construction of that encoding. The answer calls it a consistency test but does not say it is in-sample or reading-dependent. | `r2` part A |
| 5 | MINOR | G3.10 table; `h1_h2_redox_dl_energy.py` line 22; §9 item 20 | Bug: LiCoO₂ + 3C has 7 atoms, but the script uses N_at = 6. 0.5 × 3.7/7 = 0.264 eV/atom, not 0.308. The planner's 0.26 was right, and §9 item 20 wrongly presents it as revised. The range (0.23 to 1.22) and the gaps are unchanged. Needs a fix with a regression test (CLAUDE.md rule). | `r6` §8 |
| 6 | MINOR | G2.5 R1; G2.3 | The R1 example "Σ*_Al/Σ*_Cu 0.45 to 0.50 with secondary Al" pairs recycled Al with primary Cu. Supply route is not an x-dependent feature, so under the fairness rule the incumbent may be recycled too. The symmetric pairs give 0.932 (ICE) and 0.647 (Nuss). The ICE recycled/recycled pair flips with a +15% change of the e-ratio, and the Nuss mix pair with −17%. Two of the seven G2.3 rows are within currency or allocation uncertainty of the break-even 2.025. | `r2` part C |
| 7 | MINOR | G2.4, G2.6 (currency) | The comparison mixes bases: embodied values are cumulative primary energy, while operating losses are delivered electrical work. Counting the loss with an upstream primary-energy factor f for electricity (UNSURE, of order 2 to 3) divides (J²τ)* and Δη_be by f. This strengthens G2.6 and moves the A4 crossovers to lower duty. f cancels in the Kelvin ratio of G2.3. | reasoning; `r2` part C |
| 8 | MINOR | G1.4, §9 item 6 (B3) | The dip of the Al/Cu R_ac ratio to 1.216 (at t/δ_Cu = 4.66 by quadrature; 4.72 on the S2 grid) appears only when both metals use the same thickness. With each at its own optimum (ξ = π/2, F/ξ = 0.9172), the ratio is exactly κ^(1/2) = 1.280. Under the fairness rule the relevant number is 1.280. | `r6` §6 |
| 9 | MINOR | G3.13 | f_h = μ₀M_s²/(4K_h) = 0.098 is the minimum hard fraction in the model. The multilayer of the 1993 abstract (2.4 nm hard, 9 nm soft) has a hard volume fraction of 0.21, which gives about 4.7 wt% rare earth with densities 7.7 and 8.1 g/cm³ (UNSURE), consistent with the abstract's 5 wt%. "f_h 0.10 to 0.24" understates the quoted realisation by about 2×. A search result places "1 090 kJ/m³ for Sm₂Fe₁₇N₃/Fe₆₅Co₃₅" in the companion 1993 paper "Aligned two-phase magnets: permanent magnetism of the future?", not in Phys. Rev. B 48, 15812 (UNSURE, secondary). | `r6` §4; search |
| 10 | MINOR | G3.6 / N2 | B-10's RI/(0.45σ₀) = 1.004 includes a +0.45% bias from lin-lin quadrature on a sparse file (146 points, spacing ratio 1.30 in E). Log-log quadrature gives 0.9999. Harmless; within the ±5% test. | `r4` |
| 11 | MINOR | G4.2/G4.4 input (d) | "Decidable from inputs a scenario can supply" holds only if the scenario author supplies the governing equation, c_s, c_g, the ceiling value, and (in step 3) the list of compensation routes. Most of the physics is pushed into the inputs. | reasoning |
| 12 | MINOR | `s4_checks.py` G | S4 encodes case 6 with an envelope stated but cases 4 and 16 without one, although none of the three case texts states an envelope. This has no effect on outcomes, because π ≤ 1 is tested first. | `s4_checks.py` list `C` |
| 13 | MINOR | G1.7, §9 item 5 | The revision is correct. More precisely, the Δη error is err(η_g) − err(η_s), bounded by err(min(η_s, η_g)), so the planner's condition on η_s alone is enough whenever η_g ≥ η_s (no area compensation). The 2 mV thresholds 83.90 and 104.44 mV were verified by a direct Butler–Volmer root. | `r6` §2 |
| 14 | MINOR | G3.4 | The two Monte Carlo codes agree (−0.3% to +0.2% on x_C/x_W), but they share the physics choices: no coherent scattering, no fluorescence (W K x-rays matter most at 0.5 MeV; magnitude UNSURE), free-electron Klein–Nishina, transmitted energy over the whole plane. The agreement verifies the code, not the buildup physics. | `r3` |

Counts: BLOCKER 0, MAJOR 4, MINOR 10.

## 3. Reproducibility

| Item | Result | Evidence |
|---|---|---|
| Data CSVs rebuilt from `data/raw/` (f0, n0 builders) | 33 of 33 identical | `outputs/r0_rerun_all.txt` |
| Analysis scripts (36, including `j1_gate_matrix.py` and `s4_checks.py`) | 36 of 36 identical; F6 differs only in 4 elapsed-time lines | same |
| `outputs/n1_values.csv` | identical | same |
| `n1_fetch_endf_sigma.py` | not rerun (network); the raw files it wrote were used by N1 and by `r4` | — |
| Answer numbers against outputs | 578 tokens checked; 3 not found, all the year "2009". The match is loose (rounding, scale factors) and can pass a number quoted out of context | `outputs/r1_answer_numbers.txt` |
| Load-bearing numbers checked by hand in context | c4 (1.04, 1.33, 1.41, 208.7), h3 (14.4, 4.8 to 96), p1 (5.7, 10.7, 60%, 283×), n5 (38.4, 332.8), s4 A to G | read in outputs |
| F6 buildup Monte Carlo | x_C/x_W: 1.9505/1.9555 (0.5 MeV, 1e-2), 1.8892/1.8849 (0.5 MeV, 1e-3), 1.1598/1.1629 (1 MeV, 1e-2), 1.1424/1.1436 (1 MeV, 1e-3); differences within 0.3% (within statistics) | `outputs/r3_f6_mc_independent.txt` |
| N1 RI integration | lin-lin on each file's own grid matches S2 to ≤ 6e-6; log-log is 0.4 to 0.9% lower; against Mughabghab 2003 capture values (S3): In −2.1%, Hf −1.1%, nat Gd +1.0%, Cd-113 −0.9% | `outputs/r4_n1_ri_independent.txt` |
| E1 voxel solve | matches S2 to ≤ 4.5e-4 at N = 32; N = 64 refinement raises σ_eff by 0.44 to 0.80%; all points 0.51 to 0.94 of the Hashin–Shtrikman bound | `outputs/r5_e1_voxel_independent.txt` |
| B3 strip | quadrature of the cosh field matches the closed form to 2.5e-14; minimum ratio 1.2157 | `outputs/r6_derivations.txt` §6 |
| S4 gate on the 18 cases | reproduced, 13/5/0 under a literal reading; 14/4/0 under reading B | `outputs/r2_gate_independent.txt` A |

Checks that are identities or true by construction: the S4 gate tally (hand-encoded inputs); the C4 exponents 3.44 and −3.00 (S2 says so); F6 energy balance; M5 optimiser against formula; H3 "t* = E_c/P_b"; A2 ratio independence (it follows algebraically from the closed form); G2.1's "evidence" (each item is an instance of the lemma); G4.3 once the gate tests joint feasibility; the E1 bound check (it confirms a theorem on one geometry).

## 4. Derivation checks

| Derivation | Result | Script |
|---|---|---|
| A4 crossover D_c = (1 − x)/(κ − 1); D_c > 1 ⇔ x < 2 − κ = 0.3616 | Verified (sympy). Nuss primary pair: x = 0.9858, D_c = 0.0222, (J²τ)* = 6.84e17 A²·s/m⁴, or 6.84e5 s at 1 A/mm². Matches [s4-C]. | `r6` §1 |
| D1 Tafel threshold (2 mV, α_a = α_c = 0.5) | 83.90 mV at 298.15 K and 104.44 mV at 353.15 K; a direct Butler–Volmer root gives exactly 2.000 mV at these points. "Both above threshold" is sufficient (finding 13). | `r6` §2 |
| Shape-anisotropy ceiling | Within the stated model (rectangular loop per needle, M_r = pM_s, Néel H_c = (1 − p)M_s/2, coherent rotation): branch p ≤ 1/2 has maximum 1/16; edge branch μ₀M_s²(3p − 1)(1 − p)/4 has its maximum 1/12 at p = 2/3. 398.1 kJ/m³ (2.45 T), 306.5 kJ/m³ (Fe). Correct for the model; curling reversal makes it an upper bound of an idealisation. | `r6` §3 |
| Exchange-spring formulas | Numbers reproduced: f_h 0.0979, 1 091 kJ/m³; 0.2397, 985 kJ/m³; wall width 4.01 nm. The formula form is not checked against the paper (UNSURE). See finding 9. | `r6` §4 |
| G1.4 limits | Wrong for the fin and the absorber slab (finding 3). | `r6` §5 |
| Kelvin optimum | A* and Σ* verified (sympy); J*(Cu) = 0.2128 A/mm². | `r6` §7 |
| Optimum rectangular fin | β = 1.41922; constant 0.50425. | `r6` §7 |
| Hashin–Shtrikman 2φ/(3 − φ) | Re-derived by hand from the HS upper bound with a void phase; the voxel solves lie below it. | `r5` |
| 1/v RI factor 2·sqrt(0.0253/0.5) = 0.4499 | Correct (also S2's own numerical check). | — |
| κ per mass Cd/Al = 2.62e3 | (2520/112.41)/(0.231/26.98) = 2.62e3; matches [s4-E]. | arithmetic |
| G3.10 per-atom energies | Correct for four of five cells; LiCoO₂ + 3C is wrong (finding 5). | `r6` §8 |

## 5. Missed regimes and fair comparisons (task 4)

1. **Is the gate decidable from scenario inputs?** Only if the scenario supplies most of the physics (finding 11), and only after step 4 is fixed so that it tests joint feasibility (finding 1). With that fix, step 4 becomes "is there any g in the admissible set that meets F_req within all caps", which is a constrained feasibility problem. That is the hard part of the Σ comparison anyway. The wording also leaves case 16 (π per route or per quantity), case 4 ("thin" as a cap) and case 10 (whether the field threshold is activated) open (finding 4).
2. **Does "incomplete" in 5 of 18 make it unusable?** No. One case is a defect of the test case (8: g not named); one needs a lookup the scenario could cite (17: Pourbaix datum); three need an envelope or margin (4, 14, 16). The real issue is what the completions show: in all four completed cases (4a/b, 8/8′, 14a/b, 16a to d) both classes can be reached with plausible envelope inputs [s4-G]. The class depends on the declared envelope, and the gate has no default for it (the answer concedes this).
3. **Would the Σ comparison alone give the same classification (G4.3)?** Class I is "g cannot meet F_req within the envelope or thresholds". A constrained Σ comparison returns exactly that as "g infeasible", so for a correct gate G4.3 holds as an identity, not as evidence. The gate as written can be stricter than the comparison (finding 1), so the two can disagree, always towards "retain x". The out-of-scope N exit (case 18) removes a case that a Σ comparison would still rank on Σ_init alone (choice of wall material). That is a loss, not a saving.
4. **Dependence on the undefined Σ_init currency.** The section 8 gate takes no Σ_init input, so its classification does not depend on the currency. The Class II outcomes do. Two of the seven G2.3 pairs flip with a 15 to 17% change of the e-ratio (finding 6). G2.6 needs a factor of 20 to 36 on e_Pt, so it is robust to the CED-versus-exergy choice and fragile only against a scarcity-pricing currency. The mismatch between primary and final energy (finding 7) moves G2.4 and G2.6 by a factor of order 2 to 3 (UNSURE), in the direction that strengthens G2.6.
5. **Missed fair comparisons.** Pipe against pipe (finding 2). Each metal at its own optimum thickness in B3 (finding 8). Symmetric supply routes in R1 (finding 6). The incumbent may also roughen its catalyst (R4, finding 2).
6. **Missed regime that does favour the answer.** G3.5 (heavy-element substitution inside Class I) is a real gap in the prompt's gate, and the answer flags it correctly.

## 6. Claim-by-claim (task 5)

A = agree, D = disagree, U = unsupported by the evidence presented.

| Claim | Call | Note |
|---|---|---|
| G1.1 | A | Jensen theorem; the F5 sweep illustrates it |
| G1.2 | A (as taxonomy) / U (as complete) | cases written by the planner |
| G1.3 | A | |
| G1.4 | D | finding 3 |
| G1.5 | A | fin constants verified; flow exponents are identities |
| G1.6 | A | reasoning only |
| G1.7 | A | thresholds verified |
| G1.8 | A | theorem; voxel solve is one geometry |
| G2.1 | A | lemma; the listed evidence is instances, not tests |
| G2.2 | A | sympy |
| G2.3 | A with caveat | finding 6 |
| G2.4 | A | |
| G2.5 | D in part | R4 and R5 are not separate doors under the fairness rule; R1 example asymmetric (findings 2, 6) |
| G2.6 | A | Pt row 243 000 (178 000 to 326 000) MJ/kg confirmed in `raw/nuss/s1.txt` line 7633 onward |
| G2.7 | D (as a fairness-rule regime) | finding 2; inputs unverified |
| G2.8 | U | logic sound, film values are MEMORY |
| G2.9 | A | |
| G2.10 | U | reasoning only; plausible |
| G3.1 to G3.3 | A | NIST lookups reproduced from raw; S3 agrees |
| G3.4 | A | Jensen; Monte Carlo code verified (finding 14) |
| G3.5 to G3.9 | A | G3.9 on a secondary source |
| G3.10 | A after correction | finding 5 |
| G3.11 | U | all inputs MEMORY |
| G3.12 | A | derivation verified; inputs secondary |
| G3.13 | A in thrust | finding 9 |
| G3.14 | A | optimiser is near-identity |
| G4.1 | A | |
| G4.2 | A with stronger caveat | finding 4 |
| G4.3 | D as worded | finding 1; identity once corrected |
| G5.1 | A | the verdict follows; restated sentence 2 needs editing (drop "a switch of transport mechanism" or recast it as dilution; class R4 as the index) |

The restated demarcation: sentence 1 follows and is the right joint test; sentence 2 overstates (finding 2); sentence 3 follows.

## 7. Citations (task 6)

| Item | Answer status | This review |
|---|---|---|
| Nuss and Eckelman 2014, S1 Table S38, Pt rows | P | Confirmed from the raw text: "Pt TOTAL" CED 243 000, 95% 178 000 to 326 000 MJ/kg |
| ANSI/ANS-6.4.3-1991 coverage of C and W | S | Search results (secondary) list 23 elements including C and W, 0.015 to 15 MeV, 40 mfp; standard withdrawn 2001. Agrees with the answer. Buildup comparison still not run |
| Xia et al. 2009, 21 µF/cm², 550 F/g | UNSURE | Citing works attribute 21 µF/cm² to Xia et al. as a measured double-layer capacitance at a graphene/ionic-liquid interface. 550 F/g is a later product with about 2 630 m²/g. The answer's UNSURE is fair; add the electrolyte context (ionic liquid, not aqueous). Secondary |
| Skomski and Coey 1993, PRB 48, 15812 | S | Abstract (via a citing page) confirms 2.4 nm Sm₂Fe₁₇N₃ / 9 nm Fe₆₅Co₃₅, 1 MJ/m³ (120 MG Oe), 5 wt% rare earth. "1 090 kJ/m³" appears in the companion paper "Aligned two-phase magnets" per a search snippet: attribution UNSURE (finding 9) |
| Skomski et al. 2010, μ₀M_s²/12 at p = 2/3 | S | My search did not show the statement; not reconfirmed (UNSURE). The derivation itself is verified within the model (§4) |
| B-10 (n,α) resonance integral | none found | Search found the Atlas thermal value 3 837 ± 9 b but no (n,α) RI; still computed only |
| Planner MEMORY inputs still unverified | MEMORY | k of Cu, Al, 6063, AlSi10Mg; graphite, B₄C, steel densities; foam specific area; cell voltages; Ragone inputs; magnet μ₀M_s, K₁ and grade values; ITO film; wick k; Ir loading. None checked here |

Web searches used titles, authors and technical terms only.

## 8. What still needs external checking

- **Most decisive single check:** an out-of-sample test. Have someone other than the planner write about 20 complete scenarios. Run the corrected gate (joint-feasibility step 4) on them, and separately run a constrained Σ optimisation that allows mixed compensation routes. Count disagreements and cases left incomplete. This tests G4.2, G4.3 and restated sentence 1 directly; nothing else in the run does.
- Broad-beam buildup against ANSI/ANS-6.4.3 (or DLC-129) for C and W at 0.5 and 1 MeV, with fluorescence included (G3.4).
- A tabulated B-10 (n,α) resonance integral (G3.6).
- The framework's Σ_init definition (G2.3, G2.4, G2.6), plus the primary-energy factor for operating electricity (finding 7).
- Pourbaix datum for Ni–Fe oxides in acid at OER potential (case 17).
- Magnet inputs from Coey's tables; realised exchange-spring values (G3.12 to G3.14).
- ITO film data (Ellmer 2012) and a minimum mesh line width (G2.8).
- A measured heat pipe with a steel or Al envelope compared with a Cu one at the same dimensions (G2.7 under the fairness rule).

Code fix owed by the owner of `prompt_5_code/`: `h1_h2_redox_dl_energy.py` LiCoO₂ + 3C N_at = 7, with a regression test (finding 5).
