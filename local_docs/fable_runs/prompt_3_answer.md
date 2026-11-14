# Prompt 3 answer (stage S4, finaliser): lattice fatigue micromechanics

Context file (`local_docs/`, never cited by the spec). Written 2026-11-14. Question: `local_docs/fable_questions.md`, section "Prompt 3". Earlier answers to Q1 and Q2: `prompt_3_q1_web_answer.md`, `prompt_3_q2_web_answer.md`. Plan: `prompt_3_plan.md` (S1). Computations: `prompt_3_code/` (S2, plus two `s4_*` scripts added here). Citation check: `prompt_3_citations.md` (S3, two passes, snippets and abstracts only).

**Status of everything here: claim at level `derived` (unverified).** No measurement was made and no finite-element run exists. Every material constant is a memory or snippet value. Agreement between stages is not evidence.

## 0. How to read this file

Every number carries a tag for the output that produces it. Outputs are in `prompt_3_code/outputs/`; the script has the same name with `.py` in `prompt_3_code/`. "R6" is a row of the plan's computation spec; "§3" is a section of an S4 output.

| Tag | Output file | Stage | Content |
|---|---|---|---|
| [U] | `p3_unit_cells.txt` | S2 | R1–R9: octet and BCC cell models, beam integrals |
| [L] | `p3_q4_limits.txt` | S2 | R10–R15: collapse, first yield, fatigue limits |
| [E] | `p3_q4_entropy.txt` | S2 | R16–R21: dissipation, life totals, comparators |
| [S] | `p3_sensitivity.txt` | S2 | R22–R25: damping exponent, thermoelastic, sensitivity, stress ratio |
| [N] | `p3_q3_normalisation.txt` | S2 | R26–R27: life over-prediction, endurance ratio |
| [M] | `p3_mismatch.txt` | S2 | R28–R32: mismatch stress, life, dissipation |
| [4Q] | `s4_q4_rerun.txt` | S4 | Q4 re-run with σ_w7 = 30 MPa, σ_u = 460 MPa, LPBF to 600 MJ/kg, closed-form N_x, damping conventions |
| [4M] | `s4_mismatch_rerun.txt` | S4 | mismatch re-run with α_s to 27e-6 /K and σ_w7 = 30 MPa, bilayer bending, closed-form ΔT_x |

Both S4 scripts print regression lines against S2 values; all agree ([4Q] §0, §5; [4M] §1, §2, §5).

Notation. ρ̄ relative density; E_s, σ_y, σ_u solid modulus, yield, ultimate; σ_a macroscopic stress amplitude; E_eff lattice modulus in the load direction; k_peak = (peak nominal strut stress)/σ_a; σ_rms energy-equivalent strut stress; r = σ_peak/σ_rms; σ_w7 fatigue strength amplitude of the strut material at 1e7 cycles, R = −1; b Basquin exponent; K_n notch factor of node and strut irregularity not already contained in σ_w7; ε_m = abs(α_s − α_2)·ΔT; S = M_L·H_L/(M_2·H_2) with M = E/(1−ν); c = (peak nominal strut stress)/(E_s·ε_m). Cells: A = Gibson–Ashby open-cell foam constants (no geometry); B = BCC strut lattice, beam model; C = octet truss, pin-jointed model, loaded along [100] or [110]. Central inputs unless stated: AlSi10Mg, E_s = 70 GPa, σ_y = 250 MPa, ρ̄ = 0.2, V_env = 1e-3 m³, ψ = 5e-3, T₀ = 300 K.

Two input changes run through the whole file (S3 findings, section 3 of this file):

- **σ_w7 (as-built) is 30 to 60 MPa, not 60.** No source gives 60 MPa. One record (Aboulkhair 2016) puts the amplitude at or below about 31.5 MPa if its stress range is at R = 0.1 ([4Q] §1; basis UNSURE). Every result is given for both ends.
- **α_s is 21e-6 to 27e-6 /K.** A snippet reports 26.6e-6 /K for the build direction as built (UNSURE). Mismatch results are given for 21, 23 and 27e-6 /K.

## 1. Verdicts in brief

- **Q4, materiality.** Fatigue dissipation is immaterial for diurnal loading in every case (at most 7.4 J/K in 30 years against 1.5e3 J/K for the smallest comparator). At 1 Hz it stays below 1 % of realistic process plus primary-metal terms for bending-dominated cells. It reaches 4 to 38 % of the smallest LPBF figure only for a stretch-dominated cell run continuously near its fatigue limit for 1e8 to 1e9 cycles. Otherwise fatigue matters through τ_wearout only (claim 1).
- **Q5 defaults.** Dissipation: macroscopic form with the cell's own modulus (claim 2). Life: local-stress Basquin with a service cap (claim 3). Mismatch: ½·K_n·c·E_s·Δα·ΔT/(1+S) (claim 4).
- **Q1 and Q2.** The earlier answers stand in structure. Five constants are revised (section 4).
- **Q3.** Basquin with macroscopic stress and solid constants over-predicts life by 8 to 22 decades. No standard knock-down exists (claims 23 to 28).

## 2. Claims

Each claim: statement; equations in plain text with units; numbers with tags; confidence; falsifier; status against the plan.

### 2.1 Headline claims (Q4 verdict, Q5 defaults)

**1. Fatigue dissipation is material only in one corner: a stretch-dominated lattice cycled at about 1 Hz near its fatigue limit for decades. In all other cases fatigue enters through τ_wearout only.**

- Diurnal (1 per day), any cell, 10 to 30 years: 3.5e-3 to 7.4 J/K ([4Q] §5). The 6.63 J/K case is 0.41 % of the melt floor and 7.5e-5 of LPBF at 50 MJ/kg ([4Q] §6). Mismatch-driven dissipation is at most 0.29 J/K in 30 years ([4M] §5).
- 1 Hz, bending-dominated (A, B), 10 to 30 years: 18 to 2.97e3 J/K ([4Q] §5). The largest is 1.8 times the melt floor, 3.0 times the low end of the prompt's range, 3.3 % of LPBF at 50 MJ/kg and 0.67 % of LPBF at 50 MJ/kg plus primary aluminium at 200 MJ/kg ([4Q] §6).
- 1 Hz, stretch-dominated (C), 10 to 30 years: 74 to 3.42e4 J/K ([4Q] §5). The largest (σ_w7 = 60 MPa, b = −0.095, K_n = 1, 30 years, strut amplitude 39 MPa) is 21 times the melt floor, 34 % of the high end of the prompt's range, 38 % of LPBF at 50 MJ/kg, 3.2 % of LPBF at 600 MJ/kg, 9.6 % of primary aluminium and 7.7 % of the two together ([4Q] §6). With σ_w7 = 30 MPa and its anchored b = −0.1929 the same case gives 3.5e3 J/K (3.9 % of LPBF at 50 MJ/kg); with K_n = 2 as well, 8.8e2 J/K.
- Comparators for the 0.534 kg part: melt-and-reject floor 1.46e3 to 1.65e3 J/K (c_p 739 to 922 J/(kg·K)); LPBF electricity 8.9e4 to 1.07e6 J/K (50 to 600 MJ/kg); primary aluminium 2.7e5 to 4.6e5 J/K (150 to 260 MJ/kg) ([4Q] §6). The prompt's 1e3 to 1e5 J/K sits at and below the low end of these.
- These are upper bounds: the part is assumed to be loaded at the amplitude that fails exactly at the end of service. A design factor of 0.6 on stress multiplies them by 0.36 ([4Q] §5).
- Confidence: medium for diurnal and bending-dominated; medium-low for the stretch corner (depends on ψ at 30 to 60 MPa strut amplitude and on Basquin beyond 1e7 cycles).
- Falsifier: a measured ψ of LPBF AlSi10Mg at 30 to 60 MPa of 1.3e-2 or more (2.6 times the assumed value; 1/0.384 from [4Q] §6) puts the 1 Hz stretch corner above LPBF at 50 MJ/kg. The diurnal verdict would need ψ about 245 times larger (ratio 4.08e-3 against the melt floor, [4Q] §6), which exceeds 1 and is not possible for an elastic part.
- Status: plan C10 kept in substance; ranges widened (σ_w7 to 30 MPa, LPBF to 600 MJ/kg, 30-year cap).

**2. Default dissipation form: macroscopic, with the modulus of the actual cell and load direction.**

