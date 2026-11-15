# Prompt 6 review (S5): combining degradation mechanisms (OQ-20)

Status: independent adversarial review of `prompt_6_answer.md` (S4). Everything here is a claim at level `derived` (unverified). Agreement between this review and the answer is not validation. No measurement was used.

Read: the Prompt 6 fenced block in `local_docs/fable_questions.md`, `prompt_6_answer.md`, `prompt_6_plan.md` (by search only), `prompt_6_s4_brief.md`, all of `prompt_6_code/` and `prompt_6_code/outputs/`, `prompt_6_citations.md`. Written: this file and `prompt_6_review_code/rv01_core_independent.py`, `rv02_rainflow_a11.py`, `rv03_not_recomputed_rows.py`, with stdout in `prompt_6_review_code/outputs/rv0*.txt`. Tags `[rv01]`, `[rv02]`, `[rv03]` refer to those. Two web searches were made (technical terms only).

## Summary verdict

1. Reproducibility is clean. All 35 scripts re-run with byte-identical stdout. Both `s4_*` scripts reproduce S2 at b = −0.102: 33 of 33 checks pass, not the 37 the answer says. Independent ODE, root and rainflow routes `[rv01]` `[rv02]` match every headline number.
2. Verdict items 1, 3 and 4 and Rule R follow from the evidence. Verdict item 2 has two wrong magnitudes. The concurrent-case factor "894 / 268 at s = 1" is the slow-case-alone factor, not the error of the minimum rule: that error is 100 to 1.9 depending on φ (MAJOR). The section-loss "at most 4.38 / 6.77" ignores the answer's own parabolic (25.5) and p = 3 (8.9) cases (MAJOR).
3. Rule W (M4.2) does not follow as written. It caps life at perforation but leaves out pit-initiated fatigue, which M2.9 shows can govern. One in-model case overstates life by 4.45 / 2.42 (MAJOR).
4. Verdict item 5 ("b changes numbers by up to about 40 %") is wrong: the change reaches 84 % on the pit life factor and 70 % on (1 + s)^m. Its conclusion still holds: no default rule changes (MAJOR, wording and support).
5. No BLOCKER. The most decisive open check is a paired air and saline S–N data set for a 2xxx aluminium alloy at 1e7 cycles or more. F_env sets the ranking and the "undetermined" margin (0.012), and it still rests only on the planner's range.

## Findings table

