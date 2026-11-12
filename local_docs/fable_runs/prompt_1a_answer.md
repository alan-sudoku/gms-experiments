# Answer to Prompt 1a (writer agent)

Date: 2026-11-12

Note: every claim in this file is unverified (level `derived`). The numbers come from my own scripts and my own derivations. No independent tool, measurement or second person has checked them.

Answered from the prompt text alone. No other repository file was read.

---

## 0. Short version, conventions, and where the code is

**Short version.** Claim A is wrong for a lattice. Its formula describes one flat foil in a one-dimensional field, and it is applied to each strut as if that strut were alone. In a lattice all struts are joined in parallel at every node, so the current distributes itself over the cross-section of the whole bar, and the skin effect appears at the scale of the bar with a skin depth set by the effective conductivity. Thin struts do not prevent this. For the 10 mm × 100 mm envelope, an aluminium lattice at relative density 0.3 has 2.0 to 4.0 times the AC resistance of solid copper and 1.6 to 3.2 times that of solid aluminium. The prompt's suspicion is correct in substance. It is incomplete in several ways, listed in A2.8. The most important one: there are two real ways in which geometry lets aluminium beat a solid copper bar (transposed insulated strands, and interleaving go and return foils), and a third in which shape lets aluminium match copper (more perimeter, wall of about 1.6 skin depths). None of the three is a lattice.

**Conventions.**

- R′ is AC resistance per metre, in µΩ/m. Dissipation at I_rms = 1 kA is P′ = R′·I² in W/m (numerically equal to R′ in µΩ/m). Σ̇ = P′/T₀ with T₀ = 298.15 K (my assumption; the prompt does not give T₀).
- δ = sqrt(1/(π f μ₀ σ)). Conductivities as given in the prompt, taken as 20 °C values: σ_Cu = 5.96e7 S/m, σ_Al = 3.77e7 S/m. μ = μ₀ everywhere.
- Envelope: width W = 100 mm, thickness T = 10 mm, area A = 1000 mm², perimeter P = 220 mm.
- "Fill" or ρ̄ is the metal area fraction. σ_eff is the effective conductivity along the bar axis.
- "Isolated bar" means the return conductor is far away. A3.5 quantifies what changes when it is close.
- "Thin-skin limit" means every conductor dimension is much larger than δ.
- κ ("edge factor") is the ratio of the true thick-bar resistance to the naive estimate 1/(σ δ P). It exceeds 1 because current crowds towards the narrow edges of a flat bar.

**Code.** Every number in this answer is printed by a script saved in `local_docs/fable_runs/prompt_1a_code/`. Each script runs standalone with `python3 <script>` from any directory and needs only numpy. Saved outputs are in `local_docs/fable_runs/prompt_1a_code/outputs/` under the same name with extension `.txt`.

| Script (in `local_docs/fable_runs/prompt_1a_code/`) | What it produces | Used in |
|---|---|---|
| `eddy2d.py` | The 2-D field solver (module). Run directly: three validation cases | all |
| `a1_analytic_numbers.py` | Skin depths, Claim A's formula, what the claim predicts, Litz estimate, strut-level loss estimate | A1, A2.7, A3 |
| `a3_busbar_rac.py` | The A3 table, three mesh levels | A3, A2.1, A2.6 |
| `a3_go_return_sensitivity.py` | Same conductors with a nearby return conductor | A3.5 |
| `a2_strand_bundle_scan.py` | Explicit strand bundles compared with the homogenised bar | A2.1 to A2.3, A1.4 |
| `a2_transposed_bundle.py` | The same bundle with equal strand currents (ideal transposition) | A2.4 |
| `a2_laminations.py` | Laminated strips, not interleaved and interleaved | A1.1, A2.6 |
| `a2_sigma_sweep_tubes.py` | R′ against conductivity; tube wall sweep; wider aluminium tubes | A2.1, A2.5, A2.6 |
| `a2_hf_limit_bem.py` | Independent thin-skin boundary-element check; capacity bound | A2.5, A3.4 |

---

## A1. Is the quoted R_ac expression the right model for a lattice of struts?

**A1.1. The quoted expression is the one-dimensional solution for a flat foil with magnetic field on one face only.**
The factor F(ξ) = ξ·[sinh 2ξ + sin 2ξ]/[cosh 2ξ − cos 2ξ] is R_ac/R_dc for a flat conductor of thickness t_w, much wider than it is thick, carrying a net current, with tangential field H = I/width on one face and H = 0 on the other. It is the first term of Dowell's layer formula, which is all that remains for a single layer (m = 1):

F_R = ξ·{ [sinh 2ξ + sin 2ξ]/[cosh 2ξ − cos 2ξ] + (2(m² − 1)/3)·[sinh ξ − sin ξ]/[cosh ξ + cos ξ] } (Dowell 1966; equation number not checked against the paper).

Three consequences that the claim does not state:

- For an isolated plate with field on both faces, each half behaves like a foil with field on one face, so the formula applies with ξ = t/(2δ), not t/δ.
- For small ξ, F ≈ 1 + 4ξ⁴/45. For ξ < 1 the formula returns essentially the DC resistance (F = 1.052 at ξ = 0.88).
- F/ξ has a minimum of 0.917 at ξ = π/2. A wall of 1.57 δ has 8 % less resistance than an infinitely thick one.

Check performed: in a stack of interleaved go and return foils the 2-D field solution agrees within 1.1 % with a 1-D model built from this formula (interior foils with ξ = t/2δ, end foils with ξ = t/δ): 56.89 against 56.91, 53.28 against 53.72, 107.14 against 107.79, and 53.96 against 54.02 µΩ/m (`a2_laminations.py`). Applying the formula with ξ = t/δ to every foil, as Claim A writes it, gives 204.9 instead of 107.1 µΩ/m for 1 mm foils at 100 kHz.

- Confidence: high.
- Falsifier: a 1-D finite-difference solution of d²H/dy² = jωμσH across a foil with H = I/w on one face and 0 on the other that does not reproduce F(ξ) to solver accuracy.

**A1.2. It is not the right model for a lattice, and using it reverses the conclusion.**
The formula assumes that the only field at the conductor is the field of its own current. Two things are missing:

1. Each strut sits in the field of the current in all the other struts. That field is set by the total current of the bar, not by the strut.
2. The struts are connected in parallel (in a lattice, at every node). How the total current divides among them is decided by the flux each one links. Struts near the surface link less flux and take most of the current. This is the skin effect at the scale of the bar, and no property of an individual strut removes it.

Size of the error for the A3 case, with struts of 0.228 mm (`a1_analytic_numbers.py`, section 3):