- Σ̇ = ν·ψ·V_env·σ_a²/(2·E_eff·T₀) [W/K], with ν [Hz], V_env [m³], σ_a [Pa], E_eff [Pa], T₀ [K], ψ [-].
- ψ is ΔU/U per cycle as the prompt defines it. For small damping ψ = 2π·η = 4π·ζ (η loss factor, ζ damping ratio). A literature value must be converted before use ([4Q] §7).
- ψ is to be evaluated at the strut stress σ_rms = σ_a·sqrt(E_s/(ρ̄·E_eff)) [Pa], not at σ_a.
- E_eff: measured in the load direction where possible. Otherwise: octet ρ̄·E_s/9 along [100], ρ̄·E_s/6 along [110], ρ̄·E_s/5 along [111] ([U] R1); BCC along [001] 0.090·E_s·ρ̄² (Euler–Bernoulli) or 0.082·E_s·ρ̄² (Timoshenko) at ρ̄ = 0.2 ([U] R6); E_s·ρ̄² for foams only.
- Under strain control (thermal mismatch, equibiaxial): ΔS per cycle = ψ·V_env·M_L·ε_a²/T₀ [J/K], ε_a = ε_m/(2·(1+S)).
- Screening bound with no modulus: S_life ≤ N·ψ·ρ̄·V_env·σ_w(N)²/(2·E_s·T₀·K_n²·r²) [J/K].
- Assumptions: linear elastic, ψ independent of amplitude, isothermal at T₀.
- Validity: peak strut stress below σ_y; ρ̄ ≤ 0.3 for the beam constants; frequency well below the Zener frequency of the strut for bending cells (claim 11).
- Anchor: none exists for AlSi10Mg. Needed test: hysteresis loop or free decay of a lattice and a solid coupon from the same build, at strut amplitudes of 10 to 60 MPa and 0.1 to 10 Hz. Nearest published work: Rosa 2018 (316L lattices damp more than bulk; no values seen).
- Confidence: high for the form (it is an energy identity, claim 14); low for any value of ψ.
- Falsifier: lattice loss factor differing from the solid coupon's by more than 2 at matched strut stress and frequency.
- Status: plan Q5 candidate kept; the ψ convention is added.

**3. Default life form: local-stress Basquin with a service cap.**

- N_f = 1e7·(K_n·k_peak·σ_a/σ_w7)^(1/b) [cycles]; τ_wearout = min(N_f/ν, τ_service) [s].
- k_peak from the lattice's own measured strength where it exists: k_peak = f·σ_y/σ_pl,lattice for bending cells (f = 1.5 rectangular, 1.70 circular section), σ_y/σ_pl,lattice for stretch cells. Then the form is the yield-normalised S–N law of the lattice literature: σ_a/σ_pl,lattice = [σ_w7/(f·K_n·σ_y)]·(N/1e7)^b. For BCC this drops the axial term (11.43 against 11.88 in the constant at ρ̄ = 0.2, [U] R6).
- k_peak without test data, at ρ̄ = 0.2: 55.9 (A, f = 1.5), 132.8 (B), 15 (C [100]), 30 (C [110]) ([L] R13). Scaling: 5.0·ρ̄^(−1.5) (A), 11.43·ρ̄^(−1.5) + 1/ρ̄ (B), 3/ρ̄ and 6/ρ̄ (C).
- Parameters for as-built AlSi10Mg until data exist: σ_w7 30 to 60 MPa, b −0.095 to −0.19, K_n 1 to 2. All UNSURE.
- Assumptions: constant amplitude; crack initiation at the strut surface; R = −1, or a stated mean-stress rule.
- Validity: 1e3 < N < 1e7; struts in tension or bending, not compressive ratcheting; peak nominal strut stress below σ_y.
- Anchor: yield-normalised S–N sets for Ti-6Al-4V lattices (Amin Yavari 2013, 2015; Hrabe 2011); for the alloy family, Boniotti 2019 (AlSi7Mg); one unchecked candidate for AlSi10Mg (section 3, entry C1).
- Confidence: medium for the form; low for the parameters.
- Falsifier: a lattice S–N set where this form with independently measured σ_w7, b and static strength misses the life by more than a factor of 10 at K_n between 1 and 2.
- Status: plan Q5 candidate kept; the link to measured static strength is now the preferred source of k_peak, and stretch cells are no longer credited with a higher endurance ratio (claim 25).

**4. Default mismatch form: solid modulus, strain-controlled.**

- σ_a,loc = ½·K_n·c·E_s·abs(α_s − α_2)·ΔT/(1+S) [Pa]; macroscopic stress on the interface σ̄ = M_L·ε_m/(1+S) [Pa].
- c = 1 for stretch-dominated cells and for any cell under hydrostatic constraint ([U] R4, R7). BCC under equibiaxial strain with a free normal: c = 0.64 to 0.68 at ρ̄ = 0.1, 0.86 to 0.94 at 0.2, 1.08 to 1.29 at 0.4 (Timoshenko to Euler–Bernoulli; [4M] §4). c = 1/(1−ν_s) for bonded strut roots, core–shell struts and sheet TPMS (not computed; UNSURE).
- S = 0 is the screening value (upper bound on stress). 1/(1+S) holds when the plate is kept flat; a plate free to bend relieves more (claim 18).
- Assumptions: uniform temperature, one mismatched interface, bonded, elastic.
- Validity: nominal strut stress range c·E_s·ε_m/(1+S) plus mean below σ_y; H_L ≤ H_2 or bending restrained; L/H_L below about 4 for an interlayer. A notch-root range K_n·c·E_s·ε_m above σ_y is a warning, not a limit (claim 19).
- Anchor: none known. Needed: thermal cycling of a co-printed lattice on a dissimilar plate with strain measured in the first cell row, or a unit-cell FE with at least 5 cells per side.
- Confidence: high that E_s governs and E_eff does not; medium for c; low for life numbers derived from it.
- Falsifier: FE or test in the validity range with first-row peak strut stress above twice c·E_s·ε_m.
- Status: plan Q5 candidate kept; c table recomputed, validity rewritten, S handling decided.

### 2.2 Q4: load case, dissipation and totals

**5. The load case is limited by strut fatigue, not by collapse. Largest elastic, survivable σ_a at 1e7 cycles, R = −1, K_n = 1: 0.54 to 1.07 MPa (A), 0.23 to 0.45 MPa (B), 2.0 to 4.0 MPa (C [100]), 1.0 to 2.0 MPa (C [110]), for σ_w7 = 30 to 60 MPa.**

- Fatigue limit σ_a = σ_w(N)/(K_n·k_peak); first yield σ_y/k_peak; collapse 0.3·σ_y·ρ̄^1.5 (A), 0.1486·σ_y·ρ̄^1.5 (B), ρ̄·σ_y/3 (C [100]), ρ̄·σ_y/6 (C [110]).
- First yield: 4.47, 1.88, 16.7, 8.33 MPa. Collapse: 6.71, 3.32, 16.7, 8.33 MPa ([L] R14, R11). K_n = 2 halves the fatigue values ([4Q] §2). Elastic buckling does not bind for ρ̄ ≥ 0.039 ([L] R12).
- The prompt's "1 to 2 MPa" matches A at 60 MPa and the octet at 30 MPa. The superseded 20 MPa case puts the peak strut stress at 1118, 2655, 300 and 600 MPa, all above σ_y ([L] R15).
- Fatigue binds for all N above N_x = 1e7·(K_n·σ_y/σ_w7)^(1/b). N_x is 476 cycles for the central curve and below 100 cycles for 64 of 80 parameter combinations; its largest value is 1.0e5 ([4Q] §3).
- The order of the cells (octet about 4 times A, 9 times B) is a model result. The one experimental comparison S3 found (Dallago 2018, cubic-cell variants, Ti-6Al-4V, fully reversed) reports no advantage of stretch-dominated cells.
- Confidence: medium for the bending cells; low for the octet advantage.
- Falsifier: an as-built AlSi10Mg strut S–N set with σ_w7 outside 30 to 60 MPa; a unit-cell FE with k_peak·ρ̄^1.5 below 3 for BCC at ρ̄ ≤ 0.2.
- Status: plan C4 and C5 revised (σ_w7 range; N_x statement; ordering demoted).

**6. Σ̇ at that σ_a, with each cell's own modulus.**

| Cell | E_eff [GPa] | σ_a [MPa] (σ_w7 60 / 30) | Σ̇ at 1 Hz [W/K] | Σ̇ at 1 per day [W/K] | Total over 1e7 cycles [J/K] |
|---|---|---|---|---|---|
| A (E_s·ρ̄²) | 2.80 | 1.07 / 0.54 | 3.43e-6 / 8.57e-7 | 3.97e-11 / 9.92e-12 | 34.3 / 8.6 |
| B (BCC) | 0.228 to 0.253 | 0.452 / 0.226 | 6.74e-6 to 7.46e-6 / 1.68e-6 to 1.86e-6 | 7.80e-11 to 8.63e-11 / 1.95e-11 to 2.16e-11 | 67.4 to 74.6 / 16.8 to 18.6 |
| C [100] (ρ̄·E_s/9) | 1.556 | 4.00 / 2.00 | 8.57e-5 / 2.14e-5 | 9.92e-10 / 2.48e-10 | 857 / 214 |
| C [110] (ρ̄·E_s/6) | 2.333 | 2.00 / 1.00 | 1.43e-5 / 3.57e-6 | 1.65e-10 / 4.13e-11 | 143 / 35.7 |

