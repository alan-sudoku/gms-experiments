# Prompt 3, S1 plan: Q3, Q4, Q5 (lattice fatigue micromechanics)

Context file (`local_docs/`, never cited by the spec). Written 2026-11-14 by the S1 planner per `local_docs/orchestration/fable_delegation_plan.md` §3. Inputs: the Prompt 3 block in `local_docs/fable_questions.md`, the two low-budget answers `prompt_3_q1_web_answer.md` and `prompt_3_q2_web_answer.md`, and §5.1 "Q4's inputs". No code was run and no source was opened. Every statement is a claim at level `derived`. Every number in this file is hand arithmetic for S2 to recompute; none is a result.

Notation. ρ̄ relative density; E_s, σ_y, σ_u solid modulus, yield, ultimate; σ_a macroscopic stress amplitude; σ_max = σ_a + σ_m; E_eff = C1·E_s·ρ̄^n; σ_peak peak nominal strut stress (beam theory, no notch); σ_rms energy-equivalent strut stress; k_peak = σ_peak/σ_a; r = σ_peak/σ_rms; f plastic shape factor (1.5 rectangular, 16/(3π) = 1.698 circular); σ_w(N) fatigue strength amplitude of the strut material at N cycles, R = −1; K_n notch factor of node, fillet and strut irregularity that is not already in σ_w; ε_m = abs(α_s − α_2)·ΔT; ν load frequency [Hz]; ν_s Poisson ratio. "Topology A" = generic Gibson–Ashby bending foam constants; "B" = BCC strut lattice, slender-beam model derived in D3; "C" = octet truss, pin-jointed affine model.

## 0. Position on the prompt, the orchestrator note and the Q1/Q2 answers

Accepted (used as stated):

- Q1 claim 1 (energy identity; the two dissipation forms agree if and only if the strut form uses σ_rms and E_eff is the true modulus). Rows R3 and R9 test it on two geometries.
- Q1 claim 5 (constant ψ transfers from a solid coupon without a bending correction).
- Q1 octet constants E_100 = ρ̄·E_s/9, ν = 1/3, strut stress 3·σ_a/ρ̄. Re-derived in D2; R1 and R2 recompute them numerically.
- Q1 claim 6 formula κ = 3^n_d/(n_d+1)² for a rectangular section (re-derived, D5).
- Q2 claim 1 for stretch-dominated lattices (strain control; E_s governs strut stress; no 1/(1−ν) in a slender strut).
- Q2 claim 2 (lattice takes the mismatch; S is small), claim 4 (bimaterial strut formula; the 0.125 + 0.375 check re-derived), claim 6 (hydrostatic case is stretch-dominated; re-derived for BCC in D3).

Disputed:

- **Orchestrator, strut stress at 20 MPa.** "224 MPa bending" is σ_a·ρ̄^(−1.5): that is the RMS stress with C1 = 1, not the peak. "100 MPa stretch" is σ_a/ρ̄: the area average, low by 3 for octet [100]. The peak values are about 1100 MPa (A), 2700 MPa (B) and 300 MPa (C). The conclusion (not survivable) stands; the numbers do not.
- **Q1 claim 4 against Q2 claim 1.** They use different peak constants for the same lattice class. Q1: σ_peak = C_σ·σ_a·ρ̄^(−1.5) with C_σ ≈ 5. Q2: C_b ≈ 0.75–1.5 in σ_peak = C_b·E_s·ρ̄^0.5·ε, obtained with M = F·l/8, ρ̄ = (t/l)² and σ̄ = E_s·ρ̄²·ε, which implies C_σ = 0.75. The Q2 chain mixes the empirical C1 = 1 with an idealised beam cell whose own modulus is 16·E_s·(t/l)⁴. C_b = C_σ·C1 must come from one geometry (D4).
- **Q2 claim 8, "conservative by 1–4 for bending-dominated strut lattices".** For BCC under equibiaxial strain the slender-beam model gives σ_peak/(E_s·ε_m) ≈ 2.10·ρ̄^0.5 + 0.37·ρ̄, which is 0.70 at ρ̄ = 0.1 and 1.48 at ρ̄ = 0.4. The margin is about 0.7–1.4, and c = 1 is non-conservative above ρ̄ ≈ 0.2 (D4, R7).
- **Q2 claim 8, K_f ≈ 2–3.** If σ_w is taken from as-built specimens, roughness is already in it. Applying K_f = 2–3 on top counts it twice. Only K_n belongs in the formula then.
- **Q1 claim 7 (Zener damping) as a Q4 issue.** At 1 Hz it is below 2 % of ψ = 5e-3 for struts up to 0.5 mm, about 20 % for 2 mm struts, and nil at 1 per day (R23). It matters near 20–400 Hz only.
- **Prompt, "E_eff ≈ E_s·ρ̄²" as a default.** For BCC, the common AM bending lattice, the slender-beam value is 0.092·E_s·ρ̄² (D3). The two moduli the prompt offers cross at ρ̄ = 1/9; above it the "octet" modulus is the lower one.
- **Prompt Q4, "use the largest σ_a that passes both".** The collapse check never binds for high-cycle loading (C4), "elastic" needs the first-yield limit, not the collapse limit (C5), and the largest σ_a does not maximise the life-integrated entropy (C9).
- **Prompt Q4, the suspicion that fatigue matters only through τ_wearout.** True for diurnal loading; not established for N above about 1e8 cycles (C9, C10).

Needs a computation or a source to settle: the constants C1, C_σ, C_b for a real cell (R6, R7; FE is out of scope and is listed in §6); every material constant marked FROM MEMORY in §3.1; the reported normalised endurance ratios (S3); ψ of AlSi10Mg and its amplitude dependence (S3).

## 1. Claims

Each claim: statement; confidence; falsifier (row ids refer to §3.2).

**Q4 and the Q1 inputs it needs**

- **C1. Energy identity holds; the form does not matter, the stress definition does.** V_env·σ_a²/(2·E_eff) = ρ̄·V_env·σ_rms²/(2·E_s) [J]. Confidence: high. Falsifier: R3 or R9 finds the two energies different by more than 1e-6 relative in a linear cell model.
- **C2. The fatigue check needs σ_peak, and k_peak is 5 to 12 times ρ̄^(−1.5) for bending cells.** k_peak = (f/C_pl)·ρ̄^(−1.5) for A (C_pl = 0.3, so 5.0 to 5.7) and 11.43·ρ̄^(−1.5) + 1/ρ̄ for B. At ρ̄ = 0.2: about 56 (A), 133 (B), 15 (C along [100] or [111]), 30 (C along [110]). Confidence: medium (exponents high, constants medium). Falsifier: R6 gives C_σ below 3 for BCC at ρ̄ ≤ 0.2; or a published unit-cell FE result with k_peak·ρ̄^1.5 below 3.
- **C3. E_eff = E_s·ρ̄² overstates the modulus of a BCC strut lattice by about 10 in the slender limit.** E_BCC,[001] = (√3/(6π))·E_s·ρ̄² = 0.0919·E_s·ρ̄²; collapse 0.1486·σ_y·ρ̄^1.5. Node volume raises both at ρ̄ ≥ 0.2 (size of the correction UNSURE, perhaps 2 to 4 on the modulus). Confidence: high for the slender-beam algebra, medium-low for applicability at ρ̄ = 0.2 (l/d = 4.5). Falsifier: R6 disagrees with 0.0919 at ρ̄ = 0.02 by more than 1 %; or S3 finds measured BCC moduli with C1 near 1.
- **C4. Within one topology the fatigue limit and the collapse limit have the same ρ̄ exponent, so there is no crossover in ρ̄.** Ratio of fatigue-limited to collapse-limited σ_a: σ_w(N)/(f·K_n·σ_y) for bending, σ_w(N)/(K_n·σ_y) for stretch. With σ_w = 60 MPa, σ_y = 250 MPa, K_n = 1: 0.16 and 0.24. The crossover is in N: the first-yield limit takes over below N_x ≈ 5e2 cycles (as-built curve, D6). Confidence: high given the models (the ρ̄-independence is true by construction in them). Falsifier, experimental: for one topology and process, the ratio of lattice fatigue strength to lattice yield strength varies systematically with ρ̄ (a strut-size effect). S3 checks whether the cited datasets show this.
- **C5. Largest elastic, survivable σ_a at ρ̄ = 0.2, N = 1e7, R = −1, K_n = 1: about 1.1 MPa (A), 0.45 MPa (B), 4.0 MPa (C, [100]), 2.0 MPa (C, [110]).** K_n = 2 halves each. The prompt's "1–2 MPa" fits A only. "Elastic" is the first-yield limit σ_y/k_peak (4.5, 1.9, 16.7, 8.3 MPa), which is below collapse for bending cells. Confidence: medium (inputs FROM MEMORY). Falsifier: R14; S3 finds σ_w(1e7) of as-built AlSi10Mg outside 40–100 MPa.
- **C6. Σ̇ at those amplitudes, ν = 1 Hz: about 3.4e-6 W/K (A), 6.7e-6 W/K (B), 8.6e-5 W/K (C). At 1 per day: divide by 86 400.** At fixed σ_a the modulus choice changes Σ̇ by 9·ρ̄ (1.8 at ρ̄ = 0.2, 1 at ρ̄ = 1/9). Between self-consistent pairs (σ_a and E_eff from the same topology) it changes by about 25. A table that crosses σ_a from one topology with E_eff from the other is not a physical case. Confidence: high for the arithmetic, medium for the inputs. Falsifier: R16, R17.
- **C7. The life-integrated entropy does not depend on ν.** S_life = N_f·ψ·V·σ_a²/(2·E_eff·T₀). ν sets Σ̇ and τ_wearout = N_f/ν only. The 1 Hz and 1 per day cases differ in total only when a service-life cap τ_s truncates one of them: S = Σ̇·min(N_f/ν, τ_s). Confidence: high (true by construction in the model). Falsifier, physical: ψ depends on frequency between 1e-5 and 1 Hz (R23 covers the thermoelastic part only).
- **C8. With the strut stress as the constraint, E_eff drops out.** S_life ≤ N·ψ·ρ̄·V_env·σ_w(N)²/(2·E_s·T₀·K_n²·r²). At N = 1e7: 857 J/K divided by r² (r² = 1 for C [100], 1.8 for C [111], 6 for C [110], about 12.7 for B, 25 for A): about 857, 476, 143, 67 and 34 J/K. Confidence: high for the formula, medium for the values. Falsifier: R18 against R16×N.
- **C9. Life entropy grows as N^(1+2b), so the fatigue-limited case at 1e7 cycles is not the upper bound.** With b between −0.095 and −0.143 the bound for C [100] reaches about 1.6e4–2.5e4 J/K at N = 6.3e8 (1 Hz for 20 years, strut amplitude 33–40 MPa), and about 2.5–5 J/K at N = 7305 (1 per day for 20 years). Confidence: medium (Basquin extrapolated past 1e7; constant ψ). Falsifier: R19 shows the maximum of S(σ_a) at a sweep edge or a different order of magnitude.
- **C10. Verdict candidate: fatigue dissipation is immaterial for diurnal loading in every case, and for bending cells below about 1e9 cycles; it is borderline for a stretch-dominated lattice run near its fatigue limit for more than about 1e8 cycles.** "Borderline" is against the prompt's comparator of 1e3–1e5 J/K. Against LPBF process energy and primary-metal exergy (about 1e5–1e6 J/K for 0.53 kg, FROM MEMORY, UNSURE) it stays below about 10 %. Confidence: medium-low (depends on the comparator and on ψ at 30–60 MPa). Falsifier: R19, R20; S3 on LPBF specific energy and on ψ.
- **C11. The part mass is 0.53 kg, not about 1 kg.** m = ρ_s·ρ̄·V_env. Confidence: high. Falsifier: R10.
- **C12. The ψ given in the prompt has no stated amplitude, which leaves a factor of about 0.2–6 on Σ̇.** With D ∝ σ^n_d, the factor is κ·(σ_rms/σ_ref)^(n_d−2). Confidence: medium. Falsifier: S3 finds data showing n_d = 2 for Al alloys up to 60 MPa; R22 quantifies the range.
- **C13. Local accumulated entropy at the strut hot spot at N = 1e7 is about 4.3 MJ/(m³·K) with ψ = 5e-3 and 60 MPa.** This is the same order as the fatigue fracture entropy reported for Al 6061-T6 (about 4 MJ/(m³·K), FROM MEMORY, UNSURE). It is an order-of-magnitude cross-check on ψ, not a validation: that quantity is defined from plastic work in low-cycle tests. Confidence: low. Falsifier: R21; S3 on the value.

