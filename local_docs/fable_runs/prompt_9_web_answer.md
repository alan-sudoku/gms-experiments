# Prompt 9: incumbent wearout (low-budget run, OQ-3)

Context file (`local_docs/`, never cited by the spec). Run 2026-11-15 per `local_docs/orchestration/fable_delegation_plan.md` §5.1, as a Fable agent (`fable`, effort high, no tools); input was the Prompt 9 block in `local_docs/fable_questions.md` verbatim. The reply below is saved as returned. Every claim is at level `derived`; an `opus` S5 checks it against GMS-100 (DEF-LIFECYCLE-SIDE-PROFILE, EQ-LIFECYCLE-REPLACEMENT-COUNT, EQ-LIFECYCLE-SIDE-IRREVERSIBILITY, EQ-LIFECYCLE-RETIRED-UNIT-EOL, REQ-LIFECYCLE-EOL-ALLOCATION, the costing boundary), OQ-9, OQ-19 and plan §6.3 and Q14.

Orchestrator note (2026-11-15): the "possible double count" in claim 2 comes from the block's wording, which listed "make-up of unrecovered x, remelt" next to "retired-unit EOL". In GMS-100, EQ-LIFECYCLE-RETIRED-UNIT-EOL already contains remelt of the recovered fraction and dispersal plus virgin make-up of the unrecovered fraction, so an R_s built by the spec's terms would count each once. S5 should check claim 2 against the spec, not the block.

---

No files read and nothing run; everything below is derived by hand (level `derived`). Notation: r_k = τ − m_k·τ_w,k (age of the unit in service, s); f_∞ = f with m_s = 0.

**1. τ_w,s = ∞ is not equal-function when τ_w,s < τ; it biases toward the incumbent and gives an upper bound on f.**
- f = f_∞ − Δ_s, with Δ_s = m_s·R_s + K_s·[m_s·√τ_w,s + √r_s − √τ] ≥ 0 (J/K), because √ is subadditive and R_s ≥ 0.
- So f_∞ < 0 means g wins for any incumbent life, with no R_s needed. If τ_w,s ≥ τ then m_s = 0 and Δ_s = 0, identical to ∞.
- "No outcome" for every finite τ_w,s is therefore over-strict. It is needed only when f_∞ ≥ 0, τ_w,s < τ and R_s is unavailable; otherwise evaluate with m_s > 0.
- Example: f = 4.4e6 − 2·R_s, so the verdict flips for R_s > 2.2e6 J/K.
- Confidence: high.
- Falsifier: any parameter set with R_s ≥ 0, K_s ≥ 0 and constant Σ̇_s where Σ_s(finite life) < Σ_s(∞).

**2. The boundary asymmetry stays one-sided in sign when both sides are replaced, but its size grows with m_s.**
- Σ_s,full − Σ_s,declared = ω_s,init + m_s(τ)·ω_s,rep ≥ 0 (J/K), where ω is the omitted stages per unit. "g wins" stays robust; "g loses" weakens as τ grows.
- Example: the declared boundary (R_s = 1.0e6) gives f = 2.4e6, "s wins, one-sided". It flips if ω_s,rep > 1.2e6 J/K, or > 0.8e6 J/K if the first unit omits the same stage.
- R_s = 2.5e6 with Σ_s,init unchanged is a mixed boundary (f = −0.6e6). Charging the first unit the same 1.5e6 gives f = 2.4e6 − 3·1.5e6 = −2.1e6.
- One-sidedness breaks only if an omitted stage is negative (a recovery credit) or a flow is counted twice.
- Possible double count: the example's R_s lists "make-up, remelt" and also "retired-unit EOL", which by the stated allocation already contains both. That would overstate Σ_s and favour g.
- Confidence: high on the sign; medium on whether the double count is real in the spec.
- Falsifier: an itemized R_s in which every physical flow appears once and the sum still equals the listed total.

**3. Minimal consistent rule for R_s.**
- R_s = (the recurring stages charged in Σ_s,init, applied to the restored stock) + retired-unit EOL (J/K). Use the same stage list for the first and replacement units; each flow once; no one-offs.
- Report the break-even omitted stage with every "g loses": ω* = f/(m_s + 1) (J/K per unit).
- "Same stages as R_g" is a best estimate with no robust direction, and is consistent only if Σ_s,init is raised too.
- Confidence: medium (this is a convention choice; the bound itself is high).
- Falsifier: a case where this rule gives f < 0 but a full symmetric inventory gives f ≥ 0.