| | 10 kHz | 100 kHz |
|---|---|---|
| Lattice R′ according to Claim A (F(ξ)·R_dc, ξ = t_w/δ_Al) | 88.5 µΩ/m | 93.0 µΩ/m |
| Lattice R′ from the field solution (homogenised, σ_eff = 0.3 σ_Al) | 414 µΩ/m | 1293 µΩ/m |
| Factor by which Claim A underestimates | 4.7 | 13.9 |
| R_lattice/R_solid Cu according to Claim A (Cu bar as a 1-D plate, field on one face / on both faces) | 0.34 / 0.69 | 0.11 / 0.23 |
| R_lattice/R_solid Cu from the field solution | 2.32 | 2.29 |

- Confidence: high.
- Falsifier: a 2-D finite-element harmonic solution of a bundle of thin parallel aluminium strands filling the envelope (the setup in A4) that returns an R′ close to its DC value at 10 kHz.

**A1.3. What replaces it: a two-scale model.**

*Bar scale.* Replace the lattice by a homogeneous conductor with an effective conductivity tensor and μ = μ₀. For a long straight bar only the axial component σ_eff matters, because the electric field is purely axial. Solve the bar-scale eddy-current problem

∇²E_z = jωμ₀σ_eff·E_z inside, with the open-boundary field outside,

which gives δ_eff = sqrt(1/(π f μ₀ σ_eff)) and, when the bar is thicker than about 3 δ_eff,

R′ ≈ κ/(σ_eff · δ_eff · P) = κ·sqrt(π f μ₀/σ_eff)/P.

*Strut scale.* Add the loss of each strut in the local transverse field Ĥ (peak value) of the bar-scale solution. This is the proximity effect between struts. For a strut much thinner than δ the loss per unit length is

P′_strut = σ ω² μ₀² Ĥ² t⁴/24 (square strut of side t), or π σ ω² μ₀² Ĥ² d⁴/128 (round strut of diameter d).

The round-strut expression is the standard low-frequency strand loss used for Litz wire (Sullivan 1999; equation number not checked). The square-strut expression is my derivation: ∫x² dA = t⁴/12 over the section. For struts that are not thin, the exact round-wire result uses Bessel functions, and the separation into a "skin" part and a "proximity" part that can be added is the orthogonality shown by Ferreira (1994). An equivalent packaging is a complex effective permeability for the strand region (Gyselinck and Dular 2005; Meeker 2012). Those two papers treat windings whose turns are in series; for a lattice the net current distribution must come from the bar-scale problem above, and only the permeability part carries over.

- Confidence: high for structures that are uniform along the bar; medium for a real 3-D lattice (see A1.5).
- Falsifier: the explicit strand computation in A2.1 disagreeing with the homogenised bar when the pitch is much smaller than δ_eff. It agrees within 1.2 %.

**A1.4. Strut-level eddy loss is small when t_w < δ, so the claim's premise is true and nearly irrelevant.**
Integrating the strut loss of A1.3 over the depth δ_eff/2 in which the field decays, and dividing by the bar-scale loss, gives (my derivation)

strut-level loss / bar-scale loss ≈ ρ̄·(t/δ)²/6 for square struts, ρ̄·(d/δ)²/8 for round struts.

At ρ̄ = 0.3 this is 0.4 % for t = 0.228 mm at 10 kHz and 3.9 % at 100 kHz (`a1_analytic_numbers.py`, section 5). The field solution agrees: resolving each strand with 2 × 2 cells instead of 1 raises R′ by 0.36 % at 10 kHz and 3.9 % at 100 kHz (`a2_strand_bundle_scan.py`, last block; 2 × 2 cells capture about 75 % of the dipole loss and also some skin effect inside the strand, so the agreement is in order of magnitude only).

So "struts thinner than δ suppress eddy currents inside each strut" is correct. Those currents account for under 5 % of the loss. The other 95 % is the bar-scale skin effect, which strut thickness does not touch.

- Confidence: medium (own derivation, coarse numerical check).
- Falsifier: a finite-element model with finely meshed round strands in which the strand-level share of the loss exceeds about twice the estimate for d < δ and pitch below δ_eff/2.

**A1.5. Transverse struts and nodes (the 3-D part of a real lattice) do not help.**
In a long straight bar the transverse struts carry no net current, by symmetry. They are metal that does not conduct along the bar, which is exactly what the tortuosity factor counts. The nodes connect every strut to its neighbours once per cell, which is the opposite of the strand insulation that Litz wire needs. The loops formed by axial and transverse struts link the transverse magnetic flux, and the currents they carry are the bar-scale skin effect itself, already counted in A1.3. They are not an extra mechanism.

- Confidence: medium. I did not solve a 3-D lattice.
- Falsifier: a 3-D solution (FastHenry setup in A4) of a node-connected lattice whose R_ac/R_dc at thickness ≥ 6 δ_eff lies more than 20 % below the homogenised bar that has the same DC resistance.

---

## A2. Is the suspicion correct, wrong, or incomplete?

Short answer: correct in substance, incomplete in six specific ways (A2.8).

**A2.1. The effective-medium result is right when the lattice pitch is much smaller than δ_eff.**

*Derivation.* Average Ohm's law over a cell: ⟨J_z⟩ = σ_eff·E_z. Ampère's law for the averaged field with μ = μ₀: ∇×H = ⟨J⟩. Faraday's law is unchanged. Together these are the equations of a homogeneous conductor of conductivity σ_eff, so everything known for solid bars applies with σ → σ_eff:

- thin bar (thickness ≪ δ_eff): R′ = 1/(σ_eff·A), proportional to 1/σ_eff;
- thick bar: R′ = κ/(σ_eff·δ_eff·P), proportional to 1/sqrt(σ_eff).

At a fixed shape and frequency R′ falls monotonically as σ rises. I checked this numerically for the 10 × 100 mm bar over σ = 1e5 to 1.2e8 S/m at both frequencies (16 points each, no exception; `a2_sigma_sweep_tubes.py`, section 1). So a lattice in a given envelope is always worse than the solid of the same metal: by a factor between sqrt(σ/σ_eff) (thick) and σ/σ_eff (thin).

*What σ_eff can be.* With ρ̄ = 0.3:

| Assumption | σ_eff/σ_Al | Tortuosity τ in the prompt's notation | R′/R′_solid Al (thick) | R′/R′_solid Cu (thick) |
|---|---|---|---|---|
| All metal runs along the bar (upper bound for any structure) | 0.300 | 1 | 1.83 | 2.30 |
| Isotropic structure, Hashin–Shtrikman upper bound 2ρ̄/(3 − ρ̄) | 0.222 | 1.35 | 2.12 | 2.67 |
| Low-density strut lattice or open foam, ρ̄/3 (Lemlich 1978) | 0.100 | 3 | 3.16 | 3.98 |

(`a1_analytic_numbers.py`, section 4.) The Hashin–Shtrikman bound is from Hashin and Shtrikman (1962), who state that it also holds for electrical conductivity. A real printed lattice has a further penalty that I have not included: printed aluminium alloys conduct worse than the 3.77e7 S/m assumed here. A secondary source gives about 30 % IACS for AlSi10Mg, roughly half the assumed value (UNSURE; I did not find a primary figure).

