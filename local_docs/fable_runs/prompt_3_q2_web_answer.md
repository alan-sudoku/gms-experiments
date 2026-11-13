# Prompt 3, question 2: thermal mismatch (low-budget run)

Context file (`local_docs/`, never cited by the spec). Run 2026-11-13 per `local_docs/orchestration/fable_delegation_plan.md` §5.1, as a Fable agent (`fable`, effort high, no tools) instead of the web chat; input was the §5.1 Q2 block verbatim. The reply below is saved as returned. Every claim is at level `derived`; S1 receives it as input and S5 reviews it.

---

All claims are level `derived` (reasoning only, nothing verified). Notation: ε_m = |α_s − α_2|·ΔT [-]; stresses in Pa; Basquin amplitude σ_a = Δσ/2; ρ̄ = relative density; a = cell size; d = strut diameter; L = bonded width; H_L = lattice height.

1. **Local strut stress is strain-controlled and set by E_s, not E_eff.** The stiffer partner imposes macroscopic strain ε_m on the lattice, and strut strain is of order ε_m.
 - Stretch-dominated (octet), strut along a strained direction: Δσ_strut = E_s·ε_m. This is uniaxial: a slender strut has free lateral surfaces, so no 1/(1−ν).
 - Bending-dominated (strut gyroid, deviatoric loading): Δσ_strut ≈ C_b·E_s·ρ̄^(1/2)·ε_m, with C_b ≈ 0.75–1.5 (UNSURE). Steps: σ̄ = E_s·ρ̄²·ε; F = σ̄·l²; M ≈ F·l/8; σ = 6M/t³; ρ̄ ≈ (t/l)².
 - Sheet TPMS: wall membrane stress up to E_s/(1−ν_s)·ε_m (biaxial in the wall).
 - The original E_s·ρ̄²·ε_m is the macroscopic uniaxial stress. Used as local stress it is low by ρ̄^(−3/2) to ρ̄^(−2), about 4–100.
 - Confidence: high for scaling, medium for constants.
 - Falsifier: beam FE of at least 5×5×5 cells under imposed boundary strain. Peak stress/(E_s·ε_m) should be independent of ρ̄ for octet and ∝ ρ̄^0.5 for strut gyroid.

2. **2a macroscopic: equibiaxial, and the lattice takes almost all the mismatch.** For a lattice layer H_L on a substrate H_2, away from edges:
 - σ̄_L = M_L·ε_m/(1+S), with M_L = E_L/(1−ν_L), M_2 = E_2/(1−ν_2), S = M_L·H_L/(M_2·H_2). Bending is neglected, an O(S) correction.
 - S ≈ (0.01–0.16)·H_L/H_2 even for E_2 ≈ E_s, so "much stiffer" and "comparable" substrates give the same strut strain within about 15 %.
 - Lattice compliance lowers interface traction, substrate stress and debond driving force (all ∝ E_L). It does not lower strut stress: in-plane struts see Δσ = E_s·ε_m/(1+S).
 - Confidence: high.
 - Falsifier: FE with E_2/E_s varied 0.3–3 at H_2 ≥ H_L. Strut stress should change by less than 20 %.

3. **2a peak location and decay.** The peak sits at strut roots and nodes of the first cell row, worst in the free-edge and corner cells.
 - Bonded root on a dissimilar alloy: biaxial constraint over the footprint, Δσ_root ≈ ε_m/[(1−ν_s)/E_s + (1−ν_2)/E_2]. This tends to E_s/(1−ν_s)·ε_m for a rigid substrate. It decays along the strut within about 1·d.
 - The root perimeter is a bimaterial free edge (Bogy-type wedge singularity, exponent UNSURE). A point stress there is not mesh-convergent.
 - Macroscopic decay, thin layer (L ≫ H_L): strain is uniform through H_L, with an edge zone of about 1–2·H_L.
 - Macroscopic decay, tall block (H_L ≳ L): e-fold height ≈ L/4 (Saint-Venant strip; UNSURE for anisotropic lattices, scale by √(E_L/G_L)).
 - Non-affine boundary layer: 1–2 cells. Corner-cell amplification ≈ (H_L/a)^λ, λ ≈ 0.2–0.4 (UNSURE), which can reach about 2.
 - Confidence: medium.
 - Falsifier: solid FE of one strut root (decay over d); lattice FE varying L/H_L and H_L/a.

