# Prompt 3 review (stage S5): lattice fatigue micromechanics

Context file (`local_docs/`, never cited by the spec). Written 2026-11-14 by an independent S5 reviewer. Inputs: `fable_questions.md` (Prompt 3 block and status), `prompt_3_q1_web_answer.md`, `prompt_3_q2_web_answer.md`, `prompt_3_plan.md`, `prompt_3_answer.md`, `prompt_3_citations.md`, `prompt_3_code/` and its `outputs/`. Review code: `prompt_3_review_code/rv1_unit_cells.py`, `rv2_entropy_mismatch.py`, outputs in `prompt_3_review_code/outputs/`. Web searches used titles, authors and technical terms only.

**Status: everything here is a claim at level `derived` (unverified).** My scripts are computation, not evidence. Where I agree with the answer, that agreement does not raise any level.

## Summary verdict

1. All eight scripts re-run byte-identical, and every answer number I traced matches its output. An independent energy-route model reproduces every S2 octet and BCC constant. The arithmetic is sound.
2. The Q4 verdict holds for the two asked frequencies: diurnal fatigue dissipation is immaterial by any margin, and at 1 Hz it stays below the LPBF and primary-metal terms. Claim 1 states it too broadly, though: the life bound grows as (ν·τ_s)^(1+2b), and at 10 to 100 Hz it reaches or exceeds the LPBF term.
3. Two model gaps are larger than any spread the answer reports. The octet is modelled pin-jointed, but a monolithic AM octet has rigid joints: at ρ̄ = 0.2 the peak strut stress roughly doubles and r² goes from 1 to about 4. For BCC, rigid node zones (not Timoshenko shear) set the uncertainty in E_eff and c, and they push c up to 1.05–2.35 at ρ̄ = 0.2.
4. Claim 19 reports the no-mean-stress end of its own bound pair. The cool-down mean is tensile in the lattice, and the Q5 validity condition fails at a realistic stress-free temperature. With Goodman, the plan-input Ti-6Al-4V case lasts 0.4 to 72 years, not 1.3e4 to 1.7e4.
5. A cell-scale thermoelastic mechanism (heat flow between tension and compression struts) gives ψ of the same order as 5e-3 for octet cells of 5 to 10 mm at 1 Hz. The answer accepts Q1-7's statement that this damping is "about zero" for stretch cells; that statement is wrong at the cell scale.

Counts: BLOCKER 0, MAJOR 6, MINOR 10.

## Findings

