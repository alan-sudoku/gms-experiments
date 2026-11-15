# Prompt 8 S5 review: infrastructure credit shared by several products (OQ-14)

Context file (`local_docs/`, never cited by the spec). Written 2026-11-15 by an independent `opus` S5 reviewer. Inputs: `fable_questions.md` Prompt 8 block (lines 287–325); `fable_runs/prompt_8_web_answer.md`; GMS-100 §1.2, §2.1, REQ-LIFECYCLE-CEXC-SOURCE, EQ-LIFECYCLE-INCUMBENT-INITIAL-CAPITAL, Open items; drafting notes E16, U2, U6; OQ-14; Prompt 2 synthesis D4; `prompt_2_review_code/rv03_ledger_and_misc.py` §D (re-run to scratch: D1–D3 identical to the saved output). Scripts: `fable_runs/prompt_8_review_code/rv01`–`rv06`, outputs in `outputs/`. Every statement here is a claim at level `derived`. That the reviewer agrees with the answer is not validation. All the inputs are made-up numbers from rv03.

## Summary verdict

1. Every number in the answer reproduces (rv01). Claims 1, 3 and 4 are correct within the linear single-block model. Claim 2 is correct for rules that must return pass or fail, and the answer's three-way rule is the most decisive sound rule possible from one product's data in that model (rv02).
2. The proposed first-edition rule ("λ = v/T unconditional") is not a lower bound under market rebound or a convex B_infra. There it gives wrong verdicts labelled unconditional (losses 6.58e9 to 2.20e10 J/K). Under capacity steps the lower bound holds.
3. Cases exist where every alternative (E16, the average share without the gate, marginal only, and the answer) is wrong: capacity steps, partial rebound and convex B_infra. They occur in 2–12 % of random profiles in those regimes and in 0 % of linear profiles (rv04).
4. The current spec is wrong in rv03's own case (loss 2.62e10 J/K). It also has two defects the answer could not see: REQ-LIFECYCLE-CEXC-SOURCE item 4 lets the average share return through CExC when λ_ℰ = 0 (loss 1.01e11 J/K), and no rule keeps the operating part of B_infra out of CExC (double count, loss 2.88e10 J/K).
5. For 0.1 the spec could adopt a sound three-way verdict built only on B_infra, T₀ and one new input N_k (rv04 R5: no wrong unconditional verdict in any regime tested), and close the two CExC gaps. The F/v split, partial-exit credit and the owner of a multi-product verdict stay open (OQ-14).

## Findings

