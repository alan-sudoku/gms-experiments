# Prompt 4 review (S5): solver lemma red-team, C1-C5

Context file (`local_docs/`). Reviewer: `opus`, adversarial, 2026-11-14. Inputs: the Prompt 4 block in `local_docs/fable_questions.md`, `prompt_4_brief.md`, `prompt_4_answer.md`, `prompt_4_code/` and its `outputs/`. Own checks: `prompt_4_review_code/r1..r4_*.py`, stdout in `prompt_4_review_code/outputs/`. Everything here is level `derived`. Agreement between the answer and this review is not validation.

## Summary verdict

All five verdicts stand. No counterexample to the intended content of C1-C5, and none was found by four independent exact-arithmetic checks (r1-r4).
Two points in the answer need correcting before they feed the solver brief. First, the C5 condition "product box of independent intervals; coupling can break C5" is wrong: the per-coefficient bounding box always works. What does break C5 is taking corners in an underlying parameter space, or subtracting λ twice. Second, the tie hazard is undersized: float and exact m disagree in 44.7 % of intended ties, not 5.4 %.
The rest are evidence-quality and labelling issues (grid undercounts, a vacuous margin, mislabelled float examples), not verdict changes.
Decisive further check: when the solver exists, run a differential property test of its float64 screening against an exact-rational reference, with ties carried as integer j and the tolerance band given under Float64 issues below.

## Findings