**Q2 inputs that Q5 needs**

- **C14. For pin-jointed affine lattices the strut stress under mismatch cannot exceed E_s times the largest principal macroscopic strain magnitude.** Octet, equibiaxial ε_m, free normal: in-plane struts at E_s·ε_m, ε_zz = −ε_m, biaxial modulus ρ̄·E_s/6. Confidence: high. Falsifier: R4.
- **C15. For BCC the mismatch constant is C_b ≈ 1.05 (uniaxial stress) and ≈ 2.10 (equibiaxial, free normal), plus an axial term.** σ_peak/(E_s·ε) = 1.05·ρ̄^0.5 + 0.092·ρ̄ (uniaxial); 2.10·ρ̄^0.5 + 0.37·ρ̄ (equibiaxial). The equibiaxial value passes 1 at ρ̄ ≈ 0.20. The Gibson–Ashby pair (C_σ = 5, C1 = 1) would give 5·ρ̄^0.5; that pair is two foam fits, not one geometry, and should not be multiplied. Confidence: medium. Falsifier: R6, R7; unit-cell FE (§6).
- **C16. S = M_L·H_L/(M_2·H_2) is below about 0.1 for H_L = H_2 and the listed partners, so the partner stiffness changes strut stress by less than about 10 %.** This is inside Q2's "within about 15 %". Q2's range "0.01–0.16" is E_L/E_s, not S; S is lower because of the biaxial factors and the partner modulus. Confidence: high. Falsifier: R29.
- **C17. Diurnal mismatch alone is not life-limiting for AlSi10Mg with ΔT ≤ 50 K.** Worst listed pair (Ti-6Al-4V, Δα = 12.4e-6/K): E_s·ε_m = 43 MPa, σ_a,loc = 22·K_n MPa. With K_n = 3: N ≈ 6e6 cycles, about 1.5e4 years at 1 per day. The ΔT that gives N = 1.1e4 cycles (30 years) is about 120 K for K_n = 3. Confidence: medium. Falsifier: R30 finds N below 1.1e4 inside ΔT ≤ 50 K, c ≤ 1.5, K_n ≤ 3 without mean stress.
- **C18. Mean stress can reverse C17.** Cool-down mismatch E_s·Δα·ΔT_ref reaches σ_y for ΔT_ref ≈ 290 K (Ti partner). A mean stress near σ_y raises the equivalent amplitude by 1/(1 − σ_m/σ_u), up to about 2.7 (Goodman). For any R ≠ −1 the collapse and first-yield checks apply to σ_max, not σ_a. Confidence: medium. Falsifier: R25, R30.
- **C19. Under strain control the modulus choice acts in the opposite direction.** Dissipation per cycle = ψ·V·M_L·ε_a² (equibiaxial), rising with E_eff; under stress control it falls with E_eff. Diurnal mismatch dissipation over 30 years is about 0.04 J/K: immaterial by more than four orders. Confidence: high. Falsifier: R31.

**Q3**

- **C20. Basquin with macroscopic σ_a and solid-material σ_f', b is not acceptable.** It overpredicts life by (K_n·k_peak)^(−1/b): about 1e8 (C, b = −0.143) to 1e22 (B, b = −0.095) at ρ̄ = 0.2. Two acceptable forms: (i) local stress, σ_loc = K_n·k_peak·σ_a into an S–N curve of as-built thin struts; (ii) a lattice-level power law with the stress divided by the same lattice's quasi-static yield or plateau stress, fitted per topology and process. Confidence: high for the first sentence, medium for the rest. Falsifier: R26; a dataset where solid constants with macroscopic stress predict lattice life within a factor of 10.
- **C21. The literature normalises in three ways.** (a) By the lattice's own yield or plateau stress: Hrabe 2011, Amin Yavari 2013 and 2015, Zhao 2016; numerically Zargarian 2016. (b) By a power law in ρ̄ for the fatigue strength: Li 2012, Zargarian 2016. (c) By local strut stress from beam theory or FE on as-built geometry: Van Hooreweder and Kruth 2017, Dallago 2018 and 2019, Burr 2020. Normalising by lattice yield collapses densities within one cell type but not across cell types (Amin Yavari 2015, Ahmadi 2018). Normalising by the solid's fatigue strength appears in reviews (Benedetti 2021), UNSURE. Confidence: medium (from memory). Falsifier: S3.
- **C22. C4 predicts the normalised endurance ratio.** σ_a,lattice/σ_y,lattice at run-out = σ_w/(f·K_n·σ_y): 0.14–0.16 for bending cells in as-built Ti-6Al-4V and AlSi10Mg with K_n = 1 (0.21–0.24 for stretch cells). Reported values are of this order (0.15–0.25 in Hrabe 2011, about 0.2 in Amin Yavari 2013, up to about 0.6 for sheet TPMS in Bobbert 2017; all UNSURE, and the reported stress is usually σ_max at R = 0.1, not σ_a). Confidence: medium-low. Falsifier: R27 with S3-verified ratios; a mismatch above a factor of 3 after converting σ_max to σ_a.
- **C23. As-built surface and near-surface porosity control strut fatigue, and there is no standard knock-down factor.** Reported reductions from machined to as-built surface are about 0.4–0.6 in Ti-6Al-4V and 0.5–0.8 in AlSi10Mg (FROM MEMORY, UNSURE). Thin struts are worse than bulk as-built coupons (waviness, section variation, partly fused powder). HIP alone helps little with an as-built surface; chemical etching with HIP helps (Van Hooreweder 2017). Defect-based prediction uses the √area parameter (Murakami 2002; Romano 2018; Beretta and Romano 2017). Confidence: medium. Falsifier: S3.
- **C24. Lattice S–N data are mostly compression–compression at R = 0.1, and their exponent should not be transferred to tension, shear or mismatch loading.** Failure there combines cyclic ratcheting and strut cracking (Li 2012; Zhao 2016). Tension–tension lives are shorter (Lietaert 2018); the stress ratio matters (de Krijger 2017). Confidence: medium. Falsifier: S3.
- **C25. τ_wearout = N/ν needs a cap.** Aluminium alloys have no endurance limit, constant-b extrapolation beyond 1e7–1e8 is unverified, and at 1 per day N = 1e7 means 27 000 years. Use τ = min(N_f/ν, τ_service). Confidence: high. Falsifier: none computational; R18 shows the magnitudes.
- **C26. The as-built anchor fixes b.** A curve through σ_w(1e7) = 60 MPa with b = −0.10 implies σ_f' = 322 MPa, below σ_u. Holding σ_f' = 1.67·σ_u = 668 MPa gives b = −0.143. S2 carries both b = −0.095 (notch as a constant stress multiplier) and b = −0.143 (as-built curve), and a wider sweep. Confidence: medium. Falsifier: R14 consistency output; S3 on as-built AlSi10Mg S–N slopes.

## 2. Derivations