| # | Severity | Location | Finding | Evidence |
|---|---|---|---|---|
| 1 | MAJOR | spec, REQ-LIFECYCLE-CEXC-SOURCE item 4 | Item 4 forces capital goods out of CExC only when λ_ℰ > 0. Under E16 a partial exit has λ_ℰ = 0, so a CExC source that includes capital goods brings the average share back through Σ_s,init and bypasses the gate. The answer flagged this risk (claim 5); it is real. | rv06, rv03 case, config B: `E16 -> [1] (gate shut, lambda = 0), loss 1.0087e+11 J/K` |
| 2 | MAJOR | spec, B_infra definition and item 4 | B_infra includes "monitoring, assaying and maintaining", which are operating flows that a CExC source may already contain. Item 4 removes only capital goods, so when the gate opens v/T₀ is counted twice. The answer's "never both" safeguard cannot be enforced because the spec has no F/v split. | rv06 d0=(230,230), config C: `E16 -> [1, 2] (gate open ...), loss 2.8759e+10 J/K`; `double count 67.0803 J/K per position` |
| 3 | MAJOR | answer claims 6, 7 | "λ = v/T unconditional" fails as a lower bound when outside users absorb freed supply (rebound ρ) and when B_infra is convex and v is read as B′(N). It holds under capacity steps. | rv04: `rho=0.5: true lone-exit saving per position = 33.54 J/K`; `(v) ... true saving per position = 44.4407 J/K`; `(ii) min ... = 1.0000` |
| 4 | MAJOR | all rules | Cases exist where E16, the average share without the gate, marginal only and the answer's rule are all wrong (see Missed regimes). | rv04 `every alternative R1-R4 wrong: True` (three hand cases); random shares 0.021 / 0.119 / 0.045 |
| 5 | MAJOR | spec, E16 + λ_ℰ | E16 loses the whole joint gain in rv03's case. Because B_infra includes the sunk "establishing" part, it also credits sunk exergy when the gate opens. | rv04 base `R1: ... loss = 2.6241e+10`; (i) α=0.5 `R1: S = [1, 2] ... loss = 1.9839e+10` |
| 6 | MAJOR | answer claim 6 vs U6 | The staggered-switching modifier makes λ_hi depend on the last switching date and on the remaining maintenance horizon. U6 makes λ_ℰ independent of τ. | rv05: `t_last < H (1 - sum phi) = 5.868 yr`; λ_hi of last mover `1229.81` vs `1050.93 J/K` |
| 7 | MAJOR | answer claim 7 vs GMS-100 (e) | A system verdict over several products cannot be reached inside GMS-100. EQ-LIFECYCLE-OBJECTIVE covers one system, and no symbol carries another product's N_k or d_k, F_av, or the outside users. | spec text (Fit, point e) |
| 8 | MINOR | answer claim 2 | "No per-product rule ... can agree" is too broad as worded. It holds for complete (pass/fail) rules only. A sound three-way rule exists, and the answer's band is exactly the region that one product's data cannot decide. | rv02 T2a (band edges 67.0803 and 216.1477); T2b `wrong unconditional verdicts = 0` |
| 9 | MINOR | answer claim 5 | The under-credit of 67.08 J/K holds only when v sits outside CExC and the source excludes capital goods (config A). With v inside CExC there is no under-credit; with capital goods inside, there is an over-credit. The d1 = 50 example understates the loss: the optimum there is all switch, not product 1 alone. | rv01 `W(all) at d1=50,d2=400 = +1.1624e+11`; rv06 claim 5 config A `loss 1.1624e+11` |
| 10 | MINOR | answer claim 3 | "Not Shapley" depends on who the players are. With equal blocks of positions as players, the Shapley value is the average share. | rv03 G4 `lambda1 = 201.2410, lambda2 = 201.2410` |
| 11 | MINOR | answer, all claims | The answer uses T_ref where the spec uses T₀. The rule's structure is invariant when every term uses the same T₀; mixing T_ref in λ_lo with T₀ in Σ shifts the threshold. | rv06 (a) T0=250: `sum 0.80441` vs mixed `0.88515` |
| 12 | MINOR | answer claim 7 | "Average rule loses 7.46e10 J/K" is measured against doing nothing. Against the optimum the loss is 1.0087e11 J/K. | rv01 `loss vs optimum = 1.0087e+11 J/K` |
| 13 | MINOR | answer claim 3 | The uniform-λ condition max d_k < B/(T N) is true by construction: it restates the budget constraint. | rv03 G5 |
| 14 | MINOR | answer open point 3 | Uncertainty in d_k does not bias the decision, because W(S) is linear in d and so a decision taken on means maximises expected W. It does make the "unconditional" labels near the edges unreliable. | rv05 `mean d = 60.0 ... P(true d > v/T) = 0.2398`; `sd = 10 % ... P(...) = 0.0312` |

## Reproducibility (rv01 unless stated)

