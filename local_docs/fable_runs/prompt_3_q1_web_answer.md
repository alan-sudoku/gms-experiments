# Prompt 3, question 1: dissipation forms (low-budget run)

Context file (`local_docs/`, never cited by the spec). Run 2026-11-13 per `local_docs/orchestration/fable_delegation_plan.md` §5.1, as a Fable agent (`fable`, effort high, no tools) instead of the web chat; input was the §5.1 Q1 block verbatim. The reply below is saved as returned. Every claim is at level `derived`; S1 receives it as input and S5 reviews it.

---

All claims are level `derived`: reasoning only, no tools, nothing checked numerically. Symbols: C and n are defined by E_eff = C·E_s·ρ̄^n; ⟨·⟩ is the average over strut volume.

1. **(1a) The two forms are identical if and only if the strut stress is the energy-equivalent (RMS) stress.**
 - Equation: V_env·σ_a²/(2·E_eff) = ∫_struts σ_loc²/(2·E_s) dV = ρ̄·V_env·σ_rms²/(2·E_s) [J], so σ_rms = σ_a·sqrt(E_s/(ρ̄·E_eff)) [Pa].
 - This is work–energy equality (Clapeyron / Hill–Mandel) for a linear-elastic periodic cell, with E_eff the actual modulus in the load direction; no Gibson–Ashby assumption is needed.
 - For stubby struts, define σ_rms² = 2·E_s·⟨u⟩ so that shear energy is included.
 - Confidence: high.
 - Falsifier: unit-cell FE with periodic boundary conditions, where ∫u dV differs from V_env·σ_a²/(2·E_eff) beyond mesh error.

2. **(1d) Verdict: default to the macroscopic form with measured or FE E_eff, and evaluate ψ at σ_rms, not at σ_a.** The forms disagree by more than 2 only when the strut stress is not σ_rms or E_eff is wrong:
 - Area-average stress σ_a/ρ̄: macro/strut = 1/(C·ρ̄^(n−1)), which is 2.5–10 for bending (C≈1) and 9 for octet [100]. This exceeds 2 over the whole range ρ̄ = 0.1–0.4.
 - Peak surface stress: the strut form overestimates by (σ_peak/σ_rms)² ≈ 9–25 in bending.
 - E_eff = E_s·ρ̄² applied to a stretch-dominated lattice: see claim 8.
 - Stress-dependent ψ with damping exponent n_d ≳ 3.3: see claim 6.
 - Confidence: high for the first two, medium for the last two.
 - Falsifier: the same FE as claim 1, comparing each stress definition.

3. **(1b) RMS strut stress scales as ρ̄^(−(n+1)/2).**
 - Equation: σ_rms = σ_a·C^(−1/2)·ρ̄^(−(n+1)/2) [Pa].
 - Bending (n=2, C≈1; Gibson–Ashby open cell, constant UNSURE): σ_rms ≈ σ_a·ρ̄^(−3/2), which is about 32·σ_a at ρ̄=0.1 and 4·σ_a at ρ̄=0.4.
 - Stretch (n=1): σ_rms = σ_a/(sqrt(C)·ρ̄).
 - Octet along [100], pin-jointed affine model, derived here: C_ijkl = ρ̄·E_s·⟨n_i n_j n_k n_l⟩ gives E_100 = ρ̄·E_s/9 and ν = 1/3. Every strut family then has |ε| = ε_macro/3, so |σ_strut| = 3·σ_a/ρ̄ in all struts and RMS equals nominal peak.
 - Confidence: high for exponents, medium for constants. The slender-beam assumption degrades at ρ̄ ≳ 0.3.
 - Falsifier: FE strut-stress histogram at ρ̄ = 0.1 and 0.2; a log-log slope different from −1.5 (bending) or −1 (stretch).

4. **(1b) Peak surface stress has the same ρ̄ exponent as RMS in bending, but a larger constant; dissipation uses RMS and fatigue uses peak.**
 - Equation: σ_peak = C_σ·σ_a·ρ̄^(−3/2) [Pa], from M ~ σ_a·l³ and σ = 6M/t³.
 - Ideal beam with linear moment: ⟨σ²⟩/σ_peak² = (1/3)·(1/3) for a rectangular section and (1/4)·(1/3) for a circular one. So σ_peak/σ_rms = 3 (rectangular) or 2√3 ≈ 3.5 (circular).
 - C_σ ≈ 5 if back-derived from the Gibson–Ashby collapse constant σ_pl ≈ 0.3·σ_y·ρ̄^(3/2) with a 2/3 shape factor (UNSURE).
 - Stretch: σ_peak ≈ σ_rms × nodal K_t.
 - Dissipation takes the second moment σ_rms (for constant ψ). Fatigue life takes σ_peak × K_t (node fillet, as-built roughness), amplified by the Basquin exponent.
 - Confidence: medium.
 - Falsifier: FE ratio of maximum surface stress to RMS outside 2.5–6 for a slender bending cell.