4. **2b, two alloys across the strut axis (laminate or core–shell).** The stress is self-equilibrated along the whole strut and independent of ρ̄ and lattice topology.
 - σ_A = E_A·ε_AB/(1 + E_A·A_A/(E_B·A_B)), with ε_AB = |α_A − α_B|·ΔT. Uniaxial.
 - Equal E and equal area: E·ε_AB/2, whether bending is restrained by nodes or free. Timoshenko bimetal check: 0.125 + 0.375 = 0.5 at the interface.
 - Thin shell on a core: biaxial, E_shell/(1−ν)·ε_AB.
 - Shear transfer at strut ends and nodes over about 1 strut thickness. The interface free edge is singular.
 - Confidence: high for the formula, medium for the end zone.
 - Falsifier: 3D FE of a single bimetal strut, free and end-clamped.

5. **2b, two alloys along the strut axis (butt joint).**
 - A free strut has no axial stress. The lattice sees α_strut = Σ f_i·α_i.
 - Same α_strut in every strut: no macroscopic stress. Different between struts: Δσ ~ E_s·Δα_strut·ΔT·O(1) for stretch-dominated lattices, reduced by about ρ̄^(1/2) for bending-dominated.
 - At the joint, radial mismatch gives biaxial stress in the interface plane: Δσ ≈ ε_AB/[(1−ν_A)/E_A + (1−ν_B)/E_B]. Zero net force. Decays within about d/2–d each side.
 - Peak at the perimeter: singular, or log/finite if the elastic constants are equal (UNSURE).
 - Confidence: medium.
 - Falsifier: axisymmetric FE of a butt-jointed rod; check the decay length and the interface-plane stress.

6. **2c, lattice in a housing.**
 - Fully enclosed, stiff housing: homogeneous triaxial mismatch, σ̄ = E_L/(1−2ν_L)·ε_m/(1+S_h). Bonded and sliding are identical, since no shear is needed.
 - Every strut strains ε_m, so Δσ_strut = E_s·ε_m. Octet: K = ρ̄·E_s/9. Strut gyroid: planar 120° three-strut nodes carry equal tensions, so hydrostatic loading is stretch-dominated (UNSURE).
 - One face pair gives uniaxial E_L; two pairs give biaxial E_L/(1−ν_L).
 - Spherical-shell estimate: S_h ≈ 3K_L·R·(1−ν_h)/(2·E_h·t_h), which is ≪ 1 unless t_h/R ≲ 0.05.
 - Unbonded contact is unilateral: only the compressive half-cycle loads. A clearance g gives ε_eff = max(0, ε_m − g/L). Example: 5e-4 × 50 mm = 25 µm removes it entirely.
 - Bonded on some faces only: treat as 2a.
 - Peak at contact nodes and cut surface cells (1–2 cells) and at housing corners. With friction μ the interior sticks, slip zone ℓ ≈ σ̄·H/(μ·p), and fretting there is outside Basquin.
 - Confidence: medium.
 - Falsifier: FE with contact, bonded vs frictionless vs gap.

7. **Shear trap: lattice as an interlayer bonded between two dissimilar (or differently heated) stiff parts.**
 - Edge shear strain γ ≈ ε_m·L/(2·H_L), which replaces ε_m in claim 1.
 - Strut stress ~ E_s·γ·O(0.5) for stretch-dominated lattices, concentrated at edge cells.
 - It exceeds claim 1 by more than 2 when L/H_L ≳ 4–8.
 - Confidence: medium.
 - Falsifier: sandwich FE varying L/H_L.

8. **2d verdict.** σ_a = ½·K_f·c·E_s·|α_s − α_2|·ΔT/(1+S).
 - c = 1 for strut lattices. c = 1/(1−ν_s) for bonded roots, core–shell and sheet TPMS.
 - K_f is the node/roughness fatigue notch factor, about 2–3 as-built (UNSURE).
 - Validity: elastic (K_f·c·E_s·ε_m < σ_y); uniform temperature; S ≲ 0.2; ρ̄ ≤ 0.4; bonded or closed contact; a single mismatched interface.
 - Conservative by 1–4 for bending-dominated strut lattices.
 - Non-conservative by more than 2 when:
   - K_f is omitted;
   - there are singular bimaterial edges or corner cells;
   - the lattice is an interlayer with L/H_L ≳ 4–8;
   - thin struts lag or lead a massive partner thermally, which adds E_s·α_s·ΔT_lag even at Δα = 0;
   - cool-down mean stress (ΔT_ref ≫ ΔT) is ignored.
 - Confidence: medium.
 - Falsifier: any FE case within the validity range where the peak exceeds twice the formula.

Open points:
- Constants are unsettled: C_b, K_f, λ and the singularity orders. A point stress at a bimaterial edge is ill-defined, so a critical-distance or fracture measure is needed there.
- Whether a real strut gyroid, with finite node volume and ρ̄ up to 0.4 (not slender), stays stretch-dominated under hydrostatic strain and bending-relieved under deviatoric strain.
- Transient thermal lag and build-residual mean stress are not modelled. Either may dominate the diurnal Δα term.