| # | Severity | Location | Finding | Evidence or script |
|---|---|---|---|---|
| 1 | MAJOR | Verdict 2, third bullet; M2.3; M3.2 row 6 | "(1 + s)^m = … 894 / 268 at s = 1" is presented as the error of treating concurrent cases separately. At s = 1 the fast case governs, so the minimum rule overstates life by only 100 / 30.6 (φ = 9), 28 / 9.1 (33), 7.9 / 3.1 (129), 1.87 / 1.26 (1025). Miner over cases gives 90 to 1.9. The real worst case over s is 318 / 97 at s ≈ 0.8 (φ = 9) and 52 / 18 (φ = 1025). (1 + s)^m is an approximate upper value of min-rule/block only where the slow case dominates (s below about φ^(−1/m)). The answer's s = 1 figure overstates by 9 to 480 times. | `[rv01]` [conc]; `[b4]` columns tmin/tau_blk and tauMiner/tau_blk already show 100.2, 28.1, 7.9, 1.87 |
| 2 | MAJOR | Verdict 2, fifth bullet; M2.5; M2.7 "ranking survives"; M4.2 "worst-case error 1.84 to 4.38"; section 2 table | "Section loss … at most 4.38 / 3.91 (wall) and 6.77 / 5.96 (round strut)" holds only for linear recession under axial or membrane load. The answer's own M2.5 gives parabolic F_min = 11.7 (q = m) and 25.5 (q = 2m). `[c6]` computed q = 3m = 29.4 (round member in bending or torsion), F = 8.91. A wall in bending has p = 2. Parabolic with p = 3 gives 42.2 / 33.0, which is above the low end of the F_env range (35.9 / 24.1). The claim "F_env stays above the section-loss maximum at every point of the range" therefore holds only for linear recession and p ≤ 2. The k₈ at which the two are equal drops from 0.82 to 0.67 (parabolic strut). | `[rv01]` [sec] and [env]; `[c6]` q = 29.412; `[c9]` |
| 3 | MAJOR | M4.2 Rule W; M2.11 | τ_wearout = min(τ_c, x_allow·t_c, t_perf) has no pit-initiated-fatigue term, but M2.9 shows that this mode governs for b = −0.102 in the worked thin wall (1.31 yr against t_perf 1.50 yr). For a 3 mm wall attacked on one side (PF = 3, r = 10 µm/yr, same stress), Rule W gives 12.7 yr while the answer's own pit model gives 2.86 yr: 4.45 times non-conservative (2.42 at b = −0.124, about 2 under the E647 ΔK convention of #12). Perforation is an upper bound on life, not a conservative cap. Either add τ_pit to the minimum or move "pitting alloy" from "use t_perf" to the reject list. | `[rv01]` [pit] Rule W check; `[c12]` (linear pit lives) |
| 4 | MAJOR | Verdict 5 | "The choice of b changes numbers by up to about 40 %" is contradicted by the answer's own table. The ratios between the two b values are: pit life factor 0.163 (−84 %), (1 + s)^m at s = 1 0.299 (−70 %), w_fat 0.427 (−57 %), E4 margin with the environment curve 1.54 (+54 %), pit life 2.12. The statement that no default changes still holds (the two b values give the same ordering of the defects). | `[s4b]` summary; `[rv01]` sensitivity block |
| 5 | MINOR | Provenance line | "37 comparison lines, all reproduced": there are 33 (25 in `s4_b_sensitivity.txt`, 8 in `s4_d5_d6_mismatch.txt`). All 33 do reproduce, and the hard-coded S2 reference values match the S2 output files. | `grep -c reproduced`; S2 files c1, c6, c10, c12, d5, d6, e2, e4, e5 |
| 6 | MINOR | M1.6 | "the upper bound … is loose: up to 42.5 times the rainflow value". 42.52 is UB/separate-sum at n = 3, φ = 33, s = 0.1. UB/rainflow peaks at 32.7. The 24 rainflow ratios are reproduced exactly by an independent four-point count on analytic turning points. | `[rv02]` |
| 7 | MINOR | M1.12 | "0.0212 / 0.0218", "0.150 / 0.177", "10.4 / 6.03" are first-order / exact at b = −0.102. The header reserves "x / y" for the two b values. | `[e5]` |
| 8 | MINOR | M2.10, C14 null case (work item 7) | S4 says that with q = 0 "t_c drops out … the life is τ₀ for every ρ" and that the UNDECIDED cases are an artefact. In the model, recession still ends the part at t_c, so the null life is min(τ₀, t_c), and τ/τ₀ = 1/ρ for ρ ≥ 1 (0.1 at ρ = 10). The script stopped correctly at t_c; the expected value the null test used was wrong for ρ ≥ 1. The verdict "identity, tests only the event logic" stands, with the expectation corrected. | `[rv01]` [C14 null]; `[c14]` |
| 9 | MINOR | "Rows affected by b but not recomputed" | Spot-checked: C7 "about 10 % lower" is right (7 to 12 %). C13 "longer by up to about 2" is right (up to 2.28). C9 "about 10 to 15 %" is too small (8 to 21 %; 18 to 21 % at the ρ = 1 maxima). B1 s* "up to about 10 %" is too small (14 % at φ = 1000). C15 "longer" has the **wrong direction**: τ₀ does not depend on b, and τ/τ₀ falls (1.053 → 1.043 at ρ = 0.01; 1.388 → 1.289 at 0.05), so the displacement-control lives get shorter. | `[rv03]` |
| 10 | MINOR | M3.4 ("B on one case"), M2.11 ("B") | The E4 bound-exceeds-exact check is an identity, and the E4 output itself flags it (τ_LB ≤ τ_c was proved in C8, and an end value is at least the average). Work item 10 says such a check is not evidence. M2.11's lower bound can be proved: ∫₀ˣ(1 − u)^(−q)du ≤ x(1 − x)^(−q), so x_c ≥ x*. It should be class P, with the grid as a code check only. | `[e4]` IDENTITY line; derivation below |
| 11 | MINOR | M2.10 (i), M3.2 row 12, M4.4 | The plan's qualifier "bending under imposed curvature" was dropped. Under imposed axial displacement σ_a does not depend on the section (p = 0), and the gain over τ₀ is nil. σ ∝ (1 − x)^(+1) holds for imposed curvature or deflection in bending only. | plan line 220 vs answer M2.10 |
| 12 | MINOR | M2.9 | a₀ uses Δσ = 2σ_a (full range at R = −1) with a ΔK_th quoted for R ≈ 0.1 (S3, L02). If only the tensile part is used for R < 0 (common practice for R < 0, UNSURE whether E647 mandates it), a₀ = 477 / 1187 µm, the life factor of a 100 µm pit falls to 2.5 / 1.4, and perforation governs for both b. "Fatigue governs for b = −0.102" depends on this unstated convention. The perforation cap is unaffected. | `[rv01]` [pit] |
| 13 | MINOR | M4.1 flag band; M4.3 in-sample warning (work item 11) | The Rule R flag band "0.7 to 1.1 of the sum, n = 2, well separated frequencies" comes from the A11 grid on which M1.6 was revised, so the test is in-sample, and M4.3 does not say so. A phase sweep at φ = 3 gives 0.33 to 1.33 (n = 2) and 0.27 to 2.12 (n = 3). At φ = 9 it gives 1.03 to 1.08 (n = 2). "Well separated" needs a number. | `[rv02]` phase sweep |
| 14 | MINOR | Verdict 2, fourth bullet | "Pitting … at least 10" equals the input PF = 10 by construction (t_perf = t_c/PF when t_c < τ₀). It restates an unsourced input; it is not a computed effect. | `[s4b]`, `[c12]` |
| 15 | MINOR | M1.4, M1.6, M4.1 (missed regime) | Lazan's exponent n is not 2 near the endurance level. Search snippets report n from 2 to 8 depending on stress, rising above the cyclic stress sensitivity limit (UNSURE: snippet only). For a round strut p = 2n − 2 could reach 14, which moves the Rule R gate to x_e ≤ 0.007, and the concurrent-hysteresis factors scale as (1 + s)^n. The prompt's ψσ²/(2E) assumes n = 2, and the answer does not flag that. | web snippet (DTIC AD0003566); `[rv03]` Lazan lines |
| 16 | MINOR | M4.4 (missed regime) | No entry for sustained-load mechanisms (stress-corrosion cracking) or intergranular and exfoliation attack, to which 2024-T4 is known to be susceptible (memory, UNSURE). They are time-based and non-uniform, and neither Miner nor a uniform r covers them. | none (argument) |
| 17 | MINOR | M3.6 | The margin 0.181 uses τ_LB although the closed form τ_c is available inside the same model. With the exact life the margin is 0.244 / 0.271. Using τ_LB loosens the bound by a factor of 1.35 that protects against no model error the answer names. Say what τ_LB is meant to cover (Miner under rising stress, M2.10 (iii), is 1 to 8 % the other way). | `[rv01]` [E4] |