*Numerical check of the homogenisation.* A bundle of 240 × 24 square aluminium strands of side 0.228 mm on a 0.417 mm pitch (fill 0.3), all connected in parallel, every strand resolved, gives R′ = 409.4 µΩ/m at 10 kHz. The homogenised bar with σ_eff = 0.3 σ_Al gives 414.5 µΩ/m. The difference is 1.2 % (`a2_strand_bundle_scan.py`). This bundle is the most favourable geometry Claim A could ask for: all metal is axial and the strands are perfectly insulated from each other.

- Confidence: high.
- Falsifier: the same comparison in an independent finite-element code differing by more than 5 % at pitch/δ_eff < 0.3.

**A2.2. Where homogenisation breaks down.**

(a) *Pitch comparable to δ_eff.* For axial square strands, pitch/δ_eff equals t/δ exactly (because t = pitch·sqrt(ρ̄) and δ_eff = δ/sqrt(ρ̄)). So the homogenised model starts to fail at the same point where the claim's own premise t_w < δ starts to fail. The explicit bundle then has lower R′ than the homogenised bar (`a2_strand_bundle_scan.py`, fill 0.3):

| Frequency | t/δ_Al = pitch/δ_eff | R′_explicit/R′_homogenised |
|---|---|---|
| 10 kHz | 0.28 | 0.99 |
| 10 kHz | 0.42 | 0.97 |
| 10 kHz | 0.56 | 0.95 |
| 10 kHz | 0.84 | 0.90 |
| 100 kHz | 0.88 | 0.88 |
| 10 kHz | 1.11 | 0.85 |
| 100 kHz | 1.32 | 0.79 |
| 10 kHz | 1.67 | 0.74 |
| 100 kHz | 2.11 | 0.68 |
| 10 kHz | 3.34 | 0.67 |
| 100 kHz | 3.52 | 0.66 |
| 100 kHz | 5.28 | 0.66 |

The practical reading: as struts are made thinner relative to δ, the lattice converges to the homogenised value, which is the worst case. Thin struts do not suppress the bar-scale skin effect; they make the effective-medium description of it exact. With coarse struts the "lattice" is a few thick bars with gaps, and it is still worse than the solid (A2.3).

(b) *Few cells across the bar.* With fewer than about five cells across the thickness there is no scale separation.

(c) *Terminations and bends.* Where current is injected the field is three-dimensional over a length of the order of the bar width, and transverse struts do carry current. Not computed.

(d) *Defects.* Broken or necked struts and poor node fusion lower σ_eff locally. Not computed.

- Confidence: medium-high for (a), computed for square axial strands only; low for (b) to (d), which are qualitative.
- Falsifier for (a): a finite-element strand bundle with t/δ < 0.3 whose R′ lies more than 5 % below the homogenised bar.

**A2.3. No lattice regime beats a solid copper bar of the same envelope at equal I_rms. None beats solid aluminium either.**
Evidence: 26 explicit bundles (fill 0.3, 0.6, 0.85; pitch 0.417 to 5 mm; 10 kHz and, for fill 0.3, 100 kHz; `a2_strand_bundle_scan.py`). The lowest ratio found is R′/R′_solid Al = 1.02 and R′/R′_solid Cu = 1.29, at fill 0.85 with strands 4.6 mm thick, which is nearly a solid bar. At fill 0.3 the range is 1.2 to 1.8 times solid aluminium and 1.5 to 2.3 times solid copper. In the regime the claim describes (t_w < δ_Al, fill 0.3) the ratio to solid copper is 2.29 at 10 kHz and 2.03 at 100 kHz.

The reason is general. Removing metal from inside the envelope lowers R′ only when the metal removed lies deeper than about 1.6 δ from the surface, and then by at most a few per cent (A2.5). A lattice removes metal from the skin, where the current flows.

- Confidence: high for structures uniform along the bar and connected in parallel, at these two frequencies. Medium for general 3-D lattices, which I did not simulate; their transverse metal lowers σ_eff further.
- Falsifier: any node-connected aluminium lattice in the 10 × 100 mm envelope, computed with the tools in A4 or measured, with R′ below 178 µΩ/m at 10 kHz or below 565 µΩ/m at 100 kHz.

**A2.4. Current sharing needs transposition. The same bundle with equal strand currents has 4.5 times less resistance.**
I solved the 0.228 mm strand bundle a second time with every strand forced to carry the same net current, which is what insulation plus transposition achieves on average (`a2_transposed_bundle.py`):

| Fill 0.3 Al, strands 0.228 mm, same cross-section | 10 kHz | 100 kHz |
|---|---|---|
| Strands in parallel, not transposed (the lattice case) | 409 µΩ/m | 1143 µΩ/m |
| Equal strand currents (ideal transposition) | 91.4 µΩ/m | 382 µΩ/m (under-resolved, see below) |
| Solid copper, same envelope | 178 µΩ/m | 565 µΩ/m |
| DC resistance of the bundle | 88.4 µΩ/m | 88.4 µΩ/m |

At 10 kHz the identical piece of aluminium is 2.3 times worse than solid copper when connected like a lattice and 1.95 times better when transposed. Insulation alone does not do this: the non-transposed bundle in the first row already has perfect insulation between strands.

At 100 kHz the 2 × 2 sub-cells capture only about 75 % of the strand-level loss, so the true value is higher than 382, probably between 380 and 480 µΩ/m. With 0.274 mm strands and 3 × 3 sub-cells the result is 586 µΩ/m, which is no better than solid copper. This shows a second point the claim misses: even with transposition, "strand thinner than δ" is not the right criterion in a thick bundle. The strand-level loss ratio is ρ̄²·T²·d²/(48 δ⁴) for round strands (my derivation, 1-D field in a bundle of thickness T), so the strand must satisfy roughly d < 7 δ²/(ρ̄·T), which is 0.16 mm here at 100 kHz, not d < δ = 0.26 mm.

- Confidence: high at 10 kHz; medium at 100 kHz (resolution).
- Falsifier: the FEMM setup in A4 with each strand in its own series circuit giving R′ at 10 kHz outside 85 to 100 µΩ/m.

**A2.5. Shape alone can gain only a little. A bound for any non-transposed structure.**
The suspicion says that any advantage comes from macro-shape. That is true for parallel-connected conductors, and the advantage is bounded.

*Bound (my derivation).* In the thin-skin limit, any set K of parallel-connected conductors of one material satisfies

R′ ≥ R_s/(2π·c(K)), with R_s = 1/(σδ) and c(K) the logarithmic capacity of the cross-section.

