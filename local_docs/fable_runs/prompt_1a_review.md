# Review of Prompt 1a answer (reviewer agent)

Date: 2026-11-12

All conclusions here are at level `derived`. They come from my own derivations and scripts and from the writer's scripts. No independent field solver (FEMM, Elmer, FastHenry) and no measurement was used.

Inputs read: the Prompt 1a text block in `local_docs/fable_questions.md`, `local_docs/fable_runs/prompt_1a_answer.md`, and the scripts and outputs in `local_docs/fable_runs/prompt_1a_code/`. My scripts are in `local_docs/fable_runs/prompt_1a_review_code/` (numpy only, standalone). Their outputs are saved in its `outputs/` folder:

| Reviewer script | What it checks |
|---|---|
| `r1_vie_independent.py` | A separately written 2-D volume-integral solver. It uses a numerical self-term, numerical near and far quadrature, and its own mesh and symmetry handling. It is checked against the exact Bessel solution for a round wire. It re-derives the A3 numbers and adds equal-mass copper tubes. |
| `r2_sc_thin_skin.py` | Exact Schwarz–Christoffel map of the exterior of a rectangle. Gives the thin-skin edge factor κ and the logarithmic capacity c, independently of the writer's BEM. |
| `r3_layer_transfer.py` | Exact 1-D layered solutions. Checks Dowell's formula, homogenisation of parallel foil stacks, the strut-level loss ratio, the transposed (Litz) ratio, monotonicity in σ, multi-layer series windings (a regime the writer missed), and the interleaved go/return stacks. |
| `r4_g_factor.py` | Brute-force (FFT filament sum) computation of the field factor g for a uniform-current 100 × 10 mm bundle. |

---

## Summary verdict

1. Reproducibility is clean. All nine writer scripts run from `/` and match the saved outputs line for line (timings excepted). Every number I checked in the answer traces to a script.
2. The central physics holds up against independent checks. My separate 2-D solver reproduces the A3 table within 0.1 %. The exact Schwarz–Christoffel map reproduces κ = 1.561 and c = 29.76 mm within 0.05 %. Exact 1-D solutions confirm homogenisation, Dowell's formula and the Litz ratio. For an isolated (or go/return) bar, a node-connected lattice is worse than solid Cu and solid Al. I found no BLOCKER.
3. Two statements are too broad, and one test is mis-specified (MAJOR). The "no lattice regime beats solid Cu of the same envelope" and "R′ falls monotonically with σ" statements are false in proximity-dominated, series-connected multi-layer windings. There a homogenised Al lattice layer beats a solid Cu layer of the same thickness by up to 2.6×, although a thinner solid foil beats both. The "Al beats Cu" mechanisms (Litz, interleaving) win through topology that copper can use equally. The proposed 3-D FastHenry falsifier cannot reach the regime it is meant to test.
4. The verdict "invalid as stated" is supported. The restated claim is substantially right but imprecise. It should exclude node connectivity, not "the lattice", and it should state the imposed-field exception and the copper-with-same-topology baseline.

## Findings table