| # | Severity | Location | Finding | Evidence or script |
|---|---|---|---|---|
| F1 | MAJOR | Claims 1, 3, 5, 6, 8, 15; §4 row Q1-3; Q5 life table (k_peak C = 15) | The octet is a pin-jointed model. Its nodes form an FCC Bravais lattice with inversion symmetry, so the deformation is exactly affine with zero node rotation, and rigid (monolithic) joints add fixed-guided bending of 3·E_s·abs(g)·(d/l). At ρ̄ = 0.2 along [100]: k_peak·ρ̄ = 5.79 (EB) or 5.63 (Timoshenko), against 3; r² = 3.95 or 3.72, against 1. The [100] advantage over [110] disappears (5.79 against 5.81). Fatigue-limited σ_a falls from 4.00 to 2.07 MPa. The stretch-corner maximum falls from 3.42e4 to 8.6e3 J/K (9.7 % of LPBF at 50 MJ/kg instead of 38 %). This strengthens the verdict, but the corner's quoted values and the claim "r = 1, RMS equals peak" are artefacts of the pin joints. | rv1 §4, §5; rv2 §2 (r² = 3.95 column) |
| F2 | MAJOR | Claims 4, 16, 17; §4 rows Q2-1, Q2-8; Changed items 5, 12, 13 | For BCC, the answer brackets E_eff, k_peak and c between Euler–Bernoulli and Timoshenko. That bracket has the wrong sign for the dominant correction: rigid node zones (struts overlap up to about 0.87·d from the node centre at 70.5°). A rigid-zone sensitivity with a_r = 0.25·d to 0.87·d at ρ̄ = 0.2 gives E_s·ρ̄²/E_eff = 2.65 to 8.88 (answer: 11.1 to 12.3), k_peak 83.6 to 118.6 (answer 132.8), and equibiaxial c = 1.05 to 2.35 (answer 0.86 to 0.94). The c = 1 crossover moves from 0.227–0.309 to 0.075–0.18. So the Q5 mismatch default's statement "margin 1.5 to 1.6 at ρ̄ = 0.1" is not supported; c = 1 may be non-conservative by up to about 2 at ρ̄ = 0.2. With rigid zones the octet's equibiaxial c is 1.21 at a_r = 0.5·d, so c = 1 is not a bound for stretch cells either. Rigid-zone length is UNSURE; this is a sensitivity, not a value. | rv1 §3, §4 (eta 0.5 rows) |
| F3 | MAJOR | Claim 1 ("In all other cases fatigue enters through τ_wearout only"); claim 7 | With a service cap, the life maximum is S(1e7)·(ν·τ_s/1e7)^(1+2b)/r², so it grows with frequency. For 30 years, σ_w7 = 60 MPa, b = −0.095: at 10 Hz, pin octet 2.2e5 J/K (2.5 × LPBF at 50 MJ/kg), rigid octet 5.6e4 (0.63 ×); at 100 Hz, BCC 1.24e5 (1.4 ×), rigid octet 3.6e5 (4.0 ×), A 5.7e4 (0.64 ×). The prompt asked for 1 Hz and 1 per day only, but claim 1's last sentence is unconditional. It should read "for ν ≤ about 1 Hz". These values extrapolate Basquin to 1e10–1e11 cycles (UNSURE). | rv2 §2 |
| F4 | MAJOR | Claim 11; claim 2 validity; §4 row Q1-7 accepted; open point 11 | A stretch-dominated lattice has a second thermoelastic relaxation at the cell scale. Under [100] stress, tension struts cool and compression struts heat, and heat flows through the nodes; 89 % of the strut-stress variance relaxes this way (83 % for [110], 80 % for [111]). A 1D model with each strut held at the node temperature gives f_1 = π·D/(2·l²): 18.9 to 1.7 Hz for cells of 3 to 10 mm. ψ_inter(1 Hz) is 0.19 to 1.56 × ψ for α_s = 21e-6 /K and 0.31 to 2.57 × for 27e-6 /K. That reaches the answer's own falsifier threshold (2.6 × ψ) in the corner the verdict depends on. It is real entropy generation and belongs in Σ̇. It is negligible at 1 per day (≤ 2e-7). Q1-7's "about zero for stretch-dominated cells" holds only within a strut. The 1D model ignores node heat capacity and convection (UNSURE). | rv2 §3(b) |
| F5 | MAJOR | Claim 19 headline; claim 4 (Q5 mismatch default); claim 20 evidence | Claim 19 ("with the plan's inputs it does not limit life") uses no mean stress and c = 1. In the cases claim 19 lists, the partner has the lower α, so after cool-down the lattice holds a tensile mean. de Krijger 2017 (compression–compression, macroscopic R) is not evidence for this case; Lietaert 2018 (tension) and claim 27 point the other way. At the Goodman end (σ_m = min(σ_y, E_s·Δα·300 K), σ_u = 460 MPa), lives below 30 years are 4, 22 and 35 of 60 cases at K_n = 1, 2, 3, against the 0, 4 and 10 claim 19 reports. Ti-6Al-4V, plan inputs, K_n = 3, 50 K: 18 to 72 years (b = −0.1434, σ_u 400 to 460 MPa) or 0.44 to 3.5 years (b = −0.095), against 1.3e4 to 1.7e4. With c = 1.49 (bonded roots, part of the Q5 default) and no mean: 1, 10 and 24 of 60. The Q5 validity condition ("nominal range plus mean below σ_y") fails at ΔT_ref = 300 K for Ti-6Al-4V (304 MPa) and Invar (483 MPa). As written, the default formula has no mean-stress term while its validity condition excludes the typical co-printed pair. | rv2 §5 |
| F6 | MAJOR | Input change 1 ("σ_w7 30 to 60 MPa"); claim 26 (ratio 0.23 to 0.27; "0.5 to 0.8 not supported at its upper end"); Changed item 23 | In Aboulkhair 2016, "as-built" names a heat-treatment condition. The paper tested four conditions (as-built, as-built + machined, heat-treated, heat-treated + machined). Its abstract says machining played a minor role compared with heat treatment, and a secondary summary reports heat-treated, unmachined samples surviving at 94 MPa. The 63 MPa "maximum stress range" is therefore a no-heat-treatment microstructure result whose stress basis is unknown. It is not a surface knock-down. The 30 MPa lower end may still be a fair conservative input, but the ratio 0.23 to 0.27 and the rejection of the plan's 0.5 to 0.8 rest on a misattribution. The paper's own finding (surface minor next to heat treatment) points toward the plan's upper end for bulk coupons; thin struts remain open. | Web search (abstract and secondary summaries; full text not opened; R ratio still UNSURE) |
| F7 | MINOR | Claim 1, diurnal bullet and falsifier | The headline gives a maximum of 7.4 J/K, but the ratios are quoted for the 6.63 J/K case (0.41 % of the melt floor; "245 times"). For 7.43 J/K the figures are 0.46 % and 219 times. | s4_q4 §5, §6; rv2 §6 |
| F8 | MINOR | Claim 11; open point 14 | For round struts the first radial thermal mode gives f_Z = 2.158·D/d², 1.37 times the reed value. ψ_TE(1 Hz) is then 0.72 to 0.75 times the quoted values; at 5 mm it is 0.98 × ψ, not 1.31 × (α_s = 21e-6 /K). The direction of the conclusion is unchanged. | rv2 §3(a) |
| F9 | MINOR | Claim 8; open point 1 (gyroid) | The bound S ∝ 1/r² with r ≥ 1 does not cover sheet TPMS. An equibiaxial membrane wall has σ_rms = sqrt(2(1−ν_s))·σ_peak, so r² = 1/(2(1−ν_s)) = 0.75, and the bound can exceed the pin-octet value by 1.34. Bobbert 2017's 60 % endurance applies to "some" TPMS designs only (abstract). The gap affects the verdict only through σ_w, ψ and that factor of 1.34. | Hand algebra; Bobbert abstract |
| F10 | MINOR | Open point 11; claim 12 | Σ̇ in the prompt is defined as entropy generation. Anelastic and thermoelastic dissipation are real entropy production and belong in Σ̇ whether or not they cause damage. Only the link to damage (claim 12) is in doubt. The answer leaves this open; it can be decided. | Reasoning |
| F11 | MINOR | Claim 1, comparators | The LPBF figures are probably electricity. Upstream primary energy is about 2 to 3 times higher (UNSURE). Primary-Al energy/T₀ also counts the chemical exergy retained in the metal. Both corrections push the comparators up or leave them unchanged, so the verdict is unchanged. | Reasoning |
| F12 | MINOR | Claim 23 | With rigid joints, k_peak(C [100]) is about 29, so the octet over-prediction is 10.2 to 15.4 decades instead of 8.2 to 12.4. The stated range "8 to 22" shifts slightly at the low end. | rv2 §6 |
| F13 | MINOR | Claim 16 confidence "high for the beam algebra" | The beam algebra is right (reproduced to every digit), but the number quoted from it (11.1 to 12.3) is not the quantity a reader needs. See F2. | rv1 §2, §3 |
| F14 | MINOR | §4 row Q2-1 ("C_b revised to c = 0.64 to 1.29") | This is a revision within one beam model; see F2. Q2-1's octet statement (c = 1) holds at η = 0 even with rigid joints (out-of-plane strut bending 0.51·E_s·ε_m at ρ̄ = 0.2, 0.70 at 0.4). It fails with rigid node zones (1.21). | rv1 §4 |
| F15 | MINOR | Claim 25 / citation Hrabe 2011 | The abstract compares the lattice's 0.15 to 0.25 with "0.4 for solid of the same microstructure". That suggests normalisation by a static strength, but yield against ultimate is still not stated. The basis stays UNSURE, as the answer says. | Web search |
| F16 | MINOR | Claim 1 falsifier wording | "ψ ≥ 1 is not possible for an elastic part": ψ = ΔU/U ≥ 1 means a hysteresis loop as large as the stored energy. Implausible for an elastic metal part, but not impossible by definition. | Reasoning |

