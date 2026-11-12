# Prompt 2 review: adversarial check of `prompt_2_answer.md`

Status: every statement here is a claim at level `derived` (unverified). Agreement with the answer is not validation. Numbers come from scripts in `local_docs/fable_runs/prompt_2_review_code/` (outputs in `outputs/`); re-runs of the original scripts are in `outputs/rerun/`. Environment: python3, numpy 2.5.3, no scipy.

## Summary verdict

1. Arithmetic is sound: all 7 scripts re-run byte-identical, and every number in the answer that I checked matches the saved outputs. Independent quadrature reproduces R32–R34b to 3e-4 or better.
2. The BLOCKER (L1) is a currency choice, not a logic error. The framework's `W/T0` ledger is exactly a lost-work (exergy-destroyed) ledger divided by one constant, a defensible alternative to the answer's entropy ledger. V5's claim that the two give the "same decisions" is false: they disagree in 5.06 % of random cases.
3. Q2 holds: charging `b` at dispersal plus `CExC − b` at make-up exactly closes a ledger built from mass flows. The answer's S4-B "event ledger" is a tautology, like the R13 check it replaced.
4. L8/V7 misreads the framework's scope, L7 is conditional on a sign convention, and "provable for any spectrum" (V9) overclaims. The by-product rule in `CExC` (L16) is under-rated.
5. Counts: 0 BLOCKER, 3 MAJOR (1 conditional), 9 MINOR. The answer is usable after re-labelling L1 and fixing V5, V7 and V9.

## Findings table

