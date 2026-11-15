# Prompt 8: infrastructure credit shared by several products (low-budget run, OQ-14)

Context file (`local_docs/`, never cited by the spec). Run 2026-11-15 per `local_docs/orchestration/fable_delegation_plan.md` §5.1, as a Fable agent (`fable`, effort high, no tools; about 42k tokens, 2 min); input was the Prompt 8 block in `local_docs/fable_questions.md` verbatim. The reply below is saved as returned. Every claim is at level `derived`; an `opus` S5 checks it against E16, U2, U6 and `prompt_2_review_code/rv03_ledger_and_misc.py` in Prompt 8's own session.

---

No tools were used; all figures are hand arithmetic from the numbers in the question, and every claim is level `derived`.

**1. The decision object is the set of products that switch, not a single product.** Confidence: high.
- W(S) = sum_{k in S} N_k·(v/T_ref − d_k) + [S = all users]·F/T_ref, in J/K; choose the S that maximises W.
- For B_infra = F + v·N only two candidates can be optimal: S_m = {k: d_k < v/T_ref}, or all users.
- All switch iff F/T_ref > sum_k N_k·max(0, d_k − v/T_ref).
- Here: 1.3416e11 > 7.463e10 + 3.329e10 = 1.0792e11 J/K, so both switch, with a gain of 2.62e10 J/K.
- W({1}) = −7.46e10 J/K and W({2}) = −3.33e10 J/K.
- Falsify: enumerate the 4 subsets; any W above 2.62e10 J/K refutes this.

**2. No per-product rule built on own-product data can agree with the system test.** Confidence: high.
- Counterexample: hold product 1's inputs fixed and set d2 = 700 J/K. Then N1·d1 + N2·d2 = 2.05e11 > 2.0124e11 J/K, and the optimum is that nobody switches.
- At d2 = 400 J/K the optimum is that both switch. The flip is at d2* = 662.4 J/K.
- Product 1's inputs (F, v, N, N1, d1) are identical in both cases, so any λ(F, v, N, N1, d1) gives the wrong verdict in one of them.
- Cause: F is a threshold saving (non-convex), so no single price decentralises the decision.
- Falsify: exhibit a function of those five inputs that gives product 1 the right verdict at both d2 = 400 and d2 = 700.

**3. It is a cooperative cost game; supporting λ_k exist after the fact, but they are not uniform, not the average share and not Shapley.** Confidence: high for the arithmetic, medium for the game-theory labels.
- Cost game: c(S) = F + v·N_S (J) for non-empty S. It is concave, so the core is non-empty (convex-game result; UNSURE of the exact statement).
- Core here: y_k = v·N_k + f_k with f_k >= 0 and sum f_k = F. This gives λ_k = v/T_ref + f_k/(T_ref·N_k).
- Every per-product test agrees with the system test iff f_k/T_ref > N_k·(d_k − v/T_ref) for all k. That is feasible exactly when the inequality in claim 1 holds.
- Here f_1/F must lie in (0.556, 0.752).
- The per-position split gives f_1/F = 0.90, so λ = 201.24 < 400 and product 2 fails.
- The Shapley split (F/2 each) gives λ_1 = 141.6 < 150, so product 1 fails; λ_2 = 737.9 J/K.
- A uniform λ that does not credit more than is saved exists iff max_k d_k < B_infra/(T_ref·N).
- Any supporting split needs every product's d_j and N_j, which a single-product analyst does not have.
- Falsify: recompute λ_1 with f_1 = F/2.

**4. Per-product rule: a three-way verdict with a bracket whose top is not the average share.** Confidence: high within the model.
- λ_lo = v/T_ref.
- λ_hi,k = v/T_ref + F_av/(T_ref·N_k), where F_av is the avoidable part of F.
- If d_k < λ_lo: prefer g, unconditionally.
- If d_k > λ_hi,k: keep s, unconditionally, because even the whole of F cannot pay for it.
- Otherwise the verdict is "conditional", and the specification reports the required share φ_k = N_k·(d_k − v/T_ref)·T_ref/F_av (dimensionless).
- System verdict: all switch iff sum of φ_k < 1 over all users with φ_k > 0.
- Here λ_hi = 216.15 J/K (product 1) and 1408.7 J/K (product 2); φ = 0.556 and 0.248, sum 0.804 < 1.
- The average share 201.24 J/K is not an upper bound: product 2 should switch at d2 = 400.
- Falsify: find a profile with d_k > λ_hi,k where the optimum still contains k.

**5. The all-or-nothing gate is right for F and wrong for v·N.** Confidence: high; medium for the bypass risk.
- Product k saves v·N_k by leaving alone. The current rule gives a lone switcher λ = 0, an under-credit of 67.08 J/K.
- Example: d1 = 50 J/K with product 1 switching alone gives W = 9e8·(67.08 − 50) = +1.54e10 J/K, yet the current rule rejects it.
- Fix: count v always, either inside x's cumulative exergy or as λ_lo, never both. Gate only F.
- Risk: if x's cumulative exergy includes capital goods at the average share whenever λ = 0, the 201.24 J/K enters through Σ_s and bypasses the gate. This depends on the spec wording.
- Falsify: compute W({1}) at d1 = 50.

**6. The four modifiers.** Confidence: medium.
- **F partly avoidable:** F becomes F_av = α·F. Exergy already spent is sunk and earns no credit. The verdict flips when α < sum φ_k = 0.804; at α = 0.8, W(all) = −5.9e8 J/K.
- **Capacity steps:** B_infra = v·N + F_0 + F_step·ceil(N/Q). A partial exit that crosses a step earns F_step, so the gate is wrong. The two-candidate shortcut fails and subsets must be tested (knapsack-like). The core may be empty (UNSURE). λ_lo remains a valid lower bound.
- **Outside users that stay:** F is never avoided, so λ = v/T_ref is exact and in this example neither product switches. N_alloc must count the outside users, otherwise the average share over-credits.
- **Staggered switching:** F_av is saved only after the last exit, t_last = max t_k, and shrinks with delay. Early switchers get only v. Under myopic sequential tests the last mover sees λ_hi,k and early movers see λ_lo, so nobody moves first in this example although joint switching gains.
- Falsify: recompute W(all) at α = 0.8.

**7. Verdict for a first edition.** Confidence: medium.
- Rule: λ = v/T_ref, unconditional. F enters only a system verdict (sum φ_k < 1 with all users enumerated). Otherwise report "conditional" with [λ_lo, λ_hi,k] and φ_k.
- Validity: linear B_infra with a single fixed block, F_av known, simultaneous switching, no outside users.
- It is wrong by enough to flip a verdict whenever λ_lo < d_k < λ_hi,k. The bracket width is F_av/(T_ref·N_k): 149 J/K for product 1 and 1342 J/K for product 2.
- In this example the marginal-only rule forgoes 2.62e10 J/K, and the average rule loses 7.46e10 J/K if product 1 switches alone.

**Open points**
- Whether F and v can be separated in real data, and how much of F is avoidable rather than sunk; F_av is the dominant uncertain input.
- Market-mediated effects (outside users absorbing freed supply), non-linear B_infra(N), and whether the core is empty under capacity steps.
- How uncertainty in d_k propagates into φ_k and the sum φ_k < 1 test.