**4. Wearout time is a given life for concave ageing (K·√a) and a chosen interval only for convex ageing (Σ̇ rising with age).**
- With loss rate σ(a) (W/K), the long-run rate is c(T) = [R + ∫₀ᵀ σ da]/T (W/K). It is stationary where σ(T*) = c(T*), that is ∫₀^T* a·σ′(a) da = R. (Renewal-reward / economic-life result; the form is derived here, UNSURE of textbook notation.)
- K·√a: the left side is −K·√T/2 < 0, so never replace voluntarily; τ_w = failure life.
- σ = σ₀ + β·a: T* = √(2R/β) (s). With both terms: β·T²/2 − K·√T/2 = R.
- Rule: τ_w,k = min(τ_fail,k, T*_k). The two differ iff T* < τ_fail.
- Over a finite τ, replacing at all pays iff R < β·τ²/4. The optimum is n* = argmin over n ≥ ceil(τ/τ_fail) of [(n−1)·R + n·L(τ/n)], with equal intervals (Jensen, L convex).
- The formula's "full lives plus remainder" schedule is not optimal for a chosen interval unless τ/τ_w is an integer.
- Confidence: high on the condition; medium on equal intervals when L mixes concave and convex parts.
- Falsifier: brute force over n = 1..10 and unequal splits for linear β.

**5. The same rule applies to both sides, with one safety asymmetry.**
- Σ_s must be costed at the incumbent's optimal schedule (a lower bound); Σ_g may use any feasible schedule (an upper bound). That keeps "g wins" robust.
- For a gradually degrading incumbent, τ_w,s = ∞ or run-to-failure overstates Σ_s by ∫ of the ageing loss minus the optimum. This favours g, which is the unsafe direction and reverses the bias of claim 1.
- Confidence: medium-high.
- Falsifier: an incumbent with β > 0 and R_s < β·τ²/4 where the unreplaced Σ_s ≤ the n = 2 value.

**6. The three-roots-per-segment bound survives two restarting clocks.**
- On a segment of the merged breakpoints, f = c₀ + c₁·τ + K_g·√(τ−a) − K_s·√(τ−b), with a = m_g·τ_w,g and b = m_s·τ_w,s.
- f″ = ¼[K_s·(τ−b)^(−3/2) − K_g·(τ−a)^(−3/2)] = 0 iff (τ−a)/(τ−b) = (K_g/K_s)^(2/3). The left side is monotone in τ, so there is at most one zero.
- Exception: a = b and K_g = K_s makes f linear, and f ≡ 0 on the segment is possible.
- There are at most m_g + m_s + 1 segments.
- New behaviour: −R_s jumps give downward sign changes with no root, and f′ → −∞ just after an incumbent restart. The solver must test the value at each breakpoint and its right limit, not only continuous roots.
- Confidence: high.
- Falsifier: a dense grid showing four sign changes inside one segment.

**7. Monotonicity survives for the present profile: a shorter τ_w,s never raises f.**
- d/dτ_w,s of the oxidation part = (K_s·m_s/2)·[τ_w,s^(−1/2) − r_s^(−1/2)] ≤ 0, since r_s ≤ τ_w,s. It is continuous where m_s changes, and m_s·R_s is a non-increasing step for R_s ≥ 0.
- So f_∞ = sup f, which is what makes claim 1 work.
- It fails for R_s < 0 or age-increasing Σ̇_s, where Σ_s is U-shaped in the interval (claim 4).
- Confidence: high.
- Falsifier: scan τ_w,s over (0, 2τ) and look for any rise in Σ_s.

**8. Tie convention and verdict.**
- Keep f left-continuous on both sides (a unit reaching τ_w exactly at τ is not replaced). The right-limit jump at a coincident breakpoint is R_g − R_s, of either sign.
- The g-wins set is closed at g-breakpoints and open at s-breakpoints; f = 0 retains the incumbent.
- ceil(τ/τ_w) at integer ratios is fragile in floating point. A spurious −R_s is in the unsafe direction, so compute m with a declared tolerance and flag "breakpoint-sensitive" when sign f(τ) ≠ sign f(τ⁺).
- **Verdict:** in a first edition, evaluate f with m_s from a given failure life on both sides, R_s by claim 3, and three outputs: g wins / g loses (one-sided, with ω*) / no outcome.
- Validity range: constant Σ̇_k, K_k ≥ 0, R_k ≥ 0, non-negative omitted stages.
- Forcing ∞ flips the verdict iff 0 ≤ f_∞ < Δ_s (in the example, R_s > 2.2e6 J/K). "No outcome" discards a determinate verdict whenever f_∞ < 0 or τ_w,s ≥ τ.
- Confidence: medium-high.
- Falsifier: an in-range case where the three-output rule says "g wins" and a full symmetric inventory says otherwise.

**Open points**
- Whether the spec's R_s really counts make-up and remelt twice (claim 2) could not be checked without reading it.
- For chosen intervals, the functional limit (performance threshold) that sets τ_fail for gradual degradation is undefined here, and so is the optimal schedule for mixed concave and convex ageing.
- No defensible upper bound on ω_s exists yet, so "s wins" can never be made robust, only reported with ω*.