Sketch of proof. In this limit the vector potential is the same constant on all conductors, so outside them it is −(μ₀I/2π)·g, where g is the Green's function of the exterior with pole at infinity: g = 0 on the conductors and g = ln|z| − ln c + o(1) far away. The surface current density is (I/2π)|∇g|, so R′ = R_s·∮|∇g|² dl/(2π)². The function u = ln|∇g| + g is subharmonic in the exterior, including the point at infinity, where it equals −ln c. A subharmonic function is at most its boundary average weighted by harmonic measure, and the harmonic measure seen from infinity is |∇g| dl/2π. On the boundary g = 0, so −ln c ≤ ∫ ln|∇g| dω. Jensen's inequality then gives 1/c ≤ ∫|∇g| dω = ∮|∇g|² dl/2π. Equality holds only for a circle.

Capacity does not increase when metal is removed, so for anything inside the envelope c(K) ≤ c(envelope). For the 10 × 100 mm rectangle c = 29.76 mm, so 2πc = 187.0 mm. The solid bar has R′ = R_s·κ/P with P/κ = 140.9 mm (`a2_hf_limit_bem.py`; the capacity computation reproduces the exact values for a thin strip, w/4, and for a square, 0.59017 × side). Therefore:

- No parallel-connected structure of the same metal inside the envelope can have less than 0.753 of the solid bar's thin-skin resistance.
- No aluminium structure inside the envelope can have less than 0.947 of the solid copper bar's.
- The bound cannot be attained inside a rectangle.

*What is actually achieved.* Hollowing the bar to a wall of 1.57 δ lowers R′ by 6.3 % in the 2-D solution at 10 kHz (210.4 against 224.7 µΩ/m; 1-D theory says 8.3 %; `a2_sigma_sweep_tubes.py`, section 2). That 8 % dip occurs at finite δ and is outside the assumptions of the bound, so the two statements together are: a few per cent from wall thickness, and at most 25 % from any reshaping within the envelope.

- Confidence: medium. The proof is mine and has not been checked by anyone; I did not search for it in the literature.
- Falsifier: a z-invariant, parallel-connected cross-section inside the envelope, with all features much larger than δ, whose computed R′ is below 0.753 of the solid bar's; or an error found in the proof.

**A2.6. The alternatives a designer would use, same 10 × 100 mm envelope unless stated.**

| Option | 10 kHz R′ (µΩ/m) | 100 kHz R′ (µΩ/m) | Mass (kg/m) | Script |
|---|---|---|---|---|
| Solid Cu | 178.4 | 564.7 | 8.96 | `a3_busbar_rac.py` |
| Cu tube, wall 1.40 mm | 174.1 | 564.6 | 2.69 | `a3_busbar_rac.py` |
| Solid Al | 224.7 | 709.4 | 2.70 | `a3_busbar_rac.py` |
| Al tube, wall 1.40 mm (same mass as the lattice) | 212.1 | 709.4 | 0.81 | `a3_busbar_rac.py` |
| Al lattice ρ̄ = 0.3, σ_eff = 0.3 σ_Al (best case) | 414.5 | 1294 (homogenised), 1143 (explicit strands) | 0.81 | `a3_busbar_rac.py`, `a2_strand_bundle_scan.py` |
| Al strips in parallel, 10 × 0.9 mm or 20 × 0.45 mm, insulated, not interleaved | 231 / 235 | 720 / 720 | 2.43 | `a2_laminations.py` |
| Al tube 126 × 10 mm (26 % wider), wall 1.6 δ_Al | 175.3 | 549.6 | 0.94 / 0.30 | `a2_sigma_sweep_tubes.py` |
| Ideal Al Litz, fill 0.3 (strand 0.2 mm at 10 kHz, 0.071 mm at 100 kHz) | 90 | 107 | 0.81 | `a1_analytic_numbers.py` |
| Interleaved go/return Al foils, 20 + 20 foils of 0.25 mm (stack 13.9 mm for both polarities) | 53.3 per polarity | 54.0 per polarity | 1.35 per polarity | `a2_laminations.py` |

Reading the table:

- *Hollow tube.* At equal mass the aluminium tube has half the resistance of the lattice. It is 19 % (10 kHz) to 26 % (100 kHz) worse than solid copper at 9 % of the mass. The copper tube shows that 70 % of the copper in the solid bar does nothing at 10 kHz. At 100 kHz a copper wall of 1.6 δ = 0.33 mm would be enough, about 7 % of the solid bar's copper (stated from the 1-D optimum, not computed in 2-D for copper).
- *Laminated strips without interleaving* behave like the solid bar. Subdividing without transposition does nothing, as A2.4 says.
- *More perimeter.* A 26 % wider aluminium tube matches solid copper. This follows from R′ ∝ 1/(sqrt(σ)·P): the penalty for aluminium is sqrt(σ_Cu/σ_Al) = 1.257 instead of 1.58 at DC.
- *Litz and interleaving* are discussed in A2.7.

- Confidence: high for the tubes, strips and solid bars (2-D field solutions, mesh-converged); medium for the interleaved stack (2-D, ideal); medium-low for the Litz row (closed form, ideal).
- Falsifier: FEMM or equivalent returning values more than 3 % away for the first seven rows.

**A2.7. Two mechanisms that are not macro-shape and do beat solid copper.**

*Transposed insulated strands (Litz).* With ideal transposition R′ ≈ R_dc/ρ̄ × (1 + ρ̄²T²d²/(48 δ⁴)). For aluminium at fill 0.3 in this envelope: 89.9 µΩ/m at 10 kHz with 0.2 mm strands, and 106.9 µΩ/m at 100 kHz with 0.071 mm strands (about 76 000 strands). That is 2.0 and 5.3 times below solid copper (`a1_analytic_numbers.py`, section 6). The 10 kHz value is supported by the field solution in A2.4 (91.4 µΩ/m for 0.228 mm square strands). Aluminium Litz and aluminium windings as a copper substitute at high frequency are established practice (Sullivan 2008). Practical caveats that I have not quantified: achievable fill, lay length, bundle-level construction for tens of thousands of strands, and terminating aluminium Litz.

*Interleaved go and return foils (laminated busbar).* When go and return foils alternate, each foil sees only the field of its neighbours, the 1-D formula of A1.1 applies, and foils thinner than δ carry nearly uniform current. Forty aluminium foils of 0.25 mm give 53 to 54 µΩ/m per polarity at both frequencies, against 231 and 739 µΩ/m per conductor for a pair of solid 10 × 100 mm copper bars 2 mm apart (`a2_laminations.py`, `a3_go_return_sensitivity.py`). This is the one situation in which Claim A's formula, and its conclusion that thin aluminium beats thick copper, are correct. It requires the return conductor to be interleaved. It is a different topology from a single bar and has nothing to do with a lattice.

- Confidence: medium (ideal models; magnitudes are large enough that the ranking is not in doubt).
- Falsifier: measurement or 3-D computation showing an interleaved aluminium foil bus or an aluminium Litz conductor of these dimensions with higher R′ than the solid copper bar at 10 kHz.