| # | Sev. | Location | Finding | Evidence |
|---|---|---|---|---|
| 1 | MAJOR | answer C5 restatement, C5 (ii); issues.md item 8; c5 part 3 | The answer requires "a product box of independent intervals" and says "if any coefficient is tied to tw ... C5 can fail (UNSURE)". Neither holds. f is coordinatewise monotone at every point with K_g, R_g ≥ 0, so moving one coordinate at a time from any x to the corner gives f_pess ≥ f(x) ≥ f_opt for every x in the per-coefficient bounding box. A coupled set is a subset of that box. The hazards that do break C5 are different: (a) corners taken in an underlying parameter p (e.g. evaluating p_lo and p_hi) when coefficients depend on p non-monotonically, and (b) λ subtracted again when the d₀ interval is already net of λ. | r3 part 3: 19,200 coupled checks, 0 violations. Counterexample to (a): τ = 744.499, max(f(p=0), f(p=1)) = −5.24 but max over interior p = +0.424. r3 part 4: (b) gives f = −0.3 at the "pessimistic" corner while the true worst input has f = +0.2. |
| 2 | MAJOR | answer C4 float paragraph; issues.md float item 1 | The tie hazard is real but mis-sized, and the cited example belongs to a different class than the quoted count. With τ = fl(j·τ_w): float floor ≠ j in 10,825/200,000, but float floor ≠ exact floor of the doubles in **89,470/200,000 (44.7 %)**. The cited example (τ_w = 0.0367344509464381, j = 960439) is one of the 89,470 (float m = j, exact m = j−1), not one of the 10,825. The float floor equals the intended j more often (94.6 %) than the exact floor of the doubles does (49.9 %), so exact arithmetic on τ doubles does not fix intended ties; only an integer j does. The disagreement band is ≤ 0.5 ulp(τ) and the f error inside it is R_g. | r4 part 1 (same seed and call order as c4 part 3). |
| 3 | MINOR | c3 part 5 (ā = 0, K_s > 0) | The rounding margin \|a\|·2⁻⁵²·τ makes the assertion vacuous (margin ≥ \|f\|) in about 9 % of draws (263/3000, same strategy shape, not identical draws). The conclusion survives: an exact check with rational √τ_w, exact a and ā = 0 shows f < 0 at all 12,000 targeted τ > T₀, including dt = τ_w/4, where the upper bound is tight. | r2 parts 1-2. |
| 4 | MINOR | c1 parts 2-3 | The grid (40,000 points) under-counts roots. Measured against an exact quartic count it misses roots in 103/1928 cases (94 in near-tangent windows). This can only hide a 4th root, never invent one, so the "≤ 3" property test is weaker than it reads. The proof carries the bound; r1 confirms ≤ 3 exactly in 1928 cases, m up to 10⁶. | r1. |
| 5 | MINOR | answer C1 "60000 tuned ... searches" | Only 6 of the 60,000 "tuned" draws reached the 3-root window ("histogram {3: 6}"), so the effective tuned sample is 6, not 60,000. | c1 output (2). |
| 6 | MINOR | answer C1 restatement; "Not settled" | The restatement omits two things: 3 roots require K_g > 0 and 1 ≤ m < ρ−1, and the case K_s = K_g > 0 with m ≥ 1 (f'' < 0, no zero) is not covered. "3-root window nonempty over all classes" can be settled: for every m ≥ 1 and ρ > m+1 (K_g > 0), picking −a just above min f' puts both critical points near x* inside (0, τ_w), and d' is free through d₀. r1 constructs 3-root cases at m = 1, 2, 3, 10, 100, 1000 and 10⁶ (45 with m ≥ 1000), and finds no 3-root case outside 1 ≤ m < ρ−1. | r1; proof sketch below. |
| 7 | MINOR | answer C2 float sentence | "Error at t_m of order K_g √ulp (e.g. 5.7e-6 at τ_w = 1e9, m = 1e7 ...)". That row has dt = 0 exactly, and 5.65e-6 < ulp(f)/2 = 6.1e-5: it is plain rounding of f, and so is the τ_w = 1e3 row. Only the τ_w = 0.1, m = 3 row (1.58e-8 = 3·√2.78e-17) is the √ulp effect. | r4 part 3. |
| 8 | MINOR | issues.md float item 2 | "dt = 1.907e-6 ... pure rounding noise" is wrong for that example. Float dt equals the exact dt (Sterbenz), so the value is exact. The real effect is conditioning: ∂f/∂τ = K_g/(2√dt) = 362 K_g s⁻¹ there, so one ulp of τ moves f by 1.38e-3 K_g. Rounding of fl(m·τ_w) when it is inexact (the τ_w = 0.1 row) is the other source. The K_g·√ulp(τ) order is right as a worst case. | r4 parts 3-4. |
| 9 | MINOR | answer C3 "Not settled: T bounds valid but not tight" | For R_g = 0 and ā > 0 the lower bound is attained at every tie (r = 0 at dt = 0), so T is sharp there. In 13 cases f = 0 exactly at τ = T (a tie, consistent with "for all τ > T"). | r2 part 3: 188 attained, 13 exact zeros. |
| 10 | MINOR | issues.md ambiguity 3 | "162 of 564 K_s>K_g>0 cases" has no 564 in any output. The output gives `fpp:Ks>Kg>0: 624`, which includes m = 0. | c1 output (3a). |
| 11 | MINOR | issues.md "Failed or vacuous" 1 | "Fully non-degenerate boxes appear in about 1/128 of draws". 1/128 is the design rate. The observed rate is 6/3000 (2994 had a degenerate coordinate). The concern is small because the chain argument makes joint interaction irrelevant; r3 tests 120 fully non-degenerate boxes (364,800 evaluations, 0 violations). | c5 output; r3 part 2. |
| 12 | MINOR | issues.md float item 4 | The "textbook root returns 0 at |ā| ~ 1e-263" result is not in any saved output. It is reproduced now: textbook y = 0.0, stable y = 1.0. | r2 part 4. |
| 13 | MINOR | all `prompt_4_code` scripts | Despite `database=None`, hypothesis 6.170.15 writes `.hypothesis/constants/` in the current directory, and importing `common` writes `__pycache__/` next to the scripts. Both appeared on re-run and were deleted by this reviewer. Future in-repo property tests need `hypothesis.configuration.set_hypothesis_home_dir(<tmp>)` or a gitignore entry. | re-run log. |
| 14 | MINOR | c1 part 1, c4 part 1 | Some "Proof" lines are printed prose, not computed. The uniqueness and sign pattern of f'' in C1 and the sign of dh/ds in C4 are not checked symbolically. The SymPy lines verify only the formula for x*, the expression for dh/ds, and continuity at s = τ/k. The argument is correct (checked by hand below), but it should not be read as machine-checked. | code inspection. |
| 15 | MINOR | missed by answer | The winning-set boundary count per segment is ≤ 3 roots plus the jump at t_m: f can leave the win set at a boundary (jump +R_g) with no root. C1 alone does not bound the number of win/lose switches; a solver bracketing only roots misses these. | C2 + C1, by hand. |
| 16 | MINOR | missed by answer | For an intended ā = 0, the float value of ā is non-zero in 48 % of draws (2405 positive, 2400 negative of 10,000). The implied verdict time is ≥ 2.18e22 s, far beyond a 1e10 s horizon, and the drift \|ā\|τ lies inside the ε·S band. A solver must not declare "permanent" verdicts from sign(ā) alone; it must compare T with the horizon. | r4 part 5c. |