- Source: [E] R16, R18; [4Q] §4. The B range is Euler–Bernoulli to Timoshenko.
- τ_wearout = 1e7/ν is 0.317 years at 1 Hz and 27 379 years at 1 per day ([E] R18). At 1 per day the part never reaches 1e7 cycles; over 30 years at this amplitude it generates 0.94 J/K (C [100]) or 0.038 J/K (A) ([4Q] §4).
- The prompt's literal cross (one σ_a, both moduli): at 1 MPa, 2.98e-6 W/K with E_s·ρ̄² and 5.36e-6 W/K with ρ̄·E_s/9 at 1 Hz; at 2 MPa, 1.19e-5 and 2.14e-5 W/K ([E] R16). The ratio is 9·ρ̄ = 1.8. These pairs are not one physical case: 1 MPa means a 56 MPa strut peak in A (life 0.52 years at 1 Hz, total 49 J/K) and a 15 MPa strut peak in the octet (Basquin life 5000 years, so the 30-year total is 5.1e3 J/K at 1 Hz) ([4Q] §4).
- Between self-consistent pairs Σ̇ differs by 25 (C [100] over A) and 12.7 (C [100] over B) ([4Q] §4).
- Confidence: high for the arithmetic; medium-low for the inputs.
- Falsifier: none computational beyond the inputs; the 1.8 and 25 ratios follow from claim 15.
- Status: plan C6 kept; B now a range; σ_w7 = 30 MPa column added.

**7. The life-integrated entropy does not depend on frequency; frequency sets Σ̇ and τ_wearout only.**

- S_life = N_f·ψ·V_env·σ_a²/(2·E_eff·T₀) [J/K]. With a service cap: S = Σ̇·min(N_f/ν, τ_service).
- This is true by construction for a frequency-independent ψ. The thermoelastic part of ψ is frequency dependent (claim 11).
- Confidence: high within the model.
- Falsifier: ψ of the alloy varying by more than 2 between 1e-5 and 1 Hz at fixed amplitude.
- Status: plan C7 kept.

**8. With strut fatigue as the constraint, E_eff drops out, and the bound grows as N^(1+2b).**

- S_life ≤ N·ψ·ρ̄·V_env·σ_w(N)²/(2·E_s·T₀·K_n²·r²) [J/K], σ_w(N) = σ_w7·(N/1e7)^b.
- r²: 1 (C [100]), 1.8 (C [111]), 6 (C [110]), 11.5 to 12.7 (B), 25 (A) ([U] R2, R9; [4Q] §0). The value for A is defined by the energy identity, not computed from a geometry.
- At 1e7 cycles, σ_w7 = 60 MPa: 857, 476, 143, 67 and 34 J/K ([E] R18). At σ_w7 = 30 MPa: one quarter.
- With a cap, the maximum is at N_f = ν·τ_service. C [100] at 1 Hz, σ_w7 = 60 MPa, K_n = 1: 0.95e4 to 1.4e4 J/K (10 years), 2.0e4 to 3.4e4 J/K (30 years); at 1 per day 1.4 to 7.4 J/K ([E] R19; [4Q] §5). All 36 maxima S2 searched are interior and below first yield ([E] R19).
- Confidence: high for the formula; medium-low beyond 1e7 cycles.
- Falsifier: S–N data for the as-built alloy showing a fatigue limit or a slope change between 1e7 and 1e9 cycles.
- Status: plan C8 and C9 kept; 30-year values added.

**9. The total is most sensitive to K_n, ψ and σ_w7, in that order.**

- Over the plan's ranges the 1 Hz, 20-year maximum changes by 16 (K_n 1 to 4), 10 (ψ 1e-3 to 1e-2), 6.25 (σ_w7 40 to 100 MPa), 2.9 (b −0.07 to −0.20), 0.87 (E_s) and not at all with σ_y ([S] R24). The scalings with K_n, ψ, σ_w7 and E_s are identities of the formula, so this is a ranking, not a test.
- Confidence: high.
- Falsifier: not applicable (ranking of a closed form).
- Status: new from S2.

**10. ψ = 5e-3 is inside the range general aluminium data give, has no source for this alloy, and carries a factor of 0.35 to 12 from its unstated reference amplitude.**

- Converted literature values: dural η 4e-4 to 1e-3 gives ψ 2.5e-3 to 6.3e-3; pure Al gives 1.3e-4 to 1.3e-2; modal damping ratios reported for LPBF AlSi10Mg, 0.013 to 0.311 %, give 1.6e-3 to 3.9e-2, and one study's 1.03 % gives 0.13 ([4Q] §7). Modal values include fixture and air damping; conversions are S4 arithmetic on snippet values (UNSURE).
- If damping energy scales as σ^n_d, Σ̇ is multiplied by κ(n_d)·(σ_rms/σ_ref)^(n_d−2). For n_d 2.3 to 3 and σ_ref 5 to 60 MPa the factor is 0.35 to 12 ([S] R22). At n_d = 2.3 it is 0.72 to 2.1; at n_d = 4 it reaches 144 for the octet ([4Q] §8). The largest values belong to the octet because all its struts sit at the full 60 MPa.
- κ for a linear moment: rectangular section 1.69 (n_d = 3), 3.24 (4); circular 1.76, 3.60 ([U] R5).
- Confidence: medium.
- Falsifier: lattice hysteresis energy against amplitude with a log–log slope of 2 (then the factor is 1).
- Status: plan C12 revised (0.2 to 6 became 0.35 to 12).

**11. Thermoelastic damping is negligible at 1 Hz for struts up to 1 mm and not for thick struts; it is nil at 1 per day.**

- ψ_TE(f) = 2π·Δ_E·x/(1+x²), x = f/f_Z, f_Z = π·D/(2·t²) [Hz], Δ_E = E_s·α_s²·T₀/(ρ_s·c_p) [-], D = k/(ρ_s·c_p) [m²/s]. Reed formula applied to round struts; prefactors UNSURE; bending part of the strain energy only.
- α_s = 21e-6 /K: Δ_E = 3.85e-3, maximum ψ_TE = 1.21e-2. At 1 Hz, ψ_TE/5e-3 is 0.014 (t = 0.5 mm), 0.057 (1 mm), 0.23 (2 mm), 1.31 (5 mm) ([S] R23). With α_s = 27e-6 /K: maximum 2.0e-2; 0.024, 0.094, 0.38, 2.2 ([4Q] §9). f_Z is 340, 85, 21 and 3.4 Hz.
- At 1/86 400 Hz ψ_TE is below 2e-7 ([S] R23).
- Confidence: medium-low.
- Falsifier: a frequency sweep of a bending-dominated lattice across f_Z with no loss peak.
- Status: plan §0 position revised ("matters near 20 to 400 Hz only" is wrong for struts of 2 mm and more).

**12. The match between the hot-spot entropy density and the fatigue fracture entropy is a coincidence of one N and is withdrawn as a cross-check on ψ.**

- s(N) = N·ψ·σ_w(N)²/(2·E_s·T₀) [J/(m³·K)]. Ratio to 4 MJ/(m³·K): 1.07 at 1e7 cycles, 0.17 to 0.21 at 1e6, 5.5 to 6.9 at 1e8, 29 to 45 at 1e9 (σ_w7 = 60 MPa); 0.27 at 1e7 for σ_w7 = 30 MPa ([E] R21; [4Q] §10).
- A constant accumulated entropy at failure together with Basquin needs the damaging dissipation per cycle to scale as σ^(−1/b), exponent 7.0 to 10.5 for b = −0.1434 to −0.095 ([4Q] §10). Anelastic damping scales as σ^2 to σ^4. So most of the hysteretic entropy at high-cycle amplitudes is not damage-related, and the two quantities should not be equated.
- Confidence: medium (algebra); the physical reading is low.
- Falsifier: calorimetric data on the alloy showing dissipation per cycle rising as σ^7 or steeper below 60 MPa.
- Status: plan C13 withdrawn.

**13. The part mass is 0.534 kg, not about 1 kg.**

- m = ρ_s·ρ̄·V_env = 2670 × 0.2 × 1e-3 kg ([L] R10; [4Q] §6).
- Confidence: high. Falsifier: none. Status: plan C11 kept.

### 2.3 Q1: dissipation forms (see also section 4)

**14. The macroscopic and strut-level forms give the same energy if and only if the strut form uses σ_rms and E_eff is the true modulus.**

- V_env·σ_a²/(2·E_eff) = ρ̄·V_env·σ_rms²/(2·E_s) [J]; σ_rms = σ_a·sqrt(E_s/(ρ̄·E_eff)) [Pa].
- The two routes agree to 1e-9 on the octet (three directions) and to 2.5e-9 on the BCC beam cell ([U] R3, R9; [E] R17). This tests Clapeyron's theorem and the code on linear models. It does not test the pin-jointed or beam assumptions.
- Confidence: high.
- Falsifier: periodic unit-cell FE where the volume integral of strain energy differs from V_env·σ_a²/(2·E_eff) beyond mesh error.
- Status: plan C1 kept.

**15. Knock-down between macroscopic and strut stress.**