| Claim | Answer value | Script value (output line) | Status |
|---|---|---|---|
| 1 | F/T = 1.3416e11; excess 7.463e10 + 3.329e10 = 1.0792e11 J/K | `F/T = 1.34161e+11`; `7.4628e+10`, `3.3292e+10`, `sum = 1.07920e+11` | ok |
| 1 | gain 2.62e10 J/K; W({1}) = −7.46e10, W({2}) = −3.33e10 | `W([1, 2]) = +2.6241e+10`; `-7.4628e+10`; `-3.3292e+10` | ok |
| 2 | d2=700: 2.05e11 > 2.0124e11; flip d2* = 662.4 J/K | `2.0500e+11 J/K vs B/T = 2.01241e+11`; `flip d2* = ... 662.4099` | ok (counterexample valid) |
| 3 | f1/F ∈ (0.556, 0.752) | `(0.5563, 0.7519)`; grid rv03 G3 `[0.5563, 0.7519]` | ok |
| 3 | per-position f1/F = 0.90, λ = 201.24 | `f1/F = N1/N = 0.900 -> lambda = 201.2410` | ok |
| 3 | Shapley λ1 = 141.6, λ2 = 737.9 J/K | `lambda1 = 141.6140, lambda2 = 737.8836` | ok, but depends on the player definition (F10) |
| 4 | λ_hi = 216.15, 1408.7 J/K; φ = 0.556, 0.248, sum 0.804 | `216.1477`, `1408.6869`; `phi1 = 0.55626, phi2 = 0.24815, sum = 0.80441` | ok |
| 5 | v/T = 67.08; d1=50: W({1}) = +1.54e10 J/K | `v/T = 67.0803`; `W({1}) = +1.5372e+10` | ok; optimum there is all, `+1.1624e+11` (F9) |
| 6 | α flip 0.804; α=0.8: W(all) = −5.9e8 J/K | `alpha = 0.80000: W(all) = -5.9115e+08`; at 0.80441 `-1.5259e-05` (≈0) | ok |
| 7 | widths 149, 1342 J/K | `149.0674`, `1341.6066` | ok |
| 7 | marginal-only forgoes 2.62e10; average loses 7.46e10 | `forgoes 2.6241e+10`; `W({1}) = -7.4628e+10` | ok; second is vs doing nothing (F12) |
| rv03 D | λ = 201.24, v/T = 67.08, under-credit 134.16, 1.75e11 vs 2.01e11 | `201.2410`, `67.0803`, `134.1607`, `1.7500e+11`, `2.01241e+11`; saved rv03 output identical | ok |

## Claim by claim