**D1. Dissipation and its bound.** Per cycle and per unit envelope volume the stored energy at amplitude is u = σ_a²/(2·E_eff) [J/m³]; dissipated energy ΔW = ψ·u·V_env [J]; entropy per cycle ΔS = ΔW/T₀ [J/K]; Σ̇ = ν·ΔS [W/K]. By Clapeyron, u·V_env = ρ̄·V_env·σ_rms²/(2·E_s), which defines σ_rms. With σ_peak = r·σ_rms and the fatigue constraint K_n·σ_peak ≤ σ_w(N):
ΔS ≤ ψ·ρ̄·V_env·σ_w(N)²/(2·E_s·T₀·K_n²·r²), and S_life = N·ΔS.
At N = 1e7, σ_w = 60 MPa, ρ̄·V_env = 2e-4 m³, E_s = 70 GPa: (60e6)²/(1.4e11) = 25 714 J/m³; × 2e-4 = 5.143 J; × 5e-3 / 300 = 8.571e-5 J/K per cycle; × 1e7 = 857 J/K, divided by K_n²·r².
With σ_w(N) = σ_w7·(N/1e7)^b: S_life(N) = S_life(1e7)·(N/1e7)^(1+2b).

**D2. Octet, pin-jointed affine model.** Six strut axes ⟨110⟩/√2. C_ijkl = ρ̄·E_s·⟨n_i n_j n_k n_l⟩. ⟨n_1⁴⟩ = 1/6, ⟨n_1² n_2²⟩ = 1/12, so C11 = ρ̄E_s/6, C12 = C44 = ρ̄E_s/12.
- E_100 = (C11−C12)(C11+2C12)/(C11+C12) = ρ̄E_s/9; ν = C12/(C11+C12) = 1/3; G = ρ̄E_s/12; bulk modulus ρ̄E_s/9.
- In units of 1/(ρ̄E_s): S11 = 9, S12 = −3, S44 = 12. E_110 = ρ̄E_s/6; E_111 = ρ̄E_s/5.
- Strut stress = E_s·n·ε·n. Load along [100]: all struts at ±3σ_a/ρ̄ (r = 1). Along [111]: three families at +3σ_a/ρ̄, three at −σ_a/ρ̄ (peak 3/ρ̄, r² = 9/5). Along [110]: one family at 6σ_a/ρ̄, the rest at zero (peak 6/ρ̄, r² = 6).
- Collapse (first yield equals collapse for axial struts): ρ̄σ_y/3 along [100] and [111]; ρ̄σ_y/6 along [110].
- Euler buckling of a solid round strut, pin ends: σ_E = π²·E_s·(a/l)²/4 with ρ̄ = 6√2·π·(a/l)². σ_E = σ_y at ρ̄ ≈ 0.039 for σ_y/E_s = 250/70 000. Yield governs for ρ̄ ≥ 0.05.
- So "ρ̄E_s/9, ρ̄σ_y/3" is the cube-axis case. Off-axis loading halves the survivable σ_a.

**D3. BCC strut lattice, slender-beam model.** Cubic cell of side L; eight round struts of diameter d from the centre to the corners, length l = √3·L/2, direction n = (1,1,1)/√3. ρ̄ = √3·π·(d/L)² (node overlap ignored). For strains aligned with the cube axes, mirror symmetry gives zero node rotation: each strut is a fixed–guided beam.
- Uniaxial stress σ̄ along z, lateral faces free: each strut carries F = σ̄·L²/4 along z (the lateral force vanishes by symmetry). Transverse component F·√(2/3), axial component F/√3.
- End moment M = F·√(2/3)·l/2. Peak bending stress 32M/(π d³) = (2√2/π)·σ̄·(L/d)³ = 11.43·σ̄·ρ̄^(−1.5). Axial stress 4F/(√3·π·d²) = σ̄/ρ̄. So k_peak = 11.43·ρ̄^(−1.5) + 1/ρ̄.
- Deflection: δ_t = F_t·l³/(12·E_s·I), I = π d⁴/64; δ_z = δ_t·√(2/3) + axial part. Bending only: E* = (√3·π/2)·E_s·(d/L)⁴ = (√3/(6π))·E_s·ρ̄² = 0.0919·E_s·ρ̄². Axial part adds 1/((8/3)(l/d)²) to the compliance: 1.8 % at ρ̄ = 0.2. Poisson ratio → 0.5.
- Collapse with plastic hinges at both ends, M_p = σ_y·d³/6: σ_pl = (4√2/3)·σ_y·(d/L)³ = 0.1486·σ_y·ρ̄^1.5. First yield (bending only) = σ_pl/1.698.
- RMS: circular section and linear moment give σ_peak,bending/σ_rms = 2√3. With the axial stress in the peak, r ≈ 3.57 at ρ̄ = 0.2 (r² ≈ 12.7).
- Hydrostatic strain: the corner displacement is along n, so the strut is purely axial, σ = E_s·ε_m (agrees with Q2 claim 6).
- At ρ̄ = 0.2: d/L = 0.192, l/d = 4.5. Euler–Bernoulli is stretched; Timoshenko shear softens k_t by about 10 %, node volume stiffens it. Expect ±20 % or worse on the constants (UNSURE).

**D4. Strain-controlled peak stress (mismatch).** General: strut force F = k_a·(Δ·n)·n + k_t·(Δ − (Δ·n)·n), with Δ = (L/2)·(ε_x, ε_y, ε_z), k_a = E_s·A/l, k_t = 12·E_s·I/l³. Peak stress = E_s·[abs(Δ·n)/l] + 3·E_s·d·abs(Δ_t)/l².
- The axial force must be kept even though Δ·n → 0: k_a·(Δ·n) stays finite. Dropping it gives a modulus low by 1.5 (a trap for S2).
- Uniaxial stress: Δ_t magnitude (L/2)·ε·√1.5; σ_peak = 2.449·E_s·ε·(d/L) + σ̄/ρ̄ = (1.050·ρ̄^0.5 + 0.092·ρ̄)·E_s·ε.
- Equibiaxial ε_x = ε_y = ε_m, σ_zz = 0: ε_z → −2ε_m; Δ_t magnitude (L/2)·ε_m·√6; axial force N = √3·k_t·L·ε_m; biaxial modulus σ̄_xx/ε_m = 6k_t/L = 0.1838·E_s·ρ̄² (equal to E*/(1−0.5), a consistency check between two routes). σ_peak = (2.100·ρ̄^0.5 + 0.368·ρ̄)·E_s·ε_m. Equal to E_s·ε_m at ρ̄ ≈ 0.195.
- Relation between the Q1 and Q2 constants: C_b = C_σ·C1 on the same geometry. BCC: 11.43 × 0.0919 = 1.05. Q2's chain: C_σ = 0.75 with C1 = 1, while its own beam cell (fixed–fixed, central load) has C1 = 16 and σ_peak/(E_s·ε) = 12·(t/l).

**D5. Section and moment integrals.** Linear moment along the strut gives ⟨M²⟩/M_max² = 1/3 and ⟨abs(M)^n⟩/M_max^n = 1/(n+1). Rectangular section: ⟨abs(y)^n⟩/(t/2)^n = 1/(n+1). Circular: ⟨abs(y)^n⟩/R^n = (2/π)·B((n+1)/2, 3/2), which is 1/4, 0.1698 and 1/8 for n = 2, 3, 4. Hence σ_peak/σ_rms = 3 (rectangular), 2√3 (circular). κ(n_d) = ⟨abs(σ)^n_d⟩/σ_rms^n_d: rectangular 3^n_d/(n_d+1)² = 1, 1.69, 3.24; circular 1, 1.76, 3.60 for n_d = 2, 3, 4.

**D6. Q4 limits at ρ̄ = 0.2** (ρ̄^1.5 = 0.08944; σ_y = 250 MPa; σ_w7 = 60 MPa; K_n = 1; R = −1).

| Topology | E_eff [GPa] | Collapse [MPa] | First yield [MPa] | k_peak | Fatigue-limited σ_a at 1e7 [MPa] | Binding |
|---|---|---|---|---|---|---|
| A, f = 1.5 | 2.80 | 6.71 | 4.47 | 55.9 | 1.07 | fatigue |
| B (BCC) | 0.253 | 3.32 | 1.88 | 132.8 | 0.452 | fatigue |
| C [100] | 1.556 | 16.7 | 16.7 | 15 | 4.00 | fatigue |
| C [110] | 2.33 | 8.33 | 8.33 | 30 | 2.00 | fatigue |

Elastic buckling: A, 0.05·E_s·ρ̄² = 140 MPa; C, strut Euler stress about 1300 MPa at ρ̄ = 0.2. Neither binds.
Basquin anchored at 1e7: σ_w(N) = σ_w7·(N/1e7)^b. Implied σ_f' = σ_w7·(2e7)^(−b): 322 MPa for b = −0.10, 668 MPa for b = −0.1434. First yield overtakes fatigue where σ_w(N_x) = K_n·σ_y: N_x = 1e7·(K_n·σ_y/σ_w7)^(1/b) ≈ 475 cycles for b = −0.1434.

**D7. Σ̇ at the fatigue-limited amplitude, ρ̄ = 0.2, V = 1e-3 m³, ψ = 5e-3, T₀ = 300 K.**
- A: (1.0733e6)²/(2 × 2.8e9) = 205.7 J/m³; ΔS = 205.7 × 1e-3 × 5e-3/300 = 3.43e-6 J/K per cycle.
- B: (0.4519e6)²/(2 × 2.527e8) ≈ 404 J/m³; ΔS ≈ 6.7e-6 J/K per cycle.
- C [100]: (4.0e6)²/(2 × 1.5556e9) = 5143 J/m³; ΔS = 8.57e-5 J/K per cycle.
- Σ̇ = ΔS × 1 Hz, or ΔS/86 400 for 1 per day (3.97e-11, 7.8e-11, 9.92e-10 W/K).
- Fixed σ_a = 1 MPa: 2.98e-6 J/K per cycle with E_s·ρ̄², 5.36e-6 with ρ̄·E_s/9 (ratio 9ρ̄ = 1.8).
- Regression of the orchestrator figure: 20 MPa with E_s·ρ̄² gives 1.19e-3 W/K at 1 Hz and 3.76e4 J/K per year.