- Energy-equivalent stress: σ_rms/σ_a = C1^(−1/2)·ρ̄^(−(n+1)/2) for E_eff = C1·E_s·ρ̄^n: exponent −1.5 for bending cells, −1 for stretch cells.
- Peak nominal stress: k_peak = 5.0·ρ̄^(−1.5) to 5.66·ρ̄^(−1.5) (A, f = 1.5 to 1.70), 11.43·ρ̄^(−1.5) + 1/ρ̄ (B), 3/ρ̄ (octet [100], [111]), 6/ρ̄ (octet [110]) ([L] R13; [U] R2, R6).
- σ_peak/σ_rms for a linear bending moment: 3 (rectangular), 2√3 = 3.46 (circular) ([U] R5); 3.57 for BCC with its axial stress at ρ̄ = 0.2 ([U] R9); 1 for the octet along [100] only ([U] R2).
- At the fatigue-limited amplitudes σ_rms is 12.0 MPa (A), 16.8 MPa (B) and 60 MPa (C [100]) for σ_w7 = 60 MPa ([S] R22). Dissipation uses σ_rms; fatigue uses K_n·σ_peak.
- Confidence: high for exponents; medium for constants (no node volume, no fillets).
- Falsifier: FE strut-stress histogram with log–log slope against ρ̄ other than −1.5 (bending) or −1 (stretch); peak over RMS outside 2.5 to 6 for a slender bending cell.
- Status: plan C2 kept.

**16. E_eff = E_s·ρ̄² is wrong for both named strut lattices.**

- Octet [100]: ρ̄·E_s/9, so E_s·ρ̄² is 9·ρ̄ times too large (1.8 at ρ̄ = 0.2); the two cross at ρ̄ = 1/9 ([U] R1; [E] R16).
- BCC [001]: 0.0919·E_s·ρ̄² in the slender limit, 0.0902 (Euler–Bernoulli) and 0.0815 (Timoshenko) at ρ̄ = 0.2, so E_s·ρ̄² is 11.1 to 12.3 times too large ([U] R6; [4Q] §0). Node volume acts the other way; its size is unknown.
- Gyroid: not computed (open point 1).
- Confidence: high for the beam algebra; medium-low at ρ̄ ≥ 0.2 (strut length over diameter 4.5).
- Falsifier: measured BCC modulus over E_s·ρ̄² near 1 at ρ̄ ≤ 0.2.
- Status: plan C3 revised (Timoshenko added; attribution of the closed forms to Ushijima 2011 withdrawn).

### 2.4 Q2: thermal mismatch (see also section 4)

**17. Strut stress under mismatch is set by E_s and the imposed strain. For pin-jointed cells it cannot exceed E_s·ε_m; for BCC the beam models give c between 0.64 and 1.29.**

- Octet, equibiaxial ε_m, free normal: in-plane struts at E_s·ε_m exactly, others at zero, normal strain −ε_m, biaxial modulus ρ̄·E_s/6. Hydrostatic: all struts at E_s·ε_m ([U] R4).
- BCC, equibiaxial: c = 0.68, 0.94, 1.14, 1.29 at ρ̄ = 0.1, 0.2, 0.3, 0.4 (Euler–Bernoulli); 0.64, 0.86, 0.99, 1.08 (Timoshenko). c passes 1 at ρ̄ = 0.227 or 0.309 ([U] R7; [4M] §4). BCC, hydrostatic: struts purely axial at E_s·ε_m ([U] R7).
- The margin of the c = 1 screen for BCC is 1/c = 1.5 to 1.6 at ρ̄ = 0.1 and 0.78 to 0.92 at ρ̄ = 0.4 ([4M] §4).
- The original E_s·ρ̄²·ε_m, used as a local stress, is low by 21 to 25 at ρ̄ = 0.2 ([4M] §4).
- Confidence: high for the octet; medium for BCC (the two beam theories differ by 5 to 16 % over ρ̄ = 0.1 to 0.4; node volume absent).
- Falsifier: beam or solid FE of 5×5×5 cells with first-row peak stress over E_s·ε_m outside these values by more than 30 %.
- Status: plan C14 kept; C15 revised (crossover 0.20 became 0.23 to 0.31; the closed form 2.10·ρ̄^0.5 + 0.37·ρ̄ is 7 % high at ρ̄ = 0.2: 1.013 against 0.943, [U] R7).

**18. S is small for equal thicknesses, but 1/(1+S) is the flat-plate result. S = 0 is the screening value.**

- S at H_L = H_2: 4.3e-4 (BCC, ρ̄ = 0.1, steel) to 0.093 (A, ρ̄ = 0.4, Ti-6Al-4V); octet, ρ̄ = 0.2, Ti-6Al-4V: 0.0135. At H_L/H_2 = 10 it reaches 0.93 ([M] R29).
- Decision on the S2 discrepancy: the values with S are the correct evaluation of the stated formula. The plan's expected values for R28, R30 and R31 left S out (a slip in the hand arithmetic). With S: σ_a,loc = 21.41 MPa (K_n = 1) and 64.23 MPa (K_n = 3); N(50 K) = 6.22e6 cycles; ΔT_x = 124.1 K; 30-year dissipation 0.0399 J/K ([M] R28, R30, R31). S changes stress by 1.3 % and life by 10 to 15 % ([4M] §2).
- If the bilayer is free to bend, the relief is larger. Exact two-unknown plate solution, octet ρ̄ = 0.2 on Ti-6Al-4V, H_L = H_2: strut-stress factor 0.920 at the interface, 0.852 at mid-height, 0.784 at the top, against 0.987 for 1/(1+S). To first order the interface factor is 1 − (4 + 3·H_L/H_2)·S ([4M] §1). The interface-row factor stays between 0.71 and 1.00 in all listed cases.
- The same solver returns the bimetal check: equal modulus and thickness give 1/8 + 3/8 = 0.5 of E·ε at the interface ([4M] §1).
- Confidence: high for the plate algebra; medium that plate theory describes a lattice block a few cells high.
- Falsifier: FE with E_2/E_s varied from 0.3 to 3 at H_2 ≥ H_L, bending restrained, changing first-row strut stress by more than 20 %.
- Status: plan C16 revised (bending relief and the H_L/H_2 = 10 case added; "below about 0.1" holds at H_L = H_2 only).

**19. Whether diurnal mismatch limits life depends on σ_w7 and K_n. With the plan's inputs it does not; with σ_w7 = 30 MPa and K_n ≥ 2 it can.**

- N = 1e7·(σ_a,loc/σ_w7)^(1/b), 1 cycle per day, ΔT = 50 K, octet S at H_L = H_2, c = 1, no mean stress.
- Plan inputs (α_s = 21e-6 /K, σ_w7 = 60 MPa): shortest life 100 years (Invar, K_n = 3, b = −0.095); Ti-6Al-4V, K_n = 3: 1.3e4 to 1.7e4 years ([4M] §2). The largest listed Δα is Invar's (19.7e-6 /K), not Ti-6Al-4V's as the plan said.
- σ_w7 = 30 MPa, α_s unchanged: 4.9 years (Invar, K_n = 2), 9.1 years (Ti-6Al-4V, K_n = 3), 0.07 years (Invar, K_n = 3), all at b = −0.095 ([4M] §2).
- Over the whole grid (5 partners × 3 α_s × 2 σ_w7 × 2 b): lives below 30 years in 0 of 60 cases at K_n = 1, 4 of 60 at K_n = 2, 10 of 60 at K_n = 3 ([4M] §2).
- Halving σ_w7 at fixed b multiplies life by 0.008 (b = −0.1434) or 0.0007 (b = −0.095) ([4M] §2). A life number from this model is an order-of-magnitude statement at best.
- ΔT at which N = 10 958 cycles (30 years), K_n = 3: Ti-6Al-4V 89 to 124 K and Invar 56 to 78 K with plan inputs; Ti-6Al-4V 45 to 82 K and Invar 28 to 52 K with σ_w7 = 30 MPa; lowest in the grid 21.5 K (Invar, α_s = 27e-6 /K, σ_w7 = 30 MPa, b = −0.095) ([4M] §3). The form is closed, so no bracket is needed; the cases S2 found above 500 K with the plan inputs (316L and copper at K_n = 1, steel at K_n = 1 with b = −0.1434) mean no limit in any service range.
- Elastic flag. At ΔT_x the notch-root amplitude equals σ_w(10 958) by construction: 159.5 MPa for the central curve, so the notch-root range is 319 MPa and exceeds σ_y for every K_n, as S2 found for K_n = 3. The flag is a property of the S–N curve (it fires when σ_w(10 958) exceeds σ_y/2) and does not fire for the other three curves (57 to 115 MPa). The nominal strut range exceeds σ_y only at K_n = 1 ([4M] §3). Reading: with K_n as a fatigue notch factor, a notch-root range between σ_y and 2·σ_y is a shakedown case where stress-life is marginal; a nominal range above σ_y is outside the model.
- Confidence: medium that K_n = 1 cases are safe; low for any specific life.
- Falsifier: thermal-cycling test of an AlSi10Mg lattice on Ti-6Al-4V or Invar at ΔT ≤ 50 K failing before 1e4 cycles with measured σ_w7 above 60 MPa.
- Status: plan C17 revised (no longer a general statement; worst partner corrected; S included; flag reinterpreted).