No BLOCKER.

## Reproducibility

| Script | Re-run vs saved output | Runtime | Answer numbers vs output |
|---|---|---|---|
| c1_root_count.py | byte-identical | 16.6 s | all match (3-root example, roots, signs, 37/126, 162, coverage). Exceptions: "60000 tuned" (finding 5) and issues "564" (finding 10) |
| c2_boundary_jump.py | byte-identical | 2.3 s | match (2500; 1166/1149/512/897). Float labels mis-characterised (finding 7) |
| c3_long_run.py | byte-identical | 7.3 s | match (1402/1370; 1992/961/1373/1559/1296; 4000 periodic, 0 bad; −1/8 example). The 1e-263 claim was not in the output (finding 12) |
| c4_tw_monotone.py | byte-identical | 6.4 s | match (1051/1880/2099/696; 10825/200000; 1.907e-6). Example class mismatch (finding 2) |
| c5_interval_screening.py | byte-identical | 8.7 s | match (311-769; 589/468/564/447/260; 857/511/329/310/287/310/396/1196; 952/1616; 0 float violations). "1/128" is design, not observed (finding 11) |
| r1_c1_exact_roots.py (review) | deterministic (re-run diff empty) | ~10 s | — |
| r2_c3_long_run.py (review) | deterministic | ~2 s | — |
| r3_c4_c5_monotone.py (review) | saved output | ~21 s | — |
| r4_float64.py (review) | deterministic | ~3 s | — |

## Proof checks

**C1. Agree: holds with conditions.** On (0, τ_w), f'' = −K_g/(4dt^{3/2}) + K_s/(4(t_m+dt)^{3/2}). It has the sign of φ = K_s·dt^{3/2} − K_g·(t_m+dt)^{3/2}, which vanishes iff ψ = dt/(t_m+dt) = ρ⁻¹. ψ is strictly increasing for t_m > 0, so there is at most one zero, at dt = t_m/(ρ−1), and only when K_s > K_g and m ≥ 1. It lies in (0, τ_w) iff m < ρ−1. If K_s < K_g, f'' < 0 for every m (since t_m+dt ≥ dt). If m = 0, f'' = (K_s−K_g)/(4dt^{3/2}) has constant sign, or is identically 0 when K_s = K_g. The crossing is transversal, so f is concave then convex. f is analytic on (0, τ_w) and continuous at dt = 0, so either it is identically 0 or, by Rolle applied twice, it has at most (number of zeros of f'') + 2 ≤ 3 distinct roots on [0, τ_w). Three roots need f'' to change sign inside, hence K_g > 0 and 1 ≤ m < ρ−1. They are attained: the answer's mp-60 example, confirmed by the exact quartic in r1 (count 3). For every such (m, ρ) a window exists (finding 6). The literal "at most one zero" fails only when f'' ≡ 0 (m = 0 with K_s = K_g, or K_g = K_s = 0). The answer's restatement follows, apart from the omissions in finding 6.