## Reproducibility

| Item | Result |
|---|---|
| `p3_unit_cells`, `p3_q4_limits`, `p3_q4_entropy`, `p3_sensitivity`, `p3_q3_normalisation`, `p3_mismatch`, `s4_q4_rerun`, `s4_mismatch_rerun` | Re-run with system `python3`: exit 0, no stderr, stdout byte-identical to the saved `outputs/*.txt` (8 of 8) |
| Octet constants (E_100, E_110, E_111 = 1/9, 1/6, 1/5; ν = 1/3; r² = 1, 6, 1.8; equibiaxial ε_zz = −1, c = 1, M = ρ̄E_s/6; hydrostatic 1) | Reproduced to 1e-9 by an energy route (rv1 §1), independent of S2's force route |
| BCC C1, k_peak, r², c, crossovers (0.0902/0.0815; 132.77; 12.72/11.50; 0.943/0.857; 0.2267/0.3093; ρ̄ = 0.1 to 0.4 rows of claim 17) | Reproduced to all printed digits (rv1 §2) |
| Life-integrated maxima (3.418e4, 2.973e3, 7.429, 659.1 J/K) | A brute-force σ_a grid (20 001 points) is within 3.5e-4 to 5.7e-4 below the closed form, as expected on a grid (rv2 §1) |
| Bilayer factors (0.9203, 0.8522, 0.7840; 0.7150 for A; bimetal 1/8 + 3/8) | Reproduced exactly by Timoshenko's 1925 closed-form curvature (rv2 §4), independent of S4's 2×2 solve |
| Claim 19 counts 0, 4, 10 of 60; lives 100 y, 4.9 y, 9.1 y, 0.07 y, 1.3e4 to 1.7e4 y | Reproduced (rv2 §5; s4_mismatch §2) |
| Claims 1, 5, 6, 8, 10, 11, 12, 13, 18, 20, 21, 22, 23, 25: every number checked against the outputs | All match ([4Q] §0–§11, [4M] §1–§6, [E] R18/R21, [S] R22/R24, [M] R29/R31, [L] R12–R15) |
| R21 range "1e-4 to 290", R24 factors 16, 10, 6.25, 2.9, 0.87 | Match `p3_q4_entropy.txt` and `p3_sensitivity.txt` |