| # | Severity | Location | Finding | Evidence or script |
|---|---|---|---|---|
| F1 | MAJOR | L1 (BLOCKER), V5, plan C8/D5(1) | The framework's margin is `Σ W_k/T0 + S_op` = `(W_earth + T0·S_op)/T0`. That is the sum of lost work, each loss valued in its own environment, divided by one constant. Its R25 verdict ("g loses", +300 J/K) equals the lost-work verdict (+60 000 J) in 100 % of sweep cases. Gouy–Stodola does not decide whether entropy or lost work is the currency across environments; the prompt's own definition ("lost work / T₀") supports the framework's reading. So L1 is a declaration that must be made, not an error with a unique correction. The "corrected margin −193.80 J/K" is the entropy-basis verdict, not "the" correct one. V5's alternative "exergy against one `T0*`" is only the entropy ledger rescaled, so "same decisions" is circular. The real alternative disagrees with the entropy basis in 5.06 % of cases (T0 between 150 and 290 K). | `rv02_dead_state_currency.py` |
| F2 | MAJOR | L8, V7 | The answer concedes (plan D7) that the average share is the correct per-unit figure in the all-or-nothing case. That case is what "credited only if x leaves the whole system" describes. So "`λ_ℰ` is an average, not a marginal" is not the defect. The defect is that a per-product rule conditions its credit on a system event that the same rule can veto. In the example, product 1 passes (150 < 201.241 J/K), product 2 fails (400 J/K), so `x` stays in the system and product 1's credit is unearned, yet switching both passes the system test. Other open conditions are sunk versus avoidable `F`, and per unit versus per mole. V7's default (the marginal `v`) under-credits by 134.161 J/K per unit in exactly the scenario the framework defines. V7 fits a single-product decision, which is a different question. | `rv03_ledger_and_misc.py` D1–D3 |
| F3 | MAJOR (conditional, UNSURE) | L16 (MINOR), V6 | Condition (iii), no substitution credit, is likely violated by the canonical tables themselves: the plan's own K1 note says Szargut handles by-products by the replaced-process (substitution) method (not read, UNSURE). Scarce elements are often by-products of host metals, so `CExC(x)`, and hence `Σ_s,init`, can be set by the allocation rule. MINOR is too low wherever `x` is a by-product. | Plan K1 and D1 (R4 mechanism); magnitude UNSURE |
| F4 | MINOR | L7 | `q·(1 − T0/T)` is the standard exergy-of-heat expression and is already correct for `T < T0` when `q` is signed as heat into the converter (gives +20 W/m²). It is wrong only if `q_thermal` is a non-negative magnitude. The answer lists clamping as unknown, but states the error unconditionally. | `rv03` C2 |
| F5 | MINOR | L12, V9, R35 | "Provable for any spectrum (R35)" needs brightness temperature `T_b ≤ Ts` everywhere. R35 draws `n = f·n_s` with `f ≤ 1`, so it excludes `T_b > Ts` by construction. With `T_b` up to 1.1·Ts, 2559 of 20 000 modes violate the `(1 − T0/Ts)` bound (max excess 0.22 %); the bound with each mode's own `T_b` has 0 violations. The real Sun likely exceeds 5772 K in the blue-green: about 5936 K at 480 nm, if AM0 is about 2.05 W/m²/nm (input from memory, UNSURE). Fix: use `Ts` = maximum spectral brightness temperature, or the first-law bound `q_solar`. | `rv01_spectral.py` |
| F6 | MINOR | §3 "Weak spots", L3, S4-B | S4-B builds the charges and "destroyed" from the same per-event increments, so "B equals destroyed" and "destroyed = IN − stock" hold by construction, like the R13 self-comparison it replaced. R21 (non-negative `d_omit`), R23 (same algebra rearranged) and R35 (see F5) are also true by construction. My mass-flow balance (resource drawn × `CExC` − metal held × `b`) checks the answer's corrected L3 formulas independently: agreement 1.4e-15. | `rv03` A1 |
| F7 | MINOR | L10 | The scrap correction charges unrecovered scrap `(1 − R_scrap)·w_ext` only, which is inconsistent with V1 (dispersed `b` charged). It omits `(1 − R_scrap)·n_scrap·b`: 266.7 kJ (894.4 J/K) in the R8 example with a made-up `b` = 400 kJ/mol. | `rv03` B |
| F8 | MINOR | L5 | The oxide counterexample's sign depends on the production route. Functional oxides of scarce metals are often made from refined metal; then `CExC_oxide > CExC_metal` and the framework under-charges the incumbent, which agrees with the prompt's claim. The prompt's boundary claim is true for omissions (the answer's own "true part"). "False" rests on one assumed data mismatch. MAJOR stands for the one-sidedness of "geometry loses" verdicts. | Reasoning; plan D4 |
| F9 | MINOR | L4 | The `r_el` correction applies only to dissipation fed by a purchased carrier. If `Σ̇` is environment-driven (for example thermal-cycling hysteresis), no upstream factor applies. The flip threshold is set by the made-up `D`: 0.472, 1.890 and 4.724 for `D` = 1e6, 4e6 and 1e7 J/K. The example shows the mechanism, not materiality. | `rv03` E |
| F10 | MINOR | L11 | Fixed 0.933 equals `η_L(T0, 5772 K)` at 290.05 K and is safe above that. It understates by 0.98 % at 250 K and 2.18 % at 200 K. "MAJOR for a colder dead state" applies only when the margin is within about 2 % of the solar line. | `rv03` C3–C4 |
| F11 | MINOR | L6 | The prompt's "lower bound" wording is defensible: the included sum is a lower bound on the total upper bound the test needs. The disagreement is semantic; the consequence is agreed. | Reasoning |
| F12 | MINOR | L3 corrected `Σ_g,EOL` | The corrected formula charges the in-service unit's dispersal, `(1 − R)·n·b`, before it occurs (excess exactly `(1 − R)nb` with the last unit in service). This is consistent only under V2's "retired at τ" commitment, which should be written into the term's definition, not only into V2. | `rv03` A3 |

## Reproducibility table

| Script | Re-run matches saved output? | Numbers in answer match? |
|---|---|---|
| `r01_r07_toy_chain.py` | Yes, byte-identical | Yes (1030, 730, 3454.64, 150, 1 883 105.8, −2 350 682.5) |
| `r08_r13_extraction_closure.py` | Yes | Yes (13.333, 3180.0, 10 665.8, 25 600.0, 85 862.8, 3520, 4800, 480, 4160, 4640). R13 is a self-comparison (acknowledged). |
| `r14_r21_closed_form_conventions.py` | Yes | Yes (251.55, 10 196.21, 9944.66, 1140/1100/680/428/260, 1920/1880/1040, 2012.41, 1157.14, 855.27, 0 and 2122). R14 is a reconstruction (acknowledged); R21 is true by construction. |
| `r22_r31_dead_state_and_sinks.py` | Yes | Yes (403.230, −67.08, 2012.41, 3000.00, 1.49075, −193.80/+300, −26 569, 0.933335, 0.953800, 0.948345, 0.017216, 153.100, 8.007, 16.122, 29.350, 16.814, ±20) |
| `r32_r35_spectral_exergy.py` | Yes | Yes (0.931130, 0.93554, 0.7321, 0.8378, 0.1057, 0.1097, 9797, tolerance gaps 5.5e-9, 1.7e-5, 0.027, 0.0016) |
| `r36_r39_landsberg_infrastructure.py` | Yes | Yes (1269.81, 1298.12, 201.241, 67.080, 51.241, 34.109, 1705.432) |
| `s4_literal_r14_and_reconcile.py` | Yes | Yes (5.9e-16, 1.7e-15, −1 292 235.5, 1.8896, 219.47, 6.1e-4, 20.308, 29.350) |
| `rv01_spectral.py` (new, Gauss–Legendre, grid edge at `u_c`) | n/a | R32 to 1e-16; R33 ψ 0.935541 (energy fraction 0.765496 exact series against 0.765483 trapezoid); R34a 0.732144 (additive étendue mixture 0.732474); R34b 0.837844 |
| `rv02`, `rv03` (new) | n/a | 219.474 K flip reproduced; other values in the findings |

