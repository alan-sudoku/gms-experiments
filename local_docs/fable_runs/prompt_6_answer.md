# Prompt 6 answer (S4): combining degradation mechanisms (OQ-20)

Status: S4 finaliser output. Everything here is a claim at level `derived` (unverified). No measurement was used anywhere in this run, and agreement between S1, S2, S3 and S4 does not raise the level.

**Provenance.**
- Read: the Prompt 6 fenced block in `local_docs/fable_questions.md`; `prompt_6_plan.md`; every file in `prompt_6_code/outputs/` (`issues.md`, `row_status.md` and the row outputs); `prompt_6_citations.md`; the S4 brief. No spec file was read. No web search was made in S4.
- Written: `prompt_6_code/s4_b_sensitivity.py`, `prompt_6_code/s4_d5_d6_mismatch.py`, their stdout in `prompt_6_code/outputs/s4_b_sensitivity.txt` and `outputs/s4_d5_d6_mismatch.txt`, and this file. Both scripts restate the plan's formulas and reproduce the saved S2 values at b = −0.102 (37 comparison lines, all "reproduced") before changing an input. The S2 row set was not re-run. Nothing was committed.
- Order of sections: the prompt's output format ends with "Open points"; the brief asks for a final section "Changed since plan", so that follows it.

**How to read the numbers.** Every number carries a tag naming the script whose saved stdout contains it: tag `[c6]` means `prompt_6_code/c6_c7_worst_case.py` with output `outputs/c6_c7_worst_case.txt`. Tags: `[a1]` a1_a2_a3_multipliers, `[a4]` a4_a5_a12_simple, `[a6]` a6_arrhenius_dT, `[a7]` a7_a8_electrothermal, `[a9]` a9_drying, `[a11]` a11_concurrent_hysteresis, `[b1]` b1_b2_miner_vs_min, `[b3]` b3_damage_curve_extremes, `[b4]` b4_b5_concurrent, `[b6]` b6_b7_slopes, `[c1]` c1_c2_baseline, `[c3]` c3_c4_section_loss, `[c5]` c5_rk4_verify, `[c6]` c6_c7_worst_case, `[c8]` c8_lower_bound, `[c9]` c9_parabolic, `[c10]` c10_c11_environment, `[c12]` c12_c13_pits, `[c14]` c14_damage_curve, `[c15]` c15_displacement, `[c16]` c16_dnv_anchor, `[c17]` c17_nu_crit, `[d1]` d1_d2_paralinear, `[d3]` d3_d4_spallation, `[d5]` d5_d7_scale_thresholds, `[d6]` d6_scale_cracking, `[d8]` d8_breakaway, `[e1]` e1_cost_sensitivity, `[e2]` e2_verdict_error, `[e3]` e3_a10_shares, `[e4]` e4_cost_bound, `[e5]` e5_coupling_numbers, `[s4b]` s4_b_sensitivity, `[s4d]` s4_d5_d6_mismatch.

**Two values of b.** The Basquin exponent of 2024-T4 is not settled (plan −0.102; a secondary table −0.124; same σ_f′ = 900 MPa; the primary table was not read). Where a number depends on it, both values are given as "x / y" in that order. "Not recomputed" marks rows where only the direction and rough size are given.

**Evidence classes.** S2 flagged identity checks in 30 of 49 rows. They are counted as arithmetic, not as evidence. Each claim names its class:
- P: proved by algebra (a grid check then confirms the code only).
- N: two independent numerical routes agree on the same model (closed form against quadrature or ODE).
- B: a bound tested against the exact solution of the same model.
- X: two different models compared (rainflow against an idealised block; damage curve against Miner).
- A: arithmetic only (identity or single-pass evaluation).
- L: an input that S3 matched to an external source. U: an unsourced planner input.
No class is a test against measurement.

---

## 0. Verdict

1. **Rates.** Adding the rates is exact bookkeeping. The error of the current rule is that every term is evaluated at the pristine, isothermal state. The sum is then a lower bound at fixed duty and accelerating couplings, and the direction reverses or is undetermined in five named cases (M1.3). Keep the sum as the default, gated by coupling numbers (M4.1).
2. **Wearout.** The current rule (fatigue only, minimum over load cases, air S–N curve) is not acceptable as a default. Defects in order of size, as the factor by which life is overstated for the side the rule is applied to:
   - no wearout by recession: unbounded (F_cur ≥ ρ; 1554 at ρ = 1000, q = 9.804 `[c6]`);
   - air S–N curve in a saline environment: 154 / 97 at the planner's baseline, 36 to 459 / 24 to 290 across the planner's range `[s4b]`. This rests on an unsourced range, not on data. The one sourced anchor (welded steel, design code) gives 3 to 21 `[c16]`;
   - concurrent load cases treated separately: (1+s)^m = 2.5 / 2.2 at s = 0.1, 894 / 268 at s = 1 `[s4b]`, if load cases can act at the same time;
   - pitting of a passive alloy: at least 10 in the worked thin wall (perforation at 1.5 yr against 15 yr) `[s4b]`;
   - section loss raising the stress: at most 4.38 / 3.91 (wall) and 6.77 / 5.96 (round strut) relative to "minimum of separate mechanisms" `[s4b]`;
   - minimum instead of Miner over sequential cases: at most the number of load cases, and not invariant to how a spectrum is split into cases (M2.1).
   These do not multiply (M2.8).