**D8. Entropy over life.** τ_wearout = N/ν: 1e7 cycles is 0.317 years at 1 Hz and 27 379 years at 1 per day; S_life is the same for both (C7). With a service cap τ_s = 20 years:
- 1 Hz: N = 6.31e8. b = −0.1434: σ_w = 33.1 MPa, S(C [100]) = 857 × 63.1 × 0.552² ≈ 1.65e4 J/K, σ_a = 2.21 MPa. b = −0.095: σ_w = 40.5 MPa, S ≈ 2.46e4 J/K.
- 1 per day: N = 7305. b = −0.1434: σ_w = 169 MPa (below σ_y, so fatigue still binds), S ≈ 5.0 J/K, σ_a = 11.3 MPa. b = −0.095: S ≈ 2.5 J/K.
- A and B: divide by 25 and by about 12.7.
- S(σ_a) at fixed τ_s rises as σ_a² until N_f(σ_a) = ν·τ_s, then falls as σ_a^(2+1/b). The maximum is interior; R19 must bracket it.

**D9. Comparators** (m = 0.534 kg). Melt-and-reject floor: m·(c_p·(T_liq − T₀) + h_f)/T₀ = 0.534 × (900 × 573 + 397e3)/300 ≈ 1.6e3 J/K. LPBF electricity 50–500 MJ/kg: 0.9e5–9e5 J/K. Primary aluminium, about 200 MJ/kg: 3.6e5 J/K. The prompt's range is 1e3–1e5 J/K. All but the first are FROM MEMORY and UNSURE.

**D10. Mismatch magnitudes.** AlSi10Mg on Ti-6Al-4V, ΔT = 50 K: ε_m = 6.2e-4; E_s·ε_m = 43.4 MPa; σ_a,loc = ½·K_n·c·E_s·ε_m/(1+S) = 21.7 MPa (K_n = c = 1), 65 MPa (K_n = 3). Life with b = −0.1434: N = 1e7·(65.1/60)^(1/b) ≈ 5.7e6 cycles. Allowable at N = 10 958 (30 years): 159 MPa, so ΔT_x = 159/(1.302 MPa/K) ≈ 122 K for K_n = 3. Dissipation, octet, equibiaxial: U = V·M_L·ε_a² = 1e-3 × 2.333e9 × (3.1e-4)² = 0.224 J; ΔS = 3.7e-6 J/K per cycle; 0.041 J/K in 30 years. Thermal lag term E_s·α_s·ΔT_lag equals the Δα term when ΔT_lag/ΔT = Δα/α_s (0.59 for Ti, 0.24 for 316L).

**D11. Thermoelastic damping.** Δ_E = E_s·α_s²·T₀/(ρ_s·c_p) = 3.85e-3; ψ_TE(f) = 2π·Δ_E·(f/f_Z)/(1 + (f/f_Z)²), maximum π·Δ_E = 1.21e-2; f_Z = π·D/(2·t²), D = k/(ρ_s·c_p) = 5.41e-5 m²/s. t = 0.5 mm: f_Z = 340 Hz, ψ_TE(1 Hz) = 7.1e-5. t = 2 mm: f_Z = 21 Hz, ψ_TE(1 Hz) = 1.1e-3. The reed formula is applied to round struts, so prefactors are UNSURE. It applies to the bending part only.

## 3. Computation spec

Plain Python and numpy only. One script per group; suggested names in `local_docs/fable_runs/prompt_3_code/`: `p3_unit_cells.py` (R1–R9), `p3_q4_limits.py` (R10–R15), `p3_q4_entropy.py` (R16–R21), `p3_sensitivity.py` (R22–R25), `p3_q3_normalisation.py` (R26–R27), `p3_mismatch.py` (R28–R32). Each script prints every row's value, the expected value and pass or fail. A row that is true by construction is labelled "identity" and is not a check.

### 3.1 Inputs

FROM MEMORY marks a value S3 must check first. Ranges are sweep bounds, not uncertainties.