## Derivation checks

- **D1 / L16.** The balance identity `CExC − b = B_waste + B_destroyed` is correct. Its use as `Tref·S_gen` needs the four conditions; see F3 on (iii).
- **D2 / L3 (Q2).** Confirmed from mass flows (`rv03` A1–A4). Prompt as written: short by `(m + 1)(1 − R)nb`. Answer's formulas: close exactly. "Full-`CExC` make-up plus `b` at every dispersal": over by `m(1 − R)nb`. No double count. Premises not tested: full `b` destroyed at dispersal; `CExC` includes ore exergy; no chemical exergy inside the `K·sqrt(τ)` terms; melt losses inside `w_rm` would need their own `b` charge.
- **C5 / S4-A / L13.** The literal prompt sum against the closed form is a genuine two-expression check (5.9e-16); I confirmed it by hand (coefficients `1 + m(1 − R)`, `m + 1`, `(m + 1)R`). The `−m·R` multiplier with `w_lost,prec` fixed is correct and trivial.
- **D3 / L14.** Single-life and chain formulas check by hand. CFF with `R1` = 0, `A` = 0, `Q_sout` = 0 reduces to `E_V + R2·E_rec` = framework (1140). The 50:50 form agrees with the PEF 2013 formula as I recall it (UNSURE, not read).
- **D4 / L5.** The proposition is correct and trivial. Counterexample (a) is route-dependent (F8). Counterexample (b) uses other asymmetries, not the boundary.
- **D5 / L1, L2.** The `b(T0)` formula is verified from Gibbs–Helmholtz at constant `ΔH_r` with reference-species terms scaling with `T0`. `Δb_M = −½·Δμ_O2` and the 3974 J/mol `O2` value check. The `CExC` non-transformability argument is accepted. D5(1)'s "same ordering" is circular (F1).
- **D6 / L6, L7, L11, L12.** The direction-of-error table is correct for a necessary condition: overstating the budget or understating the requirement is safe. Solar and cold-sky channels occupy distinct radiation modes, so adding them is the joint bound (my reasoning, not computed). Landsberg on diluted light: confirmed safe and loose (0.732 against 0.931). Carnot caveat: F5. Cold-sink formula and the 153.100 W/m² limit check.
- **D7 / L8, L9.** The algebra is correct. The interpretation conflicts with the stated scope (F2). L9's double count is accepted as conditional.

## Missed regimes

1. Lost-work currency as the alternative to entropy across environments (F1). It flips the R25 verdict and is the framework's literal reading.
2. By-product `x` with substitution-based `CExC` (F3). It may dominate the incumbent's charge.
3. Oxide made via refined metal (F8). This reverses the L5 counterexample.
4. Signed heat convention (F4).
5. Brightness temperature above `Ts` in real sunlight (F5).
6. Environment-driven operational dissipation, where L4 does not apply (F9).
7. Multi-product use of `x` where per-unit `λ` tests disagree (F2, D3).
8. Recycling melt losses: dispersed metal hidden inside `w_rm` escapes the V1 `b` charge (D2 note).

## Per-finding agreement