No number in the answer contradicts its tagged output. The disagreements above are about method and scope, not arithmetic.

## Derivation checks

- **Energy identity (claim 14, Q1-1).** Correct. With E_s = 1, the energy route gives W = ½σ·ε exactly for all three octet directions (rv1 §1). It cannot test the joint model.
- **BCC model (claims 15 to 17).** The fixed-guided strut with zero node rotation is exact for an affine BCC (the nodes form a Bravais lattice). Keeping the axial force is correct. Timoshenko with κ = 0.9 is correctly implemented (k_t/(1+Φ), Φ = 12EI/(κGAl²)). Under stress control k_peak is unchanged by shear and r² falls; under strain control c falls. Both are right. Missing: node overlap and rigid zones, which at l/d = 4.5 change E_eff by 2 to 4 and c by up to 2.5 (F2).
- **Octet (claims 5, 8, 15, 17).** Pin-jointed constants are exact for that model. For a monolithic lattice, affine rigid-joint bending is exact in beam theory and not small at ρ̄ ≥ 0.1 (F1). This removes the r = 1 case that drives the stretch corner.
- **Peak-stress knock-downs.** For A, k_peak = f/(0.3·ρ̄^1.5) is a back-derivation from a fitted collapse constant: a heuristic, not geometry. The answer says so ("the value for A is defined by the energy identity"). For B, the result reproduces. For C, see F1. The claim 3 link k_peak = f·σ_y/σ_pl,lattice holds for plastic-hinge bending cells. For stretch cells a measured σ_pl that is buckling- or node-limited makes k_peak conservative.
- **Mismatch formula with S (claim 18).** The 1/(1+S) flat-plate result is correct. The first-order bending relief 1 − (4 + 3·H_L/H_2)·S checks by hand: the thin-film relief is 4S, and the lever arm (H_L + H_2)/2 adds 3·S·H_L/H_2. The exact values are reproduced by an independent closed form. The plate model of a lattice block a few cells high is UNSURE, as the answer says.
- **Life-integrated entropy ∝ N^(1+2b) (claims 7, 8).** Correct. With a cap the maximum sits at the kink N_f = ν·τ_s, because S ∝ σ_a² below it and S ∝ σ_a^(2+1/b) above, and 2 + 1/b < 0 for b > −0.5. Confirmed by the grid. Corollary not drawn by the answer: the total depends on ν through ν·τ_s (F3).
- **Damping exponent factor κ·(σ_rms/σ_ref)^(n_d−2) (claim 10).** Correct derivation from D = J·σ^n_d. κ circular (1.764 at n_d = 3, 3.60 at 4) checks by hand. The bending-coupon factor 3/(n_d+1) in Q1-6 checks.
- **Thermoelastic (claim 11).** The reed formula is correctly evaluated; for round struts see F8. The cell-scale mechanism is missing (F4).
- **Goodman and closed-form ΔT_x (claims 19, 20).** Algebra correct. The reading of the evidence is the problem (F5).
- **Endurance ratio (claim 25).** Arithmetic correct. The comparison remains basis-limited (F15).
- **Q1/Q2 web claims the answer accepts.** Q1-1, Q1-5, Q1-6, Q2-2, Q2-4 (1/8 + 3/8; peak 0.5·E·ε both free and restrained) and Q2-6 (bulk factor 3K, S_h for a thin spherical shell) check by hand. Q1-3 "RMS equals peak along [100]" is pin-only (F1). Q1-7 "about zero for stretch cells" fails at the cell scale (F4). Q2-3, Q2-5 and Q2-7 are untested, as the answer says.