| # | Severity | Location in answer | Finding | Evidence / script |
|---|---|---|---|---|
| 1 | MAJOR | A2.1 ("a lattice in a given envelope is always worse"), A2.3 ("No lattice regime beats a solid copper bar of the same envelope"), A5.1 | **The claim is true only for net-current, self-field conductors (isolated bar, go/return pair).** In a series-connected multi-layer winding (Dowell m ≥ 2, field imposed by the other turns), R at fixed thickness is **not** monotone in σ. Low-frequency proximity loss grows like σ·ξ⁴/ξ² ∝ σ, so lowering σ can lower loss. Per-layer results for the same layer thickness: a homogenised Al lattice (σ_eff = 0.3 σ_Al) gives R/R_Cu = 0.61 (m = 4, 100 kHz, h = 0.5 mm), 0.48 (m = 8, same), 0.86 and 0.77 (m = 4 and 8, 10 kHz, h = 2 mm), and 0.79 and 0.38 (m = 4 and 8, 10 kHz, h = 1 mm). The explicit parallel-foil lattice agrees within 2 %. Solid Al also beats solid Cu here (0.74 to 0.99). This does **not** rescue Claim A as a lattice mechanism: in these cases the best *thinner solid* Cu foil gives 0.06 to 0.35 and beats the lattice by 2.3× to 13×. So it is a macro-shape (layer thickness) effect. But the answer's universal statements and its answer to A2's "ANY lattice regime" question are wrong as worded. | `r3_layer_transfer.py` sections D, E |
| 2 | MAJOR | A2.7, A2.8 item 3, A5.3, Verdict ("two connection-topology mechanisms ... let aluminium beat a solid copper bar") | **This compares Al with a topology advantage against Cu without it.** Copper with the same topology wins by 1.26 (thick) to 1.58 (DC-like). Examples: interleaved Cu foils of the writer's geometry ≈ 53.3/1.58 ≈ 34 µΩ/m against 53.3 for Al; ideal Cu Litz at fill 0.3 has R_dc = 55.9 µΩ/m against 88.4 for Al. Neither mechanism is element substitution in the framework's sense. Each is a reason the *incumbent* should not be a solid bar. A related gap: at equal mass **and** equal envelope at 100 kHz, a Cu tube (wall 0.414 mm, 0.81 kg/m) gives 541 µΩ/m. The equal-mass Al tube gives 710 and the lattice 1294. The Cu tube even beats the solid Cu bar (565). At 10 kHz the order reverses (Al tube 212, Cu tube 265). With each metal's optimal wall (1.6 δ), R × mass is 158 (Al) against 341 (Cu) µΩ·kg/m² at 100 kHz. That is the DC figure of merit ρ_m/σ (ratio 2.09) again. The A2.8(5) R × mass ranking is given at 10 kHz only and omits the Cu thin-wall section. | `r1_vie_independent.py`; writer `a2_sigma_sweep_tubes.py` §3 (Al 1.6 δ tube, 659.35 µΩ/m, 0.24 kg/m) |
| 3 | MAJOR | A4.2 (FastHenry setup and falsifier) | **The proposed 3-D falsifier cannot reach its own regime.** Its lattice is 4 cells across the thickness (pitch 0.5 mm). The falsifier requires thickness ≥ 6 δ_eff *and* struts thinner than δ. With 4 cells, T ≥ 6 δ_eff means pitch ≥ 1.5 δ_eff. For square axial strands, t/δ = pitch/δ_eff (the writer's own identity in A2.2a), so t/δ ≥ 1.5. The two conditions cannot hold together. It also contradicts A2.2(b) ("fewer than about five cells across ... no scale separation"). Since A1.5 (3-D nodes and transverse struts) is the one part not computed at all, it needs a valid test: at least 12 cells across the thickness with pitch ≤ δ_eff/2. | Arithmetic from A2.2(a) and A4.2 |
| 4 | MAJOR | Verdict, restated claim | **The scope is placed on the wrong property.** "Removing the lattice" should be "removing node connectivity / parallel connection". An additively manufactured architected geometry of mutually insulated, transposed strands (a printed Litz-like or braided structure) is an architected geometry that realises mechanism A5.3. The restated claim also omits finding 1's imposed-field exception and finding 2's same-topology Cu baseline. Smaller imprecisions: "26 % more perimeter" is 26 % more *width* (perimeter +23.6 %, 272 against 220 mm). The "penalty of 1.26 at equal envelope" holds only in the thick limit, rising towards 1.58 when the bar is thinner than about 2 δ. "Only a surface layer of about 1.6 δ carries current" is the 1-D optimum wall for one-sided field, not a current-carrying depth. | Answer text; `a2_sigma_sweep_tubes.py` §3 |
| 5 | MINOR | A3.4 ("two methods agree within 2.4 %") | The BEM (δ → 0) and the volume solver (finite δ) solve different problems. The 2.4 % is a physical finite-δ effect plus an extrapolation argument, not an agreement test. For the square, which the writer does not report, the deficit is non-monotone in b/δ: −0.005, +0.026, +0.027, +0.021. The numbers themselves are right. My Schwarz–Christoffel map gives κ = 1.5606 against BEM 1.5611 to 1.5618, and c = 29.7647 against 29.7646 mm. My independent volume solver matches the finite-δ values within 0.1 %. | `r2_sc_thin_skin.py`, `r1_vie_independent.py`, writer `a2_hf_limit_bem.txt` §4 |
| 6 | MINOR | A1.1, A2.7 (interleaved foils, "1-D model ... within 1.1 %") | The "corrected 1-D model" assumes interior foils carry twice the end-foil current. That is the thick-foil limit. Thin foils share equally. The exact 1-D parallel-connected solution gives 57.07, 53.29, 107.79 and 53.99 µΩ/m. The writer's 2-D values are 56.89, 53.28, 107.14 and 53.96 (within 0.6 %). The model gives 56.91, 53.72, 107.79 and 54.02. The conclusion is unaffected. The 2-D go/return solver is confirmed. | `r3_layer_transfer.py` §F |
| 7 | MINOR | A1.4 ("under 5 % of the loss") | The strut-level ratio ρ̄(t/δ)²/6 is exact to leading order: the 1-D intra-foil share matches to 4 digits for t/δ ≤ 0.4. It underestimates near t/δ ≈ 1: 0.060 against 0.040 at t/δ = 0.89. At 100 kHz the share is therefore about 6 %, not 3.9 %. Separately, the net explicit-minus-homogenised difference is dominated by an opposite-sign discreteness term of order (pitch/δ_eff)²: −5 % for 1-D foils at t/δ = 0.28. The answer gets the sign right in A2.2, but the A1.4 text could be read as if the strut term were the whole deviation. | `r3_layer_transfer.py` §B, §G |
| 8 | MINOR | A2.4, A2.7 (Litz formula; "fully resolved ≈ 484 / 660 µΩ/m") | The 1-D part of the formula is exact for t/δ ≤ 0.4 but 3 % high at t/δ = 0.89 (exact 2.863 against 2.949). The 100 kHz "fully resolved" extrapolations are therefore slightly high. The 2 × 2 and 3 × 3 sub-cell agreement is partly by construction: both are dipole-level approximations. g = 1.552 is confirmed (0.7762 + 0.7762). "Exactly as much" is right to four digits for 10:1 but is not an identity: for 100 × 1 the components are 0.960 and 0.963. The writer's g = 1.910 for 100 × 1 is under-resolved (my value is about 1.925). It is not used anywhere. | `r3_layer_transfer.py` §C, `r4_g_factor.py` |
| 9 | MINOR | A2.1, A3.5, citation 15 (AlSi10Mg conductivity) | Primary sources exist: the EOS AlSi10Mg datasheet (about 25 % IACS as built, about 44 % IACS heat-treated) and Silbernagel et al. 2018, "Electrical resistivity of additively manufactured AlSi10Mg for use in electric motors", Additive Manufacturing 21. I verified existence only. At 25 % IACS against the 65 % IACS assumed (3.77e7 S/m), the thick-limit penalty is sqrt(65/25) = 1.61, not "up to about 1.4". The conclusion moves further against the lattice. | Web search (titles only) |
| 10 | MINOR | A2.3, A2.2 (100 kHz explicit bundles) | The sub-cell resolution check covers 10 kHz with t/δ ≤ 1.67 only. The 100 kHz thick-strand cases (t/δ 2.1 to 5.3) use uniform sub-cells up to 0.45 δ and are not convergence-tested. The ranking margin (≥ 1.5 × Cu) is far larger than any plausible error. | writer `a2_strand_bundle_scan.txt` |
| 11 | MINOR | A1.2 table | The "factor 13.9" at 100 kHz uses the homogenised 1293 µΩ/m. Against the explicit strands (1143) it is 12.3. The direction and conclusion are unchanged. | writer outputs |

No BLOCKER: no number in the answer is irreproducible, and no derivation I checked is wrong in a way that changes the verdict on Claim A.

## Reproducibility table

All runs: `python3 <absolute path>` from `/`, Python 3, numpy 2.x. "Identical" means a line-by-line diff of stdout against `outputs/*.txt`, with timing brackets ignored.

| Script | Run time here | Matches saved output | Answer numbers traced to it | Mismatch |
|---|---|---|---|---|
| `eddy2d.py` | 18 s | identical | round wire 1.8032 to 1.8084 / 3.6923 to 3.6991, DC 16.78 | none |
| `a1_analytic_numbers.py` | 2 s | identical | δ table, F(ξ) facts, 88.5/93.0, 4.7/13.9, 0.34/0.69 and 0.11/0.23, 0.4 %/3.9 %, Litz 90.7/117.1, d = 0.125 mm, g = 1.552 | none |
| `a3_busbar_rac.py` | 54 s | identical | full A3 tables, R × mass, mesh spread ≤ 0.25 % (max lvl1→lvl2 0.25 %, Al tube 10 kHz) | none |
| `a3_go_return_sensitivity.py` | 38 s | identical | A3.5 values, +30 % / +5 %, ratio change < 3 % (worst −2.8 %) | none |
| `a2_sigma_sweep_tubes.py` | 16 s | identical | monotonicity (16 + 16 points), 210.4 against 224.7 (−6.3 %), 126 mm tube 175.3/549.6 at 0.94/0.30 kg/m | none |
| `a2_hf_limit_bem.py` | 8 s | identical | κ 1.561, c 29.76 mm, 0.753, 0.947, deficits 0.036/0.028/0.021 | none |
| `a2_laminations.py` | 2 min 43 s | identical | 231/235 and 720/720, interleaved 56.89 … 53.96, 204.9 | none |
| `a2_strand_bundle_scan.py` | 7 min 17 s | identical | 409.4 against 414.5 (1.2 %), A2.2 table, 26 bundles, min 1.02 × Al and 1.29 × Cu, 1143.3, 0.36 %/3.9 % | none |
| `a2_transposed_bundle.py` | 3 min 54 s (about 2 GB) | identical | 91.4, 382, 586, 0.034/3.33/0.057/5.63 | none |

Numbers in the answer that no script prints directly but that follow by arithmetic from printed values: 1.95× (178.44/91.38), 4.5× (409/91), the "484" and "660" extrapolations (88.42 × (1 + 4.476) and 88.42 × (1 + 6.446)), and "10 %/3 % of its mass" (0.94/8.96, 0.30/8.96). Two statements are not computed by any script: "at 100 kHz a copper wall of 1.6 δ = 0.33 mm would be enough, about 7 %" and "1/(σδP) is 34 % low". My `r1` confirms the first: a Cu tube with a 1.6 δ wall gives 524.8 µΩ/m at 0.65 kg/m (7.3 % of the mass), 7 % below the solid bar. The second is 1 − 1/1.525 = 34 % ✓.

Independent re-derivation of the key 2-D values (`r1_vie_independent.py`, fine mesh, relative to the writer): solid Cu 178.36 (−0.05 %) and 564.51 (−0.03 %); lattice 0.3 σ_Al 414.10 (−0.09 %) and 1293.95 (−0.02 %); equal-mass Al tube 211.91 (−0.10 %) and 709.67 (+0.04 %); round wire within 0.2 % of Bessel. Note on S16: my first run disagreed by 5 % on the 100 kHz tube. The cause was a mesh-grading bug in **my** code (wall cells coarsest at the wall faces). Only the disagreement exposed it. That is the practical case for a third, external solver.

## Derivation checks

**D1. Claim A's formula (A1.1).** Confirmed. F(ξ) = ξ(sinh 2ξ + sin 2ξ)/(cosh 2ξ − cos 2ξ) is the m = 1 term of Dowell's formula: a foil carrying net current with tangential H = I/w on one face and 0 on the other. It is also the classical deep-slot conductor case. The exact 1-D solution reproduces Dowell to 4 decimals for m = 1, 2, 4 and ξ = 0.3 to 3 (`r3` §A). The small-ξ form 1 + 4ξ⁴/45 and the minimum of F/ξ (0.9172 at ξ = π/2) are correct. Using ξ = t/(2δ) for an isolated plate is correct.

**D2. Homogenisation σ_eff = ρ̄σ/τ (A2.1).** Confirmed for z-invariant structures. In a 2-D TM problem (E = E_z ẑ) only σ_zz enters, so transverse struts and nodes do not change the bar-scale equation. Transverse struts carry no net current far from the ends, because the transverse line integral of E vanishes when A is axial and φ is common. The bound σ_zz ≤ ρ̄σ (all metal axial) is the Wiener parallel bound. The isotropic HS value 2ρ̄/(3 − ρ̄) is correctly computed. Exact 1-D foil stacks converge to the homogenised slab as t/δ → 0 and lie below it by about 0.63 (t/δ)² ≈ 0.19 (pitch/δ_eff)² (`r3` §B). This is consistent with the writer's 2-D bundle (−1.2 % at t/δ = 0.28, where pitch/δ_eff is smaller for square strands). In the thick limit R′ ∝ κ/(σ_eff δ_eff P) ∝ 1/sqrt(σ_eff). κ depends only on shape. Monotone decrease of R with σ is confirmed for isolated and one-sided 1-D slabs (60-point sweeps, `r3` §D) and for the writer's bar (16 + 16 points). It is **not** general: see finding 1.

**D3. Capacity lower bound R′ ≥ R_s/(2πc) for parallel-connected (non-transposed) structures (A2.5).** The proof is correct as sketched, and I re-derived each step. (i) In the thin-skin limit with all conductors in parallel, jωA = V′ on every surface, so A is one constant on all of K. Outside, A = A₀ − (μ₀I/2π)g, with g the Green's function with pole at ∞. (ii) The surface current is K = (I/2π)|∇g|, so R′ = R_s∮|∇g|²dl/(2π)² for peak or rms used consistently. (iii) ∇g = Re-part of h′ with h′ analytic and single-valued even for a multiply connected exterior. So u = ln|h′| + g is subharmonic, and u → −ln c at ∞ (z·h′ → 1). (iv) The sub-mean property with harmonic measure dω = |∇g|dl/2π gives −ln c ≤ ∫ln|∇g|dω. Jensen then gives 1/c ≤ ∮|∇g|²dl/2π. (v) Capacity is monotone under set inclusion. Numerically, the exact Schwarz–Christoffel map gives c = 29.7647 mm and κ = 1.5606, so the bound ratio is 0.7538 (writer 0.7535) and 0.9477 for any Al structure against the solid Cu bar (`r2`). Scope: thin-skin limit, isolated parallel-connected set, one material. It does not cover finite δ (the 1.57 δ wall gains about 6 to 8 %) or imposed external fields (finding 1). **Holds** within that scope.

**D4. Strut-level loss ratio ρ̄(t/δ)²/6 (A1.4).** Re-derived. For a thin strut in a uniform transverse field Ĥ (peak), E_z = jωμ₀Ĥx, so P′ = σω²μ₀²Ĥ²t⁴/24 (∫x²dA = t⁴/12). The number of struts per unit area is ρ̄/t², and ∫|H|²dy over the decay depth is |H₀|²δ_eff/2. The bar loss per unit area is |H₀|²/(2σ_effδ_eff). The ratio is ρ̄σω μ₀ t²/12 = ρ̄(t/δ)²/6 ✓. For round struts it is ρ̄(d/δ)²/8 ✓. The capture factors 0.75 (2 × 2) and 8/9 (3 × 3) are correct. The exact 1-D intra-foil share matches the formula to 4 digits for t/δ ≤ 0.4 and is 50 % higher at t/δ = 0.89 (`r3` §G). **Holds** for t/δ ≲ 0.5. It is an underestimate near t/δ ≈ 1.

**D5. Litz proximity ratio g ρ̄²T²d²/(48δ⁴), g = 1.55 (A2.4).** Re-derived. With uniform macroscopic J₀ and the 1-D field ⟨H²⟩ = J₀²T²/12, the strand loss per unit volume is ρ̄σω²μ₀²⟨H²⟩d²/32 (round) and the DC loss is J₀²/(2ρ̄σ). Their ratio is ρ̄²T²d²/(48δ⁴) (round) and ρ̄²T²t²/(36δ⁴) (square) ✓. The exact 1-D equal-current stack matches the square form for t/δ ≤ 0.4 and is 3 % lower at 0.89 (`r3` §C). g by brute force is 1.5524 (`r4`). In the thin-strip limit the normal component's mean square equals the 1-D value (the mean of ln²((1+u)/(1−u)) over (−1, 1) is π²/3), hence g → 2 ✓. **Holds** for d/δ ≲ 0.5 under ideal transposition. Bundle-level transposition imperfections are not included, and the writer says so.

**D6. Solver soundness (eddy2d.py).** The formulation J/σ + jωA = V′ with A = −(μ₀/2π)∫J ln|r − r′| is correct. The closed-form cell integral is correct (V1 matches quadrature to 8 digits), and the self-term at the cell centre is the exact integral. The free-space log reference (1 m) only shifts Im Z, so R is gauge-independent. Using peak phasors throughout, R = Re(V′/I) = P/|I|² is consistent, and P′ = R·I_rms² is correct. Quarter-symmetry images are correct for even (isolated) and odd-in-y (go/return) cases. I checked the per-polarity bookkeeping in the interleaved stack (I_go = 2Σ sign·J·a, P_go = half the total) and it is right. Current constraints are right: a common V′ for parallel, a per-strand V′ with unit current for transposed. Mesh convergence is ≤ 0.25 % (lvl1→lvl2). The round-wire validation tests the kernel, self-term, image handling and finite-δ accuracy at δ/9 to δ/4 resolution. It does **not** test corner or edge crowding or graded high-aspect cells. Those are covered by my independent `r1` (≤ 0.1 %) and by the δ → 0 limit (`r2`).

## Missed regimes

| Regime (from the brief) | Does it rescue Claim A? | Evidence |
|---|---|---|
| Lattice thinner than δ_eff (DC-like) | No. Monotone in σ for self-field conductors, so the penalty rises towards σ_Cu/σ_eff = 5.27 (fill 0.3, τ = 1). The writer covered this. | writer `a2_sigma_sweep_tubes.py` §1; `r3` §D |
| Anisotropic lattice, aligned axial paths, no transverse struts | No. This is exactly the writer's insulated parallel strand bundle: ≥ 1.29 × Cu (fill 0.85), ≥ 1.5 × Cu (fill 0.3). In exact 1-D foil stacks (full-width foils, effectively a hollow section) the minimum is 1.17 × Cu. | writer `a2_strand_bundle_scan.txt`; `r3` §B |
| Field not one-sided: imposed external field, multi-layer series winding | **Partly. This is the one regime the writer missed.** A homogenised Al lattice layer beats a solid Cu layer of the same thickness by up to 2.6× (m = 8, 10 kHz, h = 1 mm: 0.38). A thinner solid Cu foil does much better (0.13 in that case), so the gain is macro-shape (layer thickness), not lattice. A node-connected lattice is never the optimum. | `r3` §E (finding 1) |
| Go/return pair (field one-sided per bar) | No. Ratios unchanged within 3 %. | writer `a3_go_return_sensitivity.txt` |
| Very high frequency (δ smaller than struts) | No. The capacity bound caps any parallel-connected reshaping at 0.754 × solid of the same metal, and 0.948 × solid Cu for Al. | `r2`, D3 |
| Equal mass instead of equal envelope | The lattice still loses: the equal-mass Al tube has about half its R. Between metals, at equal mass and envelope the winner depends on frequency (Al tube 212 against Cu tube 265 µΩ/m at 10 kHz; Cu 541 against Al 710 at 100 kHz). With optimal walls, Al is 2.1× better in R × mass at any frequency (ρ_m/σ). | `r1`; finding 2 |
| Equal cost | Not computed. Al is cheaper per kg than Cu, which strengthens the Al thin-wall section, not the lattice (AM lattices add manufacturing cost, and the Al tube dominates the lattice at equal mass). | qualitative |
| Printed alloy conductivity | Against the lattice: AlSi10Mg at about 25 to 44 % IACS. | finding 9 |

## Claims: agree / disagree / unsupported

| Claim | Verdict | Reason |
|---|---|---|
| A1.1 | Agree | D1; `r3` §A. Minor caveat about the "corrected" model (finding 6). |
| A1.2 | Agree | Numbers reproduced. Factor 12.3 rather than 13.9 against the explicit strands (finding 11). |
| A1.3 | Agree | The two-scale model is standard and consistent with D2/D4. |
| A1.4 | Agree, with qualification | Formula right for t/δ ≲ 0.5. At 100 kHz the share is about 6 % (finding 7). |
| A1.5 | Unsupported (plausible) | Not computed. The argument is sound for the z-invariant interior, and the proposed falsifier is invalid (finding 3). |
| A2.1 | Agree within scope, disagree as worded | Correct for self-field conductors. "Always worse" fails for imposed-field windings (finding 1). |
| A2.2 | Agree | Reproduced. My 1-D result shows the same sign and scaling. (b) to (d) are qualitative. |
| A2.3 | Disagree as worded, agree for isolated or go/return bars | Finding 1. |
| A2.4 | Agree | 10 kHz value solid. 100 kHz extrapolations a few % high (finding 8). |
| A2.5 | Agree | Proof checked (D3). Numbers confirmed by an independent method (`r2`). |
| A2.6 | Agree | Values reproduced. The table lacks a Cu thin-wall section at equal mass (finding 2). |
| A2.7 | Agree on physics, disagree on framing | Topology is available to Cu too (finding 2). |
| A2.8 | Mostly agree | Item 3 is overstated (finding 2). Item 5 is incomplete at 100 kHz (finding 2). Item 1 is correct. |
| A3.3a / A3.3b | Agree | Reproduced by `r1` within 0.1 %. |
| A3.4 | Agree on numbers, disagree on the "agree within 2.4 %" description | Finding 5. |
| A3.5 | Agree | Reproduced. The material-conductivity penalty is underestimated (finding 9). |
| A4.1 | Agree | A reasonable setup. In FEMM, case 4 is simpler as one *series* circuit over all strand blocks (equal current per block). FEMM's licence is not OSI open source to my knowledge (UNSURE); Elmer and GetDP are suitable fallbacks. |
| A4.2 | Disagree | The falsifier cannot be met (finding 3). |
| A4.3 | Agree | Sound in principle. |
| A5.1 | Agree for the stated case (busbar in self-field) | It needs the imposed-field caveat. |
| A5.2 | Agree, imprecise | Finding 4 ("26 % more perimeter", 1.26 thick-limit only). |
| A5.3 | Agree on physics, disagree on framing | Finding 2. |
| A5.4 | Agree | δ_Cu(5 kHz) = 0.922 mm. |
| A5.5 | Agree | — |
| Verdict | Supported: "invalid as stated". | Restated claim: see finding 4. A more precise version: "For a conductor in its own field, subdividing the cross-section into parallel-connected (node-connected) paths cannot lower AC resistance below that of the solid of the same metal and envelope by more than a few per cent at finite δ, or by more than 25 % in the thin-skin limit. A lattice of fill ρ̄ raises it by sqrt(σ/σ_eff) to σ/σ_eff. In the skin-limited regime Al costs a factor 1.26 at equal shape (up to 1.58 when thinner than about 2 δ) and can match Cu with about 24 % more perimeter at about half the mass of an optimal-wall Cu section. Transposition of insulated strands or go/return interleaving lowers AC resistance for either metal and does not change the Cu/Al ratio. In imposed-field (proximity-dominated) windings a lower σ_eff can lower loss at fixed layer thickness, but a thinner solid layer does better." |

## Citations

Checked by web search of titles, authors and physics terms only, on 2026-11-12. I did not open full texts, so "supports" means the abstract or bibliographic record is consistent with the use.

| # | Citation | Status | Note |
|---|---|---|---|
| 1 | Dowell 1966, Proc. IEE 113(8) 1387–1394 | verified | Layer model for multilayer windings; supports the use. |
| 2 | Ferreira 1994, IEEE TPEL 9(1) 127–131 | verified | The abstract states the skin/proximity orthogonality. |
| 3 | Sullivan 1999, IEEE TPEL 14(2) 283–291 | verified | Litz strand proximity analysis. |
| 4 | Sullivan 2008, IEEE TPEL 23(4) 2044–2051 | verified | The abstract supports "Al resistivity matters less at high frequency". This paper also supports finding 1 (Al vs Cu in proximity-dominated windings); per the abstract only, that point is UNSURE. |
| 5 | Silvester 1967, IEEE PAS-86(6) 770–774 | verified | Its curves claim about 0.5 % accuracy for R. They would be an external anchor for the solid-bar values, but neither writer nor reviewer compared against them. |
| 6 | Weeks et al. 1979, IBM J. R&D 23(6) 652–660 | verified | Filament method. |
| 7 | Gyselinck & Dular 2005, IEEE Trans. Magn. 41(5) 1416–1419 | verified | Homogenisation of wire bundles. |
| 8 | Meeker 2012, J. Comput. Appl. Math. | verified (existence, DOI 10.1016/j.cam.2012.04.009) | Volume and pages UNSURE, as the writer says. |
| 9 | Hashin & Shtrikman 1962, J. Appl. Phys. 33(10) 3125–3131 | verified | The abstract states the bounds transfer to electrical conductivity. |
| 10 | Lemlich 1978 (some sources 1977), J. Colloid Interface Sci. 64, 107 | verified via citing works | σ ≈ φ/3 for dry foam (Phelan et al. citing it). The year ambiguity is as the writer notes. |
| 11 | Morgan 1949, J. Appl. Phys. 20(4) 352–362 | verified | The abstract: parallel grooves raise loss about one-third as much as transverse. Supports the use. |
| 12 | Kamon, Tsuk, White 1994, IEEE MTT 42(9) 1750–1758 | verified | — |
| 13 | Meeker 2013, IEEE Trans. Magn. 49(10) 5243–5247 | verified | The writer's recalled volume and pages are correct. |
| 14 | Dwight 1918, AIEE | verified (two index records: Trans. pp. 1379–1403 and Proc. 37(8) 977–998) | As the writer says. |
| 15 | AlSi10Mg about 30 % IACS | resolvable | EOS datasheet (about 25 % as built, 44 % heat-treated) and Silbernagel et al. 2018, Additive Manufacturing 21 (existence only, values from the snippet). See finding 9. |

## What still needs external checking

Every conclusion above, the writer's and mine, is at level `derived`. Agreement between us is not validation. My `r1` uses the same integral-equation physics as `eddy2d.py`, so it checks the implementation, not the formulation.

Still needs an independent field solver or a measurement:

1. **3-D node-connected lattice (A1.5, A4.2).** This is the only part where the lattice geometry itself was never computed. It needs FastHenry or a 3-D FEM with **≥ 12 cells across the thickness** and pitch ≤ δ_eff/2 at T ≥ 6 δ_eff (finding 3).
2. Absolute 2-D values for the solid and tube rows (FEMM, Elmer or GetDP, or Silvester 1967's published curves for the solid bars).
3. The imposed-field multi-layer regime (finding 1): a 2-D FEM of an m = 4 layer winding in a core window with Cu layers, Al layers, an Al lattice and thin solid foils.
4. Real AM Al lattice conductivity and surface/strut defects (measurement).
5. 100 kHz transposed bundle and thick-strand bundle convergence (findings 8, 10). These do not change the ranking.

**Single most decisive check:** a 3-D solution (FastHenry, or Elmer in 3-D) of a node-connected simple-cubic aluminium lattice bar with at least 12 cells across the thickness. Sweep frequency so that T/δ_eff runs from 0.5 to 10. Compare R_ac/R_dc with the homogenised solid of equal DC resistance, and R_ac with a solid Cu bar of the same envelope. The verdict on Claim A is falsified if the lattice's R_ac/R_dc lies well below (more than about 20 %) the equal-DC solid's at T ≥ 6 δ_eff with struts thinner than δ, or if its R_ac falls below the solid Cu bar's at any frequency. This is the only test that probes what makes a lattice different from the z-invariant bundles both of us computed.