1. **Agree.** Enumeration over 20 000 random profiles (2–6 products, including ties d_k = v/T, d_k < v/T and exact ties F/T = Σ excess) found no case where the optimum differs from max(W(S_m), W(all)) and no violation of the switching condition. rv02: `optimum != max(W(S_m), W(all)): 0 cases; switching-condition violations: 0 cases`. Under ties both candidates are optimal.
2. **Agree, with a narrower scope.** The counterexample is valid: product 1's verdict must be "switch" at d2 = 400 and "stay" at d2 = 700, and both optima are unique. The impossibility rules out any complete rule (pass/fail, or a λ) built from (F, v, N, N_k, d_k) that matches the system optimum for every profile of the other products. It applies only while v/T < d_k < v/T + F/(T N_k) and N > N_k (rv02 T2a: outside the band, and for a sole user, one product's data decide). It does not rule out: (i) a sound three-way rule; (ii) rules that use shared information (a register of every product's N_j and d_j); (iii) rules that are right in expectation under a prior on the other products; (iv) a verdict that is explicitly conditional on a declared scenario (E16 is such a verdict, but it hides the condition). The answer's rule escapes only by returning "conditional", and its conditional band is exactly the region where one product's data cannot decide. It is therefore the most decisive sound rule possible from one product's data in the linear model (`derived`). rv02 T2b: 0 wrong unconditional verdicts out of 80 251, 42.2 % conditional.
3. **Agree on the arithmetic; the labels are partly UNSURE.** Submodularity (0 violations), the core equal to {f_k ≥ 0, Σ f_k = F} (300/300 games) and the supporting interval all check out (rv03 G1–G3). "Concave cost game ⇒ non-empty core containing the Shapley value" is the convex-game result. The exact attribution (Shapley 1971) is UNSURE and was not checked here. "Not Shapley" holds only with products as players (F10). The uniform-λ condition is true by construction (F13). The core of a game is a stability concept. A split that supports the joint decision is a different requirement; here every supporting split happens to lie in the core, but the answer does not keep the two apart.
4. **Agree within the linear model.** The rule is sound and is exactly the decidable/undecidable boundary (claim 2 above). Outside the linear model, see claim 6 and F3.
5. **Partly agree.** "Gate only F" is right in the linear model. The bypass risk is real under the current wording (F1). The under-credit of 67.08 J/K holds only in config A (rv06). Under config C (v is an operating flow inside every CExC), the lone switcher already receives v through Σ_s. Under config B it receives the average share and is over-credited by 134.16 J/K. The d1 = 50 example understates the loss (F9).
6. **Partly agree.** The α part is right (flip at α = 0.80441; rv01). On capacity steps: λ_lo stays a lower bound (rv04 `min ... = 1.0000`), the two-candidate shortcut fails (rv04 (ii): optimum {2}), and the core can be empty (rv03 G6: `core EMPTY` with F_step = 3 > F0 = 1, three products of 4 against Q = 10). On outside users: λ = v/T is exact only when there is no rebound (rv04 (iii): saving 33.54 at ρ = 0.5 and 0.00 at ρ = 1). On staggered switching: right (rv05: the myopic sequential outcome is `[]` for every date pair, while committed joint switching at dates (2, 4) yr gives `W(all, committed) = +8.3529e+09`), but it conflicts with U6 (F6).
7. **The verdict follows only inside its stated validity range** (linear, single fixed block, F_av known, simultaneous switching, no outside users). There, R4 has 0 losses in the linear and α regimes (rv04 random). It does not follow as a 0.1 spec rule, for three reasons. (a) F, v and F_av are not spec symbols, and where v sits inside CExC cannot be checked (F2). (b) "Unconditional" λ_lo fails under rebound and convexity (F3); the validity range lists "no outside users" but the text of claim 6 calls λ_lo "exact" with outside users. (c) No document owns the system verdict (F7). The bracket widths (149.07 and 1341.61 J/K) are right.

## Derivation checks

- **Two candidates (claim 1).** For S ≠ all, W is additive over products, so the best partial set is S_m. "All" adds F/T. Hence the optimum is max(W(S_m), W(all)), and all is optimal iff F/T > Σ N_k max(0, d_k − v/T). Confirmed by enumeration (rv02).
- **Core (claim 3).** The singleton constraints give f_k ≤ F. The complement constraints give y_k ≥ v N_k, i.e. f_k ≥ 0. So the core is the simplex of F splits (rv03 G2, by LP).
- **Supporting split.** f_k > φ_k F for every k with φ_k > 0, Σ f_k = F, which is feasible iff Σ φ_k < 1. This is the same inequality as claim 1.
- **Sound bounds.** In any model where B is non-decreasing in the draw, adding product k to any switching set changes W by between −N_k d_k and −N_k d_k + B_av(N)/T₀. So "pass if d_k < 0" and "fail if d_k > B_av(N)/(T₀ N_k)" are sound without any F/v split. This is R5; rv04 random reports `wrong unconditional ... R5 0.000` in all five regimes. The answer's tighter bounds need B(M) − B(M − N_k) ≥ v N_k for every M, which fails under rebound and under convexity with v = B′(N).
- **Uncertainty.** For fixed S, W(S) is linear in d, so the decision on means maximises expected W. Uncertainty affects regret and the labels, not the expected-value decision (rv05: E[W(all)] stays about `+2.62e+10` from sd 5 % to 30 %).

## Missed regimes, including cases where every alternative is wrong

R1 = E16 (source without capital goods), R2 = average share without the gate, R3 = marginal only, R4 = the answer with full information. All lines are from rv04.

| Case | Optimum | Loss of R1 / R2 / R3 / R4 (J/K) | Every alternative wrong? |
|---|---|---|---|
| rv03 base (linear) | {1,2}, `+2.6241e+10` | 2.6241e10 / 1.0087e11 / 2.6241e10 / 0 | no |
| (i) α = 0.5, d = (150, 190) | {} | 1.9839e10 / 1.9839e10 / 0 / 0 | no (E16 credits sunk F) |
| (ii) steps: N = (4,3,3)e8, d = (200,120,400), F0 = 2e13, F_step = 1e13, Q = 3.5e8 | {2}, `+1.7664e+10` | 1.7664e10 / 1.9628e10 / 1.7664e10 / 1.7664e10 | **yes** |
| (iii) outside users 5e8, ρ = 0.5, N = (4,1)e8, d = (50, 20) | {2}, `+1.3540e+09` | 1.3540e9 / 6.5839e9 / 6.5839e9 / 6.5839e9 (R4 labels product 1 "unconditional pass" wrongly) | **yes** |
| (iii) same, ρ = 1 | {} | 0 / 2.2000e10 / 2.2000e10 / 2.2000e10 (both labels wrong) | no (E16 right by luck) |
| (v) convex, N = (9,1)e8, d = (55, 5000) | {} | 0 / 9.5034e9 / 9.5034e9 / 9.5034e9 | no |
| (v) convex, N = (6,3,1)e8, d = (55, 20, 5000) | {2}, `+1.1860e+10` | 1.1860e10 / 1.0863e10 / 1.0863e10 / 1.0863e10 | **yes** |
| (iv) staggered, dates (2, 4) yr, H = 30 yr (rv05) | all committed, `+8.3529e+09` | E16 and marginal 8.35e9; myopic answer 8.35e9; R4 with F_av(t_last) known 0 | no |

Random search (rv04, 3 products, 4 000 profiles per regime). Share of profiles where all of R1–R4 are wrong: linear 0.000, α 0.000, steps 0.021, outside users with rebound 0.119, convex 0.045. Wrong-verdict share of R4: 0.000 / 0.000 / 0.069 / 0.352 / 0.080. Wrong unconditional verdicts of R4: 0 in linear, α and steps; 0.352 with rebound; 0.078 convex. The reviewer's sound bracket R5 never gives a wrong unconditional verdict, but its decisions are wrong more often in the linear regime (0.071 against 0.000), because it gives no credit for a partial exit.

## Fit with the spec

- **(a) T₀ ≠ T_ref.** None of the answer's rule changes in structure when every term is divided by the evaluation's T₀. φ_k is a ratio of lost works and stays at 0.80441 at 250 K and 200 K when lost work does not depend on T₀ (rv06). Read literally with T_ref (λ_lo = v/T_ref) next to Σ at T₀, it gives Σφ = 0.88515 at T₀ = 250 K and 0.96900 at 200 K, and the edge moves from 67.08 to 80.00 J/K at 250 K. Separately, d_k itself moves with T₀ when it mixes operational entropy fixed by the process with upstream lost work (made-up split: Σφ 0.8044 → 0.4975 → 0.1787). This is the ranking effect EQ-LIFECYCLE-LOST-WORK-CURRENCY already states, not new. Fix: replace T_ref by T₀ throughout.
- **(b) Sunk "establishing".** Yes. For an existing supply chain, λ_ℰ as the average share of the whole of B_infra credits exergy already spent. rv04 (i), α = 0.5, d = (150, 190): E16 switches both and loses 1.9839e10 J/K. The answer's F_av = αF is the right correction for the sunk part. Two caveats: future re-establishment (mine replacement within the horizon) is avoidable and belongs in F_av, which ties (b) to (d); and B_infra is defined as a *minimum* exergy, which as a credit understates actual avoided destruction (UNSURE whether that was intended).
- **(c) What the current spec credits a lone switcher (rv03 case).** Under E16 the gate is shut because product 2 fails even at 201.24, so λ_ℰ = 0 for both products.
  - Config A (source without capital goods; v capital-like, outside CExC): credit 0. Nobody switches, loss 2.6241e10 J/K. Here claim 5's under-credit of v holds.
  - Config B (λ_ℰ = 0, so item 4 allows capital goods, assumed allocated at the average share): Σ_s gains about 201.24 J/K. Product 1 switches alone, loss 1.0087e11 J/K. This is the answer's bypass, confirmed (F1).
  - Config C (v is an operating flow in every CExC): the lone switcher already receives v. Claim 5's under-credit does not exist, and adding λ_lo would double count. When the gate opens, E16 itself double counts v/T₀: at d0 = (230, 230) the loss is 2.8759e10 J/K (F2).
  - So claim 5 holds in A, is double counting in C, and is the reverse (over-credit) in B. The spec cannot tell A from C because it has no F/v split.
- **(d) U6.** In the answer's validity range (simultaneous switching) there is no conflict. Its staggered modifier conflicts: F_av = m(H − t_last) makes λ_hi a function of the switching dates and of the remaining maintenance horizon. If H is the product horizon τ, λ depends on τ, which U6 excludes, and the piecewise structure of f(τ) changes. Staying within U6 needs the switching dates and the infrastructure horizon to be scenario inputs fixed independently of τ. Note that d_k already depends on τ, so any system verdict (Σφ_k < 1) is τ-dependent regardless.
- **(e) One system, and within-product sharing.** EQ-LIFECYCLE-OBJECTIVE minimises over (ℰ*, 𝓖) for one system, per functional unit. No term carries another product's Σ, N_k or the outside users, and E16 reads "x leaves every product" as a fact, not as a computed outcome. A multi-product system verdict is therefore not reachable inside GMS-100. It needs an owner that consumes several products' GMS-100 results. A higher-tier scenario or portfolio document would satisfy DEF-DEPENDENCY-RULE. The within-product case (two components of one product using x) has the same cost structure (F is saved only when every component drops x) but not the same information problem: one analyst holds every d_k, and dropping x from ℰ* is a joint choice. So the subset enumeration is reachable there. GMS-100 still lacks a product-level functional that sums several component positions, and its parity assumption ("no other component uses x") excludes the case rather than treating it.

## What the spec could adopt for 0.1, and what stays open (proposals, not decisions)

Could adopt with existing symbols plus one scenario input:
1. **Close the bypass (F1).** REQ-LIFECYCLE-CEXC-SOURCE item 4 would read: excludes capital goods for x in every evaluation in which B_infra(x) is in scope, not only when λ_ℰ(x) > 0. No new input.
2. **Partition rule (F2).** A new condition: no upstream flow is counted in both CExC(x) and B_infra(x), and the source declares which of "monitoring, assaying, maintaining" it contains. No new symbol. It needs a statement from the data source.
3. **Three-way verdict for a partial exit (R5).** Pass unconditionally if f(τ) < 0 with λ_ℰ = 0. Fail unconditionally if f(τ) ≥ 0 with credit B_infra(x)/(T₀ N_k). Otherwise report "conditional on the other products" together with ψ_k = N_k T₀ (Σ_g − Σ_s)/B_infra. The one new input is N_k, the positions of this product sharing B_infra(x), a scenario input like N_alloc. In rv03's case: product 1 (0, 223.60), product 2 (0, 2012.41), ψ = 0.6708 and 0.1988, sum 0.8696 < 1 (rv06). It is sound in every regime tested (rv04). The price is a wider conditional band than the answer's (67.08, 216.15).
4. **State the sunk-part bias.** Either define B_infra as the avoidable (forward-looking) part, which is a semantic change and is free before the tag, or record that λ_ℰ over-credits the sunk "establishing" part as a known bias with a known-bug test.
5. Replace T_ref by T₀ wherever the answer's form is used (F11).

Stays open (OQ-14 and new OQ text):
- The F/v split and its data, and therefore any partial-exit credit above 0 (the answer's λ_lo). It also needs the rebound and convexity conditions (F3).
- The owner of a multi-product system verdict and its inputs: N_k and d_k (or ψ_k) of every sharing product, the outside users, and the avoidable B_infra (F7).
- Capacity steps and other non-linear B_infra, where subset enumeration is needed.
- Staggered switching versus U6 (F6).
- Margins under uncertainty for the "unconditional" labels (F14).

## What still needs external checking

- Whether real CExC(x) sources contain capital goods and the operating "maintaining/monitoring" flows, and at what allocation (configs A/B/C).
- The avoidable fraction α of the fixed part, and the F/v split for a real scarce element.
- Whether market rebound is material for scarce elements: ρ for outside users of x.
- The attribution of the convex-game core result (UNSURE label).

**Single most decisive check:** for one real scarce element, take the CExC data source GMS-100 would use and decompose its supply-chain exergy into capital (fixed and throughput-proportional), operating and maintenance parts. Compare that with an independent B_infra estimate split into sunk, avoidable-fixed and variable parts. This one decomposition decides which config (A, B or C) the spec is in, and so whether E16 under-credits, over-credits or double counts. It also gives α, on which rv03's joint verdict flips at 0.804.