## Missed regimes and fair comparisons

- **Frequency above 1 Hz** (F3). This is the regime that most changes the verdict. Vibration environments at 10 to 100 Hz put the bound at or above the LPBF term even for bending cells.
- **Rigid joints and node volume** (F1, F2). They move the octet one way (lower dissipation, lower allowable σ_a) and BCC c the other way (higher mismatch stress). The Euler–Bernoulli against Timoshenko spread the answer reports is the smaller effect.
- **Cell-scale thermoelastic damping** in stretch cells at 1 Hz (F4). It roughly offsets F1 in the stretch corner: a rigid octet with ψ_total = 1.28e-2 gives about 2.2e4 J/K, 25 % of LPBF at 50 MJ/kg. The 1 Hz verdict survives both corrections.
- **Mean stress in the diurnal mismatch case** (F5). The mean is tensile, near σ_y at a 300 K stress-free offset, and shakedown at the notch is likely. Stress-life with Goodman is then the more relevant end. A local-strain or shakedown treatment is the correct tool and is not attempted anywhere.
- **Bonded strut roots** (c = 1.49 plus a singular bimaterial edge). These sit in the Q5 default but not in claim 19's life grid (F5).
- **Gyroid sheet against skeletal** (F9). The sheet type is near stretch-dominated with biaxial walls (r² down to 0.75) and reportedly higher endurance. The skeletal type is bending-like. Neither changes the diurnal verdict. The sheet type could move the 1 Hz corner by up to 1.34 times through r, and by more through a higher σ_w.
- **Nodal stress concentration** beyond nominal beam stresses. It enters only through K_n, which is not derived. For the octet, the rigid-joint bending of F1 sits at the node face, so the node fillet K_t multiplies an already doubled peak.
- **Manufacturing comparator** (F11). Correcting it strengthens the verdict. Against the prompt's own 1e3 J/K floor, the 1 Hz cases exceed it. The answer states this and leaves the choice to the user, which is fair.
- **Anelastic and thermoelastic entropy in Σ̇** (F10). They count as entropy generation, and the answer could say so.