**20. Cool-down mean stress gives a bound pair, not a reversal.**

- Lower bound on ΔT_x: Goodman, σ_ar = σ_a,loc/(1 − σ_m/σ_u), σ_m = min(σ_y, E_s·Δα·ΔT_ref). Upper bound: no mean-stress effect.
- The factor is 2.67 for σ_u = 400 MPa and 2.19 for 460 MPa at σ_m = σ_y. σ_m reaches σ_y at ΔT_ref = 288 K (Ti-6Al-4V) or 181 K (Invar) for α_s = 21e-6 /K ([4M] §3).
- Ti-6Al-4V, K_n = 3, plan inputs: ΔT_x between 46.5 K (Goodman, σ_u = 400 MPa; 56.7 K with 460 MPa) and 124.1 K. Worst listed: Invar, α_s = 27e-6 /K, σ_w7 = 30 MPa, 14.8 to 39.6 K ([4M] §3). S2's 45.9 K is the same case at S = 0 ([M] R30).
- The literature is split. de Krijger 2017 (compression–compression, diamond Ti-6Al-4V lattices) reports life governed by amplitude and insensitive to mean stress. Lietaert 2018 reports shorter tension–tension lives through local tensile mean stress. Goodman is therefore kept as the conservative bound only.
- For any R other than −1, collapse and first yield apply to σ_max = 2·σ_a/(1−R). At R = 0.1 the Goodman allowable local amplitude is 50.7 MPa instead of 60 MPa ([S] R25).
- Confidence: medium-low.
- Falsifier: lattice S–N data at two mean stresses in tension showing either no shift or a shift larger than Goodman predicts.
- Status: plan C18 revised ("can reverse" became "bounded between").

**21. Mismatch dissipation is immaterial, and the modulus acts in the opposite direction to stress control.**

- ΔS per cycle = ψ·V_env·M_L·ε_a²/T₀. Octet, Ti-6Al-4V, 50 K: 3.64e-6 J/K per cycle, 0.0399 J/K in 30 years; A 0.067 J/K; BCC 0.0084 J/K ([M] R31). With α_s = 27e-6 /K: 0.088, 0.148 and 0.018 J/K; largest listed case 0.29 J/K ([4M] §5).
- Under strain control A dissipates 1.68 to 1.71 times the octet; at fixed stress the octet dissipates 1.8 times A ([M] R31; [E] R16).
- Confidence: high.
- Falsifier: none short of ψ larger by three orders.
- Status: plan C19 kept; value now with S.

**22. Thermal lag and interlayer shear can exceed the Δα term; both are magnitudes only here.**

- Lag stress E_s·α_s·ΔT_lag: 14.7 MPa for 10 K (18.9 MPa with α_s = 27e-6 /K) against 43.4 MPa (Ti-6Al-4V) and 17.5 MPa (316L) for the Δα term at 50 K. Break-even ΔT_lag/ΔT = Δα/α_s: 0.59 (Ti-6Al-4V), 0.24 (316L) ([M] R32; [4M] §6).
- Interlayer between two stiff parts: edge shear strain γ ≈ ε_m·L/(2·H_L), above 2·ε_m for L/H_L above 4 (definition, not a check; [M] R32).
- Confidence: medium for the lag magnitude; low for the shear estimate (no model of the cell under shear).
- Falsifier: transient thermal FE of a strut lattice on a massive partner; sandwich FE varying L/H_L.
- Status: plan R32 kept as magnitudes.

### 2.5 Q3: fatigue life and the literature

**23. Basquin with macroscopic σ_a and solid-material constants is not acceptable. It over-predicts life by 8 to 22 decades at ρ̄ = 0.2.**

- Over-prediction = (K_n·k_peak)^(−1/b). K_n = 1: 12.4 and 8.2 decades (C [100]; b = −0.095 and −0.1434), 18.4 and 12.2 (A), 22.3 and 14.8 (B) ([N] R26).
- Acceptable: (i) local stress K_n·k_peak·σ_a into an S–N curve of as-built thin struts; (ii) a lattice-level power law with stress divided by the same lattice's static yield or plateau stress. Claim 3 shows these are one equation.
- Confidence: high.
- Falsifier: a lattice dataset where solid constants with macroscopic stress predict life within a factor of 10.
- Status: plan C20 kept.

**24. The literature normalises lattice S–N data in three ways.**

- (a) By the lattice's own yield or plateau stress: Hrabe 2011; Amin Yavari 2013 (four porosities on one power law, R² = 0.94); Amin Yavari 2015; Zhao 2016.
- (b) By a power law in ρ̄: Zargarian 2016, which is an FE study validated on literature data, not a test; it finds the S–N exponent depends on the bulk material only. Li 2012 is cited for this in the plan but its abstract was not seen (UNSURE).
- (c) By local strut stress: Van Hooreweder and Kruth 2017; Van Hooreweder 2017; Boniotti 2019 (strength equals the local fatigue limit at hot spots, AlSi7Mg); Dallago 2018 and 2019 (notches and geometric imperfection control strength).
- Normalising by lattice yield collapses densities within one cell type but not across types (Amin Yavari 2015). Ahmadi 2018 finds the normalised curve depends more on material than on topology. The two disagree on what the normalisation removes.
- Burr 2020 is a progressive strut-failure framework, not a local-stress method from as-built strut data; it is removed from (c).
- Confidence: medium (abstract level).
- Falsifier: full-text reading contradicting any attribution above.
- Status: plan C21 revised.

**25. The model reproduces the order of the reported normalised endurance ratios but not their spread, and its higher ratio for stretch cells is not supported.**

- Model, amplitude over lattice yield at run-out: σ_w7/(f·K_n·σ_y) for bending, σ_w7/(K_n·σ_y) for stretch. K_n = 1: AlSi10Mg 0.08 to 0.16 (bending) and 0.12 to 0.24 (stretch) for σ_w7 = 30 to 60 MPa; Ti-6Al-4V (σ_w 200 MPa, σ_y 950 MPa) 0.14 and 0.21 ([N] R27; [4Q] §11).
- Reported: 0.15 to 0.25 at 1e6 cycles (Hrabe 2011, R = 0.1); below 0.2 (Amin Yavari 2013); up to 0.6 for TPMS (Bobbert 2017). Whether these are σ_max over yield is not confirmed (UNSURE).
- If they are σ_max at R = 0.1, the model's Ti-6Al-4V bending value is 0.31 on that basis, 1.25 to 2.1 times the reported 0.15 to 0.25 ([4Q] §11). That is inside the factor of 3 the plan set as its falsifier. The same ratio is the K_n that would close the gap; quoting it as K_n would be a fit.
- The reported spread (0.15 to 0.6) is as wide as the model's whole range. The model assigns the high end to stretch cells; Dallago 2018 found no such advantage in fully reversed tests, and the 0.6 belongs to TPMS sheets or skeletons, which the model does not cover.
- Confidence: low.
- Falsifier: after the stress basis is confirmed from full text, a mismatch above 3 for strut lattices.
- Status: plan C22 revised (weakened; ordering by topology withdrawn as a prediction).

**26. As-built surface and near-surface defects control strut fatigue. There is no standard lattice knock-down.**

- Machined LPBF AlSi10Mg: 110 MPa at 2e7 (EOS data sheet, machined), 125 to 130 MPa at 1e7 (snippets, R not stated). As-built: no amplitude value found; "below 70 MPa" (snippet, basis unclear) and at most about 31.5 MPa from Aboulkhair 2016 if its range is at R = 0.1 ([4Q] §1).
- Implied as-built over machined ratio: 0.46 to 0.55 for 60 MPa, 0.23 to 0.27 for 30 MPa ([4Q] §1). The plan's 0.5 to 0.8 for AlSi10Mg is not supported at its upper end.
- Roughness acts as micro-notches and the effect is larger in smaller sections (Pegues 2018, Ti-6Al-4V). Defect-based prediction uses the √area parameter (Murakami 2002; Romano 2018; Beretta and Romano 2017). HIP with chemical etching improved diamond Ti-6Al-4V lattices (Van Hooreweder 2017; numbers not seen).
- Standards: no lattice-specific knock-down was found in NASA-STD-6030. Secondary sources give high-cycle stress limits of 80 % (improved surface) and 60 % (as-built surface) of the applicable fatigue limit (UNSURE; the standard was not opened).
- Confidence: medium for the statements; low for every number.
- Falsifier: an S–N curve of as-built AlSi10Mg thin struts with σ_w7 above 60 MPa at R = −1.
- Status: plan C23 revised (ratio range).

**27. Published lattice S–N data are mostly compression–compression at R = 0.1; their slopes and endurance ratios should not be transferred to tension, shear or mismatch loading.**