**A2.8. Where the suspicion is right, and where it is incomplete or imprecise.**

Right:

- A homogenisable lattice behaves as a conductor of conductivity σ_eff ≈ ρ̄σ/τ (A2.1).
- Eddy currents inside struts are suppressed and the bar-scale skin effect remains, with δ_eff (A1.4, A2.1).
- In the thick limit R′ ∝ 1/sqrt(σ_eff), worse than solid aluminium and solid copper of the same envelope (A2.3).
- Without transposition parallel struts do not share current evenly (A2.4).

Incomplete or imprecise:

1. *The scaling.* 1/sqrt(σ_eff) holds only when the bar is thicker than about 3 δ_eff. Otherwise the penalty is larger, up to 1/σ_eff. Also 1/(σ δ P) underestimates a flat bar by the edge factor κ ≈ 1.53. κ is the same for every homogeneous conductor of this shape, so it cancels in ratios but not in absolute values.
2. *Homogenisation is slightly pessimistic near its limit.* At t/δ ≈ 0.9 the explicit bundle is 10 to 12 % below the homogenised value (A2.2). The conclusion does not change.
3. *"Any advantage comes from macro-shape" misses two mechanisms.* Transposition and go/return interleaving are connection topology, not shape, and both let aluminium beat a solid copper bar by factors of 2 to 5 (A2.7). The suspicion mentions Litz only as the thing the lattice lacks.
4. *The macro-shape advantage is bounded and small inside a fixed envelope.* About 6 % from hollowing, at most 25 % from any reshaping (A2.5). The real lever for aluminium against copper is not a gain; it is that the penalty is only 1.26 and can be bought back with 26 % more perimeter.
5. *"Worse than solid" is true per envelope, not per kilogram.* R′ × mass at 10 kHz is 1599 (solid Cu), 607 (solid Al), 336 (lattice, best case) and 172 (Al tube) µΩ·kg/m². The lattice beats both solid bars on this measure. It is dominated by the tube, not by the solid bar. If the framework's Σ_init term rewards low mass, this distinction matters.
6. *Both the claim and the suspicion ignore the return conductor.* A return bar 2 mm away raises every R′ by about 30 % and leaves all ratios unchanged within 3 % (A3.5).

---

## A3. Worked comparison: 10 mm × 100 mm envelope, 10 kHz and 100 kHz, I_rms = 1 kA

### A3.1 Formulas

- Skin depth: δ = sqrt(1/(π f μ₀ σ)).
- DC: R′_dc = 1/(σ A).
- Thick-bar estimate without edge crowding: R′_0 = 1/(σ δ P).
- Thick bar with edge crowding: R′ = κ·R′_0. For this 10:1 rectangle κ = 1.561 in the limit δ → 0 and 1.525 at the skin depths of this problem (A3.4).
- Lattice: the same formulas with σ → σ_eff = ρ̄σ_Al/τ. I give three values of τ (A2.1) and treat τ = 1 as the headline because it is the most favourable to Claim A.
- Equal-mass tube: metal area ρ̄·A = 300 mm² in the same outer envelope. Wall w from W·T − (W − 2w)(T − 2w) = ρ̄·W·T, so w = [(W + T) − sqrt((W + T)² − 4ρ̄WT)]/4 = (110 − 104.403)/4 = 1.399 mm.
- Tube, 1-D estimate: R′ ≈ κ·F(w/δ)/(σ·w·P_mid), with F from A1.1.
- Entropy generation rate per metre: Σ̇ = R′·I_rms²/T₀.

Skin depths in mm (`a1_analytic_numbers.py`, section 1):

| | Cu | Al | Lattice 0.300 σ_Al | Lattice 0.222 σ_Al | Lattice 0.100 σ_Al |
|---|---|---|---|---|---|
| 10 kHz | 0.652 | 0.820 | 1.497 | 1.739 | 2.592 |
| 100 kHz | 0.206 | 0.259 | 0.473 | 0.550 | 0.820 |

Hand check for solid copper at 10 kHz: R′_0 = 1/(5.96e7 × 6.519e-4 × 0.22) = 117.0 µΩ/m; × 1.525 = 178.4 µΩ/m.

### A3.2 Method for the numbers

A closed form is not adequate for a finite rectangular bar, because the current crowds towards the narrow edges. I therefore solved the 2-D eddy-current problem numerically with a volume integral equation (filament method, as in Silvester 1967 and Weeks et al. 1979): the cross-section is divided into rectangular cells with constant current density, the logarithmic kernel is integrated exactly over each cell, and the open boundary is exact because the kernel is the free-space one. The solver is `eddy2d.py`. Meshes are graded towards the surface with the first cell at δ/3, δ/6 and δ/10.

### A3.3 Results

From `local_docs/fable_runs/prompt_1a_code/a3_busbar_rac.py` (finest mesh) unless another script is named.

**10 kHz**