## Claim-by-claim verdicts

| Claim | Verdict | Note |
|---|---|---|
| 1 | Partly agree | Holds at ν ≤ 1 Hz; unconditional last sentence wrong (F3); stretch-corner value pin-joint inflated (F1); TE missing (F4); ratio quoted for 6.63 not 7.4 (F7) |
| 2 | Agree | Form is an identity. Validity should add the cell-scale TE frequency for stretch cells; the BCC E_eff table lacks node effects (F2) |
| 3 | Agree (form) | The no-data octet k_peak (15, 30) is low by about 2 along [100] (F1) |
| 4 | Disagree as stated | c table not bracketed (F2); no mean-stress term while validity fails for typical pairs (F5) |
| 5 | Partly agree | A and B fine; octet values about 2 × high (F1); ordering already demoted |
| 6 | Agree (arithmetic) | Octet row inherits F1 |
| 7 | Agree | Within the model; the cap makes the total depend on ν·τ_s (F3) |
| 8 | Agree (formula) | Octet r² = 1 is pin-only (F1); sheet TPMS can go below 1 (F9) |
| 9 | Agree | Ranking of a closed form |
| 10 | Agree | Conversions checked |
| 11 | Agree, incomplete | Intra-strut values about 1.37 × high for round struts (F8); inter-strut mechanism missing (F4) |
| 12 | Agree | Algebra checks; withdrawal justified |
| 13 | Agree | 0.534 kg |
| 14 | Agree | Reproduced by an independent route |
| 15 | Partly agree | Exponents fine; "r = 1 along [100]" pin-only (F1) |
| 16 | Partly agree | Algebra right; "11.1 to 12.3" not bracketed, 2.7 to 12.3 with node zones (F2) |
| 17 | Partly agree | Numbers reproduce; range and crossover under-bracketed (F2) |
| 18 | Agree | Reproduced by Timoshenko's closed form |
| 19 | Disagree (headline) | No-mean, c = 1 end only (F5) |
| 20 | Agree as a bound pair | Evidence for the no-mean end does not apply to tensile mismatch mean (F5) |
| 21 | Agree | |
| 22 | Agree | Magnitudes only |
| 23 | Agree | Low end shifts to about 10 decades for a rigid octet (F12) |
| 24 | Agree (abstract level) | |
| 25 | Agree (weak) | Basis UNSURE (F15) |
| 26 | Unsupported (ratio part) | Aboulkhair misread (F6); the qualitative statements stand |
| 27 | Agree | |
| 28 | Agree | b anchoring unverified, as stated |

**Q5 defaults.** Dissipation: follows (energy identity), with the ψ caveats of F4 and F10. Life: follows in form; the octet k_peak table must include joint bending (F1); deriving k_peak from measured lattice strength, as the answer prefers, partly absorbs this. Mismatch: does not follow as stated, because of the c bracket (F2) and the missing mean-stress term (F5).

