# Prompt 5 answer (S4): Class I / Class II demarcation (GMS-300 gate)

Stage: S4 finaliser. Date: 2026-11-14. Level of everything in this file: `derived` (unverified).

Inputs read: the Prompt 5 text block; `prompt_5_plan.md` (S1); `prompt_5_code/outputs/` and `prompt_5_code/data/` (S2); `prompt_5_citations.md` (S3). No S2 computation was repeated. One new script was written: `prompt_5_code/s4_checks.py`, output `prompt_5_code/outputs/s4_checks.txt`.

## 0. How to read this file

**Verdict in one line:** valid with restated scope. The function-level split and the "transport-governed" criterion do not hold; a gate on (function, operating regime, binding envelope) with a threshold test and a compensation-price test does (sections 7 and 8).

**Source tags.** Every number carries a tag in square brackets. A tag names the S2 output file that printed it; the script has the same name with `.py`, in `local_docs/fable_runs/prompt_5_code/`.

| Tag | Output file in `prompt_5_code/outputs/` | Tag | Output file |
|---|---|---|---|
| [a1] | `a1_conductor_area_mass.txt` | [f6] | `f6_buildup_mc.txt` |
| [a2] | `a2_kelvin_optimum.txt` | [f7] | `f7_kedge_window.txt` |
| [a3] | `a3_break_even_embodied.txt` | [n1] | `n1_thermal_ri.txt` |
| [a4] | `a4_duty_crossover.txt` | [n2] | `n2_one_over_v_test.txt` |
| [b12] | `b1_b2_skin_dowell.txt` | [n3] | `n3_self_shielding.txt` |
| [b3] | `b3_ac_ratio_strip.txt` | [n4] | `n4_moderation.txt` |
| [c1] | `c1_fin_efficiency.txt` | [n5] | `n5_water_vs_cd.txt` |
| [c23] | `c2_c3_optimum_fin.txt` | [n6] | `n6_abundance_production.txt` |
| [c4] | `c4_pumping_price.txt` | [h12] | `h1_h2_redox_dl_energy.txt` |
| [d1] | `d1_overpotential.txt` | [h3] | `h3_ragone_crossover.txt` |
| [d2] | `d2_porous_electrode.txt` | [m12] | `m1_m2_ceiling_hardness.txt` |
| [d3] | `d3_break_even_overpotential.txt` | [m3] | `m3_shape_anisotropy.txt` |
| [e1] | `e1_voxel_conduction.txt` | [m4] | `m4_exchange_spring.txt` |
| [f1] | `f1_mass_attenuation.txt` | [m5] | `m5_magnet_circuit.txt` |
| [f2] | `f2_ratio_crossings.txt` | [p1] | `p1_heat_pipe.txt` |
| [f3] | `f3_thickness_ratio.txt` | [t1] | `t1_transparent_conductor.txt` |
| [f4] | `f4_photoelectric_exponents.txt` | [j1] | `j1_gate_matrix.txt` |
| [f5] | `f5_nonuniform_shield.txt` | [s4-A] to [s4-G] | `s4_checks.txt`, sections A to G |

[S3] means `prompt_5_citations.md` (the part or row is named). [search] means a web-search result page read in this stage; it is a secondary source and is not a reading of the paper.

**Labels.** MEMORY: an input from the planner's memory that no stage confirmed from a source. UNSURE: not verified. LOOKUP: read from a named table by S2 or S3. "Identity" marks a check that is true by construction and is not evidence.

**Symbols.** c: the coefficient through which the scarce element x acts. κ = c_s/c_g ≥ 1 (incumbent over candidate). Γ: geometry. ρ: density (kg/m³). e: embodied energy per kg (J/kg), used as the stand-in for Σ_init·T₀ per kg. τ: service time under load (s). T₀: reference temperature (K). Subscripts s (incumbent) and g (candidate).

**Limit that applies to all of G2.** No stage could read the framework's definition of Σ_init. All embodied values used here are cumulative energy demand (ICE v2.0 "embodied energy"; Nuss and Eckelman "CED"), not exergy destroyed. If the framework prices scarcity another way, the break-even values in G2.3, G2.4 and G2.6 move. UNSURE.

## 1. G1: is "transport-governed" a sound criterion?

**G1.1** "Transport-governed" is neither necessary nor sufficient for substitutability. Two of the Class I examples are linear transport problems with the same compensation law as conduction.
- Equations: narrow-beam photon transmission T = exp(−(μ/ρ)·x), x = areal density (kg/m²); required x = ln(1/T)/(μ/ρ). Conduction G = k·A/L (W/K); required A = G·L/k. Both: required extensive quantity ∝ 1/coefficient.
- Evidence: no thickness distribution at equal mean areal density transmitted less than the uniform slab (smallest ratio 1.0003, 202 sweep points, three cases) [f5]. Thin-absorber neutron capture is linear in τ: P/(2τ) = 0.996 at τ = 1e-3 [n3].
- Confidence: high.
- Falsified by: a geometry that reaches a given narrow-beam transmission with less areal mass than ln(1/T)/(μ/ρ).

**G1.2** A test decidable from the governing equation exists. Write the requirement as F(c, Γ) ≥ F_req, with Γ in the admissible set bounded by the scenario's envelope. Then x acts in one of four ways.
- Type T (threshold): c enters an inequality with no Γ in it (T_op < T_C; stability window; edge, line or resonance energy; state as manufactured). No geometric compensation.
- Type E (extensive): F = c^a·S(Γ) with S unbounded when the envelope is free. Compensation always exists, at price κ^a in S.
- Type U (utilisation): F = c·N·η_u(Γ), η_u ≤ 1. Geometry raises η_u towards 1 for either material and no further.
- Type M (matched): the target is a value of c·S, not an extremum. Any conductor reaches it; x is not needed at all.
- Confidence: medium. The 18 gate cases contained no function outside these types [j1], but the cases were written by the planner and are not an independent test.
- Falsified by: a function that fits no type, or a Type T case where geometry compensates. A known near-miss: coercivity looks like a threshold on K₁ and is partly geometric (G3.12).

**G1.3** Bulk-limited linear conduction (DC current, steady heat conduction): geometry compensates whenever volume is free, with no operating price.
- Equations: A_g/A_s = κ; V_g/V_s = κ; m_g/m_s = κ·ρ_g/ρ_s.
- Numbers, Al against Cu: area ratio 1.638, mass ratio 0.494 (0.498 with ρ_Cu = 8 890 kg/m³) [a1]. Independent check: IEC 60228:2004 Table 2 class 2 conductors give an Al/Cu resistance ratio of 1.651 to 1.683 over 17 sizes at equal nominal area (LOOKUP, publisher preview PDF) [a1]. The standard's ratio is 1 to 3% above the 61% IACS arithmetic.
- Confidence: high.
- Falsified by: a published conductor table with an equal-resistance Al/Cu area ratio outside 1.6 to 1.7.

**G1.4** Penetration-limited regimes share one law. Fin conduction, the porous electrode and absorber self-shielding obey u″ = u/λ² with utilisation η_u = tanh(ξ)/ξ (slab absorber: P/(2τ)); the skin effect is the complex analogue. In the thick limit the function scales as c^(1/2).
- Equations: same-geometry penalty κ^(1/2) in the thick limit, κ in the thin limit. Skin depth δ = sqrt(2/(ω·μ₀·σ)) (m). Dowell factor F(ξ) = ξ·(sinh 2ξ + sin 2ξ)/(cosh 2ξ − cos 2ξ).
- Numbers: thick-limit log-log slope 0.5000 to 0.5003 for the porous electrode, closed form and finite differences [d2]. Fin efficiency ratio tends to sqrt(k_g/k_s) = 0.7071 (k 200 against 400 W/(m·K)) [c1]. Strip R_ac ratio Al/Cu: 1.638 thin, 1.280 thick, finite differences and closed form agree to 7e-5 [b3]. δ at 50 Hz: Cu 9.35 mm, Al 11.96 mm [b12]. Minimum of F/ξ: 0.9172 at ξ = π/2 [b12].
- Revised (see section 9): the path between the two limits is not monotonic for the skin effect. The Al/Cu ratio dips to 1.216 at t/δ_Cu = 4.72, which is below the thick-limit value 1.280 [b3]. The statement "the penalty lies between κ^(1/2) and κ" holds for the real (tanh) problems and fails for the complex one. The ratio stays above 1 everywhere in the sweep, so the ranking never reverses.
- Confidence: high (limits), medium (that these four problems cover the Class II list).
- Falsified by: a thick-limit slope outside 0.5 ± 0.02 in any of the four problems; an R_ac ratio below 1 at any thickness.