**C2. Agree: holds for m ≥ 1.** Segment m−1 at dt → τ_w gives a·t_m − K_s√t_m + d₀ + (m−1)R_g + m·K_g√τ_w. Segment m at dt = 0 gives the same plus R_g. The difference is −R_g by the definition of d_m', as the answer flags. The K_g√dt term restarts at 0 while m·K_g√τ_w steps by K_g√τ_w, so the K_g part is continuous. The hypothesis test on the global evaluator is a genuine (if easy) check.

**C3. Agree: holds as stated.** ā·τ expands to a·τ + m(R_g + K_g√τ_w) + (R_g + K_g√τ_w)·dt/τ_w. The remainder is r = −R_g·dt/τ_w + K_g√τ_w·(u − u²), u = √(dt/τ_w) ∈ [0,1). This gives −R_g < r ≤ K_g√τ_w/4, and r ≥ 0 when R_g = 0. The bounds, the three T formulas, and the use of the stable root are all correct. The bounds are sharp when R_g = 0 (finding 9). ā = 0 with K_s > 0 wins for τ > (max(c,0)/K_s)² with c = d₀ + K_g√τ_w/4, for every d₀, R_g and K_g (r2 part 1, exact). ā = 0 with K_s = 0 makes f exactly τ_w-periodic, and "periodic" is all the claim says. The ā = 0 cases are correct.

**C4. Agree: holds with conditions (K_g > 0 and s ∈ (0, τ] for strictness).** On (τ/(k+1), τ/k], m = k and dh/ds = (K_g·k/2)(s^{−1/2} − r^{−1/2}) with 0 ≤ r < s, so the derivative is negative. The one-sided derivative is −∞ from the left at s = τ/k, and 0 from the right for k ≥ 2: h is nearly flat just above each tie but still strictly decreasing. At s = τ/k both branches give K_g√(kτ), so h is continuous. m = floor(τ/s) is non-increasing and left-continuous, so m·R_g is too. For s ≥ τ, h = K_g√τ is constant. Shorter τ_w is therefore never favourable, weakly for all τ_w > 0. r3 part 1 scans every tie s = τ/k (68 k values) with ±1e-30 neighbours: 0 increases under floor, and 0 under the alternative convention m = ceil(τ/s) − 1 (which the answer argued but did not test).

**C5. Agree with the directions and the inclusion. Disagree with the stated condition (finding 1).** The partial derivatives give pessimistic = (a max, K_g max, K_s min, d₀ max, R_g max, τ_w min, λ min). The τ_w part follows from C4 plus the flat region τ_w > τ, where m drops from 1 to 0 as τ_w crosses τ, a downward step of R_g. Ties need no extra convention, because floor(τ/s) is monotone in s for any τ. Shrinking τ_w can move τ into a later segment, but that raises m·R_g and raises h, so it never lowers f (r3 part 1). Strict win sets: f_pess < 0 ⇒ f_x < 0 ⇒ f_opt < 0, and f = 0 is never a win. A product box is a proof device, not an input assumption. r3 part 2: 120 fully non-degenerate boxes, all 128 vertices plus 24 interior points, ties for 4 τ_w values with ±1 ulp: 364,800 evaluations, 0 order or inclusion violations, 312 pessimistic wins, 1003 optimistic-only wins.

## Missed cases