5. **(1c) With amplitude-independent ψ, neither form is "more correct" and no bending correction is needed.**
 - Equation: ΔU = ∫ψ·u dV = ψ·U_total, so ψ_lattice = ψ_solid [–].
 - Non-uniform stress through the section does not matter, and a uniaxial or bending coupon ψ transfers directly into the macroscopic form.
 - Confidence: high, given the premise.
 - Falsifier: the measured lattice loss factor (ψ/2π) differs from the solid coupon value at matched microstructure in the amplitude-independent regime.

6. **(1c) With stress-dependent ψ, a correction factor κ is needed and ψ must be evaluated at strut stress.**
 - Assume a power law for damping energy, D = J·σ^n_d [J/m³ per cycle] (Lazan-type; exponent range UNSURE, about 2–3 at low stress and higher near the fatigue limit). Then ψ_u(σ) = 2·E_s·J·σ^(n_d−2).
 - Equation: Σ̇ = ν·V_env·κ·ψ_u(σ_rms)·σ_a²/(2·E_eff·T₀) [W/K], with κ = ⟨|σ|^n_d⟩/σ_rms^n_d.
 - Rectangular section with linear moment: κ = 3^n_d/(n_d+1)², which is 1, 1.69 and 3.24 for n_d = 2, 3 and 4. It exceeds 2 for n_d ≳ 3.3. For ideal stretch, κ = 1.
 - Evaluating ψ at σ_a instead of σ_rms is wrong by (σ_rms/σ_a)^(n_d−2), about 4–32 for n_d = 3 in bending.
 - Coupon caveat: a bending-coupon ψ quoted at its surface stress equals 3/(n_d+1) times the uniaxial ψ at that stress (rectangular section, uniform moment). Convert before use.
 - Confidence: medium.
 - Falsifier: lattice hysteresis measured against amplitude; a log-log slope of ΔU against σ_a equal to 2 means κ = 1 and this claim is moot.

7. **(1c) Bending struts add thermoelastic (Zener) damping that a uniaxial coupon does not see and a thick bending coupon sees at the wrong frequency.**
 - Equations (prefactors UNSURE): f_Z ≈ π·a/(2·t²) [Hz], with a the thermal diffusivity [m²/s] and t the strut thickness [m]; ψ_TE,max ≈ π·E_s·α²·T₀/(ρ·c_p) [–].
 - Estimates from memory-quality property values, t = 0.5 mm: Ti-6Al-4V f_Z ≈ 18 Hz and ψ_TE ≈ 3e-3; AlSi10Mg f_Z ≈ 380 Hz and ψ_TE ≈ 1.4e-2.
 - That is the same order as the assumed ψ range, and it depends on size and frequency, so it is not a transferable material constant. It is about zero for stretch-dominated cells.
 - Confidence: medium-low.
 - Falsifier: a frequency sweep of lattice loss factor across f_Z showing no Debye-type peak.

8. **(Adversarial) E_eff ≈ E_s·ρ̄² is the wrong default for octet and uncertain for gyroid.**
 - Octet is stretch-dominated: model/true E_eff = 9·ρ̄ along [100]. At fixed σ_a the macroscopic form underestimates Σ̇ by 9·ρ̄, which exceeds 2 for ρ̄ > 0.22.
 - Gyroid: the strut (skeletal) type is closer to n ≈ 2 and the sheet type has a lower n (UNSURE).
 - Use measured E_eff. Adhered powder also inflates weighed ρ̄ relative to load-bearing ρ̄.
 - Confidence: medium.
 - Falsifier: measured E_eff/E_s against ρ̄ for octet showing slope 2.

**Open points**
- The constants C, C_σ and κ for real gyroid and octet geometry (node volume, fillets, anisotropy, ρ̄ > 0.3) need unit-cell FE; only the exponents are argued here.
- The form and exponent of ψ(σ) for as-built AM material (porosity, roughness, particle friction) are unknown; wrought coupon ψ may not transfer.
- Not settled: whether all hysteretic entropy (including the thermoelastic and anelastic parts) should count toward a damage-related Σ̇, or only the plastic fraction.
