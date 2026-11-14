# Prompt 4 synthesis (orchestrator)

Context file (`local_docs/`, never cited by the spec). Date: 2026-11-14. Inputs: `prompt_4_answer.md` (`sonnet`, one stage: plan, scripts and answer from `prompt_4_brief.md`), `prompt_4_review.md` (S5, `opus` high), with `prompt_4_code/outputs/issues.md` and `prompt_4_review_code/` behind them. No Fable stage (§4 matrix). Everything here is level `derived`: passing property tests and two models agreeing are evidence, not proof.

## Result

No counterexample to the intended content of C1–C5, by the implementer's hypothesis tests (2,500–3,000 examples per property) or by the reviewer's four exact-arithmetic checks. All scripts re-ran byte-identical.

| Claim | Verdict (answer, review agrees) | Condition or correction |
|---|---|---|
| C1 f'' zero, ≤ 3 roots | holds with conditions | A zero of f'' inside (0, τ_w) needs K_g > 0 and 1 ≤ m < ρ − 1, i.e. K_s² > K_g²·(m+1)³. 3 roots are attained, for every m ≥ 1 tested up to 10⁶, and only in that window. m = 0 with K_s = K_g gives f linear (f ≡ 0 if also a = d′ = 0). The formula t_m/(ρ − 1) divides by zero at K_g = 0 or K_s = K_g. |
| C2 jump +R_g | holds (m ≥ 1) | True by construction of d_m′; the property test is the real check. |
| C3 ā | holds as stated | Explicit bounds ā·τ − K_s√τ + d₀ − R_g < f ≤ ā·τ − K_s√τ + d₀ + K_g√τ_w/4 give T; sharp when R_g = 0. ā = 0, K_s = 0: periodic, which is not "always wins". |
| C4 shorter τ_w never helps | holds with conditions | Strict only for K_g > 0 and τ_w ≤ τ; weak otherwise. h is continuous at τ_w = τ/k; m·R_g steps. |
| C5 interval screening | holds | Pessimistic corner: a, K_g, d₀, R_g at max; K_s, τ_w, λ_ℰ at min. Review MAJOR F1: the answer's "needs a product box of independent intervals" is wrong; corners of the per-coefficient bounding box bound f for any (coupled) input inside it. What breaks C5: corners taken in an underlying parameter on which coefficients depend non-monotonically, and subtracting λ_ℰ twice (d₀ interval already net of λ_ℰ). |

## Where the reviewer disagrees (0 BLOCKER, 2 MAJOR, 14 MINOR)

1. **F1, C5 condition** (above). Changes the wording the solver spec needs, not the verdict.
2. **F2, tie hazard undersized.** With τ = fl(j·τ_w), float floor and exact floor of the doubles disagree in 44.7 % of draws, not 5.4 %; inside the band of about 0.5 ulp(τ), f is off by exactly R_g. Exact arithmetic on τ does not fix this; carrying the tie as an integer j with dt = 0 does.
3. **Minor, evidence quality:** the C1 dense grid undercounts roots (103/1928; the exact quartic count confirms ≤ 3); only 6 of "60,000 tuned" draws reached the 3-root window; some "proof" lines are printed prose, not computed (C1 uniqueness, C4 sign); a count in `issues.md` is in no output; two float examples mislabelled; hypothesis writes `.hypothesis/constants/` despite `database=None`.
4. **Minor, missed cases:** win/lose switches per segment are ≤ 3 roots plus the jump at t_m, so a solver bracketing roots alone misses losses at jumps; for an intended ā = 0, float ā is non-zero in 48 % of draws, so "permanent" verdicts must compare T with the horizon, not trust sign(ā).

**Tolerance model (review r4, empirical, `derived`):** |f_float − f_exact| ≤ 4ε·S + 2·K_g·ulp(τ)/√(dt + ulp(τ)), ε = 2⁻⁵², S the sum of the absolute values of the terms of f. Worst case 0.43 of the bound in 38,570 draws. Not a proven error bound.

