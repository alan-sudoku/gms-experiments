# Prompt 7: entropy currency across environments (low-budget run, OQ-13)

Context file (`local_docs/`, never cited by the spec). Run 2026-11-15 per `local_docs/orchestration/fable_delegation_plan.md` §4 (Prompt 7 row) and §5.1, as a Fable agent (`fable`, effort high, no tools; about 44k tokens, 6 min); input was the Prompt 7 block in `local_docs/fable_questions.md` verbatim. The reply below is saved as returned. Every claim is at level `derived`; `opus` S5 checks it against E15 and `prompt_2_review_code/rv02_dead_state_currency.py` in Prompt 7's own session.

---

No tools were used; everything below is first-principles reasoning with no external check.

**1. Neither currency is a resource measure; (A) is the closer one.**
- For a fixed functional unit, resource cost is primary exergy drawn from the resource store: C = Σ_k c_k · T₀,k · S_gen,k [J], where c_k [–, ≥ 1] is primary exergy per J of work delivered in environment k.
- (A) is this with c_k = 1 everywhere. (B), multiplied through by T_ref, is this with c_k = T_ref/T₀,k.
- c_k = 1 is a physical limit (lossless work transfer). T_ref/T₀,k has no physical basis: for a heat resource at T_h, c = T_h/(T_h − T₀), which rises with T₀, opposite to (B).
- Confidence: high for the decomposition, medium for "(A) is closer".
- Falsifier: compute c_op/c_up for one real supply chain; if it tracks T_ref/T₀,op over 150–290 K, (B) is right.

**2. Entropy is commensurable as a physical tally; work is commensurable as a cost.**
- S_gen = ΔS_sys + Σ Q_out/T_boundary [J/K] does not depend on any dead-state choice and adds over disjoint control volumes.
- Its work price is local: W_lost,k = T₀,k · S_gen,k [J] (Gouy–Stodola), where T₀,k must be the reservoir that actually receives the heat.
- A joule of delivered work is the same resource anywhere, but lost work is not process-invariant: the same process in another environment loses different work.
- A resource question asks for the cost, so the J sum is the relevant one.
- Confidence: high.
- Falsifier: two identical resistors each dissipate 1 J from one battery, at 150 K and 300 K. Predicted battery draw is 1 J each, with S_gen = 6.67e-3 and 3.33e-3 J/K. A measured 2:1 draw falsifies the claim.

**3. (B) ranks wrongly for pure work dissipation.**
- One spacecraft, one battery. Design 1 dissipates 100 J in a 290 K phase: S = 100/290 = 0.345 J/K. Design 2 dissipates 60 J in a 150 K phase: S = 60/150 = 0.400 J/K.
- (B) prefers Design 1, which drains 67 % more from the same store. (A) ranks them correctly (100 J against 60 J).
- Cause: for dissipated work, W_lost = W regardless of T₀, while S_gen = W/T₀.
- Confidence: high.
- Falsifier: an energy balance showing the 290 K dissipation costs the battery less than 60 J.

**4. (A) ranks wrongly when delivered work costs differ between environments.**
- T₀,op = 150 K. Design 1: upstream 1000 MJ, operational lost work 10 MJ. Design 2: upstream 950 MJ, operational 50 MJ.
- (A) gives 1010 against 1000 MJ and prefers Design 2.
- If on-board work costs c_op = 3 J of primary exergy per J (an assumed value), the true cost is 1030 against 1100 MJ, so Design 1 is better. The break-even is c_op = 1.25.
- (B) gives 3.421 against 3.520 MJ/K and picks Design 1, but only by accident: its implicit rate is 1.99, unrelated to 3.
- Confidence: high for the arithmetic, medium for relevance, since c_op is mission-specific.
- Falsifier: show c_op ≤ 1.25 for the actual power chain.

**5. The flip condition is narrow and can be written down exactly.**
- Let ΔU and ΔO be the upstream and operational lost-work differences [J], and r = T_ref/T₀,op. (A) ranks by sign(ΔU + ΔO); (B) by sign(ΔU + r·ΔO).
- They disagree if and only if ΔU·ΔO < 0 and 1 < |ΔU|/|ΔO| < r.
- r = 1.028 at 290 K and 1.988 at 150 K.
- In every flipped case the margin under (A) satisfies |ΔU + ΔO| < (r − 1)·|ΔO|.
- Confidence: high.
- Falsifier: any one of the 5 % flipped random cases that violates the inequality.

**6. Cumulative exergy consumption divided by T_ref is not upstream entropy generation.**
- The balance is CExC = Ex_product + I_cumulative (Szargut; exact terminology UNSURE), with waste exergy counted as destroyed in the environment.
- So S_gen,up = (CExC − Ex_product)/T_ref [J/K]. Dividing all of CExC overstates it by Ex_product/T_ref.
- For aluminium, Ex_ch ≈ 33 MJ/kg (UNSURE, ±10 %), which is about 0.11 MJ/(kg·K). The bias is larger in fractional terms for fuels and polymers, and it does not cancel between designs with different materials or masses.
- T_ref is also a normalisation: real plants reject heat at site ambient.
- Confidence: medium.
- Falsifier: an exergy balance over one tabulated chain where CExC − Σ destruction ≈ 0 instead of ≈ Ex_product.

**7. Adding I_up/T_ref to operational S_gen is consistent bookkeeping but not a resource total.**
- Entropy is extensive, so the sum is legitimate, but it carries three defects.
- It weights joules by 1/T₀,k (claims 1 and 3).
- A spacecraft's "effective T₀" is a convention. For dissipated work, ∂ln S_gen/∂ln T₀ = −1, so choosing 150 K over 290 K scales the operational term by 1.93. The lost work itself is unchanged.
- The embodied Ex_product is destroyed later in another environment, where its exergy differs from the T_ref value.
- Confidence: medium-high.
- Falsifier: an operational S_gen that is insensitive to the T₀ convention for an electrically dominated loss budget.

**8. T₀,eval in (A) is a pure scale factor.**
- Σ_A = (1/T₀,eval) · Σ_k T₀,k · S_gen,k, so T₀,eval cannot change a ranking, and Σ_A is not an entropy generation unless every T₀,k = T₀,eval.
- If the implementation instead re-refers each loss as T₀,eval · S_gen,k, (A) collapses to (B).
- Confidence: high.
- Falsifier: rerun the random cases at two values of T₀,eval; any rank change means the code re-references losses.

**Verdict:** use (A) for the first edition, preferably reported in J, with T₀,eval stated as a scale only.
- Validity range: same functional unit; losses paid by work-like inputs of roughly equal delivered cost; each T₀,k the real heat-rejection reservoir; upstream term taken as CExC − Ex_product.
- Report (B) alongside as a diagnostic. Mark the result "undecided" whenever claim 5's inequality holds: an upstream-against-operation trade-off with ratio between 1 and T_ref/T₀,op, which is at most 1.99 at 150 K.
- Confidence: medium.

**Open points**
- c_k is not derived here. If the operational input is a free flux such as sunlight, operational lost work draws no stock and its cost sits in hardware already inside CExC, so adding it risks double counting.
- Chemical exergy in a non-Earth environment (reference composition, not only T₀) is undefined here, which leaves end-of-life destruction of Ex_product unsettled.
- Claims 6 and 7 rest on recalled forms of Szargut's balance and the aluminium figure; both need checking against a source.