**G1.5** Convective heat transfer: the solid's k enters only through fin efficiency and spreading resistance. Geometry compensates by fin thickness (price: mass and flow blockage) or by flow (price: pumping power).
- Equations: fin parameter m = sqrt(2h/(k·t)) (1/m); η_f = tanh(mL)/(mL). Equal η_f at equal L and h needs t_g/t_s = κ; fin mass ratio κ·ρ_g/ρ_s. Optimum rectangular fin: mL = 1.4192, profile area A_p = 0.504·(q′/θ_b)³/(h²·k) (m²), so fin mass per unit duty ∝ ρ/k. Blockage at fixed pitch and flow rate: ΔP ∝ b⁻³ (b = channel gap). Turbulent duct: P_pump ∝ (h)^3.44.
- Numbers: optimum mL = 1.41922 and constant 0.50425 for all 36 cases [c23]. Fin mass ratio Al/Cu at equal duty: 0.603 (k_g = 200), 0.509 (237), 0.927 (130); mass crossover at k_g = 120.5 W/(m·K) [c23]. Baseline fin (h = 50 W/(m²·K), L = 30 mm, t = 1 mm): η_Cu = 0.931, η_Al = 0.873, ratio 0.937 [c1].
- Compensation by flow in fully developed laminar channels works only through the caloric term. For the 6.3% deficit the pumping power ratio is 1.04 at NTU₀ = 2.5 and 1.33 at NTU₀ = 0.78; for a 29.3% deficit it is 1.41 at NTU₀ = 2.5 and about 200 at NTU₀ = 0.78 (the compensated flow is outside the laminar range there, so this value is indicative only); at NTU₀ ≤ 0.25 the 29.3% deficit cannot be recovered by flow at all [c4].
- Limits of the evidence: the exponents 3.44 and −3.00 follow from the assumed correlations (identity) [c4]. The plan's exponent 5 for a developing laminar boundary layer was not computed by any row: UNSURE. Fin k values are MEMORY (AlSi10Mg 130 W/(m·K) UNSURE, range 100 to 180).
- Confidence: medium-high (fin laws), medium (flow prices).
- Falsified by: an optimum fin not at mL = 1.4192; a measured heat sink where a flow increase recovers a conduction deficit at NTU ≪ 1.

**G1.6** Viscous dissipation is not a substitution domain. No coefficient of the solid enters the flow problem with no-slip walls, so geometry acts on a shared fluid and is equally available to every wall material. It belongs on the price side of G1.5.
- Equation: Hagen–Poiseuille P = 128·μ·L·Q²/(π·D⁴) (W), μ the fluid viscosity.
- Evidence: reasoning only. No row computed it; gate case 18 was decided by its own premise [j1].
- Confidence: high for no-slip walls.
- Falsified by: a scenario where an x-dependent property enters the flow problem (slip coating, process-set roughness, wall strength limiting D).

**G1.7** Electrocatalysis has two compensation routes with different laws.
- Area route: roughness factor R_f,g/R_f,s = κ while the electrode is thinner than the reaction depth λ = sqrt(σ_ion·R·T/(a·j₀·F)) (m); beyond that the gain saturates as κ^(1/2) (G1.4).
- Overpotential route: Δη = b·log₁₀(κ·R_f,s/R_f,g) (V), b = 2.303·R·T/(α_a·F) (V/decade). Operating price Σ̇ = j·Δη/T₀ (W/(K·m²)).
- Numbers: b = 118.3, 59.2, 39.4, 29.6 mV/decade for α_a = 0.5, 1, 1.5, 2 at 298.15 K [d1]. At 353.15 K, α_a = 0.5, j = 1e4 A/m²: Δη = 140.15 mV per decade of κ from the full Butler–Volmer root against 140.17 from the Tafel form; price 4.70 W/(K·m²) per decade [d1]. Ionic conductivity of 30 wt% KOH at 80 °C: 138 S/m (Gilliam correlation as quoted by citing works, partly confirmed) [d2]. Metal foam with a = 5e3 m²/m³ (MEMORY UNSURE) at L = 3 mm has L/λ from 0.004 to 1.35, so plain foam is in the thin-to-transition range where the area route still works [d2].
- Revised (see section 9): the Tafel form is within 2 mV of the full solution only when both overpotentials, η_s and η_g, are in the Tafel range. The planner's condition (η_s > 100 mV only) failed with a 104 mV deviation, because area compensation can bring η_g below 100 mV [d1]. The correct threshold from the closed form of the back-reaction error is η > 104.4 mV at 353.15 K and 83.9 mV at 298.15 K for α_a = α_c = 0.5 and a 2 mV error [s4-B]. The kinetics must be written with separate anodic and cathodic coefficients, j = j₀·[exp(α_a·F·η/(R·T)) − exp(−α_c·F·η/(R·T))], both positive; the planner's cathodic exponent −(1 − α) is unphysical for α > 1.
- Confidence: high (formulas), medium (numbers).
- Falsified by: a full Butler–Volmer solution differing from b·log₁₀κ by more than 2 mV with both overpotentials above the threshold in [s4-B].

**G1.8** Utilisation ceiling. Geometry raises the fraction of atoms that take part towards 1 and never beyond the intrinsic per-volume or per-atom coefficient.
- Equations: Hashin–Shtrikman σ_eff/σ_s ≤ 2φ/(3 − φ) (isotropic, solid fraction φ); Wiener σ_eff/σ_s ≤ φ (aligned). Jensen: E[exp(−μx)] ≥ exp(−μ·E[x]).
- Numbers: a simple-cubic strut lattice lies below the Hashin–Shtrikman bound at all 13 solid fractions, with specific utilisation σ_eff/(φ·σ_s) from 0.34 (φ = 0.003) to 1 (solid) [e1]. A shield with thickness uniform on [0, 2x̄] at μx̄ = 5 transmits 14.8 times more than the uniform slab [f5].
- Confidence: high for linear bulk transport and linear absorption (two theorems). Medium as a general statement (catalyst site activity, coercivity and near-field optics are not covered by a theorem).
- Falsified by: a voxel conduction solve above the bound; a documented structure whose per-atom coefficient exceeds bulk in a listed domain.

**Price table for the Class II domains (summary of G1.3 to G1.7).**

| Domain | Coefficient of x | Geometry compensates when | Price and scaling law |
|---|---|---|---|
| Bulk conduction, DC or heat | σ_el, k | volume is free | volume ∝ κ; mass ∝ κ·ρ_g/ρ_s; no operating price |
| AC conduction, skin-limited | σ_el | width is free, or subdivision is allowed | thick conductor: width ∝ κ^(1/2); subdivided (foil, litz): metal area ∝ κ plus the fill-factor volume |
| Convective heat transfer | k of the fin | fin thickness or flow is free | fin thickness ∝ κ, fin mass ∝ ρ/k; blockage ΔP ∝ b⁻³; pumping power ∝ h^3.44 (turbulent); laminar: only through the caloric term, not at NTU ≲ 0.25 |
| Viscous flow | none | not applicable | not a substitution domain (G1.6) |
| Electrocatalysis | j₀ | area is free and L < λ, or loss is allowed | area ∝ κ (∝ κ^(1/2) effect beyond λ); or Δη = b·log₁₀κ with Σ̇ = j·Δη/T₀ |

## 2. G2: does Class II substitution ever pay under the fairness rule?

**G2.1** Monotonicity lemma. If F(c, Γ) is non-decreasing in c for every Γ and both materials share the admissible set, the candidate cannot beat the incumbent on function at equal geometry. The three "findings so far" are instances of this lemma and are not three independent results.
- Equation: for c_g ≤ c_s, sup_Γ F(c_g, Γ) ≤ sup_Γ F(c_s, Γ).
- Evidence: every same-geometry ratio computed is on the incumbent's side: R_ac ratio ≥ 1.216 [b3]; fin efficiency ratio ≤ 1 over 15 625 points [c1]; Δη ≥ 0 for κ ≥ 1 at equal area [d1].
- Confidence: high.
- Falsified by: a Class II function that is non-monotonic in its coefficient. Matched functions (G1.2 Type M) are, and there x is not needed.

