# Prompt 9 synthesis: incumbent wearout (OQ-3, plan Q4)

Context file (`local_docs/`, never cited by the spec). Orchestrator synthesis of `prompt_9_web_answer.md` (Fable, no tools) and `prompt_9_review.md` (`opus` S5), written 2026-11-15. Every result is at level `derived`; all example inputs are made up.

## Verdict

- **The answer's strongest result is claim 1, and the review proves it for the spec's profile.**
  - With a constant Σ̇_s, K_ox,s ≥ 0 and R_s ≥ 0, f evaluated with the incumbent never replaced (f_∞) is an upper bound on f for every incumbent life τ_wearout,s.
  - So f_∞ < 0 means the candidate wins whatever the incumbent's life, without knowing R_s.
  - A shorter τ_wearout,s never raises f (claim 7). This is the plan's Q14 argument applied to side s.
  - Under GMS-100's terms R_s ≥ 0: remelt is exergy destroyed, and CExC ≥ b_ch is a REQ.
- **GMS-100's "τ_wearout,s < ∞ → no outcome" row is over-strict.** It discards this determinate verdict, and it also discards the case τ_wearout,s ≥ τ, where m_s = 0 and the evaluation is exactly the τ_wearout,s = ∞ one.
- **The answer's own verdict for 0.1 is premature.** It proposed evaluating with m_s > 0, R_s by its claim 3, and a given failure life. In two regimes every alternative is wrong, and the answer's rule errs toward the candidate, which is the unsafe direction:
  - **Regime A, an incumbent whose loss rises with age, with a performance limit** (for example a catalyst whose overpotential rises). Truth: f = +1.5e6 J/K, the incumbent wins. τ_wearout,s = ∞ errs by −12.0e6, "no outcome" returns nothing, and the answer's rule errs by −3.0e6. GMS-100's profile cannot represent an age-increasing Σ̇, and every 0.1 mechanism has an age-independent Σ̇. So regime A arises only from a scenario-supplied incumbent such as the GMS-310 Part C catalyst.
  - **Regime C, GMS-230's upper bound on side s** (K_s√t where the real scale grows paralinearly). Truth: +0.27e6 J/K. τ_wearout,s = ∞ errs by −0.54e6, and the answer's rule by −4.72e6, because the bound then applies to every incumbent unit. The f_∞ rule inherits the −0.54e6 error, which the existing GMS-500 flag for "a candidate-wins verdict that rests on a combined-case term on side s" already covers.
- **R_s, once it is specified, has a clean form.** Read consistently with how R_g is built, R_s = M_s·b_transport/T₀ + Σ_s,EOL^ret. There is no double count; the one claim 2 raised came from the block's wording, as the orchestrator note said. A "candidate loses" verdict should report Ω* = f, the total omitted irreversibility that would flip it, not ω* = f/(m_s + 1).
- **Two of the answer's other claims need correcting:**
  - Claim 4's "τ_w = min(τ_fail, T*)" contradicts its own finite-horizon optimum. The correct rule is the argmin over the number of units n, with each interval at most the given life.
  - The three-roots-per-segment bound survives two restarting clocks, but plan §6.3 steps 1–2 do not carry over. After an incumbent restart, the inflection window needs K_g > K_s, and f′ → −∞ at the left end. The generalised test is sign D(L⁺) ≠ sign D(U⁻), with D = K_s²·α³ − K_g²·β³. It is needed only once m_s > 0 is evaluated.

Reviewer counts: 0 BLOCKER, 5 MAJOR, 8 MINOR. All 7 review scripts reproduce byte for byte (orchestrator re-run from `/`, 2026-11-15).

## Where the review disagrees with the answer

| Answer | Review | Orchestrator view |
|---|---|---|
| Verdict: evaluate with m_s > 0, R_s by claim 3, given failure life | Premature: unsafe in regimes A and C; the safe part is claim 1 | Agree; adopt only the f_∞ rule in 0.1 (D1) |
| Claim 2: possible double count in R_s | Not real under the spec's terms; it came from the block's wording | Agree; the orchestrator note said so |
| Claim 3: R_s = recurring Σ_s,init stages on restored stock + retired-unit EOL | Ambiguous; the consistent reading is transport + Σ_s,EOL^ret; report Ω* = f, not ω* | Agree (D2) |
| Claim 4: τ_w = min(τ_fail, T*) | Over a finite horizon it replaces too often (overstates Σ_s by 5.0 at R = 12): use the argmin over n | Agree; record in OQ-3 (D3) |
| Claim 6: three roots survive | Yes; plan §6.3 window and left-end rules do not | Agree; GMS-400 note for when m_s > 0 lands (D3) |
| Claim 8: tolerance on ceil(τ/τ_w) | Use integer ties (j, i), as in plan §6.3 step 5 | Agree (D3) |