- Cyclic ratcheting with strut cracking dominates in compression (Zhao 2016). Tension–tension lives are shorter (Lietaert 2018, R = 0.1, −1 and 10). Under compression the S–N curve shifts with R while amplitude governs life (de Krijger 2017).
- Confidence: medium.
- Falsifier: tension–tension and compression–compression S–N curves of one lattice coinciding on a local-stress basis.
- Status: plan C24 kept; de Krijger's finding stated as found.

**28. τ_wearout = N/ν needs a cap, and the as-built Basquin slope is not fixed by the data in hand.**

- Aluminium alloys have no endurance limit and constant-b extrapolation beyond 1e7 to 1e8 cycles is unverified. At 1 per day, 1e7 cycles is 27 379 years ([E] R18). Use τ = min(N_f/ν, τ_service).
- Anchoring the as-built curve at σ_f' = 1.67·σ_u gives b = −0.143 to −0.152 for σ_w7 = 60 MPa and −0.185 to −0.193 for 30 MPa (σ_u 400 to 460 MPa). The same law predicts a machined σ_w7 of 135 to 156 MPa against the 110 to 130 MPa found ([4Q] §1). The law is for wrought alloys; its use here is unverified.
- For b = −0.07 and −0.095 with low σ_w7 the implied σ_f' is below σ_y (97 to 198 MPa, [4Q] §3). Those curves are local fits around 1e7 cycles and cannot be used below about 1e4 cycles.
- Confidence: high for the cap; low for b.
- Falsifier: none computational.
- Status: plan C25 kept; C26 revised (b is a range).

## 3. Citations

Status words are S3's (title and abstract level; no full text was opened). Equation, figure and section numbers were not checked by any stage and are UNSURE throughout; none is given where it is not known. No entry was marked "not found". Entries the claims do not use are omitted.

**Lattice S–N data and normalisation**

- Hrabe, Heinl, Flinn, Körner, Bordia (2011). "Compression-compression fatigue of selective electron beam melted cellular titanium (Ti-6Al-4V)". J. Biomed. Mater. Res. B 99B, 313–320. Verified: R = 0.1, normalised strength 0.15 to 0.25 at 1e6 cycles. Normalisation basis UNSURE. Figure UNSURE.
- Li, Murr, Cheng, Zhang, Hao, Yang, Medina, Wicker (2012). "Compression fatigue behavior of Ti–6Al–4V mesh arrays fabricated by electron beam melting". Acta Materialia 60, 793–802. Exists; content not checked (UNSURE).
- Amin Yavari, Wauthle, van der Stok, Riemslag, Janssen, Mulier, Kruth, Schrooten, Weinans, Zadpoor (2013). "Fatigue behavior of porous biomaterials manufactured using selective laser melting". Mater. Sci. Eng. C 33, 4849–4858. Verified: one power law, R² = 0.94, endurance below 0.2. Figure UNSURE.
- Amin Yavari, Ahmadi, Wauthle, Pouran, Schrooten, Weinans, Zadpoor (2015). "Relationship between unit cell type and porosity and the fatigue behavior of selective laser melted meta-biomaterials". J. Mech. Behav. Biomed. Mater. 43, 91–100. Verified: collapse within a cell type only.
- Zargarian, Esfahanian, Kadkhodapour, Ziaei-Rad (2016). "Numerical simulation of the fatigue behavior of additive manufactured titanium porous lattice structures". Mater. Sci. Eng. C 60, 339–347. Verified with a caveat: FE study, not test data.
- Zhao, Li, Hou, Hao, Yang, Misra (2016). "The influence of cell morphology on the compressive fatigue behavior of Ti-6Al-4V meshes fabricated by electron beam melting". J. Mech. Behav. Biomed. Mater. 59, 251–264. Verified.
- Van Hooreweder, Kruth (2017). "Advanced fatigue analysis of metal lattice structures produced by Selective Laser Melting". CIRP Annals 66(1), 221–224. Verified (diamond cells, CoCr and Ti-6Al-4V).
- Van Hooreweder, Apers, Lietaert, Kruth (2017). "Improving the fatigue performance of porous metallic biomaterials produced by Selective Laser Melting". Acta Biomaterialia 47, 193–202. Verified; numbers not seen.
- Lietaert, Cutolo, Boey, Van Hooreweder (2018). "Fatigue life of additively manufactured Ti6Al4V scaffolds under tension-tension, tension-compression and compression-compression fatigue load". Scientific Reports 8, 4957. Verified.
- de Krijger, Rans, Van Hooreweder, Lietaert, Pouran, Zadpoor (2017). "Effects of applied stress ratio on the fatigue behavior of additively manufactured porous biomaterials under compressive loading". J. Mech. Behav. Biomed. Mater. 70, 7–16. Verified.
- Ahmadi, Hedayati, Li, Lietaert, Tümer, Fatemi, Rans, Pouran, Weinans, Zadpoor (2018). "Fatigue performance of additively manufactured meta-biomaterials: The effects of topology and material type". Acta Biomaterialia 65, 292–304. Verified.
- Bobbert, Lietaert, Eftekhari, Pouran, Ahmadi, Weinans, Zadpoor (2017). "Additively manufactured metallic porous biomaterials based on minimal surfaces: A unique combination of topological, mechanical, and mass transport properties". Acta Biomaterialia 53, 572–584. Verified: endurance up to 60 % of yield in the abstract; stress basis UNSURE.
- Benedetti, du Plessis, Ritchie, Dallago, Razavi, Berto (2021). "Architected cellular materials: A review on their mechanical properties towards fatigue-tolerant design and fabrication". Mater. Sci. Eng. R 144, 100606. Verified (review).
- Dallago, Fontanari, Torresani, Leoni, Pederzolli, Potrich, Benedetti (2018). "Fatigue and biological properties of Ti-6Al-4V ELI cellular structures with variously arranged cubic cells made by selective laser melting". J. Mech. Behav. Biomed. Mater. 78, 381–394. Verified with a caveat: no advantage of stretch-dominated cells in fully reversed tests.
- Dallago, Winiarski, Zanini, Carmignato, Benedetti (2019). "On the effect of geometrical imperfections and defects on the fatigue strength of cellular lattice structures additively manufactured via Selective Laser Melting". Int. J. Fatigue 124, 348–360. Verified.
- Burr, Persenot, Doutre, Buffiere, Lhuissier, Martin, Dendievel (2020). "A numerical framework to predict the fatigue life of lattice structures built by additive manufacturing". Int. J. Fatigue 139, 105769. Exists; does not say what the plan cited it for (progressive strut failure, EBM). Used only as stated in claim 24.
- Boniotti, Beretta, Patriarca, Rigoni, Foletti (2019). "Experimental and numerical investigation on compressive fatigue strength of lattice structures of AlSi7Mg manufactured by SLM". Int. J. Fatigue 128, 105181. Verified (record); AlSi7Mg, not AlSi10Mg.

**As-built surface, porosity, knock-down**

- Aboulkhair, Maskery, Tuck, Ashcroft, Everitt (2016). "Improving the fatigue behaviour of a selectively laser melted aluminium alloy: Influence of heat treatment and surface quality". Materials & Design 104, 174–182. Verified: as-built (Ra 17.1 µm) did not reach 3e7 cycles at maximum stress ranges of 63 to 220 MPa. Stress ratio UNSURE.
- Mower, Long (2016). "Mechanical behavior of additive manufactured, powder-bed laser-fused materials". Mater. Sci. Eng. A 651, 198–213. Verified: as-fabricated fatigue strength inferior to conventional. No value used.
- Romano, Brückner-Foit, Brandão, Gumpinger, Ghidini, Beretta (2018). "Fatigue properties of AlSi10Mg obtained by additive manufacturing: Defect-based modelling and prediction of fatigue strength". Eng. Fract. Mech. 187, 165–189. Verified.
- Beretta, Romano (2017). "A comparison of fatigue strength sensitivity to defects for materials manufactured by AM or traditional processes". Int. J. Fatigue 94, 178–191. Verified.
- Pegues, Roach, Williamson, Shamsaei (2018). "Surface roughness effects on the fatigue strength of additively manufactured Ti-6Al-4V". Int. J. Fatigue 116, 543–552. Verified.
- Murakami (2002). "Metal Fatigue: Effects of Small Defects and Nonmetallic Inclusions". Elsevier. Verified.
- EOS GmbH, material data sheet "EOS Aluminium AlSi10Mg". Verified, conditions differ: 110 MPa at 2e7, fully reversed, machined; yield 233 to 270 MPa; ultimate 461 to 466 MPa; modulus 70 to 75 GPa. Year UNSURE; values via a secondary summary.
- NASA-STD-6030 (2021), "Additive Manufacturing Requirements for Spaceflight Systems". Exists; no lattice knock-down found; the 80 % and 60 % limits are from a conference slide (UNSURE).
- ISO 13314:2011, "Mechanical testing of metals — Ductility testing — Compression test for porous and cellular metals". Verified.

**Basquin and mean stress**