| Conductor | σ (S/m) | R′_dc (µΩ/m) | R′_0 = 1/(σδP) (µΩ/m) | R′ 2-D (µΩ/m) | R′/R′_solid Cu | P′ at 1 kA (W/m) | Σ̇ (W/(K·m)) | Mass (kg/m) |
|---|---|---|---|---|---|---|---|---|
| Solid Cu | 5.96e7 | 16.78 | 117.0 | 178.4 | 1.000 | 178.4 | 0.598 | 8.96 |
| Solid Al | 3.77e7 | 26.53 | 147.1 | 224.7 | 1.259 | 224.7 | 0.753 | 2.70 |
| Al lattice, σ_eff = 0.300 σ_Al (τ = 1) | 1.131e7 | 88.42 | 268.6 | 414.5 | 2.323 | 414.5 | 1.390 | 0.81 |
| Same, explicit 0.228 mm strands (`a2_strand_bundle_scan.py`) | — | 88.42 | — | 409.4 | 2.294 | 409.4 | 1.373 | 0.81 |
| Al lattice, σ_eff = 0.222 σ_Al (τ = 1.35) | 8.378e6 | 119.4 | 312.0 | 483.0 | 2.707 | 483.0 | 1.620 | 0.81 |
| Al lattice, σ_eff = 0.100 σ_Al (τ = 3) | 3.770e6 | 265.3 | 465.1 | 712.5 | 3.993 | 712.5 | 2.390 | 0.81 |
| Al tube, wall 1.399 mm (equal mass) | 3.77e7 | 88.42 | — | 212.1 | 1.189 | 212.1 | 0.711 | 0.81 |
| For reference: lattice according to Claim A (`a1_analytic_numbers.py`) | — | 88.42 | — | 88.5 | 0.34 to 0.69 (by the claim's own Cu value) | — | — | 0.81 |

**100 kHz**

| Conductor | σ (S/m) | R′_dc (µΩ/m) | R′_0 = 1/(σδP) (µΩ/m) | R′ 2-D (µΩ/m) | R′/R′_solid Cu | P′ at 1 kA (W/m) | Σ̇ (W/(K·m)) | Mass (kg/m) |
|---|---|---|---|---|---|---|---|---|
| Solid Cu | 5.96e7 | 16.78 | 369.9 | 564.7 | 1.000 | 564.7 | 1.894 | 8.96 |
| Solid Al | 3.77e7 | 26.53 | 465.1 | 709.4 | 1.256 | 709.4 | 2.379 | 2.70 |
| Al lattice, σ_eff = 0.300 σ_Al (τ = 1) | 1.131e7 | 88.42 | 849.2 | 1294.3 | 2.292 | 1294.3 | 4.341 | 0.81 |
| Same, explicit 0.228 mm strands (`a2_strand_bundle_scan.py`) | — | 88.42 | — | 1143.3 | 2.025 | 1143.3 | 3.835 | 0.81 |
| Al lattice, σ_eff = 0.222 σ_Al (τ = 1.35) | 8.378e6 | 119.4 | 986.7 | 1504.2 | 2.664 | 1504.2 | 5.045 | 0.81 |
| Al lattice, σ_eff = 0.100 σ_Al (τ = 3) | 3.770e6 | 265.3 | 1470.9 | 2246.5 | 3.978 | 2246.5 | 7.535 | 0.81 |
| Al tube, wall 1.399 mm (equal mass) | 3.77e7 | 88.42 | — | 709.4 | 1.256 | 709.4 | 2.379 | 0.81 |
| For reference: lattice according to Claim A (`a1_analytic_numbers.py`) | — | 88.42 | — | 93.0 | 0.11 to 0.23 (by the claim's own Cu value) | — | — | 0.81 |

**A3.3a.** At equal envelope and equal current the aluminium lattice generates 2.0 to 4.0 times the entropy of solid copper and 1.6 to 3.2 times that of solid aluminium, depending on σ_eff and frequency.
- Confidence: high for the homogenised rows given σ_eff; the choice of σ_eff is the dominant uncertainty.
- Falsifier: as A2.3.

**A3.3b.** The equal-mass aluminium tube has 51 % (10 kHz) and 55 to 62 % (100 kHz) of the best-case lattice's resistance, and is 19 % and 26 % above solid copper.
- Confidence: high.
- Falsifier: FEMM tube model (A4) outside 212.1 ± 3 % at 10 kHz or 709.4 ± 3 % at 100 kHz.

### A3.4 Numerical accuracy

- *Kernel and formulation.* The closed-form cell integral matches brute-force quadrature to 8 digits. The DC limit is reproduced. For a round copper wire of radius 2 mm (staircase mesh) R_ac/R_dc is 1.8032 to 1.8084 against the exact Bessel value 1.8036 at 10 kHz, and 3.6923 to 3.6991 against 3.6934 at 50 kHz, an error of at most 0.3 % (`eddy2d.py`).
- *Mesh.* Medium to fine mesh changes R′ by at most 0.25 % in every case of the table (`a3_busbar_rac.py`).
- *Independent method.* A boundary-element solution of the thin-skin limit gives κ = 1.561 (`a2_hf_limit_bem.py`). The volume solver gives 1.525 at b/δ = 7.7 and 24, 1.533 at 77 and 1.540 at 243. The deficit shrinks slowly as the skin gets thinner (0.036, 0.028 and 0.021 at b/δ = 24, 77 and 243), which is the sign and roughly the rate expected from the rounding of the corner singularity over a distance δ. The two methods therefore agree within 2.4 %, with the difference in the expected direction.
- *Strand bundles.* Halving or coarsening the sub-cell size changes R′ by at most 1.2 % (`a2_strand_bundle_scan.py`, resolution block).
- My estimate of the numerical error: ±1 % for homogeneous conductors and tubes, ±2 % for explicit strand bundles with strands in parallel. The transposed-bundle value at 100 kHz is not converged (A2.4).
- For comparison, the estimate without edge crowding, 1/(σ δ P), is 34 % low.

### A3.5 Model assumptions and their effect

- *Isolated bar.* With an identical return bar broadside at a 2 mm gap, R′ per conductor rises to 231.5 (Cu), 290.0 (Al), 522.6 (lattice 0.3) and 270.9 (Al tube) µΩ/m at 10 kHz, and 739.5, 928.6, 1686.6 and 928.7 µΩ/m at 100 kHz: about 30 % higher, because the current moves to the facing surfaces. At a 20 mm gap the rise is about 5 %. The ratios to copper change by less than 3 % (`a3_go_return_sensitivity.py`).
- *Temperature.* All values use 20 °C conductivities. In the thick limit R′ ∝ sqrt(resistivity), so a 50 K rise adds about 10 % to every row and does not change the ranking. The operating point itself is thermally severe: 0.56 to 1.3 kW per metre at 100 kHz from a surface of 0.22 m² per metre. I did not compute temperatures.
- *Lattice material.* Printed aluminium alloys conduct less than 3.77e7 S/m (A2.1, UNSURE on the value). That would raise the lattice rows by a further factor of up to about 1.4.
- *Surface roughness* of printed parts is 10 to 20 µm against δ of 200 to 800 µm here, so I neglect it. Grooves parallel to the current raise the loss less than transverse ones but still raise it (Morgan 1949, from the abstract; I did not read the full paper).
- *Infinitely long, straight.* Terminations and bends are not modelled.

---

## A4. Independent tool and setup that would test A2 and A3

**A4.1. 2-D test with FEMM** (Finite Element Method Magnetics, D. C. Meeker, femm.info; source is available; I am UNSURE whether its licence counts as open source in the strict sense, so Elmer FEM or GetDP with Gmsh are the fallback, both GPL-family).

Setup:

- Problem type: planar, harmonic, frequency 10 kHz and 100 kHz, length unit mm, depth 1000 mm.
- Geometry: rectangle 100 × 10 mm centred in a circular air region of radius 300 mm, closed with FEMM's open-boundary shells (improvised asymptotic boundary condition, Meeker 2013).
- Materials: μ_r = 1; σ = 59.6 MS/m (copper), 37.7 MS/m (aluminium), 11.31 MS/m (homogenised lattice, 0.3 σ_Al).
- Excitation: one circuit property, parallel connection, total current corresponding to 1 kA rms. I am UNSURE whether FEMM takes peak or rms amplitude; computing R′ = Re(V/I) or loss/|I|² avoids the question.
- Mesh: element size at most δ/3 within 3 δ of every conductor surface (0.07 mm for copper at 100 kHz).
- Output: R′ from the real part of voltage drop over current in the circuit result, cross-checked against the integrated resistive loss.

Cases:

1. Solid Cu, solid Al, homogenised block.
2. Al tube 100 × 10 mm, wall 1.399 mm.
3. Explicit bundle: 240 × 24 square aluminium strands of side 0.228 mm on a 0.4167 mm pitch (scripted in Lua or Python), all assigned to the same parallel circuit.
4. The same bundle with every strand in its own circuit, all circuits carrying the same current (ideal transposition).

Results that would falsify my conclusions:

| Test | My value | Falsified if |
|---|---|---|
| Solver check: solid Cu | 178.4 (10 kHz), 564.7 (100 kHz) µΩ/m | outside ±2 % |
| Homogenisation: case 3 against homogenised block, 10 kHz | 409.4 against 414.5 µΩ/m | differ by more than 5 % |
| Main conclusion: case 3 against solid Cu | 2.29 (10 kHz), 2.03 (100 kHz) times higher | bundle R′ at or below solid Cu at either frequency |
| Transposition: case 4, 10 kHz | 91.4 µΩ/m | outside 85 to 100 µΩ/m |
| Tube | 212.1 (10 kHz), 709.4 (100 kHz) µΩ/m | outside ±3 % |

**A4.2. 3-D test of a real node-connected lattice with FastHenry** (Kamon, Tsuk and White 1994; a 3-D filament solver that returns R(f) and L(f) for networks of straight segments, which is exactly what a strut lattice is).

Setup: a simple-cubic aluminium lattice, strut 0.25 mm square, pitch 0.5 mm, envelope 4 × 16 cells (2 × 8 mm) and at least 16 cells long, every strut one segment subdivided into 2 × 2 filaments, the two end faces each tied to one node, frequency sweep 1 kHz to 3 MHz. Compare with a solid bar of the same envelope and length in the same tool, with conductivity chosen to give the same DC resistance, and with solid aluminium and solid copper bars. The reduced size keeps the segment count near 3000; the frequency is scaled up so that thickness/δ_eff covers the range 0.5 to 10.

Falsified if: the lattice's R_ac/R_dc lies more than 20 % below that of the equal-DC-resistance solid bar at thickness ≥ 6 δ_eff with struts thinner than δ; or the lattice's R_ac falls below the solid copper bar's at any frequency.

**A4.3. Experiment.** Print the lattice bar and a solid bar of the same alloy and envelope, measure R(f) with an impedance analyser in a four-terminal coaxial return fixture, or calorimetrically at fixed current. Falsified if the lattice's R_ac at thickness ≥ 6 δ_eff is below the solid bar's.

- Confidence that these tests would confirm rather than falsify: high for A4.1, medium-high for A4.2 and A4.3.

---

## A5. Verdict claims

**A5.1.** "A lattice with struts thinner than δ suppresses the skin effect, so aluminium beats copper" is invalid as a substitution mechanism. The lattice suppresses only the eddy currents inside individual struts, which carry under 5 % of the loss. The skin effect of the bar remains, with a larger skin depth and a higher resistance, R′ ∝ 1/sqrt(σ_eff).
- Confidence: high.
- Falsifier: A4.1 case 3 or A4.2.

**A5.2.** A valid mechanism exists at the macro-shape level. In the skin-limited regime R′ of a fixed shape scales as 1/sqrt(σ), so aluminium costs a factor 1.26 against copper instead of 1.58 at DC; only a skin of about 1.6 δ carries current; and R′ is inversely proportional to the effective perimeter. An aluminium tube 26 % wider than the copper bar, with a wall of 1.6 δ, matches the solid copper bar at 10 % (10 kHz) or 3 % (100 kHz) of its mass. Within a fixed envelope, reshaping cannot gain more than 25 % and aluminium cannot beat solid copper by more than 5 % (thin-skin bound, A2.5).
- Confidence: high for the tube numbers, medium for the bound.
- Falsifier: A4.1 tube case; a counter-example to the bound.

**A5.3.** A second valid mechanism exists at the level of connection topology: mutually insulated strands that are transposed, or go and return foils that are interleaved. Both let aluminium beat a solid copper bar of the same envelope by factors of 2 to 5. A node-connected lattice is the opposite of both.
- Confidence: medium-high.
- Falsifier: A4.1 case 4; a measured aluminium Litz or laminated bus worse than the solid copper bar.

**A5.4.** The statement "at f > 5 kHz thick solid copper bars suffer current constriction" is correct: δ_Cu = 0.92 mm at 5 kHz, so any bar thicker than about 2 mm is affected.
- Confidence: high.

**A5.5.** For the framework: with Σ̇ = I²R′/T₀ the lattice row is 2.0 to 4.0 times the copper row, so the operational term goes the wrong way. A lattice may still be chosen for stiffness per mass or for cooling surface. Those are different functions and need their own accounting; they do not make the conduction claim true. A lattice core inside a solid skin of about 1.6 δ is electrically a tube, and it is the skin that does the conducting.
- Confidence: high for the first sentence; the rest is scope, not a computed result.

---

## Citations

Existence of each reference (authors, title, journal, volume, pages) was checked by web search of bibliographic records on 2026-11-12, except where marked. I did not open the full texts, so no equation number is given; where the prompt's format asks for an equation or page, I give the page range.

1. P. L. Dowell (1966), "Effects of eddy currents in transformer windings", Proc. IEE 113(8), pp. 1387–1394. Used for: origin of the quoted formula (single-layer case of the layer model).
2. J. A. Ferreira (1994), "Improved analytical modeling of conductive losses in magnetic components", IEEE Trans. Power Electronics 9(1), pp. 127–131. Used for: skin and proximity losses are orthogonal and can be added.
3. C. R. Sullivan (1999), "Optimal choice for number of strands in a litz-wire transformer winding", IEEE Trans. Power Electronics 14(2), pp. 283–291. Used for: low-frequency strand proximity loss.
4. C. R. Sullivan (2008), "Aluminum windings and other strategies for high-frequency magnetics design in an era of high copper and energy costs", IEEE Trans. Power Electronics 23(4), pp. 2044–2051. Used for: aluminium's resistivity penalty matters less at high frequency; aluminium conductors as established practice.
5. P. Silvester (1967), "AC resistance and reactance of isolated rectangular conductors", IEEE Trans. Power Apparatus and Systems PAS-86(6), pp. 770–774. Used for: the problem class and a published reference solution for rectangular bars. I did not compare my numbers with its curves.
6. W. T. Weeks, L. L. Wu, M. F. McAllister, A. Singh (1979), "Resistive and inductive skin effect in rectangular conductors", IBM J. Research and Development 23(6), pp. 652–660. Used for: the filament method.
7. J. Gyselinck, P. Dular (2005), "Frequency-domain homogenization of bundles of wires in 2-D magnetodynamic FE calculations", IEEE Trans. Magnetics 41(5), pp. 1416–1419. Used for: complex-permeability homogenisation of strand bundles.
8. D. C. Meeker (2012), "An improved continuum skin and proximity effect model for hexagonally packed wires", J. Computational and Applied Mathematics. Existence and year verified; volume and pages UNSURE (I recall 236(18), pp. 4635–4644). Used for: same as 7.
9. Z. Hashin, S. Shtrikman (1962), "A variational approach to the theory of the effective magnetic permeability of multiphase materials", J. Applied Physics 33(10), pp. 3125–3131. Used for: upper bound on isotropic effective conductivity.
10. R. Lemlich (1978), "A theory for the limiting conductivity of polyhedral foam at low density", J. Colloid and Interface Science 64(1), pp. 107–110. Existence verified through citing papers; one source gives the year as 1977. Used for: σ_eff = ρ̄σ/3 for a low-density strut network.
11. S. P. Morgan (1949), "Effect of surface roughness on eddy current losses at microwave frequencies", J. Applied Physics 20, p. 352. Used for: grooves parallel to the current increase loss, less than transverse grooves (abstract only).
12. M. Kamon, M. J. Tsuk, J. K. White (1994), "FASTHENRY: a multipole-accelerated 3-D inductance extraction program", IEEE Trans. Microwave Theory and Techniques 42(9), pp. 1750–1758. Used for: the 3-D tool in A4.2.
13. D. C. Meeker (2013), "Improvised open boundary conditions for magnetic finite elements", IEEE Trans. Magnetics. Existence verified; volume and pages UNSURE (I recall 49(10), pp. 5243–5247). Used for: open boundary in A4.1.
14. H. B. Dwight (1918), "Skin effect in tubular and flat conductors", AIEE. Existence verified; records disagree on Transactions pp. 1379–1403 or Proceedings 37(8), pp. 977–998, so pages UNSURE. Mentioned only as the classical source for tubular conductors; my tube numbers are my own computation and I have not checked them against it.
15. Conductivity of printed AlSi10Mg of about 30 % IACS: from a search-result snippet of a secondary source. UNSURE; no primary reference identified.

The logarithmic capacity of a square, Γ(1/4)²/(4π^1.5) = 0.59017 × side, is a classical closed form that I used as a numerical check; I give no citation for it.

---

## What I could not compute or verify

1. No 3-D lattice was simulated. Everything numerical is uniform along the bar. Transverse struts, nodes, terminations, bends and defects are argued, not computed (A1.5, A2.2 b–d).
2. No independent field solver was run. FEMM, Elmer and FastHenry are not installed and I installed nothing. The checks are internal: an exact round-wire solution, mesh refinement, and a second method of my own for the thin-skin limit.
3. The transposed-bundle result at 100 kHz is under-resolved (A2.4). Only its order of magnitude is usable.
4. The Litz numbers are a closed form for ideal transposition in a 1-D field. Real fill, lay, bundle construction and terminations are not included.
5. The capacity lower bound (A2.5), the strut-level loss ratio (A1.4) and the Litz proximity ratio (A2.4, A2.7) are my own derivations. I did not look for them in the literature and nobody has checked them.
6. Monotonic decrease of R′ with σ was shown numerically for this one shape, not proved.
7. Equation numbers in the cited papers were not checked against the full texts. Items marked UNSURE in the citation list are unresolved.
8. Temperature rise, temperature-dependent conductivity and thermal feasibility of 1 kA at 100 kHz were not computed.
9. The conductivity of a printed aluminium lattice was not established; the tables use the prompt's 3.77e7 S/m.
10. I did not compare my solid-bar values with Silvester's (1967) published curves.

---

## Verdict

**Invalid as stated; valid only with a restated scope that removes the lattice.** The quoted formula is the one-dimensional result for a single foil with field on one face, and applying it strut by strut ignores that the struts are in parallel and share one magnetic field. A node-connected lattice behaves as a conductor of effective conductivity σ_eff ≈ ρ̄σ/τ, keeps the full skin effect at the scale of the bar, and has R′ ∝ 1/sqrt(σ_eff): for the 10 mm × 100 mm envelope at 1 kA, an aluminium lattice at ρ̄ = 0.3 dissipates 409 to 713 W/m at 10 kHz and 1143 to 2247 W/m at 100 kHz, against 178 and 565 W/m for solid copper, 225 and 709 W/m for solid aluminium, and 212 and 709 W/m for a hollow aluminium section of the same mass as the lattice. Claim A's own model underestimates the lattice by factors of 4.7 and 13.9. The suspicion in the prompt is correct in substance and incomplete: it omits that the shape advantage inside a fixed envelope is small and bounded, and that two connection-topology mechanisms (transposed insulated strands, interleaved go and return foils) do let aluminium beat a solid copper bar. The restated claim that I would defend is: "In the skin-limited regime the AC resistance of a conductor of fixed shape scales as 1/sqrt(σ) and inversely with its effective perimeter, and only a surface layer of about 1.6 δ carries current. Aluminium can therefore replace copper at a resistance penalty of 1.26 at equal envelope, or at no penalty with about 26 % more perimeter, in a thin-walled section of a small fraction of the mass. Subdividing the cross-section lowers AC resistance only if the strands are mutually insulated and transposed, or if go and return conductors are interleaved. A node-connected lattice does neither and raises the AC resistance."

---

## Appendix: reproducing the numbers

All scripts are in `local_docs/fable_runs/prompt_1a_code/`. Run any of them with `python3 <path>` from any directory (Python 3 with numpy; nothing else). Outputs of the runs that produced the numbers above are saved in `local_docs/fable_runs/prompt_1a_code/outputs/`.

| Script | Run time | Saved output |
|---|---|---|
| `eddy2d.py` | 10 s | `outputs/eddy2d.txt` |
| `a1_analytic_numbers.py` | 5 s | `outputs/a1_analytic_numbers.txt` |
| `a3_busbar_rac.py` | 1 min | `outputs/a3_busbar_rac.txt` |
| `a3_go_return_sensitivity.py` | 20 s | `outputs/a3_go_return_sensitivity.txt` |
| `a2_sigma_sweep_tubes.py` | 1 min | `outputs/a2_sigma_sweep_tubes.txt` |
| `a2_hf_limit_bem.py` | 1 min | `outputs/a2_hf_limit_bem.txt` |
| `a2_laminations.py` | 3 min | `outputs/a2_laminations.txt` |
| `a2_strand_bundle_scan.py` | 6 min | `outputs/a2_strand_bundle_scan.txt` |
| `a2_transposed_bundle.py` | 4 min, about 2 GB memory | `outputs/a2_transposed_bundle.txt` |

The two key scripts are reproduced verbatim below: the solver and the A3 table.

### `local_docs/fable_runs/prompt_1a_code/eddy2d.py`

```python
@@EDDY2D@@
```

### `local_docs/fable_runs/prompt_1a_code/a3_busbar_rac.py`

```python
@@A3@@
```