- **a < 0 with large m:** no effect on any verdict. It does not enter f'', and ∂f/∂a = τ ≥ 0 whatever the sign of a.
- **K_s > K_g with ρ−1 small:** for m ≥ 1 an inflection inside needs ρ > m+1 ≥ 2, so small ρ−1 never matters. Float ρ−1 has 50 % relative error at K_s = K_g(1 + 2⁻⁵²), which is harmless because x* > 1e15·t_m. K_s == K_g raises ZeroDivisionError, and so does K_g = 0. Test `m ≥ 1 and K_s² > K_g²(m+1)³` instead of forming x* (r4 5a-5b).
- **Tie convention vs τ_w-monotonicity:** no effect under either convention (r3 part 1).
- **λ inside d₀:** safe if D and λ are boxed separately. If the d₀ interval is already net of λ and λ is subtracted again, the pessimistic corner can claim a win the true worst input does not have (r3 part 4).
- **Corners in an underlying parameter space:** this breaks C5 (r3 part 3). The spec should say that corners are taken per coefficient over intervals that contain every value the coefficient can take.
- **Win/lose switches at jumps:** at most 3 roots plus 1 jump per segment (finding 15).
- **Winning-set inclusion at ties:** f = 0 is not a win, and it is handled correctly by the strict inequalities. r2 shows f = 0 exactly at τ = T, so a solver must decide the tie at the boundary deliberately.

## Float64 issues

1. **Tie hazard: real, undersized (finding 2).** Within 0.5 ulp(τ) of j·τ_w, float m and exact m can differ, and when they do, f is off by exactly R_g (r4 part 1: f_float − f_exact = 7.0 for R_g = 7). Implication: carry tie points as an integer j with dt = 0, never as τ = fl(j·τ_w) followed by floor. For a general τ, treat |τ − j·τ_w| ≤ ulp(τ) + j·ulp(τ_w) as ambiguous and evaluate both sides.
2. **dt cancellation: real in the magnitude claimed, mislabelled (finding 8).** With m correct, r4 part 2 gives |f_float − f_exact| ≤ 4ε·S + 2·K_g·ulp(τ)/√(dt + ulp(τ)) in all 38,570 cases (max ratio 0.432), where S = |aτ| + K_s√τ + |d₀| + m·R_g + m·K_g√τ_w + K_g√dt + λ and ε = 2⁻⁵². This is a usable solver tolerance on f. The ε·S term alone reached 1.34 ε·S, and the dt term alone 0.865 of its model.
3. **K_s = K_g at m = 0: real but small.** It reproduces (float f == 0 at 999/999 points while the exact f = a·dt > 0). It is one instance of the general rule that the sign of f is undetermined when |f| < 4ε·S. The tolerance in item 2 covers it; the special-case rewrite is optional.
4. **Sign of ā: not raised by the answer (finding 16).** Covered by the same tolerance once T is compared with the horizon.

Solver tolerance, in short: classify f < −tol as a win, f > tol as a loss, and |f| ≤ tol as undetermined, with tol from item 2. Add the R_g ambiguity inside the tie band of item 1, and give ties as integers.

## What still needs external checking

- **C1 and C4 proofs.** The convexity/Rolle argument and the piecewise-derivative plus continuity argument are hand sketches (here and in the answer). The SymPy lines check only fragments (finding 14). A written proof checked by a person, or a second CAS such as Maxima or Mathematica, is needed for anything above `derived`.
- **C5 interface statement.** It needs the per-coefficient bounding-box wording and the λ handling (finding 1). It cannot be tested until the solver's screening code exists.
- **Tolerance model.** The model above is empirical (40,000 draws) and is not a proven error bound. A proven forward-error bound for the evaluator is outstanding.
- **Single most decisive further check:** when the solver exists, a differential property test of its float64 screening and verdicts against an exact-rational reference evaluator (like `f_exact` in r3/r4). Ties go in as integer j. Use fully non-degenerate boxes, and assert that every float verdict outside the tolerance band agrees with the exact one. The lemmas themselves are short proofs; the failures demonstrated in this round (tie misassignment, corner construction, λ double count) all live at that interface.

UNSURE: none of the numbers above. Finding 3's 263/3000 comes from the same strategy shape, not the implementer's identical draws.