## What it means for the spec

- **GMS-100 (accepted).** A small change before the tag, new correction E29:
  - The decision-table row "τ_wearout,s < ∞ → no outcome" is replaced. If τ_wearout,s ≥ τ, evaluate with m_s = 0 as now. If τ_wearout,s < τ, evaluate with m_s = 0 (f_∞): the candidate wins if f_∞ < 0; otherwise there is no outcome.
  - An assumption sentence gives the reason and the validity: Σ̇_s constant, K_ox,s ≥ 0, R_s ≥ 0.
  - The same restriction applies to E28's shared-infrastructure verdict. With τ_wearout,s < τ, its "incumbent wins" row becomes no outcome; its "candidate wins" row stays robust.
  - DEF-LIFECYCLE-SIDE-PROFILE says that the incumbent is evaluated without replacement and that a finite τ_wearout,s is used only by the decision rule.
  - EQ-LIFECYCLE-PARITY-FUNCTION's validity is widened from "τ_wearout,s = ∞".
  - The R_s Open item records the R_s form and Ω*.
- **No change to GMS-220, GMS-230 or the solver in 0.1.** GMS-220's sentences on side s ("τ_wearout,s = ∞ in this edition") should be aligned in its pending fix pass. GMS-230 is untouched. The GMS-500 combined-case flag already covers regime C under the f_∞ rule.
- **OQ-3 narrows** to the m_s > 0 evaluation and what it brings:
  - R_s;
  - GMS-230's side-s bound across units;
  - the chosen-interval branch for incumbents whose loss rises with age, with Rule W's t_perf as a constraint;
  - possibly 4 roots per segment with an age-linear term;
  - the GMS-400 generalisation.
- **GMS-310 Part C.** The Pt or Ir catalyst incumbent may be a regime-A case. The Part C brief must say whether its loss rises with age. If it does, GMS-100's profile cannot represent it, and the verdict needs the rising-loss branch (open) or a stated bound.

## Decisions for the user

| # | Decision | Options | Recommendation |
|---|---|---|---|
| D1 | Incumbent with a finite life (review finding 5) | (a) New correction E29 (GMS-100): replace the "τ_wearout,s < ∞ → no outcome" row with: τ_wearout,s ≥ τ → evaluate with m_s = 0; τ_wearout,s < τ → evaluate with m_s = 0, the candidate wins if f < 0, otherwise no outcome. Add the reason (f ≤ f_∞ when Σ̇_s is constant, K_ox,s ≥ 0, R_s ≥ 0). Apply the same restriction to REQ-LIFECYCLE-SHARED-INFRASTRUCTURE-VERDICT's "incumbent wins" row. DEF-LIFECYCLE-SIDE-PROFILE and the validity of EQ-LIFECYCLE-PARITY-FUNCTION follow. (b) The answer's verdict (evaluate with m_s > 0): unsafe in regimes A and C. (c) Leave as is | (a). It returns a determinate, safe verdict that is lost today, with no new symbol, no R_s and no solver change |
| D2 | R_s form for later (findings 6–8) | (a) Record in GMS-100's R_s Open item and in OQ-3: under the asymmetric boundary, R_s = M_s·b_transport/T₀ + Σ_s,EOL^ret (no double count); a "candidate loses" verdict with m_s > 0 reports Ω* = f. (b) Nothing | (a) |
| D3 | What stays open and brief notes | Rewrite OQ-3 (plan Q4 "open, narrowed"): m_s > 0 evaluation; side-s combined bound across units; chosen-interval branch (finite-horizon argmin over n with intervals ≤ min(τ_c, x_allow·t_c, t_perf), not min(τ_fail, T*)); 4 roots with an age-linear term (UNSURE); GMS-400 generalisation (inflection test D, left-end sign by restart type, integer (j, i) ties, Bounds corner R_s minimum and τ_wearout,s maximum). Brief notes: GMS-220 fix pass (align the side-s sentences with E29); GMS-310 Part C (state whether the incumbent catalyst's loss rises with age); GMS-240 (Rule W has no chosen-interval branch; out of scope for 0.1). Decisive check, added to OQ-3 as a Phase 6 item: a measured record of loss against unit age, with the industrial replacement interval, for the Part C oxygen-electrode catalyst | Adopt |
| D4 | Plan record | V19: Prompt 9 outcome (E29, OQ-3 narrowed, brief notes); Q4 row "open, narrowed" | Adopt |

## Cost

| Stage | Model | Time | Tokens | Tool calls |
|---|---|---|---|---|
| Fable stage (no tools) | `fable` high | 3 min | about 48k | 0 |
| S5 reviewer | `opus` high | 16 min | about 172k | 41 |