| Symbol | Value | Range | Source status |
|---|---|---|---|
| ρ̄ | 0.2 (Q4) | 0.05, 0.10, 1/9, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50 | prompt; sweep widened |
| V_env | 1e-3 m³ | — | prompt |
| ψ | 5e-3 | 1e-3 to 1e-2 | prompt |
| T₀ | 300 K | — | prompt |
| ν | 1 Hz; 1/86 400 Hz | — | prompt |
| year | 3.15576e7 s | — | definition (365.25 d) |
| E_s | 70 GPa | 65–75 | FROM MEMORY |
| ν_s | 0.33 | — | FROM MEMORY |
| ρ_s | 2670 kg/m³ | — | FROM MEMORY |
| σ_y (LPBF AlSi10Mg) | 250 MPa | 200–280 | FROM MEMORY |
| σ_u | 400 MPa | 330–460 | FROM MEMORY |
| σ_w7, as-built surface, R = −1, amplitude at 1e7 | 60 MPa | 40–100 | FROM MEMORY, UNSURE |
| σ_w7, machined | 135 MPa (from σ_f', b below) | 90–150 | FROM MEMORY, UNSURE |
| σ_f' | 1.67·σ_u = 668 MPa | — | FROM MEMORY (uniform material law for Al alloys) |
| b, machined | −0.095 | −0.07 to −0.20 | FROM MEMORY |
| b, as-built | ln(σ_w7/σ_f')/ln(2e7) = −0.1434 | same sweep | derived from the two rows above |
| K_n | 1 | 1, 1.5, 2, 3, 4 | assumption; Q2 quotes 2–3 (UNSURE) |
| Gibson–Ashby C1 | 1 | — | FROM MEMORY |
| Gibson–Ashby C_pl | 0.3 | — | FROM MEMORY |
| Gibson–Ashby buckling constant | 0.05 | — | FROM MEMORY |
| Shape factor f | 1.5; 16/(3π) | — | derived (standard) |
| Octet C1, strength constant | 1/9; 1/3 | — | derived in D2; also FROM MEMORY of the octet paper |
| BCC constants | 0.0919; 0.1486; 11.43 | — | derived in D3; closed forms FROM MEMORY of the BCC paper |
| α_s (AlSi10Mg) | 21e-6 /K | 20–23e-6 | FROM MEMORY |
| k (AlSi10Mg) | 130 W/(m·K) | 100–170 | FROM MEMORY |
| c_p | 900 J/(kg·K) | — | FROM MEMORY |
| h_f (Al) | 397 kJ/kg | — | FROM MEMORY |
| T_liq | 873 K | — | FROM MEMORY |
| Partner α [1e-6/K], E [GPa], ν | Ti-6Al-4V 8.6, 114, 0.34; steel 12, 200, 0.30; 316L 16, 193, 0.30; Cu 16.5, 120, 0.34; Invar 1.3, 141, 0.29 | — | FROM MEMORY |
| ΔT (diurnal) | 10, 20, 30, 50 K | extended to 100, 200, 300, 500 K to bracket the crossover | prompt; extension is S1's |
| ΔT_ref (cool-down) | 100, 200, 300 K | — | assumption |
| Fatigue fracture entropy, Al 6061-T6 | 4 MJ/(m³·K) | — | FROM MEMORY, UNSURE |
| LPBF specific energy | 50–500 MJ/kg | — | FROM MEMORY, UNSURE |
| Primary Al embodied energy | 200 MJ/kg | 150–220 | FROM MEMORY, UNSURE |
| Ti-6Al-4V σ_y; as-built σ_w at 1e6–1e7 | 950 MPa; 200 MPa | 150–300 | FROM MEMORY, UNSURE |
| Lazan exponent n_d | 2 | 2, 2.3, 2.5, 3 | FROM MEMORY, UNSURE |
| σ_ref for ψ | 20 MPa | 5, 20, 60 MPa | assumption (the prompt gives none) |
| Timoshenko shear factor, round | 0.9 | — | FROM MEMORY |

### 3.2 Rows

| Row | Quantity | Method or formula | Inputs with units | Sanity check or expected range | Tolerance | Supports claim |
|---|---|---|---|---|---|---|
| R1 | Octet elastic constants E_100, E_110, E_111, ν, G, bulk modulus, each over ρ̄·E_s | Build C_ijkl = ρ̄·E_s·(1/6)·Σ_k n_i n_j n_k n_l over the six unit vectors ⟨110⟩/√2; form the 6×6 Voigt matrix (engineering shear); invert numerically. For a direction d apply stress d⊗d and read strain along d | ρ̄ = 1 and E_s = 1 (normalised) | 1/9, 1/6, 1/5, 1/3, 1/12, 1/9 (closed forms of D2, an independent hand route) | 1e-9 relative | C1, C6 |
| R2 | Octet strut stress over σ_a, per family, for load along [100], [110], [111]; peak and RMS | Strain from R1 compliance; strut strain n·ε·n; stress E_s × strain | as R1; report × ρ̄ | [100]: all ±3, r² = 1. [111]: +3 (three families), −1 (three), r² = 1.8. [110]: 6 (one family), 0 (five), r² = 6 | 1e-9 | C2, C5, C8 |
| R3 | Octet energy identity | U_macro = σ_a²/(2·E_d) from R1 against U_strut = ρ̄·mean(σ_k²)/(2·E_s) from R2, three directions | as R1 | Equal. Tests Clapeyron and the implementation by two routes; it does not test the pin-jointed assumption | 1e-9 | C1 |
| R4 | Octet under mismatch strain: (a) equibiaxial ε_x = ε_y = ε_m with σ_zz = 0; (b) hydrostatic | Solve ε_zz from σ_zz = 0 with C from R1; strut strains; macroscopic stress | ε_m = 1 (normalised) | (a) ε_zz = −1; in-plane struts at E_s·ε_m; others 0; σ̄_xx = ρ̄E_s/6. (b) all struts at E_s·ε_m; σ̄ = ρ̄E_s/3. Max strut strain ≤ ε_m | 1e-9 | C14 |
| R5 | Beam integrals: ⟨σ²⟩/σ_peak² and κ(n_d) for rectangular and circular sections with linear moment | Numerical quadrature (midpoint, ≥ 2000 points per direction) of abs(M(x)·y)^n over length and section area | n_d = 2, 2.3, 2.5, 3, 4 | ⟨σ²⟩/σ_peak²: 1/9 and 1/12. κ rectangular: 1, 1.69, 3.24 at n_d = 2, 3, 4; circular: 1, 1.76, 3.60. κ(2) = 1 is an identity | 1e-3 | C12, Q1 claim 6 |
| R6 | BCC single strut, uniaxial stress along z: C1(ρ̄) = E*/(E_s·ρ̄²), C_σ = σ_peak·ρ̄^1.5/σ̄ (bending only and with axial), C_b = σ_peak/(E_s·ε·ρ̄^0.5), Poisson ratio | Stiffness route: F = k_a·(Δ·n)·n + k_t·(Δ − (Δ·n)·n); Δ = (L/2)(ε_x, ε_x, ε_z); solve ε_x from F_x = 0; σ̄ = 4·F_z/L². Run Euler–Bernoulli, then Timoshenko with k_t/(1+Φ), Φ = 12·E_s·I/(0.9·G_s·A·l²) | L = 1; d/L = sqrt(ρ̄/(√3·π)); ρ̄ = 0.02 and the sweep list; E_s = 1; ν_s = 0.33 | At ρ̄ = 0.02, Euler–Bernoulli: C1 = 0.0919 (within 0.5 % low), C_σ,bending = 11.43, C_b,bending = 1.050, Poisson ratio → 0.5. At ρ̄ = 0.2: C1 ≈ 0.0902, k_peak ≈ 132.8. The closed forms come from a force (flexibility) route in D3 | 1 % at ρ̄ = 0.02; report the drift at higher ρ̄ and the Timoshenko difference | C2, C3, C15 |
| R7 | BCC under equibiaxial strain with σ_zz = 0: ε_z/ε_m, σ_peak/(E_s·ε_m), biaxial modulus, ρ̄ at which σ_peak = E_s·ε_m; also hydrostatic strain | Same strut model; Δ = (L/2)(ε_m, ε_m, ε_z); solve ε_z from F_z = 0; σ̄_xx = 4·F_x/L²; root by bisection on ρ̄ in 0.02–0.6 | as R6 | Slender limit: ε_z/ε_m → −2; σ_peak/(E_s·ε_m) = 2.100·ρ̄^0.5 + 0.368·ρ̄; biaxial modulus 0.1838·E_s·ρ̄² and equal to E*/(1−ν) from R6 (two routes); crossover ρ̄ in 0.19–0.23. Hydrostatic: σ_strut = E_s·ε_m, zero bending | 2 % at ρ̄ = 0.02; crossover reported, not pass/fail | C15, Q2 claims 1, 6, 8 |
| R8 | BCC collapse and first yield against ρ̄ | Collapse (4√2/3)·σ_y·(d/L)³; first yield σ_y/k_peak with k_peak from R6 | σ_y = 250 MPa; sweep ρ̄ | At 0.2: collapse 3.32 MPa; first yield 1.88 MPa. Ratio collapse to bending-only first yield = 16/(3π): algebra check, not physics | 1 % | C3, C5 |
| R9 | BCC energy identity and r | U_macro = σ̄²/(2·E*) from R6 against (8/L³)·[∫M(x)²/(2·E_s·I) dx + N²·l/(2·E_s·A)] by quadrature, M(x) = F_t·(l/2 − x); σ_rms from the energy; r = σ_peak/σ_rms | as R6, Euler–Bernoulli | Equal energies; r(bending only) → 2√3 = 3.464 at ρ̄ = 0.02; r with axial ≈ 3.57 at ρ̄ = 0.2 | 1e-6 on energy; 1 % on r | C1, C8 |
| R10 | Strut volume and mass | V_s = ρ̄·V_env; m = ρ_s·V_s | ρ̄ = 0.2; V_env = 1e-3 m³; ρ_s = 2670 kg/m³ | 2e-4 m³; 0.534 kg | exact | C11 |
| R11 | Collapse strength against ρ̄, four cases | A: 0.3·ρ̄^1.5·σ_y. B: R8. C [100]: ρ̄·σ_y/3. C [110]: ρ̄·σ_y/6 | σ_y = 250 MPa (and 200, 280); sweep ρ̄ | At 0.2: 6.71, 3.32, 16.67, 8.33 MPa. The first and third reproduce the orchestrator's 6.7 and 17 MPa (regression of arithmetic only) | 0.5 % | C4, C5 |
| R12 | Elastic buckling limits | A: 0.05·E_s·ρ̄². C: ρ̄·σ_E/3, σ_E = π²·E_s·(a/l)²/4, (a/l)² = ρ̄/(6√2·π). Report the ρ̄ where buckling equals yield collapse | E_s = 70 GPa; σ_y = 250 MPa; sweep ρ̄ plus 0.01–0.05 | A at 0.2: 140 MPa. C: crossover ρ̄ ≈ 0.039; at ρ̄ = 0.05 σ_E ≈ 324 MPa. Yield governs over the whole sweep | 2 % | C5 |
| R13 | k_peak(ρ̄) for A (f = 1.5 and 1.698), B, C [100], C [110], and the orchestrator's ρ̄^(−1.5) and 1/ρ̄ | A: (f/0.3)·ρ̄^(−1.5). B: R6. C: R2 | sweep ρ̄ | At 0.2: 55.9, 63.3, ≈132.8, 15, 30; orchestrator 11.18 and 5 | 0.5 % (B: 1 %) | C2 |
| R14 | Limits on σ_a against N: fatigue σ_w7·(N/1e7)^b/(K_n·k_peak); first yield σ_y/k_peak; collapse (R11); binding limit; N_x where fatigue = first yield; implied σ_f' = σ_w7·(2e7)^(−b) | Direct | N = 1e2 … 1e10 (≥ 5 points per decade); b ∈ {−0.07, −0.095, −0.1434, −0.20}; σ_w7 ∈ {40, 60, 100} MPa; K_n ∈ {1, 1.5, 2, 3, 4}; ρ̄ sweep; four topologies | Central (ρ̄ = 0.2, σ_w7 = 60, K_n = 1, N = 1e7): 1.07, 0.452, 4.00, 2.00 MPa; fatigue binds. N_x ≈ 475 cycles (b = −0.1434), about 6 (b = −0.10). Implied σ_f': 322 MPa (b = −0.10), 668 MPa (b = −0.1434). Fatigue-to-collapse ratio is independent of ρ̄: identity, report once | 1 % | C4, C5, C26 |
| R15 | Regression of the superseded 20 MPa case | σ_peak = k_peak·20 MPa per topology; compare with σ_y and collapse; Σ̇ with E_s·ρ̄² | ρ̄ = 0.2; ψ, V, T₀ from the prompt; ν = 1 Hz | Peak ≈ 1118, 2655, 300, 600 MPa (all above σ_y for A, B, C); orchestrator's 224 and 100 MPa are R13's last two factors × 20. Σ̇ = 1.19e-3 W/K; 3.76e4 J/K per year | 1 % | §0 dispute |
| R16 | ΔS per cycle and Σ̇ for the matrix σ_a × E_eff × ν | ΔS = ψ·V·σ_a²/(2·E_eff·T₀); Σ̇ = ν·ΔS | σ_a ∈ {R14 central values for A, B, C [100]; 1 MPa; 2 MPa}; E_eff ∈ {E_s·ρ̄² = 2.8 GPa; ρ̄·E_s/9 = 1.556 GPa; B from R6}; ν ∈ {1, 1/86 400} Hz | Self-consistent pairs, per cycle: A 3.43e-6, B ≈ 6.7e-6, C 8.57e-5 J/K. At 1 MPa: 2.98e-6 and 5.36e-6 J/K (ratio 1.8). Flag the off-diagonal cells as "inconsistent pair" in the output | 1 % (B: 5 %) | C6 |
| R17 | Strut-form Σ̇ | ν·ψ·ρ̄·V·σ_rms²/(2·E_s·T₀) with σ_rms from R2 (C) and R9 (B) | as R16 | Equals R16 self-consistent pairs for B and C (two routes). For A there is no geometry: σ_rms is defined by the identity, so that cell is an identity, not a check | 1e-6 (C); 1e-4 (B) | C1, C6 |
| R18 | Life entropy bound and τ_wearout against N | S = N·ψ·ρ̄·V·σ_w(N)²/(2·E_s·T₀·K_n²·r²); τ = N/ν in years for both ν | N as R14; b ∈ {−0.095, −0.1434}; r² from R2, R9 and 25 for A | At 1e7: 857, 476, 143, ≈67, 34 J/K (C [100], C [111], C [110], B, A). τ: 0.317 years and 27 379 years. Must equal R16's ΔS × N for the self-consistent pairs | 1 % (B: 5 %) | C7, C8, C25 |
| R19 | S(σ_a) with a service cap; location and value of the maximum | S = ν·ΔS(σ_a)·min(N_f(σ_a)/ν, τ_s); N_f = 1e7·(K_n·k_peak·σ_a/σ_w7)^(1/b); mark σ_a above first yield as "not elastic" and exclude | σ_a = 0.05 … 30 MPa, log grid ≥ 80 points (spans the fatigue limits 0.25–11 MPa and both collapse limits 3.3–16.7 MPa); τ_s ∈ {10, 20, 30} years; both ν; b ∈ {−0.095, −0.1434}; topologies A, B, C | Maximum interior to the grid, at N_f = ν·τ_s. C [100], 20 years: 1 Hz → σ_a ≈ 2.21 MPa, S ≈ 1.65e4 J/K (b = −0.1434) or ≈ 2.46e4 J/K (b = −0.095); 1 per day → σ_a ≈ 11.3 MPa, S ≈ 5.0 J/K or ≈ 2.5 J/K. A: divide S by 25. If a maximum sits on a grid edge, widen the grid and record it in `issues.md` | 3 % | C9, C10 |
| R20 | Comparators and ratios | Melt floor m·(c_p·(T_liq − T₀) + h_f)/T₀; LPBF m·e_LPBF/T₀; primary metal m·e_Al/T₀; ratio of each R19 maximum to each comparator and to 1e3 and 1e5 J/K | m from R10; inputs of §3.1 | Melt floor ≈ 1.6e3 J/K; LPBF 0.9e5–9e5 J/K; primary ≈ 3.6e5 J/K | 1 % | C10 |
| R21 | Local entropy density at the hot spot against N | s = N·ψ·σ_w(N)²/(2·E_s·T₀·K_n²) | N as R14; both b | 4.29 MJ/(m³·K) at 1e7. Report the ratio to 4 MJ/(m³·K); interpretive, no pass or fail | 1 % | C13 |
| R22 | Factor on Σ̇ from amplitude-dependent ψ | κ(n_d)·(σ_rms/σ_ref)^(n_d−2); σ_rms at the R14 central amplitudes (A: 12.0 MPa, B: ≈ 16.8 MPa, C: 60 MPa); κ from R5 (1 for C [100]) | n_d ∈ {2, 2.3, 2.5, 3}; σ_ref ∈ {5, 20, 60} MPa | n_d = 2 gives 1 (identity). Expect a range of about 0.2–6 over the grid; report min and max | 1 % | C12 |
| R23 | Thermoelastic damping | D = k/(ρ_s·c_p); f_Z = π·D/(2·t²); Δ_E = E_s·α_s²·T₀/(ρ_s·c_p); ψ_TE = 2π·Δ_E·x/(1+x²), x = f/f_Z | t ∈ {0.2, 0.5, 1, 2, 5} mm; f ∈ {1/86 400, 1, 10, 100, 1000} Hz; k ∈ {100, 130, 170} W/(m·K) | Δ_E = 3.85e-3; max 1.21e-2. t = 0.5 mm: f_Z ≈ 340 Hz, ψ_TE(1 Hz) ≈ 7.1e-5. t = 2 mm: f_Z ≈ 21 Hz, ψ_TE(1 Hz) ≈ 1.1e-3. Report ψ_TE/5e-3 | 2 % | §0 dispute with Q1 claim 7 |
| R24 | One-at-a-time sensitivity of σ_a,max (N = 1e7) and of the R19 maximum (1 Hz, 20 years) | Recompute with each input at its range ends | σ_w7 40–100 MPa; σ_y 200–280 MPa; E_s 65–75 GPa; K_n 1–4; ψ 1e-3–1e-2; b −0.07 to −0.20; f 1.5–1.698 | S ∝ ψ·σ_w7²/(K_n²·E_s) is an identity; the b dependence is not. Report a table ranked by effect | — | C5, C9, C10 |
| R25 | Stress-ratio effects | σ_max = 2·σ_a/(1−R); limit on σ_a from collapse and first yield applied to σ_max; Goodman σ_ar = σ_a/(1 − σ_m,loc/σ_u) and Morrow with σ_f', for tensile mean only | R ∈ {−1, 0, 0.1}; compression–compression R = 10 reported without a mean-stress factor and flagged; σ_u = 400 MPa | R = 0.1, Goodman: allowable local amplitude 60/(1 + 1.222·60/400) = 50.7 MPa. R = −1 returns R14 (identity) | 1 % | C18, C24 |
| R26 | Life over-prediction of solid-constant macroscopic Basquin | log10[(K_n·k_peak)^(−1/b)] | ρ̄ sweep; K_n ∈ {1, 2}; b ∈ {−0.095, −0.1434}; A, B, C | ρ̄ = 0.2, K_n = 1: C 12.4 and 8.2 decades; A 18.4 and 12.2 decades; B about 22.3 and 14.8 decades | 0.05 decade | C20 |
| R27 | Predicted normalised endurance ratio | σ_w/(f·K_n·σ_y) for bending, σ_w/(K_n·σ_y) for stretch; also as σ_max/σ_y at R = 0.1 (× 2/(1−R), with and without Goodman) | AlSi10Mg: σ_w 40–100, σ_y 250 MPa. Ti-6Al-4V: σ_w 150–300, σ_y 950 MPa. K_n ∈ {1, 1.5, 2, 3} | K_n = 1, amplitude basis: AlSi10Mg 0.16 (bending), 0.24 (stretch); Ti-6Al-4V 0.14, 0.21. Compare with literature values only after S3 confirms them and their stress basis. ρ̄-independence is an identity | 1 % | C4, C22 |
| R28 | Mismatch strain and local amplitude | ε_m = abs(α_s − α_2)·ΔT; σ_a,loc = ½·K_n·c·E_s·ε_m/(1+S) with c ∈ {1; 1/(1−ν_s); BCC value from R7 at each ρ̄} | Partner list; ΔT list including the extension; K_n ∈ {1, 2, 3}; S from R29 | Ti partner, 50 K: ε_m = 6.2e-4; E_s·ε_m = 43.4 MPa; 21.7 MPa (K_n = c = 1); 65 MPa (K_n = 3). Flag cells with K_n·c·E_s·ε_m > σ_y as "not elastic" | 1 % | C17 |
| R29 | Stiffness ratio S and 1/(1+S) | S = M_L·H_L/(M_2·H_2); M_L: octet ρ̄E_s/6; BCC from R7; A as E_s·ρ̄²/(1−0.3); M_2 = E_2/(1−ν_2) | ρ̄ ∈ {0.1, 0.2, 0.4}; H_L/H_2 ∈ {0.1, 1, 10}; partner list | H_L = H_2: S between about 0.0005 (BCC, ρ̄ = 0.1, steel) and about 0.09 (A, ρ̄ = 0.4, Ti); 1/(1+S) ≥ 0.91. Octet, ρ̄ = 0.2, Ti: S ≈ 0.0135 | 2 % | C16 |
| R30 | Mismatch life and the ΔT at which N = 10 958 cycles | N = 1e7·(σ_ar/σ_w7)^(1/b); σ_ar = σ_a,loc from R28, optionally Goodman with σ_m = min(σ_y, E_s·Δα·ΔT_ref); bisection on ΔT in 1–500 K | b ∈ {−0.095, −0.1434}; K_n ∈ {1, 2, 3}; c ∈ {1, 1.49}; ΔT_ref ∈ {0, 100, 200, 300} K; partner list | Ti, c = 1, K_n = 3, no mean, b = −0.1434: N(50 K) ≈ 5.7e6; ΔT_x ≈ 122 K. K_n = 1: ΔT_x ≈ 367 K, outside the elastic range (flag). Expect ΔT_x > 50 K without mean stress and possibly < 50 K with σ_m = σ_y | 3 % | C17, C18 |
| R31 | Mismatch dissipation under strain control | ΔS = ψ·V·M_L·ε_a²/T₀, ε_a = ε_m/(2·(1+S)); total over 10 958 cycles; ratio between moduli | M_L as R29; Ti partner; ΔT ∈ {10, 50} K; ρ̄ = 0.2 | Octet, 50 K: 3.7e-6 J/K per cycle; 0.041 J/K in 30 years. Ratio A/octet = 6ρ̄/0.7 = 1.71 (A dissipates more), opposite in direction to R16's 1.8 | 2 % | C19 |
| R32 | Interlayer shear and thermal-lag magnitudes | γ/ε_m = L/(2·H_L); lag stress E_s·α_s·ΔT_lag; ratio to E_s·Δα·ΔT | L/H_L ∈ {1, 2, 4, 8, 16}; ΔT_lag ∈ {1, 5, 10} K; ΔT = 50 K; partners Ti and 316L | γ/ε_m > 2 for L/H_L > 4 (identity; magnitude table only). Lag 10 K: 14.7 MPa against 43.4 MPa (Ti) and 17.5 MPa (316L, Δα = 5.0e-6/K) | 1 % | Q5 "what would change it" |

## 4. Citations for S3

Status: all from memory. "sure" means I am confident the work exists with this title; the claimed content still needs checking. Equation and figure numbers are given only where I recall them and are UNSURE throughout.

**Lattice S–N data and normalisation**

1. Hrabe, Heinl, Flinn, Körner, Bordia (2011). "Compression-compression fatigue of selective electron beam melted cellular titanium (Ti-6Al-4V)". J. Biomed. Mater. Res. B 99B, 313–320. For: fatigue strength normalised by lattice yield, about 0.15–0.25 at 1e6 cycles. Existence sure; the ratio UNSURE.
2. Li, Murr, Cheng, Zhang, Hao, Yang, Medina, Wicker (2012). "Compression fatigue behavior of Ti–6Al–4V mesh arrays fabricated by electron beam melting". Acta Materialia 60, 793–802. For: fatigue strength against relative density (power law); ratcheting plus strut cracking. Sure; exponent UNSURE.
3. Amin Yavari, Wauthle, van der Stok, Riemslag, Janssen, Mulier, Kruth, Schrooten, Weinans, Zadpoor (2013). "Fatigue behavior of porous biomaterials manufactured using selective laser melting". Mater. Sci. Eng. C 33, 4849–4858. For: S–N curves of different porosities collapse onto one power law when normalised by yield stress. Sure; the normalised S–N figure number UNSURE.
4. Amin Yavari, Ahmadi, Wauthle, Pouran, Schrooten, Weinans, Zadpoor (2015). "Relationship between unit cell type and porosity and the fatigue behavior of selective laser melted meta-biomaterials". J. Mech. Behav. Biomed. Mater. 43, 91–100. For: collapse within a cell type, not across types. Sure.
5. Zargarian, Esfahanian, Kadkhodapour, Ziaei-Rad (2016). "Numerical simulation of the fatigue behavior of additive manufactured titanium porous lattice structures". Mater. Sci. Eng. C 60, 339–347. For: fatigue-strength coefficients as power laws of ρ̄; normalised S–N independent of ρ̄. Sure.
6. Zhao, Li, Hou, Hao, Yang, Misra (2016). "The influence of cell morphology on the compressive fatigue behavior of Ti-6Al-4V meshes fabricated by electron beam melting". J. Mech. Behav. Biomed. Mater. 59, 251–264. For: topology dependence; bending against buckling struts. Sure.
7. Van Hooreweder, Kruth (2017). "Advanced fatigue analysis of metal lattice structures produced by Selective Laser Melting". CIRP Annals 66(1), 221–224. For: local-stress method. Sure.
8. Van Hooreweder, Apers, Lietaert, Kruth (2017). "Improving the fatigue performance of porous metallic biomaterials produced by Selective Laser Melting". Acta Biomaterialia 47, 193–202. For: HIP and chemical etching; local stress. Sure.
9. Lietaert, Cutolo, Boey, Van Hooreweder (2018). "Fatigue life of additively manufactured Ti6Al4V scaffolds under tension-tension, tension-compression and compression-compression fatigue load". Scientific Reports 8, 4957. For: loading-mode dependence. Sure.
10. de Krijger, Rans, Van Hooreweder, Lietaert, Pouran, Zadpoor (2017). "Effects of applied stress ratio on the fatigue behavior of additively manufactured porous biomaterials under compressive loading". J. Mech. Behav. Biomed. Mater. 70, 7–16. For: R-ratio effect. Sure.
11. Ahmadi, Hedayati, Li, Lietaert, Tümer, Fatemi, Rans, Pouran, Weinans, Zadpoor (2018). "Fatigue performance of additively manufactured meta-biomaterials: The effects of topology and material type". Acta Biomaterialia 65, 292–304. For: normalised S–N across materials and topologies. Sure.
12. Bobbert, Lietaert, Eftekhari, Pouran, Ahmadi, Weinans, Zadpoor (2017). "Additively manufactured metallic porous biomaterials based on minimal surfaces: A unique combination of topological, mechanical, and mass transport properties". Acta Biomaterialia 53, 572–584. For: sheet-TPMS endurance up to about 60 % of yield. Sure; the 60 % UNSURE.
13. Benedetti, du Plessis, Ritchie, Dallago, Razavi, Berto (2021). "Architected cellular materials: A review on their mechanical properties towards fatigue-tolerant design and fabrication". Mater. Sci. Eng. R 144, 100606. For: review of normalisation practice and knock-downs. Sure.
14. Dallago, Fontanari, Torresani, Leoni, Pederzolli, Potrich, Benedetti (2018). "Fatigue and biological properties of Ti-6Al-4V ELI cellular structures with variously arranged cubic cells made by selective laser melting". J. Mech. Behav. Biomed. Mater. 78, 381–394. For: local stress on as-built geometry. Sure.
15. Dallago, Winiarski, Zanini, Carmignato, Benedetti (2019). "On the effect of geometrical imperfections and defects on the fatigue strength of cellular lattice structures additively manufactured via Selective Laser Melting". Int. J. Fatigue 124, 348–360. For: geometric imperfection as the notch source. Sure.
16. Hedayati, Hosseini-Toudeshky, Sadighi, Mohammadi-Aghdam, Zadpoor (2016). "Computational prediction of the fatigue behavior of additively manufactured porous metallic biomaterials". Int. J. Fatigue 84, 67–79. For: beam-model S–N prediction. Sure.
17. Burr, Persenot, Doutre, Buffiere, Lhuissier, Martin, Dendievel (2020). "A numerical framework to predict the fatigue life of lattice structures built by additive manufacturing". Int. J. Fatigue 139, 105769. For: local approach with as-built strut data. Existence fairly sure; details UNSURE.
18. Zadpoor (2019). "Mechanical performance of additively manufactured meta-biomaterials". Acta Biomaterialia 85, 41–59. For: review. Sure.
19. Boniotti, Beretta, Patriarca, Rigoni, Foletti (2019). "Experimental and numerical investigation on compressive fatigue strength of lattice structures of AlSi7Mg manufactured by SLM". Int. J. Fatigue 128, 105181. For: an aluminium-alloy lattice S–N dataset. UNSURE (authors, article number).
20. A fatigue dataset for AlSi10Mg lattices specifically: I cannot name one with confidence. UNSURE; S3 to search.

**As-built surface, porosity, knock-down (bulk and thin struts)**

21. Brandl, Heckenberger, Holzinger, Buchbinder (2012). "Additive manufactured AlSi10Mg samples using Selective Laser Melting (SLM): Microstructure, high cycle fatigue, and fracture behavior". Materials & Design 34, 159–169. For: S–N of LPBF AlSi10Mg. Sure.
22. Aboulkhair, Maskery, Tuck, Ashcroft, Everitt (2016). "Improving the fatigue behaviour of a selectively laser melted aluminium alloy: Influence of heat treatment and surface quality". Materials & Design 104, 174–182. For: as-built against machined; heat treatment. Sure.
23. Mower, Long (2016). "Mechanical behavior of additive manufactured, powder-bed laser-fused materials". Mater. Sci. Eng. A 651, 198–213. For: as-built AlSi10Mg fatigue strength against wrought. Sure.
24. Romano, Brückner-Foit, Brandão, Gumpinger, Ghidini, Beretta (2018). "Fatigue properties of AlSi10Mg obtained by additive manufacturing: Defect-based modelling and prediction of fatigue strength". Eng. Fract. Mech. 187, 165–189. For: defect-based prediction. Sure.
25. Beretta, Romano (2017). "A comparison of fatigue strength sensitivity to defects for materials manufactured by AM or traditional processes". Int. J. Fatigue 94, 178–191. Sure.
26. Uzan, Shneck, Yeheskel, Frage (2017). "Fatigue of AlSi10Mg specimens fabricated by additive manufacturing selective laser melting (AM-SLM)". Mater. Sci. Eng. A 704, 229–237. For: fatigue limit values. Fairly sure.
27. Tang, Pistorius (2017). "Oxides, porosity and fatigue performance of AlSi10Mg parts produced by selective laser melting". Int. J. Fatigue 94, 192–201. Sure.
28. Yadollahi, Shamsaei (2017). "Additive manufacturing of fatigue resistant materials: Challenges and opportunities". Int. J. Fatigue 98, 14–31. For: review of surface and defect effects. Sure.
29. Pegues, Roach, Williamson, Shamsaei (2018). "Surface roughness effects on the fatigue strength of additively manufactured Ti-6Al-4V". Int. J. Fatigue 116, 543–552. Sure.
30. Persenot, Burr, Martin, Buffiere, Dendievel, Maire (2019). "Effect of build orientation on the fatigue properties of as-built Electron Beam Melted Ti-6Al-4V alloy". Int. J. Fatigue 118, 65–76. For: thin as-built struts. Fairly sure.
31. Murakami (2002). "Metal Fatigue: Effects of Small Defects and Nonmetallic Inclusions". Elsevier. For: the √area model.
32. Arola, Williams (2002). "Estimating the fatigue stress concentration factor of machined surfaces". Int. J. Fatigue 24, 923–930. For: K_t from roughness parameters. Sure.
33. Kempen, Thijs, Van Humbeeck, Kruth (2012). "Mechanical properties of AlSi10Mg produced by Selective Laser Melting". Physics Procedia 39, 439–446. For: E_s, σ_y, σ_u of as-built AlSi10Mg. Sure.
34. EOS GmbH, material data sheet "EOS Aluminium AlSi10Mg". For: E_s, σ_y, σ_u and a fatigue strength of about 97 MPa. Year and test conditions UNSURE.
35. NASA-STD-6030 (2021), "Additive Manufacturing Requirements for Spaceflight Systems". For: whether any standard prescribes a lattice knock-down (I believe none does). UNSURE.
36. ISO 13314:2011, "Mechanical testing of metals — Ductility testing — Compression test for porous and cellular metals". For: the static normalising test (plateau and yield stress). Sure.

**Basquin and mean stress**

37. Basquin (1910). "The exponential law of endurance tests". Proc. ASTM 10, 625–630. Sure.
38. Bäumel, Seeger (1990). "Materials Data for Cyclic Loading, Supplement 1". Elsevier. For: uniform material law, σ_f' = 1.67·σ_u and b = −0.095 for aluminium and titanium alloys. Existence sure; constants UNSURE.
39. Dowling, "Mechanical Behavior of Materials" (4th ed., 2013). Pearson. For: Basquin, Goodman, Morrow, notch factor. Chapter numbers UNSURE.

**Gibson–Ashby, octet, BCC, TPMS stiffness and strength**

40. Gibson, Ashby (1997). "Cellular Solids: Structure and Properties", 2nd ed., Cambridge University Press. For: E*/E_s ≈ ρ̄², σ_pl/σ_ys ≈ 0.3·ρ̄^1.5, σ_el ≈ 0.05·E_s·ρ̄² for open cells (chapter 5; equation numbers UNSURE).
41. Ashby (2006). "The properties of foams and lattices". Phil. Trans. R. Soc. A 364, 15–30. For: bending against stretch scaling; stretch-dominated E ≈ ρ̄·E_s/3 as an ideal. Sure.
42. Deshpande, Fleck, Ashby (2001). "Effective properties of the octet-truss lattice material". J. Mech. Phys. Solids 49, 1747–1769. For: E_33 = ρ̄E_s/9, G = ρ̄E_s/12, yield ρ̄σ_y/3, strut buckling. Sure; equation numbers UNSURE.
43. Deshpande, Ashby, Fleck (2001). "Foam topology: bending versus stretching dominated architectures". Acta Materialia 49, 1035–1040. Sure.
44. Ushijima, Cantwell, Mines, Tsopanos, Smith (2011). "An investigation into the compressive properties of stainless steel micro-lattice structures". J. Sandwich Struct. Mater. 13, 303–329. For: BCC closed forms, E* = (√3·π/2)·E_s·(d/L)⁴ and σ_pl = (4√2/3)·σ_y·(d/L)³. Existence fairly sure; that the paper states exactly these forms is UNSURE.
45. Gümrük, Mines (2013). "Compressive behaviour of stainless steel micro-lattice structures". Int. J. Mech. Sci. 68, 125–139. For: BCC with node effects. Fairly sure.
46. Leary, Mazur, Elambasseril, McMillan, Chirent, Sun, Qian, Easton, Brandt (2016). "Selective laser melting (SLM) of AlSi12Mg lattice structures". Materials & Design 98, 344–357. For: measured moduli of Al-alloy strut lattices against C1. Fairly sure.
47. Maskery, Aboulkhair, Aremu, Tuck, Ashcroft, Wildman, Hague (2016). "A mechanical property evaluation of graded density Al-Si10-Mg lattice structures manufactured by selective laser melting". Mater. Sci. Eng. A 670, 264–274. For: AlSi10Mg BCC static properties. Sure.
48. Al-Ketan, Rowshan, Abu Al-Rub (2018). "Topology-mechanical property relationship of 3D printed strut, skeletal, and sheet based periodic metallic cellular materials". Additive Manufacturing 19, 167–183. For: gyroid sheet against skeletal scaling exponents. Sure; exponents UNSURE.
49. Yan, Hao, Hussein, Young, Huang, Zhu (2015). "Microstructure and mechanical properties of aluminium alloy cellular lattice structures manufactured by direct metal laser sintering". Mater. Sci. Eng. A 628, 238–246. For: AlSi10Mg gyroid static data. Fairly sure.

**Bimaterial thermal mismatch**

50. Timoshenko (1925). "Analysis of bi-metal thermostats". J. Opt. Soc. Am. 11, 233–255. For: bimetal strip stresses (the 1/8 + 3/8 split). Sure.
51. Stoney (1909). "The tension of metallic films deposited by electrolysis". Proc. R. Soc. A 82, 172–175. For: thin-layer limit. Sure.
52. Suhir (1986). "Stresses in bi-metal thermostats". J. Appl. Mech. 53, 657–660. For: interfacial shear and peel edge zones. Sure.
53. Freund, Suresh (2003). "Thin Film Materials: Stress, Defect Formation and Surface Evolution". Cambridge University Press. For: biaxial modulus E/(1−ν), layer on substrate, edge zone length. Sure.
54. Bogy (1971). "Two edge-bonded elastic wedges of different materials and wedge angles under surface tractions". J. Appl. Mech. 38, 377–386. For: free-edge singularity. Sure.
55. Hutchinson, Suo (1992). "Mixed mode cracking in layered materials". Adv. Appl. Mech. 29, 63–191. For: debond driving force scaling with the compliant layer's modulus. Sure.

**Damping and dissipation**

56. Lazan (1968). "Damping of Materials and Members in Structural Mechanics". Pergamon. For: D = J·σ^n, exponents, aluminium-alloy data. Sure; values UNSURE.
57. Zhang, Perez, Lavernia (1993). "Documentation of damping capacity of metallic, ceramic and metal-matrix composite materials". J. Mater. Sci. 28, 2395–2404. For: loss factors of Al alloys (order 1e-4 to 1e-2). Sure; values UNSURE.
58. Zener (1937). "Internal friction in solids. I. Theory of internal friction in reeds". Phys. Rev. 52, 230–235; and (1938) part II, Phys. Rev. 53, 90–99. For: thermoelastic damping, f_Z and Δ_E. Sure.
59. Nowick, Berry (1972). "Anelastic Relaxation in Crystalline Solids". Academic Press. For: thermoelastic relaxation strength. Sure.
60. Naderi, Amiri, Khonsari (2010). "On the thermodynamic entropy of fatigue fracture". Proc. R. Soc. A 466, 423–438. For: fatigue fracture entropy, about 4 MJ/(m³·K) for Al 6061-T6. Existence sure; value UNSURE.
61. Rosa, Manzoni, Casati (2018). "Damping behavior of 316L lattice structures produced by Selective Laser Melting". Materials & Design 160, 1010–1018. For: a measured lattice loss factor against solid (not aluminium). Fairly sure.
62. Damping capacity of LPBF AlSi10Mg (solid or lattice): I cannot name a source. UNSURE; S3 to search. Without it ψ = 5e-3 rests on general Al-alloy data only.

**Manufacturing energy comparators**

63. Gutowski, Branham, Dahmus, Jones, Thiriez, Sekulic (2009). "Thermodynamic analysis of resources used in manufacturing processes". Environ. Sci. Technol. 43, 1584–1590. For: exergy intensity of manufacturing processes. Sure.
64. Faludi, Baumers, Maskery, Hague (2017). "Environmental impacts of selective laser melting: do printer, powder, or power dominate?". J. Ind. Ecol. 21(S1), S144–S156. For: LPBF energy per kg of aluminium part. Fairly sure; values UNSURE.
65. Kellens, Mertens, Paraskevas, Dewulf, Duflou (2017). "Environmental impact of additive manufacturing processes: does AM contribute to a more sustainable way of part manufacturing?". Procedia CIRP 61, 582–587. For: specific energy ranges. UNSURE (title and venue).

## 5. Q5: candidate defaults

**Dissipation.** Candidate: the macroscopic form with a topology-specific modulus, Σ̇ = ν·ψ·V_env·σ_a²/(2·E_eff·T₀), E_eff measured or C1·E_s·ρ̄^n from a table (octet [100]: 1/9, n = 1; BCC: about 0.09 slender, n = 2; E_s·ρ̄² only for foams), with ψ taken at σ_rms = σ_a·sqrt(E_s/(ρ̄·E_eff)). Companion bound for screening, with no modulus: Σ̇ ≤ ν·ψ·ρ̄·V_env·σ_w(N)²/(2·E_s·T₀·K_n²·r²). Under strain control (mismatch) use ψ·V·M_L·ε_a² instead.
- Assumptions: linear elastic, constant ψ, fully reversed, isothermal at T₀.
- Validity: σ_max below first yield; ρ̄ ≤ 0.3 for beam constants; frequency well below f_Z.
- Anchor: a measured lattice loss factor against a solid coupon of the same build (citation 61 is the nearest; none known for AlSi10Mg).
- Would change it: R22 showing a factor above 2 for plausible n_d (then add κ and a stated σ_ref); S3 finding ψ of AlSi10Mg well away from 5e-3; R6 or FE showing E_eff constants off by more than 2; evidence of friction damping from trapped powder.

**Mismatch stress.** Candidate: two outputs. Strut amplitude for fatigue: σ_a,loc = ½·K_n·c·E_s·abs(α_s − α_2)·ΔT/(1+S), with c = 1 for stretch-dominated cells, c = C_b·ρ̄^0.5 + axial term for bending cells from a unit-cell analysis (BCC equibiaxial: 2.10·ρ̄^0.5 + 0.37·ρ̄), c = 1/(1−ν_s) for bonded roots, core–shell struts and sheet TPMS. Macroscopic stress for the interface and the partner: σ̄ = M_L·ε_m/(1+S) with M_L = E_eff/(1−ν_L).
- Assumptions: uniform temperature, one mismatched interface, elastic, bonded.
- Validity: K_n·c·E_s·ε_m < σ_y; S ≤ 0.2; L/H_L below about 4 for an interlayer.
- Anchor: thermal-cycling test or FE of a co-printed lattice on a dissimilar substrate with strain measurement in the first cell row; none known to me (UNSURE).
- Would change it: R7 or FE showing c above 1 for bending cells in the working ρ̄ range (then c = 1 is not a safe screen); R30 showing mean stress from cool-down controls life (then σ_m enters the default); R32 showing lag or interlayer shear above the Δα term for the intended geometry.

**Life.** Candidate: local-stress Basquin with a cap. N_f = 1e7·(K_n·k_peak(topology, ρ̄)·σ_a/σ_w7)^(1/b), with σ_w7 and b from as-built thin-strut data of the same alloy and process, and τ_wearout = min(N_f/ν, τ_service). Equivalent lattice-level statement where test data exist: σ_a/σ_y,lattice = A·(2N)^b fitted per topology and process.
- Assumptions: constant amplitude, crack initiation at the strut surface, R = −1 or a stated mean-stress rule.
- Validity: 1e3 < N < 1e7 (extrapolation beyond is unverified); tension or bending of struts, not compression ratcheting; first yield not exceeded.
- Anchor: normalised S–N sets in citations 3, 4 and 11 (Ti-6Al-4V); an AlSi10Mg lattice set is needed (citations 19, 20).
- Would change it: R27 with S3-verified ratios off by more than 3 (then prefer the empirical lattice-level form); S3 finding as-built AlSi10Mg σ_w7 or b outside the sweep; evidence that K_n depends on ρ̄ through strut size.

## 6. Points I could not plan

- **Gyroid.** The prompt names gyroid first. I have no closed form for its C1, n, k_peak or r, for sheet or skeletal type. Topologies A, B, C bracket it only loosely. Needs FE or verified literature constants (citation 48).
- **Unit-cell FE.** Every falsifier in the Q1 and Q2 answers is an FE run. numpy-only rows R6, R7, R9 test the beam algebra on one cell (BCC), not node volume, fillets, roughness or boundary layers.
- **Singular strut roots and corner cells** (Q2 claims 3 and 8). No computation here; a point stress is not defined there.
- **K_n.** No derivation and no source I trust; it is swept, not estimated.
- **ψ for LPBF AlSi10Mg and its amplitude dependence.** No source (citation 62).
- **What counts as the manufacturing comparator.** The prompt's 1e3–1e5 J/K is unverified and may be low by one to two orders; C10 depends on it.
- **Whether all hysteretic entropy should count** (anelastic and thermoelastic parts against the plastic part). Open in Q1; not resolved here. C13 only frames it.