## What it means

- **Spec:** no document changes now. GMS-400 is not drafted (W2b); everything lands in its brief. Plan §4.1, §4.2 and §6.3 stay correct; §6.3 step 1 "only when K_s > K_g" is necessary, not sufficient (also m ≥ 1 and m < ρ − 1).
- **Validation level:** stays `derived`. To reach `cross-checked`, the C1 and C4 arguments need a written proof checked by a person or a second CAS, and the solver needs the differential test below.
- **Decisive further check:** when the solver exists, a differential property test of its float64 screening against an exact-rational reference evaluator, with ties as integer j and fully non-degenerate boxes; every float verdict outside the tolerance band must match the exact one.
- **Tooling:** SymPy, hypothesis and numpy are now in the project `.venv` (user, 2026-11-14) but not in `pyproject.toml`; `.hypothesis/` is not in `.gitignore`.

## Decisions proposed

- **D1, GMS-400 brief notes (`orchestrator_state.md` §4, item (f) onward):** C1 restated with its window (K_g > 0, 1 ≤ m < ρ − 1; test `K_s² > K_g²·(m+1)³` instead of forming t_m/(ρ − 1)); C4 strictness conditions; C5 as per-coefficient bounding-box corners with λ_ℰ boxed separately from the rest of d₀ and never subtracted twice; ā = 0 cases; switches per segment ≤ 3 roots + 1 jump.
- **D2, solver numerics for the brief:** ties carried as integer j (dt = 0), never τ = fl(j·τ_w) then floor; three-way classification win / loss / undetermined with the r4 tolerance as the starting model (empirical, to be replaced by a proven bound or kept with that label); permanent verdicts by comparing T with the horizon.
- **D3, plan change V14:** §6.3 step 1 condition corrected; §9.3 root-count and two-clock oracle tests use an exact root count (quartic in √dt or rational/mpmath), not a dense grid alone; §9.3 adds the differential exact-reference test; property-test strategies must reach the 3-root window and non-degenerate boxes (coverage asserted).
- **D4, tooling:** add `hypothesis`, `sympy` (and `numpy` if Phase 2 needs it) to the `dev` list in `pyproject.toml`, and `.hypothesis/` to `.gitignore`; property tests set the hypothesis home to a temporary directory.
- **D5, levels:** record no level change; list the hand-proof review of C1 and C4 as an open item for GMS-400 acceptance.

## Decisions recorded (user, 2026-11-14)

D1–D5 accepted as proposed. The user added **D6**: our pure-Python checks need another solver to cross-check them (SciPy, numpy). Recorded:

- D1, D2, D5, D6 → `orchestrator_state.md` §4, GMS-400 brief items (f)–(k).
- D3, D6 → plan V14: §6.3 step 1 condition, new steps 5–6 (ties, classification), §9.3 independent-solver oracle, exact root count, differential test, Bounds wording, hypothesis home; §9.6 `cross-checked` example; Q14 strictness.
- D4, D6 → `pyproject.toml` `dev` list (numpy, scipy, sympy, hypothesis), `.gitignore` `.hypothesis/`, CLAUDE.md set-up line; SciPy 1.18.1 installed in `.venv`.
- D6 applied now: a `sonnet` cross-check of C1, C3, C4 and C5 with SciPy and numpy as an independent oracle, own evaluator, no shared code (`prompt_4_xcheck_brief.md`, `prompt_4_xcheck.md`). Result: agrees on all four (no root count above 3; 0 corner violations in 300 `differential_evolution` boxes; h strictly decreasing at 11,700 exact ulp pairs). New: float64 root counting is unreliable for m ≥ about 1e5 (GMS-400 brief item (l)). Level stays `derived`.
- Follow-up (user, same session): Prompts 5–7 written into `fable_questions.md` (Class I / II gate; combining degradation mechanisms, OQ-20; entropy currency, OQ-13) and added to the delegation plan §4 and §7.