**Q4 materiality verdict.** Follows for 1 per day (robust by four or more orders) and for 1 Hz against LPBF plus primary metal. It does not extend to higher frequencies (F3). Against the prompt's own comparator, the 1 Hz cases are material, which the answer states.

## Citations spot-checked

| Source | Answer's use | Check | Result |
|---|---|---|---|
| Dallago et al. 2018, J. Mech. Behav. Biomed. Mater. 78, 381–394 | No stretch advantage in fully reversed tests | Abstract and highlights via search | Confirmed: the stretch-over-bending advantage was "not found"; sharp notches dominate |
| de Krijger et al. 2017, J. Mech. Behav. Biomed. Mater. 70, 7–16 | Mean stress has little effect | Abstract via search | Confirmed, but for compression–compression, R = 0.1 to 0.8, with R defined on the whole structure. Not transferable to a tensile mismatch mean (F5) |
| Aboulkhair et al. 2016, Mater. Des. 104, 174–182 | As-built σ_w7 ≤ about 31.5 MPa; surface knock-down | Abstract via search; repository page refused access (403) | "As-built" is a heat-treatment condition; machining played a minor role; R not found (F6) |
| Bobbert et al. 2017, Acta Biomater. 53, 572–584 | Up to 60 % of yield for TPMS | Abstract (PubMed text via search) | Confirmed, "some" designs only; basis not stated |
| Hrabe et al. 2011, J. Biomed. Mater. Res. B 99B, 313–320 | 0.15 to 0.25 at 1e6, R = 0.1 | Abstract via search | Confirmed (15 Hz, R = 0.1, compared with 0.4 for solid); normaliser not stated (F15) |
| Ushijima et al. 2011, J. Sandwich Struct. Mater. 13, 303–329 (S3: may not say this) | BCC closed forms, attribution withdrawn | Search records | Euler–Bernoulli analysis of E* and σ_pl confirmed (secondary); exact formulas not seen. The withdrawal is appropriate. Citing papers say shear matters for d/L above about 0.1 |
| Burr et al. 2020 (S3: may not say this) | Removed from the local-stress group | Not re-searched | The answer's restricted use is consistent with S3 |

## What still needs external checking

- **Unit-cell FE** (solid elements, real node geometry, periodic boundaries) for the octet and BCC at ρ̄ = 0.1 to 0.4: k_peak, r², E_eff and equibiaxial c. This settles F1 and F2 and every Q1/Q2 constant. FE is still computation, so its results stay `derived`.
- **Lattice damping**: a frequency sweep from about 0.1 to 100 Hz and an amplitude sweep at strut-level 10 to 60 MPa, on as-built AlSi10Mg octet and BCC coupons, with a solid coupon from the same build. This settles ψ, the convention, F4 and claim 10.
- **S–N of as-built AlSi10Mg thin struts** at R = −1 and in tension with a mean, with the heat-treatment state stated (F6, claim 26, open point 3).
- **Full text** of Aboulkhair 2016 (R, loading mode), Hrabe 2011, Amin Yavari 2013 and Bobbert 2017 (stress basis).
- **Thermal-cycling test** of a co-printed AlSi10Mg lattice on Ti-6Al-4V or Invar, with the stress-free temperature recorded (F5).
- **Gyroid constants** (sheet and skeletal): Yan 2015, Al-Ketan 2018, or FE.

**Single most decisive check:** measure the hysteresis energy per cycle at 1 Hz on an as-built AlSi10Mg octet lattice, cycled at macroscopic amplitudes that put the struts at 20 to 60 MPa, together with its S–N life at those amplitudes. Only a measurement can move the stretch corner, the one place the Q4 verdict is close, off level `derived`. It captures ψ, the cell-scale thermoelastic term and the joint-bending r² in one quantity, ΔS per cycle against N_f.