3. **Per side.** Every coupling scales as 1/h₀, so ignoring couplings favours the thin-featured side: verdict error 5.65 / 5.14 at an embodied share of 1 and 3.58 / 3.26 at 0.5 for the worked pair `[s4b]`. A one-directional bound exists, but a robust "g is better" then needs a modelled cost ratio below 0.18 / 0.20 from section loss alone, and below 0.012 / 0.019 if the environment curve is unknown and applied to g only `[s4b]`. A third verdict class "undetermined" is needed.
4. **Defaults.** Rule R (rates) and Rule W (wearout life) of M4.1 and M4.2, with their reject list (M4.4). Rule W has no aluminium anchor in open data.
5. **Effect of the two open inputs.** The choice of b changes numbers by up to about 40 % (and one example's governing mode, M2.9) but changes neither the ranking above nor any default `[s4b]`. The corrected expansion mismatch tightens the scale-spallation gate for an aluminium substrate by a factor 4.4 at equal temperature change `[s4d]`; it changes one gate input, not the rule.

---

## 1. Claims

### M1: additivity of rates

**M1.1 Additivity is exact in form; the error is in the state at which each term is evaluated.**
Equation: Σ̇_total(t) = Σ_i Σ̇_i(S(t)) [W/K], S = (remaining section [m], scale thickness [m], part temperature [K], damage [–]); the current rule uses Σ_i Σ̇_i(S₀). Error to first order: Σ_i Σ_j (∂Σ̇_i/∂S_j)·ΔS_j.
Confidence: high. Evidence: argument (entropy production as a sum of flux-times-force products); rows A1, A7, A8 confirm numerics only (N).
Falsifier: a coupled case where the total differs from the sum of terms evaluated at the coupled state.

**M1.2 The sum double-counts when Σ̇_op comes from a boundary power balance that already contains hysteresis or Joule terms. Counting reaction heat once (inside b_degrad) is right, and that heat is negligible as self-heating.**
Equation: q″ = r·(ρ_m/M)·ΔH [W/m²]; ΔT = q″/h_c [K]. At r = 10 µm/yr: q″ = 0.0274 W/m², ΔT ≤ 5.5e-3 K for h_c ≥ 5 W/(m²·K) `[a4]`.
Confidence: high. Evidence: A.
Falsifier: ΔT above 0.1 K for any corrosion rate in the model's range.

**M1.3 At fixed duty with monotone degradation the pristine-state sum is a lower bound on the true total. The direction reverses or is not fixed in five cases:** constant-voltage operation; wall recession that widens a flow channel at fixed mass flow; displacement-controlled cyclic loading; self-heating that dries a surface in atmospheric corrosion; and (added in S4) rate-independent hysteresis under concurrent load cases, where the sign depends on phase (M1.6).
Equation: multiplier (1 − x_e) for constant voltage; (1 + 2h/D)^(−k), k = 5 turbulent, 4 laminar, for channel widening: 0.402 at D = 1 mm, h = 100 µm; adherent scale narrowing: 3.33 (PBR 2.07), 1.33 (PBR 1.28) `[a4]`.
Confidence: high for the fixed-duty direction; medium that the list is complete. Evidence: A (the Pilling–Bedworth ratios are unsourced, U).
Falsifier: any fixed-duty, accelerating coupling with a multiplier below 1.

**M1.4 Section thinning and series resistances.** A rate that scales as (1 − x)^(−p) has a life-averaged multiplier M.
Equation: linear recession, M_lin = [(1 − x_e)^(1−p) − 1]/((p − 1)·x_e), p ≠ 1; −ln(1 − x_e)/x_e, p = 1. Parabolic recession, p = 1: M_par = −2·(a + ln(1 − a))/a², a = x_e. Series resistance at fixed duty: 1 + R_f/R₀ (heat transfer: 1 + R_f·U_clean, R_f in m²·K/W). Exponents: Joule heating at constant current, p = 1 (wall), 2 (round wire); hysteresis under load control with D_s = J·σ_a^n, p = n − 1 (wall), 2n − 2 (round strut). Added in S4: the corrosion term itself goes as the exposed area, so p = −1 for a round strut and 0 for a wall attacked on its faces.
Numbers: 5 % error at x_e = 0.0937 (linear, p = 1), 0.0476 (p = 2), 0.0240 (p = 4); 0.0710 (parabolic, p = 1), 0.0360 (p = 2) `[a1]`. So the gate is about 0.095/p for linear and 0.07/p for parabolic recession.
Confidence: high (mathematics); medium (exponents). Evidence: N (closed form against Simpson, max relative difference 5.3e-10 `[a1]`).
Falsifier: a measured resistance or dissipation history of a thinning conductor that departs from (1 − x)^(−p) at fixed duty.

**M1.5 Hysteresis rising with damage is a bounded multiplier on one term.**
Equation: ψ = ψ₀·(1 + β·D^γ) gives a life-average factor 1 + β/(γ + 1); effect on the total 1 + w_fat·β/(γ + 1).
Numbers: the fatigue-hysteresis share of the worked strut is 0.100 / 0.043, so β = 5, γ = 1 changes the total by a factor 1.25 / 1.11 `[s4b]`.
Confidence: high (form), low (magnitude: no anchor for β, γ; ψ = 2e-3 is unsourced; the embodied input was confirmed by S3 as an energy figure, not an exergy figure). Evidence: A.
Falsifier: measured ψ(N/N_f) with a life-average factor outside [1, 1 + β_max].

**M1.6 (revised) Summing hysteresis over load cases is exact for linear (viscoelastic) damping at distinct frequencies and for sequential cases. For rate-independent hysteresis under concurrent cases the separate sum is neither an upper nor a lower bound.**
Equation: Σ̇_fat = (1/T₀)·V·J·Σ_k σ_a,k^n per unit time, summed over the rainflow cycles k of the combined history [W/K]. Upper bound: Σ̇_fat ≤ ν_max·V·J·(Σ_l σ_l)^n/T₀. Same frequency, in phase: ratio to the separate sum (1 + s)^n/(1 + s^n).
Numbers `[a11]`: rainflow/separate sum from 0.70 to 1.84 over n = 2, 3; φ = 3, 9, 33; s = 0.1, 1/3, 1. For n = 2 and φ = 9, 33: 1.00 to 1.11. For φ = 1 in phase: up to 2 (n = 2) and 4 (n = 3). The upper bound held in 24 of 24 cases (it is loose: up to 42.5 times the rainflow value).
Decision on the failed check (work item 4): both the claim and the test were at fault.
- The plan's idealised block (one cycle at σ₁ + σ₂ plus φ − 1 cycles at σ₂) is wrong as an estimate. Rainflow closes fewer and smaller fast cycles on the flanks of the slow wave (one cycle at φ = 3, s = 0.1; five at φ = 9, s = 0.1). The idealised ratio was at or above the rainflow ratio in all 24 cases, by up to 65.5 %. The plan's "maximum 1 + 1/√φ at s = 1/√φ" is withdrawn (1.33 claimed at φ = 9, s = 1/3; rainflow gives 1.085).
- The φ = 3 cases were mis-posed for a formula that assumes aligned peaks: with both sines at zero phase and φ = 3, the fast trough sits on the slow crest, the largest cycle is smaller than σ₁ alone, and the ratio falls below 1 (0.70 to 0.89 for n = 2). That result is correct for that phase, and it shows the plan's "more than the sum" was wrong as a general statement.
Consequence: with the fatigue share at 0.04 to 0.10 the effect on the total is about 1 % for n = 2 at well separated frequencies; it matters only for same-frequency in-phase loads or n ≥ 3.
Confidence: medium. Evidence: X for the range; B for the upper bound; the viscoelastic part is an identity (A).
Falsifier: a rainflow dissipation above ν_max·V·J·(Σσ_l)^n/T₀; or measured loop areas under two-frequency loading outside the rainflow prediction.

**M1.7 Scale loss. The pure parabolic law is a lower bound on metal consumed whenever scale is lost; parabolic + linear is an upper bound; max(parabolic, linear) is a lower bound.**
Equation (Tedmon form): dδ/dt = k_p′/δ − k_l [m/s]; metal consumed m(t) = δ(t) + k_l·t; with θ = k_l²·t/k_p′: max(√(2θ), θ) ≤ m̃ ≤ √(2θ) + θ.
Numbers: the sum overstates by at most 1.369 (at θ = 3.32); the max understates by at most 1.474 (at θ = 2); both bounds held at all 161 grid points `[d1]`. Periodic complete spallation: parabolic low by √N, sum high by 1 + 1/√N; inequalities held at 100 001 grid points `[d3]`. Breakaway to a linear rate κ times the parabolic rate at onset: 1.74 (κ = 1) and 14.5 (κ = 10) times the parabolic loss at ten times the onset time `[d8]`.
Confidence: high (bounds within the two models), medium (that either model describes a given scale). Evidence: B. Both bounds fail if the regrown scale is less protective than the first.
Falsifier: a paralinear data set with metal loss above parabolic + linear at fitted constants.

**M1.8 (revised) Criteria for scale spallation and cracking, with the substrate's own expansion mismatch.**
Equation: δ_c = G_c·(1 − ν_ox)/(E_ox·ε²) [m], ε = Δα·ΔT + ε_mech; ε_c = K_Ic/(f·E_ox·√(π·c)), f = 1.12; reject parabolic kinetics when the scale exceeds δ_c or the strain the scale sees exceeds ε_c.
Restated D5 `[s4d]`: Δα = 7e-6 /K is right for a Ni-base or Fe–Cr substrate and the S2 table stands for those (δ_c = 0.20 µm at G_c = 5 J/m², ΔT = 1000 K; 0.81 µm at 500 K). For an aluminium alloy against alumina Δα = 14.7e-6 /K: at equal ΔT the mismatch strain and stress are 2.10 times larger, δ_c is 4.41 times smaller and the time to reach it 19.5 times shorter. Example, G_c = 5 J/m²: δ_c = 1.14 µm at ΔT = 200 K (5.03 µm with the plan's value), 4.57 µm at 100 K. The ΔT = 500 and 1000 K columns do not apply to an aluminium alloy (above its solidus; memory, UNSURE).
Restated D6 `[s4d]`: cyclic strain amplitude ε_a = 1.49e-3 / 0.94e-3; crossover flaw size for K_Ic = 1 MPa√m: 0.79 / 1.97 µm. For aluminium the thermal mismatch strain equals ε_a at ΔT = 101 / 64 K, so the criterion must use ε_a + Δα·ΔT; at ΔT = 100 K the crossover falls to 0.20 / 0.30 µm.
What survives: a 10 nm native film has ε_c ≥ 6.6e-3, above the largest strain in the aluminium table (4.4e-3), so on this model a native film on aluminium is not cracked by either strain. What changes: any alumina layer of micrometre thickness on aluminium (thermal, anodic or sprayed; the last two are my examples, UNSURE) fails the gate at a temperature change of order 100 to 200 K, not 500 K.
Confidence: medium (form), low (inputs: G_c, K_Ic, E_ox, ν_ox are unsourced grids; the cited sources were not seen to contain these forms). Evidence: A.
Falsifier: published critical strains for alumina scales outside 1e-3 to 1e-2; spallation thickness on a known substrate off the δ_c line by more than the G_c range.

**M1.9 Temperature coupling.**
Equation: T = T_env + R_th·P(T, x); rate multiplier exp[(Q/R)·(1/T_env − 1/T)]; adequacy to ε when ΔT < T²·c/(1 − T·c), c = R·ln(1 + ε)/Q. Electro-thermal loop at constant current: ΔT = ΔT₀/(1 − x − α·ΔT₀), runaway at x = 1 − α·ΔT₀.
Numbers: 5 % at ΔT = 0.73 K (Q = 50 kJ/mol, 300 K) and 2.93 K (200 kJ/mol, 1200 K) `[a6]`. Time to lose half the section relative to isothermal: 0.639 (ΔT₀ = 5 K), 0.193 (20 K); with α = 0.004 /K: 0.631, 0.162; runaway section loss 0.80 at ΔT₀ = 50 K `[a7]`.
Confidence: high (form), medium (numbers; α is unconfirmed, U). Evidence: N. If the model prescribes the part temperature, not the environment temperature, the coupling is already included; which one GMS uses was not read (UNSURE).
Falsifier: an Arrhenius-rate measurement on a self-heated part that matches the environment-temperature rate.

**M1.10 For wet-film (atmospheric) corrosion the Arrhenius direction can be wrong: modest self-heating dries the surface.**
Equation: RH_s = RH_amb·p_sat(T_env)/p_sat(T_env + ΔT), Magnus form for p_sat.
Numbers: 2.81 K takes a surface at 20 °C from 95 % to 80 %; 3.65 K from 100 % to 80 %; 8.52 K from 100 % to 60 % `[a9]`.
Confidence: medium (the 80 % threshold was not confirmed, U; the Magnus coefficients were, L). Evidence: N.
Falsifier: corrosion rate of a self-heated specimen in humid air not falling when the surface humidity crosses the threshold.

**M1.11 (revised) Summing K_ox over surface patches is exact only if all patches share one clock and one temperature. It is low when patches are renewed at different times.**
Equation: fraction F_A spalling per interval Δt, patches in rotation: long-run recession rate √(2·k_p·F_A/Δt) [m/s].
Numbers `[d3]`: the ensemble is 1.33 times the parabolic law at t = n₀·Δt (n₀ = 1/F_A), 3.27 at 10·n₀·Δt, 10.03 at 100·n₀·Δt. The plan's "crossover with the parabolic law at t = n₀·Δt" is wrong: only the asymptote crosses there; the ensemble is already 33 % above.
Confidence: high (direction), medium (the patch model). Evidence: A (the slope ratio is by construction).
Falsifier: cyclic-oxidation mass data with long-run slope differing from √(2·k_p·F_A/Δt) at independently measured F_A.

**M1.12 (revised) Adequacy criterion.**
Equation: the pristine-state model is adequate to ε when c_true/c_model − 1 = w_emb·(F − 1) + w_ox·(√F − 1) + Σ_i w_i·(M_i − 1) ≤ ε, shares w at the modelled life, F the life overstatement (exact form of M2.5), M_i the multiplier of rate i (M1.4, M1.9). First-order screens: p_i·x_e/2 for a rate; Q·ΔT/(R·T²) for self-heating; q·ρ/2 for life.
Numbers: first-order rate error against exact: 0.0212 / 0.0218 (s), 0.150 / 0.177 (g). First-order life error against exact: 0.259 / 0.244 (s, ρ = 0.053); 10.4 / 6.03 (g, ρ = 1.06), wrong by 72 % `[e5]`. So q·ρ/2 may be used only as a screen (ignore section loss below 0.05); above that the closed form is required.
Definition of the weighted sum (work item 8): the plan's computation spec did not define it. S2 used corrosion share × the p = 2 rate error + embodied share × life error (4.18 exact) `[e5]`. I use the cost form above, with the p = 2 error on the hysteresis share and p = −1 on the corrosion share of a round strut: 4.14 / 3.78, of which the embodied-life term is 4.14 / 3.79 `[s4b]`. The two readings differ by 1 %, because the life term dominates. Any document that adopts this criterion must define the sum; it is not defined anywhere I read.
Confidence: medium. Evidence: A; the first-order comparison is on the worked pair only (in-sample, see M4).
Falsifier: a case with x_e ≤ 0.1 where the first-order rate estimate misses the exact multiplier error by more than 30 %.

### M2: wearout under several mechanisms

**M2.1 (extended) Sequential load cases: τ_Miner ≤ τ_min ≤ L·τ_Miner. The minimum is never conservative, is off by at most the number of load cases L, and is not a well-posed rule for a spectrum.**
Equation: τ_l = N_l/ν_l [s]; 1/τ_Miner = Σ_l 1/τ_l; τ_min/τ_Miner ∈ [1, L].
Added in S4: τ_min depends on how the load history is split into cases. Splitting one case into two identical halves (each with half the cycle rate) doubles τ_min and leaves τ_Miner unchanged. A rule whose result changes under a relabelling of the same loading cannot be a default.
Numbers `[b1]`: the ratio stayed in [1, L] in every sample. For L cases with stress amplitudes within ±5 % (log-uniform) the median ratio is 1.75 (L = 2), 3.74 (L = 5), 13.3 (L = 20).
Confidence: high. Evidence: P.
Falsifier: none within the algebra; the open question is which accumulation rule is physically right (M2.4).

**M2.2 (qualified) For two cases of distinct severity the Miner–minimum gap is small, because S–N curves are steep; for many cases of similar severity it approaches L.**
Equation: the ratio exceeds 1.1 only when (s/s*)^m ∈ [0.1, 10], s* = φ^(−1/m).
Numbers: window in s/s*: [0.791, 1.265] / [0.752, 1.331] `[s4b]`; see M2.1 for the many-case medians.
Confidence: high. Evidence: P, N.
Falsifier: as M2.1.

**M2.3 (extended) Concurrent load cases: the minimum and Miner-over-cases are both non-conservative, by up to about (1 + s)^m relative to the dominant case alone.** The damaging cycle is the envelope cycle of the combined history, so cycle counting on the combined history is required.
Equation: damage per slow period d ≈ 1/N(σ₁ + σ₂) + (φ − 1)/N(σ₂); τ = 1/(ν₁·d).
Numbers: (1 + s)^m = 2.55 / 2.16 (s = 0.1), 5.97 / 4.35 (s = 0.2), 894 / 268 (s = 1) `[s4b]`. Rainflow damage is 0.905 to 1.000 of the block value over 30 cases (b = −0.102); a mean-stress correction raises it by up to 1.78 `[b4]`.
Added in S4: (1 + s)^m is the worst-phase value. S2 tested aligned and even frequency ratios only. For a low frequency ratio with opposed phase the envelope is smaller than σ₁ + σ₂ (seen in `[a11]` at φ = 3), so the factor is an upper value, approached for any phase as φ grows (largest amplitude 0.9999 of σ₁ + σ₂ at φ = 128 `[b4]`).
Confidence: high (mathematics), medium (applicability: whether GMS-220 load cases can act at the same time was not read). Evidence: X.
Falsifier: variable-amplitude test lives under two-frequency loading within 20 % of the separate-case Miner prediction at s = 0.2.

**M2.4 Miner itself is uncertain by a factor of about 3 to 5 under step loading.**
Equation (damage-curve approach): Miner sum at failure f(u) = u + 1 − u^a, a = (N₁/N₂)^0.4, u = n₁/N₁.
Numbers: 0.673 to 1.327 (life ratio 10), 0.405 to 1.595 (100), 0.222 to 1.778 (1000); high-then-low is the non-conservative order `[b3]`.
Confidence: medium. Evidence: N on the formula; the exponent form (N₁/N₂)^0.4 was not seen in the source by S3; the allowable sum 0.3 is supported by secondary sources only, and 0.5 by a calculator site only.
Falsifier: two-level test data with sums far outside the band.

**M2.5 Section loss under load control. With linear recession and Miner accumulation the coupled life has a closed form.**
Equation: σ_a(t) = σ_a0·(1 − t/t_c)^(−p); t_c = h₀/(n_s·r) (wall) or d₀/(2r) (round strut) [s]; ρ = τ₀/t_c; q = p·m; **τ_c = t_c·{1 − [1 + (q − 1)·ρ]^(−1/(q−1))}**. F_min = min(τ₀, t_c)/τ_c has its maximum 1/(1 − q^(−1/(q−1))) at ρ = 1.
Numbers: maximum 4.38 / 3.91 (wall, q = m) and 6.77 / 5.96 (round strut, q = 2m) `[s4b]`. With an allowable section loss x_allow the maximum sits at ρ = x_allow: 1.84 (0.2), 2.87 (0.5), 3.79 (0.8) for q = 9.804; 2.50, 4.24, 5.79 for q = 19.608 `[c6]` (b = −0.102 only; about 10 % lower for b = −0.124, not recomputed). Parabolic recession: F_min = 1.70, 3.53, 11.7, 5.60 at ρ = 0.01, 0.1, 1, 10 (q = 9.804) and 25.5 at ρ = 1 (q = 19.608) `[c9]`; this is the largest of four ρ values, not a located maximum, and was not recomputed for b = −0.124 (lower).
Limits of the sweeps (work item 5): the maxima are maxima over ρ ∈ [1e-3, 1e3] only. For three (q, x_allow) pairs the point ρ₁ above which the recession cap alone governs (closed form 1.6e5, 2.1e4, 5.5e11) lies outside even the extended sweep [1e-4, 1e4]; for those pairs the statement "F_min = 1 for ρ ≥ ρ₁" is closed-form only, and what the sweep supports is that F_min stays above 1 throughout the swept range `[c6]`.
Confidence: high (closed form), medium (Miner under continuously rising stress, see M2.10). Evidence: N (RK4 against the closed form to 1e-9 `[c5]`; same ODE).
Falsifier: fatigue life of thin specimens corroding at a known rate under load control that exceeds min(τ₀, t_c)/F_min by more than the S–N scatter.

**M2.6 The current rule (fatigue only; recession not modelled) is worse than "minimum of separate mechanisms": its error is unbounded.**
Equation: F_cur = τ₀/τ_c = ρ/(1 − [1 + (q − 1)·ρ]^(−1/(q−1))) ≥ ρ.
Numbers: F_cur/ρ = 1.554 at ρ = 1000, q = 9.804 `[c6]`; 0.3 mm strut at 0.1 Hz and 10 µm/yr: F_cur = 42.7 while F_min = 4.04 `[c3]`.
Confidence: high. Evidence: P.
Falsifier: none within the model; a lightly stressed thin feature that outlives h₀/(n_s·r) would refute the recession model itself.

**M2.7 (revised) An environment-modified S–N curve is probably the largest finite effect, but for aluminium its size rests on an unsourced range.**
Equation: σ_env(N) through σ_env(1e5) = k₅·σ_air(1e5) and σ_env(1e8) = k₈·σ_air(1e8); b_env = log₁₀[σ_env(1e8)/σ_env(1e5)]/3; F_env = N_air(σ)/N_env(σ).
Numbers `[s4b]`: at the stress equal to the air strength at 5e8 cycles and (k₅, k₈) = (0.9, 0.4): F_env = 154 / 97. Across the planner's range (k₅ 0.8 to 1.0, k₈ 0.25 to 0.6): 36 to 459 / 24 to 290.
Status of the inputs (work item 3): no open source gives k₅ or k₈. S3 found figures only (not read), and one secondary statement ("3 to 4 times lower in seawater", R = 0, cycle count not stated) that would put k₈ near 0.25 to 0.33 if it referred to 1e8 cycles. So 154 is the planner's range, not data. Sensitivity that decides something: F_env stays above the section-loss maximum for every point of the range (lowest 36 / 24 against 6.77 / 5.96); it would fall to the section-loss maximum only at k₈ = 0.82 / 0.80, outside the range. The ranking in the verdict therefore survives the range but not an arbitrary k₈.
Sourced anchor (welded steel, design code, constants matched by S3): free corrosion against air 3.0 at and above 52.63 MPa, 5.2 at 40 MPa, 9.2 at 30 MPa, 20.7 at 20 MPa `[c16]`; the factor 3.0 is the ratio of two tabulated constants.
Limits of the sweep (work item 5): F_env rises monotonically as stress falls, so the sweep [100, 400] MPa has no interior maximum and no worst case can be claimed; "unbounded as stress falls" is a property of the two-line construction. Two crossovers of the air and environment curves (447.6 and 486.7 MPa) lie outside the sweep; they are extrapolations of two power laws to stresses where Basquin does not apply, and nothing is claimed from them. The plan's "for k₅ < 1 the crossing is below 1e5 cycles" holds only for k₈ < k₅; for k₈ = 1 the construction crosses at 1e8 cycles and gives F_env < 1 at the baseline stress `[c10]`, an artefact.
Humid air against laboratory air: no number; the plan's "small" is unverified.
Confidence: medium (direction), low (size for aluminium). Evidence: U for aluminium; L for the steel code.
Falsifier: a paired air and saline S–N set for a 2xxx or 7xxx alloy with k₈ > 0.8.

**M2.8 The effects do not multiply.** Once the environment curve is used the life is short and section loss adds little, except at low frequency or in very thin sections.
Numbers: 0.3 mm wall attacked on both sides at 10 µm/yr, extra factor 2.34 / 2.88 (0.01 Hz), 1.15 / 1.22 (0.1 Hz), 1.016 / 1.022 (1 Hz) `[s4b]`. On the full geometry grid 7 of 27 cases stay below 1.05 down to 0.01 Hz `[c10]` (b = −0.102).
Confidence: medium, conditional on the range of M2.7. Evidence: A.
Falsifier: corrosion-fatigue lives of thin specimens at 1 Hz shorter than the environment S–N prediction by more than 1.1.

**M2.9 (revised) For a passive alloy, localised attack governs a thin feature, either as pit-initiated fatigue or as perforation; which of the two is not decided by the available inputs. Perforation is the robust cap.**
Equation: pit as a crack-like defect: a₀ = (1/π)·(ΔK_th/(Y·2σ_a0))² [m]; knockdown K(a) = √(a₀/(a₀ + a)); life factor K^(−m); linear pit growth a = PF·r·t: τ = t_a·{[1 + (m/2 + 1)·τ₀/t_a]^(1/(m/2+1)) − 1}, t_a = a₀/(PF·r); perforation t_perf = h₀/(n_s·PF·r).
Numbers `[s4b]`: a₀ = 119 / 297 µm (ΔK_th = 3 MPa√m); life factor of a 100 µm pit 19.8 / 3.2; worked wall (0.3 mm, both sides, PF = 10, r = 10 µm/yr, 1 Hz): pit-initiated fatigue at 1.31 / 2.78 yr against perforation at 1.50 yr, so fatigue governs for b = −0.102 and perforation for b = −0.124. Either way the life is at most 1.5 yr against min(τ₀, t_c) = 15 yr: a factor of at least 10.
Cube-root pit growth (work item 6): the plan expected a longer life than linear growth for lives above 1 yr. S2 found the opposite at PF = 10, r = 10 (1.19 against 1.31 yr) `[c12]`. The expectation was wrong, not the computation: the two laws are matched at 1 yr, the cube-root pit is deeper before 1 yr, and damage is an integral over the whole history, so the break-even life is later than 1 yr (between 1.3 and 2.9 yr of linear-law life on this grid; not located). The direction also depends on the arbitrary 1 yr matching time. The comparison is inconsistent in one respect: S2's perforation time uses the linear law for both.
Status: the pit-depth data (L06) have no open source; a secondary report of 6 to 8 for pre-pitted 7075-T6 `[issues.md, C12]` lies between the two computed factors, which is not a confirmation.
Confidence: low to medium. Evidence: N on the formulas; U on PF, ΔK_th (S3: about 3 MPa√m for 2024-T3, within range) and the growth law.
Falsifier: pre-pitted fatigue data with life factors below 2 for 100 µm pits.

**M2.10 (revised) "Minimum of separate mechanisms" is not always non-conservative.** It is conservative or neutral when: (i) loading is displacement-controlled; (ii) Basquin is used without an endurance limit in a benign environment; (iii) stress rises monotonically and accumulation is nonlinear; (iv) dissolution outruns short cracks; (v) oxide-induced closure raises the near-threshold resistance; (vi) the separate lives came from design curves.
Equation (i): σ_a ∝ (1 − x)^(+1): fatigue fails only if ρ < ρ* = 1/(m + 1); then τ = t_c·{1 − [1 − (m + 1)·ρ]^(1/(m+1))} > τ₀.
Numbers: ρ* = 0.0926 / 0.110 `[s4b]`; τ/τ₀ = 1.053 (ρ = 0.01), 1.388 (0.05) `[c15]`. (ii) Extension against a cut-off, m = 12: 3.54 at 0.9 of the endurance stress, 4096 at 0.5 `[b6]`. (iii) Revised: the damage-curve life is 1.009, 1.054, 1.081, 1.050 times the Miner closed form at ρ = 0.01, 0.1, 1, 10 `[c14]`, so the gain is 1 to 8 %, not the "up to about 1.8" of the plan (that figure is a Miner sum under step loading, not a life ratio under smoothly rising stress); b = −0.102 only, four ρ values, not recomputed. (iv) ν below 3.2e-4 to 3.2e-3 Hz for 1 to 10 µm/yr `[c17]`.
Null case of C14 (work item 7): decided. With q = 0 the nonlinear term is multiplied by zero and t_c drops out of the equation, so the life is τ₀ for every ρ; the two "undecided" cases (ρ = 1, 10) are an artefact of an integration limit at t_c that has no meaning when q = 0. The null case therefore passes, but it is an identity and tests only the event logic, not the damage-curve term. The test that would exercise that term is a smoothed two-level step compared with the closed-form sums of M2.4; it was not run.
Confidence: high (i), (ii); medium (iii); low (iv), (v) (the closure source concerns steels).
Falsifier: a displacement-controlled corroding specimen failing earlier than τ₀.

**M2.11 Screening rule for τ_wearout.**
Equation: τ_M = [Σ_l ν_l/N_l]⁻¹ from an S–N curve valid for the service environment, after cycle counting if cases are concurrent; τ_wearout = min(τ_c(τ_M, t_c, q), x_allow·t_c, t_perf). Ignore section loss when q·τ_M/(2·t_c) < 0.05. Bounds: τ_LB = x*·t_c ≤ τ_c ≤ min(τ_M, t_c), x* the root of x = ρ·(1 − x)^q.
Numbers: τ_LB/τ_c between 0.727 and 0.998 over ρ ∈ [1e-3, 1e3] for q = 4.56, 9.80, 19.61; minima 0.736, 0.730, 0.727, interior `[c8]`.
Confidence: medium. Evidence: B (the lower bound held at all 363 grid points). The t_perf term is added in S4 (M2.9).
Falsifier: any (ρ, q) with τ_LB above τ_c.

**M2.12 (flagged) Oxidation-assisted initiation gives a time-based cap independent of cycle count.**
Equation: t_i = a_tr²/(2·k_p′) [s], a_tr = (1/π)·(ΔK_th/(Y·Δσ))² [m].
Numbers: a_tr = 39.6 µm, t_i = 7.86e6 s (91 d) for k_p′ = 1e-16 m²/s, Δσ = 400 MPa, ΔK_th = 5 MPa√m, Y = 1.12 `[d5]`. Flag: Y = 1.12 is the edge-crack factor; with the semicircular factor 0.713 used elsewhere, t_i would be about 6 times longer (Y^(−4); not recomputed). ΔK_th = 5 MPa√m is unsourced.
Confidence: low. Evidence: A.
Falsifier: high-temperature fatigue data where initiation life does not scale with 1/k_p′.

### M3: direction of error per side

**M3.1 A life error matters through the embodied (replacement) share.**
Equation: c_true/c_model = w_emb·F + w_ox·√F + w_lin·M, with w_emb + w_ox + w_lin = 1 at the modelled life.
Numbers: w_emb = 0.5, F = 4.4: 2.70; F = 150: 75.5 `[e1]`.
Confidence: high, conditional on the cost form (embodied + K_ox·√τ + ∫rates)/τ, which was inferred from the prompt and not read in the spec (UNSURE). Evidence: A.
Falsifier: the spec's cost function having a different dependence on τ.

**M3.2 (one row added) Direction table.** "Understates" means the simplification makes the side it is applied to look cheaper; it is non-conservative for "g is better" when it understates g or overstates s.

| # | Simplification | Effect on that side's cost | Size | Lower bound | Upper bound |
|---|---|---|---|---|---|
| 1 | Rates at pristine state, fixed duty | understates | (1 − x_e)^(−p) at end of life | pristine value | end-of-life value |
| 2 | Same, constant voltage or channel widening | overstates | (1 − x_e)^(+1) etc. | end-of-life value | pristine value |
| 3 | Paralinear sum | overstates | ≤ 1.37 (Tedmon), ≤ 2 (spall) | max(parabolic, linear) | the sum |
| 4 | Parabolic only, scale lost | understates | √N | parabolic law | needs loss rate or spall interval |
| 5 | Minimum over sequential cases | understates | ≤ L on life | min rule | Miner with a reduced sum |
| 6 | Concurrent cases treated separately (life) | understates | up to (1 + s)^m | separate treatment | envelope amplitude Σσ_l at ν_max |
| 6b | Concurrent cases, hysteresis rate summed (new) | either sign | 0.70 to 1.84 on the grid; 2 to 4 in phase | none general | ν_max·V·J·(Σσ_l)^n/T₀ |
| 7 | Air S–N curve in an aggressive environment | understates | 24 to 459 on unsourced inputs; unbounded with a fatigue limit | air curve | needs environment S–N data |
| 8 | No section-loss coupling | understates | ≤ 1/(1 − q^(−1/(q−1))) | min(τ_M, t_c) | τ_LB |
| 9 | No recession wearout | understates | unbounded | none | x_allow·t_c |
| 10 | Uniform rate for a pitting alloy | understates | about PF on recession life | uniform rate | needs PF |
| 11 | Basquin without endurance limit, benign environment | overstates | unbounded | Basquin extension | cut-off curve |
| 12 | Displacement control treated as load control | overstates | see M2.10 | load-control life | recession life |
| 13 | Isothermal, high-temperature oxidation | understates | exp[Q·ΔT/(R·T²)] | isothermal | needs R_th and P |
| 14 | Isothermal, wet-film corrosion with self-heating | overstates | up to total | zero if dried | isothermal |
| 15 | Constant ψ | understates | 1 + β/(γ + 1) | constant ψ | needs β |
| 16 | Miner under smoothly rising stress | overstates slightly | 1 to 8 % on life | Miner closed form | none needed |
| 17 | Reaction heat counted once | exact | none | none | none |
| 18 | Σ̇_op from a boundary balance plus component terms | overstates | the duplicated term | subtract duplicate | none |

Confidence: medium. Evidence: the signs of rows 1, 2, 3, 8, 12, 14, 16 were computed (`[a1]`, `[a4]`, `[d1]`, `[c8]`, `[c15]`, `[a9]`, `[c14]`); the rest are argued.
Falsifier: any computed row with the opposite sign.

**M3.3 (revised) Ignoring couplings favours the side with thinner features.** If g is the thin-featured side (an assumption), the current rule is non-conservative for "g is better".
Numbers `[s4b]`, worked pair (g: 0.3 mm round strut; s: 3 mm wall attacked on one side; same alloy and stress; 10 µm/yr; 1 Hz): life overstated by 7.03 / 6.19 for g and 1.244 / 1.203 for s; cost ratio g/s understated by 5.65 / 5.14 (w_emb = 1), 3.58 / 3.26 (0.5), 1.57 / 1.49 (0.1), and 4.40 / 4.17 at the computed embodied share 0.686 / 0.730.
Added in S4: this asymmetry is the air-curve figure. If the same environment S–N curve is applied to both sides at 1 Hz, the remaining section-loss factors are 1.031 (g) and 1.0008 (s) `[c10]`, so the bias falls to about 3 %. The thin side then remains exposed through perforation (t_perf ∝ h₀/n_s) and through low-frequency duty (M2.8). The worked g case also sits at ρ = 1.06, next to the worst case ρ = 1, by the choice of 1 Hz, 0.3 mm and 10 µm/yr; at 1 µm/yr the same strut has F_cur = 1.86 `[c3]`.
Confidence: medium. Evidence: A.
Falsifier: a pair of geometries with equal surface-to-section ratio showing a verdict error far from 1.

**M3.4 A one-directional bound construction exists but is conditional.** Lower bound on cost (use for s): pristine-state rates, life = min(τ_M, t_c), oxidation = max(parabolic, linear). Upper bound (use for g): end-of-life rates, life = τ_LB with an environment S–N curve and a reduced damage sum, oxidation = parabolic + linear, hysteresis under concurrent loads at ν_max·V·J·(Σσ_l)^n/T₀. Valid only where each coupling is monotone-accelerating; for the cases of M1.3 the ends swap. Without environment data (S–N in environment, pitting factor, spall onset) no finite upper bound exists, and the model must return "undetermined".
Numbers: the bound exceeded the exact modelled cost in all 12 share cases for the single g unit; bound/exact = 1.35 at w_emb = 0.5 `[e4]`, `[s4b]`.
Confidence: medium. Evidence: B on one case.
Falsifier: τ_LB above τ_c; a sign-reversal case not in M1.3.

**M3.5 Common-mode errors cancel only partly.** A knockdown shared by both sides cancels in the ratio only if both sides have the same shares and the same h₀ (M3.3 shows the non-cancelling case).
Confidence: medium. Evidence: A.
Falsifier: as M3.3.

**M3.6 (revised) The bound is loose for thin features, and without environment data it is useless.**
Equation: c_U/c_model = w_emb·(τ₀/τ_LB) + w_ox·√(τ₀/τ_LB) + w_lin·(1 − τ_c/t_c)^(−p_r); the verdict "g is better" is robust if the modelled c_g/c_s is below 1/(c_U/c_model), s being taken at its modelled cost.
Numbers `[s4b]`, g of M3.3, w_emb = 0.5, w_lin = 0.5, p_r = 2: τ_LB = 1.64 / 1.86 yr; c_U/c_model = 5.53 / 4.98; margin 0.181 / 0.201; over the share grid 0.11 to 0.49 / 0.13 to 0.52. With a reduced damage sum of 0.3: 0.125 / 0.138. New in S4: if the environment curve is not known for either side and is applied to g only, the margin is 0.012 / 0.019 at the baseline and 0.004 to 0.042 / 0.007 to 0.058 across the planner's range.
Reading of "0.3·τ₀" (work item 9): adopted reading: the reduced damage sum enters the lower-bound life only (ρ′ = 0.3·ρ in the x* equation) and the modelled life in the numerator stays τ₀, because the model being bounded does not use a reduced sum. The alternative (0.3·τ₀ in the numerator as well) gives 0.347 / 0.373. The headline margin 0.181 uses no reduced sum and does not depend on the reading; only the 0.125 figure does.
Confidence: medium. Evidence: A.
Falsifier: a g unit whose measured life falls below τ_LB at measured inputs.

### M4: default rules

**M4.1 (revised) Rule R, rates.**
Equation: Σ̇_total = Σ̇_corr + Σ̇_fat + Σ̇_op + d/dt[K_ox·√t_age] (+ a linear scale-loss term where a loss rate is declared) [W/K]; each term at the pristine section, the prescribed part temperature and fixed duty; oxidation with declared scale loss as parabolic + linear.
Valid when all hold: x_e ≤ 0.095/p (linear recession) or 0.07/p (parabolic) for every rate `[a1]`; self-heating ΔT ≤ 0.05·R·T²/Q where the environment temperature is the prescribed one `[a6]`; scale thickness below δ_c and strain (cyclic plus Δα·ΔT, with the substrate's own Δα) below ε_c `[s4d]`; load cases sequential, or damping linear. Error then about 5 % per term.
Flag, usable with a stated multiplier: x_e up to three times the gate (apply M_lin or M_par); series resistance above 0.1·R₀; paralinear regime (state the band); concurrent rate-independent hysteresis at well separated frequencies with n = 2 (band 0.7 to 1.1 of the sum on the computed grid).
Changes from the plan: gate for parabolic recession added; the scale gate takes the substrate's Δα and the thermal strain; the concurrent-hysteresis condition is restated from "more than the sum" to "either sign".
Confidence: medium.

**M4.2 (revised) Rule W, wearout life.**
Equation: τ_M = [Σ_l ν_l/N_l]⁻¹ (Miner over load cases, after cycle counting on the combined history if cases can be concurrent; N_l from an S–N curve valid for the service environment and frequency); t_c = h₀/(n_s·r) or d₀/(2r); τ_c = t_c·{1 − [1 + (q − 1)·τ_M/t_c]^(−1/(q−1))}, q = p·m; **τ_wearout = min(τ_c, x_allow·t_c, t_perf)**, t_perf = h₀/(n_s·PF·r) where a pitting factor is declared.
It reduces to the current rule when one case dominates, τ_M ≪ t_c and there is no pitting, and to the recession life when τ_M ≫ t_c.
Valid for load-controlled stress, linear uniform recession (use the parabolic form of M2.5 for oxidation), x_allow declared (there is no safe default: the worst-case error ranges from 1.84 to 4.38 with it `[c6]`).
Changes from the plan: the perforation cap is in the rule, not only in the reject list; x_allow must be declared; the first-order life screen is limited to q·τ_M/(2·t_c) < 0.05.
Confidence: medium.

**M4.3 (revised) Anchors.**
- Rule R, paralinear band: Opila and Hann 1997 is open (US government report) and gives k_p and k_l tables; S2's conversion gives a limiting thickness of 10.4 µm against the paper's 6.9 µm `[d1]`, `[issues.md, D2]`. The anchor is therefore available but not yet reproduced; the unit conversion is the suspect. Tedmon 1966 is paywalled.
- Rule R, section-loss multiplier: electrical-resistance probes (ASTM G96, method confirmed by S3); no data set read.
- Rule W, environment factor: the welded-steel design code (air and free-corrosion curves; constants matched by S3; older editions public) is the only sourced anchor, and it is for another material and a design curve.
- Rule W, aluminium: no open, tabulated corrosion-fatigue S–N pair and no open pre-pitted data set were found. EN 1999-1-3 clause 6.4 (detail category lowered by exposure) exists as a rule, not as data.
- Proposed test: load-controlled fatigue of thin struts (0.3 to 1 mm) in salt fog and in laboratory air at two frequencies; compare the life ratio with M2.7, M2.8 and M2.9.
In-sample warning (work item 11): the gates of Rule R are defined as the points where the modelled error is 5 %, so they are true by construction; the first-order screens were compared with exact values only on the worked pair g and s; the perforation cap and the x_allow requirement of Rule W were added in S4 because of the same worked example. None of this is a test. An out-of-sample test is still needed for both rules: a case with different material, geometry and frequency, chosen before computing, and at least one measured life or mass-loss history.
Confidence: low to medium.

**M4.4 (revised) Must reject or return "undetermined".** Concurrent load cases without cycle counting; S–N data from a milder environment or a higher frequency than service; a pitting alloy with only a uniform rate; a spectrum supplied as "load cases" with the minimum rule (M2.1); constant-voltage or other non-fixed-duty function, and displacement-controlled loading (sign reversal: treat with their own multipliers, not the default); spallation or breakaway without a declared loss rate; electro-thermal loop gain α·ΔT₀/(1 − x) above 0.5; Σ̇_op from a boundary power balance together with component terms; any verdict whose modelled cost ratio lies between the margin of M3.6 and its reciprocal.
Confidence: medium.

---

## 2. Worked numbers

**Inputs (all restated in `s4_b_sensitivity.py`).** Alloy 2024-T4: σ_f′ = 900 MPa (secondary source only); b = −0.102 or −0.124 (open); N₀ = 5e8 cycles; E = 73 GPa; ρ_m = 2780 kg/m³; M = 26.98 g/mol; T₀ = 298.15 K; ψ = 2e-3 (unsourced); embodied 200 MJ/kg (an energy figure); chemical exergy of Al 795.7 kJ/mol (revised value, S3). Loading: fully reversed, load-controlled, ν = 1 Hz, amplitude equal to the air strength at N₀. Environment: r = 10 µm/yr uniform; environment curve k₅ = 0.9, k₈ = 0.4 (unsourced range); pitting factor 10; ΔK_th = 3 MPa√m; Y = 0.713. Geometry: g = round strut d₀ = 0.3 mm, length 3 mm (p = 2, t_c = 15 yr); s = wall h₀ = 3 mm, one side attacked (p = 1, t_c = 300 yr); thin wall for M2.8 and M2.9: 0.3 mm, both sides (t_c = 15 yr). 1 yr = 3.15576e7 s. Because the stress is defined as the strength at N₀, τ₀ = N₀/ν = 15.844 yr and ρ do not depend on b.

| Quantity | b = −0.102 | b = −0.124 | Ratio |
|---|---|---|---|
| m = −1/b | 9.804 | 8.065 | 0.82 |
| σ_a0 (MPa) | 108.70 | 68.90 | 0.63 |
| ρ for g; for s | 1.056; 0.0528 | same | 1 |
| τ_c for g (yr) | 2.253 | 2.561 | 1.14 |
| F_cur for g; F_min for g | 7.03; 6.66 | 6.19; 5.86 | 0.88 |
| F_cur for s | 1.244 | 1.203 | 0.97 |
| Worst F_min over ρ: wall; strut | 4.38; 6.77 | 3.91; 5.96 | 0.89; 0.88 |
| Verdict error, w_emb = 1; 0.5; 0.1 | 5.65; 3.58; 1.57 | 5.14; 3.26; 1.49 | 0.91; 0.91; 0.95 |
| τ_LB for g (yr); x* | 1.639; 0.1093 | 1.864; 0.1243 | 1.14 |
| E4 margin (w_emb = 0.5, p_r = 2) | 0.181 | 0.201 | 1.11 |
| E4 margin, reduced sum, adopted reading | 0.125 | 0.138 | 1.10 |
| E4 margin, environment curve on g only (new) | 0.012 | 0.019 | 1.54 |
| F_env at (0.9, 0.4) | 154.1 | 97.4 | 0.63 |
| F_env over the planner's range | 35.9 to 459 | 24.1 to 290 | 0.63 to 0.67 |
| k₈ at which F_env equals the strut section-loss maximum | 0.819 | 0.799 | |
| Section-loss factor on top of the environment curve, thin wall, 0.01; 0.1; 1 Hz | 2.34; 1.15; 1.016 | 2.88; 1.22; 1.022 | |
| (1 + s)^m at s = 0.1; 0.2; 1 | 2.55; 5.97; 894 | 2.16; 4.35; 268 | |
| a₀ (µm); life factor of a 100 µm pit | 119; 19.8 | 297; 3.2 | 2.49; 0.16 |
| Thin wall with pits: pit-fatigue life; perforation (yr) | 1.31; 1.50 | 2.78; 1.50 | governing mode changes |
| Shares fatigue; corrosion; embodied | 0.100; 0.214; 0.686 | 0.043; 0.227; 0.730 | |
| Displacement-control threshold ρ* | 0.0926 | 0.110 | 1.19 |

All from `[s4b]`; the b = −0.102 column reproduces `[c1]`, `[c6]`, `[e2]`, `[e4]`, `[c10]`, `[c12]`, `[e3]`.

**Answer to the prompt's worked example** (aluminium alloy in saline air, amplitude at the endurance level, r = 10 µm/yr, 0.3 mm strut, 1 Hz): "minimum of separate mechanisms" (15 yr) overstates life by 6.7 / 5.9 from section loss alone; by at least 10 if the alloy pits with a pitting factor of 10 (thin wall); and by 154 / 97 (range 24 to 459, unsourced) if the air S–N curve is used in place of a saline one. These do not multiply: with the saline curve in place, section loss adds 1.03 at 1 Hz `[c10]`. For r = 1 µm/yr and a 3 mm wall attacked on one side the section-loss factor is 1.03 `[c3]`. For humid air no number can be given.

**Which b?** Not decided. Two cross-checks, neither a confirmation: the MIL-HDBK-5 equation for unnotched 2024-T3 sheet (matched by S3) gives 5e8 cycles at 92.7 MPa for R = −1; b = −0.102 puts σ_a0 17 % above that (the equation then gives 0.087·N₀), b = −0.124 puts it 26 % below, under the equation's 15.8 ksi asymptote, where it predicts no failure `[s4b]`. A data sheet quoted by S3 gives 138 MPa at 5e8 cycles in rotating bending, above both. The different temper, product form and loading mode mean these do not select a value. The planner's −0.102 and any recollection of it are one source, not two.

**Corrected mismatch (M18), D5 and D6** `[s4d]`:

| Quantity | Δα = 7e-6 /K (Ni-base, Fe–Cr) | Δα = 14.7e-6 /K (Al alloy) |
|---|---|---|
| Mismatch stress in the scale at ΔT = 200 K (GPa) | 0.71 | 1.49 |
| δ_c at G_c = 5 J/m², ΔT = 200 K (µm) | 5.03 | 1.14 |
| δ_c at G_c = 5 J/m², ΔT = 100 K (µm) | 20.1 | 4.57 |
| δ_c at G_c = 5 J/m², ΔT = 200 K, plus ε_mech = 1.5e-3 (µm) | 1.17 | 0.50 |
| ΔT at which mismatch strain equals ε_a (b = −0.102 / −0.124) (K) | 213 / 135 | 101 / 64 |

Inputs: E_ox = 380 GPa, ν_ox = 0.25, f = 1.12 (all unsourced or unconfirmed).

---

## 3. Citations

Status from S3 (`prompt_6_citations.md`); nothing was re-checked in S4. "Not seen" means the source exists but the content it is cited for was not seen in what S3 read. No equation or figure number is relied on unless given.

Verified (record or abstract supports the use):
- de Groot, Mazur, 1962, Non-Equilibrium Thermodynamics, North-Holland (entropy production as flux-times-force products; chapter not checked).
- Basquin, 1910, The exponential law of endurance tests, Proc. ASTM 10, 625–630.
- Palmgren, 1924, Die Lebensdauer von Kugellagern, VDI-Z. 68, 339–341.
- Miner, 1945, Cumulative damage in fatigue, J. Appl. Mech. 12, A159–A164.
- Manson, Halford, 1981, Practical implementation of the double linear damage rule and damage curve approach for treating cumulative fatigue damage, Int. J. Fracture 17, 169–192 (the exponent 0.4 seen; the form (N₁/N₂)^0.4 not seen; equation number UNSURE).
- Fatemi, Yang, 1998, Cumulative fatigue damage and life prediction theories: a survey of the state of the art for homogeneous materials, Int. J. Fatigue 20, 9–34.
- Haibach, 1970, Modifizierte lineare Schadensakkumulations-Hypothese …, LBF TM 50/70 (slope 2m − 1 below the knee).
- ASTM E1049-85, Standard Practices for Cycle Counting in Fatigue Analysis, Section 5.4 (rainflow).
- Smith, Watson, Topper, 1970, A stress–strain function for the fatigue of metals, J. Materials 5, 767–778.
- Lazan, 1968, Damping of Materials and Members in Structural Mechanics, Pergamon (D = J·σ^n; exponent for aluminium not confirmed).
- Wagner, 1933, Beitrag zur Theorie des Anlaufvorgangs, Z. Phys. Chem. B21, 25–41.
- Tedmon, 1966, The effect of oxide volatilization on the oxidation kinetics of Cr and Fe–Cr alloys, J. Electrochem. Soc. 113, 766–768 (equation number UNSURE; constants not read).
- Opila, Hann, 1997, Paralinear oxidation of CVD SiC in water vapor, J. Am. Ceram. Soc. 80, 197–205; Tables III and IV read by OCR from the NASA reprint (column assignment of some rows UNSURE).
- Lowell, Barrett, Palmer, Auping, Probst, 1991, COSP: a computer model of cyclic oxidation, Oxid. Met. 36, 81–112.
- Kitagawa, Takahashi, 1976, Applicability of fracture mechanics to very small cracks or the cracks in the early stage, Proc. 2nd Int. Conf. Mechanical Behavior of Materials, 627–631.
- El Haddad, Topper, Smith, 1979, Prediction of non propagating cracks, Eng. Fract. Mech. 11, 573–584.
- Kondo, 1989, Prediction of fatigue crack initiation life based on pit growth, Corrosion 45, 7–11.
- Harlow, Wei, 1994, Probability approach for prediction of corrosion and corrosion fatigue life, AIAA J. 32, 2073–2079.
- Godard, 1960, The corrosion behavior of aluminum in natural waters, Can. J. Chem. Eng. 38, 167–173 (cube-root pit growth).
- Sankaran, Perez, Jata, 2001, Effects of pitting corrosion on the fatigue behavior of aluminum alloy 7075-T6: modeling and experimental studies, Mater. Sci. Eng. A 297, 223–229; Dolley, Lee, Wei, 2000, The effect of pitting corrosion on fatigue life, Fatigue Fract. Eng. Mater. Struct. 23, 555–560 (both exist; the life factors were not seen; no open data).
- Gangloff, 1990, Corrosion fatigue crack propagation in metals, NACE-10, 55–109; Wei, Landes, 1969, Correlation between sustained-load and fatigue crack growth in high-strength steels, Mater. Res. Stand. 9, 25–27; Suresh, Zamiski, Ritchie, 1981, Oxide-induced crack closure …, Metall. Trans. A 12, 1435–1443 (steels).
- ISO 9223:2012, Corrosion of metals and alloys: corrosivity of atmospheres, Table 2 (aluminium classes; the humidity threshold not checked).
- DNV-RP-C203, Fatigue design of offshore steel structures: curve D in air and in free corrosion (free-corrosion table is Table 2-3 in the 2008 and 2011 editions, Table 2-4 in 2016; S2 used the 2010 edition).
- ASTM E647 (threshold at 1e-10 m/cycle); ASTM G96 (electrical-resistance method).
- Alduchov, Eskridge, 1996, Improved Magnus form approximation of saturation vapor pressure, J. Appl. Meteorol. 35, 601–609, eq. 21.
- EN 1999-1-3:2007+A1:2011, clause 6.4 (table values not read; superseded by the 2023 edition).
- Szargut, Morris, Steward, 1988, Exergy Analysis of Thermal, Chemical, and Metallurgical Processes, Hemisphere (secondary: 888.4 kJ/mol older, 795.7 kJ/mol revised).

Exists, cited content not seen:
- Dowling, Mechanical Behavior of Materials, 4th ed., 2013, Table 9.1 (title confirmed; the 2024-T4 row not read: this is the open b).
- MIL-HDBK-5J (the equation was found in MIL-HDBK-5H, Fig. 3.2.3.1.8(e); 5J figure number UNSURE).
- Schütz, 1996, A history of fatigue, Eng. Fract. Mech. 54, 263–300 (no numeric range of Miner sums seen).
- FKM guideline, 6th ed., 2012 (0.3 from secondary sources; section UNSURE).
- Pilling, Bedworth, 1923, The oxidation of metals at high temperatures, J. Inst. Metals 29, 529–591 (the ratios used are not from this paper).
- Smialek, 2003, A deterministic interfacial cyclic oxidation spalling model, Acta Mater. 51, 469–483 (long-run linear rate not in the abstract; the formula here is derived, not quoted).
- H. E. Evans, 1995, Stress effects in high temperature oxidation of metals, Int. Mater. Rev. 40, 1–40 (strain-energy criterion not in the abstract; Evans and Lobb 1984, Corros. Sci. 24, is a candidate source, not read).
- Schütze, 1997, Protective Oxide Scales and Their Breakdown, Wiley (no values seen).
- Hancock, Nicholls, 1988, Application of fracture mechanics to failure of surface oxide scales, Mater. Sci. Technol. 4, 398–406 (the form of ε_c not seen).
- TEMA standards (fouling values conflict by edition).

UNSURE:
- Bejan, 1996, Entropy Generation Minimization, CRC Press (no catalogue record read).
- ASM Handbook Vol. 19, Fatigue and Fracture, 1996, chapter by Bucci et al., pp. 771–812, air and seawater figures for 2024 and 7075 sheet (figures not read; this is the missing aluminium anchor).

---

## 4. Open points

1. Are GMS-220 load cases sequential or concurrent, and can a spectrum be passed as load cases? This decides whether M2.1 to M2.3 are a minor or the main defect of the wearout rule.
2. The Basquin exponent of 2024-T4 (−0.102 or −0.124) is unread at source; it moves σ_a0 and F_env by 0.63 and flips the pit example's governing mode, but not the verdict or any default.
3. No open aluminium corrosion-fatigue S–N pair and no open pre-pitted data exist in what S3 found: F_env (24 to 459), the pit factors and the humid-air case are unanchored, so Rule W has no aluminium anchor until the proposed thin-strut test or the handbook figures are read.
4. The cost form, the verdict form (ratio, shares, an "undetermined" class) and the weighted adequacy sum were inferred, not read from the spec; the embodied input is an energy, not an exergy, figure.
5. Neither default rule has an out-of-sample test, and the one open paralinear anchor did not reproduce the published limiting thickness (10.4 against 6.9 µm).

---

## 5. Changed since plan

Count: 23 of 34 claims changed; 11 unchanged.

**Revised in substance (13).**

| Claim | Plan | Now | Cause |
|---|---|---|---|
| M1.6 | Concurrent rate-independent hysteresis gives more than the sum; ratio ≈ (1 + 2s + φs²)/(1 + φs²), maximum 1 + 1/√φ | Either sign (0.70 to 1.84 on the grid); idealised ratio withdrawn as an estimate; only the upper bound is tested | A11 (b), work item 4 |
| M1.8 | Δα = 7e-6 /K for the worked case; crossover flaw 0.8 µm | 7e-6 kept for Ni-base and Fe–Cr; 14.7e-6 for aluminium (δ_c 4.4 times smaller); thermal strain added to the cracking criterion; crossover 0.79 / 1.97 µm | M18, work item 2 |
| M1.11 | Ensemble crosses the parabolic law at t = n₀·Δt | Ensemble is 1.33 times the parabolic law there; only the asymptote crosses | D4 |
| M1.12 | First-order sum Σ w_i·e_i with life error q·ρ/2 | Sum defined through the cost form; q·ρ/2 is a screen only (off by 72 % at ρ = 1.06) | E5, work item 8 |
| M2.7 | Life factor about 150 (40 to 350) | 154 / 97; 24 to 459 over the range and both b; stated as unsourced; crossing statement corrected; no worst case claimed from the sweep | L01, M03, C10, work items 1, 3, 5 |
| M2.9 | 100 µm pit: factor about 20; coupled factor about 12; cube-root life expected longer | Factor 19.8 / 3.2; governing mode fatigue / perforation; perforation is the robust cap (factor at least 10); cube-root expectation withdrawn and explained | M03, C13, L06, work items 1, 6 |
| M2.10 | (iii) Miner sums up to about 1.8 under rising stress | Life gain 1 to 8 %; C14 null case decided (identity; passes; tests nothing about the nonlinear term) | C14, work item 7 |
| M3.3 | Life overstated 7.0 (g), 1.24 (s); verdict error 5.7, 3.6 | 7.03 / 6.19 and 1.244 / 1.203; 5.65 / 5.14 and 3.58 / 3.26; bias falls to about 3 % at 1 Hz once a common environment curve is used | M03, C11 |
| M3.6 | Margin about 0.18 | 0.181 / 0.201 from section loss; 0.012 / 0.019 if the environment curve is unknown; reading of 0.3·τ₀ fixed | M03, L01, work item 9 |
| M4.1 | Gate x_e ≤ 0.1/p; generic scale gate; "no concurrent correlated loads" | 0.095/p linear, 0.07/p parabolic; scale gate with the substrate's Δα and thermal strain; concurrent hysteresis flagged as either sign | A3, M18, A11 |
| M4.2 | τ_wearout = min(τ_c, x_allow·t_c) | Perforation cap added; x_allow must be declared; cycle counting stated in the rule | C13, C7, B5 |
| M4.3 | Anchors exist for each rule; aluminium anchor "not identified with certainty" | No open aluminium anchor; paralinear anchor open but not reproduced; in-sample warning added | S3, D2, work item 11 |
| M4.4 | Reject list | Adds: spectrum passed as load cases with the minimum rule; S–N data at higher frequency than service; verdicts inside the bound margin | M2.1, M3.6 |

**Extended or flagged, statement otherwise kept (7).** M1.3 (fifth case: concurrent hysteresis). M1.4 (corrosion term's own exponent: p = −1 for a round strut; parabolic gate values). M2.1 (minimum rule is not invariant to how a spectrum is split). M2.2 (many near-equal cases: gap approaches L; window given for both b). M2.3 ((1 + s)^m is a worst-phase value; both b). M2.12 (geometry factor inconsistent; about 6 times longer with the other factor, not recomputed). M3.2 (rows 6b and 16 added).

**Numbers only, now given for both b (3).** M1.5 (fatigue share 0.100 / 0.043). M2.5 (maxima 4.38 / 3.91 and 6.77 / 5.96). M2.8 (extra factors 2.34 / 2.88, 1.15 / 1.22, 1.016 / 1.022).

**Unchanged (11).** M1.1, M1.2, M1.7, M1.9, M1.10, M2.4, M2.6, M2.11 (apart from the cap carried over from M4.2), M3.1, M3.4, M3.5.

**Rows affected by b but not recomputed** (direction and rough size): C7 maxima (lower by about 10 %); C9 parabolic factors (lower; rough size as C6, about 10 to 15 %); C11 full grid (higher by up to about 25 % at 0.01 Hz, a few per cent at 1 Hz); C13 other PF and r cases and the cube-root variant (pit-fatigue lives longer by up to about 2; perforation unchanged); C14 (smaller q, so a gain no larger than 8 %); C15 lives (longer; threshold given); B1 equal-life points s* (lower by up to about 10 % at φ = 1000); B2 medians (somewhat higher, since the curve is less steep); B5 rainflow ratios (closer to 1); E1 (independent of b); E5 thermal numbers (independent of b).

**Work list coverage.** 1: section 2 and M2.5, M2.7, M2.9, M3.3, M3.6 (verdict and defaults unchanged). 2: M1.8 and section 2. 3: M2.7, M3.6. 4: M1.6. 5: M2.5, M2.7. 6: M2.9. 7: M2.10. 8: M1.12. 9: M3.6. 10: evidence classes in the header and in each claim. 11: M4.3.

---

## Errata (S5)

Added by the orchestrator on 2026-11-15 (user decision D7, `prompt_6_synthesis.md`). The text above is unchanged; these corrections from `prompt_6_review.md` take precedence. Numbers are at b = −0.102 / −0.124 unless stated.

1. **Verdict 2, third bullet; M2.3; M3.2 row 6 (review #1).** "(1 + s)^m = 894 / 268 at s = 1" is the slow case alone, not the error of the minimum rule. At s = 1 the minimum rule overstates life by 100 (φ = 9), 28 (33), 7.9 (129) and 1.87 (1025) at b = −0.102 (30.6 down to 1.26 at b = −0.124); Miner over separate cases by 90 to 1.9. The worst case over s is about 318 / 97 near s ≈ 0.8 (φ = 9). (1 + s)^m approximates the error only where the slow case dominates (s below about φ^(−1/m)). `[b4]`, `prompt_6_review_code/rv01_core_independent.py` [conc].
2. **Verdict 2, fifth bullet; M2.5; M2.7; M4.2 (review #2).** "At most 4.38 / 3.91 (wall) and 6.77 / 5.96 (round strut)" covers linear recession under axial or membrane load only. Round member in bending or torsion (p = 3): 8.91 `[c6]`. Parabolic recession: 11.7 (wall) and 25.5 (strut) at their maxima (ρ = 1); 42.2 / 33.0 with p = 3. "F_env stays above the section-loss maximum at every point of the range" holds only for linear recession with p ≤ 2. M4.2's "worst-case error 1.84 to 4.38" becomes 1.84 to 8.91 (linear) and up to 42.2 (parabolic). `[rv01]` [sec], [env].
3. **M4.2 Rule W (review #3).** Rule W has no pit-initiated-fatigue term. For a 3 mm wall with PF = 3 at 10 µm/yr, Rule W gives 12.7 yr against 2.86 yr from the M2.9 pit model (4.45 times non-conservative; 2.42 at b = −0.124). Perforation is an upper bound on life, not a conservative cap. Decision D3: a pitting alloy without a declared pit-fatigue life returns undetermined; a declared one enters the minimum. `[rv01]` [pit].
4. **Verdict 5 (review #4).** b changes numbers by up to 84 % (pit life factor, ratio 0.163), 70 % ((1 + s)^m at s = 1), 57 % (fatigue share) and +54 % (E4 margin with the environment curve on g), not "about 40 %". No default and no ranking changes. `[s4b]`.
5. **Provenance (review #5).** The S4 scripts make 33 comparison lines with S2 (25 + 8), not 37; all 33 reproduce.
6. **M1.6 (review #6).** The upper bound reaches 32.7 times the rainflow value, not 42.5 (42.5 is upper bound over separate sum). `prompt_6_review_code/rv02_rainflow_a11.py`.
7. **M2.10, C14 null case (review #8).** With q = 0, recession still ends the part at t_c, so the null life is min(τ₀, t_c), and τ/τ₀ = 1/ρ for ρ ≥ 1. The script was right; the null test's expected value was wrong for ρ ≥ 1.
8. **Rows not recomputed (review #9).** C15: lives get shorter, not longer (τ/τ₀ 1.053 → 1.043 at ρ = 0.01; 1.388 → 1.289 at 0.05). C9: 8 to 21 % lower (18 to 21 % at the ρ = 1 maxima), not 10 to 15 %. B1 s*: up to 14 % at φ = 1000, not 10 %. `prompt_6_review_code/rv03_not_recomputed_rows.py`.
9. **M3.4, M2.11 (review #10).** The E4 bound check is an identity, not evidence (class A). M2.11's lower bound x_c ≥ x* is proved (class P): the integrand is increasing, so ρ ≤ x_c(1 − x_c)^(−q).
10. **M2.10 (i) (review #11).** σ ∝ (1 − x)^(+1) holds for imposed curvature or deflection in bending only; under imposed axial displacement p = 0 and there is no gain over τ₀.
11. **M2.9 (review #12).** a₀ uses the full range at R = −1 with a ΔK_th quoted near R = 0.1. With the tensile part only, a₀ = 477 / 1187 µm, the 100 µm pit life factor falls to 2.5 / 1.4, and perforation governs for both b.
12. **M4.3 (review #13).** The Rule R flag band for concurrent hysteresis (0.7 to 1.1) is in-sample; a phase sweep at φ = 3 gives 0.33 to 1.33 (n = 2) and 0.27 to 2.12 (n = 3).
13. **Verdict 2, fourth bullet (review #14).** "Pitting at least 10" equals the input pitting factor PF = 10 by construction; it is not a computed effect.
14. **M3.6 (review #17).** The 0.181 margin uses τ_LB; with the exact τ_c it is 0.244 / 0.271.