**G2.2** Separability lemma. Where F = c·S(Γ), Σ_init = (e/T₀)·ρ·V(Γ) and the minimum volume for a shape factor is homogeneous, V*(S) ∝ S^n, geometry cancels and the Σ-optimal choice is decided by the material index c^n/(ρ·e).
- Equations (conductor of free cross-section, Kelvin's law): Σ(A) = e·ρ·A·L/T₀ + I²·L·τ/(σ·A·T₀) (J/K); A* = I·sqrt(τ/(σ·ρ·e)) (m²); Σ* = 2·I·L·sqrt(ρ·e·τ/σ)/T₀; Σ*_g/Σ*_s = sqrt[(e_g·ρ_g/σ_g)/(e_s·ρ_s/σ_s)].
- Numbers: numerical minimum against the closed form agrees to 3e-8 in A* and 7e-16 in Σ*; the ratio does not change with I, L or τ (spread 1e-15 over 18 load cases) [a2]. Kelvin current density for Cu at e = 55 MJ/kg and τ = 6.31e8 s: 0.213 A/mm² [a2].
- Confidence: high (mathematics).
- Falsified by: a ratio that depends on I, L or τ in a correct implementation.

**G2.3** Al against Cu conductors with free cross-section: Al wins in Σ if and only if e_Al/e_Cu < (ρ_Cu/σ_Cu)/(ρ_Al/σ_Al) = 2.025 [a3]. The outcome is set by the embodied values, which are scenario inputs, and not by geometry.
- Numbers with LOOKUP values (ICE v2.0 Summary Tables; Nuss and Eckelman 2014 Table S38) [a3]:

| Pair (Al / Cu), MJ/kg | e_Al/e_Cu | Σ*_Al/Σ*_Cu | Al wins |
|---|---|---|---|
| ICE virgin 218 / 57.0 | 3.82 | 1.374 | no |
| Nuss primary 194 / 59.3 | 3.27 | 1.271 | no |
| Nuss supply mix 131 / 53.7 | 2.44 | 1.098 | no |
| ICE recycled Al 29.0 / virgin Cu 57.0 | 0.51 | 0.501 | yes |
| Nuss old-scrap Al 23.8 / primary Cu 59.3 | 0.40 | 0.445 | yes |
| ICE recycled 29.0 / recycled 16.5 | 1.76 | 0.932 | yes |
| Nuss secondary 23.8 / secondary 28.1 | 0.85 | 0.647 | yes |

- On mass alone Al always wins (0.494) [a1].
- Confidence: medium (inputs are energy demand, not exergy; Σ_init definition UNSURE).
- Falsified by: table values of e that move a pair across 2.025; a Σ_init definition that is not proportional to mass.

**G2.4** Duty rule. With D = Σ̇_s·τ/Σ_init,s, an operating penalty ε (fractional rise in Σ̇) and an embodied saving β (fractional fall in Σ_init), substitution pays if and only if ε·D < β.
- Equations, Al for Cu at equal volume: pays if J²·τ < (e_s·ρ_s − e_g·ρ_g)/(1/σ_g − 1/σ_s) (A²·s/m⁴). With x = e_g·ρ_g/(e_s·ρ_s): a crossover exists if x < 1, and it sits at D_c = (1 − x)/(κ − 1), κ = σ_s/σ_g = 1.638. Al loses for D > D_c.
- Numbers: secondary Al against primary Cu: (J²τ)* = 3.93e19 (ICE) and 4.24e19 A²·s/m⁴ (Nuss), that is 1.24 and 1.34 full-load years at 1 A/mm² [a4]. Secondary against secondary: 6.3e18 (ICE) and 1.7e19 (Nuss) [a4].
- Revised (see section 9): "with primary Al the condition is never satisfied" depends on the source. x = 1.096 (MEMORY pair) and 1.152 (ICE virgin pair) give no crossover; x = 0.986 (Nuss primary pair) gives a crossover at D_c = 0.022, (J²τ)* = 6.8e17 A²·s/m⁴, 6.8e5 s at 1 A/mm² [a4] [s4-C]. The two primary sources straddle x = 1, so the sign of the embodied saving for primary Al at equal volume is not settled by the data. Either way primary Al pays only at very low duty.
- Revised: the planner's check "D > 1 wherever Al loses" is false in general. It holds only for x < 2 − κ = 0.362 [s4-C]. For the ICE recycled/recycled pair D_c = 0.74 and for the Nuss mix D_c = 0.42 [a4] [s4-C].
- Confidence: medium.
- Falsified by: a sign or crossover in a full comparison that differs from D_c.

**G2.5** Regimes where substitution pays while the incumbent is free to use the same geometry, each with an order-of-magnitude example.

| Regime | Condition | Example | Source |
|---|---|---|---|
| R1 envelope-free bulk conduction | index c^n/(ρ·e) favours g, or mass is the function's own constraint | Al busbar: 1.64 times the area, 0.49 times the mass; Σ*_Al/Σ*_Cu 0.45 to 0.50 with secondary Al, 1.27 to 1.37 with primary Al | [a1] [a3] |
| R2 bottleneck elsewhere | the solid's resistance is a fraction φ of the total; penalty φ·(κ^n − 1) | air-cooled fin, h = 50 W/(m²·K), 30 mm × 1 mm: Al delivers 6.3% less than Cu at 0.30 times the mass | [c1] [s4-F] |
| R3 low duty | D < D_c | Al at equal volume, secondary Al: below 1.2 to 1.3 full-load years at 1 A/mm² | [a4] |
| R4 activated kinetics, area route | area free and L < λ | roughness ratio equal to κ removes the overpotential penalty; price is mass and, beyond λ, a κ^(1/2) return | [d1] [d2] |
| R5 mechanism switch | G2.7 | heat pipe | [p1] |
| R6 function decoupling | G2.8 | metal mesh for a transparent conductor | [t1] |

- Confidence: medium.
- Falsified by: any example failing in its row.

**G2.6** Regimes where it does not pay: volume-capped, solid-limited, high duty. In an embodied-energy currency a scarce catalyst at mg/cm² loading is nearly free against operating dissipation.
- Equation: break-even overpotential penalty of a non-scarce catalyst Δη_be = e_x·m″_x/(j·τ) (V), m″_x = loading of x (kg/m²).
- Numbers at j = 5e3 A/m², τ = 2.88e8 s (80 000 h), 0.5 mg/cm² of Pt [d3] [s4-A]:

| Row of Nuss and Eckelman Table S38 | e_x, MJ/kg | Δη_be, mV |
|---|---|---|
| Pt TOTAL (supply mix, 23% secondary) | 243 000 | 0.84 |
| Pt primary, South Africa | 308 000 | 1.07 |
| Pt primary, Russia | 327 000 | 1.13 |
| Pt primary, Russia, upper 97.5% bound | 430 000 | 1.49 |
| Pt secondary | 11 900 | 0.04 |

- Which row applies: S2 read the "Pt TOTAL" row and S3 read the two primary-route rows of the same table; the mix reproduces the total to 0.2% (0.63·308 000 + 0.14·327 000 + 0.23·11 900 = 242 557) [s4-A]. For a comparison that asks what newly mined x costs, the primary rows apply (1.07 to 1.13 mV, 1.5 mV at the upper bound). For an average purchase the mix applies (0.84 mV). The conclusion is the same for every row.
- Ir (the anode catalyst in an acidic cell), loading 1 to 2 mg/cm² (MEMORY UNSURE): 1.2 to 2.4 mV; 3.1 mV at the upper bound of the Russian route [s4-A].
- Comparison: one decade of κ costs 30 to 118 mV [d1]. For the break-even to reach 30 mV the embodied value of x, or the reciprocal of the duty j·τ, would have to be 20 to 36 times larger (Pt rows above) [s4-A]. At the central duty that means a loading above 10 to 18 mg/cm² [s4-A].
- Consequence for the framework: if Σ_init is embodied energy, the scarcity of x is hardly priced, and a substitution that costs more than about 1 mV of overpotential at continuous duty loses. This is a finding about the currency, not about the gate. UNSURE until the Σ_init definition is read.
- Confidence: medium.
- Falsified by: a Σ_init definition that prices x more than about 20 times above its cumulative energy demand.

**G2.7** Mechanism switch (R5). Geometry pays when it moves the limiting resistance away from the solid's coefficient by enabling another transport mechanism.
- Equations: capillary limit Q_max = (ρ_l·σ_l·h_fg/μ_l)·(K·A_w/L_eff)·(2/r_eff) (W); k_eff = L_eff/(A_x·R_total) (W/(m·K)).
- Numbers (6 mm water heat pipe at 60 °C, wick k = 40 W/(m·K) UNSURE): merit number 3.29e11 W/m²; Q_max = 56 W; k_eff = 1.13e5, 1.07e5 and 4.8e4 W/(m·K) for wall k = 400, 200 and 16 W/(m·K), that is 283, 268 and 120 times solid Cu [p1].
- Revised (see section 9): the plan said a Cu envelope "gains nothing from being Cu". It gains little or much depending on the wick and the wall: the wall's share of the total resistance at wall k = 200 is 10.7% with wick k = 40, 23% with wick k = 100 and 37.5% with wick k = 200; with a wall of k = 16 it is 60% [p1]. The claim that stands: a pipe with a less scarce envelope still exceeds solid Cu by two orders of magnitude in effective conductivity.
- Not done: the worked example of Reay, Kew and McGlen was not reproduced. Fluid–wall compatibility (water with Al is excluded, MEMORY) is a threshold input.
- Confidence: medium-low.
- Falsified by: a measured heat pipe with a non-Cu envelope whose k_eff is below 10 times solid Cu at these dimensions.

**G2.8** Function decoupling (R6). Geometry pays when it separates in space two functions that x couples in one material.
- Equations: mesh sheet resistance R_s = 1/(σ·t·(w/p)) (Ω/sq); transmittance T = (1 − w/p)²; Haacke figure of merit T¹⁰/R_s.
- Numbers: Cu mesh, w/p = 0.025, t = 0.5 µm: 1.38 Ω/sq at T = 0.951, figure of merit 0.44 /Ω, against 0.010 to 0.070 /Ω for the indium tin oxide film cases [t1]. A Cu mesh matching the mid film (10 Ω/sq, T = 0.875) needs 27 nm thickness and 0.030 g/m² of Cu, against 0.79 g/m² of In [t1].
- Limits: the film values are the planner's UNSURE endpoints, not a lookup (Ellmer 2012 not read). The mesh model ignores diffraction and haze, and the minimum line width (a process input) was not supplied.
- Confidence: medium-low.
- Falsified by: a looked-up film figure of merit above the mesh values at a line width that can be made.

**G2.9** What remains of Class II otherwise: (a) thrifting x by raising its utilisation towards 1; (b) matched functions; (c) geometry that is material-independent (flow networks).
- Equation: x_min = F_req/(c_x at η_u = 1).
- Numbers that show the room for thrifting: a 1 mm Cd sheet in an isotropic thermal flux has f = 0.043, so about 96% of its atoms are idle; f = 0.9 needs 4.4 µm [n3]. A Cu strip 6.4 skin depths thick has η_u = 0.31 [b3]. An exchange-coupled magnet needs a hard-phase fraction of 0.10 to 0.24 (formula values, MEMORY inputs) [m4].
- Confidence: medium-high.
- Falsified by: standard practice already holding η_u ≥ 0.9 for the incumbent in every listed domain.

**G2.10** The fairness rule needs two amendments. (i) The admissible geometry set depends on the material through process limits (minimum feature, extrudability, weldability) and through the Σ_init of making the geometry, so the scenario must supply these per material. (ii) The rule cuts both ways: the candidate must also be allowed plain solid forms; a solid Al bar is a legitimate candidate.
- Evidence: none computed. Gate step 4 of the plan (the fair comparator) was not evaluated by any row [j1].
- Confidence: medium (reasoning only).
- Falsified by: a demonstration that process limits never change the admissible set in the three analysed cases.

## 3. G3: the Class I examples

Order as in the prompt: (2) photons, (1) neutrons, (3) storage, (4) magnets.

### Example (2): photon attenuation

**G3.1** Mass attenuation ratio W/C: 29.3 at 100 keV, 1.58 at 500 keV, 1.04 at 1 MeV, 1.52 at 5 MeV.
- Table relied on: NIST XCOM (Standard Reference Database 8), total attenuation with coherent scattering, Z = 6 and Z = 74, and NIST X-ray mass attenuation tables (Hubbell and Seltzer, NISTIR 5632) Table 3. Both were read on 2026-11-14 by S2 and, separately, by S3. No value here is from memory. The pages print no version number (UNSURE: XCOM 3.1).

| E, MeV | μ/ρ carbon, cm²/g | μ/ρ tungsten, cm²/g | W/C |
|---|---|---|---|
| 0.1 | 0.1514 | 4.437 (Table 3: 4.438) | 29.31 |
| 0.5 | 0.08715 | 0.1378 | 1.581 |
| 1.0 | 0.06362 (Table 3: 0.06361) | 0.06618 | 1.040 |
| 5.0 | 0.02708 | 0.04103 | 1.515 |

- Source: [f1]; the same eight values in [S3, Part 2b, row F1].
- Independent check: N_A·(Z/A)·σ_KN from the Klein–Nishina formula reproduces carbon's tabulated value to −0.18% at 0.5 MeV and −0.13% at 1 MeV [f1].
- Confidence: high.
- Falsified by: a different reading of the two NIST tables.

**G3.2** Class I membership of example (2) depends on the binding constraint. On a mass basis it fails over more than a decade of energy; on a thickness basis it holds at every energy.
- Equations: mass ratio for equal narrow-beam transmission m_C/m_W = (μ/ρ)_W/(μ/ρ)_C; thickness ratio (μ/ρ·ρ)_W/(μ/ρ·ρ)_C.
- Mass basis (restated, see section 9): W/C is below 2 from 0.403 MeV to 7.58 MeV [f2] (S3: 0.403 and 7.56 MeV [S3, Part 2b, row F2]). The lowest tabulated ratio is 0.965 at 1.5 MeV, and the ratio is below 1 from 1.16 to 2.02 MeV, where carbon needs less mass than tungsten [f2] [s4-D]. The minimum sits on a grid point, so its energy is only as good as the grid.
- Other light shields against W, lowest ratio at 1.5 MeV: water 0.869, concrete 0.946, Al 0.999, Fe 1.024; W/Fe stays below 2 from 0.41 to 55.7 MeV [f2].
- Thickness basis: the ratio never falls below 8.24 (graphite 2.26 g/cm³) or 10.96 (1.70 g/cm³); it is 250 to 333 at 100 keV; for a carbon lattice of relative density 0.1 to 0.5 the minimum is 16 to 110 [f3]. Graphite densities are MEMORY UNSURE.
- Confidence: high (mass basis), medium-high (thickness basis, densities unverified).
- Falsified by: a table reading that moves the crossings by more than 10% in energy.

**G3.3** The quoted law μ/ρ ∝ Z⁴/E³ is not what produces the quoted 25 to 30. The ratio 29.3 at 100 keV is tungsten's photoelectric absorption divided by carbon's Compton scattering.
- Numbers: at 100 keV carbon attenuates 96.8% by incoherent scattering (0.1466 of 0.1514 cm²/g); its photoelectric part is 0.00103 cm²/g. The photoelectric parts alone give W/C = 4 028. The fitted photoelectric exponents are Z^3.25 per unit mass (Z^4.34 per atom) at 100 keV over seven elements, and E^−2.65 for W from 100 to 500 keV [f4].
- So the law is roughly right for the photoelectric part and wrong as the reason for the quoted mass factor. The factor itself (25 to 30) is right at 100 keV.
- Confidence: medium-high.
- Falsified by: a per-mass Z exponent of 3.9 or more, or a carbon Compton fraction below 0.85 at 100 keV.

**G3.4** Geometry cannot reduce the areal mass needed for narrow-beam attenuation; voids and thickness variation only raise transmission. Broad-beam buildup penalises low Z further.
- Equation: E[exp(−μx)] ≥ exp(−μ·E[x]) (Jensen).
- Numbers: ratio ≥ 1 at every sweep point (smallest 1.0003) [f5]. Slab Monte Carlo, transmitted energy: carbon needs 1.16 times (T_E = 1e-2) and 1.14 times (1e-3) the areal mass of tungsten at 1 MeV, against 1.008 in a narrow beam with the same physics; at 0.5 MeV 1.96 and 1.88, against 1.49 [f6].
- Limits: the Monte Carlo neglects coherent scattering, fluorescence and electron transport, and its comparison with published buildup factors (ANSI/ANS-6.4.3-1991) was not run [f6]. Citing papers list both C and W among the standard's 23 elements [search]; the standard itself was not read.
- Confidence: high (Jensen), low (buildup numbers).
- Falsified by: a thickness distribution with lower mean transmission than the uniform slab; published buildup factors that differ from [f6] by more than a factor 1.5.

**G3.5** Inside Class I the retained element depends on the spectrum, and it need not be x.
- Numbers, μ/ρ in cm²/g (NIST XCOM) [f7]:

| E, keV | Sn | W | Pb | Bi | Gd | Ba | Leader |
|---|---|---|---|---|---|---|---|
| 40 | 19.43 | 10.67 | 14.36 | 14.95 | 6.92 | 24.57 | Ba |
| 60 | 6.565 | 3.713 | 5.020 | 5.233 | 11.75 | 8.511 | Gd |
| 80 | 3.029 | 7.809 | 2.419 | 2.522 | 5.573 | 3.963 | W |
| 100 | 1.677 | 4.437 | 5.549 | 5.737 | 3.109 | 2.195 | Bi |

- The plan's three-element ranking holds (Sn > Pb > W at 60 keV, W > Sn > Pb at 80 keV, Pb > W > Sn at 100 keV). Restated (see section 9): with Ba, Gd and Bi included the leader changes at every one of the four energies, and tungsten leads only at 80 keV. At the prompt's own 100 keV, lead and bismuth attenuate more per unit mass than tungsten (5.55 and 5.74 against 4.44). Tungsten's advantage there is density, which is a thickness argument.
- Consequence: Class I says "a high-Z element is needed", not "x is retained". Substitution of one heavy element by another with a K-edge just below the working energy is open, and the gate does not cover it.
- Confidence: medium-high.
- Falsified by: one element leading at all four energies.

### Example (1): neutron capture

**G3.6** The example is mislabelled. B-10 absorbs by (n,α) with a smooth 1/v cross-section; it is not a resonance absorber. Cd-113 and Gd-155/157 owe their thermal cross-sections to resonances near or below thermal energy; Hf, In and Ag are epithermal resonance absorbers.
- Equation: for a 1/v absorber the resonance integral above 0.5 eV is RI = 2·σ₀·sqrt(0.0253/0.5) = 0.450·σ₀.
- Numbers, RI/(0.450·σ₀): B-10 1.004, Li-6 1.007; natural Cd 0.057, natural Gd 0.018; Hf 42, In 36, Ag 27 [n2].
- Limits: the resonance integrals were computed by S2 from ENDF/B-VII.1 pointwise data, not read from a table; σ₀ is from Sears 1992. S3 found no published resonance integral for B-10 absorption.
- Confidence: high.
- Falsified by: a tabulated B-10 absorption resonance integral outside 0.95 to 1.05 times 0.450·σ₀.

**G3.7** For a compact thermal absorber Class I holds by dynamic range.
- Numbers (Sears 1992, thermal absorption at 2 200 m/s): B-10/C = 1.10e6; natural Cd/Al = 1.09e4 [n1]. Restated (see section 9): the ratio depends on the pair and on the basis. Over the pairs (Cd metal or natural B₄C) against (Al or graphite) and the bases per atom, per mass and per thickness, the smallest κ is 2.6e3 (Cd against Al, per mass); natural B against Al is 3.3e3 per atom [s4-E]. The plan's "κ ≥ 1e4" is too high for these pairs; "κ ≥ 2.6e3" holds.
- Confidence: high that no practical envelope tolerates a factor of this size.
- Falsified by: tabulated thermal cross-sections that differ by a factor of 2 from Sears 1992.

**G3.8** Geometry changes how much absorber is needed, in three ways.
- Self-shielding: a slab in an isotropic flux absorbs P = 1 − 2·E₃(τ), τ = Σ_a·t; the per-atom factor is f = P/(2τ). Numbers: f = 0.996, 0.837, 0.390, 0.164, 0.050 at τ = 0.001, 0.1, 1, 3, 10; Monte Carlo agrees at all 21 points [n3]. f = 0.9 needs τ = 0.051: 4.4 µm of Cd, 6.1 µm of natural B₄C, 0.34 µm of Gd, 0.15 mm of steel with 1 wt% B [n3].
- Saturation: a 1 mm sheet is black for Cd (τ = 11.7), natural B₄C (8.4) and Gd (150) [n3]. Where both absorbers stay black the weaker one is a free substitute.
- Moderation: a 1/v cross-section rises by sqrt(E/E_th), 6 287 times from 1 MeV to thermal; 18.2 collisions in H, 25.1 in D, 115.3 in C from 2 MeV to thermal [n4].
- Bulk shielding needs no scarce absorber: water alone attenuates a thermal flux by 1e-3 in 19.7 cm, at 38 times the areal mass and 333 times the thickness of a Cd sheet [n5]. Order of magnitude only: the Cd sheet is a beam at 2 200 m/s and the water value is a diffusion asymptote; the diffusion length 2.85 cm is from an LLNL handbook table, and measured values are 2.73 to 2.77 cm [S3, Part 1, row 20].
- Confidence: medium-high.
- Falsified by: a transport calculation of a slab in isotropic flux that departs from 1 − 2·E₃(τ).

**G3.9** The scarce element in typical absorber choices is not boron.
- Numbers, crustal abundance in mg/kg: B 10 against Gd 6.2, Hf 3.0, In 0.25, Cd 0.15, Ag 0.075 [n6]. These are the planner's values; they equal a Wikipedia copy of the CRC Handbook table (85th ed.) for all 18 elements with both values, so the check is not independent [n6] [S3, Part 1, row 23]. The narrowest margin is B/Gd = 1.6.
- World production 2025 (USGS Mineral Commodity Summaries 2026, hand-transcribed): Cd 23 000 t, Ag 26 000 t, In 1 100 t; no world total is published for B, Hf or the individual rare earths [n6].
- Scarce inputs in practice: Ag and In in Ag–In–Cd, Hf, Gd, Dy, Eu, and isotopically enriched B-10 (not covered by any data read here: UNSURE).
- Confidence: medium.
- Falsified by: the CRC table read directly giving boron below Cd, Ag, In, Hf or Gd.

### Example (3): stored energy

**G3.10** For stored energy this is a mechanism question, not a geometry question. Bulk faradaic storage scales with the number of host atoms; double-layer storage scales with the number of surface sites. Geometry reaches its ceiling when every carbon atom is a surface atom.
- Equations: cell reaction with n electrons at voltage V: n·F·V/M (J/kg); per atom n·F·V/(N_at·N_A). Double layer, symmetric cell: ½·(C_sp/4)·V² per kg of both electrodes; C_sp = C_dl·SSA.
- Numbers [h12]: geometric surface area of graphene 2 627 m²/g; with 21 µF/cm² the ceiling is 552 F/g per electrode.

| System | eV per atom of active material |
|---|---|
| 4Li + 2SOCl₂, 3.65 V | 1.217 |
| Zn + 2MnO₂, 1.5 V | 0.429 |
| LiCoO₂ + 3C at 0.5 Li, 3.7 V | 0.308 |
| LiFePO₄ + 6C, 3.3 V | 0.254 |
| Pb + PbO₂ + 2H₂SO₄, 2.05 V | 0.228 |
| Double layer, 100 F/g, 1.0 V | 0.00156 |
| Double layer, 100 F/g, 2.7 V | 0.0113 |
| Double layer, geometric ceiling, 2.7 V | 0.0626 |
| Double layer, geometric ceiling, 4.0 V | 0.137 |

- The prompt's figures mix bases: "1 to 4 eV" is energy per transferred electron (the cell voltage); per atom of reactants it is 0.23 to 1.22 eV. "0.002 eV/atom" matches a 100 F/g carbon near 1 V.
- Gap, redox over double layer, per atom (restated, see section 9): 22 to 780 in practice (LiFePO₄ against 2.7 V; Li/SOCl₂ against 1.0 V); 4.1 to 19 at the 2.7 V geometric ceiling; 1.8 to 9 at a 4.0 V ceiling [h12]. The ceiling excludes electrolyte, separator and collectors.
- Limits: cell voltages and atomic masses are MEMORY; the handbook value for Li/SOCl₂ was not read (computed 1 473 Wh/kg). The attribution of 21 µF/cm² to Xia et al. 2009 is UNSURE: the abstract does not state it, and 550 F/g appears only in citing works [S3, Part 3, entry 42] [search].
- Confidence: medium-high (structure), medium (numbers).
- Falsified by: a double-layer electrode with more than 0.14 eV per carbon atom at 4 V without a faradaic contribution.

**G3.11** "Primary cell against double-layer capacitor" is a category error: a capacitor holds no energy as manufactured. On the fair function (deliver energy E in time t per unit mass) the ranking reverses below a discharge time t* ≈ E_c/P_b. Rate capability is geometric; capacity and voltage are not.
- Numbers: t* = 14.4 s for the central inputs, 4.8 to 96 s over 16 corner cases [h3]. All inputs are MEMORY UNSURE; the two Ragone models differ by up to a factor 2.46 at the corners; Christen and Carlen 2000 was not read [h3].
- Confidence: medium-low.
- Falsified by: measured Ragone curves of commercial cells crossing outside 1 to 1 000 s.

### Example (4): magnets

**G3.12** Invariant part: spontaneous magnetisation M_s(T), Curie temperature, anisotropy constant K₁, exchange stiffness. Geometric part: coercivity, remanence ratio, loop squareness.
- Equations: (BH)max ≤ μ₀·M_s²/4 (J/m³). Shape anisotropy alone (aligned needles at packing p, coherent rotation): H_c = (1 − p)·M_s/2, and (BH)max ≤ μ₀·M_s²/12 at p = 2/3. Hardness parameter κ_h = sqrt(K₁/(μ₀·M_s²)); a magnet of arbitrary shape needs κ_h > 1.
- Numbers: ceilings μ₀M_s²/4: Nd₂Fe₁₄B 516, Ba ferrite 45.8, Fe 920, Fe₆₅Co₃₅ 1 194 kJ/m³ [m12]. Shape-anisotropy ceiling: the grid maximum is 1/12 at p = 0.667; 398 kJ/m³ for Fe₆₅Co₃₅ (2.45 T), 306 kJ/m³ for Fe [m3]. κ_h: Nd₂Fe₁₄B 1.54, SmCo₅ 4.35, Ba ferrite 1.34, Fe 0.114 [m12]. Realised over ceiling: NdFeB 0.92, ferrite 0.87, Alnico 9 0.22 of μ₀M_s²/4 (realised values MEMORY; Alnico 5 saturation used for Alnico 9) [m12].
- Published support found in this stage: the abstract of Skomski et al. 2010 gives μ₀M_s²/12 at packing fraction 2/3 as the bulk limit [search]. Skomski and Coey 2016 define κ with the square root [search]. Both are search-result readings, not readings of the papers.
- Limits: the μ₀M_s and K₁ inputs are from a secondary review (Granados-Miralles et al., arXiv:2310.02106, Table 1), not from Coey's tables. The [m3] grid check is a check of the numerics, not of the model.
- Confidence: high (μ₀M_s²/4), medium (shape ceiling).
- Falsified by: a shape-anisotropy magnet above μ₀M_s²/12.

**G3.13** Exchange-coupled two-phase magnets thrift the rare earth; they do not replace it.
- Equations (Skomski and Coey 1993, equation numbers UNSURE): hard-phase fraction f_h = μ₀·M_s²/(4·K_h); (BH)max = (μ₀·M_s²/4)·(1 − μ₀·(M_s − M_h)·M_s/(2·K_h)); soft regions below about twice the hard-phase wall width π·sqrt(A/K_h).
- Numbers (MEMORY inputs): Sm₂Fe₁₇N₃ with Fe₆₅Co₃₅: f_h = 0.098, 1 091 kJ/m³; Nd₂Fe₁₄B with Fe₆₅Co₃₅: f_h = 0.24, 985 kJ/m³, wall width 4.0 nm [m4].
- Published support: the abstract of Skomski and Coey 1993 gives 1 MJ/m³ (120 MG Oe) for a multilayer of 2.4 nm Sm₂Fe₁₇N₃ and 9 nm Fe₆₅Co₃₅ with 5 wt% rare earth [search]. The plan's "1 090 kJ/m³ at 9%" was not seen and stays UNSURE; the agreement of [m4] with it is not independent, because the inputs are the planner's.
- Confidence: medium (formula), low (that such a magnet can be made; no realised value was looked up).
- Falsified by: the paper's own numbers differing from [m4] by more than 10%.

**G3.14** At device level a magnet is compensable: magnet volume ∝ 1/(BH). Of the four Class I examples this is the weakest.
- Equation: V_m = B_g²·V_g/(μ₀·abs(BH)) (m³), ideal iron, no leakage.
- Numbers: ferrite (31.8 kJ/m³) against NdFeB (345 kJ/m³) for the same gap: 10.8 times the volume and 7.1 times the mass; the ferrite operates at 155 kA/m against a coercivity of 250 to 400 kA/m (MEMORY UNSURE) [m5].
- The function is Class I only when volume or mass is capped below these factors, when the demagnetising field exceeds the candidate's coercivity, or when the operating temperature exceeds its Curie temperature.
- Limits: the optimiser and the formula share the same equations (near-identity); leakage and fringing are not modelled [m5].
- Confidence: high (scaling), medium (numbers).
- Falsified by: a magnetic-circuit optimisation with leakage that differs from the formula by more than 5%.

## 4. G4 and G5 claims

**G4.1** The gate must classify a triple (function, operating regime, binding envelope), not a function and not only a (function, regime) pair. "Envelope" has to include the requirement margin, and the pair (g, s) must be named.
- Evidence: the same function and regime changes class with the envelope: photon attenuation at 1 MeV is Class II with a mass cap of 3 (price 1.04 to 1.16) and Class I with a thickness cap of 3 (price 8.9 to 11.8) [j1]; ferrite for NdFeB is Class I with a volume cap of 2 and Class II with volume free (price 10.8) [j1]; an Al winding is Class I under "loss ≤ incumbent's loss" and undecided under "within the temperature limit" until the incumbent's margin is known (Class II only if its rise is below 0.61 of the limit) [j1] [s4-F].
- Confidence: high.
- Falsified by: a listed example whose class is the same for every regime and envelope.

**G4.2** Revised (see section 9). The plan's claim was that its 5-step procedure is decidable from scenario inputs and reproduces the expected class in all 18 test cases. Its own falsifier fired: 13 of 18 matched, 5 were undecided because an input was missing (cases 4, 8, 14, 16, 17), and none landed on the opposite class [j1].
- Restated claim: the revised procedure of section 8 returns either a class or "out of scope: incomplete" with the missing input named. Applied to the same 18 cases it returns the expected class in 13, "incomplete" in 5, and the opposite class in none [s4-G]. With the missing input added: case 4 is Class I for any cap below 2.6e3 times the incumbent's usage; case 8 is Class II with g = double layer at the central inputs; case 17 is Class I if the instability of the candidate in acid is confirmed; cases 14 and 16 take either class depending on the incumbent's margin and on which quantity is capped [s4-G]. Those completions are illustrations, not results.
- Limits: the cases and their expected classes were written by the planner, so this is a consistency test and not an independent one. Cases 12 and 18 are decided by their own premise and test no number [j1].
- Confidence: medium-low.
- Falsified by: a complete scenario for which the procedure returns no outcome, or an outcome that a constrained Σ comparison contradicts.

**G4.3** The gate is a feasibility and threshold pre-check. A correctly constrained Σ comparison would deliver the same result (as infeasible, or as Σ_g far above Σ_s). The gate saves work; it is not an independent physical principle.
- Evidence: reasoning only. No Σ comparison was run on a Class I case. In [j1] every Class II outcome is "the price test passed"; the plan's steps 4 and 5 changed no class.
- Confidence: medium-low (untested).
- Falsified by: a Class I case that the constrained comparison ranks in favour of g.

**G5.1** Verdict: valid with restated scope (section 7). No result moved the verdict towards "invalid" or towards "valid as written".
- Against "valid as written": W/C is below 2 at three of the prompt's four energies [f1]; magnets and bulk neutron shields are compensable when volume is free [m5] [n5]; some Class II substitutions pay [a3] [p1] [t1].
- Against "invalid": the compact-absorber and 100 keV examples keep prices of 2.6e3 and 29, which no stated envelope absorbs [s4-E] [f1]; the threshold step decides cases no price can (cases 9 and 12) [j1].
- Confidence: medium.

## 5. Citations

Only sources that a claim above relies on. "Status" says what was actually read. P: primary table or paper read by S2 or S3. S: secondary copy or search result. N: not read; the citation is from memory and its locator is UNSURE.

| Author, year | Title and source | Table, equation or page | Used in | Status |
|---|---|---|---|---|
| Berger, Hubbell, Seltzer et al., 1987 (online 2010) | XCOM: Photon Cross Sections Database, NIST Standard Reference Database 8 | total and partial cross-section tables, Z = 6, 13, 26, 29, 50, 56, 64, 74, 82, 83 | G3.1 to G3.5 | P (web form, 2026-11-14; version not printed) |
| Hubbell and Seltzer, 1995 | Tables of X-Ray Mass Attenuation Coefficients and Mass Energy-Absorption Coefficients, NISTIR 5632 | Table 3 (elements), Table 4 (water, concrete), Table 1 (densities, Z/A) | G3.1, G3.2 | P (NIST web tables) |
| Klein and Nishina, 1929 | Über die Streuung von Strahlung durch freie Elektronen nach der neuen relativistischen Quantendynamik von Dirac, Z. Phys. 52, 853–868 | total cross-section formula (equation number UNSURE) | G3.1 check | record verified; formula reproduced tables to 0.2% |
| American Nuclear Society, 1991 | ANSI/ANS-6.4.3-1991, Gamma-Ray Attenuation Coefficients and Buildup Factors for Engineering Materials | buildup tables for C and W (table numbers UNSURE) | G3.4 | N; coverage of C and W from citing papers only (S) |
| Jensen, 1906 | Sur les fonctions convexes et les inégalités entre les valeurs moyennes, Acta Math. 30, 175–193 | the inequality | G1.8, G3.4 | record verified |
| Sears, 1992 | Neutron scattering lengths and cross sections, Neutron News 3(3), 26–37 | Table 1, absorption at 2 200 m/s | G3.6 to G3.8 | P (NIST NCNR web copy) |
| Chadwick et al., 2011 | ENDF/B-VII.1 Nuclear Data for Science and Technology: Cross Sections, Covariances, Fission Product Yields and Decay Data, Nucl. Data Sheets 112, 2887–2996 (citation from memory, UNSURE; S2 used the pointwise data from NNDC Sigma) | reconstructed cross-sections, MT 102, 103, 105, 107 | G3.6 | P for the data files; the resonance integrals are S2's own integration |
| Mughabghab, 2003 | Thermal neutron capture cross sections, resonance integrals and g-factors, INDC(NDS)-440 | capture tables | G3.6 cross-check by S3 | P (capture channel only; no B-10 (n,α)) |
| LLNL / NCSP | Hand Calculation Methods for Nuclear Criticality Safety; year and report number UNSURE | Table 2-2 (L and D for water) | G3.8 | P for the table; its textbook origin UNSURE |
| U.S. Geological Survey, 2026 | Mineral Commodity Summaries 2026 | commodity pages | G3.9 | P (hand-transcribed) |
| Haynes (ed.), 2016 | CRC Handbook of Chemistry and Physics, 97th ed. | section 14, Abundance of Elements in the Earth's Crust and in the Sea | G3.9 | N; a Wikipedia copy of the 85th ed. values was used (S) |
| International Electrotechnical Commission, 2004 | IEC 60228, Conductors of insulated cables, ed. 3.0 | Table 2, class 2, maximum DC resistance | G1.3 | P (publisher preview PDF) |
| Hammond and Jones, 2011 | Inventory of Carbon and Energy (ICE), Version 2.0, University of Bath | Summary Tables, aluminium and copper rows | G2.3, G2.4 | P |
| Nuss and Eckelman, 2014 | Life cycle assessment of metals: a scientific synthesis, PLoS ONE 9(7), e101298 | Supporting Information S1, Table S38, column "CED [MJ/kg]" | G2.3, G2.4, G2.6 | P |
| Thomson (Kelvin), 1881 | On the economy of metal in conductors of electricity, Report of the British Association, 51st meeting | pp. 526–528 | G2.2 | record verified, text not read |
| Dowell, 1966 | Effects of eddy currents in transformer windings, Proc. IEE 113(8), 1387–1394 | AC resistance factor (equation number UNSURE) | G1.4 | record verified, text not read |
| Incropera, DeWitt, Bergman, Lavine, 2007 | Fundamentals of Heat and Mass Transfer, 6th ed. | Table A.4 (air at 300 K) | G1.5 | S (scanned appendix, edition not printed) |
| Schmidt, 1926 | Die Wärmeübertragung durch Rippen, Z. VDI 70, 885–889 and 947–951 | optimum fin | G1.5 | record verified; 1.4192 seen only in secondary sources |
| Hashin and Shtrikman, 1962 | A variational approach to the theory of the effective magnetic permeability of multiphase materials, J. Appl. Phys. 33, 3125–3131 | bounds (equation number UNSURE) | G1.8 | record verified, text not read |
| Newman and Tobias, 1962 | Theoretical analysis of current distribution in porous electrodes, J. Electrochem. Soc. 109, 1183–1191 | penetration depth | G1.7 | record verified, text not read |
| Gilliam, Graydon, Kirk, Thorpe, 2007 | A review of specific conductivities of potassium hydroxide solutions for various concentrations and temperatures, Int. J. Hydrogen Energy 32, 359–364 | conductivity correlation | G1.7 | S (coefficients from citing works) |
| Cengel and Cimbala, 2014 | Fluid Mechanics: Fundamentals and Applications, 3rd ed. | Table A-3, saturated water at 60 °C | G2.7 | P (substitute for Incropera Table A.6) |
| Haacke, 1976 | New figure of merit for transparent conductors, J. Appl. Phys. 47, 4086–4089 | T¹⁰/R_s | G2.8 | record verified, text not read |
| Ellmer, 2012 | Past achievements and future challenges in the development of optically transparent electrodes, Nature Photonics 6, 809–817 | film resistivity and transmittance | G2.8 | N (film values are MEMORY) |
| Granados-Miralles, Saura-Múzquiz, Andersen; year UNSURE (arXiv number implies 2023) | Permanent magnets based on hard ferrite ceramics, arXiv:2310.02106 | Table 1 (B_s, K₁ at room temperature) | G3.12 | P for the table; it is a secondary review whose own source was not identified |
| Skomski and Coey, 2016 | Magnetic anisotropy: how much is enough for a permanent magnet?, Scripta Materialia 112, 3–8 | definition of κ; Table 1 | G3.12 | S (definition from search results; Table 1 not read) |
| Skomski, Liu, Shield, Hadjipanayis, Sellmyer, 2010 | Permanent magnetism of dense-packed nanostructures, J. Appl. Phys. 107, 09A739 | abstract: μ₀M_s²/12 at packing fraction 2/3 | G3.12 | S (abstract as returned by search) |
| Skomski and Coey, 1993 | Giant energy product in nanostructured two-phase magnets, Phys. Rev. B 48, 15812–15816 | abstract: 1 MJ/m³; formulas (equation numbers UNSURE) | G3.13 | S (abstract as returned by search); formulas from memory |
| Stoner and Wohlfarth, 1948 | A mechanism of magnetic hysteresis in heterogeneous alloys, Phil. Trans. R. Soc. A 240, 599–642 | shape-anisotropy coercivity | G3.12 | record verified, text not read |
| Xia, Chen, Li, Tao, 2009 | Measurement of the quantum capacitance of graphene, Nature Nanotechnology 4, 505–509 | 21 µF/cm² (location in the paper UNSURE) | G3.10 | record verified; the cited numbers not confirmed |
| Christen and Carlen, 2000 | Theory of Ragone plots, J. Power Sources 91, 210–216 | matched-load relation | G3.11 | record verified, text not read |
| Linden and Reddy (eds.), 2002 | Handbook of Batteries, 3rd ed. | Table 1.2 | G3.10 | N |
| Reay, Kew, McGlen, 2014 | Heat Pipes: Theory, Design and Applications, 6th ed. | capillary limit, merit number | G2.7 | N |
| Pourbaix, 1974 | Atlas of Electrochemical Equilibria in Aqueous Solutions, 2nd English ed. | diagrams for Ni and Fe | gate case 17 | N; no datum was looked up |

Bibliographic records marked "record verified" were checked against Crossref by S3 [S3, Part 3].

## 6. Not verified

These items were not confirmed by any stage. A claim that leans on one says so.

1. The framework's definition of Σ_init. All of G2.3, G2.4 and G2.6 use cumulative energy demand in its place.
2. Thermal conductivities of Cu, Al, 6063 and AlSi10Mg; densities of AlSi10Mg, graphite, B₄C and steel; metal-foam specific area [S3, Part 1, rows 9, 10, 12, 14, 17].
3. The buildup comparison with ANSI/ANS-6.4.3-1991 (G3.4).
4. A published resonance integral for B-10 absorption (G3.6).
5. Cell voltages, the handbook specific energy of Li/SOCl₂, activated-carbon capacitance and all Ragone inputs (G3.10, G3.11).
6. The location of 21 µF/cm² in Xia et al. 2009, and the origin of 550 F/g (G3.10).
7. μ₀M_s and K₁ from Coey's own tables; realised (BH)max values; coercivity of ferrite and NdFeB grades (G3.12, G3.14).
8. "1 090 kJ/m³ at 9%" in Skomski and Coey 1993, and the Sm₂Fe₁₇N₃ inputs (G3.13).
9. Indium tin oxide film data (G2.8); the Reay heat-pipe worked example and the wick conductivity (G2.7).
10. The Pourbaix stability of Ni–Fe oxides in acid at the oxygen-evolution potential (gate case 17). No row looked it up.
11. Cycle life of double-layer and Li-ion cells (gate case 8).
12. Crustal abundances from the CRC Handbook itself (G3.9).
13. Several "published" check values in the magnet and storage rows are the planner's memory. Where a computed value agrees with them (κ_h, 1 090 kJ/m³, 1 470 Wh/kg), the agreement is weak evidence.
14. The exponent 5 for pumping power against heat-transfer coefficient in a developing laminar boundary layer (G1.5).

## 7. Verdict paragraph

**Valid with restated scope.** The demarcation as written does not hold. "Transport-governed" does not separate the classes: photon attenuation and thin-absorber neutron capture are linear transport with the same 1/coefficient compensation law as conduction (G1.1), and viscous flow has no coefficient of x at all (G1.6). No listed function is Class I in every regime: on a mass basis tungsten is within a factor 2 of carbon from 0.40 to 7.6 MeV and carbon is better from 1.16 to 2.02 MeV (G3.2); bulk neutron shields and black absorbers need no scarce absorber (G3.8); a magnet is compensable at 11 times the volume (G3.14); below a discharge time of order 5 to 100 s the storage ranking reverses (G3.11, inputs unverified). What does hold is a pre-check on a (function, regime, envelope) triple. The three null results reported in the prompt are what the monotonicity and separability lemmas predict for monotonic, separable, solid-limited cases (G2.1, G2.2); they do not show that Class II substitution never pays. It pays where the envelope is free and the material index favours the candidate, where the bottleneck is elsewhere, at low duty, by a switch of transport mechanism, and by spatial decoupling of two functions (G2.5, G2.7, G2.8); the last two rest on unverified inputs.

Restated demarcation (3 sentences):

1. A (function, regime, envelope) triple is Class I when the candidate fails an intensive threshold that no geometry enters, or when the extra mass, volume, area or loss that the governing equation demands to make up κ does not fit inside the stated envelope and requirement margin; otherwise it is Class II.
2. In Class II, under the fairness rule, geometry cancels wherever the function separates as coefficient times shape factor, so the outcome is decided by a material index c^n/(ρ·e) and by duty; geometry changes the outcome only through a truncated envelope, material-specific process limits, a switch of transport mechanism, or spatial decoupling of two functions that x couples.
3. Geometry's own general contribution is to raise the utilisation of whichever material is used towards its per-atom limit, which reduces the amount of x and does not replace it.

What would still change the verdict: a Σ_init definition that prices scarcity far above embodied energy (G2.6); a constrained Σ comparison that contradicts a Class I outcome (G4.3); an independent set of test scenarios on which the procedure of section 8 fails (G4.2).

## 8. Proposed gate procedure

Unit of classification: one triple (function, operating regime, binding envelope) for a named pair (g, s). Outcomes: Class I (retain x), Class II (compare), out of scope. "Out of scope" carries a reason: N (not a substitution question) or U (scenario incomplete; the missing input is named and the scenario goes back to its author).

**Inputs the scenario supplies.**

- (a) g, s and x by name. The function as a requirement F ≥ F_req (or F ≤ F_req) with units, the quantity held equal, and the incumbent's delivered value F_s.
- (b) The regime: temperature, frequency or spectrum, chemical environment, applied fields, and the state required at delivery.
- (c) The envelope: for each capped quantity (mass, volume or thickness, footprint, auxiliary power, loss) the cap and the incumbent's usage; or the statement "nothing capped".
- (d) The governing equation and the coefficient c through which x acts, with c_s and c_g at the regime: demonstrated values for both, and for g also the ceiling value at utilisation 1.
- (e) For each threshold of step 2 that the regime activates, the datum for g.
- (f) Process limits per material (minimum feature size and the like).

**Steps.**

1. **Scope.** If any of input (a) or (d) is missing: out of scope (U). If no property of the solid enters the governing equation for F, so that the geometry acts on a shared medium: out of scope (N). If F cannot be written as one requirement that both g and s can be tested against: out of scope (N). Whether g survives the incumbent's environment is not tested here; it is a threshold (step 2).
2. **Threshold.** Check each intensive condition that the regime activates and that contains no geometry: (i) operating temperature against the Curie, melting or decomposition temperature of g; (ii) chemical stability of g in the stated environment; (iii) a required edge, line, resonance or gap energy; (iv) the state required at delivery (for example, holds its energy without a charger for the shelf time); (v) an applied field or stress against the intrinsic limit of g, taken as the best value any admissible microstructure and shape can give. If g fails one: **Class I**. If an activated condition has no datum: out of scope (U). A life requirement (cycles, hours) is not a threshold; it goes to the replacement term of Σ unless the scenario forbids replacement.
3. **Compensation price.** For each way g can make up the deficit, compute the price π_q: the amount of quantity q that the smallest admissible g needs to meet F_req, divided by the incumbent's usage of q. Use the basis of the cap (per mass, per volume or thickness, per area). Use demonstrated coefficients on both sides to decide; record the price with the ceiling value of c_g beside it. Screening values: π = κ for bulk-limited transport and for attenuation; κ^(1/2) for a thick penetration-limited part; 1 for a saturated (black) part. Between those limits evaluate the regime function itself (tanh ξ/ξ for a fin or porous electrode, the Dowell factor for a strip, 1 − 2·E₃(τ) for an absorber sheet); do not pick an exponent. For activated kinetics the price is the loss Δη = b·log₁₀κ.
4. **Envelope test.** Slack of a capped quantity is cap divided by the incumbent's usage; it is at least 1, because the incumbent fits its own cap. A quantity the scenario declares free has infinite slack; a quantity it does not name is treated as free and is listed in the result as an assumption. The requirement margin F_s/F_req counts as slack in the function. If some compensation route has π ≤ 1: pass. Otherwise, if the scenario makes no envelope statement at all, or states the requirement as a limit without the incumbent's margin: out of scope (U). If every compensation route has π above the slack of some capped quantity: **Class I**. Otherwise pass.
5. **Class II and hand-off.** Define s′, the incumbent with the best admissible geometry within its own process limits (the thrifted-x option). Record each geometry feature of g that s′ cannot use, with the reason. Pass g, s′ and the duty ratio D to the Σ comparison. The result is **Class II**; the gate says nothing about which side wins. Report with the class: the deciding step, the basis of κ, the quantities assumed free, and whether the ceiling value of c_g would change the class.

**How this settles the wording problems found in the test matrix** (numbering of the Row J1 issue list in `outputs/issues.md`).

| # | Problem | Resolution in the procedure above |
|---|---|---|
| 1 | Unstated envelope read as "out of scope" would also throw out threshold cases | The threshold step comes before any envelope input. A missing envelope returns U at step 4, and only when the price exceeds 1. |
| 2 | Slack ≥ 1 was assumed, not stated | Stated in step 4. |
| 3 | "Free" caps | "Free" applies to the named quantity only. Unnamed quantities are treated as free and listed. This is a risk the reader of a result must see: a mass cap at the incumbent's usage would turn cases 5 and 11 into Class I (prices 38 and 7.1) [j1]. |
| 4 | Stoichiometric bound sat in step 2 but needs the cap | Moved to step 3 as the ceiling value of c_g. The demonstrated value decides; the ceiling is recorded. Case 7: 33 demonstrated; 2.76 at a 2.7 V ceiling and 1.26 at a 4.0 V ceiling, against a slack of 2 [j1]. |
| 5 | Case 9 could exit at step 1 or step 2 | Step 2 (iv), state at delivery. Step 1 no longer has an environment clause. |
| 6 | Steps 1 and 2 overlapped for case 17 | Same change: stability in the stated environment is step 2 (ii) only. |
| 7 | Choice of n for short fins and thin sheets | No choice is made: the regime function is evaluated. Case 16: 1.067 at mL = 0.47, not the thick-fin value 1.414 [s4-F]. |
| 8 | Which thresholds to check | A fixed list of five; the scenario states which the regime activates; an activated one without a datum returns U. |
| 9 | Which of the pair is g | Input (a). |
| 10 | Basis of κ | The basis of the cap; demonstrated values decide. |
| 11 | Cases decided by their own premise (12, 18) | Not a wording problem and not resolved. These cases need real data (a Curie temperature; a wall property that enters the flow problem) to be tests. |
| 12 | Steps 4 and 5 changed no class | Merged into one hand-off step. |

**What the procedure does not settle.** It gives no default envelope: a default of "free" turns Class I cases into Class II and a default of "at the incumbent's usage" does the reverse, and the matrix contains both flips (cases 4, 5, 11, 14, 16) [j1] [s4-G]. It does not cover replacing x by another scarce element (G3.5). It does not say how Σ_init prices scarcity (G2.6).

## 9. Changed since plan

Claims revised because a result contradicted them:

1. **G3.2, upper end of the interval.** Plan: W/C below 2 from about 0.4 to about 6 MeV. Result: 0.403 to 7.58 MeV [f2]; S3 agrees (7.56 MeV).
2. **G3.2, minimum.** Plan: near 1.0 (0.98 to 1.05) at 1.5 to 2 MeV. Result: 0.965 at 1.5 MeV; carbon is better per unit mass from 1.16 to 2.02 MeV [f2] [s4-D].
3. **G2.4, primary aluminium.** Plan: no crossover with primary Al at equal volume. Result: true for the MEMORY and ICE pairs, false for the Nuss primary pair (crossover at D = 0.022) [a4] [s4-C]. The claim is now conditional on the source.
4. **G2.4, the check "D > 1 wherever Al loses".** False in general; it holds only for x < 0.362 [a4] [s4-C]. Replaced by D > D_c = (1 − x)/(κ − 1).
5. **G1.7, validity of the Tafel form.** Plan: valid for η_s > 100 mV. Result: fails by up to 104 mV when area compensation brings η_g below the Tafel range [d1]. Now: both overpotentials above 104 mV (353 K) or 84 mV (298 K) for α = 0.5 [s4-B]. The kinetics are written with separate α_a and α_c.
6. **G1.4 and the plan's derivation D2, door (a).** Plan: the same-geometry penalty lies between κ^(1/2) and κ. Result: for the skin effect it dips to 1.216, below κ^(1/2) = 1.280 [b3]. The bound is kept for the tanh problems only.
7. **G2.6, platinum.** Plan: e_x ≈ 2.4e5 MJ/kg, Δη_be ≈ 1 mV. S2 read the supply-mix row (2.43e5), S3 the primary rows (3.08e5, 3.27e5). Both are right; they are different rows [s4-A]. The claim now gives 0.84 mV (mix) and 1.07 to 1.13 mV (primary), 1.5 mV at the upper bound. The conclusion does not change.
8. **G3.5.** Plan: ranking among Sn, W, Pb. Holds. Added: with Ba, Gd and Bi the leaders are Ba (40 keV), Gd (60 keV), W (80 keV), Bi (100 keV) [f7]; the claim now says that Class I does not fix which heavy element is retained.
9. **G3.7 and gate case 4.** Plan: κ ≥ 1e4. Result: natural B against Al is 3.3e3 per atom, and the smallest value over pairs and bases is 2.6e3 [s4-E].
10. **G4.2.** Plan: the procedure reproduces all 18 cases. Result: 13 of 18; 5 lacked an input [j1]. The claim is restated for the revised procedure, which returns "incomplete" for those 5 [s4-G].
11. **Gate procedure (plan section 5).** Environment clause removed from step 1; five named threshold types; the stoichiometric bound moved to the price step as a ceiling value; exponent choice replaced by evaluation of the regime function; explicit slack ≥ 1, "free" and "unnamed" rules; requirement margin added as an input; an "incomplete" reason added to out of scope; plan steps 4 and 5 merged.
12. **G4.1.** The unit of classification now includes the requirement margin and the named pair.
13. **G2.7.** Plan: a Cu envelope "gains nothing from being Cu". Result: the wall's share is 6 to 60% depending on wall and wick conductivity [p1]. The claim is narrowed. Confidence lowered to medium-low.
14. **G1.2.** A fourth type (matched functions) is listed with the three of the plan.

Numbers updated, claim unchanged:

15. G2.3: Σ*_Al/Σ*_Cu for primary metals 1.27 to 1.37 from the looked-up values, against 1.34 from memory [a3].
16. G1.3: the IEC table gives 1.65 to 1.68, against 1.64 from conductivities [a1].
17. G3.3: the photoelectric ratio W/C at 100 keV is 4 028, against "order 10³" [f4].
18. G3.4: buildup penalty 1.14 to 1.16 at 1 MeV (inside the plan's 1.1 to 1.4); 1.88 to 1.96 at 0.5 MeV is new [f6].
19. G3.8: water against Cd 38 times the areal mass and 333 times the thickness, against "about 40" and "about 300" [n5].
20. G3.10: redox range 0.23 to 1.22 eV/atom (plan 0.26 to 1.2); gap 22 to 780 in practice and 4.1 to 19 at the 2.7 V ceiling (plan 20 to 800 and 4 to 20) [h12].
21. G3.12: Fe₆₅Co₃₅ read as 2.45 T, giving 398 kJ/m³ for the shape ceiling (plan 390) [m3]; κ_h of Fe 0.114 (plan 0.12) [m12].

Status of sources changed in this stage (search results, secondary):

22. G3.12: the μ₀M_s²/12 limit at packing 2/3 is stated in the abstract of Skomski et al. 2010. The plan had it as the planner's own derivation, UNSURE as a published result.
23. G3.12: Skomski and Coey 2016 use the square-root form of κ.
24. G3.13: the abstract of Skomski and Coey 1993 gives 1 MJ/m³ for a 2.4 nm / 9 nm multilayer with 5 wt% rare earth. "1 090 kJ/m³ at 9%" stays UNSURE.
25. G3.4: ANSI/ANS-6.4.3-1991 covers both C and W according to citing papers. The comparison itself is still not run.
26. G3.10: the 21 µF/cm² and 550 F/g attribution to Xia et al. 2009 stays UNSURE.

Confidence lowered: G2.7 and G2.8 (medium to medium-low), G3.11 (medium to medium-low), G4.2 and G4.3 (medium to medium-low).

Claims that stand as planned: G1.1, G1.3, G1.5, G1.6, G1.8, G2.1, G2.2, G2.5, G2.9, G2.10, G3.1, G3.6, G3.9, G3.14, G5.1.

New script: `local_docs/fable_runs/prompt_5_code/s4_checks.py`, output `local_docs/fable_runs/prompt_5_code/outputs/s4_checks.txt`.