- Basquin (1910). "The exponential law of endurance tests". Proc. ASTM 10, 625–630. Verified (bibliographic).
- Bäumel, Seeger (1990). "Materials Data for Cyclic Loading, Supplement 1". Elsevier. Verified through secondary sources: σ_f' = 1.67·σ_u, b = −0.095 for aluminium and titanium alloys (wrought). Applicability to LPBF AlSi10Mg unverified.
- Dowling, "Mechanical Behavior of Materials", 4th ed. (2012 or 2013), Pearson. Exists; Goodman, Morrow and notch-factor chapters not individually confirmed (UNSURE).

**Cell stiffness and strength**

- Gibson, Ashby (1997). "Cellular Solids: Structure and Properties", 2nd ed., Cambridge University Press, chapter 5. Constants 1, 0.3 and 0.05 confirmed through secondary sources only; equation numbers UNSURE.
- Ashby (2006). "The properties of foams and lattices". Phil. Trans. R. Soc. A 364, 15–30. Verified (contains the 0.05 constant).
- Deshpande, Fleck, Ashby (2001). "Effective properties of the octet-truss lattice material". J. Mech. Phys. Solids 49, 1747–1769. Verified at abstract level; the values ρ̄·E_s/9, ρ̄·E_s/12 and ρ̄·σ_y/3 are derived here ([U] R1, R2) and were not seen in the paper (UNSURE).
- Deshpande, Ashby, Fleck (2001). "Foam topology: bending versus stretching dominated architectures". Acta Materialia 49, 1035–1040. Verified.
- Ushijima, Cantwell, Mines, Tsopanos, Smith (2011). "An investigation into the compressive properties of stainless steel micro-lattice structures". J. Sandwich Struct. Mater. 13, 303–329. Exists; may not state the closed forms used here. The BCC forms in this file are derived ([U] R6, R8), not attributed. A later paper reports up to 42 % error of this kind of model at larger strut aspect ratio (secondary).
- Yan, Hao, Hussein, Young, Huang, Zhu (2015). "Microstructure and mechanical properties of aluminium alloy cellular lattice structures manufactured by direct metal laser sintering". Mater. Sci. Eng. A 628, 238–246. Verified: AlSi10Mg gyroid, static. Candidate for gyroid constants.
- Al-Ketan, Rowshan, Abu Al-Rub (2018). "Topology-mechanical property relationship of 3D printed strut, skeletal, and sheet based periodic metallic cellular materials". Additive Manufacturing 19, 167–183. Verified: sheet TPMS near stretching-dominated, skeletal bending-dominated; maraging steel; exponents not seen.

**Bimaterial mismatch**

- Timoshenko (1925). "Analysis of bi-metal thermostats". J. Opt. Soc. Am. 11, 233–255. Verified.
- Stoney (1909). "The tension of metallic films deposited by electrolysis". Proc. R. Soc. A 82, 172–175. Verified.
- Suhir (1986). "Stresses in bi-metal thermostats". J. Appl. Mech. 53, 657–660. Verified.
- Freund, Suresh (2003). "Thin Film Materials: Stress, Defect Formation and Surface Evolution". Cambridge University Press. Verified.
- Bogy (1971). "Two edge-bonded elastic wedges of different materials and wedge angles under surface tractions". J. Appl. Mech. 38, 377–386. Verified.

**Damping and entropy**

- Lazan (1968). "Damping of Materials and Members in Structural Mechanics". Pergamon. Exists; D = J·σ^n with n between 2 and 4 (secondary); no aluminium values found.
- Zhang, Perez, Lavernia (1993). "Documentation of damping capacity of metallic, ceramic and metal-matrix composite materials". J. Mater. Sci. 28, 2395–2404. Verified (record); values not seen.
- Zener (1937). "Internal friction in solids. I. Theory of internal friction in reeds". Phys. Rev. 52, 230–235; (1938) part II, Phys. Rev. 53, 90–99. Verified.
- Nowick, Berry (1972). "Anelastic Relaxation in Crystalline Solids". Academic Press. Verified.
- Naderi, Amiri, Khonsari (2010). "On the thermodynamic entropy of fatigue fracture". Proc. R. Soc. A 466, 423–438. Verified: about 4 MJ/(m³·K) for Al 6061-T6, from low-cycle tests.
- Rosa, Manzoni, Casati (2018). "Damping behavior of 316L lattice structures produced by Selective Laser Melting". Materials & Design 160, 1010–1018. Verified: lattice damping above bulk; no numbers.

**Manufacturing energy**

- Gutowski, Branham, Dahmus, Jones, Thiriez, Sekulic (2009). "Thermodynamic analysis of resources used in manufacturing processes". Environ. Sci. Technol. 43, 1584–1590. Verified.
- Faludi, Baumers, Maskery, Hague (2017). "Environmental impacts of selective laser melting: do printer, powder, or power dominate?". J. Ind. Ecol. 21(S1), S144–S156. Exists; values not seen.
- Kellens, Mertens, Paraskevas, Dewulf, Duflou (2017). "Environmental impact of additive manufacturing processes: does AM contribute to a more sustainable way of part manufacturing?". Procedia CIRP 61, 582–587. Verified; 80 to 140 kWh/kg from a secondary snippet.

**Candidates S3 found (not evidence, not checked)**

- C1. "Experimental Evaluation of Fatigue Strength of AlSi10Mg Lattice Structures Fabricated by AM", Aerospace 2023, 10(5), 400. Authors and data availability UNSURE.
- C2. NASA-HDBK-5026 (2024), guidance on strength, fatigue and fracture for AM hardware. UNSURE.
- C3. A study of as-built AlSi10Mg surfaces, Procedia Structural Integrity (2020), "Influence of as-built surfaces on the fatigue behavior of AlSi10Mg ...". Authors UNSURE.

## 4. Q1 and Q2 against the earlier web answers

Claim numbers on the left are those of `prompt_3_q1_web_answer.md` and `prompt_3_q2_web_answer.md`.

| Earlier claim | Verdict | What changed, with source |
|---|---|---|
| Q1-1 energy identity | Accepted | Two-route agreement to 1e-9 and 2.5e-9 ([U] R3, R9); implementation check only |
| Q1-2 default macroscopic form, ψ at σ_rms | Accepted | Strut form with peak stress overestimates by r²: 9 (rectangular), 12 (circular), 12.7 (BCC, ρ̄ = 0.2) ([U] R5, R9). The "25" is the Gibson–Ashby constant pair, not a geometry |
| Q1-3 σ_rms scaling; octet constants | Accepted, one limit added | Octet values confirmed ([U] R1, R2). "RMS equals peak" holds along [100] only; along [110] the peak is 6·σ_a/ρ̄ and r² = 6 |
| Q1-4 peak constant C_σ ≈ 5 | Revised | 5.0 to 5.66 is the foam value; BCC gives 11.43 plus an axial term ([L] R13). Peak over RMS 3 and 3.46 confirmed ([U] R5) |
| Q1-5 constant ψ transfers | Accepted | Premise unverified for this alloy (claim 10) |
| Q1-6 κ and ψ(σ) | Accepted | κ rectangular 1.69, 3.24; circular 1.76, 3.60 added ([U] R5). Resulting factor 0.35 to 12 ([S] R22) |
| Q1-7 Zener damping | Accepted in form, numbers revised | f_Z = 340 Hz at 0.5 mm (was 380); maximum ψ_TE 1.21e-2 (was 1.4e-2), 2.0e-2 with α_s = 27e-6 /K ([S] R23; [4Q] §9). Relevant at 1 Hz for struts of 2 mm and more |
| Q1-8 E_s·ρ̄² wrong for octet | Accepted, extended | Also wrong for BCC by 11 to 12 ([4Q] §0) |
| Q2-1 strain control, E_s governs | Accepted; bending constant revised | C_b "0.75 to 1.5" becomes c = 0.64 to 1.29 for BCC equibiaxial over ρ̄ 0.1 to 0.4 ([4M] §4). Sheet TPMS factor not computed |
| Q2-2 lattice takes the mismatch; S small | Accepted with two revisions | S at equal thickness is 4.3e-4 to 0.093, not 0.01 to 0.16 ([M] R29). "Bending neglected, O(S)" understates it: the interface relief is (4 + 3·H_L/H_2)·S ([4M] §1) |
| Q2-3 peak location and decay | Not tested | No FE. Kept as stated, UNSURE |
| Q2-4 bimaterial strut, laminate | Accepted | 1/8 + 3/8 = 0.5 reproduced ([4M] §1) |
| Q2-5 butt joint | Not tested | Kept as stated, UNSURE |
| Q2-6 housing, hydrostatic | Accepted for octet and BCC | All struts at E_s·ε_m, zero bending in BCC ([U] R4, R7). Gyroid UNSURE |
| Q2-7 interlayer shear trap | Not tested | Magnitude only ([M] R32) |
| Q2-8 verdict formula | Revised | K_f becomes K_n (roughness is already in an as-built σ_w7). "Conservative by 1 to 4 for bending cells" becomes a margin of 0.78 to 1.56 ([4M] §4). Mean stress is a bound pair (claim 20). Validity rewritten (claim 4) |

## 5. Rows that are identities, not evidence

S2 marked these as true by construction. None is used as support above.