| Item | Agree / disagree / unsupported | Verdict follows? |
|---|---|---|
| L1 BLOCKER | Disagree with severity and uniqueness; agree a declaration is needed | No. Make it a MAJOR convention choice (F1). |
| L2 | Agree | Yes |
| L3 (Q2) | Agree | Yes; add the S4-B caveat (F6) and the timing note (F12) |
| L4 | Agree for computation and manufacturing carriers; conditional for `Σ̇` | MAJOR only if `Σ̇` is carrier-fed (F9) |
| L5 (Q4) | Partly agree | "False" is unsupported as a general statement; one-sidedness is supported (F8) |
| L6 | Agree | Yes (F11 is wording only) |
| L7 | Unsupported as unconditional | Conditional MAJOR (F4) |
| L8 (Q7) | Partly agree | The reason is misidentified; MAJOR stands for the per-product and system mismatch (F2) |
| L9 | Agree (conditional) | Yes |
| L10 | Agree | Yes; the correction needs the V1 term (F7) |
| L11 | Agree on direction | Severity MINOR unless margins are about 2 % (F10) |
| L12 | Agree | Yes, with the F5 caveat |
| L13 | Agree | Yes |
| L14 (Q3) | Agree | Yes |
| L15 | Agree | Yes |
| L16 | Agree on conditions | Severity possibly MAJOR (F3) |
| V1 | Agree | |
| V2 | Agree | Charges future events (F12) |
| V3 | Agree | |
| V4 | Agree | |
| V5 | Disagree | "Same decisions" is false (F1) |
| V6 | Agree, low confidence | |
| V7 | Disagree for the stated scenario | F2 |
| V8 | Agree | Makes the test nearly vacuous on Earth: +153 W/m² against about 187 W/m² solar |
| V9 | Agree with caveat | F5 |

## Citations

- **K67 (L6).** Web search snippets of the preprint attribute 153.1 W/m² as the ultimate limit at 300 K ambient and 3 K space to this paper, as an analogue of the Landsberg limit, plus 93.3 % Landsberg at (6000 K, 300 K). Search-summary level only; full text not read (direct fetch blocked). Independently, `σT0⁴/3` = 153.100 W/m² at 300 K.
- **K9, K11 (L1).** They support the Gouy–Stodola theorem, which is not in dispute. They do not support the step from the theorem to a unique cross-environment currency (F1).
- **K41, K42 (L8).** Generic marginal against average; adequate. They do not address the scope point in F2.
- **K12, K49 (L9).** Accepted at abstract level (per S3); not re-checked.
- **Q3 mapping (K32–K38, K40).** A secondary web source confirms the structure of the CFF material term `(1 − R1)E_V + R1(A·E_rec + (1 − A)E_V·Qsin/Qp) + (1 − A)R2(E_recEoL − E*_V·Qsout/Qp)`, matching plan D3 with quality ratios 1. The 50:50 form, K38's section 5.4.7 and K29's clause numbers: not verified, UNSURE.
- Sources consulted: [arXiv 1710.02617](https://arxiv.org/pdf/1710.02617), [SPIE proceedings version](https://astronomicaltelescopes.spiedigitallibrary.org/conference-proceedings-of-spie/10759/107590N/Thermodynamic-limits-of-energy-harvesting-from-outgoing-thermal-radiation/10.1117/12.2323951.full), [PEF CFF notebook](https://wimyedema.github.io/sustainability/summaries/pef.html), [Nordic CFF appendix](https://pub.norden.org/temanord2024-515/appendixf-circular-footprint-formula-factors.html), [Cahalan et al. brightness temperature](https://link.springer.com/article/10.1007/s11207-021-01941-y) (values not seen).

## What still needs external checking

1. **Single most decisive check: the documentation of the framework's actual `CExC(x)` source.** Find out whether it includes ore exergy, which by-product rule it uses, and whether it includes capital goods. This conditions the Q2 closure premise, L9, L16 / F3 and the L5 route question at once.
2. A user decision, not a measurement: entropy or lost-work currency across environments (F1). It cannot be settled by any tool.
3. The framework text for the sign of `q_thermal` (F4), what drives `Σ̇` (F9), and gross or net `n_i` (L10).
4. Measured extraterrestrial and terrestrial solar spectral irradiance (ASTM E-490 or SORCE), to compute the maximum brightness temperature and the spectrum-integrated exergy fraction against `η_L` (F5, L12).
5. Primary texts: K67 full paper; PEF Guide 2013 section 5.4.7 (50:50) and the 2021 Annex (CFF); ISO 14044 clauses; Szargut's by-product rule in K1 or K2.
6. Validation levels: nothing here raises any claim above `derived`. The 44 passing rows and my scripts confirm algebra and quadrature on made-up inputs only.