Counts: BLOCKER 0, MAJOR 4, MINOR 13.

## Reproducibility table

| Item | Result | Evidence |
|---|---|---|
| All 35 scripts in `prompt_6_code/` (33 S2 and 2 S4) | Re-run in a scratch copy with `python3`. All exit 0, and all 35 stdout files are byte-identical to `outputs/`. | `diff -q`, 35 SAME |
| `s4_b_sensitivity.py` reproduces S2 at b = −0.102 | 25 / 25 "reproduced". Hard-coded references checked against c1, c6, e2, e4, c10, c12, e3, e5 files. | outputs |
| `s4_d5_d6_mismatch.py` reproduces S2 at Δα = 7e-6 | 8 / 8 "reproduced" (d5, d6 files) | outputs |
| Answer numbers tagged `[s4b]`, `[s4d]` | All checked against the saved stdout; all match within rounding. | section 2 tables, M1.5, M1.8, M2.2, M2.3, M2.5, M2.7, M2.8, M2.9, M2.10, M3.3, M3.6 |
| Answer numbers tagged to S2 scripts | Spot-checked a1, a4, a6, a7, a8, a9, a11, b1, b2, b3, b4, b6, c3, c6, c8, c9, c10, c12, c14, c15, c16, c17, d1, d3, d5, d8, e1, e2, e4, e5. All match except the two wording errors (#6 "42.5", #5 "37"). | outputs |
| Independent route, headline numbers | ODE plus event (LSODA), brentq and bounded optimisation reproduce σ_a0, F_min maxima, F_g, F_s, verdict errors, x*, τ_LB, margins, F_env, planner-box extremes (continuous 41 × 71 grid: 35.86 to 459.18 and 24.09 to 289.52; extremes at corners), k₈ thresholds, pit a₀ and lives, ρ*, D5 and D6, and the Tedmon bounds (max U/m 1.3693 at θ = 3.33, max m/L 1.4733 at θ = 2.00, 0 violations). | `[rv01]` |
| Independent rainflow (A11) | Four-point rule on analytic turning points. All 24 ratios match `[a11]` to 4 decimals; max UB/RF 32.7. | `[rv02]` |

## Derivation checks

- **M2.5 closed form.** Miner under σ ∝ (1 − u)^(−p) gives t_c∫₀ˣ(1 − u)^(−q)du = τ₀, so (1 − x)^(1−q) = 1 + (q − 1)ρ. Correct. The maximum of F_min is at ρ = 1: for ρ < 1, F = ρ/x(ρ) increases because x is concave with x(0) = 0; for ρ > 1, F = 1/x(ρ) decreases. Confirmed numerically for p = 1, 2, 3, linear and parabolic `[rv01]`.
- **Parabolic recession (C9).** 2∫₀ˣu(1 − u)^(−q)du = ρ, τ = x²·t_c. Values reproduced (1.703, 3.533, 11.66, 5.599). The maximum is also at ρ = 1 (25.51 for q = 2m), which the answer had not located.
- **M2.11 lower bound.** The integrand is increasing, so ρ = ∫₀^{x_c} ≤ x_c(1 − x_c)^(−q). g(x) = x(1 − x)^(−q) is increasing, so x_c ≥ x*. This is a proof (class P).
- **M2.9 linear pit growth.** ∫₀^τ(1 + t/t_a)^(m/2)dt = τ₀ gives the stated τ. Correct. The convention on Δσ is in #12.
- **M2.10 (i).** D(t_c) = t_c/((m + 1)τ₀), ρ* = 1/(m + 1); correct for imposed curvature or deflection in bending (#11).
- **M1.4.** The parabolic multiplier −2(a + ln(1 − a))/a² follows from u = √(t/τ). Correct. The exponents are correct for the stated loadings. p = −1 for the corrosion term of a round strut is correct (area ∝ d).
- **M1.7 Tedmon bounds.** Upper: dδ̃/dθ ≤ 1/δ̃ gives δ̃² ≤ 2θ. Lower: d(m̃²)/dθ = 2m̃/δ̃ ≥ 2 gives m̃² ≥ 2θ, and m̃ ≥ θ trivially. Both are proofs; the numbers are confirmed by an independent ODE `[rv01]`.
- **M1.8 δ_c.** For an equibiaxial film the stored energy is Eε²δ/(1 − ν), so δ_c = G_c(1 − ν)/(Eε²). The form is consistent; the inputs are unsourced. The sign of the mismatch strain (compressive on cooling, tensile on heating for Al with alumina) is not discussed; ε_c with K_Ic applies to the tensile half only.
- **M1.9.** ΔT ≤ cT²/(1 − cT) and the electro-thermal loop ΔT = ΔT₀/(1 − x − αΔT₀) are both correct.
- **M1.12 / E5.** The cost form c_true/c_model − 1 = w_emb(F − 1) + w_ox(√F − 1) + Σw_i(M_i − 1) follows from (embodied + K√τ + ∫rates)/τ. That cost form is inferred, not read from the spec (the answer says so).
- **M3.6 reading of 0.3·τ₀ (work item 9).** A reduced damage sum D_c = 0.3 is equivalent to τ₀′ = 0.3τ₀, hence ρ′ = 0.3ρ. The adopted reading A is the consistent one. The headline 0.181 does not depend on it. Agree.
- **A11 decision (work item 4).** Agree that both the claim and the test were at fault. The independent rainflow confirms the 24 ratios. A phase sweep confirms "either sign": at φ = 3 the ratio ranges from 0.33 to 1.33 for n = 2 `[rv02]`.
- **C13 (b) cube-root (work item 6).** The explanation (matched at 1 yr, deeper before 1 yr, damage weighted towards early depth) is consistent with `[c12]`: the cube-root life is shorter at linear lives of 1.31 and 0.61 yr and longer at 2.86 yr and above. Agree.
- **C7 / C10 sweeps (work item 5).** Agree. The unbracketed ρ₁ values are closed-form only, and no worst case is claimed outside the sweep. F_env is monotone in σ; the crossovers outside [100, 400] MPa are extrapolations.
- **E5 weighted sum (work item 8).** Handled: the definition is stated, two readings differ by 0.9 %, and the spec must fix it. Agree.
- **F_env on an unsourced range (L01, L06; work item 3).** Stated where used (verdict, M2.7, M3.6, Open points). Agree. #2 limits the "ranking survives the range" sentence.
- **Identity checks (work item 10).** The evidence classes are mostly applied correctly (M1.11 A, M2.10 null case, c16 "ratio of two tabulated constants"). The exceptions are in #10.
- **In-sample (work item 11).** M4.3 states it for the Rule R gates, the screens, the perforation cap and x_allow. It is missing for the A11-derived flag band (#13), and for Rule W's perforation term, which #3 shows fails out of sample on a second geometry.

Claim-by-claim (A agree, D disagree, U unsupported by the evidence given):

| Claim | Call | Note |
|---|---|---|
| M1.1, M1.2, M1.9, M1.10, M1.11, M3.1, M3.5 | A | |
| M1.3 | A | direction cases A; completeness U |
| M1.4 | A | exponents medium; n for hysteresis see #15 |
| M1.5 | A | form A; magnitude U (β, γ, ψ unsourced) |
| M1.6 | A | with #6 and #13 |
| M1.7 | A | bounds proved |
| M1.8 | A | arithmetic A; inputs U |
| M1.12 | A | notation #7 |
| M2.1, M2.2, M2.4, M2.6, M2.8, M2.12 | A | M2.4 exponent form U |
| M2.3 | D | the statement holds only where the slow case dominates; the verdict figure at s = 1 is wrong (#1) |
| M2.5 | A | "maximum" limited to linear recession, p ≤ 2 (#2) |
| M2.7 | A for numbers, U for the ranking clause | #2 |
| M2.9 | U | governing mode depends on the ΔK convention (#12); perforation cap A |
| M2.10 | A for (ii), (iii); D for the null-case reasoning (#8); (i) needs a qualifier (#11) | |
| M2.11 | A | P, not B (#10); add τ_pit (#3) |
| M3.2 | A | rows 6 and 8 sizes need the corrections of #1, #2 |
| M3.3 | A | |
| M3.4 | A | evidence class (#10) |
| M3.6 | A | #17 |
| M4.1 Rule R | A | #13, #15 |
| M4.2 Rule W | D as written | #3 |
| M4.3 | A | |
| M4.4 | A | add #3, #15, #16 |

## Missed regimes

1. **Bending and torsion of round members (p = 3), and walls in bending (p = 2).** The worst linear section-loss factor rises from 6.77 to 8.91 (b = −0.102). With parabolic recession it reaches 42.2, above the low end of the F_env range `[rv01]`. Rule W handles this through q = p·m only if p is declared correctly, so the rule should list p by load path.
2. **Parabolic recession.** Its worst factors (11.7 wall, 25.5 strut) are larger than the linear ones, yet the verdict and the M4.2 "worst-case 1.84 to 4.38" quote linear values only.
3. **Pit-initiated fatigue at moderate PF in thick walls.** Rule W is non-conservative by 4.45 / 2.42 in one in-model case (#3).
4. **Concurrent loads near the equal-life point** (s ≈ φ^(−1/m)). This is where the concurrent error peaks (318 / 97 at φ = 9), not at s = 1 (#1).
5. **Lazan n > 2 near the endurance level** (#15). For the 0.3 mm strut at x_e = 0.15 with p = 14 the hysteresis multiplier would be M_lin = 3.74 against 1.18 at p = 2, and the Rule R gate would fall to 0.0068 `[rv03]`. n = 8 is UNSURE.
6. **Sustained-load and intergranular mechanisms for 2xxx alloys** (#16).
7. **Comparison fairness.** The 0.012 "undetermined" margin applies the environment curve to g only. When g and s share alloy and environment, M3.3 shows the bias falls to about 3 % at 1 Hz. M4.4 should say which margin applies when the environment is common to both sides; otherwise almost every verdict falls into "undetermined". This affects the use of the third verdict class, not its need.
8. **Sign of the thermal mismatch in D6:** see Derivation checks.

None of these removes the need for the "undetermined" class or for Rule R; #3 changes Rule W.

## Citations

Spot-checked bibliographic records against memory (UNSURE where marked):
- Tedmon 1966, J. Electrochem. Soc. 113, 766–768; Opila and Hann 1997, J. Am. Ceram. Soc. 80, 197–205; Manson and Halford 1981, Int. J. Fract. 17, 169–192; Alduchov and Eskridge 1996, J. Appl. Meteorol. 35, 601–609; El Haddad, Topper, Smith 1979, Eng. Fract. Mech. 11, 573–584; Suresh, Zamiski, Ritchie 1981, Metall. Trans. A 12, 1435–1443; Smith, Watson, Topper 1970, J. Materials 5, 767–778. Titles, volumes and pages are consistent with what I recall (memory, not re-fetched).
- **Dowling Table 9.1, 2024-T4 (the open b).** A web search returned snippets of the table from secondary copies (homework-help sites): σ_f′ = 900 MPa, A = 839 MPa, b = −0.102. A table note to Table 14.1 says the non-prestrained constants are σ_f′ = 900 and b = −0.102. A = 900·2^(−0.102) = 838.6 is internally consistent. This favours −0.102 as Dowling's value, but only through a secondary snippet, so it stays UNSURE, and the source of −0.124 is unidentified. S4 was right not to pick one. Reading the primary table would close it.
- Lazan 1968: D = Jσⁿ is confirmed by S3. The range "n from 2 to 8 depending on stress" appears in a DTIC report snippet (UNSURE, not read).
- The answer's citation section copies S3's verdicts faithfully (spot-checked 10 rows against `prompt_6_citations.md`). The "not seen" qualifiers for Manson–Halford's (N₁/N₂)^0.4, Hancock–Nicholls' ε_c and Evans' strain-energy criterion are kept. Agree.
- The verdict's welded-steel anchor (DNV-RP-C203 curve D) constants re-derive as 3.0, 5.19, 9.22 and 20.7 `[c16]`; the constants were matched by S3 through search summaries only.

## What still needs external checking

- **Most decisive single check:** a paired air and saline (or salt-fog) S–N data set for a 2xxx aluminium alloy at R = −1 out to 1e7 to 1e8 cycles, for example the ASM Handbook Vol. 19 figures read numerically, or the proposed thin-strut test. It fixes k₅ and k₈, hence F_env (24 to 459), the ranking against section loss (#2), and the 0.012 margin that drives the "undetermined" class.
- Dowling Table 9.1 read at source (b of 2024-T4), and the origin of −0.124.
- Pre-pitted fatigue data for 2xxx or 7xxx alloys (life factor at about 100 µm), together with the ΔK convention at R = −1. This decides the governing mode in M2.9 and the size of the Rule W gap (#3, #12).
- A Lazan n(σ_a/σ_e) curve for an aluminium alloy (#15).
- Opila and Hann's limiting thickness (10.4 against 6.9 µm): re-derive the k_p convention (x² = k_p·t against dx/dt = k_p/x) from the paper's own equations.
- G_c, K_Ic, E_ox for alumina on aluminium (D5, D6 inputs).
- Whether GMS-220 load cases can act at the same time (decides #1's weight), and the GMS cost form (M3.1), from the spec. A tool cannot settle either; both need a reading of the spec.
- Out-of-sample test of Rule R and Rule W: a case (material, geometry, frequency) fixed before computing, with at least one measured life or mass-loss history.