- R5: κ(2) = 1 for both sections.
- R8: collapse over bending-only first yield = 16/(3π).
- R14: implied σ_f' = 668 MPa for b = −0.1434.
- R14: fatigue-to-collapse ratio independent of ρ̄ for A, C [100], C [110].
- R17: strut-form Σ̇ for A (r² = 25 defines σ_rms).
- R18: S(N)/S(1e7) = (N/1e7)^(1+2b).
- R22: factor 1 at n_d = 2.
- R24: scaling of S with ψ, σ_w7², K_n^(−2), 1/E_s.
- R25: R = −1 returns R14.
- R27: ρ̄-independence of the fatigue to first-yield ratio.
- R32: γ/ε_m = L/(2·H_L).

Also not evidence of physics: the energy equalities R3 and R9 (they test the code on one linear model); the R19 grid-against-analytic and "A = C/25" checks; every regression line in the S4 outputs (they show the S4 scripts repeat S2).

## 6. Changed since plan

Each item: plan statement, what it is now, why.

1. **Inputs, σ_w7 (as-built).** 60 MPa (range 40 to 100) became 30 to 60 MPa. S3 found no source for 60; Aboulkhair 2016 allows about 31.5 MPa.
2. **Inputs, σ_u.** 400 MPa became 400 to 460 MPa. EOS reports 461 to 466 MPa. Effect: σ_f' 668 to 768 MPa, anchored b −0.143 to −0.193, Goodman factor 2.67 to 2.19.
3. **Inputs, α_s.** 21e-6 /K (20 to 23) became 21 to 27e-6 /K. Snippet value 26.6e-6 /K, build direction, as built.
4. **Inputs, LPBF energy.** 50 to 500 became 50 to 600 MJ/kg. Melt floor is 1.46e3 to 1.65e3 J/K because c_p is uncertain (739 to 922 J/(kg·K)).
5. **C3.** "Overstates by about 10" became 11.1 to 12.3 at ρ̄ = 0.2. Timoshenko shear lowers the BCC modulus by 9.6 %. The attribution of the closed forms to Ushijima 2011 is withdrawn (S3: may not say this).
6. **C4.** "Same ρ̄ exponent, no crossover in ρ̄" is exact for A and C only; for B the ratio drifts 4.1 % (0.139 to 0.133) because of the axial term. The crossover N_x ≈ 5e2 holds for the central curve only; N_x is below 100 cycles in 64 of 80 combinations, so first yield does not bind anywhere in the high-cycle range for those.
7. **C5.** Values now 0.23 to 4.0 MPa over cells and σ_w7. The ordering of cells is a model result only (Dallago 2018).
8. **C6.** B is a range, 6.74e-6 to 7.46e-6 W/K at 1 Hz (Timoshenko raises it 10.7 %).
9. **C9, C10.** 30-year values added (to 3.42e4 J/K); "below about 10 %" now reads 7.7 % against LPBF at 50 MJ/kg plus primary metal, and 38 % against LPBF at 50 MJ/kg alone. Verdict unchanged.
10. **C12.** Factor 0.2 to 6 became 0.35 to 12 for n_d ≤ 3 (the plan's hand range left out the octet at σ_ref = 5 MPa), and 0.14 to 144 if n_d = 4.
11. **C13.** Withdrawn as a cross-check on ψ. R21 shows the ratio runs from 1e-4 to 290 over N; equality at 1e7 is a coincidence of the inputs.
12. **C15.** Crossover of c = 1 at ρ̄ ≈ 0.20 became 0.227 (Euler–Bernoulli, numeric) to 0.309 (Timoshenko). The plan's range 0.19 to 0.23 is too narrow. The closed form 2.10·ρ̄^0.5 + 0.37·ρ̄ is 7 % high at ρ̄ = 0.2.
13. **Plan §0, Q2 claim 8 margin.** "About 0.7 to 1.4, non-conservative above ρ̄ ≈ 0.2" became c = 0.64 to 1.29, non-conservative above ρ̄ = 0.23 to 0.31.
14. **C16.** "S below about 0.1" holds at H_L = H_2 only (0.93 at H_L/H_2 = 10). New: 1/(1+S) is the flat-plate case; free bending relieves (4 + 3·H_L/H_2)·S at the interface.
15. **D10 and rows R28, R30, R31.** The expected values omitted S. Correct values with S: 21.41 and 64.23 MPa, 6.22e6 cycles, 124.1 K, 0.0399 J/K.
16. **C17.** "Not life-limiting for ΔT ≤ 50 K" became conditional on σ_w7 and K_n (0, 4 and 10 of 60 cases below 30 years for K_n = 1, 2, 3). The plan named Ti-6Al-4V the worst listed pair; Invar has the larger Δα. ΔT_x ≈ 120 K for K_n = 3 carries a notch-root range of 319 MPa, above σ_y.
17. **Elastic flag (R30, Q5 validity).** K_n·c·E_s·ε_m < σ_y was a validity limit; it is now a warning, and the limit is on the nominal strut range. At ΔT_x the old criterion depends on the S–N curve only, not on K_n.
18. **R30 bracket.** ΔT_x is closed form; values above 500 K (316L, copper, steel at K_n = 1) mean no limit, not a missing root.
19. **C18.** "Mean stress can reverse C17" became a bound pair. Goodman is the conservative end; de Krijger 2017 supports no mean-stress effect, Lietaert 2018 the opposite.
20. **C19.** 0.041 J/K became 0.0399 J/K with S, and up to 0.29 J/K over the widened grid.
21. **C21.** Burr 2020 removed from the local-stress group; Zargarian 2016 labelled FE, not test; Li 2012 unverified; Ahmadi 2018 against Amin Yavari 2015 stated as a disagreement.
22. **C22.** Weakened to "order of magnitude only". The reported spread is 0.15 to 0.6, the stress basis is unconfirmed, and the higher ratio for stretch cells is contradicted by Dallago 2018.
23. **C23.** As-built over machined ratio for AlSi10Mg 0.5 to 0.8 became 0.23 to 0.55.
24. **C26.** One as-built b (−0.1434) became a range (−0.143 to −0.193); the machined check value 135 MPa is 4 to 23 % above what S3 found.
25. **Plan §0, Zener damping.** "Matters near 20 to 400 Hz only" is revised: at 1 Hz it is 23 to 38 % of ψ for 2 mm struts and exceeds ψ for 5 mm struts.
26. **R12.** "Yield governs over the whole sweep" holds for ρ̄ ≥ 0.039; below that the octet strut buckles first. The prompt's range is not affected.
27. **R29.** Expected extremes 5e-4 and 0.09 are 4.3e-4 and 0.093 (rounding in the plan).
28. **Q5 life default.** k_peak from the lattice's measured static strength is now preferred over the cell table; no higher endurance ratio is credited to stretch cells.

## 7. Open points

1. **Gyroid.** The prompt names it first. No constant in this file applies to it (sheet or skeletal). Yan 2015 and Al-Ketan 2018 are the candidates; neither was read.
2. **Unit-cell FE.** Every constant for B and C comes from beam or pin-jointed models without node volume, fillets or boundary layers. The two beam theories differ by 9 to 16 % in c at ρ̄ = 0.2 to 0.4. All falsifiers of the Q1 and Q2 answers are FE runs that have not been made.
3. **σ_w7 and b of as-built AlSi10Mg thin struts at R = −1.** No source. This input moves life by two to three orders and the dissipation total by 4.
4. **K_n.** No derivation and no source. It is swept from 1 to 3. If σ_w7 comes from as-built struts, only the node notch remains in K_n.
5. **ψ of LPBF AlSi10Mg at 10 to 60 MPa, and its amplitude exponent.** No source at a stated stress amplitude. The 1 Hz stretch corner of the verdict depends on it.
6. **Stress basis of the reported endurance ratios** (σ_max or amplitude, over yield or plateau). Needs full text of Hrabe 2011, Amin Yavari 2013 and Bobbert 2017.
7. **Mean-stress rule for as-built lattices.** Goodman against no effect; the choice moves ΔT_x by 2.2 to 2.7.
8. **Stretch against bending cells in fatigue.** The model's advantage for the octet is untested; Dallago 2018 points against it for cubic-cell variants.
9. **Singular strut roots, corner cells, butt joints, interlayer shear** (Q2 claims 3, 5, 7). Not computed; a point stress is not defined at a bimaterial edge.
10. **Thermal lag.** Only the magnitude is given; no transient model.
11. **Which hysteretic entropy counts.** Claim 12 shows that most of it cannot be damage-related if Basquin holds, but the split between anelastic, thermoelastic and plastic parts is not quantified.
12. **The comparator.** The prompt's 1e3 to 1e5 J/K is below the LPBF and primary-metal terms found by S3. Claim 1 gives ratios against each; which one the comparison should use is the user's choice.
13. **α_s = 26.6e-6 /K (build direction, as built)** is one snippet without a temperature range. If it is not confirmed, the 27e-6 /K columns can be dropped.
14. **Reed formula on round struts** (claim 11): prefactors of f_Z and Δ_E are unverified for a circular section.
